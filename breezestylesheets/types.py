'''
types

Shared type hints for various modules.
'''

import typing

if typing.TYPE_CHECKING:
    import os  # noqa

JSONKey: 'typing.TypeAlias' = 'str'
JSONValue: 'typing.TypeAlias' = typing.Union['JSONPrimitive', 'JSONArray', 'JSONObject']
JSONPrimitive: 'typing.TypeAlias' = typing.Union[float, str, None]
JSONArray: 'typing.TypeAlias' = typing.Sequence[typing.Union['JSONPrimitive', 'JSONArray', 'JSONObject']]
JSONObject: 'typing.TypeAlias' = typing.Mapping[
    'JSONKey', typing.Union['JSONPrimitive', 'JSONArray', 'JSONObject']
]

PathOrStr: 'typing.TypeAlias' = 'str | os.PathLike[str]'
