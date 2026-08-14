"""Utilities for working with QStyles."""

from typing import TYPE_CHECKING

from .cli import Args
from .qt import PyQt

if TYPE_CHECKING:
    from .typing import QtGui, QtWidgets


def style_icon(
    style: "QtWidgets.QStyle",
    qt: "PyQt",
    standard: "dict[QtWidgets.QStyle.StandardPixmap, str]",
    args: "Args",
    icon: "QtWidgets.QStyle.StandardPixmap",
    option: "QtWidgets.QStyleOption | None" = None,
    widget: "QtWidgets.QWidget | None" = None,
) -> "QtGui.QIcon":
    """Apply a custom style to a standard icon."""

    if args.stylesheet.name == "native":
        return style.standardIcon(icon, option, widget)

    resource = f"{args.stylesheet.resources}{standard[icon]}"
    if qt.QtCore.QFile.exists(resource):
        return qt.QtGui.QIcon(resource)

    return qt.QtWidgets.QCommonStyle.standardIcon(style, icon, option, widget)  # type: ignore
