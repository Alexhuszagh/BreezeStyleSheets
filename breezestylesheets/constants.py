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

DISABLED: 'dict[bool, Color]' = {
    True: Color('#454545'),
    False: Color('#6a6e71'),
}
'''The default color for a disabled item with a dark (true) or light (false) theme.'''

CRITICAL: 'dict[bool, Color]' = {
    True: Color('#80404a'),
    False: Color('#ff8c9f'),
}
'''The default color for a QMessageBox critical icon with a dark (true) or light (false) theme.'''

INFORMATION: 'dict[bool, Color]' = {
    True: Color('#406880'),
    False: Color('#8cd5ff'),
}
'''The default color for a QMessageBox information icon with a dark (true) or light (false) theme.'''

QUESTION: 'dict[bool, Color]' = {
    True: Color('#634d80'),
    False: Color('#c08cff'),
}
'''The default color for a QMessageBox question icon with a dark (true) or light (false) theme.'''

WARNING: 'dict[bool, Color]' = {
    True: Color('#99995C'),
    False: Color('#ffff8c'),
}
'''The default color for a QMessageBox warning icon with a dark (true) or light (false) theme.'''
