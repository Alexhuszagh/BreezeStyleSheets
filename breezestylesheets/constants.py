'''
constants

Constant values and aliases for library definitions.
'''

import typing

from pydantic_extra_types.color import Color

Compression: 'typing.TypeAlias' = 'typing.Literal["zlib", "lzma", "gzip", "default"]'
'''The valid compression schemes for a QT resource.'''

Framework: 'typing.TypeAlias' = 'typing.Literal["pyqt5", "pyqt6", "pyside2", "pyside6"]'
'''The valid Qt frameworks (and Python wrappers) used for the stylesheets.'''

DARK_DISABLED: 'Color' = Color('#454545')
'''The default color for a disabled item with a dark theme.'''

LIGHT_DISABLED: 'Color' = Color('#6a6e71')
'''The default color for a disabled item with a light theme.'''
