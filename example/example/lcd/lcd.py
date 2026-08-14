from typing import TYPE_CHECKING

from .cli import ARGS, COLORS, Qt

if TYPE_CHECKING:
    from PyQt6 import QtWidgets


class LCD(Qt.QtWidgets.QLCDNumber):
    """QLCDNumber with a custom palette."""

    def __init__(self, widget: "QtWidgets.QWidget | None" = None) -> None:
        super().__init__(widget)
        self.setContentsMargins(1, 1, 1, 1)
        if ARGS.stylesheet.name == "native":
            return

        # The color of the non-flat LCD numbers is still controlled
        # via the `color` stylesheet attribute.
        r, g, b, a = COLORS.highlight_dark
        color = (r, g, b, a / 255)
        self.setStyleSheet(f"QLCDNumber {{ color: rgba{color}; }}")

        palette = self.palette()
        background = Qt.QtGui.QColor(*COLORS.background)
        selected = Qt.QtGui.QColor(*COLORS.selected)
        notch = Qt.QtGui.QColor(*COLORS.notch)
        palette.setColor(Qt.QtGui.QPalette.ColorRole.Window, background)
        palette.setColor(Qt.QtGui.QPalette.ColorRole.Light, selected)
        palette.setColor(Qt.QtGui.QPalette.ColorRole.Dark, notch)
        self.setPalette(palette)
