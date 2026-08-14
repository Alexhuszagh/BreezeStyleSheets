#!/usr/bin/env python
"""Test styles of a single widget."""

from collections.abc import MutableSequence, Sequence
from typing import TYPE_CHECKING, Any, Protocol, cast
from typing_extensions import Literal, TypeAlias, TypeVar, get_args

import gc
import os
import random
import sys
import time
from dataclasses import dataclass

from example._util import cli
from example._util.assertions import nonnull
from example._util.qt import PyQt, PyQtApplication, PyQtExec
from example._util.style import style_icon

if TYPE_CHECKING:
    from example._util.typing import QtCore, QtGui, QtWidgets

LayoutType = Literal["vertical", "horizontal"]
AlignmentType = Literal["top", "vcenter", "bottom", "left", "hcenter", "right", "center"]
_W: TypeAlias = "QtWidgets.QWidget"
_Win: TypeAlias = "QtWidgets.QMainWindow"
_A: TypeAlias = "QtWidgets.QApplication"
ButtonT = TypeVar("ButtonT", bound="QtWidgets.QAbstractButton")
Return: TypeAlias = "ZeroReturn | OneReturn | ManyReturn"


@dataclass
class ZeroReturn:
    child: None = None
    layout: None = None
    show: bool = True
    quit: bool = False


@dataclass
class OneReturn:
    child: _W
    layout: LayoutType = "vertical"
    show: bool = True
    quit: bool = False


@dataclass
class ManyReturn:
    child: "Sequence[_W]"
    layout: LayoutType = "vertical"
    show: bool = True
    quit: bool = False


class TestCb(Protocol):
    def __call__(self, widget: _W, window: _Win, app: _A) -> Return: ...


class Args(cli.Args, Protocol):
    widget: str
    width: int
    height: int
    alignment: AlignmentType
    compress: bool
    print_tests: bool
    start: str


class Parser(cli.Parser[Args]):
    def __init__(self) -> None:
        super().__init__()
        self._parser.add_argument(
            "--widget",
            help="widget to test. can provide `all` to test all widgets",
            default="all",
        )
        self._parser.add_argument(
            "--width",
            help="the window width",
            type=int,
            default=1068,
        )
        self._parser.add_argument(
            "--height",
            help="the window height",
            type=int,
            default=824,
        )
        self._parser.add_argument(
            "--alignment",
            help="the layout alignment",
            choices=get_args(AlignmentType),
        )
        self._parser.add_argument(
            "--compress",
            help="add stretch on both sides",
            action="store_true",
        )
        self._parser.add_argument(
            "--print-tests",
            help="print all available tests (widget names).",
            action="store_true",
        )
        self._parser.add_argument(
            "--start",
            help="test widget to start at.",
        )


ARGS, UNKNOWN = Parser().parse()
Qt = PyQt.from_framework(ARGS.qt_framework)
STANDARD_ICONS = Qt.standard_icons
LAYOUT: "dict[LayoutType, type[QtWidgets.QVBoxLayout] | type[QtWidgets.QHBoxLayout]]" = {
    "vertical": Qt.QtWidgets.QVBoxLayout,
    "horizontal": Qt.QtWidgets.QHBoxLayout,
}
ALIGNMENT: "dict[AlignmentType, QtCore.Qt.AlignmentFlag]" = {
    "top": Qt.QtCore.Qt.AlignmentFlag.AlignTop,
    "vcenter": Qt.QtCore.Qt.AlignmentFlag.AlignVCenter,
    "bottom": Qt.QtCore.Qt.AlignmentFlag.AlignBottom,
    "left": Qt.QtCore.Qt.AlignmentFlag.AlignLeft,
    "hcenter": Qt.QtCore.Qt.AlignmentFlag.AlignHCenter,
    "right": Qt.QtCore.Qt.AlignmentFlag.AlignRight,
    "center": Qt.QtCore.Qt.AlignmentFlag.AlignCenter,
}


def is_headless() -> bool:
    """Get if the scripts are running in test mode, that is offscreen."""
    return os.environ.get("QT_QPA_PLATFORM") == "offscreen"


def get_geometry(app: "QtWidgets.QApplication") -> "QtCore.QRect":
    return Qt.QtCore.QRect(0, 0, ARGS.width, int(1.5 * app.font().pointSize()))


def add_widgets(layout: "QtWidgets.QLayout", children: "_W | Sequence[_W]") -> None:
    """Add 1 or more widgets to the layout."""

    if isinstance(children, Sequence):
        for child in children:
            layout.addWidget(child)
    else:
        layout.addWidget(children)


def abstract_button(
    cls: "type[ButtonT]",
    parent: "_W | None" = None,
    *args: Any,
    exclusive: bool = False,
    checked: "bool | QtCore.Qt.CheckState" = False,
    checkable: bool = True,
    enabled: bool = True,
) -> ButtonT:
    """Helper to simplify creating abstract buttons."""

    inst = cls(*args, parent)  # type: ignore
    inst.setAutoExclusive(exclusive)
    inst.setCheckable(checkable)
    if isinstance(checked, bool):
        inst.setChecked(checked)
    else:
        cast("QtWidgets.QCheckBox", inst).setTristate(True)
        cast("QtWidgets.QCheckBox", inst).setCheckState(checked)
    inst.setEnabled(enabled)

    return inst


def splash_timer(splash: "QtWidgets.QSplashScreen", window: _Win) -> None:
    """Non-block timer for a splashscreen."""

    splash.finish(window)
    window.show()


def standard_icon(widget: _W, icon: "QtWidgets.QStyle.StandardPixmap") -> "QtGui.QIcon":
    """Get a standard icon depending on the stylesheet."""
    style = widget.style()
    assert style is not None
    return style_icon(style, Qt, STANDARD_ICONS, ARGS, icon, widget=widget)


def close_icon(widget: _W) -> "QtGui.QIcon":
    """Get the close icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_DockWidgetCloseButton)


def reset_icon(widget: _W) -> "QtGui.QIcon":
    """Get the reset icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_DialogResetButton)


def next_icon(widget: _W) -> "QtGui.QIcon":
    """Get the next icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowRight)


def previous_icon(widget: _W) -> "QtGui.QIcon":
    """Get the previous icon depending on the stylesheet."""
    return standard_icon(widget, Qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowLeft)


def test_progressbar_horizontal(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    bar1 = Qt.QtWidgets.QProgressBar(widget)
    bar1.setProperty("value", 0)
    child.append(bar1)
    bar2 = Qt.QtWidgets.QProgressBar(widget)
    bar2.setProperty("value", 24)
    child.append(bar2)
    bar3 = Qt.QtWidgets.QProgressBar(widget)
    bar3.setProperty("value", 99)
    child.append(bar3)
    bar4 = Qt.QtWidgets.QProgressBar(widget)
    bar4.setProperty("value", 100)
    child.append(bar4)

    return ManyReturn(child)


def test_progressbar_vertical(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    bar1 = Qt.QtWidgets.QProgressBar(widget)
    bar1.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
    bar1.setProperty("value", 0)
    child.append(bar1)
    bar2 = Qt.QtWidgets.QProgressBar(widget)
    bar2.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
    bar2.setProperty("value", 24)
    child.append(bar2)
    bar3 = Qt.QtWidgets.QProgressBar(widget)
    bar3.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
    bar3.setProperty("value", 99)
    child.append(bar3)
    bar4 = Qt.QtWidgets.QProgressBar(widget)
    bar4.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
    bar4.setProperty("value", 100)
    child.append(bar4)

    return ManyReturn(child, "horizontal")


def test_progressbar_inverted(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    bar1 = Qt.QtWidgets.QProgressBar(widget)
    bar1.setProperty("value", 0)
    child.append(bar1)
    bar2 = Qt.QtWidgets.QProgressBar(widget)
    bar2.setProperty("value", 24)
    child.append(bar2)
    bar3 = Qt.QtWidgets.QProgressBar(widget)
    bar3.setProperty("value", 99)
    child.append(bar3)
    bar4 = Qt.QtWidgets.QProgressBar(widget)
    bar4.setProperty("value", 100)
    child.append(bar4)
    for bar in child:
        bar.setInvertedAppearance(True)

    return ManyReturn(child)


def test_progressbar_text(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    bar1 = Qt.QtWidgets.QProgressBar(widget)
    bar1.setProperty("value", 0)
    child.append(bar1)
    bar2 = Qt.QtWidgets.QProgressBar(widget)
    bar2.setProperty("value", 24)
    child.append(bar2)
    bar3 = Qt.QtWidgets.QProgressBar(widget)
    bar3.setProperty("value", 99)
    child.append(bar3)
    bar4 = Qt.QtWidgets.QProgressBar(widget)
    bar4.setProperty("value", 100)
    child.append(bar4)
    for bar in child:
        bar.setTextDirection(Qt.QtWidgets.QProgressBar.Direction.TopToBottom)
        bar.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)

    return ManyReturn(child, "horizontal")


def test_slider_horizontal(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSlider(widget)
    child.setOrientation(Qt.QtCore.Qt.Orientation.Horizontal)

    return OneReturn(child)


def test_slider_vertical(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSlider(widget)
    child.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)

    return OneReturn(child, "horizontal")


def test_tick_slider(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSlider(widget)
    child.setOrientation(Qt.QtCore.Qt.Orientation.Horizontal)
    child.setTickInterval(5)
    child.setTickPosition(Qt.QtWidgets.QSlider.TickPosition.TicksAbove)

    return OneReturn(child)


def test_splitter_horizontal(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSplitter(widget)
    child.addWidget(Qt.QtWidgets.QListWidget())
    child.addWidget(Qt.QtWidgets.QTreeWidget())
    child.addWidget(Qt.QtWidgets.QTextEdit())

    return OneReturn(child)


def test_splitter_vertical(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSplitter(widget)
    child.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
    child.addWidget(Qt.QtWidgets.QListWidget())
    child.addWidget(Qt.QtWidgets.QTreeWidget())
    child.addWidget(Qt.QtWidgets.QTextEdit())

    return OneReturn(child, "horizontal")


def test_large_handle_splitter(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSplitter(widget)
    child.addWidget(Qt.QtWidgets.QListWidget())
    child.addWidget(Qt.QtWidgets.QTreeWidget())
    child.addWidget(Qt.QtWidgets.QTextEdit())
    child.setHandleWidth(child.handleWidth() * 5)

    return OneReturn(child)


def test_nocollapsible_splitter(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QSplitter(widget)
    child.addWidget(Qt.QtWidgets.QListWidget())
    child.addWidget(Qt.QtWidgets.QTreeWidget())
    child.addWidget(Qt.QtWidgets.QTextEdit())
    child.setChildrenCollapsible(False)

    return OneReturn(child)


def test_rubber_band(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QRubberBand(Qt.QtWidgets.QRubberBand.Shape.Line, widget),
        Qt.QtWidgets.QRubberBand(Qt.QtWidgets.QRubberBand.Shape.Rectangle, widget),
    ]

    return ManyReturn(child)


def test_plain_text_edit(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QPlainTextEdit("Edit 1", widget),
        Qt.QtWidgets.QPlainTextEdit("Edit 2", widget),
        Qt.QtWidgets.QPlainTextEdit("Edit 3", widget),
        Qt.QtWidgets.QPlainTextEdit("Edit 4", widget),
        Qt.QtWidgets.QPlainTextEdit("Edit 5", widget),
    ]
    child[1].setBackgroundVisible(True)
    child[2].setCenterOnScroll(True)
    child[3].setCursorWidth(5)
    child[3].setPlaceholderText("Placeholder Text")
    child[4].setReadOnly(True)

    return ManyReturn(child)


def test_menu(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QMenuBar(window)
    child.setGeometry(get_geometry(app))
    menu = Qt.QtWidgets.QMenu("Main Menu", child)
    menu.addAction(Qt.QtGui.QAction("&Action 1", window))
    menu.addAction(Qt.QtGui.QAction("&Action 2", window))
    submenu = Qt.QtWidgets.QMenu("Sub Menu", menu)
    submenu.addAction(Qt.QtGui.QAction("&Action 3", window))
    action1 = Qt.QtGui.QAction("&Action 4", window)
    action1.setCheckable(True)
    submenu.addAction(action1)
    menu.addAction(submenu.menuAction())
    action2 = Qt.QtGui.QAction("&Action 5", window)
    action2.setCheckable(True)
    action2.setChecked(True)
    menu.addSeparator()
    menu.addAction(action2)
    action3 = Qt.QtGui.QAction("&Action 6", window)
    action3.setCheckable(True)
    menu.addAction(action3)
    icon = close_icon(menu)
    menu.addAction(Qt.QtGui.QAction(icon, "&Action 7", window))
    menu.addAction(Qt.QtGui.QAction(icon, "&Action 8", window))
    submenu.addAction(Qt.QtGui.QAction(icon, "&Action 9", window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    file = Qt.QtWidgets.QMenu("File", child)
    file.addAction(Qt.QtGui.QAction("&Open", window))
    file.addAction(Qt.QtGui.QAction("&Close", window))
    child.addAction(file.menuAction())

    edit = Qt.QtWidgets.QMenu("Edit", child)
    edit.addAction(Qt.QtGui.QAction("&Cut", window))
    edit.addAction(Qt.QtGui.QAction("&Copy", window))
    edit.addAction(Qt.QtGui.QAction("&Paste", window))
    child.addAction(edit.menuAction())

    return OneReturn(child)


def _menu(window: _Win, app: _A) -> "tuple[QtWidgets.QMenuBar, QtWidgets.QMenu]":
    child = Qt.QtWidgets.QMenuBar(window)
    child.setGeometry(get_geometry(app))
    menu = Qt.QtWidgets.QMenu("Main Menu", child)
    menu.addAction(Qt.QtGui.QAction("&Action 1", window))
    menu.addAction(Qt.QtGui.QAction("&Action 2", window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return (child, menu)


def test_native_menu(_widget: _W, window: _Win, app: _A) -> OneReturn:
    child, _ = _menu(window, app)
    child.setNativeMenuBar(True)

    return OneReturn(child)


def test_popup_menu(_widget: _W, window: _Win, app: _A) -> OneReturn:
    child, _ = _menu(window, app)
    child.setDefaultUp(True)

    return OneReturn(child)


def test_tearoff_menu(_widget: _W, window: _Win, app: _A) -> OneReturn:
    child, menu = _menu(window, app)
    menu.setTearOffEnabled(True)

    return OneReturn(child)


def test_icon_menu(widget: _W, window: _Win, app: _A) -> OneReturn:
    child, menu = _menu(window, app)
    menu.setIcon(close_icon(widget))

    return OneReturn(child)


def test_collapsible_separators_menu(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QMenuBar(window)
    child.setGeometry(get_geometry(app))
    menu = Qt.QtWidgets.QMenu("Main Menu", child)
    menu.addSeparator()
    menu.addAction(Qt.QtGui.QAction("&Action 1", window))
    menu.addSeparator()
    menu.addSeparator()
    menu.addAction(Qt.QtGui.QAction("&Action 2", window))
    menu.addSeparator()
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setSeparatorsCollapsible(True)

    return OneReturn(child)


def test_tooltips_menu(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QMenuBar(window)
    child.setGeometry(get_geometry(app))
    menu = Qt.QtWidgets.QMenu("Main Menu", child)
    action1 = Qt.QtGui.QAction("&Action 1", window)
    action1.setToolTip("Action 1")
    menu.addAction(action1)
    action2 = Qt.QtGui.QAction("&Action 2", window)
    action2.setToolTip("Action 1")
    menu.addAction(action2)
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setToolTipsVisible(True)

    return OneReturn(child)


def test_mdi_area(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QMdiArea(widget)
    child.addSubWindow(Qt.QtWidgets.QMdiSubWindow())
    subwindow = Qt.QtWidgets.QMdiSubWindow()
    flags = subwindow.windowFlags()
    flags |= Qt.QtCore.Qt.WindowType.WindowContextHelpButtonHint
    flags |= Qt.QtCore.Qt.WindowType.WindowShadeButtonHint
    subwindow.setWindowFlags(flags)
    subwindow.setWindowTitle("Subwindow")
    child.addSubWindow(subwindow)

    return OneReturn(child)


def test_partial_mdi_area(widget: _W, window: _Win, app: _A) -> ManyReturn:
    first = Qt.QtWidgets.QWidget()
    area = Qt.QtWidgets.QMdiArea(widget)
    first.setMinimumSize(200, 200)
    area.addSubWindow(Qt.QtWidgets.QMdiSubWindow())
    subwindow = Qt.QtWidgets.QMdiSubWindow()
    flags = subwindow.windowFlags()
    flags |= Qt.QtCore.Qt.WindowType.WindowContextHelpButtonHint
    flags |= Qt.QtCore.Qt.WindowType.WindowShadeButtonHint
    subwindow.setWindowFlags(flags)
    subwindow.setWindowTitle("Subwindow")
    area.addSubWindow(subwindow)

    return ManyReturn([first, area])


def test_statusbar(_widget: _W, window: _Win, _app: _A) -> OneReturn:
    child = Qt.QtWidgets.QStatusBar(window)
    window.setStatusBar(child)

    return OneReturn(child)


def test_no_sizegrip_statusbar(_widget: _W, window: _Win, _app: _A) -> OneReturn:
    child = Qt.QtWidgets.QStatusBar(window)
    child.setSizeGripEnabled(False)
    window.setStatusBar(child)

    return OneReturn(child)


def test_spinbox(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    spin1 = Qt.QtWidgets.QSpinBox(widget)
    spin1.setValue(10)
    child.append(spin1)
    spin2 = Qt.QtWidgets.QSpinBox(widget)
    spin2.setValue(10)
    spin2.setPrefix("$")
    spin2.setSuffix("%")
    spin2.setEnabled(False)
    child.append(spin2)

    return ManyReturn(child, "horizontal")


def test_double_spinbox(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    spin1 = Qt.QtWidgets.QDoubleSpinBox(widget)
    spin1.setValue(10.5)
    child.append(spin1)
    spin2 = Qt.QtWidgets.QDoubleSpinBox(widget)
    spin2.setValue(10.5)
    spin2.setEnabled(False)
    spin2.setPrefix("$")
    spin2.setSuffix("%")
    child.append(spin2)

    return ManyReturn(child, "horizontal")


def test_combobox(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    combo1 = Qt.QtWidgets.QComboBox(widget)
    combo1.addItem("Item 1")
    combo1.addItem("Item 2")
    child.append(combo1)
    combo2 = Qt.QtWidgets.QComboBox(widget)
    combo2.addItem("Very Very Long Item 1")
    combo2.addItem("Very Very Long Item 2")
    child.append(combo2)
    combo3 = Qt.QtWidgets.QComboBox(widget)
    combo3.setEditable(True)
    combo3.addItem("Edit 1")
    combo3.addItem("Edit 2")
    nonnull(combo3.lineEdit()).setPlaceholderText("Placeholder")
    child.append(combo3)
    combo4 = Qt.QtWidgets.QComboBox(widget)
    combo4.addItem("Item 1")
    combo4.addItem("Item 2")
    combo4.addItem("Item 3")
    combo4.addItem("Item 4")
    combo4.addItem("Item 5")
    combo4.addItem("Item 6")
    combo4.setMaxVisibleItems(5)
    child.append(combo4)

    return ManyReturn(child, "horizontal")


def _test_tabwidget(widget: _W, position: "QtWidgets.QTabWidget.TabPosition") -> "QtWidgets.QTabWidget":
    child = Qt.QtWidgets.QTabWidget(widget)
    child.setTabPosition(position)
    child.addTab(Qt.QtWidgets.QWidget(), "Tab 1")
    child.addTab(Qt.QtWidgets.QWidget(), "Tab 2")
    child.addTab(Qt.QtWidgets.QWidget(), "Tab 3")

    return child


def test_tabwidget_top(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    return OneReturn(child)


def test_tabwidget_left(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.West)
    return OneReturn(child)


def test_tabwidget_right(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.East)
    return OneReturn(child)


def test_tabwidget_bottom(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.South)
    return OneReturn(child)


def test_autohide_tabwidget(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []

    item1 = Qt.QtWidgets.QTabWidget(widget)
    item1.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
    item1.addTab(QtWidgets.QWidget(), "Tab 1")
    item1.setTabBarAutoHide(True)
    child.append(item1)

    item2 = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.East)
    item2.setTabBarAutoHide(True)
    child.append(item2)

    return ManyReturn(child)


def test_nonexpanding_tabwidget(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    nonnull(child.tabBar()).setExpanding(False)

    return OneReturn(child)


def test_movable_tabwidget(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    nonnull(child.tabBar()).setMovable(True)

    return OneReturn(child)


def test_closable_tabwidget_top(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    child.setTabsClosable(True)

    return OneReturn(child)


def test_closable_tabwidget_right(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.East)
    child.setTabsClosable(True)

    return OneReturn(child)


def test_use_scroll_tabwidget(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QTabWidget(widget)
    child.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
    for i in range(1, 100):
        child.addTab(QtWidgets.QWidget(), f"Tab {i}")
    child.setUsesScrollButtons(True)

    return OneReturn(child)


def test_no_scroll_tabwidget(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QTabWidget(widget)
    child.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
    for i in range(1, 100):
        child.addTab(QtWidgets.QWidget(), f"Tab {i}")
    child.setUsesScrollButtons(False)

    return OneReturn(child)


def test_rounded_tabwidget_north(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Rounded)

    return OneReturn(child)


def test_triangle_tabwidget_north(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)

    return OneReturn(child)


def test_rounded_tabwidget_east(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.East)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Rounded)

    return OneReturn(child)


def test_triangle_tabwidget_east(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.East)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)

    return OneReturn(child)


def test_rounded_tabwidget_west(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.West)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Rounded)

    return OneReturn(child)


def test_triangle_tabwidget_west(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.West)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)

    return OneReturn(child)


def test_rounded_tabwidget_south(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.South)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Rounded)

    return OneReturn(child)


def test_triangle_tabwidget_south(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.South)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)

    return OneReturn(child)


def test_closable_triangle_tabwidget_north(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.North)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)
    child.setTabsClosable(True)

    return OneReturn(child)


def test_closable_triangle_tabwidget_south(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.South)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)
    child.setTabsClosable(True)

    return OneReturn(child)


def test_closable_triangle_tabwidget_east(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.East)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)
    child.setTabsClosable(True)

    return OneReturn(child)


def test_closable_triangle_tabwidget_west(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _test_tabwidget(widget, Qt.QtWidgets.QTabWidget.TabPosition.West)
    child.setTabShape(Qt.QtWidgets.QTabWidget.TabShape.Triangular)
    child.setTabsClosable(True)

    return OneReturn(child)


def test_button_position_tabwidget(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QTabWidget(widget)
    child.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
    for i in range(1, 10):
        child.addTab(QtWidgets.QWidget(), f"Tab {i}")
        if i % 2 == 0:
            side = Qt.QtWidgets.QTabBar.ButtonPosition.LeftSide
        else:
            side = Qt.QtWidgets.QTabBar.ButtonPosition.RightSide
        nonnull(child.tabBar()).setTabButton(i - 1, side, Qt.QtWidgets.QWidget(widget))
    child.setUsesScrollButtons(True)

    return OneReturn(child)


def test_text_browser(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QTextBrowser(widget)
    child.setOpenExternalLinks(True)
    child.setMarkdown("[QTextBrowser](https://doc.qt.io/qt-6/qtextbrowser.html)")

    return OneReturn(child)


def test_dock(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    all_features = (
        Qt.QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable
        | Qt.QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable
        | Qt.QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable
    )
    dock1 = Qt.QtWidgets.QDockWidget("&Dock widget 1", window)
    dock1.setFeatures(all_features)
    dock2 = Qt.QtWidgets.QDockWidget("&Dock widget 2", window)
    dock2.setFeatures(all_features)
    dock3 = Qt.QtWidgets.QDockWidget("&Dock widget 3", window)
    dock3.setFeatures(Qt.QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar)
    window.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock1)
    window.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock2)
    window.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock3)
    window.tabifyDockWidget(dock1, dock2)

    return ZeroReturn()


def test_radio(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    widget_type = Qt.QtWidgets.QRadioButton
    child.append(abstract_button(widget_type, widget))
    child.append(abstract_button(widget_type, widget, checked=True))
    child.append(abstract_button(widget_type, widget, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=True, enabled=False))
    child.append(abstract_button(widget_type, widget, "With Text"))

    return ManyReturn(child)


def test_checkbox(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    widget_type = Qt.QtWidgets.QCheckBox
    partial = Qt.QtCore.Qt.CheckState.PartiallyChecked
    child.append(abstract_button(widget_type, widget))
    child.append(abstract_button(widget_type, widget, checked=True))
    child.append(abstract_button(widget_type, widget, checked=partial))
    child.append(abstract_button(widget_type, widget, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=True, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=partial, enabled=False))
    child.append(abstract_button(widget_type, widget, "With Text"))
    child.append(abstract_button(widget_type, widget, "With Large Text"))
    checkbox_font = app.font()
    checkbox_font.setPointSizeF(50.0)
    child[-1].setFont(checkbox_font)

    return ManyReturn(child)


def _get_table(widget: _W) -> "QtWidgets.QTableWidget":
    child = Qt.QtWidgets.QTableWidget(widget)
    child.setColumnCount(2)
    child.setRowCount(4)
    item = Qt.QtWidgets.QTableWidgetItem("Row 1")
    child.setVerticalHeaderItem(0, item)
    item = Qt.QtWidgets.QTableWidgetItem("Row 2")
    child.setVerticalHeaderItem(1, item)
    item = Qt.QtWidgets.QTableWidgetItem("Row 3")
    child.setVerticalHeaderItem(2, item)
    item = Qt.QtWidgets.QTableWidgetItem("Row 4")
    child.setVerticalHeaderItem(3, item)
    item = Qt.QtWidgets.QTableWidgetItem("Column 1")
    child.setHorizontalHeaderItem(0, item)
    item = Qt.QtWidgets.QTableWidgetItem("Column 2")
    child.setHorizontalHeaderItem(1, item)

    return child


def test_table(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(_get_table(widget))


def test_sortable_table(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    child.setSortingEnabled(True)

    return OneReturn(child)


def test_nocorner_table(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    child.setCornerButtonEnabled(False)

    return OneReturn(child)


def test_nogrid_table(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    child.setShowGrid(False)

    return OneReturn(child)


def test_gridstyle_table(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    child.setGridStyle(Qt.QtCore.Qt.PenStyle.DotLine)

    return OneReturn(child)


def test_nohighlight_header_view(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    nonnull(child.horizontalHeader()).setHighlightSections(False)

    return OneReturn(child)


def test_movable_header_view(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    nonnull(child.horizontalHeader()).setSectionsMovable(True)

    return OneReturn(child)


def test_noclick_header_view(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = _get_table(widget)
    nonnull(child.horizontalHeader()).setSectionsClickable(False)

    return OneReturn(child)


def test_list(widget: _W, window: _Win, app: _A) -> OneReturn:
    alignments = [
        Qt.QtCore.Qt.AlignmentFlag.AlignLeft,
        Qt.QtCore.Qt.AlignmentFlag.AlignRight,
        Qt.QtCore.Qt.AlignmentFlag.AlignHCenter,
    ]
    child = Qt.QtWidgets.QListWidget(widget)
    for index in range(10):
        item = Qt.QtWidgets.QListWidgetItem(f"Item {index + 1}")
        item.setTextAlignment(random.choice(alignments))
        child.addItem(item)
    icon = close_icon(child)
    for index in range(10):
        item = Qt.QtWidgets.QListWidgetItem(icon, f"Item {index + 1}")
        item.setTextAlignment(random.choice(alignments))
        child.addItem(item)

    return OneReturn(child)


def test_sortable_list(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QListWidget(widget)
    child.setSortingEnabled(True)
    for index in range(10):
        item = Qt.QtWidgets.QListWidgetItem(f"Item {index + 1}")
        child.addItem(item)

    return OneReturn(child)


def test_editable_list(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QListWidget(widget)
    child.setSortingEnabled(True)
    for index in range(10):
        item = Qt.QtWidgets.QListWidgetItem(f"Item {index + 1}")
        item.setFlags(item.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsEditable)
        child.addItem(item)

    return OneReturn(child)


def test_key_sequence_edit(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QKeySequenceEdit(widget))


def test_completer(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit(widget)
    completer = Qt.QtWidgets.QCompleter(["Fruit", "Fruits Basket", "Fruba"])
    child.setCompleter(completer)

    return OneReturn(child)


def test_scrollbar_vertical(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QListWidget(widget)
    for index in range(100):
        child.addItem(Qt.QtWidgets.QListWidgetItem(f"Item {index + 1}"))

    return OneReturn(child)


def test_scrollbar_horizontal(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QTableWidget(widget)
    child.setColumnCount(100)
    child.setRowCount(1)
    item = Qt.QtWidgets.QTableWidgetItem("Row 1")
    child.setVerticalHeaderItem(0, item)
    for index in range(100):
        item = Qt.QtWidgets.QTableWidgetItem(f"Column {index + 1}")
        child.setHorizontalHeaderItem(index, item)

    return OneReturn(child)


def test_toolbar(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    toolbar1 = Qt.QtWidgets.QToolBar("Toolbar")
    toolbar1.addAction("&Action 1")
    toolbar1.addAction("&Action 2")
    toolbar1.addSeparator()
    toolbar1.addAction("&Action 3")
    toolbar1.addAction("&Action 3 Really Long Name")
    icon = close_icon(toolbar1)
    toolbar1.addAction(icon, "&Action 4")
    toolbar1.setMovable(False)
    window.addToolBar(Qt.QtCore.Qt.ToolBarArea.TopToolBarArea, toolbar1)

    toolbar2 = Qt.QtWidgets.QToolBar("Toolbar")
    toolbar2.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
    toolbar2.addAction("&Action 1")
    action2 = Qt.QtGui.QAction("&Action 2", window)
    action2.setStatusTip("Status tip")
    action2.setWhatsThis("Example action")
    toolbar2.addAction(action2)
    toolbar2.addSeparator()
    toolbar2.addAction("&Action 3")
    toolbar2.addAction("&Action 3 Really Long Name")
    toolbar2.addAction(Qt.QtWidgets.QWhatsThis.createAction(toolbar2))
    icon = close_icon(toolbar2)
    toolbar2.addAction(icon, "&Action 4")
    toolbar2.setFloatable(True)
    toolbar2.setMovable(True)
    window.addToolBar(Qt.QtCore.Qt.ToolBarArea.LeftToolBarArea, toolbar2)

    statusbar = Qt.QtWidgets.QStatusBar(window)
    window.setStatusBar(statusbar)

    return ZeroReturn()


def test_toolbutton(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    window.setTabOrder(child[3], child[4])
    window.setTabOrder(child[4], child[5])
    window.setTabOrder(child[5], child[6])
    window.setTabOrder(child[6], child[7])
    child[0].setText("Simple ToolButton")
    child[1].setText("Action Toolbutton")
    child[2].setText("Menu Toolbutton")
    child[3].setText("Instant Toolbutton")
    child[1].addActions([
        Qt.QtGui.QAction("&Action 5", window),
        Qt.QtGui.QAction("&Action 6", window),
    ])
    child[2].setPopupMode(Qt.QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
    child[2].addActions([
        Qt.QtGui.QAction("&Action 9", window),
        Qt.QtGui.QAction("&Action 10", window),
    ])
    child[3].setPopupMode(Qt.QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
    child[3].addActions([
        Qt.QtGui.QAction("&Action 11", window),
        Qt.QtGui.QAction("&Action 12", window),
    ])
    child[4].setArrowType(Qt.QtCore.Qt.ArrowType.LeftArrow)
    child[5].setArrowType(Qt.QtCore.Qt.ArrowType.RightArrow)
    child[6].setArrowType(Qt.QtCore.Qt.ArrowType.UpArrow)
    child[7].setArrowType(Qt.QtCore.Qt.ArrowType.DownArrow)
    icon = close_icon(widget)
    child[8].setIcon(icon)

    return ManyReturn(child, "horizontal")


def test_raised_toolbutton(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    child[0].setArrowType(Qt.QtCore.Qt.ArrowType.LeftArrow)
    child[1].setArrowType(Qt.QtCore.Qt.ArrowType.RightArrow)
    child[2].setArrowType(Qt.QtCore.Qt.ArrowType.UpArrow)
    child[3].setArrowType(Qt.QtCore.Qt.ArrowType.DownArrow)
    for item in child:
        item.setAutoRaise(True)

    return ManyReturn(child, "horizontal")


def test_toolbutton_style(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    window.setTabOrder(child[3], child[4])
    window.setTabOrder(child[4], child[5])
    window.setTabOrder(child[5], child[6])
    window.setTabOrder(child[6], child[7])
    window.setTabOrder(child[7], child[8])
    window.setTabOrder(child[8], child[9])
    child[0].setText("Button 1")
    child[1].setText("Button 2")
    child[2].setText("Button 3")
    child[3].setText("Button 4")
    child[4].setText("Button 5")
    child[5].setText("Button 6")
    child[6].setText("Button 7")
    child[7].setText("Button 8")
    child[8].setText("Button 9")
    child[9].setText("Button 10")
    child[0].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
    child[1].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
    child[2].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
    child[3].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    child[4].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonFollowStyle)
    child[5].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
    child[6].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly)
    child[7].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
    child[8].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    child[9].setToolButtonStyle(Qt.QtCore.Qt.ToolButtonStyle.ToolButtonFollowStyle)
    icon = close_icon(widget)
    for item in child:
        item.setIcon(icon)
    for item in child[5:]:
        item.setAutoRaise(True)

    return ManyReturn(child, "horizontal")


def test_toolbutton_menu(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
        Qt.QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    child[0].setText("Button 1")
    child[1].setText("Button 2")
    child[2].setText("Button 3")
    child[3].setText("Button 4")
    child[1].addActions([
        Qt.QtGui.QAction("&Action 5", window),
        Qt.QtGui.QAction("&Action 6", window),
    ])
    child[2].setPopupMode(Qt.QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
    child[2].addActions([
        Qt.QtGui.QAction("&Action 9", window),
        Qt.QtGui.QAction("&Action 10", window),
    ])
    child[3].setPopupMode(Qt.QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
    child[3].addActions([
        Qt.QtGui.QAction("&Action 11", window),
        Qt.QtGui.QAction("&Action 12", window),
    ])
    child[0].setProperty("hasMenu", False)
    # Incorrectly trims this normally... but set hasMenu true
    child[1].setAutoRaise(True)
    child[1].setProperty("hasMenu", True)

    return ManyReturn(child, "horizontal")


def test_pushbutton(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    widget_type = Qt.QtWidgets.QPushButton
    child.append(abstract_button(widget_type, widget, "Button 1", checked=True))
    child.append(abstract_button(widget_type, widget, "Button 2", enabled=False))
    child.append(abstract_button(widget_type, widget, "Button 3", checkable=False))
    icon = close_icon(widget)
    child.append(abstract_button(widget_type, widget, icon, "Button 4", checkable=False))
    flat = Qt.QtWidgets.QPushButton("Flat")
    flat.setFlat(True)
    child.append(flat)
    auto_default = Qt.QtWidgets.QPushButton("Auto Default")
    auto_default.setAutoDefault(True)
    child.append(auto_default)

    return ManyReturn(child, "horizontal")


def test_column_view(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QColumnView(widget)
    model = Qt.QtGui.QFileSystemModel(widget)
    model.setRootPath("/")
    child.setModel(model)
    child.setResizeGripsVisible(True)

    return OneReturn(child)


def test_nosizegrip_column_view(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QColumnView(widget)
    model = Qt.QtGui.QFileSystemModel(widget)
    model.setRootPath("/")
    child.setModel(model)
    child.setResizeGripsVisible(False)

    return OneReturn(child)


def test_comprehensive_frame(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
        Qt.QtWidgets.QFrame(widget),
    ]
    child[0].setFrameShape(Qt.QtWidgets.QFrame.Shape.NoFrame)
    child[1].setFrameShape(Qt.QtWidgets.QFrame.Shape.Box)
    child[2].setFrameShape(Qt.QtWidgets.QFrame.Shape.Panel)
    child[3].setFrameShape(Qt.QtWidgets.QFrame.Shape.StyledPanel)
    child[4].setFrameShape(Qt.QtWidgets.QFrame.Shape.HLine)
    child[5].setFrameShape(Qt.QtWidgets.QFrame.Shape.VLine)
    child[6].setFrameShape(Qt.QtWidgets.QFrame.Shape.WinPanel)
    child[7].setFrameStyle(cast(int, Qt.QtWidgets.QFrame.StyleMask.Shadow_Mask))
    child[8].setFrameStyle(cast(int, Qt.QtWidgets.QFrame.StyleMask.Shape_Mask))
    child[9].setFrameShadow(Qt.QtWidgets.QFrame.Shadow.Plain)
    child[10].setFrameShadow(Qt.QtWidgets.QFrame.Shadow.Raised)
    child[11].setFrameShadow(Qt.QtWidgets.QFrame.Shadow.Sunken)
    for item in child[7:]:
        item.setFrameShape(Qt.QtWidgets.QFrame.Shape.StyledPanel)

    return ManyReturn(child)


def test_tree(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    tree1 = Qt.QtWidgets.QTreeWidget(widget)
    tree1.setHeaderLabel("Tree 1")
    item1 = Qt.QtWidgets.QTreeWidgetItem(tree1, ["Row 1"])
    item2 = Qt.QtWidgets.QTreeWidgetItem(tree1, ["Row 2"])
    item3 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.1"])
    item3.setFlags(item3.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item3.setCheckState(0, Qt.QtCore.Qt.CheckState.Unchecked)
    item4 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.2"])
    item5 = Qt.QtWidgets.QTreeWidgetItem(item4, ["Row 2.2.1"])
    item6 = Qt.QtWidgets.QTreeWidgetItem(item5, ["Row 2.2.1.1"])
    item7 = Qt.QtWidgets.QTreeWidgetItem(item5, ["Row 2.2.1.2"])
    item7.setFlags(item7.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item7.setCheckState(0, Qt.QtCore.Qt.CheckState.Checked)
    item8 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.3"])
    item8.setFlags(item8.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserTristate)
    item8.setCheckState(0, Qt.QtCore.Qt.CheckState.PartiallyChecked)
    item9 = Qt.QtWidgets.QTreeWidgetItem(tree1, ["Row 3"])
    item10 = Qt.QtWidgets.QTreeWidgetItem(item9, ["Row 3.1"])
    item11 = Qt.QtWidgets.QTreeWidgetItem(tree1, ["Row 4"])
    child.append(tree1)
    tree2 = Qt.QtWidgets.QTreeWidget(widget)
    tree2.setHeaderLabel("Tree 2")
    nonnull(tree2.header()).setSectionsClickable(True)
    item12 = Qt.QtWidgets.QTreeWidgetItem(tree2, ["Row 1", "Column 2", "Column 3"])
    child.append(tree2)

    return ManyReturn(child)


def test_sortable_tree(widget: _W, window: _Win, app: _A) -> OneReturn:
    tree = Qt.QtWidgets.QTreeWidget(widget)
    tree.setObjectName("treeWidget")
    item_0 = Qt.QtWidgets.QTreeWidgetItem(tree)
    item_1 = Qt.QtWidgets.QTreeWidgetItem(tree)
    item_2 = Qt.QtWidgets.QTreeWidgetItem(item_1)
    item_2.setText(0, "subitem")
    item_3 = Qt.QtWidgets.QTreeWidgetItem(item_2, ["Row 2.1"])
    item_3.setFlags(item_3.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item_3.setCheckState(0, Qt.QtCore.Qt.CheckState.Unchecked)
    item_4 = Qt.QtWidgets.QTreeWidgetItem(item_2, ["Row 2.2"])
    item_5 = Qt.QtWidgets.QTreeWidgetItem(item_4, ["Row 2.2.1"])
    item_6 = Qt.QtWidgets.QTreeWidgetItem(item_5, ["Row 2.2.1.1"])
    item_7 = Qt.QtWidgets.QTreeWidgetItem(item_5, ["Row 2.2.1.2"])
    item_3.setFlags(item_7.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item_7.setCheckState(0, Qt.QtCore.Qt.CheckState.Checked)
    item_8 = Qt.QtWidgets.QTreeWidgetItem(item_2, ["Row 2.3"])
    item_8.setFlags(item_8.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserTristate)
    item_8.setCheckState(0, Qt.QtCore.Qt.CheckState.PartiallyChecked)
    item_9 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 3"])
    item_10 = Qt.QtWidgets.QTreeWidgetItem(item_9, ["Row 3.1"])
    item_11 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 4"])

    nonnull(tree.headerItem()).setText(0, "qdz")
    tree.setSortingEnabled(False)
    nonnull(tree.topLevelItem(0)).setText(0, "qzd")
    nonnull(tree.topLevelItem(1)).setText(0, "effefe")
    tree.setSortingEnabled(True)

    return OneReturn(tree)


def test_editable_tree(widget: _W, window: _Win, app: _A) -> ManyReturn:
    def new_item(widget, columns):
        item = Qt.QtWidgets.QTreeWidgetItem(widget, columns)
        item.setFlags(item.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsEditable)
        return item

    child = []
    tree1 = Qt.QtWidgets.QTreeWidget(widget)
    tree1.setHeaderLabel("Tree 1")
    item1 = new_item(tree1, ["Row 1"])
    item2 = new_item(tree1, ["Row 2"])
    item3 = new_item(item2, ["Row 2.1"])
    item3.setFlags(item3.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item3.setCheckState(0, Qt.QtCore.Qt.CheckState.Unchecked)
    item4 = new_item(item2, ["Row 2.2"])
    item5 = new_item(item4, ["Row 2.2.1"])
    item6 = new_item(item5, ["Row 2.2.1.1"])
    item7 = new_item(item5, ["Row 2.2.1.2"])
    item7.setFlags(item7.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserCheckable)
    item7.setCheckState(0, Qt.QtCore.Qt.CheckState.Checked)
    item8 = new_item(item2, ["Row 2.3"])
    item8.setFlags(item8.flags() | Qt.QtCore.Qt.ItemFlag.ItemIsUserTristate)
    item8.setCheckState(0, Qt.QtCore.Qt.CheckState.PartiallyChecked)
    item9 = new_item(tree1, ["Row 3"])
    item10 = new_item(item9, ["Row 3.1"])
    item11 = new_item(tree1, ["Row 4"])
    child.append(tree1)
    tree2 = Qt.QtWidgets.QTreeWidget(widget)
    tree2.setHeaderLabel("Tree 2")
    nonnull(tree2.header()).setSectionsClickable(True)
    item12 = new_item(tree2, ["Row 1", "Column 2", "Column 3"])
    child.append(tree2)

    return ManyReturn(child)


def test_hidden_header_tree(widget: _W, window: _Win, app: _A) -> OneReturn:
    tree = Qt.QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel("Tree 1")
    item1 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 1"])
    item2 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 2"])
    item3 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.1"])

    tree.setHeaderHidden(True)

    return OneReturn(tree)


def test_indented_tree(widget: _W, window: _Win, app: _A) -> OneReturn:
    tree = Qt.QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel("Tree 1")
    item1 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 1"])
    item2 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 2"])
    item3 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.1", "Row 2.2"])

    tree.setIndentation(tree.indentation() * 2)
    tree.setColumnCount(2)
    tree.setColumnWidth(0, tree.columnWidth(0) * 2)
    tree.setColumnWidth(1, tree.columnWidth(1) * 2)

    return OneReturn(tree)


def test_all_focus_tree(widget: _W, window: _Win, app: _A) -> OneReturn:
    tree = Qt.QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel("Tree 1")
    item1 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 1"])
    item2 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 2"])
    item3 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.1", "Row 2.2"])

    tree.setAllColumnsShowFocus(True)
    tree.setColumnCount(2)

    return OneReturn(tree)


def test_nonexpandable_tree(widget: _W, window: _Win, app: _A) -> OneReturn:
    tree = Qt.QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel("Tree 1")
    item1 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 1"])
    item2 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 2"])
    item3 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.1"])

    tree.setItemsExpandable(False)

    return OneReturn(tree)


def test_undecorated_tree(widget: _W, window: _Win, app: _A) -> OneReturn:
    tree = Qt.QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel("Tree 1")
    item1 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 1"])
    item2 = Qt.QtWidgets.QTreeWidgetItem(tree, ["Row 2"])
    item3 = Qt.QtWidgets.QTreeWidgetItem(item2, ["Row 2.1"])

    tree.setRootIsDecorated(False)

    return OneReturn(tree)


def test_view_scrollarea(widget: _W, window: _Win, app: _A) -> OneReturn:
    # For us to have both scrollbars visible.
    child = Qt.QtWidgets.QTableWidget(widget)
    child.setColumnCount(100)
    child.setRowCount(100)
    for index in range(100):
        row = Qt.QtWidgets.QTableWidgetItem(f"Row {index + 1}")
        child.setVerticalHeaderItem(index, row)
        column = Qt.QtWidgets.QTableWidgetItem(f"Column {index + 1}")
        child.setHorizontalHeaderItem(index, column)

    return OneReturn(child)


def test_widget_scrollarea(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QProgressBar(widget)
    window.setMinimumSize(300, 100)
    child.setProperty("value", 24)
    window.resize(30, 30)

    return OneReturn(child)


def test_frame(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child: "MutableSequence[_W]" = []
    text = Qt.QtWidgets.QTextEdit()
    text.setPlainText("Hello world\nTesting lines")
    child.append(text)
    table = Qt.QtWidgets.QTableWidget()
    table.setColumnCount(5)
    table.setRowCount(5)
    child.append(table)

    return ManyReturn(child)


def test_groupbox(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = []
    groupbox = Qt.QtWidgets.QGroupBox("Groupbox 1", widget)
    vbox1 = Qt.QtWidgets.QVBoxLayout(groupbox)
    vbox1.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignHCenter)
    vbox1.addWidget(QtWidgets.QLineEdit("Sample Label"))
    child.append(groupbox)
    checkable = Qt.QtWidgets.QGroupBox("Groupbox 2", widget)
    checkable.setCheckable(True)
    child.append(checkable)
    vbox = Qt.QtWidgets.QVBoxLayout(checkable)
    vbox.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignHCenter)
    vbox.addWidget(QtWidgets.QLineEdit("Sample Label"))
    flat = Qt.QtWidgets.QGroupBox("Groupbox 3", widget)
    flat.setFlat(True)
    child.append(flat)

    return ManyReturn(child)


def test_dial(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [QtWidgets.QDial(widget), Qt.QtWidgets.QDial(widget)]
    child[1].setNotchesVisible(True)
    for item in child:
        item.setMinimum(0)
        item.setMaximum(100)
        item.setValue(30)

    return ManyReturn(child)


def test_command_link(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QWidget(widget)
    layout = Qt.QtWidgets.QVBoxLayout()
    layout.addStretch(1)
    next = Qt.QtWidgets.QCommandLinkButton("Next", "Go next", widget)
    next.setIcon(next_icon(next))
    layout.addWidget(next)
    previous = Qt.QtWidgets.QCommandLinkButton("Previous", "Go previous", widget)
    previous.setFlat(True)
    previous.setIcon(previous_icon(previous))
    layout.addWidget(previous)
    layout.addWidget(Qt.QtWidgets.QCommandLinkButton("Text Only", widget))
    layout.addStretch(1)

    child.setLayout(layout)

    return OneReturn(child)


def test_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QLineEdit("Sample label", widget))


def test_placeholder_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setPlaceholderText("Placeholder")

    return OneReturn(child)


def test_readonly_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setReadOnly(True)

    return OneReturn(child)


def test_noframe_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setFrame(False)

    return OneReturn(child)


def test_noecho_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setEchoMode(Qt.QtWidgets.QLineEdit.EchoMode.NoEcho)

    return OneReturn(child)


def test_password_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setEchoMode(Qt.QtWidgets.QLineEdit.EchoMode.Password)

    return OneReturn(child)


def test_password_edit_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setEchoMode(Qt.QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)

    return OneReturn(child)


def test_clear_lineedit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLineEdit("Sample label", widget)
    child.setClearButtonEnabled(True)

    return OneReturn(child)


def test_label(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QLabel("Sample label"))


def test_indented_label(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLabel("Sample label")
    child.setIndent(50)

    return OneReturn(child)


def test_markdown_label(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QLabel(),
        Qt.QtWidgets.QLabel(),
    ]
    child[0].setText("[BreezeStyleSheets](https://github.com/Alexhuszagh/BreezeStyleSheets)")
    child[0].setOpenExternalLinks(True)
    child[1].setText("# Sample Header\n- Bullet 1\n- Bullet 2")

    for item in child:
        item.setTextFormat(Qt.QtCore.Qt.TextFormat.MarkdownText)

    return ManyReturn(child)


def test_selectable_label(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLabel("Selectable label")
    child.setTextInteractionFlags(Qt.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

    return OneReturn(child)


def test_editable_label(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLabel("Editable label")
    child.setTextInteractionFlags(Qt.QtCore.Qt.TextInteractionFlag.TextEditorInteraction)

    return OneReturn(child)


def test_font_combobox(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QFontComboBox(widget))


def test_toolbox(widget: _W, window: _Win, app: _A) -> ManyReturn:
    # Test alignment with another item, in a vertical layout.
    child: "MutableSequence[_W]" = []
    child.append(Qt.QtWidgets.QGroupBox("Groupbox", widget))
    child.append(Qt.QtWidgets.QGroupBox("Really, really long groupbox", widget))
    toolbox = Qt.QtWidgets.QToolBox(widget)
    child.append(toolbox)
    page1 = Qt.QtWidgets.QWidget()
    toolbox.addItem(page1, "Page 1")
    page2 = Qt.QtWidgets.QWidget()
    vbox = Qt.QtWidgets.QVBoxLayout(page2)
    vbox.addWidget(Qt.QtWidgets.QLabel("Sample Label"))
    toolbox.addItem(page2, "Page 2")
    page3 = Qt.QtWidgets.QWidget()
    toolbox.addItem(page3, "Really, really long page 3")

    return ManyReturn(child)


def test_menubutton(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QToolButton(widget)
    child.setText("Menu Toolbutton")
    child.setPopupMode(Qt.QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
    child.addActions([
        Qt.QtGui.QAction("&Action 9", window),
        Qt.QtGui.QAction("&Action 10", window),
    ])

    return OneReturn(child)


def test_tooltip(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QPushButton("Sample Label")
    child.setToolTip("Sample Tooltip")

    return OneReturn(child)


def test_splashscreen(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    pixmap = Qt.QtGui.QPixmap("assets/Yellowstone.jpg")
    size = app.screens()[0].size()
    scaled = pixmap.scaled(size, Qt.QtCore.Qt.AspectRatioMode.KeepAspectRatio)
    splash = Qt.QtWidgets.QSplashScreen(scaled)
    splash.show()
    Qt.QtCore.QTimer.singleShot(2000, lambda: splash_timer(splash, window))

    return ZeroReturn(show=False)


def test_calendar(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(True)

    return OneReturn(child)


def test_nogrid_calendar(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(False)

    return OneReturn(child)


def test_nonavigation_calendar(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(True)
    child.setNavigationBarVisible(False)

    return OneReturn(child)


def test_time_edit(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QTimeEdit(widget))


def test_date_edit(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QDateEdit(widget))


def test_datetime_edit(widget: _W, window: _Win, app: _A) -> OneReturn:
    return OneReturn(Qt.QtWidgets.QDateTimeEdit(widget))


def test_popup_datetime_edit(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QDateTimeEdit(widget)
    child.setCalendarPopup(True)

    return OneReturn(child)


def test_formats_datetime_edit(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child = [
        Qt.QtWidgets.QDateTimeEdit(widget),
        Qt.QtWidgets.QDateTimeEdit(widget),
    ]
    child[0].setDisplayFormat("dd.MM.yyyy")
    child[1].setDisplayFormat("MMM d yy")

    return ManyReturn(child)


def test_undo_group(widget: _W, window: _Win, app: _A) -> OneReturn:
    group = Qt.QtGui.QUndoGroup(widget)
    child = Qt.QtWidgets.QUndoView(group, widget)
    child.setEmptyLabel("New")
    child.setCleanIcon(reset_icon(widget))

    stack1 = Qt.QtGui.QUndoStack(widget)
    stack1.push(Qt.QtGui.QUndoCommand("Action 1"))
    stack1.push(Qt.QtGui.QUndoCommand("Action 2"))
    group.addStack(stack1)

    stack2 = Qt.QtGui.QUndoStack(widget)
    stack2.push(Qt.QtGui.QUndoCommand("Action 3"))
    stack2.push(Qt.QtGui.QUndoCommand("Action 4"))
    group.addStack(stack2)

    group.setActiveStack(stack1)

    return OneReturn(child)


def test_undo_stack(widget: _W, window: _Win, app: _A) -> OneReturn:
    stack = Qt.QtGui.QUndoStack(widget)
    child = Qt.QtWidgets.QUndoView(stack, widget)
    child.setEmptyLabel("New")
    child.setCleanIcon(reset_icon(widget))
    stack.push(Qt.QtGui.QUndoCommand("Action 1"))
    stack.push(Qt.QtGui.QUndoCommand("Action 2"))
    stack.push(Qt.QtGui.QUndoCommand("Action 3"))
    stack.push(Qt.QtGui.QUndoCommand("Action 4"))
    stack.push(Qt.QtGui.QUndoCommand("Action 5"))

    return OneReturn(child)


def test_lcd_number(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLCDNumber(3, widget)
    child.display(15)

    return OneReturn(child)


def test_hex_lcd_number(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setHexMode()

    return OneReturn(child)


def test_outline_lcd_number(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setSegmentStyle(Qt.QtWidgets.QLCDNumber.SegmentStyle.Outline)

    return OneReturn(child)


def test_flat_lcd_number(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setSegmentStyle(Qt.QtWidgets.QLCDNumber.SegmentStyle.Flat)

    return OneReturn(child)


def test_file_icon_provider(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QPushButton()
    provider = Qt.QtWidgets.QFileIconProvider()
    child.setIcon(provider.icon(Qt.QtWidgets.QFileIconProvider.IconType.Network))

    return OneReturn(child)


def test_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QDialog(window)
    dialog.setMinimumSize(100, 100)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_modal_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QDialog(window)
    dialog.setMinimumSize(100, 100)
    dialog.setModal(True)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_sizegrip_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QDialog(window)
    dialog.setMinimumSize(100, 100)
    dialog.setSizeGripEnabled(True)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_colordialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QColor()
    Qt.QtWidgets.QColorDialog.getColor(initial)

    return ZeroReturn(show=False, quit=True)


def test_alpha_colordialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QColor()
    options = Qt.QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel
    Qt.QtWidgets.QColorDialog.getColor(initial, options=options)

    return ZeroReturn(show=False, quit=True)


def test_nobuttons_colordialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QColor()
    options = Qt.QtWidgets.QColorDialog.ColorDialogOption.NoButtons
    Qt.QtWidgets.QColorDialog.getColor(initial, options=options)

    return ZeroReturn(show=False, quit=True)


def test_qt_colordialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QColor()
    options = Qt.QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog
    Qt.QtWidgets.QColorDialog.getColor(initial, options=options)

    return ZeroReturn(show=False, quit=True)


def test_fontdialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QFont()
    Qt.QtWidgets.QFontDialog.getFont(initial)

    return ZeroReturn(show=False, quit=True)


def test_nobuttons_fontdialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QFont()
    options = Qt.QtWidgets.QFontDialog.FontDialogOption.NoButtons
    Qt.QtWidgets.QFontDialog.getFont(initial, options=options)

    return ZeroReturn(show=False, quit=True)


def test_qt_fontdialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    initial = Qt.QtGui.QFont()
    options = Qt.QtWidgets.QFontDialog.FontDialogOption.DontUseNativeDialog
    Qt.QtWidgets.QFontDialog.getFont(initial, options=options)

    return ZeroReturn(show=False, quit=True)


def test_filedialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QFileDialog(window)
    dialog.setFileMode(Qt.QtWidgets.QFileDialog.FileMode.Directory)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_qt_filedialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QFileDialog(window)
    dialog.setOption(Qt.QtWidgets.QFileDialog.Option.DontUseNativeDialog)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_error_message(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QErrorMessage(widget)
    dialog.showMessage("Error message")
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_progress_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    dialog = Qt.QtWidgets.QProgressDialog("Text", "Cancel", 0, 100, window)
    dialog.setMinimumDuration(0)
    dialog.setMinimumSize(300, 100)
    dialog.show()
    count = 5 if is_headless() else 100
    for i in range(1, count + 1):
        dialog.setValue(i)
        app.processEvents()
        time.sleep(0.02)
        if dialog.wasCanceled():
            break
    dialog.close()

    return ZeroReturn(show=False, quit=True)


def test_input_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QInputDialog(window)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_int_input_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QInputDialog(window)
    dialog.setInputMode(Qt.QtWidgets.QInputDialog.InputMode.IntInput)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_double_input_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QInputDialog(window)
    dialog.setInputMode(Qt.QtWidgets.QInputDialog.InputMode.DoubleInput)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_combobox_input_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(["Item 1", "Item 2"])
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_list_input_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(["Item 1", "Item 2"])
    dialog.setOption(Qt.QtWidgets.QInputDialog.InputDialogOption.UseListViewForComboBoxItems)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_nobuttons_input_dialog(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(["Item 1", "Item 2"])
    dialog.setOption(Qt.QtWidgets.QInputDialog.InputDialogOption.NoButtons)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def _wizard(widget: "QtWidgets.QWidget") -> "QtWidgets.QWizard":
    wizard = Qt.QtWidgets.QWizard()

    intro = Qt.QtWidgets.QWizardPage()
    intro.setTitle("Introduction")
    intro_label = Qt.QtWidgets.QLabel(
        "Some very long text to simulate wrapping of the UI when displayed, because this needs to be done."
    )
    intro_label.setWordWrap(True)
    intro_layout = Qt.QtWidgets.QVBoxLayout()
    intro_layout.addWidget(intro_label)
    intro.setLayout(intro_layout)
    pixmap = Qt.QtWidgets.QWizard.WizardPixmap.WatermarkPixmap
    intro.setPixmap(pixmap, close_icon(widget).pixmap(50, 50))
    wizard.addPage(intro)

    registration = Qt.QtWidgets.QWizardPage()
    registration.setTitle("Registration")
    registration_label = Qt.QtWidgets.QLabel("Please register your copy.")
    registration_label.setWordWrap(True)
    registration_layout = Qt.QtWidgets.QVBoxLayout()
    registration_layout.addWidget(registration_label)
    registration.setLayout(registration_layout)
    pixmap = Qt.QtWidgets.QWizard.WizardPixmap.LogoPixmap
    registration.setPixmap(pixmap, close_icon(widget).pixmap(200, 200))
    wizard.addPage(registration)

    conclusion = Qt.QtWidgets.QWizardPage()
    conclusion.setTitle("Conclusion")
    conclusion_label = Qt.QtWidgets.QLabel("Congratulations on your purchase.")
    conclusion_label.setWordWrap(True)
    conclusion_layout = Qt.QtWidgets.QVBoxLayout()
    conclusion_layout.addWidget(conclusion_label)
    conclusion.setLayout(conclusion_layout)
    pixmap = Qt.QtWidgets.QWizard.WizardPixmap.BannerPixmap
    conclusion.setPixmap(pixmap, close_icon(widget).pixmap(50, 50))
    pixmap = Qt.QtWidgets.QWizard.WizardPixmap.BackgroundPixmap
    conclusion.setPixmap(pixmap, close_icon(widget).pixmap(50, 50))
    wizard.addPage(conclusion)

    wizard.setOption(Qt.QtWidgets.QWizard.WizardOption.HaveHelpButton)

    wizard.setWindowTitle("Simple Wizard Example")

    return wizard


def test_wizard(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    wizard = _wizard(widget)
    PyQtExec(wizard).exec()

    return ZeroReturn(show=False, quit=True)


def test_classic_wizard(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    wizard = _wizard(widget)
    wizard.setWizardStyle(Qt.QtWidgets.QWizard.WizardStyle.ClassicStyle)
    PyQtExec(wizard).exec()

    return ZeroReturn(show=False, quit=True)


def test_modern_wizard(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    wizard = _wizard(widget)
    wizard.setWizardStyle(Qt.QtWidgets.QWizard.WizardStyle.ModernStyle)
    PyQtExec(wizard).exec()

    return ZeroReturn(show=False, quit=True)


def test_mac_wizard(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    wizard = _wizard(widget)
    wizard.setWizardStyle(Qt.QtWidgets.QWizard.WizardStyle.MacStyle)
    PyQtExec(wizard).exec()

    return ZeroReturn(show=False, quit=True)


def test_aero_wizard(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    wizard = _wizard(widget)
    wizard.setWizardStyle(Qt.QtWidgets.QWizard.WizardStyle.AeroStyle)
    PyQtExec(wizard).exec()

    return ZeroReturn(show=False, quit=True)


def test_system_tray(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QErrorMessage(widget)
    dialog.showMessage("Hey! System tray icon.")

    tray = Qt.QtWidgets.QSystemTrayIcon()
    icon = close_icon(widget)
    tray.setIcon(icon)
    tray.show()
    tray.setToolTip("Sample tray icon")

    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def _test_standard_button(window: _Win, app: _A, button) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    message = Qt.QtWidgets.QMessageBox(window)
    message.addButton(button)
    message.setMinimumSize(100, 100)
    PyQtExec(message).exec()

    return ZeroReturn(show=False, quit=True)


def test_ok_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Ok)


def test_cancel_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Cancel)


def test_close_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Close)


def test_open_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Open)


def test_reset_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Reset)


def test_save_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Save)


def test_saveall_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.SaveAll)


def test_restoredefaults_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.RestoreDefaults)


def test_yes_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Yes)


def test_help_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Help)


def test_no_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.No)


def test_apply_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Apply)


def test_discard_button(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_button(window, app, Qt.QtWidgets.QMessageBox.StandardButton.Discard)


def _test_standard_icon(window: _Win, app: _A, icon) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    message = Qt.QtWidgets.QMessageBox(window)
    message.setIcon(icon)
    message.setMinimumSize(100, 100)
    PyQtExec(message).exec()

    return ZeroReturn(show=False, quit=True)


def test_critical_icon(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_icon(window, app, Qt.QtWidgets.QMessageBox.Icon.Critical)


def test_info_icon(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_icon(window, app, Qt.QtWidgets.QMessageBox.Icon.Information)


def test_no_icon(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_icon(window, app, Qt.QtWidgets.QMessageBox.Icon.NoIcon)


def test_question_icon(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_icon(window, app, Qt.QtWidgets.QMessageBox.Icon.Question)


def test_warning_icon(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    return _test_standard_icon(window, app, Qt.QtWidgets.QMessageBox.Icon.Warning)


def test_horizontal_buttons(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child: "MutableSequence[_W]" = []
    child.append(QtWidgets.QTextEdit(widget))
    container = Qt.QtWidgets.QWidget(widget)
    hbox = Qt.QtWidgets.QHBoxLayout(container)
    hbox.addWidget(QtWidgets.QPushButton("Delete"))
    hbox.addWidget(QtWidgets.QPushButton("Complete"))
    child.append(container)
    child.append(QtWidgets.QLineEdit(widget))
    dialog = Qt.QtWidgets.QDialogButtonBox(Qt.QtCore.Qt.Orientation.Horizontal, widget)
    dialog.addButton("Yes", Qt.QtWidgets.QDialogButtonBox.ButtonRole.YesRole)
    dialog.addButton("Really really really long", Qt.QtWidgets.QDialogButtonBox.ButtonRole.YesRole)
    dialog.addButton(Qt.QtWidgets.QDialogButtonBox.StandardButton.Ok)
    dialog.addButton(Qt.QtWidgets.QDialogButtonBox.StandardButton.Cancel)
    child.append(dialog)

    return ManyReturn(child)


def test_vertical_buttons(widget: _W, window: _Win, app: _A) -> ManyReturn:
    child: "MutableSequence[_W]" = []
    child.append(QtWidgets.QTextEdit(widget))
    container = Qt.QtWidgets.QWidget(widget)
    hbox = Qt.QtWidgets.QHBoxLayout(container)
    hbox.addWidget(QtWidgets.QPushButton("Delete"))
    hbox.addWidget(QtWidgets.QPushButton("Complete"))
    child.append(container)
    child.append(QtWidgets.QLineEdit(widget))
    dialog = Qt.QtWidgets.QDialogButtonBox(Qt.QtCore.Qt.Orientation.Vertical, widget)
    dialog.addButton("Yes", Qt.QtWidgets.QDialogButtonBox.ButtonRole.YesRole)
    dialog.addButton("Really really really long", Qt.QtWidgets.QDialogButtonBox.ButtonRole.YesRole)
    dialog.addButton(Qt.QtWidgets.QDialogButtonBox.StandardButton.Ok)
    dialog.addButton(Qt.QtWidgets.QDialogButtonBox.StandardButton.Cancel)
    dialog.setCenterButtons(True)
    child.append(dialog)

    return ManyReturn(child)


def test_stacked_widget(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QStackedWidget(widget)
    child.addWidget(QtWidgets.QLabel("Label 1"))
    child.addWidget(QtWidgets.QLabel("Label 2"))
    child.addWidget(QtWidgets.QLabel("Label 3"))
    child.addWidget(QtWidgets.QLabel("Label 4"))
    child.setCurrentIndex(2)

    return OneReturn(child)


def test_disabled_menu(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QMenuBar(window)
    child.setGeometry(get_geometry(app))
    menu = Qt.QtWidgets.QMenu("Main Menu", child)
    menu.addAction(Qt.QtGui.QAction("&Action 1", window))
    menu.addAction(Qt.QtGui.QAction("&Action 2", window))
    submenu = Qt.QtWidgets.QMenu("Sub Menu", menu)
    submenu.addAction(Qt.QtGui.QAction("&Action 3", window))
    action1 = Qt.QtGui.QAction("&Action 4", window)
    action1.setCheckable(True)
    action1.setEnabled(False)
    submenu.addAction(action1)
    menu.addAction(submenu.menuAction())
    action2 = Qt.QtGui.QAction("&Action 5", window)
    action2.setCheckable(True)
    action2.setChecked(True)
    menu.addSeparator()
    menu.addAction(action2)
    action3 = Qt.QtGui.QAction("&Action 6", window)
    action3.setCheckable(True)
    menu.addAction(action3)
    icon = close_icon(menu)
    menu.addAction(Qt.QtGui.QAction(icon, "&Action 7", window))
    menu.addAction(Qt.QtGui.QAction(icon, "&Action 8", window))
    menu.actions()[2].setEnabled(False)
    submenu.addAction(Qt.QtGui.QAction(icon, "&Action 9", window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return OneReturn(child)


def test_disabled_menubar(widget: _W, window: _Win, app: _A) -> OneReturn:
    child = Qt.QtWidgets.QMenuBar(window)
    child.setGeometry(get_geometry(app))
    menu = Qt.QtWidgets.QMenu("Main Menu", child)
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setEnabled(False)

    return OneReturn(child)


def test_issue25(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)

    def launch_filedialog(folder: "QtWidgets.QLineEdit") -> None:
        dialog = Qt.QtWidgets.QFileDialog()
        dialog.setFileMode(Qt.QtWidgets.QFileDialog.FileMode.Directory)
        if PyQtExec(dialog).exec():
            folder.setText(dialog.selectedFiles()[0])

    def launch_fontdialog(value: "QtWidgets.QLineEdit") -> None:
        initial = Qt.QtGui.QFont()
        initial.setFamily(value.text())
        font, ok = Qt.QtWidgets.QFontDialog.getFont(initial)
        if ok:
            value.setText(font.family())

    # Attempt to recreate the UI present here:
    #   https://github.com/Alexhuszagh/BreezeStyleSheets/issues/25#issue-1187193418
    dialog = Qt.QtWidgets.QDialog(window)
    dialog.resize(ARGS.width // 2, ARGS.height // 2)

    # Add the QTabWidget
    child = Qt.QtWidgets.QTabWidget(dialog)
    child.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
    general = Qt.QtWidgets.QWidget()
    child.addTab(general, "General")
    child.addTab(Qt.QtWidgets.QWidget(), "Colors")
    layout = Qt.QtWidgets.QVBoxLayout(general)
    layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignVCenter)

    # Add the data folder hboxlayout
    data = Qt.QtWidgets.QWidget()
    layout.addWidget(data)
    data_layout = Qt.QtWidgets.QHBoxLayout(data)
    data_layout.addWidget(Qt.QtWidgets.QLabel("Data Folder"))
    data_folder = Qt.QtWidgets.QLineEdit("Data")
    data_layout.addWidget(data_folder)
    file_dialog = Qt.QtWidgets.QPushButton("...")
    file_dialog.setCheckable(False)
    data_layout.addWidget(file_dialog)
    file_dialog.clicked.connect(lambda _: launch_filedialog(data_folder))

    # Add the "Show Grid" QCheckbox.
    checkbox = Qt.QtWidgets.QCheckBox
    layout.addWidget(abstract_button(checkbox, general, "Show grid"))

    # Grid square size.
    grid_size = Qt.QtWidgets.QWidget()
    layout.addWidget(grid_size)
    grid_size_layout = Qt.QtWidgets.QHBoxLayout(grid_size)
    grid_size_layout.addWidget(Qt.QtWidgets.QLabel("Grid Square Size"))
    spin = Qt.QtWidgets.QSpinBox(grid_size)
    spin.setValue(16)
    grid_size_layout.addWidget(spin)

    # Add units of measurement
    units = Qt.QtWidgets.QWidget()
    layout.addWidget(units)
    units_layout = Qt.QtWidgets.QHBoxLayout(units)
    units_layout.addWidget(Qt.QtWidgets.QLabel("Default length unit of measurement"))
    units_combo = Qt.QtWidgets.QComboBox()
    units_combo.addItem("Inches")
    units_combo.addItem("Foot")
    units_combo.addItem("Meter")
    units_layout.addWidget(units_combo)

    # Add default font.
    font = Qt.QtWidgets.QWidget()
    layout.addWidget(font)
    font_layout = Qt.QtWidgets.QHBoxLayout(font)
    font_layout.addWidget(Qt.QtWidgets.QLabel("Default Font"))
    font_value = Qt.QtWidgets.QLineEdit("Abcdef")
    font_layout.addWidget(font_value)
    font_dialog = Qt.QtWidgets.QPushButton("...")
    font_dialog.setCheckable(False)
    font_layout.addWidget(font_dialog)
    font_dialog.clicked.connect(lambda _: launch_fontdialog(font_value))
    font_layout.addStretch(1)

    # Add the alignment options
    alignment = Qt.QtWidgets.QWidget()
    layout.addWidget(alignment)
    alignment_layout = Qt.QtWidgets.QHBoxLayout(alignment)
    align_combo = Qt.QtWidgets.QComboBox()
    align_combo.addItem("Align Top")
    align_combo.addItem("Align Bottom")
    align_combo.addItem("Align Left")
    align_combo.addItem("Align Right")
    align_combo.addItem("Align Center")
    alignment_layout.addWidget(align_combo)
    alignment_layout.addWidget(abstract_button(checkbox, general, "Word Wrap"))
    alignment_layout.addStretch(1)

    # Add item label font
    item_label = Qt.QtWidgets.QWidget()
    layout.addWidget(item_label)
    item_label_layout = Qt.QtWidgets.QHBoxLayout(item_label)
    item_label_layout.addWidget(Qt.QtWidgets.QLabel("Item Label Font"))
    item_label_value = Qt.QtWidgets.QLineEdit("Abcdef")
    item_label_layout.addWidget(item_label_value)
    item_label_dialog = Qt.QtWidgets.QPushButton("...")
    item_label_dialog.setCheckable(False)
    item_label_layout.addWidget(item_label_dialog)
    item_label_dialog.clicked.connect(lambda _: launch_fontdialog(item_label_value))
    item_label_layout.addStretch(1)

    # Need to add the Ok/Cancel standard buttons.
    dialog_box = Qt.QtWidgets.QDialogButtonBox(Qt.QtCore.Qt.Orientation.Horizontal, general)
    layout.addWidget(dialog_box)
    dialog_box.addButton(Qt.QtWidgets.QDialogButtonBox.StandardButton.Ok)
    dialog_box.addButton(Qt.QtWidgets.QDialogButtonBox.StandardButton.Cancel)

    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test_issue28(widget: _W, window: _Win, app: _A) -> ZeroReturn:
    if is_headless():
        return ZeroReturn(show=False)
    dialog = Qt.QtWidgets.QFileDialog(window)
    dialog.setFileMode(Qt.QtWidgets.QFileDialog.FileMode.Directory)
    PyQtExec(dialog).exec()

    return ZeroReturn(show=False, quit=True)


def test(name: str) -> None:
    """Test a single widget by name."""

    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)
    ARGS.stylesheet.apply(Qt)

    # Setup the main window.
    window = Qt.QtWidgets.QMainWindow()
    window.setWindowTitle(f"Unittest for {name}.")
    window.resize(ARGS.width, ARGS.height)
    widget = Qt.QtWidgets.QWidget()
    scroll = Qt.QtWidgets.QScrollArea()
    scroll.setHorizontalScrollBarPolicy(Qt.QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(Qt.QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setWidgetResizable(True)

    # Get the correct parameters for our test widget.
    try:
        function = cast(TestCb, globals()[f"test_{name}"])
    except KeyError:
        raise NotImplementedError(f"test for {name} not implemented")
    result = function(widget, window, app)

    if result.layout is not None and result.child is not None:
        widget_layout = LAYOUT[result.layout]()
        if ARGS.compress:
            widget_layout.addStretch(1)
            add_widgets(widget_layout, result.child)
            widget_layout.addStretch(1)
        else:
            add_widgets(widget_layout, result.child)
        if ARGS.alignment is not None:
            widget_layout.setAlignment(ALIGNMENT[ARGS.alignment])
        widget.setLayout(widget_layout)
    scroll.setWidget(widget)
    window.setCentralWidget(scroll)

    if result.show:
        window.show()
    if is_headless():
        window.close()
    if result.quit or is_headless():
        app.quit()
    elif not is_headless():
        PyQtApplication(app).exec()


def main() -> int:
    tests = [i for i in globals().keys() if i.startswith("test_")]
    widgets = [i[len("test_") :] for i in tests]

    if ARGS.print_tests:
        print("\n".join(sorted(widgets)))
        return 0

    if ARGS.start and ARGS.start not in widgets:
        raise ValueError(f"Got an invalid continuation of {ARGS.start}")

    # Disable garbage collection to avoid runtime errors.
    gc.disable()
    os.environ["QT_SCALE_FACTOR"] = str(ARGS.scale)
    if ARGS.widget == "all":
        if ARGS.start is not None:
            try:
                index = widgets.index(ARGS.start)
                widgets = widgets[index:]
            except IndexError:
                pass
        for widget in widgets:
            test(widget)
            gc.collect()
    else:
        test(ARGS.widget)

    return 0


if __name__ == "__main__":
    sys.exit(main())
