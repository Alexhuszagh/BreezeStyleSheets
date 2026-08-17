"""
Compatibility definitions between Qt versions.

Made a separate module for strongly-typed definitions.
This creates compat definitions consistent with PyQt6.
"""

from typing import TYPE_CHECKING, cast
from typing_extensions import override

import abc
import os
import sys
from functools import cached_property

from ..theme import Theme, get_theme

if TYPE_CHECKING:
    from breezestylesheets.constants import Framework  # type: ignore

    from .cli import Args
    from .typing import QtCore as _QtCore
    from .typing import QtGui as _QtGui
    from .typing import QtWidgets as _QtWidgets


class PyQtExec:
    """Compatibility wrapper for an executable Qt object."""

    obj: "_QtCore.QCoreApplication | _QtWidgets.QDialog"

    def __init__(self, obj: "_QtCore.QCoreApplication | _QtWidgets.QDialog") -> None:
        self.obj = obj

    def exec(self) -> int:
        """Execute the main application."""

        f = getattr(self.obj, "exec_", None)
        if f is None:
            f = getattr(self.obj, "exec", None)
        if f is None:
            raise TypeError("Unable to find a suitable `exec` method.")

        return f()


class PyQtMenu:
    """Compatibility layer for a menu."""

    obj: "_QtWidgets.QMenu"

    def __init__(self, obj: "_QtWidgets.QMenu") -> None:
        self.obj = obj

    def exec(self, pos: "_QtCore.QPoint", at: "_QtGui.QAction | None" = None) -> "_QtGui.QAction | None":
        """Execute the menu."""

        f = getattr(self.obj, "exec_", None)
        if f is None:
            f = getattr(self.obj, "exec", None)
        if f is None:
            raise TypeError("Unable to find a suitable `exec` method.")

        return f(pos, at)


class PyQtApplication(PyQtExec):
    """Compatibility wrapper for Qt applications."""

    obj: "_QtCore.QCoreApplication"  # type: ignore

    def __init__(self, app: "_QtCore.QCoreApplication") -> None:
        super().__init__(app)

    def start(self, window: "_QtWidgets.QMainWindow") -> None:
        """Start and execute the application and window."""
        window.show()
        if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
            self.obj.quit()
        else:
            self.exec()


class PyQtPosition:
    """A wrapper for a single point event."""

    event: "_QtGui.QSinglePointEvent"

    def __init__(self, event: "_QtGui.QSinglePointEvent") -> None:
        self.event = event

    def position(self) -> "_QtCore.QPoint":
        """Get the single point position for the event."""
        try:
            return self.event.position().toPoint()
        except AttributeError:
            return self.event.pos()  # type: ignore


class PyQt(abc.ABC):
    """
    Compatibility definitions between Qt versions.

    This modifies the Qt5 APIs to match the Qt6 ones, wherever possible.
    """

    _theme: "Theme | None"

    def __init__(self) -> None:
        self._theme = None

    @staticmethod
    def _to_version(version: "int") -> "tuple[int, int, int]":
        # QT_VERSION is stored in 0xMMmmpp, each in 8 bit pairs.
        # Goes major, minor, patch. 393984 is "6.3.0"
        return (version >> 16, (version >> 8) & 0xFF, version & 0xFF)

    @property
    @abc.abstractmethod
    def framework(self) -> "Framework": ...

    @cached_property
    @abc.abstractmethod
    def version(self) -> "tuple[int, int, int]": ...

    @cached_property
    @abc.abstractmethod
    def QtCore(self) -> "_QtCore._QtCore": ...  # ruff: ignore[invalid-function-name]

    @cached_property
    @abc.abstractmethod
    def QtGui(self) -> "_QtGui._QtGui": ...  # ruff: ignore[invalid-function-name]

    @cached_property
    @abc.abstractmethod
    def QtWidgets(self) -> "_QtWidgets._QtWidgets": ...  # ruff: ignore[invalid-function-name]

    @classmethod
    def from_framework(cls: "type[PyQt]", framework: "Framework") -> "PyQt":
        if framework == "pyqt5":
            return _PyQt5()
        if framework == "pyqt6":
            return _PyQt6()
        if framework == "pyside2":
            return _PySide2()
        if framework == "pyside6":
            return _PySide6()
        raise ValueError(f"Got an invalid framework value of '{framework}'.")

    def create_application(
        self,
        args: "Args",
        unknown: "list[str]",
        style_class: "type[_QtWidgets.QStyle] | None" = None,
        window_class: "type[_QtWidgets.QMainWindow] | None" = None,
    ) -> "tuple[_QtWidgets.QApplication, _QtWidgets.QMainWindow]":
        """
        Setup and create a new instance of the Qt application.

        Args:
            args: The parsed command-line arguments.
            unknown: Additional, unknown arguments passed to the CLI.
            style_class: A custom subclass of `QStyle` to use.
            window_class:  A custom subclass of `QMainWindow` to use.

        Returns:
            The instantiated Qt application and the main window for the UI.
        """

        if args.scale != 1:
            os.environ["QT_SCALE_FACTOR"] = str(args.scale)
        else:
            os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

        app = cast("_QtWidgets.QApplication | None", self.QtWidgets.QApplication.instance())
        is_initial = app is None
        if app is None:
            app = self.QtWidgets.QApplication(sys.argv[:1] + unknown)
            # NOTE: Need to detect if the style is dark mode here
            _ = self.get_theme()
        if args.style != "native":
            style = self.QtWidgets.QStyleFactory.create(args.style)
            if style_class is not None:
                style = style_class(style)  # type: ignore
            app.setStyle(style)

        if window_class is None:
            window_class = self.QtWidgets.QMainWindow
        window = window_class()

        # only need to override the font on the first run
        if not is_initial:
            # use the default font size
            font = app.font()
            if args.font_size > 0:
                font.setPointSizeF(args.font_size)
            if args.font_family:
                font.setFamily(args.font_family)
            app.setFont(font)

        return app, window

    def get_theme(self, reinitialize: bool = False) -> Theme:
        """Determine if the system theme is in dark mode."""

        if self._theme is not None and not reinitialize:
            return self._theme

        app = cast("_QtWidgets.QApplication", self.QtWidgets.QApplication.instance())
        if app is None:
            raise RuntimeError("Must initialize the global application prior to getting dark mode.")

        if self.version >= (6, 5, 0):
            style_hints = app.styleHints()
            assert style_hints is not None
            color_scheme = style_hints.colorScheme()
            theme_cls = color_scheme.__class__
            if color_scheme == theme_cls.Unknown:
                self._theme = Theme.UNKNOWN
            elif color_scheme == theme_cls.Light:
                self._theme = Theme.LIGHT
            else:
                self._theme = Theme.DARK
        else:
            self._theme = get_theme()

        return self._theme

    def _migrate_qt5(self) -> None:
        """Migrate type definitions that migrated from Qt5 to Qt6."""

        # Changes to QtCore: https://doc.qt.io/qt-6/qtcore-changes-qt6.html
        # Changes to QtGui: https://doc.qt.io/qt-6/gui-changes-qt6.html
        # Changes to QtWidgets: https://doc.qt.io/qt-6/widgets-changes-qt6.html
        self.QtGui.QAction = self.QtWidgets.QAction  # type: ignore
        self.QtGui.QActionGroup = self.QtWidgets.QActionGroup  # type: ignore
        self.QtGui.QFileSystemModel = self.QtWidgets.QFileSystemModel  # type: ignore
        self.QtGui.QUndoCommand = self.QtWidgets.QUndoCommand  # type: ignore
        self.QtGui.QUndoStack = self.QtWidgets.QUndoStack  # type: ignore
        self.QtGui.QUndoGroup = self.QtWidgets.QUndoGroup  # type: ignore

    @property
    def standard_icons(self) -> "dict[_QtWidgets.QStyle.StandardPixmap, str]":
        """Create a map of standard icons to resource paths."""

        from .icons import get_standard_icons

        return get_standard_icons(self)


class _PyQt5(PyQt):
    """Compatibility definitions for PyQt5."""

    def __init__(self):
        from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

        super().__init__()
        self._QtCore = QtCore
        self._QtGui = QtGui
        self._QtWidgets = QtWidgets
        self._migrate_qt5()

    @property
    @override
    def framework(self) -> "Framework":
        return "pyqt5"

    @cached_property
    @override
    def version(self) -> "tuple[int, int, int]":
        return self._to_version(self._QtCore.QT_VERSION)

    @cached_property
    @override
    def QtCore(self) -> "_QtCore._QtCore":
        return cast("_QtCore._QtCore", self._QtCore)

    @cached_property
    @override
    def QtGui(self) -> "_QtGui._QtGui":
        return cast("_QtGui._QtGui", self._QtGui)

    @cached_property
    @override
    def QtWidgets(self) -> "_QtWidgets._QtWidgets":
        return cast("_QtWidgets._QtWidgets", self._QtWidgets)


class _PyQt6(PyQt):
    """Compatibility definitions for PyQt6."""

    def __init__(self):
        from PyQt6 import QtCore, QtGui, QtWidgets  # type: ignore

        super().__init__()
        self._QtCore = QtCore
        self._QtGui = QtGui
        self._QtWidgets = QtWidgets

    @property
    @override
    def framework(self) -> "Framework":
        return "pyqt6"

    @cached_property
    @override
    def version(self) -> "tuple[int, int, int]":
        return self._to_version(self._QtCore.QT_VERSION)

    @cached_property
    @override
    def QtCore(self) -> "_QtCore._QtCore":
        return cast("_QtCore._QtCore", self._QtCore)

    @cached_property
    @override
    def QtGui(self) -> "_QtGui._QtGui":
        return cast("_QtGui._QtGui", self._QtGui)

    @cached_property
    @override
    def QtWidgets(self) -> "_QtWidgets._QtWidgets":
        return cast("_QtWidgets._QtWidgets", self._QtWidgets)


class _PySide2(PyQt):
    """Compatibility definitions for PySide2."""

    def __init__(self):
        from PySide2 import QtCore, QtGui, QtWidgets  # type: ignore

        super().__init__()
        self._QtCore = QtCore
        self._QtGui = QtGui
        self._QtWidgets = QtWidgets
        self._migrate_qt5()

    @property
    @override
    def framework(self) -> "Framework":
        return "pyside2"

    @cached_property
    @override
    def version(self) -> "tuple[int, int, int]":
        return self._QtCore.__version_info__[:3]  # type: ignore

    @cached_property
    @override
    def QtCore(self) -> "_QtCore._QtCore":
        return cast("_QtCore._QtCore", self._QtCore)

    @cached_property
    @override
    def QtGui(self) -> "_QtGui._QtGui":
        return cast("_QtGui._QtGui", self._QtGui)

    @cached_property
    @override
    def QtWidgets(self) -> "_QtWidgets._QtWidgets":
        return cast("_QtWidgets._QtWidgets", self._QtWidgets)


class _PySide6(PyQt):
    """Compatibility definitions for PySide6."""

    def __init__(self):
        from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore

        super().__init__()
        self._QtCore = QtCore
        self._QtGui = QtGui
        self._QtWidgets = QtWidgets

    @property
    @override
    def framework(self) -> "Framework":
        return "pyside6"

    @cached_property
    @override
    def version(self) -> "tuple[int, int, int]":
        return self._QtCore.__version_info__[:3]  # type: ignore

    @cached_property
    @override
    def QtCore(self) -> "_QtCore._QtCore":
        return cast("_QtCore._QtCore", self._QtCore)

    @cached_property
    @override
    def QtGui(self) -> "_QtGui._QtGui":
        return cast("_QtGui._QtGui", self._QtGui)

    @cached_property
    @override
    def QtWidgets(self) -> "_QtWidgets._QtWidgets":
        return cast("_QtWidgets._QtWidgets", self._QtWidgets)
