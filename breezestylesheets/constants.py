"""Constant values and aliases for library definitions."""

from typing import TYPE_CHECKING

from .pydantic.color import NullableColor

if TYPE_CHECKING:
    from typing import Literal

    Compression = Literal["zlib", "lzma", "gzip", "default"]
    """The valid compression schemes for a QT resource."""

    Framework = Literal["pyqt5", "pyqt6", "pyside2", "pyside6"]
    """The valid Qt frameworks (and Python wrappers) used for the stylesheets."""

DISABLED: "dict[bool, NullableColor]" = {
    True: NullableColor("#454545"),
    False: NullableColor("#6a6e71"),
}
"""The default color for a disabled item with a dark (true) or light (false) theme."""

CRITICAL: "dict[bool, NullableColor]" = {
    True: NullableColor("#80404a"),
    False: NullableColor("#ff8c9f"),
}
"""The default color for a QMessageBox critical icon with a dark (true) or light (false) theme."""

INFORMATION: "dict[bool, NullableColor]" = {
    True: NullableColor("#406880"),
    False: NullableColor("#8cd5ff"),
}
"""The default color for a QMessageBox information icon with a dark (true) or light (false) theme."""

QUESTION: "dict[bool, NullableColor]" = {
    True: NullableColor("#634d80"),
    False: NullableColor("#c08cff"),
}
"""The default color for a QMessageBox question icon with a dark (true) or light (false) theme."""

WARNING: "dict[bool, NullableColor]" = {
    True: NullableColor("#99995C"),
    False: NullableColor("#ffff8c"),
}
"""The default color for a QMessageBox warning icon with a dark (true) or light (false) theme."""
