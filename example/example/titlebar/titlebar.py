from collections.abc import Callable
from typing import TYPE_CHECKING, cast
from typing_extensions import TypeAlias, override

import enum
import os
import sys
from pathlib import Path

from example._util.assertions import nonnull
from example._util.qt import PyQtExec, PyQtMenu, PyQtPosition
from example._util.style import style_icon
from .cli import ARGS, COLORS, STANDARD_ICONS, Qt

if TYPE_CHECKING:
    from example._util.typing import QtCore, QtGui, QtWidgets

# 100ms between repaints, so we avoid over-repainting.
# Allows us to avoid glitchy motion during drags.
REPAINT_TIMER = 100
TRACK_TIMER = 4
# Make the titlebar size too large, so we can get the real value with min.
TITLEBAR_HEIGHT = 2**16
# QWIDGETSIZE_MAX isn't exported, which is needed to remove fixedSize constraints.
QWIDGETSIZE_MAX = (1 << 24) - 1

# Determine the Linux display server protocol we're using.
# Use `XDG_SESSION_TYPE`, since we can override it for X11.
IS_WAYLAND = os.environ.get("XDG_SESSION_TYPE") == "wayland"
IS_XWAYLAND = os.environ.get("XDG_SESSION_TYPE") == "xwayland"
IS_X11 = os.environ.get("XDG_SESSION_TYPE") == "x11"
# We can run X11 on Wayland, but this doesn't support certain
# features like mouse grabbing, so we don't use it here.
IS_TRUE_WAYLAND = "WAYLAND_DISPLAY" in os.environ
USE_WAYLAND_FRAME = IS_WAYLAND and not ARGS.wayland_testing


class MinimizeLocation(enum.IntEnum):
    """Location where to place minimized widgets."""

    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3


class WindowEdge(enum.IntEnum):
    """Enumerations for window edge positions."""

    NoEdge = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    TopLeft = 5
    TopRight = 6
    BottomLeft = 7
    BottomRight = 8


Edges: TypeAlias = "tuple[WindowEdge, WindowEdge, WindowEdge]"
MINIMIZE_LOCATION: MinimizeLocation = getattr(MinimizeLocation, ARGS.minimize_location)
TOP_EDGES: Edges = (WindowEdge.Top, WindowEdge.TopLeft, WindowEdge.TopRight)
BOTTOM_EDGES: Edges = (WindowEdge.Bottom, WindowEdge.BottomLeft, WindowEdge.BottomRight)
LEFT_EDGES: Edges = (WindowEdge.Left, WindowEdge.TopLeft, WindowEdge.BottomLeft)
RIGHT_EDGES: Edges = (WindowEdge.Right, WindowEdge.TopRight, WindowEdge.BottomRight)


def standard_icon(widget: "QtWidgets.QWidget", icon: "QtWidgets.QStyle.StandardPixmap") -> "QtGui.QIcon":
    """Get a standard icon."""
    style = widget.style()
    assert style is not None
    return style_icon(style, Qt, STANDARD_ICONS, ARGS, icon, widget=widget)


def menu_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the menu icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarMenuButton)


def minimize_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the minimize icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarMinButton)


def maximize_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the maximize icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarMaxButton)


def restore_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the restore icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarNormalButton)


def help_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the help icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarContextHelpButton)


def shade_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the shade icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarShadeButton)


def unshade_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the unshade icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarUnshadeButton)


def close_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Get the close icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton)


def transparent_icon(widget: "QtWidgets.QWidget") -> "QtGui.QIcon":
    """Create a transparent icon."""
    _ = widget
    return Qt.QtGui.QIcon()


def action(
    text: str,
    parent: "QtWidgets.QWidget | None" = None,
    icon: "QtGui.QIcon | None" = None,
    checkable: "bool | None" = None,
) -> "QtGui.QAction":
    """Create a custom QAction."""

    value = Qt.QtGui.QAction(text, parent)
    if icon is not None:
        value.setIcon(icon)
    if checkable is not None:
        value.setCheckable(checkable)

    return value


# UI WIDGETS
# These are just to populate the views: these could be anything.


class LargeTable(Qt.QtWidgets.QTableWidget):
    """Table with a large number of elements."""

    def __init__(self, parent: "QtWidgets.QWidget | None" = None) -> None:
        super().__init__(parent)

        self.setColumnCount(100)
        self.setRowCount(100)
        for index in range(100):
            row = Qt.QtWidgets.QTableWidgetItem(f"Row {index + 1}")
            self.setVerticalHeaderItem(index, row)
            column = Qt.QtWidgets.QTableWidgetItem(f"Column {index + 1}")
            self.setHorizontalHeaderItem(index, column)


class SortableTree(Qt.QtWidgets.QTreeWidget):
    """Tree with checkboxes and a sort indicator on the header."""

    def __init__(self, parent: "QtWidgets.QWidget | None" = None) -> None:
        super().__init__(parent)

        self.item0 = Qt.QtWidgets.QTreeWidgetItem(self)
        self.item1 = Qt.QtWidgets.QTreeWidgetItem(self)
        self.item2 = Qt.QtWidgets.QTreeWidgetItem(self.item1)
        self.item2.setText(0, "subitem")
        self.item3 = Qt.QtWidgets.QTreeWidgetItem(self.item2, ["Row 2.1"])
        self.item3.setFlags(self.item3.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        self.item3.setCheckState(0, Qt.QtCore.Qt.CheckState.Unchecked)
        self.item4 = Qt.QtWidgets.QTreeWidgetItem(self.item2, ["Row 2.2"])
        self.item5 = Qt.QtWidgets.QTreeWidgetItem(self.item4, ["Row 2.2.1"])
        self.item6 = Qt.QtWidgets.QTreeWidgetItem(self.item5, ["Row 2.2.1.1"])
        self.item7 = Qt.QtWidgets.QTreeWidgetItem(self.item5, ["Row 2.2.1.2"])
        self.item3.setFlags(self.item7.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        self.item7.setCheckState(0, Qt.QtCore.Qt.CheckState.Checked)
        self.item8 = Qt.QtWidgets.QTreeWidgetItem(self.item2, ["Row 2.3"])
        self.item8.setFlags(self.item8.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserTristate)
        self.item8.setCheckState(0, Qt.QtCore.Qt.CheckState.PartiallyChecked)
        self.item9 = Qt.QtWidgets.QTreeWidgetItem(self, ["Row 3"])
        self.item10 = Qt.QtWidgets.QTreeWidgetItem(self.item9, ["Row 3.1"])
        self.item11 = Qt.QtWidgets.QTreeWidgetItem(self, ["Row 4"])

        nonnull(self.headerItem()).setText(0, "qdz")
        self.setSortingEnabled(False)
        nonnull(self.topLevelItem(0)).setText(0, "qzd")
        nonnull(self.topLevelItem(1)).setText(0, "effefe")
        self.setSortingEnabled(True)


class SettingTabs(Qt.QtWidgets.QTabWidget):
    """Sample setting widget with a tab view."""

    def __init__(self, parent: "QtWidgets.QWidget | None" = None) -> None:
        super().__init__(parent)

        self.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
        self.general = Qt.QtWidgets.QWidget()
        self.addTab(self.general, "General")
        self.addTab(Qt.QtWidgets.QWidget(), "Colors")
        self.general_layout = Qt.QtWidgets.QGridLayout(self.general)
        self.general_layout.setColumnStretch(3, 10)
        for row in range(1, 10):
            self.general_layout.setRowStretch(row, 1)
        self.general_layout.setRowStretch(7, 10)

        # Add the data folder hboxlayout
        self.general_layout.addWidget(Qt.QtWidgets.QLabel("Data Folder"), 0, 0)
        self.data_folder = Qt.QtWidgets.QLineEdit(str(Path.home()))
        self.general_layout.addWidget(self.data_folder, 0, 1, 1, 3)
        self.file_dialog = Qt.QtWidgets.QPushButton("...")
        self.file_dialog.setCheckable(False)
        self.general_layout.addWidget(self.file_dialog, 0, 4)
        self.file_dialog.clicked.connect(lambda _: self.launchFiledialog(self.data_folder))

        # Add default font.
        app = cast("QtWidgets.QApplication", Qt.QtWidgets.QApplication.instance())
        self.general_layout.addWidget(Qt.QtWidgets.QLabel("Default Font"), 1, 0)
        self.font_value = Qt.QtWidgets.QLineEdit(app.font().family())
        self.general_layout.addWidget(self.font_value, 1, 1, 1, 3)
        self.font_dialog = Qt.QtWidgets.QPushButton("...")
        self.font_dialog.setCheckable(False)
        self.general_layout.addWidget(self.font_dialog, 1, 4)
        self.font_dialog.clicked.connect(lambda _: self.launchFontdialog(self.font_value))

        # Add item label font
        self.general_layout.addWidget(Qt.QtWidgets.QLabel("Item Label Font"), 2, 0)
        self.item_label_value = Qt.QtWidgets.QLineEdit(app.font().family())
        self.general_layout.addWidget(self.item_label_value, 2, 1, 1, 3)
        self.item_label_dialog = Qt.QtWidgets.QPushButton("...")
        self.item_label_dialog.setCheckable(False)
        self.general_layout.addWidget(self.item_label_dialog, 2, 4)
        self.item_label_dialog.clicked.connect(lambda _: self.launchFontdialog(self.item_label_value))

        # Add the "Show Grid" QCheckbox.
        self.grid = Qt.QtWidgets.QCheckBox("Show grid", self.general)
        self.general_layout.addWidget(self.grid, 3, 2, 1, 1)

        # Grid square size.
        self.grid_size = Qt.QtWidgets.QLabel("Grid Square Size", self.general)
        self.general_layout.addWidget(self.grid_size, 4, 0, 1, 2)
        self.grid_spin = Qt.QtWidgets.QSpinBox(self.general)
        self.grid_spin.setValue(16)
        self.general_layout.addWidget(self.grid_spin, 4, 2, 1, 1)

        # Add units of measurement
        self.units = Qt.QtWidgets.QLabel("Default length unit of measurement", self.general)
        self.general_layout.addWidget(self.units, 5, 0, 1, 2)
        self.units_combo = Qt.QtWidgets.QComboBox()
        self.units_combo.addItem("Inches")
        self.units_combo.addItem("Foot")
        self.units_combo.addItem("Meter")
        self.general_layout.addWidget(self.units_combo, 5, 2, 1, 1)

        # Add the alignment options
        self.align_combo = Qt.QtWidgets.QComboBox()
        self.align_combo.addItem("Align Top")
        self.align_combo.addItem("Align Bottom")
        self.align_combo.addItem("Align Left")
        self.align_combo.addItem("Align Right")
        self.align_combo.addItem("Align Center")
        self.general_layout.addWidget(self.align_combo, 6, 0, 1, 2)
        self.word_wrap = Qt.QtWidgets.QCheckBox("Word Wrap", self.general)
        self.general_layout.addWidget(self.word_wrap, 6, 2, 1, 1)

    def launchFiledialog(self, folder: "QtWidgets.QLineEdit") -> None:
        dialog = Qt.QtWidgets.QFileDialog()
        dialog.setFileMode(Qt.QtWidgets.QFileDialog.FileMode.Directory)
        dialog.setOption(Qt.QtWidgets.QFileDialog.Option.DontUseNativeDialog)
        dialog.setDirectory(folder.text())
        if PyQtExec(dialog).exec():
            folder.setText(dialog.selectedFiles()[0])

    def launchFontdialog(self, edit: "QtWidgets.QLineEdit") -> None:
        """Launch our font selection dialog."""
        initial = Qt.QtGui.QFont()
        initial.setFamily(edit.text())
        font, ok = Qt.QtWidgets.QFontDialog.getFont(initial)
        if ok:
            edit.setText(font.family())


# RESIZE HELPERS


def _expand_size(x: "QtCore.QSize", y: "QtCore.QSize") -> "QtCore.QSize":
    """Expand the size to the larger of the two sizes, for both the height and width."""
    return Qt.QtCore.QSize(max(x.width(), y.width()), max(x.height(), y.height()))


def _release_wayland(window: "Window") -> None:
    """Release the mouse on Wayland."""
    if not IS_TRUE_WAYLAND and sys.platform != "darwin":
        nonnull(window.window()).releaseMouse()


# WINDOW WIDGETS


class Label(Qt.QtWidgets.QLabel):
    """Custom QLabel-like class that allows text elision."""

    _text: str
    _elide: "QtCore.Qt.TextElideMode"
    _width_cb: "Callable[[], int] | None"
    _timer: "QtCore.QTimer"

    def __init__(
        self,
        text: str = "",
        parent: "QtWidgets.QWidget | None" = None,
        elide: "QtCore.Qt.TextElideMode" = Qt.QtCore.Qt.TextElideMode.ElideNone,
        width_cb: "Callable[[], int] | None" = None,
    ) -> None:
        super().__init__(text, parent)
        self._text = text
        self._elide = elide
        self._width_cb = width_cb
        self._timer = Qt.QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.elide)

    @override
    def text(self) -> str:
        """Get the internal text for the label."""
        return self._text

    @override
    def setText(self, text: str) -> None:  # type: ignore
        """Override the set text event to store the text internally."""

        # Need to set the text first, otherwise
        # the `width()` might be too small.
        self._text = text
        super().setText(text)
        self.elide()

    def elideMode(self) -> "QtCore.Qt.TextElideMode":
        """Get the elide mode for the label."""
        return self._elide

    def setElideMode(self, elide: "QtCore.Qt.TextElideMode") -> None:  # noqa: N802
        """Set the elide mode for the label."""
        self._elide = elide

    def elide(self) -> None:
        """Elide the text in the QLabel."""

        # The width estimate might not be valid: check the callback.
        width = self.width()
        if self._width_cb is not None:
            width = self._width_cb()

        metrics = Qt.QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self._text, self._elide, width)
        super().setText(elided)


class TitleButton(Qt.QtWidgets.QToolButton):
    """An icon-only button, without borders, for the titlebar."""

    def __init__(self, icon: "QtGui.QIcon", parent: "QtWidgets.QWidget | None" = None) -> None:
        super().__init__()
        _ = parent
        self.setIcon(icon)
        self.setAutoRaise(True)


class TitleBar(Qt.QtWidgets.QFrame):
    """Custom instance of a QTitlebar"""

    _window: "FramelessWindow | FramelessSubWindow"
    _state: "QtCore.Qt.WindowState"
    _window_rect: "QtCore.QRect"
    _has_help: "bool"
    _has_shade: "bool"
    _is_shaded: "bool"
    _has_shown: "bool"
    _title_column: "int"
    _move_timer: "QtCore.QTimer"
    _move_start: "QtCore.QPoint"
    _resize_timer: "QtCore.QTimer"
    _layout: "QtWidgets.QGridLayout"
    _menu: "TitleButton"
    _title: "Label"
    _min: "TitleButton"
    _max: "TitleButton"
    _restore: "TitleButton"
    _close: "TitleButton"
    _help: "TitleButton | None"
    _shade: "TitleButton | None"
    _unshade: "TitleButton | None"
    _main_menu: "QtWidgets.QMenu"
    _restore_action: "QtGui.QAction"
    _move_action: "QtGui.QAction"
    _size_action: "QtGui.QAction"
    _min_action: "QtGui.QAction"
    _max_action: "QtGui.QAction"
    _top_action: "QtGui.QAction"
    _close_action: "QtGui.QAction"
    _app: "QtWidgets.QApplication"

    def __init__(
        self,
        window: "FramelessWindow | FramelessSubWindow",
        parent: "QtWidgets.QWidget | None" = None,
        flags: "QtCore.Qt.WindowType | None" = None,
    ) -> None:
        super().__init__(parent)

        # Get and set some properties.
        self.setProperty("isTitlebar", True)
        self._window = window
        self._state = Qt.QtCore.Qt.WindowState.WindowNoState
        self._window_rect = self._window.geometry()
        self._has_help = False
        self._has_shade = False
        self._is_shaded = False
        self._has_shown = False
        self._title_column = 0
        self._move_timer = Qt.QtCore.QTimer()
        self._move_timer.timeout.connect(self.customMove)
        self._move_start = self.cursorPosition()
        self._resize_timer = Qt.QtCore.QTimer()
        self._resize_timer.timeout.connect(self.customResize)
        self._app = cast("QtWidgets.QApplication", Qt.QtWidgets.QApplication.instance())
        if flags is not None:
            self._has_help = bool(flags & Qt.QtCore.Qt.WindowType.WindowContextHelpButtonHint)
            self._has_shade = bool(flags & Qt.QtCore.Qt.WindowType.WindowShadeButtonHint)

        # Create our widgets.
        self._layout = Qt.QtWidgets.QGridLayout(self)
        self._menu = TitleButton(menu_icon(self))
        self._title = Label("", self, Qt.QtCore.Qt.TextElideMode.ElideRight, self.titleWidth)
        self._min = TitleButton(minimize_icon(self))
        self._max = TitleButton(maximize_icon(self))
        self._restore = TitleButton(restore_icon(self))
        self._close = TitleButton(close_icon(self))
        if self._has_help:
            self._help = TitleButton(help_icon(self))
        else:
            self._help = None
        if self._has_shade:
            self._shade = TitleButton(shade_icon(self))
            self._unshade = TitleButton(unshade_icon(self))
        else:
            self._shade = None
            self._unshade = None

        # Add actions to our menu.
        self._menu.setPopupMode(Qt.QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self._main_menu = Qt.QtWidgets.QMenu(self)
        self._restore_action = action("&Restore", self, restore_icon(self))
        self._restore_action.triggered.connect(self.restore)
        self._move_action = action("&Move", self, transparent_icon(self))
        self._move_action.triggered.connect(self.startCustomMove)
        self._size_action = action("&Size", self, transparent_icon(self))
        self._size_action.triggered.connect(self.startCustomResize)
        self._min_action = action("Mi&nimize", self, minimize_icon(self))
        self._min_action.triggered.connect(self.minimize)
        self._max_action = action("Ma&ximize", self, maximize_icon(self))
        self._max_action.triggered.connect(self.maximize)
        self._top_action = action("Stay on &Top", self, checkable=True)
        self._top_action.toggled.connect(self.toggleKeepAbove)
        self._close_action = action("&Close", self, close_icon(self))
        self._close_action.triggered.connect(self._window.close)
        self._main_menu.addActions([
            self._restore_action,
            self._move_action,
            self._size_action,
            self._min_action,
            self._max_action,
            self._top_action,
        ])
        self._main_menu.addSeparator()
        self._main_menu.addAction(self._close_action)
        self._menu.setMenu(self._main_menu)

        # Customize the enabled items.
        self._restore_action.setEnabled(False)

        # Create our layout.
        col = 0
        self._layout.addWidget(self._menu, 0, col)
        col += 1
        self._layout.addWidget(self._title, 0, col, Qt.QtCore.Qt.AlignmentFlag.AlignHCenter)
        self._layout.setColumnStretch(col, 1)
        self._title_column = col
        col += 1
        if self._has_help:
            self._layout.addWidget(self._help, 0, col)
            col += 1
        self._layout.addWidget(self._min, 0, col)
        self._state1_column = col
        col += 1
        self._layout.addWidget(self._max, 0, col)
        self._state2_column = col
        col += 1
        if self._has_shade:
            self._layout.addWidget(self._shade, 0, col)
            col += 1
        self._layout.addWidget(self._close, 0, col)
        self._close_column = col
        self._restore.hide()
        if self._unshade is not None:
            self._unshade.hide()

        # Add in our event triggers.
        self._min.clicked.connect(self.minimize)
        self._max.clicked.connect(self.maximize)
        self._restore.clicked.connect(self.restore)
        self._close.clicked.connect(self._window.close)
        if self._help is not None:
            self._help.clicked.connect(self.help)
        if self._shade and self._unshade is not None:
            self._shade.clicked.connect(self.shade)
            self._unshade.clicked.connect(self.unshade)

    # PROPERTIES

    @property
    def absoluteMinimumWidth(self) -> int:
        """Get the height (in pixels) for the minimum title bar width."""

        app = cast("QtWidgets.QApplication", Qt.QtWidgets.QApplication.instance())
        icon_width = self._menu.iconSize().width()
        font_size = app.font().pointSizeF()

        # We can have 4-6 icons, which with padding means we need
        # room for at least 10 characters.
        return 6 * icon_width + int(16 * font_size)

    @property
    def absoluteMinimumHeight(self) -> int:
        """Get the height (in pixels) for the minimum title bar height."""
        return TITLEBAR_HEIGHT

    @property
    def absoluteMinimumSize(self) -> "QtCore.QSize":
        """Get the minimum dimensions for the title bar."""
        return Qt.QtCore.QSize(self.absoluteMinimumWidth, self.absoluteMinimumHeight)

    def titleWidth(self) -> int:
        """Get the width of the title based on the grid layout."""
        return self._layout.cellRect(0, self._title_column).width()

    # QT-LIKE PROPERTIES

    @override
    def windowTitle(self) -> str:
        """Get the titlebar's window title."""
        return self._title.text()

    @override
    def setWindowTitle(self, title: str) -> None:  # type: ignore
        """Get the titlebar's window title."""
        self._title.setText(title)

    def isNormal(self) -> bool:
        """Get if the titlebar and therefore window has no state."""
        return self._state == Qt.QtCore.Qt.WindowState.WindowNoState

    def isMinimized(self) -> bool:
        """Get if the titlebar and therefore window is minimized."""
        return self._state == Qt.QtCore.Qt.WindowState.WindowMinimized

    def isMaximized(self) -> bool:
        """Get if the titlebar and therefore window is maximized."""
        return self._state == Qt.QtCore.Qt.WindowState.WindowMaximized

    # QT EVENTS

    @override
    def showEvent(self, event: "QtGui.QShowEvent") -> None:  # type: ignore
        """Set the minimum size policies once the widgets are shown."""

        global TITLEBAR_HEIGHT
        if not self._has_shown:
            TITLEBAR_HEIGHT = min(self.height(), TITLEBAR_HEIGHT)
            self._has_shown = True

        self.setAbsoluteMinimumSize()
        super().showEvent(event)

    # ACTIONS

    def setAbsoluteMinimumSize(self) -> None:
        """Set the minimum size of the titlebar."""
        self.setMinimumSize(self.absoluteMinimumWidth, self.absoluteMinimumHeight)

    def cursorPosition(self) -> "QtCore.QPoint":
        """Get the current cursor position mapped to the window."""
        return self._window.mapFromGlobal(Qt.QtGui.QCursor.pos())

    def startCustomMove(self) -> None:
        """Start the menu move tracking."""
        self._move_timer.start(TRACK_TIMER)

    def stopCustomMove(self) -> None:
        """Stop the menu move tracking."""
        self._move_timer.stop()
        self.window()._move = None

    def customMove(self) -> None:
        """Handle a menu move event."""
        if self._app.activeWindow() is None:
            self.stopCustomMove()
        elif self.window()._move is not None:
            self.customMoveUpdate()
        else:
            self.customMoveInitialize()

    def customMoveInitialize(self) -> None:
        """Start the process to track the menu move."""

        if self.window() == self._window:
            raise NotImplementedError("Custom move events at the window level are not yet supported.")

        window = self.window()
        window._move = self
        self._move_start = self.cursorPosition()

    def customMoveUpdate(self) -> None:
        """
        Update the position of the window after starting.

        Move the subwindow so that the position is in the center bottom
        of the title bar. The position is given in global coordinates.
        """

        if self.window() == self._window:
            raise NotImplementedError("Custom resize events at the window level are not yet supported.")

        delta = self._move_start - self.cursorPosition()
        geometry = self._window.geometry()
        position = geometry.topLeft() - delta

        bounds = self.window()._area.contentsRect()
        left = position.x()
        right = left + geometry.width()
        if left < bounds.left():
            position.setX(bounds.left())
        elif right > bounds.right():
            position.setX(bounds.right() - geometry.width())

        top = position.y()
        bottom = top + geometry.height()
        if top < bounds.top():
            position.setY(bounds.top())
        elif bottom > bounds.bottom():
            position.setY(bounds.bottom() - geometry.height())

        self._window.moveTo(position)

    def startCustomResize(self) -> None:
        """Start the menu resize tracking."""
        self._resize_timer.start(TRACK_TIMER)

    def stopCustomResize(self) -> None:
        """Stop the menu resize tracking."""

        self._resize_timer.stop()
        window = self.window()
        window._resize = None
        window.unsetCursor()
        _release_wayland(window)

    def customResize(self) -> None:
        """Handle a menu resize event."""
        if self._app.activeWindow() is None:
            self.stopCustomResize()
        elif self.window()._resize is not None:
            self.customResizeUpdate()
        else:
            self.customResizeInitialize()

    def customResizeInitialize(self) -> None:
        """Start the process to track the menu resize."""

        if self.window() == self._window:
            raise NotImplementedError("Custom resize events at the window level are not yet supported.")

        # NOTE: set the cursor FIRST and then fire, so when it
        # triggers we've already ensured the UI updates.
        geometry = self._window.geometry()
        point = geometry.bottomRight() - geometry.topLeft()
        Qt.QtGui.QCursor.setPos(self._window.mapToGlobal(point))

        window = self.window()
        window._resize = self
        self._resize_start = self.cursorPosition()
        self._resize_rect = self._window.geometry()

        window._resize = self
        self._resize_start = self.cursorPosition()
        self._resize_rect = self._window.geometry()

        window.setCursor(Qt.QtCore.Qt.CursorShape.SizeFDiagCursor)

    def customResizeUpdate(self) -> None:
        """
        Update the size of the window after starting.

        Size the window so that the position is in the center bottom
        of the title bar. The position is given in global coordinates.
        """

        if self.window() == self._window:
            raise NotImplementedError("Custom move events at the window level are not yet supported.")

        delta = self._resize_start - self.cursorPosition()
        start = self._resize_rect.topLeft()
        end = self._resize_rect.bottomRight() - delta
        rect = Qt.QtCore.QRect(start, end)

        bounds = self.window()._area.contentsRect()
        capped = bounds.bottomRight() - bounds.topLeft()
        rect.setRight(min(end.x(), capped.x()))
        rect.setBottom(min(end.y(), capped.y()))

        self._window.setGeometry(rect)

    def minimize(self) -> None:
        """Minimize the current window."""

        if self.isNormal():
            self._window_rect = self._window.geometry()
        self.setMinimized()
        self.setShaded()

        # Toggle state
        self._state = Qt.QtCore.Qt.WindowState.WindowMinimized
        self._is_shaded = False
        self._window.minimize(self._window.minimizedSize)

        # Toggle the menu actions
        # Minimized windows should not be movable, resizable, or minimizable.
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(False)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(False)
        self._max_action.setEnabled(True)

    def maximize(self) -> None:
        """Maximize the current window."""

        if self.isNormal():
            self._window_rect = self._window.geometry()
        elif self.isMinimized() and not self._is_shaded:
            self._window.unminimize()
        size = self._window.absoluteMaximumSize
        rect = Qt.QtCore.QRect(0, 0, size.width(), size.height())
        self.setMaximized()
        self.setUnshaded()

        # Toggle state
        self._state = Qt.QtCore.Qt.WindowState.WindowMaximized
        self._is_shaded = False
        self._window.maximize(rect)

        # Toggle the menu actions
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(False)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(False)

    def restore(self) -> None:
        """Restore the current window (set to no state)."""

        if self.isMinimized() and not self._is_shaded:
            self._window.unminimize()
        self.setRestored()
        self.setUnshaded()

        # Toggle state
        self._state = Qt.QtCore.Qt.WindowState.WindowNoState
        self._is_shaded = False
        self._window.restore(self._window_rect)

        # Toggle the menu actions
        self._restore_action.setEnabled(False)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(True)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(True)

    def shade(self) -> None:
        """Shade the current window."""

        # Shaded windows are treated as if they have minimized state, and
        # if the window is maximized, it sets the previous window rect
        # to the maximized geometry.
        self.setShaded()
        self.setMinimized()

        # Toggle state
        self._state = Qt.QtCore.Qt.WindowState.WindowMinimized
        self._is_shaded = True
        self._window_rect = self._window.geometry()
        width = self._window.width()
        height = self._window.minimizedSize.height()
        self._window.shade(Qt.QtCore.QSize(width, height))

        # Toggle the menu actions
        # Shaded windows should be movable, but not resizable or minimizable.
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(False)
        self._max_action.setEnabled(True)

    def unshade(self) -> None:
        """Unshade the current window."""

        if self.isMinimized() and not self._is_shaded:
            self._window.unminimize()

        # If the window is minimized, it restores to the previous
        # window state and position.
        self.setUnshaded()
        self.setRestored()

        # Toggle state
        self._state = Qt.QtCore.Qt.WindowState.WindowNoState
        self._is_shaded = False
        self._window.unshade(nonnull(self._window_rect))

        # Toggle the menu actions
        # Unshaded windows have no state: they are restored.
        self._restore_action.setEnabled(False)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(True)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(True)

    def toggleKeepAbove(self, checked: bool) -> None:
        """Toggle whether to keep the window above others."""

        # If we have a top-level widget, changing the window
        # flags causes `setParent` to be called, causing the
        # widget to hide and then re-appear. This causes major
        # visual delay, so we just ignore the hide event, then
        # set the flags, re-show the window, and unignore hides.
        # Finally, this can change the geometry of the window,
        # so we need to store the geometry and reset it.
        rect = self.window().geometry()
        if self._window.window() == self._window:
            self._window._ignore_hide = True

        flags = self._window.windowFlags()
        if checked:
            flags |= Qt.QtCore.Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~Qt.QtCore.Qt.WindowType.WindowStaysOnTopHint
        self._window.setWindowFlags(flags)

        if self._window.window() == self._window:
            self._window._ignore_hide = False
            self.window().show()
            self.window().setWindowGeometry(rect)

    def help(self) -> None:
        """Enter what's this mode."""
        Qt.QtWidgets.QWhatsThis.enterWhatsThisMode()

    # VIEW

    def window(self) -> "FramelessWindow":
        """Strongly typed override for our type checkers."""
        return cast("FramelessWindow", super().window())

    def setMinimized(self) -> None:
        """Show the restore and maximize icons."""

        if self.isMinimized():
            return

        item1 = self._layout.itemAtPosition(0, self._state1_column)
        item2 = self._layout.itemAtPosition(0, self._state2_column)
        self._layout.removeItem(item1)
        self._layout.removeItem(item2)
        self._layout.addWidget(self._restore, 0, self._state1_column)
        self._layout.addWidget(self._max, 0, self._state2_column)
        self._min.hide()
        self._restore.show()
        self._max.show()

    def setMaximized(self) -> None:
        """Show the minimize and restore icons."""

        self.setMaximized
        if self.isMaximized():
            return

        item1 = self._layout.itemAtPosition(0, self._state1_column)
        item2 = self._layout.itemAtPosition(0, self._state2_column)
        self._layout.removeItem(item1)
        self._layout.removeItem(item2)
        self._layout.addWidget(self._min, 0, self._state1_column)
        self._layout.addWidget(self._restore, 0, self._state2_column)
        self._max.hide()
        self._min.show()
        self._restore.show()

    def setRestored(self) -> None:
        """Show the minimize and maximize icons."""

        if self.isNormal():
            return

        item1 = self._layout.itemAtPosition(0, self._state1_column)
        item2 = self._layout.itemAtPosition(0, self._state2_column)
        self._layout.removeItem(item1)
        self._layout.removeItem(item2)
        self._layout.addWidget(self._min, 0, self._state1_column)
        self._layout.addWidget(self._max, 0, self._state2_column)
        self._restore.hide()
        self._min.show()
        self._max.show()

    def setShaded(self) -> None:
        """Show the unshade icon (and hide the shade icon)."""

        if self._shade and self._unshade and not (self.isMinimized() or self._is_shaded):
            self._layout.replaceWidget(self._shade, self._unshade)
            self._shade.hide()
            self._unshade.show()

    def setUnshaded(self) -> None:
        """Show the shade icon (and hide the unshade icon)."""

        if self._shade and self._unshade and (self.isMinimized() or self._is_shaded):
            self._layout.replaceWidget(self._unshade, self._shade)
            self._unshade.hide()
            self._shade.show()


class SizeFrame(Qt.QtCore.QObject):
    """An invisible frame for resizing events around a window."""

    _window: "FramelessWindow | FramelessSubWindow"
    _border_width: "int"
    _band: "QtWidgets.QRubberBand"
    _pressed: "bool"
    _cursor: "QtCore.Qt.CursorShape | None"
    _press_edge: "WindowEdge"
    _move_edge: "WindowEdge"

    def __init__(
        self,
        window: "FramelessWindow | FramelessSubWindow",
        border_width: int = 3,
    ) -> None:
        super().__init__(window)

        self._window = window
        self._border_width = border_width
        self._band = Qt.QtWidgets.QRubberBand(Qt.QtWidgets.QRubberBand.Shape.Rectangle)

        self._pressed = False
        self._cursor = None
        self._press_edge = WindowEdge.NoEdge
        self._move_edge = WindowEdge.NoEdge

        self._window.setMouseTracking(True)
        self._window.setWindowFlag(Qt.QtCore.Qt.WindowType.FramelessWindowHint, True)
        self._window.setAttribute(Qt.QtCore.Qt.WidgetAttribute.WA_Hover)

    @property
    def isActive(self) -> bool:
        """Get if the SizeFrame resize event is active."""
        return self._pressed

    def isOnTop(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the top of the widget."""
        return (
            pos.x() >= rect.x() + self._border_width
            and pos.x() <= rect.x() + rect.width() - self._border_width
            and pos.y() >= rect.y()
            and pos.y() <= rect.y() + self._border_width
        )

    def isOnBottom(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the bottom of the widget."""
        return (
            pos.x() >= rect.x() + self._border_width
            and pos.x() <= rect.x() + rect.width() - self._border_width
            and pos.y() >= rect.y() + rect.height() - self._border_width
            and pos.y() <= rect.y() + rect.height()
        )

    def isOnLeft(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the left of the widget."""
        return (
            pos.x() >= rect.x() - self._border_width
            and pos.x() <= rect.x() + self._border_width
            and pos.y() >= rect.y() + self._border_width
            and pos.y() <= rect.y() + rect.height() - self._border_width
        )

    def isOnRight(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the right of the widget."""
        return (
            pos.x() >= rect.x() + rect.width() - self._border_width
            and pos.x() <= rect.x() + rect.width()
            and pos.y() >= rect.y() + self._border_width
            and pos.y() <= rect.y() + rect.height() - self._border_width
        )

    def isOnTopLeft(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the top left of the widget."""
        return (
            pos.x() >= rect.x()
            and pos.x() <= rect.x() + self._border_width
            and pos.y() >= rect.y()
            and pos.y() <= rect.y() + self._border_width
        )

    def isOnTopRight(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the top right of the widget."""
        return (
            pos.x() >= rect.x() + rect.width() - self._border_width
            and pos.x() <= rect.x() + rect.width()
            and pos.y() >= rect.y()
            and pos.y() <= rect.y() + self._border_width
        )

    def isOnBottomLeft(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the bottom left of the widget."""
        return (
            pos.x() >= rect.x()
            and pos.x() <= rect.x() + self._border_width
            and pos.y() >= rect.y() + rect.height() - self._border_width
            and pos.y() <= rect.y() + rect.height()
        )

    def isOnBottomRight(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> bool:
        """Determine if the cursor is on the bottom right of the widget."""
        return (
            pos.x() >= rect.x() + rect.width() - self._border_width
            and pos.x() <= rect.x() + rect.width()
            and pos.y() >= rect.y() + rect.height() - self._border_width
            and pos.y() <= rect.y() + rect.height()
        )

    def cursorPosition(self, pos: "QtCore.QPoint", rect: "QtCore.QRect") -> WindowEdge:
        """Calculate the cursor position inside the window."""

        if self.isOnLeft(pos, rect):
            return WindowEdge.Left
        if self.isOnRight(pos, rect):
            return WindowEdge.Right
        if self.isOnBottom(pos, rect):
            return WindowEdge.Bottom
        if self.isOnTop(pos, rect):
            return WindowEdge.Top
        if self.isOnBottomLeft(pos, rect):
            return WindowEdge.BottomLeft
        if self.isOnBottomRight(pos, rect):
            return WindowEdge.BottomRight
        if self.isOnTopRight(pos, rect):
            return WindowEdge.TopRight
        if self.isOnTopLeft(pos, rect):
            return WindowEdge.TopLeft

        return WindowEdge.NoEdge

    def topLeft(self, rect: "QtCore.QRect") -> "QtCore.QPoint":
        """Get the top/left position of the window in global coordinates."""

        # Calculate the top left bounds of our window to get our frame.
        # We want our frame in global coordinates, but our window
        # might be a subwindow. If it has a parent, then it's a subwindow
        # and we need to map our coordinates.
        point = rect.topLeft()
        if self._window.window() != self._window:
            parent = self._window.parent()
            assert parent is not None and isinstance(parent, Qt.QtWidgets.QWidget)
            point = parent.mapToGlobal(point)

        return point

    def frame_geometry(self) -> "QtCore.QRect":
        """Calculate the frame geometry of our window in global coordinates."""

        rect = self._window.frameGeometry()
        return Qt.QtCore.QRect(self.topLeft(rect), self._window.frameSize())

    def geometry(self) -> "QtCore.QRect":
        """Calculate the geometry of our window in global coordinates."""

        rect = self._window.geometry()
        return Qt.QtCore.QRect(self.topLeft(rect), self._window.size())

    def updateCursor(self, position: "QtCore.QPoint") -> None:
        """Update the cursor shape depending on the cursor position."""

        if self._window.isMaximized() or self._window.isFullScreen():
            self.unset_cursor()
            return

        if self._pressed:
            return

        rect = self.frame_geometry()
        self._move_edge = self.cursorPosition(position, rect)
        if self._move_edge == WindowEdge.NoEdge:
            self.unset_cursor()
            return
        elif self._move_edge in (WindowEdge.Top, WindowEdge.Bottom):
            self._cursor = Qt.QtCore.Qt.CursorShape.SizeVerCursor
        elif self._move_edge in (WindowEdge.Left, WindowEdge.Right):
            self._cursor = Qt.QtCore.Qt.CursorShape.SizeHorCursor
        elif self._move_edge in (WindowEdge.TopLeft, WindowEdge.BottomRight):
            self._cursor = Qt.QtCore.Qt.CursorShape.SizeFDiagCursor
        elif self._move_edge in (WindowEdge.TopRight, WindowEdge.BottomLeft):
            self._cursor = Qt.QtCore.Qt.CursorShape.SizeBDiagCursor
        else:
            raise ValueError(f"Got an invalid move edge of {self._move_edge}.")

        self._window.setCursor(cast("QtCore.Qt.CursorShape", self._cursor))

    def resize(self, position: "QtCore.QPoint", rect: "QtCore.QRect") -> None:
        """Resize our window to the adjusted dimensions."""

        # Get our new frame dimensions.
        if self._press_edge == WindowEdge.NoEdge:
            return
        if self._press_edge == WindowEdge.Top:
            rect.setTop(position.y())
        if self._press_edge == WindowEdge.Bottom:
            rect.setBottom(position.y())
        if self._press_edge == WindowEdge.Left:
            rect.setLeft(position.x())
        if self._press_edge == WindowEdge.Right:
            rect.setRight(position.x())
        if self._press_edge == WindowEdge.TopLeft:
            rect.setTopLeft(position)
        if self._press_edge == WindowEdge.TopRight:
            rect.setTopRight(position)
        if self._press_edge == WindowEdge.BottomLeft:
            rect.setBottomLeft(position)
        if self._press_edge == WindowEdge.BottomRight:
            rect.setBottomRight(position)

        # Ensure we don't drag the widgets if we go below min sizes.
        if rect.width() < self._window.minimumWidth():
            if self._press_edge in LEFT_EDGES:
                rect.setLeft(rect.right() - self._window.minimumWidth())
            elif self._press_edge in RIGHT_EDGES:
                rect.setRight(rect.left() + self._window.minimumWidth())
        if rect.height() < self._window.minimumHeight():
            if self._press_edge in TOP_EDGES:
                rect.setTop(rect.bottom() - self._window.minimumHeight())
            elif self._press_edge in BOTTOM_EDGES:
                rect.setBottom(rect.top() + self._window.minimumHeight())

        # Calculate our rect for our widget.
        size = rect.size()
        point = rect.topLeft()
        if self._window.window() != self._window:
            assert isinstance(self._window, SubWindow)
            parent = self._window.parent()
            assert isinstance(parent, Qt.QtWidgets.QWidget)
            point = parent.mapFromGlobal(point)
        local_rect = Qt.QtCore.QRect(point, size)

        # If we have a subwindow, need to limit to the MDI area rect.
        if self._window.window() != self._window:
            assert isinstance(self._window, SubWindow)
            area_rect = nonnull(self._window.mdiArea()).contentsRect()
            # Need to calculate our shifts here.
            dx1 = max(local_rect.left(), area_rect.left()) - local_rect.left()
            dy1 = max(local_rect.top(), area_rect.top()) - local_rect.top()
            dx2 = min(local_rect.right(), area_rect.right()) - local_rect.right()
            dy2 = min(local_rect.bottom(), area_rect.bottom()) - local_rect.bottom()
            rect.adjust(dx1, dy1, dx2, dy2)
            # NOTE: Do not remove this. I have tried everything.
            # This does not work unless you keep it. There's a weird
            # bug where the window (only for QMdiSubWindow) now has
            # a bug where if you click on the title bar, it re-enters
            # a resize mode, which is independent of this. Shifting
            # the position by 1 pixel undoes this. Nothing else works,
            # and I have tried:
            #   - Not due to custom drag/move/resize/frame states.
            #   - Not due to lingering pressed/press_edge/move_edge.
            #   - Not due to a lingering cursor.
            #   - Not due to change event.
            #   - Not due to resize/show event.
            #   - Not due to mouse press/double click/release/move event.
            #   - Not due to the event filter.
            #   - Not due to the QMainWindow-level custom title bar.
            #   - `setFixedSize` on the window on the mouse release
            #       and then undoing on the next resize event eats
            #       the mouse click, but still enters the same mode
            #       (just the window can't be resized).
            #   - Not due to the window-level widgets or margins.
            #   - `setFixedSize` on the title bar just fixes title bar size.
            #   - No previous versions work if we use the local_rect.
            #   - Unsetting the band and use the window directly does nothing.
            #   - Using `setGeometry(rect)` then `setGeometry(local_rect)`.
            #   - Unsetting the band geometry in `mouse_release` event.
            #   - Simulating mouse press+release in `mouse_release`.
            #   - Simulating mouse press+release in `end_frame`.
            #   - Ignoring the subsequent mousePressEvent on the title bar.
            #       - This causes the window to disappear entirely.
            #   - Hide+show inside `mouse_release` causes window to hide.
            #   - Hide+show inside `end_frame` causes window to hide.
            #   - Not due to minimum rect size checks.
            #   - Not due to MDI area limit checks.
            #   - Not related to custom restore/min/max/shade/unshade code.
            #   - Not due to custom hide/setVisible overrides.
            #
            # This is almost certain a bug in QMdiArea, but this is a
            # workaround that produces almost is almost imperceptible,
            # since the widget is being actively resized.
            #
            # I love mess.... but not this.
            if dx1 == 0 and dy1 == 0 and dx2 == 0 and dy2 == 0:
                dx1 += 1
                dy1 += 1
                dx2 += 1
                dy2 += 1
            local_rect.adjust(dx1, dy1, dx2, dy2)

        self._window.setWindowGeometry(local_rect)
        self._band.setGeometry(rect)

    def unset_cursor(self) -> None:
        """Unset the custom cursor."""

        if self._cursor:
            self._window.unsetCursor()
        self._cursor = None

    def enter(self, event: "QtGui.QSinglePointEvent") -> None:
        """Handle the enterEvent of the window."""

        position = PyQtPosition(event).position()
        self.updateCursor(self._window.mapToGlobal(position))

    def leave(self, event: "QtGui.QSinglePointEvent") -> None:
        """Handle the leaveEvent of the window."""
        _ = event
        if not self._pressed:
            self.unset_cursor()

    def mouseMove(self, event: "QtGui.QMouseEvent") -> None:
        """Handle the mouseMoveEvent of the window."""

        position = PyQtPosition(event).position()
        if not self._pressed:
            self.updateCursor(position)
            return

        self.resize(position, self._band.geometry())

    def mousePress(self, event: "QtGui.QMouseEvent") -> None:
        """Handle the mousePressEvent of the window."""

        if event.button() == Qt.QtCore.Qt.MouseButton.LeftButton:
            position = PyQtPosition(event).position()
            rect = self.frame_geometry()
            self._press_edge = self.cursorPosition(position, rect)
            # We want to separately handle drags, so only
            # set this if we are pressing on the edge.
            if self._press_edge != WindowEdge.NoEdge:
                self._pressed = True
                self._band.setGeometry(self.geometry())

    def mouseRelease(self, event: "QtGui.QMouseEvent") -> None:
        """Handle the mouseReleaseEvent of the window."""

        if event.button() == Qt.QtCore.Qt.MouseButton.LeftButton and self._pressed:
            self._pressed = False

    def hoverMove(self, event: "QtGui.QHoverEvent") -> None:
        """Handle the hoverMoveEvent of the window."""

        position = PyQtPosition(event).position()
        self.updateCursor(self._window.mapToGlobal(position))


class SubWindow(Qt.QtWidgets.QMdiSubWindow):
    """Base subclass for a QMdiSubwindow."""

    _sizeframe: "SizeFrame | None"

    def __init__(
        self,
        parent: "QtWidgets.QWidget | None" = None,
        flags: "QtCore.Qt.WindowType" = Qt.QtCore.Qt.WindowType(0),
    ) -> None:
        super().__init__(parent, flags=flags)
        super().setWidget(Qt.QtWidgets.QWidget())
        self._sizeframe = None


class DefaultSubWindow(SubWindow):
    """Default subwindow with a window frame."""

    def __init__(
        self,
        parent: "QtWidgets.QWidget | None" = None,
        flags: "QtCore.Qt.WindowType" = Qt.QtCore.Qt.WindowType(0),
        sizegrip: bool = False,
    ):
        _ = sizegrip
        super().__init__(parent, flags=flags)


class FramelessSubWindow(SubWindow):
    """Custom subwindow instance without a window frame."""

    _central: "QtWidgets.QFrame"
    _titlebar: "TitleBar"
    _widget: "QtWidgets.QWidget"
    _border: int
    _titlebar_size: "QtCore.QSize"
    _sizegrip: "QtWidgets.QSizeGrip | None"
    _sizegrip_size: "QtCore.QSize"
    _ignore_hide: "bool"

    def __init__(
        self,
        parent: "QtWidgets.QWidget | None" = None,
        flags: "QtCore.Qt.WindowType" = Qt.QtCore.Qt.WindowType(0),
        sizegrip: bool = False,
    ):
        super().__init__(parent, flags=flags | Qt.QtCore.Qt.WindowType.FramelessWindowHint)

        # Create our widgets. Sizeframe and sizegrip are mutually exclusive.
        self._central = Qt.QtWidgets.QFrame(super().widget())
        self._central.setLayout(Qt.QtWidgets.QVBoxLayout())
        self._titlebar = TitleBar(self, self._central, flags)
        self._widget = Qt.QtWidgets.QWidget(self._central)
        self._widget.setLayout(Qt.QtWidgets.QVBoxLayout())
        self._border = ARGS.border_width
        self._titlebar_size = Qt.QtCore.QSize()
        self._sizegrip_size = Qt.QtCore.QSize()
        self._old_minimum_size = None
        self._ignore_hide = True
        if sizegrip:
            self._sizeframe = None
            self._sizegrip = Qt.QtWidgets.QSizeGrip(self._central)
        else:
            self._sizeframe = SizeFrame(self, border_width=5)
            self._sizegrip = None

        # Add our titlebar, then our central widgets, etc.
        # Make sure we have our titlebar compacted to fit.
        # The trick here is quite simple: have no spacing
        # on the parent layout (so the titlebar goes on the
        # absolute top), and all 3 widgets, with the main
        # widget expanding to the view, and make it seem like
        # it's the central widget for the layout, as is its layout.

        # Align the size grip to the bottom right, without stretch, so
        # it compacts and has the natural placement. For the titlebar,
        # align it top so when the sizegrip is hidden (as is the widget),
        # it does not have a border/padding on the top.
        bottom_right = Qt.QtCore.Qt.AlignmentFlag.AlignBottom | Qt.QtCore.Qt.AlignmentFlag.AlignRight
        layout = cast("QtWidgets.QBoxLayout", nonnull(super().layout()))
        nonnull(layout).setSpacing(0)
        nonnull(layout).addWidget(self._central, 10)
        central_layout = cast("QtWidgets.QBoxLayout", nonnull(self._central.layout()))
        central_layout.setSpacing(0)
        central_layout.addWidget(self._titlebar, 0, Qt.QtCore.Qt.AlignmentFlag.AlignTop)
        central_layout.addWidget(self._widget, 10)
        if self._sizegrip is not None:
            central_layout.addWidget(self._sizegrip, 0, bottom_right)

        # Set the border properties.
        central_layout.setContentsMargins(Qt.QtCore.QMargins(0, 0, 0, 0))
        self._central.setProperty("isWindow", True)
        if self._border > 0:
            self._central.setProperty("windowFrame", min(self._border, 5))
            self._central.setFrameShape(Qt.QtWidgets.QFrame.Shape.Box)
            self._central.setFrameShadow(Qt.QtWidgets.QFrame.Shadow.Raised)

        # Ensure our titlebar gets highest priority.
        self._titlebar.raise_()
        self._widget.lower()

    # PROPERTIES

    @property
    def borderSize(self) -> "QtCore.QSize":
        """Get the size of the border, regardless if present."""
        return Qt.QtCore.QSize(2 * self._border, 2 * self._border)

    @property
    def minimizedContentSize(self) -> "QtCore.QSize":
        """Get the minimum content size of the widget."""
        return self._titlebar_size

    @property
    def minimizedSize(self) -> "QtCore.QSize":
        """Get the minimum size of the widget, with the size grips hidden."""
        return self.minimizedContentSize + self.borderSize

    @property
    def absoluteMinimumSize(self) -> "QtCore.QSize":
        """Get the minimum size for the widget."""

        size = self.minimizedSize
        if self._sizegrip is not None and self._sizegrip.isVisible():
            # Don't modify in place: percolates later.
            size = size + self._sizegrip_size

        return size

    @property
    def absoluteMaximumSize(self):
        """Get the maximum size for the widget."""
        return nonnull(self.mdiArea()).size()

    # RESIZE

    def window(self) -> "Window":
        """Get a strongly typed variant of the window."""
        return cast("Window", nonnull(super().window()))

    def moveTo(self, position: "QtCore.QPoint") -> None:
        """Move the window to the desired position."""
        # NOTE: Do not remove and use raw `move` in case this needs to be updated later.
        self.move(position)

    def setWindowGeometry(self, rect: "QtCore.QRect") -> None:
        """Set the window geometry."""
        self.resize(rect.size())
        self.moveTo(rect.topLeft())

    def setAbsoluteMinimumSize(self) -> None:
        """Sets the minimum size of the window and the titlebar, with clobbering."""
        self._old_minimum_size = self.minimumSize()
        self._titlebar.setAbsoluteMinimumSize()
        self._titlebar_size = self._titlebar.minimumSize()
        self.setMinimumSize(self.absoluteMinimumSize)

    def expandMinimumSize(self) -> None:
        """Sets the minimum size of the window and the titlebar, without clobbering."""
        if self._old_minimum_size is not None:
            self.setMinimumSize(self._old_minimum_size)
        self._titlebar.setAbsoluteMinimumSize()
        self._titlebar_size = self._titlebar.minimumSize()
        size = _expand_size(self.absoluteMinimumSize, self.minimumSize())
        self.setMinimumSize(size)

    def minimize(self, size: "QtCore.QSize") -> None:
        """Minimize the window, hiding the main widget and size grip."""

        self._widget.hide()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.setAbsoluteMinimumSize()
        self.resize(size)
        cast("MdiArea", nonnull(self.mdiArea())).minimize(self)

    def maximize(self, rect: "QtCore.QRect") -> None:
        """Maximize the window, showing the main widget and hiding size grip."""

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.expandMinimumSize()
        self.setWindowGeometry(rect)

    def restore(self, rect: "QtCore.QRect") -> None:
        """Restore the window, showing the main widget and size grip."""

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.show()
        self.expandMinimumSize()
        self.setWindowGeometry(rect)

    def shade(self, size: "QtCore.QSize") -> None:
        """Shade the window, hiding the main widget and size grip."""

        self._widget.hide()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.setAbsoluteMinimumSize()
        self.resize(size)

    def unshade(self, rect: "QtCore.QRect") -> None:
        """Unshade the window, showing the main widget and size grip."""

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.show()
        self.expandMinimumSize()
        self.setWindowGeometry(rect)

    def unminimize(self) -> None:
        """Unminimize a minimized subwindow."""
        cast("MdiArea", nonnull(self.mdiArea())).unminimize(self)

    # QT EVENTS

    @override
    def resizeEvent(self, event: "QtGui.QResizeEvent | None") -> None:  # type: ignore
        """Handle widget resize events here."""

        # Need to trigger the titlebar title resize. Need to handle it
        # here, since the SizeFrame resizes won't always trigger a
        # Label::resizeEvent, which can cause the text to stay elided.
        title_timer = self._titlebar._title._timer
        title_timer.start(REPAINT_TIMER)

        super().resizeEvent(event)

    @override
    def showEvent(self, event: "QtGui.QShowEvent | None") -> None:  # type: ignore
        """Set the minimum size policies once the widgets are shown."""

        # Until shown, the size grip has inaccurate sizes.
        # Set the minimum size policy of the widget.
        # The show event occurs just after everything is shown,
        # so the widget sizes (and isVisible) are accurate.
        self._titlebar_size = self._titlebar.minimumSize()
        if self._sizegrip is not None:
            grip_size = self._sizegrip.sizeHint()
            self._sizegrip_size = Qt.QtCore.QSize(0, grip_size.height())
        size = _expand_size(self.absoluteMinimumSize, self.minimumSize())
        self.setMinimumSize(size)

        super().showEvent(event)

    @override
    def mouseDoubleClickEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """Override the mouse double click, and don't call the press event."""

        # By default, the flowchart for titlebar double clicks is as follows:
        #   1. If minimized, restore
        #   2. If maximized, restore
        #   3. If no state and can shade, shade
        #   4. If no state and cannot shade, maximize
        #   5. If shaded, unshade.
        widget = self._titlebar
        if event is None or not widget.underMouse() or event.button() != Qt.QtCore.Qt.MouseButton.LeftButton:
            return super().mouseDoubleClickEvent(event)
        if widget._is_shaded:
            return widget.unshade()
        if widget.isMinimized() or widget.isMaximized():
            return widget.restore()
        if widget._has_shade:
            return widget.shade()
        return widget.maximize()

    @override
    def mousePressEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """Override a mouse click on the titlebar to allow a move."""

        titlebar = self._titlebar
        window = self.window()
        if event is not None and titlebar.underMouse():
            is_left = event.button() == Qt.QtCore.Qt.MouseButton.LeftButton
            is_minimized = self.isMinimized() and not titlebar._is_shaded
            if is_left and not is_minimized and window._subwindow_frame is None:
                window._subwindow_drag = event.pos()
            elif event.button() == Qt.QtCore.Qt.MouseButton.RightButton:
                position = PyQtPosition(event).position()
                PyQtMenu(titlebar._main_menu).exec(position)

        return super().mousePressEvent(event)

    @override
    def mouseMoveEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """Reposition the window on the move event."""

        window = self.window()
        if window._subwindow_frame is not None:
            window._subwindow_drag = None
        if event is not None and window._subwindow_drag is not None:
            position = event.pos() - window._subwindow_drag
            self.moveTo(self.mapToParent(position))

        return super(type(self), self).mouseMoveEvent(event)

    @override
    def mouseReleaseEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """End the drag event."""
        self.window()._subwindow_drag = None
        super().mouseReleaseEvent(event)

    # QT-LIKE PROPERTIES

    @override
    def windowTitle(self) -> str:
        """Get the window title from the titlebar."""
        return self._titlebar.windowTitle()

    @override
    def setWindowTitle(self, title: str) -> None:  # type: ignore
        """Get the window title from the titlebar."""
        self._titlebar.setWindowTitle(title)

    @override
    def layout(self) -> "QtWidgets.QLayout | None":
        """Get the subwindow layout (mapped to self._widget)"""
        return self._widget.layout()

    @override
    def setLayout(self, layout: "QtWidgets.QLayout | None") -> None:  # type: ignore
        """Set the subwindow layout (mapped to self._widget)"""
        self._widget.setLayout(layout)

    @override
    def widget(self) -> "QtWidgets.QWidget":
        """Get the subwindow widget (mapped to self._widget)"""
        return self._widget

    @override
    def setWidget(self, widget: "QtWidgets.QWidget") -> None:  # type: ignore
        """Set the subwindow widget (mapped to self._widget)"""
        nonnull(super().layout()).replaceWidget(self._widget, widget)
        self._widget = widget

    def isMinimized(self) -> bool:
        """Overload since we use a custom minimized for our subwindow."""
        return self._titlebar.isMinimized()

    def isMaximized(self) -> bool:
        """Overload since we use a custom maximized for our subwindow."""
        return self._titlebar.isMaximized()


class MdiArea(Qt.QtWidgets.QMdiArea):
    """Override the QMdiArea for window minimization and background color."""

    _minimized: "list[FramelessSubWindow]"
    _location: "MinimizeLocation"
    _timer: "QtCore.QTimer"

    def __init__(
        self,
        parent: "QtWidgets.QWidget | None" = None,
        location: "MinimizeLocation" = MINIMIZE_LOCATION,
    ):
        super().__init__(parent)
        self._minimized = []
        self._location = location
        self._timer = Qt.QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.moveMinimized)

        # Set the background color
        background = self.background()
        background.setColor(Qt.QtGui.QColor(*COLORS.view_background))
        self.setBackground(background)

    @override
    def resizeEvent(self, event: "QtGui.QResizeEvent | None") -> None:  # type: ignore
        """Handle moving minimized windows without glitchy motion."""
        self._timer.start(REPAINT_TIMER)
        super().resizeEvent(event)

    def minimize(self, subwindow: "FramelessSubWindow") -> None:
        """Minimize a subwindow and reposition it."""

        self._minimized.append(subwindow)
        self.moveMinimized()

    def unminimize(self, subwindow: "FramelessSubWindow") -> None:
        """Unminimize a subwindow."""

        self._minimized.remove(subwindow)
        self.moveMinimized()

    def moveMinimized(self) -> None:
        """Move the minimized windows."""

        # No need to set the geometry of our minimized windows.
        if not self._minimized:
            return

        # Get the geometry of the elements, and calculate the windows per row.
        window = self._minimized[0]
        has_border = any(i._border for i in self._minimized)
        size = window.minimizedContentSize
        if has_border:
            size = size + window.borderSize
        width = size.width()
        height = size.height()
        width += max(int(0.01 * width), 1)
        height += max(int(0.01 * height), 1)
        total_size = self.size()
        minimized_count = len(self._minimized)
        row_count = max(total_size.width() // width, 1)
        rows = minimized_count // row_count
        if minimized_count % row_count != 0:
            rows += 1

        # Get how we shift our elements. Start our elements so
        # the first iteration will shift them into place.
        # We never want to place elements at a negative index,
        # so our right always starts at least at 1.
        # For our bottom, we want the last element to be placed at (_, 0)
        # if it would overflow to the top, we place it at 0 instead.
        left_x = 0
        right_x = max(total_size.width() - width, 0)
        top_y = 0
        bottom_y = max(total_size.height() - height, (rows - 1) * height)
        if self._location == MinimizeLocation.TopLeft:
            point = QtCore.QPoint(left_x, top_y)
            new_column = lambda p: Qt.QtCore.QPoint(left_x, p.y() + height)  # noqa
            shift_row = lambda p, w: p + Qt.QtCore.QPoint(w, 0)  # noqa
        elif self._location == MinimizeLocation.TopRight:
            point = Qt.QtCore.QPoint(right_x, top_y)
            new_column = lambda p: Qt.QtCore.QPoint(right_x, p.y() + height)  # noqa
            shift_row = lambda p, w: p - Qt.QtCore.QPoint(w, 0)  # noqa
        elif self._location == MinimizeLocation.BottomLeft:
            point = Qt.QtCore.QPoint(left_x, bottom_y)
            new_column = lambda p: Qt.QtCore.QPoint(left_x, p.y() - height)  # noqa
            shift_row = lambda p, w: p + Qt.QtCore.QPoint(w, 0)  # noqa
        else:
            point = Qt.QtCore.QPoint(right_x, bottom_y)
            new_column = lambda p: Qt.QtCore.QPoint(right_x, p.y() - height)  # noqa
            shift_row = lambda p, w: p - Qt.QtCore.QPoint(w, 0)  # noqa

        # Now, need to place them accordingly.
        # Need to handle unshifts, if they occur, due to the
        for index, window in enumerate(self._minimized):
            # Calculate our new column, only storing if it is a new column.
            is_new_column = index % row_count == 0
            if index != 0 and is_new_column:
                point = new_column(point)

            window.move(point)
            point = shift_row(point, width)


class Window(Qt.QtWidgets.QMainWindow):
    """Base subclass for a QMainWindow."""

    _central: "QtWidgets.QFrame"
    _layout: "QtWidgets.QBoxLayout"
    _widget: "QtWidgets.QWidget"
    _area: "MdiArea"
    _window1: "SubWindow"
    _window2: "SubWindow"
    _window3: "SubWindow"
    _tree: "SortableTree"
    _subwindow_drag: "QtCore.QPoint | None"
    _subwindow_frame: "SizeFrame | None"
    _window_drag: "QtCore.QPoint | None"
    _move: "TitleBar | None"
    _resize: "TitleBar | None"
    _window_frame: "SizeFrame | None"
    _sizeframe: "SizeFrame | None"

    def __init__(
        self,
        parent: "QtWidgets.QWidget | None" = None,
        flags: "QtCore.Qt.WindowType" = Qt.QtCore.Qt.WindowType(0),
    ) -> None:
        super().__init__(parent, flags)

        self._central = Qt.QtWidgets.QFrame(self)
        self._layout = Qt.QtWidgets.QVBoxLayout(self._central)
        self.setCentralWidget(self._central)
        self._widget = Qt.QtWidgets.QWidget(self._central)
        self._widget.setLayout(Qt.QtWidgets.QVBoxLayout())

        self._subwindow_frame = None
        self._subwindow_drag = None
        self._window_drag = None
        self._move = None
        self._resize = None
        self._window_frame = None
        self._sizeframe = None

    def setup(self) -> None:
        """Setup the main UI."""

        subwindow_class = FramelessSubWindow
        if ARGS.default_window_frame:
            subwindow_class = DefaultSubWindow

        self.resize(1068, 824)
        self.setWindowTitle("Custom SubWindow Style.")

        self._central = Qt.QtWidgets.QFrame(self)
        flags = Qt.QtCore.Qt.WindowType.SubWindow
        self._area = MdiArea(self._widget)
        self._window1 = subwindow_class(flags=flags, sizegrip=True)
        self._window1.setWindowTitle("Short Title")
        self._area.addSubWindow(self._window1)
        self.table = LargeTable(self._window1.widget())
        nonnull(self._window1.layout()).addWidget(self.table)

        flags = Qt.QtCore.Qt.WindowType.SubWindow
        flags |= Qt.QtCore.Qt.WindowType.WindowContextHelpButtonHint
        flags |= Qt.QtCore.Qt.WindowType.WindowShadeButtonHint
        self._window2 = subwindow_class(flags=flags)
        self._window2.setWindowTitle("Example of a very, very long title")
        self._area.addSubWindow(self._window2)
        self._tree = SortableTree(self._window2.widget())
        nonnull(self._window2.layout()).addWidget(self._tree)

        flags = Qt.QtCore.Qt.WindowType.SubWindow
        flags |= Qt.QtCore.Qt.WindowType.WindowShadeButtonHint
        self._window3 = subwindow_class(flags=flags, sizegrip=True)
        self._window3.setWindowTitle("Medium length title")
        self._area.addSubWindow(self._window3)
        nonnull(self._widget.layout()).addWidget(self._area)
        self.tab = SettingTabs(self._window3.widget())
        nonnull(self._window3.layout()).addWidget(self.tab)

    # PROPERTIES

    @property
    def absoluteMaximumSize(self) -> "QtCore.QSize":
        """Get the maximum size for the window."""
        # Unused since we use the window flags anyway.
        return self.maximumSize()

    # ACTIONS

    def resolveState(self) -> None:
        """Handle theoretically possible conflicts in window state."""

        # The _drag, _move, _resize, and _frame options are
        # mutually exclusive: only one can be active at a given time.
        # Since we use timers for `_move` and `_resize`, it's **possible**
        # multiple might be active here, but it's unlikely. So, we handle
        # those cases by playing favorites. _frame > _resize > _move > _drag.
        # We deal with the window-level widgets first, then the subwindow-level
        # widgets next.

        has_state = False
        if self._window_frame is not None:
            if self._resize is not None:
                self._resize.stopCustomResize()
            has_state = True
        if has_state or self._resize is not None:
            if self._move is not None:
                self._move.stopCustomMove()
            has_state = True
        if has_state or self._move is not None:
            self._window_drag = None
            has_state = True
        if has_state or self._window_drag is not None:
            self._window_frame = None
            has_state = True

    def frameEvent(self, event: "QtCore.QEvent", frame: "SizeFrame"):
        """Handle size adjustments using the window frame."""

        # No position for the event: we don't use it.
        type = event.type()
        types = Qt.QtCore.QEvent.Type
        if type in (types.Enter, types.HoverEnter):
            frame.enter(cast("QtGui.QSinglePointEvent", event))
        elif type in (types.Leave, types.HoverLeave):
            frame.leave(cast("QtGui.QSinglePointEvent", event))
        elif type == types.MouseMove:
            frame.mouseMove(cast("QtGui.QMouseEvent", event))
        elif type == types.MouseButtonPress:
            frame.mousePress(cast("QtGui.QMouseEvent", event))
        elif type == types.MouseButtonRelease:
            frame.mouseRelease(cast("QtGui.QMouseEvent", event))
        elif type == types.HoverMove:
            frame.hoverMove(cast("QtGui.QHoverEvent", event))

    # QT EVENTS

    @override
    def eventFilter(self, obj: "QtCore.QObject | None", event: "QtCore.QEvent | None") -> bool:  # type: ignore
        """Custom event filter to handle move and resize events."""

        if event is None:
            return False

        self.resolveState()
        type = event.type()
        types = Qt.QtCore.QEvent.Type
        if self._move is not None and type == types.MouseMove:
            # NOTE: explicit pass, we use a timer and not mouse clicks
            pass
        elif self._move is not None and type == types.MouseButtonPress:
            self._move.stopCustomMove()
        elif self._resize is not None and type in (types.MouseMove, types.HoverMove):
            # NOTE: explicit pass, we use a timer and not mouse clicks
            pass
        elif self._resize is not None and type == types.MouseButtonPress:
            self._resize.stopCustomResize()
        elif isinstance(obj, Window) and not obj.isMinimized() and obj._sizeframe is not None:
            self.frameEvent(event, obj._sizeframe)
            self._window_frame = obj._sizeframe if obj._sizeframe.isActive else None
        elif isinstance(obj, SubWindow) and not obj.isMinimized() and obj._sizeframe is not None:
            self.frameEvent(event, obj._sizeframe)
            self._subwindow_frame = obj._sizeframe if obj._sizeframe.isActive else None

        return super().eventFilter(obj, event)


class FramelessWindow(Window):
    """Main window with a custom event filter for all events."""

    _titlebar: "TitleBar"
    _sizegrip: "QtWidgets.QSizeGrip | None"
    _statusbar: "QtWidgets.QStatusBar | None"
    _sizeframe: "SizeFrame | None"
    _border: int
    _titlebar_size: "QtCore.QSize"
    _sizegrip_size: "QtCore.QSize"
    _statusbar_size: "QtCore.QSize"
    _old_minimum_size: "QtCore.QSize | None"
    _ignore_hide: "bool"

    def __init__(
        self,
        parent: "QtWidgets.QWidget | None" = None,
        flags: "QtCore.Qt.WindowType" = Qt.QtCore.Qt.WindowType(0),
    ) -> None:
        # On X11, the `WindowStaysOnTopHint` hint supposedly doesn't
        # work unless you bypass the window manager, but this seems
        # to no longer be true. There's major downsides to bypassing
        # the window manager, so it's not worth it anyway.
        flags |= Qt.QtCore.Qt.WindowType.FramelessWindowHint
        if ARGS.window_help:
            flags |= Qt.QtCore.Qt.WindowType.WindowContextHelpButtonHint
        if ARGS.window_shade:
            flags |= Qt.QtCore.Qt.WindowType.WindowShadeButtonHint
        super().__init__(parent, flags)

        self._titlebar = TitleBar(self, self._central, flags)
        self._sizegrip = None
        self._border = ARGS.border_width
        self._titlebar_size = Qt.QtCore.QSize()
        self._sizegrip_size = Qt.QtCore.QSize()
        self._statusbar_size = Qt.QtCore.QSize()
        self._old_minimum_size = None
        if ARGS.status_bar:
            self._statusbar = Qt.QtWidgets.QStatusBar(self._central)
            self.setStatusBar(self._statusbar)
            self._sizeframe = None
        else:
            self._statusbar = None
            self._sizeframe = SizeFrame(self, border_width=5)

        self._layout.setSpacing(0)
        self._layout.addWidget(self._titlebar, 0, Qt.QtCore.Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._widget, 10)

        # For toggling window flags, which calls `setParent`, hiding the window.
        # Since an immediate show causes an unminimize/re-minimize, this
        # causes a serious visual lag.
        self._ignore_hide = False

        # Set the border properties.
        self._layout.setContentsMargins(Qt.QtCore.QMargins(0, 0, 0, 0))
        self._central.setProperty("isWindow", True)
        if self._border > 0:
            self._central.setProperty("windowFrame", min(self._border, 5))
            self._central.setFrameShape(Qt.QtWidgets.QFrame.Shape.Box)
            self._central.setFrameShadow(Qt.QtWidgets.QFrame.Shadow.Raised)

        # Ensure our titlebar gets highest priority.
        self._titlebar.raise_()
        self._widget.lower()

        self.setup()

    # HACKS

    @override
    def hide(self) -> None:
        """Override the hide event to ignore it if desired."""

        if self._ignore_hide:
            return
        super().hide()

    @override
    def setVisible(self, visible: bool) -> None:
        """Override the hide event to ignore it if desired."""

        if self._ignore_hide and not visible:
            return
        super().setVisible(visible)

    # PROPERTIES

    @property
    def borderSize(self) -> "QtCore.QSize":
        """Get the size of the border, regardless if present."""
        return Qt.QtCore.QSize(2 * self._border, 2 * self._border)

    @property
    def minimizedContentSize(self) -> "QtCore.QSize":
        """Get the minimum content size of the widget."""
        return self._titlebar_size

    @property
    def minimizedSize(self) -> "QtCore.QSize":
        """Get the minimum size of the widget, with the size grips hidden."""
        return self.minimizedContentSize + self.borderSize

    @property
    def absoluteMinimumSize(self) -> "QtCore.QSize":
        """Get the minimum size for the widget."""

        size = self.minimizedSize
        if self._statusbar is not None and self._statusbar.isVisible():
            # Don't modify in place: percolates later.
            size = size + self._statusbar_size

        return size

    # QT-LIKE PROPERTIES

    @override
    def windowTitle(self) -> str:
        """Get the window title from the titlebar."""
        return self._titlebar.windowTitle()

    @override
    def setWindowTitle(self, title: str) -> None:  # type: ignore
        """Get the window title from the titlebar."""
        self._titlebar.setWindowTitle(title)

    # RESIZE

    def moveTo(self, position: "QtCore.QPoint") -> None:
        """Move the window to the desired position."""

        # Also updates the stored previous subwindow position, if applicable.
        # This means shading/unshading uses the new position of the window,
        # but the old sizes, rather than jump the window back.
        # NOTICE: this fails on Wayland. Worse, using `QMainWindow::move` on
        # Wayland causes the cursor position to be incorrect, causing issues
        # with other events.
        if IS_WAYLAND:
            return
        self.move(position)

    def setWindowGeometry(self, rect: "QtCore.QRect") -> None:
        """Set the window geometry."""

        self.resize(rect.size())
        window_rect = self._titlebar._window_rect
        if window_rect is not None:
            window_rect.setSize(rect.size())

        self.moveTo(rect.topLeft())

    def setAbsoluteMinimumSize(self) -> None:
        """Sets the minimum size of the window and the titlebar, with clobbering."""

        self._old_minimum_size = self.minimumSize()
        self._titlebar.setAbsoluteMinimumSize()
        self._titlebar_size = self._titlebar.minimumSize()
        self.setMinimumSize(self.absoluteMinimumSize)

    def expandMinimumSize(self) -> None:
        """Sets the minimum size of the window and the titlebar, without clobbering."""

        if self._old_minimum_size is not None:
            self.setMinimumSize(self._old_minimum_size)
        self._titlebar.setAbsoluteMinimumSize()
        self._titlebar_size = self._titlebar.minimumSize()
        size = _expand_size(self.absoluteMinimumSize, self.minimumSize())
        self.setMinimumSize(size)

    def minimize(self, size: "QtCore.QSize") -> None:
        """Minimize the window, using the actual OS to handle that."""
        self.showMinimized()

    def maximize(self, rect: "QtCore.QRect | None" = None):
        """Minimize the window, using the actual OS to handle that."""
        self.showMaximized()

    def restore(self, rect: "QtCore.QRect | None" = None) -> None:
        """Restore the window, showing the main widget and size grip."""
        self.showNormal()

    @override
    def showNormal(self) -> None:
        """Show the normal titlebar view."""
        super().showNormal()

    def shade(self, size: "QtCore.QSize") -> None:
        """Shade the window, hiding the main widget and size grip."""

        self._widget.hide()
        if self._statusbar is not None:
            self._statusbar.hide()
        self.setAbsoluteMinimumSize()
        self.resize(size)

    def unshade(self, rect: "QtCore.QRect") -> None:
        """Unshade the window, showing the main widget and size grip."""

        self._widget.show()
        if self._statusbar is not None:
            self._statusbar.show()
        self.expandMinimumSize()
        self.setWindowGeometry(rect)

    def unminimize(self) -> None:
        """Unminimize a minimized window (unimplemented)."""

    # QT EVENTS

    # NOTE: The type ignoring naming is to avoid type checker issues with
    # the random-generated names from PyQt which we use for the type checker.

    @override
    def resizeEvent(self, event: "QtGui.QResizeEvent | None") -> None:  # type: ignore
        """Handle widget resize events here."""

        # Need to trigger the titlebar title resize. Need to handle it
        # here, since the SizeFrame resizes won't always trigger a
        # Label::resizeEvent, which can cause the text to stay elided.
        title_timer = self._titlebar._title._timer
        title_timer.start(REPAINT_TIMER)

        super().resizeEvent(event)

    @override
    def showEvent(self, event: "QtGui.QShowEvent | None") -> None:  # type: ignore
        """Set the minimum size policies once the widgets are shown."""

        # Until shown, the size grip has inaccurate sizes.
        # Set the minimum size policy of the widget.
        # The show event occurs just after everything is shown,
        # so the widget sizes (and isVisible) are accurate.
        self._titlebar_size = self._titlebar.minimumSize()
        if self._statusbar is not None:
            grip_size = self._statusbar.sizeHint()
            self._statusbar_size = Qt.QtCore.QSize(0, grip_size.height())

        self.setMinimumSize(_expand_size(self.absoluteMinimumSize, self.minimumSize()))

        super().showEvent(event)

    @override
    def mouseDoubleClickEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """Override the mouse double click, and don't call the press event."""

        # By default, the flowchart for titlebar double clicks is as follows:
        #   1. If minimized, restore
        #   2. If maximized, restore
        #   3. If no state and can shade, shade
        #   4. If no state and cannot shade, maximize
        #   5. If shaded, unshade.
        widget = self._titlebar
        if event is None or not widget.underMouse() or event.button() != Qt.QtCore.Qt.MouseButton.LeftButton:
            return super().mouseDoubleClickEvent(event)
        if widget._is_shaded:
            return widget.unshade()
        if widget.isMinimized() or widget.isMaximized():
            return widget.restore()
        if widget._has_shade:
            return widget.shade()
        return widget.maximize()

    @override
    def mousePressEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """Override a mouse click on the titlebar to allow a move."""

        titlebar = self._titlebar
        if event is not None and titlebar.underMouse():
            is_left = event.button() == Qt.QtCore.Qt.MouseButton.LeftButton
            is_minimized = self.isMinimized() and not titlebar._is_shaded
            if is_left and not is_minimized and self._window_frame is None:
                self._window_drag = event.pos()
            elif event.button() == Qt.QtCore.Qt.MouseButton.RightButton:
                position = PyQtPosition(event).position()
                PyQtMenu(titlebar._main_menu).exec(position)

        return super().mousePressEvent(event)

    @override
    def mouseMoveEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """Reposition the window on the move event."""

        if self._window_frame is not None:
            self._window_drag = None
        if event is not None and self._window_drag is not None:
            position = event.pos() - self._window_drag
            self.moveTo(self.mapToParent(position))

        return super().mouseMoveEvent(event)

    @override
    def mouseReleaseEvent(self, event: "QtGui.QMouseEvent | None") -> None:  # type: ignore
        """End the drag event."""
        self._window_drag = None
        super().mouseReleaseEvent(event)

    @override
    def changeEvent(self, event: "QtCore.QEvent | None") -> None:  # type: ignore
        """Catch state changes from outside our custom titlebar."""

        super().changeEvent(event)

        # If we're restoring a top-level widget, need to ensure the
        # state is properly restored to the correct icons.
        types = Qt.QtCore.QEvent.Type
        if event is None or event.type() not in (types.ActivationChange, types.WindowStateChange):
            return

        # We have 3 states, and we can have combinations of some of them:
        #   - NoState
        #   - Minimized
        #   - Maximized
        #   - Minimized + Maximized (treat as Minimized).
        state = self.windowState()
        if state & Qt.QtCore.Qt.WindowState.WindowMinimized:
            self._titlebar.minimize()
        elif state & Qt.QtCore.Qt.WindowState.WindowMaximized:
            self._titlebar.maximize()
        else:
            self._titlebar.restore()
