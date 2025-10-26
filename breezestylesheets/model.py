"""
model

Simple, dependency-free model for data serialization and loading.
"""

import typing
import io
import json
import os.path
import sys
from contextlib import contextmanager
from collections import abc as typing_abc
from dataclasses import Field, dataclass

from . import exception, types, utils

if typing.TYPE_CHECKING:
    import typing_extensions as typing_ext


__all__ = ['Model', 'model']

# TODO: Fix `typing_extensions` if possible... I guess it's required for 3.9
Alias: 'typing_ext.TypeAlias' = 'tuple[str, ...]'
T = typing.TypeVar('T', bound='Model')
Callable = typing.TypeVar('Callable', bound='typing_abc.Callable')


def _dataclass_transform(**kwds: typing.Any) -> typing_abc.Callable[[T], T]:
    def decorator(t: T) -> T:
        return t
    return decorator


if typing.TYPE_CHECKING:
    dataclass_transform = typing.dataclass_transform
else:
    dataclass_transform = _dataclass_transform


# TODO: FIXME: We need to ensure we use this correctly
class FieldMetadata(typing.TypedDict):
    """The aliases for the field."""

    name: 'typing_ext.NotRequired[str]'
    """The primary alias, that is, what the field is serialized as."""

    aliases: 'typing_ext.NotRequired[set[str]]'
    """The additional aliases, which are valid when loading data."""

    required: 'typing_ext.NotRequired[bool]'
    """
    If the field is required from the input data.

    Note that default fields should be provided using the standard
    dataclass syntax.
    """


class Schema(dict[str, type]):
    """
    A custom schema for validating data.

    This is a mapping of the **field name** to the type, which might
    have a `foreground` or `foreground_hover` format, and the resolved
    type to parse the data as. The actual primary key for the field can
    be found via `FieldMetadata.name`.
    """

    def __repr__(self) -> str:
        # TODO: Fix this, better format the types
        return super().__repr__()


def expand_aliases(value: 'str') -> 'Alias':
    """Expand foreground and other choices to create all permutations of our choices."""

    # NOTE: This takes the `.` and `foreground`/`background` syntax, which expands this
    # TODO: Fix this!
    result = set()
    result.add(value)
    result.add(value.replace('foreground', 'fg'))
    result.add(value.replace('background', 'bg'))
    result.add(value.replace('alternate', 'alt'))
    updated: list[str] = []
    if '.' not in value:
        updated += [f'{i}.default' for i in result]
        updated += [f'{i}:default' for i in result]
        updated += [f'{i}-default' for i in result]
    else:
        updated += [i.replace('.', ':') for i in result]
        updated += [i.replace('.', '-') for i in result]
    result.update(updated)

    return tuple(sorted(result))


def field_metadata(name: 'str', *rest: str, required: bool = False) -> 'FieldMetadata':
    """Get the alias choices from the expanded values."""
    expanded = expand_aliases(name) + rest
    return FieldMetadata(name=name, aliases=set(expanded), required=required)


class Dataclass(typing.Protocol):
    """An class that implements the dataclass protocol."""

    __dataclass_fields__: typing.ClassVar[dict[str, Field]]


class Validator(typing.Generic[T]):
    """
    A custom dataclass validator, which lazily evaluates and the types
    and resolves any forward references to create a type loader.

    This does model validation upon loading, as well as field transformation,
    to ensure all types have been properly resolved (to avoid forward reference
    issues) so the field transformation can be done properly.

    Attributes:
        model (`type[Model]`): The model type to validate the data for.
    """

    __slots__ = ('model', '_schema', '_callback')
    model: 'type[T]'
    _schema: Schema
    _callback: typing_abc.Callable[[typing.Any], T]

    def __init__(self, model: 'type[T]') -> None:
        """
        Args:
            model (`type[Model]`): The model type to validate the data for.
        """
        self.model = model
        self._schema = self._create_schema(model)
        self._callback = self._create_validator(model, self._schema)

    def validate(self, data: typing.Any) -> T:
        """
        Validate the data against the model.

        Args:
            data: (`any`): The data to validate against the model.

        Returns:
            `Model`: The loaded model, after validation.

        Raises:
            `ValueError`: If the data does not match the model schema.
        """
        try:
            return self._callback(data)
        except (ValueError, TypeError) as error:
            schema = repr(self._schema)
            raise ValueError(f'Unable to validate "{data}" against schema "{schema}"') from error

    @staticmethod
    def _create_schema(model: 'type[Model]') -> Schema:
        """
        Create the type schema from the model, resolving any forward references.

        This does not expand any aliases.
        """

        schema = Schema()
        module = model.__module__
        for field, info in model.__dataclass_fields__.items():
            dtype = info.type
            if isinstance(dtype, (str, typing.ForwardRef)):
                dtype = types.evaluate_forward_ref(
                    dtype,
                    globalns=sys.modules.get(module).__dict__,
                    localns=model.__dict__,
                    module=module,
                    is_class=True,
                )
            if dtype is None:
                raise TypeError(f'Got an invalid value type for field "{field}".')

            schema[field] = dtype

        return schema

    @staticmethod
    def _create_validator(
        model: 'type[T]',
        schema: Schema,
    ) -> typing_abc.Callable[[typing.Any], T]:
        """
        Create the validator for the model type.

        This validates and loads the data from the model type and the
        schema. This resolves any aliases and correctly handles any
        missing fields present in the mapping.
        """

        aliases = model.aliases

        def validate(data: typing.Any) -> T:
            """
            The custom validator, which validates the desired data and loads it
            to the desired data types. This will use a custom loader, if present,
            otherwise, it will use the default constructor.
            """

            if not isinstance(data, typing_abc.Mapping):
                raise TypeError(F'Expected mapping, got "{data}".')
            if not all([isinstance(i, str) for i in data]):
                raise ValueError(f'All keys must be strings for data "{data}".')

            loaded = {}
            mapped = {aliases[k]: v for k, v in data.items() if k in aliases}
            extras = {k: v for k, v in data.items() if k not in aliases}
            if extras and model.unknown == 'raise':
                raise ValueError(f'Got unexpected: expected "{aliases.keys()}", got "{extras.keys()}".')

            for key, value in mapped.items():
                dtype = schema[key]
                loader = getattr(dtype, '__breeze_load__', dtype)
                loaded[key] = loader(value)

            # NOTE: these have no known loaders
            result = model(**loaded)
            if extras and model.unknown == 'include':
                for key, value in extras.items():
                    setattr(result, key, value)

            return result

        return validate


class Model(Dataclass):
    """The base, dependency-free loadable model that supports field aliases"""

    # TODO: This needs a type adaptor too!
    # This can be the validator!

    __slots__ = ()

    unknown: typing.ClassVar[typing.Literal['include', 'ignore', 'raise']] = 'raise'
    """
    TODO: Document!
    """

    @utils.lazy_attribute
    @classmethod
    def keys(cls) -> typing_abc.Collection[str]:
        """Get the name of all primary keys within the model."""
        return [v.metadata.get('name', k) for k, v in cls.__dataclass_fields__.items()]

    @utils.lazy_attribute
    @classmethod
    def aliases(cls) -> typing_abc.Mapping[str, str]:
        """
        Get all aliases associated with the class.

        This caches the stored aliases for all resolved values,
        and then computes them to their desired values, allowing
        efficient lookups of instance values from the alias.

        ```python
        {
            'foreground': 'foreground',
            'fg': 'foreground',
            'fg-default': 'foreground',
            'fg.default': 'foreground',
            'fg:default': 'foreground',
            'foreground-default': 'foreground',
        }
        ```

        Returns:
            `dict`: The mapping of all the aliases to the field names.
        """

        # NOTE: Do not `update` so we avoid overwriting existing fields.
        result: dict[str, str] = {}
        for field, info in cls.__dataclass_fields__.items():
            meta = typing.cast(FieldMetadata, info.metadata)
            result.setdefault(meta.get('name', field), field)
            aliases: set[str] = meta.get('aliases', set())
            for alias in aliases:
                result.setdefault(alias, field)

        return result

    @utils.lazy_attribute
    @classmethod
    def _validator(cls: type['typing_ext.Self']) -> Validator['typing_ext.Self']:
        """Get the custom validator for the class."""
        # NOTE: Model validator creation is expensive: cache this
        return Validator(cls)

    @classmethod
    def validate(cls: type['typing_ext.Self'], data: typing.Any) -> 'typing_ext.Self':
        """
        Validate the data against the model.

        Args:
            data: (`any`): The data to validate against the model.

        Returns:
            `Model`: The loaded model, after validation.

        Raises:
            `ValueError`: If the data does not match the model schema.
        """
        return cls._validator.validate(data)

    def get(self, alias: str) -> typing.Any:
        """
        Get a single attribute by the field alias.

        Args:
            alias (`str`): The name of the alias or field to get, such as `foreground`.

        Returns:
            `Any`: The value of that field.

        Raises:
            `ValueError`: If the provided alias is not valid.
        """
        field = self.aliases.get(alias)
        if field is None:
            raise ValueError(f'Got an unknown alias "{alias}".')
        return getattr(self, field)

    @classmethod
    def load(cls: type['typing_ext.Self'], path: 'types.PathOrStr') -> 'typing_ext.Self':
        """
        Load the stylesheet configuration settings from file.

        This adds the default configuration settings and validates
        the loaded settings are valid. This supports JSON, YAML, TOML,
        and XML file formats.

        Args:
            path (`str`, `Path`): The path to the file to load.

        Returns:
            `Model`: The loaded stylesheet configuration settings.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the configuration data.
        """
        with parse_block(path=path):
            with open(path, encoding='utf-8') as file:
                return cls.loads(file.read(), os.path.splitext(os.path.basename(path))[1])

    @classmethod
    def loads(
        cls: type['typing_ext.Self'], s: 'str | bytes | bytearray', extension: 'str'
    ) -> 'typing_ext.Self':
        """
        Load the stylesheet configuration settings from a document.

        This adds the default configuration settings and validates
        the loaded settings are valid. This supports JSON, YAML, TOML,
        and XML file formats.

        Args:
            s (`str`, `bytes`, `bytearray`): The document data, as a string or UTF-8 encoded bytes.
            extension (str): The extension of the file (to determine the file type).

        Returns:
            `Model`: The loaded stylesheet configuration settings.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the configuration data.
        """
        with parse_block(data=s):
            return cls.validate(transform_nested(loads_model(s, extension)))


@contextmanager
def parse_block(
    data: 'str | bytes | bytearray | None' = None,
    path: 'types.PathOrStr | None' = None,
    exc_type: type[exception.ParseError] = exception.ParseError,
) -> 'typing_abc.Iterator[None]':
    """A helper to parse the config data within a context block."""
    try:
        yield
    except exception.ParseError as error:
        error.path = error.path or path
        raise
    except Exception as error:
        if data is None and path is None:
            raise ValueError('Must provide either the data or the path.') from error
        if data is None:
            assert path is not None
            with open(path, encoding='utf-8') as file:
                data = file.read()
        raise exc_type(str(error), data, path, error) from error


@typing.overload
def model(cls: type[T], /) -> type[T]: ...


@typing.overload
def model(
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> 'typing_abc.Callable[[type[T]], type[T]]': ...


@dataclass_transform()
def model(
    cls: type[T] | None = None,
    /,
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
) -> 'type[T] | typing_abc.Callable[[type[T]], type[T]]':
    """
    Create a new model, with logic to serialize and deserialize fields.

    This currently mostly identical to `dataclass`, but it's implemented as
    a separate method to ensure MRO, better type hinting, and future API
    considerations.

    Args:
        init (`bool`): If to implement an `__init__` method, if one does not exist.
        repr (`bool`): If to implement an `__repr__` method, if one does not exist.
        eq (`bool`): If to implement an `__eq__` method, if one does not exist.
        order (`bool`): If to implement total ordering on the class.
        unsafe_hash (`bool`): Force the model to create a `__hash__` method,
            even if the field contents may be mutable, if one does not exist.
        frozen (`bool`): If assigning to fields will raise an exception.

    Returns:
        `T`: The model type, with loaders and aliases on the class defined.
    """

    def wrap(cls: type[T]) -> type[T]:
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

    # pylint: disable-next=arguments-differ
    def decode(self, s: 'str') -> 'types.JSONValue':  # type: ignore # noqa
        """Return the Python representation of s (a str instance containing a JSON document)."""
        lines = s.splitlines()
        lines = [i for i in lines if not i.strip().startswith('//')]
        return typing.cast('types.JSONValue', super().decode('\n'.join(lines)))


def loads_model(s: 'str | bytes | bytearray', extension: 'str') -> types.JSONObject:
    """Load an object from a document."""
    value = loads(s, extension)
    if not isinstance(value, typing_abc.Mapping):
        raise ValueError(f'Got an invalid parsed model type of "{type(value).__name__}".')
    return typing.cast(types.JSONObject, value)


def loads(s: 'str | bytes | bytearray', extension: 'str') -> typing.Any:
    """Load values from a document."""
    # NOTE: Migrate to `match` with 3.10+ support.
    if extension in ('.json', '.jsonc'):
        return loads_json(s)
    elif extension in ('.yml', '.yaml'):
        return loads_yaml(s)
    elif extension == '.toml':
        return loads_toml(s)
    elif extension == '.xml':
        return loads_xml(s)
    raise ValueError(f'Got an unknown file type of "{extension}".')


def loads_json(s: 'str | bytes | bytearray') -> typing.Any:
    """Load values from a JSON document."""
    return json.loads(decode(s), cls=CommentsDecoder)


def loads_yaml(s: 'str | bytes | bytearray') -> typing.Any:
    """Load values from a YAML document."""

    # pylint: disable-next=import-error
    import yaml  # type: ignore # noqa

    return yaml.safe_load(io.StringIO(decode(s)))


def loads_toml(s: 'str | bytes | bytearray') -> typing.Any:
    """Load values from a TOML document."""

    try:
        # pylint: disable-next=import-error
        import tomllib  # type # noqa
    except ImportError:
        # pylint: disable-next=import-error
        import tomli as tomllib  # type: ignore # noqa

    return tomllib.loads(decode(s))


def loads_xml(s: 'str | bytes | bytearray') -> typing.Any:
    """Load values from an XML document."""

    # pylint: disable-next=import-error
    import xml2dict  # type: ignore # noqa

    return xml2dict.parse(decode(s))


def decode(s: 'str | bytes | bytearray') -> str:
    """Decode the value to string as UTF-8."""
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('utf-8')
    return s


def transform_nested(v: 'types.JSONObject') -> dict[str, str]:
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

    result: dict[str, str] = {}
    for key, value in v.items():
        if not isinstance(key, str) or not isinstance(value, (str, typing_abc.Mapping)):
            raise ValueError(f'Expected JSON value to be str or mapping, got "{type(value)}".')
        if isinstance(value, str):
            result[key] = value
        elif isinstance(value, typing_abc.Mapping):
            nested = transform_nested(value)
            for subkey, subvalue in nested.items():
                result[f'{key}:{subkey}'] = subvalue

    return result
