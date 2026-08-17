from typing import TYPE_CHECKING, Any

from example._util.style import style_icon
from .cli import ARGS, STANDARD_ICONS, Qt

if TYPE_CHECKING:
    from example._util.typing import QtWidgets


class StandardIconStyle(Qt.QtWidgets.QCommonStyle):
    """A custom application style overriding standard icons."""

    style: "QtWidgets.QStyle"

    def __init__(self, style: "QtWidgets.QStyle") -> None:
        super().__init__()
        self.style = style
        style.standardIcon

    def __getattribute__(self, item: str) -> Any:
        """
        Override for standardIcon. Everything else should default to the
        system default. We cannot have `style_icon` be a member of
        `StandardIconStyle`, since this will cause an infinite recursive loop.
        """
        if item == "standardIcon":
            return lambda *x: style_icon(self, Qt, STANDARD_ICONS, ARGS, *x)
        return getattr(object.__getattribute__(self, "style"), item)
