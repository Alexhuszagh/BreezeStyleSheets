"""
Simple, dependency-free model for data serialization and loading.

This aims to support archaic versions of Python, and so older aliases
are used wherever possible, but make it compatible with modern type
checkers.
"""

from collections.abc import Callable, Collection, Iterator, Mapping
from typing import TYPE_CHECKING, Dict, ForwardRef, Generic, TypeVar, cast, overload

import io
import json
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from importlib.util import find_spec

from . import exception, utils
from .types import Dataclass, dataclass_transform, evaluate_forward_ref

if TYPE_CHECKING:
    from typing import Any, ClassVar, Literal, Self, TypedDict

    from pathlib import Path

    from .types import JSONObject, JSONValue, Loads


__all__ = ["EXTENSIONS", "Model", "model"]

ModelT = TypeVar("ModelT", bound="Model")


if TYPE_CHECKING:
    Alias = tuple[str, ...]  # type: ignore


if TYPE_CHECKING:

    class FieldMetadata(TypedDict, total=False):
        """The serialized name and other field metadata."""

        name: "str"
        """The name the field is serialized as."""

        required: "bool"
        """
        If the field is required from the input data.

        Note that default fields should be provided using the standard
        dataclass syntax.
        """

else:
    FieldMetadata = dict


EXTENSIONS: "set[str]" = {".json", ".jsonc"}
"""The support theme and icon file extensions based on the installed extensions."""

if find_spec("yaml") is not None:
    EXTENSIONS.update((".yml", ".yaml"))
if find_spec("tomllib") is not None or find_spec("tomli") is not None:
    EXTENSIONS.add(".toml")
if find_spec("xml2dict") is not None:
    EXTENSIONS.add(".xml")


class Schema(Dict["str", "type"], Generic[ModelT]):
    """
    A custom schema for validating data.

    This is a mapping of the **field name** to the type, which might
    have a `foreground` or `foreground_hover` format, and the resolved
    type to parse the data as. The actual primary key for the field can
    be found via `FieldMetadata.name`.
    """

    model_type: "type[ModelT]"
    """The type of the model used to generate the schema."""

    def __init__(self, model_type: "type[ModelT]") -> None:
        """Initialize the schema with the model type."""
        self.model_type = model_type

    def __repr__(self) -> "str":
        names = {k: f"{v.__module__}{v.__name__}" for k, v in self.items()}
        return repr(f"Schema({names})")


def field_metadata(name: "str", required: "bool" = False) -> "FieldMetadata":
    """Create the field metadata from the components."""
    return FieldMetadata(name=name, required=required)


class Validator(Generic[ModelT]):
    """
    A custom dataclass validator, which lazily evaluates and the types
    and resolves any forward references to create a type loader.

    This does model validation upon loading, as well as field transformation,
    to ensure all types have been properly resolved (to avoid forward reference
    issues) so the field transformation can be done properly.
    """

    __slots__ = ("model", "_schema", "_callback")

    model: "type[ModelT]"
    """The model type to validate the data for."""

    _schema: "Schema[ModelT]"
    _callback: "Callable[[Any], ModelT]"

    def __init__(self, model: "type[ModelT]") -> "None":
        """
        Args:
            model: The model type to validate the data for.
        """
        self.model = model
        self._schema = self._create_schema(model)
        self._callback = self._create_validator(model, self._schema)

    def validate(self, data: "Any") -> "ModelT":
        """
        Validate the data against the model.

        Args:
            data: The data to validate against the model.

        Returns:
            The loaded model, after validation.

        Raises:
            `ValueError`: If the data does not match the model schema.
        """
        try:
            return self._callback(data)
        except (ValueError, TypeError) as error:
            schema = repr(self._schema)
            raise ValueError(f'Unable to validate "{data}" against schema "{schema}"') from error

    @staticmethod
    def _create_schema(model: "type[ModelT]") -> "Schema[ModelT]":
        """Create the type schema from the model, resolving any forward references."""

        schema = Schema(model)
        module = model.__module__
        for field, info in model.__dataclass_fields__.items():
            dtype = info.type
            if isinstance(dtype, (str, ForwardRef)):
                dtype = evaluate_forward_ref(
                    dtype,
                    globalns=sys.modules.get(module).__dict__,
                    localns=dict(model.__dict__),
                    module=module,
                    is_class=True,
                )
            if dtype is None:
                raise TypeError(f'Got an invalid value type for field "{field}".')

            schema[field] = dtype

        return schema

    @staticmethod
    def _create_validator(
        model: "type[ModelT]",
        schema: "Schema[ModelT]",
    ) -> "Callable[[Any], ModelT]":
        """
        Create the validator for the model type.

        This validates and loads the data from the model type and the
        schema. This maps the field names and correctly handles any
        missing fields present in the mapping.
        """

        fields = model.fields

        def validate(data: "dict[str, Any]") -> "ModelT":
            """
            The custom validator, which validates the desired data and loads it
            to the desired data types. This will use a custom loader, if present,
            otherwise, it will use the default constructor.
            """

            if not isinstance(data, Mapping):
                raise TypeError(f'Expected mapping, got "{data}".')
            if not all(isinstance(i, str) for i in data):
                raise ValueError(f'All keys must be strings for data "{data}".')

            loaded: "dict[str, Model]" = {}
            mapped = {fields[k]: v for k, v in data.items() if k in fields}
            extras = {k: v for k, v in data.items() if k not in fields}
            if extras and model.unknown == "raise":
                raise ValueError(f'Got unexpected: expected "{fields.keys()}", got "{extras.keys()}".')

            for key, value in mapped.items():
                dtype = schema[key]
                loader = cast("type", getattr(dtype, "__breeze_load__", dtype))
                loaded[key] = cast("Model", loader(value))

            # NOTE: these have no known loaders
            result = model(**loaded)
            if extras and model.unknown == "include":
                for key, value in extras.items():
                    setattr(result, key, value)

            return result

        return validate


class Model(Dataclass):
    """The base, dependency-free loadable model that supports mapped field names."""

    __slots__ = ()

    unknown: "ClassVar[Literal['include', 'ignore', 'raise']]" = "raise"
    """
    How to handle unexpected keys when deserializing data.

    The valid values are:
    - `include`: add to the deserialized model.
    - `ignore`: exclude from the deserialized model.
    - `raise`: throw if any extra keys are found.
    """

    @utils.lazy_attribute
    @classmethod
    def keys(cls) -> "Collection[str]":
        """Get the name of all primary keys within the model."""
        return [v.metadata.get("name", k) for k, v in cls.__dataclass_fields__.items()]

    @utils.lazy_attribute
    @classmethod
    def fields(cls) -> "Mapping[str, str]":
        """
        Get all fields associated with the class.

        This caches the serialized names to the model field names.

        ```python
        {
            'foreground': 'foreground',
            'foreground:light': 'foreground_light',
            'background': 'background',
            'background:alternate': 'background_alternate',
        }
        ```

        Returns:
            The mapping of all the data to the field names.
        """

        # NOTE: Do not `update` so we avoid overwriting existing fields.
        result: dict[str, str] = {}
        for field, info in cls.__dataclass_fields__.items():
            meta = cast(FieldMetadata, info.metadata)
            result.setdefault(meta.get("name", field), field)

        return result

    @utils.lazy_attribute
    @classmethod
    def _validator(cls: "type[Self]") -> "Validator[Self]":
        """Get the custom validator for the class."""
        # NOTE: Model validator creation is expensive: cache this
        return Validator(cls)

    @classmethod
    def validate(cls: "type[Self]", data: "Any") -> "Self":
        """
        Validate the data against the model.

        Args:
            data: The data to validate against the model.

        Returns:
            The loaded model, after validation.

        Raises:
            `ValueError`: If the data does not match the model schema.
        """
        return cls._validator.validate(data)  # type: ignore[arg-type]

    def get(self, field: "str") -> "Any":
        """
        Get a single attribute by the field name.

        Args:
            field: The name of field to get, such as `foreground`.

        Returns:
            The value of that field.

        Raises:
            `ValueError`: If the provided field is not valid.
        """
        try:
            return getattr(self, self.fields[field])
        except (AttributeError, KeyError):
            raise ValueError(f'Got an unknown alias "{field}".') from None

    @classmethod
    def load(cls: "type[Self]", path: "Path") -> "Self":
        """
        Load the stylesheet configuration settings from file.

        This adds the default configuration settings and validates
        the loaded settings are valid. This supports JSON, YAML, TOML,
        and XML file formats.

        Args:
            path: The path to the file to load.

        Returns:
            The loaded stylesheet configuration settings.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the configuration data.
        """
        with parse_block(path=path):
            return cls.loads(path.read_text(encoding="utf-8"), path.suffix)

    @classmethod
    def loads(cls: "type[Self]", s: "Loads", extension: "str") -> "Self":
        """
        Load the stylesheet configuration settings from a document.

        This adds the default configuration settings and validates
        the loaded settings are valid. This supports JSON, YAML, TOML,
        and XML file formats.

        Args:
            s: The document data, as a string or UTF-8 encoded bytes.
            extension: The extension of the file (to determine the file type).

        Returns:
            The loaded stylesheet configuration settings.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the configuration data.
        """
        with parse_block(data=s):
            return cls.validate(transform_nested(loads_model(s, extension)))

    # NOTE: Aliases for a Pydantic-like API.
    model_load = validate
    model_load_json = load


@contextmanager
def parse_block(
    data: "Loads | None" = None,
    path: "Path | None" = None,
    exc_type: "type[exception.ParseError]" = exception.ParseError,
) -> "Iterator[None]":
    """A helper to parse the config data within a context block."""
    try:
        yield
    except exception.ParseError as error:
        error.path = error.path or path
        raise
    except Exception as error:
        if data is None and path is None:
            raise ValueError("Must provide either the data or the path.") from error
        if data is None:
            assert path is not None
            with open(path, encoding="utf-8") as file:
                data = file.read()
        raise exc_type(str(error), data, path, error) from error


@overload
def model(cls: "type[ModelT]") -> "type[ModelT]": ...


@overload
def model(
    *,
    init: "bool" = True,
    repr: "bool" = True,
    eq: "bool" = True,
    order: "bool" = False,
    unsafe_hash: "bool" = False,
    frozen: "bool" = False,
) -> "Callable[[type[ModelT]], type[ModelT]]": ...


@dataclass_transform()
def model(
    cls: "type[ModelT] | None" = None,
    *,
    init: "bool" = True,
    repr: "bool" = True,
    eq: "bool" = True,
    order: "bool" = False,
    unsafe_hash: "bool" = False,
    frozen: "bool" = False,
) -> "type[ModelT] | Callable[[type[ModelT]], type[ModelT]]":
    """
    Create a new model, with logic to serialize and deserialize fields.

    This currently mostly identical to `dataclass`, but it's implemented as
    a separate method to ensure MRO, better type hinting, and future API
    considerations.

    This is meant to have validation as part of the design, but without
    any dependencies so the compiled resources can be generated for C++
    as well as being used on-the-fly as a Python dependency.

    Args:
        init: If to implement an `__init__` method, if one does not exist.
        repr: If to implement an `__repr__` method, if one does not exist.
        eq: If to implement an `__eq__` method, if one does not exist.
        order: If to implement total ordering on the class.
        unsafe_hash: Force the model to create a `__hash__` method,
            even if the field contents may be mutable, if one does not exist.
        frozen: If assigning to fields will raise an exception.

    Returns:
        The model type, with loaders and mapped field names on the class defined.
    """

    def wrap(cls: "type[ModelT]") -> "type[ModelT]":
        if not issubclass(cls, Model):
            raise TypeError(f'Class "{cls}" must be a subclass of `Model`.')
        wrapped = dataclass(
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
        )
        return wrapped(cls)

    if cls is None:
        return wrap

    return wrap(cls)


class CommentsDecoder(json.JSONDecoder):
    """
    A custom decoder that removes simple comments from the JSON input.

    This removes only lines starting with `//`.
    """

    def decode(self, s: "str") -> "JSONValue":  # type: ignore
        """Return the Python representation of s (a str instance containing a JSON document)."""
        lines = s.splitlines()
        lines = [i for i in lines if not i.strip().startswith("//")]
        return cast("JSONValue", super().decode("\n".join(lines)))


def loads_model(s: "Loads", extension: "str") -> "JSONObject":
    """Load an object from a document."""
    value = loads(s, extension)
    if not isinstance(value, Mapping):
        raise ValueError(f'Got an invalid parsed model type of "{type(value).__name__}".')
    return cast("JSONObject", value)


def loads(s: "Loads", extension: "str") -> "Any":
    """Load values from a document."""
    # NOTE: Migrate to `match` with 3.10+ support.
    if extension not in EXTENSIONS:
        raise ValueError(f'Got an unknown file type of "{extension}".')
    if extension in (".json", ".jsonc"):
        return loads_json(s)
    if extension in (".yml", ".yaml"):
        return loads_yaml(s)
    if extension == ".toml":
        return loads_toml(s)
    if extension == ".xml":
        return loads_xml(s)
    raise ValueError(f'Got an unknown file type of "{extension}".')


def loads_json(s: "Loads") -> "Any":
    """Load values from a JSON document."""
    return json.loads(decode(s), cls=CommentsDecoder)


def loads_yaml(s: "Loads") -> "Any":
    """Load values from a YAML document."""

    import yaml  # type: ignore # noqa

    return yaml.safe_load(io.StringIO(decode(s)))


def loads_toml(s: "Loads") -> "Any":
    """Load values from a TOML document."""

    try:
        import tomllib  # type: ignore # noqa
    except ImportError:
        import tomli as tomllib  # type: ignore # noqa

    return tomllib.loads(decode(s))


def loads_xml(s: "Loads") -> "Any":
    """Load values from an XML document."""

    import xml2dict  # type: ignore # noqa

    return xml2dict.parse(decode(s))


def decode(s: "Loads") -> "str":
    """Decode the value to string as UTF-8."""
    if isinstance(s, (bytes, bytearray)):
        s = s.decode("utf-8")
    return s


def transform_nested(v: "JSONObject") -> "dict[str, str]":
    """
    Transform nested keys in a JSON object to `key.nested` syntax.

    This simplifies a query format popular in tools like JQ or Json.NET.

    For example, given the following JSON:

    ```json
    {
        "b": 1,
        "a": {
            "c": 2,
            "d": null
        }
    }
    ```

    This would be transformed to the equivalent JSON of:

    ```json
    {
        "b": 1,
        "a.c": 2,
        "a.d": null
    }
    ```

    This is, of course, a lossy operation and if any keys have a `.` in them
    that overlaps with a nested field, they will be overwritten.
    """

    result: "dict[str, str]" = {}
    for key, value in v.items():
        if not isinstance(key, str) or not isinstance(value, (str, Mapping)):
            raise ValueError(f'Expected JSON value to be str or mapping, got "{type(value)}".')
        if isinstance(value, str):
            result[key] = value
        elif isinstance(value, Mapping):
            nested = transform_nested(value)
            for subkey, subvalue in nested.items():
                result[f"{key}:{subkey}"] = subvalue

    return result
