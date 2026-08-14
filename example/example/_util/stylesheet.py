"""Utilities for normalizing and processing stylesheets."""

from typing import TYPE_CHECKING, cast

import importlib
import logging

from ..theme import Theme, get_theme
from .qt import PyQt

if TYPE_CHECKING:
    from .typing import QtWidgets

logger = logging.getLogger("breezestylesheets:example")


class Stylesheet:
    """Abstraction around a stylesheet type."""

    name: str

    def __init__(self, name: "str | Stylesheet") -> None:
        if isinstance(name, str):
            self.name = name
            self._normalize()
        else:
            self.name = name.name

    @property
    def resources(self) -> str:
        """Get the resource format for the Qt application."""
        return f":/{self.name}/"

    @property
    def path(self) -> str:
        """Get the Qt resource path to the stylesheet."""
        return f"{self.resources}stylesheet.qss"

    def read(self, qt: PyQt) -> str:
        """Read the contents of the stylesheet."""
        file = qt.QtCore.QFile(self.path)
        flag = qt.QtCore.QFile.OpenModeFlag.ReadOnly | qt.QtCore.QFile.OpenModeFlag.Text
        file.open(flag)
        stream = qt.QtCore.QTextStream(file)
        return stream.readAll()

    def _normalize(self) -> None:
        """Normalize the stylesheet, removing and normalizing any aliases."""

        # now we need to normalize our theme. we don't use Qt6 features
        # so we can differentiate between light/dark/unknown.
        if self.name.startswith("auto"):
            theme = get_theme()
            if theme == Theme.DARK:
                self.name = self.name.replace("auto", "dark", 1)
            elif theme == Theme.LIGHT:
                self.name = self.name.replace("auto", "light", 1)
            else:
                logger.warning("Unknown an unknown system theme, falling back to the system native theme.")
                self.name = "native"

        # Needed so we remove any aliases. See #106.
        if self.name in ("dark", "light"):
            self.name += "-blue"

    def load(self, qt: PyQt) -> None:
        """Load the stylesheet from the Qt resource bundle."""

        package = f"breeze_{qt.framework}"
        submodule = self.__module__.rsplit(".", maxsplit=1)[0]
        importlib.import_module(f"{submodule}.styles.{package}")

    def apply(self, qt: PyQt) -> None:
        """Apply the stylesheet to the application."""

        if self.name == "native":
            return
        app = cast("QtWidgets.QApplication | None", qt.QtWidgets.QApplication.instance())
        if app is None:
            raise RuntimeError("Must initialize the application prior to setting the stylesheet.")

        app.setStyleSheet(self.read(qt))
