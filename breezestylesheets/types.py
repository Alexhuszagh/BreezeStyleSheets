"""
types

Shared type hints for various modules.
"""

import typing
import os
import sys
from collections import abc as typing_abc

JSONKey: 'typing.TypeAlias' = 'str'
JSONValue: 'typing.TypeAlias' = typing.Union['JSONPrimitive', 'JSONArray', 'JSONObject']
JSONPrimitive: 'typing.TypeAlias' = typing.Union[float, str, None]
JSONArray: 'typing.TypeAlias' = typing_abc.Sequence[typing.Union['JSONPrimitive', 'JSONArray', 'JSONObject']]
JSONObject: 'typing.TypeAlias' = typing_abc.Mapping[
    'JSONKey', typing.Union['JSONPrimitive', 'JSONArray', 'JSONObject']
]

PathOrStr: 'typing.TypeAlias' = typing.Union[str, os.PathLike[str]]


def evaluate_forward_ref(
    ref: 'typing.ForwardRef | str',
    globalns: dict[str, typing.Any],
    localns: dict[str, typing.Any] | None = None,
    *,
    is_argument: bool = True,
    module: str | None = None,
    is_class: bool = False,
) -> type:
    """
    Evaluate a forward reference to the raw type.

    This aims to be Python version-generic, due to the numerous
    changes prior to Python 3.14 for the "private" API.

    Args:
        ref: The forward reference to evaluate.
        globalns: The global namespace where the reference was defined.
        localns: The local namespace where the reference was defined.
        is_argument: If the type was provided as an argument.
        module: The module the type was defined in.
        is_argument: If the type is a class.

    Returns:
        `type`: The evaluated type.
    """
    if isinstance(ref, str):
        ref = typing.ForwardRef(ref, is_argument=is_argument, module=module, is_class=is_class)

    if sys.version_info >= (3, 14, 0):
        result = typing.evaluate_forward_ref(
            forward_ref=ref,
            globals=globalns,
            locals=localns,
            type_params=None,
        )
    elif sys.version_info >= (3, 13, 0):
        result = ref._evaluate(
            globalns,
            localns,
            type_params=(),
            recursive_guard=frozenset(),
        )
    else:
        result = ref._evaluate(
            globalns,
            localns,
            recursive_guard=frozenset(),
        )

    if not isinstance(result, type):
        class_name = type(result).__name__
        msg = f'Expected an reference that evaluated to type for "{ref}", got "{class_name}".'
        raise TypeError(msg)
    return result
