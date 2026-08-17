"""
Shared type hints for various modules.

This aims for full backwards compatible for legacy types, and therefore
complete support for the earliest type checking (Python 3.4).
"""

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Union

import sys

__all__ = [
    "Dataclass",
    "JSONKey",
    "JSONValue",
    "JSONPrimitive",
    "JSONArray",
    "JSONObject",
    "dataclass_transform",
]

if TYPE_CHECKING:
    from typing import Any, ForwardRef

    JSONKey = str
    JSONValue = Union["JSONPrimitive", "JSONArray", "JSONObject"]
    JSONPrimitive = Union["float", "str", "None"]
    JSONArray = Sequence[Union["JSONPrimitive", "JSONArray", "JSONObject"]]
    JSONObject = Mapping["JSONKey", "JSONValue"]


def _identity(**kwds):
    def decorator(t):
        return t

    return decorator


if not TYPE_CHECKING:
    dataclass_transform = _identity
    Dataclass = object
    Loads = type
else:
    from typing import ClassVar, Protocol, dataclass_transform

    from dataclasses import Field

    Loads = str | bytes | bytearray

    class Dataclass(Protocol):
        """An class that implements the dataclass protocol."""

        __dataclass_fields__: "ClassVar[dict[str, Field]]"


def evaluate_forward_ref(
    ref: "ForwardRef | str",
    globalns: "dict[str, Any]",
    localns: "dict[str, Any] | None" = None,
    *,
    is_argument: "bool" = True,
    module: "str | None" = None,
    is_class: "bool" = False,
) -> type:
    """
    Evaluate a forward reference to the raw type.

    This aims to be Python version-generic, due to the numerous
    changes prior to Python 3.14 for the "private" API.

    This is only used on modern Python versions, that is, >=3.7.4.

    Args:
        ref: The forward reference to evaluate.
        globalns: The global namespace where the reference was defined.
        localns: The local namespace where the reference was defined.
        is_argument: If the type was provided as an argument.
        module: The module the type was defined in.
        is_argument: If the type is a class.

    Returns:
        The evaluated type.
    """

    if sys.version_info < (3, 7, 4):
        raise RuntimeError("Attempting to evaluating a forward reference for Python <3.7.4.")

    from typing import ForwardRef

    if isinstance(ref, str):
        if sys.version_info >= (3, 11):
            ref = ForwardRef(ref, is_argument=is_argument, module=module, is_class=is_class)
        elif sys.version_info >= (3, 10):
            ref = ForwardRef(ref, is_argument=is_argument, module=module)
        else:
            ref = ForwardRef(ref, is_argument=is_argument)

    if sys.version_info >= (3, 14):
        from typing import evaluate_forward_ref

        result = evaluate_forward_ref(
            forward_ref=ref,
            globals=globalns,
            locals=localns,
            type_params=None,
        )
    elif sys.version_info >= (3, 13):
        result = ref._evaluate(
            globalns,
            localns,
            type_params=(),
            recursive_guard=frozenset(),
        )
    elif sys.version_info >= (3, 9):
        result = ref._evaluate(
            globalns,
            localns,
            recursive_guard=frozenset(),
        )
    else:
        result = ref._evaluate(globalns, localns)

    if not isinstance(result, type):
        class_name = type(result).__name__
        msg = f'Expected an reference that evaluated to type for "{ref}", got "{class_name}".'
        raise TypeError(msg)
    return result
