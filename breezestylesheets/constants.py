'''
constants

Constant values and aliases for library definitions.
'''

import typing

Compression: 'typing.TypeAlias' = 'typing.Literal["zlib", "lzma", "gzip", "default"]'
'''The valid compression schemes for a QT resource.'''

Framework: 'typing.TypeAlias' = 'typing.Literal["pyqt5", "pyqt6", "pyside2", "pyside6"]'
'''The valid Qt frameworks (and Python wrappers) used for the stylesheets.'''
