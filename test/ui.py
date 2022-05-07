#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) <2021-Present> <Alex Huszagh>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
    test
    ====

    Test styles of a single widget.
'''

import argparse
import gc
import os
import random
import sys
import time

tests_dir = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(tests_dir)
example_dir = os.path.join(home, 'example')
sys.path.append(example_dir)

import shared

parser = shared.create_parser()
parser.add_argument(
    '--widget',
    help='widget to test. can provide `all` to test all widgets',
    default='all'
)
parser.add_argument(
    '--width',
    help='the window width',
    type=int,
    default=1068,
)
parser.add_argument(
    '--height',
    help='the window height',
    type=int,
    default=824,
)
parser.add_argument(
    '--alignment',
    help='the layout alignment',
)
parser.add_argument(
    '--compress',
    help='add stretch on both sides',
    action='store_true',
)
parser.add_argument(
    '--print-tests',
    help='print all available tests (widget names).',
    action='store_true'
)
parser.add_argument(
    '--start',
    help='test widget to start at.',
)
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
ICON_MAP = shared.get_icon_map(args, compat)

layout = {
    'vertical': QtWidgets.QVBoxLayout,
    'horizontal': QtWidgets.QHBoxLayout,
}

alignment = {
    'top': compat.AlignTop,
    'vcenter': compat.AlignVCenter,
    'bottom': compat.AlignBottom,
    'left': compat.AlignLeft,
    'hcenter': compat.AlignHCenter,
    'right': compat.AlignRight,
    'center': compat.AlignCenter,
}

def add_widgets(layout, children):
    '''Add 1 or more widgets to the layout.'''

    if isinstance(children, list):
        for child in children:
            layout.addWidget(child)
    else:
        layout.addWidget(children)

def abstract_button(
    cls,
    parent=None,
    *args,
    exlusive=False,
    checked=False,
    checkable=True,
    enabled=True,
):
    '''Helper to simplify creating abstract buttons.'''

    inst = cls(*args, parent)
    inst.setAutoExclusive(exlusive)
    inst.setCheckable(checkable)
    if isinstance(checked, bool):
        inst.setChecked(checked)
    else:
        inst.setTristate(True)
        inst.setCheckState(checked)
    inst.setEnabled(enabled)
    return inst

def splash_timer(splash, window):
    '''Non-block timer for a splashscreen.'''

    splash.finish(window)
    window.show()

def standard_icon(widget, icon):
    '''Get a standard icon depending on the stylesheet.'''
    return shared.standard_icon(args, widget, icon, ICON_MAP)

def close_icon(widget):
    '''Get the close icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_DockWidgetCloseButton)

def reset_icon(widget):
    '''Get the reset icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_DialogResetButton)

def next_icon(widget):
    '''Get the next icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_ArrowRight)

def previous_icon(widget):
    '''Get the previous icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_ArrowLeft)

def test_progressbar_horizontal(widget, *_):
    child = []
    bar1 = QtWidgets.QProgressBar(widget)
    bar1.setProperty('value', 0)
    child.append(bar1)
    bar2 = QtWidgets.QProgressBar(widget)
    bar2.setProperty('value', 24)
    child.append(bar2)
    bar3 = QtWidgets.QProgressBar(widget)
    bar3.setProperty('value', 99)
    child.append(bar3)
    bar4 = QtWidgets.QProgressBar(widget)
    bar4.setProperty('value', 100)
    child.append(bar4)

    return child

def test_progressbar_vertical(widget, *_):
    layout_type = 'horizontal'
    child = []
    bar1 = QtWidgets.QProgressBar(widget)
    bar1.setOrientation(compat.Vertical)
    bar1.setProperty('value', 0)
    child.append(bar1)
    bar2 = QtWidgets.QProgressBar(widget)
    bar2.setOrientation(compat.Vertical)
    bar2.setProperty('value', 24)
    child.append(bar2)
    bar3 = QtWidgets.QProgressBar(widget)
    bar3.setOrientation(compat.Vertical)
    bar3.setProperty('value', 99)
    child.append(bar3)
    bar4 = QtWidgets.QProgressBar(widget)
    bar4.setOrientation(compat.Vertical)
    bar4.setProperty('value', 100)
    child.append(bar4)

    return child, layout_type

def test_progressbar_inverted(widget, *_):
    child = []
    bar1 = QtWidgets.QProgressBar(widget)
    bar1.setProperty('value', 0)
    child.append(bar1)
    bar2 = QtWidgets.QProgressBar(widget)
    bar2.setProperty('value', 24)
    child.append(bar2)
    bar3 = QtWidgets.QProgressBar(widget)
    bar3.setProperty('value', 99)
    child.append(bar3)
    bar4 = QtWidgets.QProgressBar(widget)
    bar4.setProperty('value', 100)
    child.append(bar4)
    for bar in child:
        bar.setInvertedAppearance(True)

    return child

def test_progressbar_text(widget, *_):
    layout_type = 'horizontal'
    child = []
    bar1 = QtWidgets.QProgressBar(widget)
    bar1.setProperty('value', 0)
    child.append(bar1)
    bar2 = QtWidgets.QProgressBar(widget)
    bar2.setProperty('value', 24)
    child.append(bar2)
    bar3 = QtWidgets.QProgressBar(widget)
    bar3.setProperty('value', 99)
    child.append(bar3)
    bar4 = QtWidgets.QProgressBar(widget)
    bar4.setProperty('value', 100)
    child.append(bar4)
    for bar in child:
        bar.setTextDirection(compat.TopToBottom)
        bar.setOrientation(compat.Vertical)

    return child, layout_type

def test_slider_horizontal(widget, *_):
    child = QtWidgets.QSlider(widget)
    child.setOrientation(compat.Horizontal)

    return child

def test_slider_vertical(widget, *_):
    layout_type = 'horizontal'
    child = QtWidgets.QSlider(widget)
    child.setOrientation(compat.Vertical)

    return child, layout_type

def test_tick_slider(widget, *_):
    child = QtWidgets.QSlider(widget)
    child.setOrientation(compat.Horizontal)
    child.setTickInterval(5)
    child.setTickPosition(compat.TicksAbove)

    return child

def test_splitter_horizontal(widget, *_):
    child = QtWidgets.QSplitter(widget)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())

    return child

def test_splitter_vertical(widget, *_):
    layout_type = 'horizontal'
    child = QtWidgets.QSplitter(widget)
    child.setOrientation(compat.Vertical)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())

    return child, layout_type

def test_large_handle_splitter(widget, *_):
    child = QtWidgets.QSplitter(widget)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())
    child.setHandleWidth(child.handleWidth() * 5)

    return child

def test_nocollapsible_splitter(widget, *_):
    child = QtWidgets.QSplitter(widget)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())
    child.setChildrenCollapsible(False)

    return child

def test_rubber_band(widget, *_):
    return [
        QtWidgets.QRubberBand(compat.RubberBandLine, widget),
        QtWidgets.QRubberBand(compat.RubberBandRectangle, widget),
    ]

def test_plain_text_edit(widget, *_):
    child = [
        QtWidgets.QPlainTextEdit('Edit 1', widget),
        QtWidgets.QPlainTextEdit('Edit 2', widget),
        QtWidgets.QPlainTextEdit('Edit 3', widget),
        QtWidgets.QPlainTextEdit('Edit 4', widget),
        QtWidgets.QPlainTextEdit('Edit 5', widget),
    ]
    child[1].setBackgroundVisible(True)
    child[2].setCenterOnScroll(True)
    child[3].setCursorWidth(5)
    child[3].setPlaceholderText('Placeholder Text')
    child[4].setReadOnly(True)

    return child

def test_menu(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addAction(compat.QAction('&Action 1', window))
    menu.addAction(compat.QAction('&Action 2', window))
    submenu = QtWidgets.QMenu('Sub Menu', menu)
    submenu.addAction(compat.QAction('&Action 3', window))
    action1 = compat.QAction('&Action 4', window)
    action1.setCheckable(True)
    submenu.addAction(action1)
    menu.addAction(submenu.menuAction())
    action2 = compat.QAction('&Action 5', window)
    action2.setCheckable(True)
    action2.setChecked(True)
    menu.addSeparator()
    menu.addAction(action2)
    action3 = compat.QAction('&Action 6', window)
    action3.setCheckable(True)
    menu.addAction(action3)
    icon = close_icon(menu)
    menu.addAction(compat.QAction(icon, '&Action 7', window))
    menu.addAction(compat.QAction(icon, '&Action 8', window))
    submenu.addAction(compat.QAction(icon, '&Action 9', window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return child

def _menu(window, font, width):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addAction(compat.QAction('&Action 1', window))
    menu.addAction(compat.QAction('&Action 2', window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return child, menu

def test_native_menu(_, window, font, width, *__):
    child, _ = _menu(window, font, width)
    child.setNativeMenuBar(True)

    return child

def test_popup_menu(_, window, font, width, *__):
    child, _ = _menu(window, font, width)
    child.setDefaultUp(True)

    return child

def test_tearoff_menu(_, window, font, width, *__):
    child, menu = _menu(window, font, width)
    menu.setTearOffEnabled(True)

    return child

def test_icon_menu(widget, window, font, width, *_):
    child, menu = _menu(window, font, width)
    menu.setIcon(close_icon(widget))

    return child

def test_collapsible_separators_menu(_, window, font, width, *__):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addSeparator()
    menu.addAction(compat.QAction('&Action 1', window))
    menu.addSeparator()
    menu.addSeparator()
    menu.addAction(compat.QAction('&Action 2', window))
    menu.addSeparator()
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setSeparatorsCollapsible(True)

    return child

def test_tooltips_menu(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    action1 = compat.QAction('&Action 1', window)
    action1.setToolTip('Action 1')
    menu.addAction(action1)
    action2 = compat.QAction('&Action 2', window)
    action2.setToolTip('Action 1')
    menu.addAction(action2)
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setToolTipsVisible(True)

    return child

def test_mdi_area(widget, *_):
    child = QtWidgets.QMdiArea(widget)
    child.addSubWindow(QtWidgets.QMdiSubWindow())
    window = QtWidgets.QMdiSubWindow()
    flags = window.windowFlags()
    flags |= compat.WindowContextHelpButtonHint
    flags |= compat.WindowShadeButtonHint
    window.setWindowFlags(flags)
    window.setWindowTitle('Subwindow')
    child.addSubWindow(window)

    return child

def test_partial_mdi_area(widget, *_):
    child = [
        QtWidgets.QWidget(),
        QtWidgets.QMdiArea(widget),
    ]
    child[0].setMinimumSize(200, 200)
    child[1].addSubWindow(QtWidgets.QMdiSubWindow())
    window = QtWidgets.QMdiSubWindow()
    flags = window.windowFlags()
    flags |= compat.WindowContextHelpButtonHint
    flags |= compat.WindowShadeButtonHint
    window.setWindowFlags(flags)
    window.setWindowTitle('Subwindow')
    child[1].addSubWindow(window)

    return child

def test_statusbar(_, window, *__):
    child = QtWidgets.QStatusBar(window)
    window.setStatusBar(child)

    return child

def test_no_sizegrip_statusbar(_, window, *__):
    child = QtWidgets.QStatusBar(window)
    child.setSizeGripEnabled(False)
    window.setStatusBar(child)

    return child

def test_spinbox(widget, *_):
    layout_type = 'horizontal'
    child = []
    spin1 = QtWidgets.QSpinBox(widget)
    spin1.setValue(10)
    child.append(spin1)
    spin2 = QtWidgets.QSpinBox(widget)
    spin2.setValue(10)
    spin2.setPrefix('$')
    spin2.setSuffix('%')
    spin2.setEnabled(False)
    child.append(spin2)

    return child, layout_type

def test_double_spinbox(widget, *_):
    layout_type = 'horizontal'
    child = []
    spin1 = QtWidgets.QDoubleSpinBox(widget)
    spin1.setValue(10.5)
    child.append(spin1)
    spin2 = QtWidgets.QDoubleSpinBox(widget)
    spin2.setValue(10.5)
    spin2.setEnabled(False)
    spin2.setPrefix('$')
    spin2.setSuffix('%')
    child.append(spin2)

    return child, layout_type

def test_combobox(widget, *_):
    layout_type = 'horizontal'
    child = []
    combo1 = QtWidgets.QComboBox(widget)
    combo1.addItem('Item 1')
    combo1.addItem('Item 2')
    child.append(combo1)
    combo2 = QtWidgets.QComboBox(widget)
    combo2.addItem('Very Very Long Item 1')
    combo2.addItem('Very Very Long Item 2')
    child.append(combo2)
    combo3 = QtWidgets.QComboBox(widget)
    combo3.setEditable(True)
    combo3.addItem('Edit 1')
    combo3.addItem('Edit 2')
    combo3.lineEdit().setPlaceholderText('Placeholder')
    child.append(combo3)
    combo4 = QtWidgets.QComboBox(widget)
    combo4.addItem('Item 1')
    combo4.addItem('Item 2')
    combo4.addItem('Item 3')
    combo4.addItem('Item 4')
    combo4.addItem('Item 5')
    combo4.addItem('Item 6')
    combo4.setMaxVisibleItems(5)
    child.append(combo4)

    return child, layout_type

def _test_tabwidget(widget, position):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(position)
    child.addTab(QtWidgets.QWidget(), 'Tab 1')
    child.addTab(QtWidgets.QWidget(), 'Tab 2')
    child.addTab(QtWidgets.QWidget(), 'Tab 3')

    return child

def test_tabwidget_top(widget, *_):
    return _test_tabwidget(widget, compat.North)

def test_tabwidget_left(widget, *_):
    return _test_tabwidget(widget, compat.West)

def test_tabwidget_right(widget, *_):
    return _test_tabwidget(widget, compat.East)

def test_tabwidget_bottom(widget, *_):
    return _test_tabwidget(widget, compat.South)

def test_autohide_tabwidget(widget, *_):
    child = []

    item1 = QtWidgets.QTabWidget(widget)
    item1.setTabPosition(compat.North)
    item1.addTab(QtWidgets.QWidget(), 'Tab 1')
    item1.setTabBarAutoHide(True)
    child.append(item1)

    item2 = _test_tabwidget(widget, compat.East)
    item2.setTabBarAutoHide(True)
    child.append(item2)

    return child

def test_nonexpanding_tabwidget(widget, *_):
    child = _test_tabwidget(widget, compat.North)
    child.tabBar().setExpanding(False)

    return child

def test_movable_tabwidget(widget, *_):
    child = _test_tabwidget(widget, compat.North)
    child.tabBar().setMovable(True)

    return child

def test_closable_tabwidget_top(widget, *_):
    child = _test_tabwidget(widget, compat.North)
    child.setTabsClosable(True)

    return child

def test_closable_tabwidget_right(widget, *_):
    child = _test_tabwidget(widget, compat.East)
    child.setTabsClosable(True)

    return child

def test_use_scroll_tabwidget(widget, *_):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(compat.North)
    for i in range(1, 100):
        child.addTab(QtWidgets.QWidget(), f'Tab {i}')
    child.setUsesScrollButtons(True)

    return child

def test_no_scroll_tabwidget(widget, *_):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(compat.North)
    for i in range(1, 100):
        child.addTab(QtWidgets.QWidget(), f'Tab {i}')
    child.setUsesScrollButtons(False)

    return child

def test_rounded_tabwidget_north(widget, *_):
    child = _test_tabwidget(widget, compat.North)
    child.setTabShape(compat.Rounded)

    return child

def test_triangle_tabwidget_north(widget, *_):
    child = _test_tabwidget(widget, compat.North)
    child.setTabShape(compat.Triangular)

    return child

def test_rounded_tabwidget_east(widget, *_):
    child = _test_tabwidget(widget, compat.East)
    child.setTabShape(compat.Rounded)

    return child

def test_triangle_tabwidget_east(widget, *_):
    child = _test_tabwidget(widget, compat.East)
    child.setTabShape(compat.Triangular)

    return child

def test_rounded_tabwidget_west(widget, *_):
    child = _test_tabwidget(widget, compat.West)
    child.setTabShape(compat.Rounded)

    return child

def test_triangle_tabwidget_west(widget, *_):
    child = _test_tabwidget(widget, compat.West)
    child.setTabShape(compat.Triangular)

    return child

def test_rounded_tabwidget_south(widget, *_):
    child = _test_tabwidget(widget, compat.South)
    child.setTabShape(compat.Rounded)

    return child

def test_triangle_tabwidget_south(widget, *_):
    child = _test_tabwidget(widget, compat.South)
    child.setTabShape(compat.Triangular)

    return child

def test_closable_triangle_tabwidget_north(widget, *_):
    child = _test_tabwidget(widget, compat.North)
    child.setTabShape(compat.Triangular)
    child.setTabsClosable(True)

    return child

def test_closable_triangle_tabwidget_south(widget, *_):
    child = _test_tabwidget(widget, compat.South)
    child.setTabShape(compat.Triangular)
    child.setTabsClosable(True)

    return child

def test_closable_triangle_tabwidget_east(widget, *_):
    child = _test_tabwidget(widget, compat.East)
    child.setTabShape(compat.Triangular)
    child.setTabsClosable(True)

    return child

def test_closable_triangle_tabwidget_west(widget, *_):
    child = _test_tabwidget(widget, compat.West)
    child.setTabShape(compat.Triangular)
    child.setTabsClosable(True)

    return child

def test_button_position_tabwidget(widget, *_):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(compat.North)
    for i in range(1, 10):
        child.addTab(QtWidgets.QWidget(), f'Tab {i}')
        if i % 2 == 0:
            side = compat.LeftSide
        else:
            side = compat.RightSide
        child.tabBar().setTabButton(i - 1, side, QtWidgets.QWidget(widget))
    child.setUsesScrollButtons(True)

    return child

def test_text_browser(widget, *_):
    child = QtWidgets.QTextBrowser(widget)
    child.setOpenExternalLinks(True)
    child.setMarkdown('[QTextBrowser](https://doc.qt.io/qt-5/qtextbrowser.html)')

    return child

def test_dock(_, window, *__):
    dock1 = QtWidgets.QDockWidget('&Dock widget 1', window)
    dock1.setFeatures(compat.AllDockWidgetFeatures)
    dock2 = QtWidgets.QDockWidget('&Dock widget 2', window)
    dock2.setFeatures(compat.AllDockWidgetFeatures)
    dock3 = QtWidgets.QDockWidget('&Dock widget 3', window)
    dock3.setFeatures(compat.DockWidgetVerticalTitleBar)
    window.addDockWidget(compat.LeftDockWidgetArea, dock1)
    window.addDockWidget(compat.LeftDockWidgetArea, dock2)
    window.addDockWidget(compat.LeftDockWidgetArea, dock3)
    window.tabifyDockWidget(dock1, dock2)

def test_radio(widget, *_):
    child = []
    widget_type = QtWidgets.QRadioButton
    child.append(abstract_button(widget_type, widget))
    child.append(abstract_button(widget_type, widget, checked=True))
    child.append(abstract_button(widget_type, widget, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=True, enabled=False))
    child.append(abstract_button(widget_type, widget, 'With Text'))

    return child

def test_checkbox(widget, _, __, ___, ____, app):
    child = []
    widget_type = QtWidgets.QCheckBox
    child.append(abstract_button(widget_type, widget))
    child.append(abstract_button(widget_type, widget, checked=True))
    child.append(abstract_button(widget_type, widget, checked=compat.PartiallyChecked))
    child.append(abstract_button(widget_type, widget, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=True, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=compat.PartiallyChecked, enabled=False))
    child.append(abstract_button(widget_type, widget, 'With Text'))
    child.append(abstract_button(widget_type, widget, 'With Large Text'))
    checkbox_font = app.font()
    checkbox_font.setPointSizeF(50.0)
    child[-1].setFont(checkbox_font)

    return child

def test_table(widget, *_):
    child = QtWidgets.QTableWidget(widget)
    child.setColumnCount(2)
    child.setRowCount(4)
    item = QtWidgets.QTableWidgetItem('Row 1')
    child.setVerticalHeaderItem(0, item)
    item = QtWidgets.QTableWidgetItem('Row 2')
    child.setVerticalHeaderItem(1, item)
    item = QtWidgets.QTableWidgetItem('Row 3')
    child.setVerticalHeaderItem(2, item)
    item = QtWidgets.QTableWidgetItem('Row 4')
    child.setVerticalHeaderItem(3, item)
    item = QtWidgets.QTableWidgetItem('Column 1')
    child.setHorizontalHeaderItem(0, item)
    item = QtWidgets.QTableWidgetItem('Column 2')
    child.setHorizontalHeaderItem(1, item)

    return child

def test_sortable_table(widget, *_):
    child = test_table(widget)
    child.setSortingEnabled(True)

    return child

def test_nocorner_table(widget, *_):
    child = test_table(widget)
    child.setCornerButtonEnabled(False)

    return child

def test_nogrid_table(widget, *_):
    child = test_table(widget)
    child.setShowGrid(False)

    return child

def test_gridstyle_table(widget, *_):
    child = test_table(widget)
    child.setGridStyle(compat.DotLine)

    return child

def test_nohighlight_header_view(widget, *_):
    child = test_table(widget)
    header = child.horizontalHeader()
    header.setHighlightSections(False)

    return child

def test_movable_header_view(widget, *_):
    child = test_table(widget)
    header = child.horizontalHeader()
    header.setSectionsMovable(True)

    return child

def test_noclick_header_view(widget, *_):
    child = test_table(widget)
    header = child.horizontalHeader()
    header.setSectionsClickable(False)

    return child

def test_list(widget, *_):
    alignments = [compat.AlignLeft, compat.AlignRight, compat.AlignHCenter]
    child = QtWidgets.QListWidget(widget)
    for index in range(10):
        item = QtWidgets.QListWidgetItem(f'Item {index + 1}')
        item.setTextAlignment(random.choice(alignments))
        child.addItem(item)
    icon = close_icon(child)
    for index in range(10):
        item = QtWidgets.QListWidgetItem(icon, f'Item {index + 1}')
        item.setTextAlignment(random.choice(alignments))
        child.addItem(item)

    return child

def test_sortable_list(widget, *_):
    child = QtWidgets.QListWidget(widget)
    child.setSortingEnabled(True)
    for index in range(10):
        item = QtWidgets.QListWidgetItem(f'Item {index + 1}')
        child.addItem(item)

    return child

def test_key_sequence_edit(widget, *_):
    return QtWidgets.QKeySequenceEdit(widget)

def test_completer(widget, *_):
    child = QtWidgets.QLineEdit(widget)
    completer = QtWidgets.QCompleter(['Fruit', 'Fruits Basket', 'Fruba'])
    child.setCompleter(completer)

    return child

def test_scrollbar_vertical(widget, *_):
    child = QtWidgets.QListWidget(widget)
    for index in range(100):
        child.addItem(QtWidgets.QListWidgetItem(f'Item {index + 1}'))

    return child

def test_scrollbar_horizontal(widget, *_):
    child = QtWidgets.QTableWidget(widget)
    child.setColumnCount(100)
    child.setRowCount(1)
    item = QtWidgets.QTableWidgetItem(f'Row 1')
    child.setVerticalHeaderItem(0, item)
    for index in range(100):
        item = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
        child.setHorizontalHeaderItem(index, item)

    return child

def test_toolbar(_, window, *__):
    toolbar1 = QtWidgets.QToolBar('Toolbar')
    toolbar1.addAction('&Action 1')
    toolbar1.addAction('&Action 2')
    toolbar1.addSeparator()
    toolbar1.addAction('&Action 3')
    toolbar1.addAction('&Action 3 Really Long Name')
    icon = close_icon(toolbar1)
    toolbar1.addAction(icon, '&Action 4')
    toolbar1.setMovable(False)
    window.addToolBar(compat.TopToolBarArea, toolbar1)

    toolbar2 = QtWidgets.QToolBar('Toolbar')
    toolbar2.setOrientation(compat.Vertical)
    toolbar2.addAction('&Action 1')
    action2 = compat.QAction('&Action 2', window)
    action2.setStatusTip('Status tip')
    action2.setWhatsThis('Example action')
    toolbar2.addAction(action2)
    toolbar2.addSeparator()
    toolbar2.addAction('&Action 3')
    toolbar2.addAction('&Action 3 Really Long Name')
    toolbar2.addAction(QtWidgets.QWhatsThis.createAction(toolbar2))
    icon = close_icon(toolbar2)
    toolbar2.addAction(icon, '&Action 4')
    toolbar2.setFloatable(True)
    toolbar2.setMovable(True)
    window.addToolBar(compat.LeftToolBarArea, toolbar2)

    statusbar = QtWidgets.QStatusBar(window)
    window.setStatusBar(statusbar)

    return None, None

def test_toolbutton(widget, window, *_):
    layout_type = 'horizontal'
    child = [
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    window.setTabOrder(child[3], child[4])
    window.setTabOrder(child[4], child[5])
    window.setTabOrder(child[5], child[6])
    window.setTabOrder(child[6], child[7])
    child[0].setText('Simple ToolButton')
    child[1].setText('Action Toolbutton')
    child[2].setText('Menu Toolbutton')
    child[3].setText('Instant Toolbutton')
    child[1].addActions([
        compat.QAction('&Action 5', window),
        compat.QAction('&Action 6', window),
    ])
    child[2].setPopupMode(compat.MenuButtonPopup)
    child[2].addActions([
        compat.QAction('&Action 9', window),
        compat.QAction('&Action 10', window),
    ])
    child[3].setPopupMode(compat.InstantPopup)
    child[3].addActions([
        compat.QAction('&Action 11', window),
        compat.QAction('&Action 12', window),
    ])
    child[4].setArrowType(compat.LeftArrow)
    child[5].setArrowType(compat.RightArrow)
    child[6].setArrowType(compat.UpArrow)
    child[7].setArrowType(compat.DownArrow)
    icon = close_icon(widget)
    child[8].setIcon(icon)

    return child, layout_type

def test_raised_toolbutton(widget, window, *_):
    layout_type = 'horizontal'
    child = [
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    child[0].setArrowType(compat.LeftArrow)
    child[1].setArrowType(compat.RightArrow)
    child[2].setArrowType(compat.UpArrow)
    child[3].setArrowType(compat.DownArrow)
    for item in child:
        item.setAutoRaise(True)

    return child, layout_type

def test_toolbutton_style(widget, window, *_):
    layout_type = 'horizontal'
    child = [
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
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
    child[0].setText('Button 1')
    child[1].setText('Button 2')
    child[2].setText('Button 3')
    child[3].setText('Button 4')
    child[4].setText('Button 5')
    child[5].setText('Button 6')
    child[6].setText('Button 7')
    child[7].setText('Button 8')
    child[8].setText('Button 9')
    child[9].setText('Button 10')
    child[0].setToolButtonStyle(compat.ToolButtonIconOnly)
    child[1].setToolButtonStyle(compat.ToolButtonTextOnly)
    child[2].setToolButtonStyle(compat.ToolButtonTextBesideIcon)
    child[3].setToolButtonStyle(compat.ToolButtonTextUnderIcon)
    child[4].setToolButtonStyle(compat.ToolButtonFollowStyle)
    child[5].setToolButtonStyle(compat.ToolButtonIconOnly)
    child[6].setToolButtonStyle(compat.ToolButtonTextOnly)
    child[7].setToolButtonStyle(compat.ToolButtonTextBesideIcon)
    child[8].setToolButtonStyle(compat.ToolButtonTextUnderIcon)
    child[9].setToolButtonStyle(compat.ToolButtonFollowStyle)
    icon = close_icon(widget)
    for item in child:
        item.setIcon(icon)
    for item in child[5:]:
        item.setAutoRaise(True)

    return child, layout_type

def test_toolbutton_menu(widget, window, *_):
    layout_type = 'horizontal'
    child = [
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    child[0].setText('Button 1')
    child[1].setText('Button 2')
    child[2].setText('Button 3')
    child[3].setText('Button 4')
    child[1].addActions([
        compat.QAction('&Action 5', window),
        compat.QAction('&Action 6', window),
    ])
    child[2].setPopupMode(compat.MenuButtonPopup)
    child[2].addActions([
        compat.QAction('&Action 9', window),
        compat.QAction('&Action 10', window),
    ])
    child[3].setPopupMode(compat.InstantPopup)
    child[3].addActions([
        compat.QAction('&Action 11', window),
        compat.QAction('&Action 12', window),
    ])
    child[0].setProperty('hasMenu', False)
    # Incorrectly trims this normally... but set hasMenu true
    child[1].setAutoRaise(True)
    child[1].setProperty('hasMenu', True)

    return child, layout_type

def test_pushbutton(widget, *_):
    layout_type = 'horizontal'
    child = []
    widget_type = QtWidgets.QPushButton
    child.append(abstract_button(widget_type, widget, 'Button 1', checked=True))
    child.append(abstract_button(widget_type, widget, 'Button 2', enabled=False))
    child.append(abstract_button(widget_type, widget, 'Button 3', checkable=False))
    icon = close_icon(widget)
    child.append(abstract_button(widget_type, widget, icon, 'Button 4', checkable=False))
    flat = QtWidgets.QPushButton('Flat')
    flat.setFlat(True)
    child.append(flat)
    auto_default = QtWidgets.QPushButton('Auto Default')
    auto_default.setAutoDefault(True)
    child.append(auto_default)

    return child, layout_type

def test_column_view(widget, *_):
    child = QtWidgets.QColumnView(widget)
    model = compat.QFileSystemModel(widget)
    model.setRootPath('/')
    child.setModel(model)
    child.setResizeGripsVisible(True)

    return child

def test_nosizegrip_column_view(widget, *_):
    child = QtWidgets.QColumnView(widget)
    model = compat.QFileSystemModel(widget)
    model.setRootPath('/')
    child.setModel(model)
    child.setResizeGripsVisible(False)

    return child

def test_comprehensive_frame(widget, *_):
    child = [
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
    ]
    child[0].setFrameShape(compat.NoFrame)
    child[1].setFrameShape(compat.Box)
    child[2].setFrameShape(compat.Panel)
    child[3].setFrameShape(compat.StyledPanel)
    child[4].setFrameShape(compat.HLine)
    child[5].setFrameShape(compat.VLine)
    child[6].setFrameShape(compat.WinPanel)
    child[7].setFrameStyle(compat.Shadow_Mask)
    child[8].setFrameStyle(compat.Shape_Mask)
    child[9].setFrameShadow(compat.Plain)
    child[10].setFrameShadow(compat.Raised)
    child[11].setFrameShadow(compat.Sunken)
    for item in child[7:]:
        item.setFrameShape(compat.StyledPanel)

    return child

def test_tree(widget, *_):
    child = []
    tree1 = QtWidgets.QTreeWidget(widget)
    tree1.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree1, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree1, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])
    item3.setFlags(item3.flags() | compat.ItemIsUserCheckable)
    item3.setCheckState(0, compat.Unchecked)
    item4 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.2'])
    item5 = QtWidgets.QTreeWidgetItem(item4, ['Row 2.2.1'])
    item6 = QtWidgets.QTreeWidgetItem(item5, ['Row 2.2.1.1'])
    item7 = QtWidgets.QTreeWidgetItem(item5, ['Row 2.2.1.2'])
    item7.setFlags(item7.flags() | compat.ItemIsUserCheckable)
    item7.setCheckState(0, compat.Checked)
    item8 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.3'])
    item8.setFlags(item8.flags() | compat.ItemIsUserTristate)
    item8.setCheckState(0, compat.PartiallyChecked)
    item9 = QtWidgets.QTreeWidgetItem(tree1, ['Row 3'])
    item10 = QtWidgets.QTreeWidgetItem(item9, ['Row 3.1'])
    item11 = QtWidgets.QTreeWidgetItem(tree1, ['Row 4'])
    child.append(tree1)
    tree2 = QtWidgets.QTreeWidget(widget)
    tree2.setHeaderLabel('Tree 2')
    tree2.header().setSectionsClickable(True)
    item12 = QtWidgets.QTreeWidgetItem(tree2, ['Row 1', 'Column 2', 'Column 3'])
    child.append(tree2)

    return child

def test_sortable_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setObjectName('treeWidget')
    item_0 = QtWidgets.QTreeWidgetItem(tree)
    item_1 = QtWidgets.QTreeWidgetItem(tree)
    item_2 = QtWidgets.QTreeWidgetItem(item_1)
    item_2.setText(0, 'subitem')
    item_3 = QtWidgets.QTreeWidgetItem(item_2, ['Row 2.1'])
    item_3.setFlags(item_3.flags() | compat.ItemIsUserCheckable)
    item_3.setCheckState(0, compat.Unchecked)
    item_4 = QtWidgets.QTreeWidgetItem(item_2, ['Row 2.2'])
    item_5 = QtWidgets.QTreeWidgetItem(item_4, ['Row 2.2.1'])
    item_6 = QtWidgets.QTreeWidgetItem(item_5, ['Row 2.2.1.1'])
    item_7 = QtWidgets.QTreeWidgetItem(item_5, ['Row 2.2.1.2'])
    item_3.setFlags(item_7.flags() | compat.ItemIsUserCheckable)
    item_7.setCheckState(0, compat.Checked)
    item_8 = QtWidgets.QTreeWidgetItem(item_2, ['Row 2.3'])
    item_8.setFlags(item_8.flags() | compat.ItemIsUserTristate)
    item_8.setCheckState(0, compat.PartiallyChecked)
    item_9 = QtWidgets.QTreeWidgetItem(tree, ['Row 3'])
    item_10 = QtWidgets.QTreeWidgetItem(item_9, ['Row 3.1'])
    item_11 = QtWidgets.QTreeWidgetItem(tree, ['Row 4'])

    tree.headerItem().setText(0, 'qdz')
    tree.setSortingEnabled(False)
    tree.topLevelItem(0).setText(0, 'qzd')
    tree.topLevelItem(1).setText(0, 'effefe')
    tree.setSortingEnabled(True)

    return tree

def test_hidden_header_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])

    tree.setHeaderHidden(True)

    return tree

def test_indented_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1', 'Row 2.2'])

    tree.setIndentation(tree.indentation() * 2)
    tree.setColumnCount(2)
    tree.setColumnWidth(0, tree.columnWidth(0) * 2)
    tree.setColumnWidth(1, tree.columnWidth(1) * 2)

    return tree

def test_all_focus_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1', 'Row 2.2'])

    tree.setAllColumnsShowFocus(True)
    tree.setColumnCount(2)

    return tree

def test_nonexpandable_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])

    tree.setItemsExpandable(False)

    return tree

def test_undecorated_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])

    tree.setRootIsDecorated(False)

    return tree

def test_view_scrollarea(widget, *_):
    # For us to have both scrollbars visible.
    child = QtWidgets.QTableWidget(widget)
    child.setColumnCount(100)
    child.setRowCount(100)
    for index in range(100):
        row = QtWidgets.QTableWidgetItem(f'Row {index + 1}')
        child.setVerticalHeaderItem(index, row)
        column = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
        child.setHorizontalHeaderItem(index, column)

    return child

def test_widget_scrollarea(widget, window, *_):
    child = QtWidgets.QProgressBar(widget)
    window.setMinimumSize(300, 100)
    child.setProperty('value', 24)
    window.resize(30, 30)

    return child

def test_frame(widget, *_):
    child = []
    text = QtWidgets.QTextEdit()
    text.setPlainText('Hello world\nTesting lines')
    child.append(text)
    table = QtWidgets.QTableWidget()
    table.setColumnCount(5)
    table.setRowCount(5)
    child.append(table)

    return child

def test_groupbox(widget, *_):
    child = []
    groupbox = QtWidgets.QGroupBox('Groupbox 1', widget)
    vbox1 = QtWidgets.QVBoxLayout(groupbox)
    vbox1.setAlignment(compat.AlignHCenter)
    vbox1.addWidget(QtWidgets.QLineEdit('Sample Label'))
    child.append(groupbox)
    checkable = QtWidgets.QGroupBox('Groupbox 2', widget)
    checkable.setCheckable(True)
    child.append(checkable)
    vbox = QtWidgets.QVBoxLayout(checkable)
    vbox.setAlignment(compat.AlignHCenter)
    vbox.addWidget(QtWidgets.QLineEdit('Sample Label'))
    flat = QtWidgets.QGroupBox('Groupbox 3', widget)
    flat.setFlat(True)
    child.append(flat)

    return child

def test_dial(widget, *_):
    child = [
        QtWidgets.QDial(widget),
        QtWidgets.QDial(widget)
    ]
    child[1].setNotchesVisible(True)
    for item in child:
        item.setMinimum(0)
        item.setMaximum(100)
        item.setValue(30)

    return child

def test_command_link(widget, *_):
    child = QtWidgets.QWidget(widget)
    layout = QtWidgets.QVBoxLayout()
    layout.addStretch(1)
    next = QtWidgets.QCommandLinkButton('Next', 'Go next', widget)
    next.setIcon(next_icon(next))
    layout.addWidget(next)
    previous = QtWidgets.QCommandLinkButton('Previous', 'Go previous', widget)
    previous.setFlat(True)
    previous.setIcon(previous_icon(previous))
    layout.addWidget(previous)
    layout.addWidget(QtWidgets.QCommandLinkButton('Text Only', widget))
    layout.addStretch(1)

    child.setLayout(layout)

    return child

def test_lineedit(widget, *_):
    return QtWidgets.QLineEdit('Sample label', widget)

def test_placeholder_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setPlaceholderText('Placeholder')

    return child

def test_readonly_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setReadOnly(True)

    return child

def test_noframe_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setFrame(False)

    return child

def test_noecho_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setEchoMode(compat.NoEcho)

    return child

def test_password_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setEchoMode(compat.Password)

    return child

def test_password_edit_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setEchoMode(compat.PasswordEchoOnEdit)

    return child

def test_clear_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setClearButtonEnabled(True)

    return child

def test_label(widget, *_):
    return QtWidgets.QLabel('Sample label')

def test_indented_label(widget, *_):
    child = QtWidgets.QLabel('Sample label')
    child.setIndent(50)

    return child

def test_markdown_label(widget, *_):
    child = [
        QtWidgets.QLabel(),
        QtWidgets.QLabel(),
    ]
    child[0].setText('[BreezeStyleSheets](https://github.com/Alexhuszagh/BreezeStyleSheets)')
    child[0].setOpenExternalLinks(True)
    child[1].setText('# Sample Header\n- Bullet 1\n- Bullet 2')

    for item in child:
        item.setTextFormat(compat.MarkdownText)

    return child

def test_selectable_label(widget, *_):
    child = QtWidgets.QLabel('Selectable label')
    child.setTextInteractionFlags(compat.TextSelectableByMouse)

    return child

def test_editable_label(widget, *_):
    child = QtWidgets.QLabel('Editable label')
    child.setTextInteractionFlags(compat.TextEditorInteraction)

    return child

def test_font_combobox(widget, *_):
    return QtWidgets.QFontComboBox(widget)

def test_toolbox(widget, *_):
    # Test alignment with another item, in a vertical layout.
    child = []
    child.append(QtWidgets.QGroupBox('Groupbox', widget))
    child.append(QtWidgets.QGroupBox('Really, really long groupbox', widget))
    toolbox = QtWidgets.QToolBox(widget)
    child.append(toolbox)
    page1 = QtWidgets.QWidget()
    toolbox.addItem(page1, 'Page 1')
    page2 = QtWidgets.QWidget()
    vbox = QtWidgets.QVBoxLayout(page2)
    vbox.addWidget(QtWidgets.QLabel('Sample Label'))
    toolbox.addItem(page2, 'Page 2')
    page3 = QtWidgets.QWidget()
    toolbox.addItem(page3, 'Really, really long page 3')

    return child

def test_menubutton(widget, window, *_):
    child = QtWidgets.QToolButton(widget)
    child.setText('Menu Toolbutton')
    child.setPopupMode(compat.MenuButtonPopup)
    child.addActions([
        compat.QAction('&Action 9', window),
        compat.QAction('&Action 10', window),
    ])

    return child

def test_tooltip(widget, *_):
    child = QtWidgets.QPushButton('Sample Label')
    child.setToolTip('Sample Tooltip')

    return child

def test_splashscreen(_, window, __, ___, ____, app):
    pixmap = QtGui.QPixmap('assets/Yellowstone.jpg')
    size = app.screens()[0].size()
    scaled = pixmap.scaled(size, compat.KeepAspectRatio)
    splash = QtWidgets.QSplashScreen(scaled)
    splash.show()
    QtCore.QTimer.singleShot(2000, lambda: splash_timer(splash, window))

    return None, None, False

def test_calendar(widget, *_):
    child = QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(True)

    return child

def test_nogrid_calendar(widget, *_):
    child = QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(False)

    return child

def test_nonavigation_calendar(widget, *_):
    child = QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(True)
    child.setNavigationBarVisible(False)

    return child

def test_time_edit(widget, *_):
    return QtWidgets.QTimeEdit(widget)

def test_date_edit(widget, *_):
    return QtWidgets.QDateEdit(widget)

def test_datetime_edit(widget, *_):
    return QtWidgets.QDateTimeEdit(widget)

def test_popup_datetime_edit(widget, *_):
    child = QtWidgets.QDateTimeEdit(widget)
    child.setCalendarPopup(True)

    return child

def test_formats_datetime_edit(widget, *_):
    child = [
        QtWidgets.QDateTimeEdit(widget),
        QtWidgets.QDateTimeEdit(widget),
    ]
    child[0].setDisplayFormat('dd.MM.yyyy')
    child[1].setDisplayFormat('MMM d yy')

    return child

def test_undo_group(widget, *_):
    group = compat.QUndoGroup(widget)
    child = QtWidgets.QUndoView(group, widget)
    child.setEmptyLabel('New')
    child.setCleanIcon(reset_icon(widget))

    stack1 = compat.QUndoStack(widget)
    stack1.push(compat.QUndoCommand('Action 1'))
    stack1.push(compat.QUndoCommand('Action 2'))
    group.addStack(stack1)

    stack2 = compat.QUndoStack(widget)
    stack2.push(compat.QUndoCommand('Action 3'))
    stack2.push(compat.QUndoCommand('Action 4'))
    group.addStack(stack2)

    group.setActiveStack(stack1)

    return child

def test_undo_stack(widget, *_):
    stack = compat.QUndoStack(widget)
    child = QtWidgets.QUndoView(stack, widget)
    child.setEmptyLabel('New')
    child.setCleanIcon(reset_icon(widget))
    stack.push(compat.QUndoCommand('Action 1'))
    stack.push(compat.QUndoCommand('Action 2'))
    stack.push(compat.QUndoCommand('Action 3'))
    stack.push(compat.QUndoCommand('Action 4'))
    stack.push(compat.QUndoCommand('Action 5'))

    return child

def test_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    return child

def test_hex_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setHexMode()
    return child

def test_outline_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setSegmentStyle(compat.LCDOutline)
    return child

def test_flat_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setSegmentStyle(compat.LCDFlat)
    return child

def test_file_icon_provider(widget, *_):
    child = QtWidgets.QPushButton()
    provider = QtWidgets.QFileIconProvider()
    child.setIcon(provider.icon(compat.NetworkIcon))

    return child

def test_dialog(_, window, *__):
    dialog = QtWidgets.QDialog(window)
    dialog.setMinimumSize(100, 100)
    shared.execute(args, dialog)

    return None, None, False, True

def test_modal_dialog(_, window, *__):
    dialog = QtWidgets.QDialog(window)
    dialog.setMinimumSize(100, 100)
    dialog.setModal(True)
    shared.execute(args, dialog)

    return None, None, False, True

def test_sizegrip_dialog(_, window, *__):
    dialog = QtWidgets.QDialog(window)
    dialog.setMinimumSize(100, 100)
    dialog.setSizeGripEnabled(True)
    shared.execute(args, dialog)

    return None, None, False, True

def test_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial)

    return None, None, False, True

def test_alpha_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial, options=compat.ColorShowAlphaChannel)

    return None, None, False, True

def test_nobuttons_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial, options=compat.ColorNoButtons)

    return None, None, False, True

def test_qt_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial, options=compat.ColorDontUseNativeDialog)

    return None, None, False, True

def test_fontdialog(*_):
    initial = QtGui.QFont()
    QtWidgets.QFontDialog.getFont(initial)

    return None, None, False, True

def test_nobuttons_fontdialog(*_):
    initial = QtGui.QFont()
    QtWidgets.QFontDialog.getFont(initial, options=compat.FontNoButtons)

    return None, None, False, True

def test_qt_fontdialog(*_):
    initial = QtGui.QFont()
    QtWidgets.QFontDialog.getFont(initial, options=compat.FontDontUseNativeDialog)

    return None, None, False, True

def test_filedialog(_, window, *__):
    dialog = QtWidgets.QFileDialog(window)
    dialog.setFileMode(compat.Directory)
    shared.execute(args, dialog)

    return None, None, False, True

def test_qt_filedialog(_, window, *__):
    dialog = QtWidgets.QFileDialog(window)
    dialog.setOption(compat.FileDontUseNativeDialog)
    shared.execute(args, dialog)

    return None, None, False, True

def test_error_message(widget, *_):
    dialog = QtWidgets.QErrorMessage(widget)
    dialog.showMessage('Error message')
    shared.execute(args, dialog)

    return None, None, False, True

def test_progress_dialog(_, window, __, ___, ____, app):
    dialog = QtWidgets.QProgressDialog('Text', 'Cancel', 0, 100, window)
    dialog.setMinimumDuration(0)
    dialog.setMinimumSize(300, 100)
    dialog.show()
    for i in range(1, 101):
        dialog.setValue(i)
        app.processEvents()
        time.sleep(0.02)
        if dialog.wasCanceled():
            break
    dialog.close()

    return None, None, False, True

def test_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    shared.execute(args, dialog)

    return None, None, False, True

def test_int_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setInputMode(compat.IntInput)
    shared.execute(args, dialog)

    return None, None, False, True

def test_double_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setInputMode(compat.DoubleInput)
    shared.execute(args, dialog)

    return None, None, False, True

def test_combobox_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(['Item 1', 'Item 2'])
    shared.execute(args, dialog)

    return None, None, False, True

def test_list_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(['Item 1', 'Item 2'])
    dialog.setOption(compat.UseListViewForComboBoxItems)
    shared.execute(args, dialog)

    return None, None, False, True

def test_nobuttons_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(['Item 1', 'Item 2'])
    dialog.setOption(compat.InputNoButtons)
    shared.execute(args, dialog)

    return None, None, False, True

def _wizard(widget):
    wizard = QtWidgets.QWizard()

    intro = QtWidgets.QWizardPage()
    intro.setTitle('Introduction')
    intro_label = QtWidgets.QLabel('Some very long text to simulate wrapping of the UI when displayed, because this needs to be done.')
    intro_label.setWordWrap(True)
    intro_layout = QtWidgets.QVBoxLayout()
    intro_layout.addWidget(intro_label)
    intro.setLayout(intro_layout)
    intro.setPixmap(compat.WatermarkPixmap, close_icon(widget).pixmap(50, 50))
    wizard.addPage(intro)

    registration = QtWidgets.QWizardPage()
    registration.setTitle('Registration')
    registration_label = QtWidgets.QLabel('Please register your copy.')
    registration_label.setWordWrap(True)
    registration_layout = QtWidgets.QVBoxLayout()
    registration_layout.addWidget(registration_label)
    registration.setLayout(registration_layout)
    registration.setPixmap(compat.LogoPixmap, close_icon(widget).pixmap(200, 200))
    wizard.addPage(registration)

    conclusion = QtWidgets.QWizardPage()
    conclusion.setTitle('Conclusion')
    conclusion_label = QtWidgets.QLabel('Congratulations on your purchase.')
    conclusion_label.setWordWrap(True)
    conclusion_layout = QtWidgets.QVBoxLayout()
    conclusion_layout.addWidget(conclusion_label)
    conclusion.setLayout(conclusion_layout)
    conclusion.setPixmap(compat.BannerPixmap, close_icon(widget).pixmap(50, 50))
    conclusion.setPixmap(compat.BackgroundPixmap, close_icon(widget).pixmap(50, 50))
    wizard.addPage(conclusion)

    wizard.setOption(compat.HaveHelpButton)

    wizard.setWindowTitle('Simple Wizard Example')

    return wizard

def test_wizard(widget, *_):
    wizard = _wizard(widget)
    shared.execute(args, wizard)

    return None, None, False, True

def test_classic_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(compat.ClassicStyle)
    shared.execute(args, wizard)

    return None, None, False, True

def test_modern_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(compat.ModernStyle)
    shared.execute(args, wizard)

    return None, None, False, True

def test_mac_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(compat.MacStyle)
    shared.execute(args, wizard)

    return None, None, False, True

def test_aero_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(compat.AeroStyle)
    shared.execute(args, wizard)

    return None, None, False, True

def test_system_tray(widget, window, *_):
    dialog = QtWidgets.QErrorMessage(widget)
    dialog.showMessage('Hey! System tray icon.')

    tray = QtWidgets.QSystemTrayIcon()
    icon = close_icon(widget)
    tray.setIcon(icon)
    tray.show()
    tray.setToolTip('Sample tray icon')

    shared.execute(args, dialog)

    return None, None, False, True

def _test_standard_button(window, app, button):
    message = QtWidgets.QMessageBox(window)
    message.addButton(button)
    message.setMinimumSize(100, 100)
    shared.execute(args, message)

def test_ok_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageOk)
    return None, None, False, True

def test_cancel_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageCancel)
    return None, None, False, True

def test_close_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageClose)
    return None, None, False, True

def test_open_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageOpen)
    return None, None, False, True

def test_reset_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageReset)
    return None, None, False, True

def test_save_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageSave)
    return None, None, False, True

def test_saveall_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageSaveAll)
    return None, None, False, True

def test_restoredefaults_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageRestoreDefaults)
    return None, None, False, True

def test_yes_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageYes)
    return None, None, False, True

def test_help_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageHelp)
    return None, None, False, True

def test_no_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageNo)
    return None, None, False, True

def test_apply_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageApply)
    return None, None, False, True

def test_discard_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, compat.MessageDiscard)
    return None, None, False, True

def _test_standard_icon(window, app, icon):
    message = QtWidgets.QMessageBox(window)
    message.setIcon(icon)
    message.setMinimumSize(100, 100)
    shared.execute(args, message)

def test_critical_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, compat.MessageCritical)
    return None, None, False, True

def test_info_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, compat.MessageInformation)
    return None, None, False, True

def test_no_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, compat.MessageNoIcon)
    return None, None, False, True

def test_question_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, compat.MessageQuestion)
    return None, None, False, True

def test_warning_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, compat.MessageWarning)
    return None, None, False, True

def test_horizontal_buttons(widget, *_):
    child = []
    child.append(QtWidgets.QTextEdit(widget))
    container = QtWidgets.QWidget(widget)
    hbox = QtWidgets.QHBoxLayout(container)
    hbox.addWidget(QtWidgets.QPushButton('Delete'))
    hbox.addWidget(QtWidgets.QPushButton('Complete'))
    child.append(container)
    child.append(QtWidgets.QLineEdit(widget))
    dialog = QtWidgets.QDialogButtonBox(compat.Horizontal, widget)
    dialog.addButton('Yes', compat.DialogYesRole)
    dialog.addButton('Really really really long', compat.DialogYesRole)
    dialog.addButton(compat.DialogOk)
    dialog.addButton(compat.DialogCancel)
    child.append(dialog)

    return child

def test_vertical_buttons(widget, *_):
    child = []
    child.append(QtWidgets.QTextEdit(widget))
    container = QtWidgets.QWidget(widget)
    hbox = QtWidgets.QHBoxLayout(container)
    hbox.addWidget(QtWidgets.QPushButton('Delete'))
    hbox.addWidget(QtWidgets.QPushButton('Complete'))
    child.append(container)
    child.append(QtWidgets.QLineEdit(widget))
    dialog = QtWidgets.QDialogButtonBox(compat.Vertical, widget)
    dialog.addButton('Yes', compat.DialogYesRole)
    dialog.addButton('Really really really long', compat.DialogYesRole)
    dialog.addButton(compat.DialogOk)
    dialog.addButton(compat.DialogCancel)
    dialog.setCenterButtons(True)
    child.append(dialog)

    return child

def test_stacked_widget(widget, *_):
    child = QtWidgets.QStackedWidget(widget)
    child.addWidget(QtWidgets.QLabel('Label 1'))
    child.addWidget(QtWidgets.QLabel('Label 2'))
    child.addWidget(QtWidgets.QLabel('Label 3'))
    child.addWidget(QtWidgets.QLabel('Label 4'))
    child.setCurrentIndex(2)

    return child

def test_disabled_menu(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addAction(compat.QAction('&Action 1', window))
    menu.addAction(compat.QAction('&Action 2', window))
    submenu = QtWidgets.QMenu('Sub Menu', menu)
    submenu.addAction(compat.QAction('&Action 3', window))
    action1 = compat.QAction('&Action 4', window)
    action1.setCheckable(True)
    action1.setEnabled(False)
    submenu.addAction(action1)
    menu.addAction(submenu.menuAction())
    action2 = compat.QAction('&Action 5', window)
    action2.setCheckable(True)
    action2.setChecked(True)
    menu.addSeparator()
    menu.addAction(action2)
    action3 = compat.QAction('&Action 6', window)
    action3.setCheckable(True)
    menu.addAction(action3)
    icon = close_icon(menu)
    menu.addAction(compat.QAction(icon, '&Action 7', window))
    menu.addAction(compat.QAction(icon, '&Action 8', window))
    menu.actions()[2].setEnabled(False)
    submenu.addAction(compat.QAction(icon, '&Action 9', window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return child

def test_disabled_menubar(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setEnabled(False)

    return child

def test_issue25(widget, window, font, width, *_):

    def launch_filedialog(folder):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(compat.Directory)
        if shared.execute(args, dialog):
            folder.setText(dialog.selectedFiles()[0])

    def launch_fontdialog(value):
        initial = QtGui.QFont()
        initial.setFamily(value.text())
        font, ok = QtWidgets.QFontDialog.getFont(initial)
        if ok:
            value.setText(font.family())

    # Attempt to recreate the UI present here:
    #   https://github.com/Alexhuszagh/BreezeStyleSheets/issues/25#issue-1187193418
    dialog = QtWidgets.QDialog(window)
    dialog.resize(args.width // 2, args.height // 2)

    # Add the QTabWidget
    child = QtWidgets.QTabWidget(dialog)
    child.setTabPosition(compat.North)
    general = QtWidgets.QWidget()
    child.addTab(general, 'General')
    child.addTab(QtWidgets.QWidget(), 'Colors')
    layout = QtWidgets.QVBoxLayout(general)
    layout.setAlignment(compat.AlignVCenter)

    # Add the data folder hboxlayout
    data = QtWidgets.QWidget()
    layout.addWidget(data)
    data_layout = QtWidgets.QHBoxLayout(data)
    data_layout.addWidget(QtWidgets.QLabel('Data Folder'))
    data_folder = QtWidgets.QLineEdit('Data')
    data_layout.addWidget(data_folder)
    file_dialog = QtWidgets.QPushButton('...', checkable=False)
    data_layout.addWidget(file_dialog)
    file_dialog.clicked.connect(lambda _: launch_filedialog(data_folder))

    # Add the "Show Grid" QCheckbox.
    checkbox = QtWidgets.QCheckBox
    layout.addWidget(abstract_button(checkbox, general, 'Show grid'))

    # Grid square size.
    grid_size = QtWidgets.QWidget()
    layout.addWidget(grid_size)
    grid_size_layout = QtWidgets.QHBoxLayout(grid_size)
    grid_size_layout.addWidget(QtWidgets.QLabel('Grid Square Size'))
    spin = QtWidgets.QSpinBox(grid_size)
    spin.setValue(16)
    grid_size_layout.addWidget(spin)

    # Add units of measurement
    units = QtWidgets.QWidget()
    layout.addWidget(units)
    units_layout = QtWidgets.QHBoxLayout(units)
    units_layout.addWidget(QtWidgets.QLabel('Default length unit of measurement'))
    units_combo = QtWidgets.QComboBox()
    units_combo.addItem('Inches')
    units_combo.addItem('Foot')
    units_combo.addItem('Meter')
    units_layout.addWidget(units_combo)

    # Add default font.
    font = QtWidgets.QWidget()
    layout.addWidget(font)
    font_layout = QtWidgets.QHBoxLayout(font)
    font_layout.addWidget(QtWidgets.QLabel('Default Font'))
    font_value = QtWidgets.QLineEdit('Abcdef')
    font_layout.addWidget(font_value)
    font_dialog = QtWidgets.QPushButton('...', checkable=False)
    font_layout.addWidget(font_dialog)
    font_dialog.clicked.connect(lambda _: launch_fontdialog(font_value))
    font_layout.addStretch(1)

    # Add the alignment options
    alignment = QtWidgets.QWidget()
    layout.addWidget(alignment)
    alignment_layout = QtWidgets.QHBoxLayout(alignment)
    align_combo = QtWidgets.QComboBox()
    align_combo.addItem('Align Top')
    align_combo.addItem('Align Bottom')
    align_combo.addItem('Align Left')
    align_combo.addItem('Align Right')
    align_combo.addItem('Align Center')
    alignment_layout.addWidget(align_combo)
    alignment_layout.addWidget(abstract_button(checkbox, general, 'Word Wrap'))
    alignment_layout.addStretch(1)

    # Add item label font
    item_label = QtWidgets.QWidget()
    layout.addWidget(item_label)
    item_label_layout = QtWidgets.QHBoxLayout(item_label)
    item_label_layout.addWidget(QtWidgets.QLabel('Item Label Font'))
    item_label_value = QtWidgets.QLineEdit('Abcdef')
    item_label_layout.addWidget(item_label_value)
    item_label_dialog = QtWidgets.QPushButton('...', checkable=False)
    item_label_layout.addWidget(item_label_dialog)
    item_label_dialog.clicked.connect(lambda _: launch_fontdialog(item_label_value))
    item_label_layout.addStretch(1)

    # Need to add the Ok/Cancel standard buttons.
    dialog_box = QtWidgets.QDialogButtonBox(compat.Horizontal, general)
    layout.addWidget(dialog_box)
    dialog_box.addButton(compat.DialogOk)
    dialog_box.addButton(compat.DialogCancel)

    shared.execute(args, dialog)

    return None, None, False, True

def test_issue28(_, window, *__):
    dialog = QtWidgets.QFileDialog(window)
    dialog.setFileMode(compat.Directory)
    shared.execute(args, dialog)

    return None, None, False, True

def test(args, test_widget):
    '''Test a single widget.'''

    app, window = shared.setup_app(args, unknown, compat)
    shared.set_stylesheet(args, app, compat)

    # Setup the main window.
    window = QtWidgets.QMainWindow()
    window.setWindowTitle(f'Unittest for {test_widget}.')
    window.resize(args.width, args.height)
    widget = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setHorizontalScrollBarPolicy(compat.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(compat.ScrollBarAsNeeded)
    scroll.setWidgetResizable(True)

    # Get the correct parameters for our test widget.
    try:
        function = globals()[f'test_{test_widget}']
    except KeyError:
        raise NotImplementedError(f'test for {test_widget} not implemented')
    font = app.font()
    result = function(widget, window, font, args.width, args.height, app)
    child = []
    layout_type = 'vertical'
    show_window = True
    quit = False
    if result and isinstance(result, list):
        # Have a single value passed as a list
        child = result
    elif isinstance(result, tuple):
        child = result[0]
    else:
        child = result
    if isinstance(result, tuple) and len(result) >= 2:
        layout_type = result[1]
    if isinstance(result, tuple) and len(result) >= 3:
        show_window = result[2]
    if isinstance(result, tuple) and len(result) >= 4:
        quit = result[3]

    # Add the widgets to the layout.
    if layout_type is not None and child is not None:
        widget_layout = layout[layout_type]()
        if args.compress:
            widget_layout.addStretch(1)
            add_widgets(widget_layout, child)
            widget_layout.addStretch(1)
        else:
            add_widgets(widget_layout, child)
        if args.alignment is not None:
            widget_layout.setAlignment(alignment[args.alignment])
        widget.setLayout(widget_layout)
    scroll.setWidget(widget)
    window.setCentralWidget(scroll)

    # run
    if show_window:
        window.show()
    if quit:
        return app.quit()
    return shared.execute(args, app)

def main():
    'Application entry point'

    def test_names():
        return [i for i in globals().keys() if i.startswith('test_')]

    def widget_names():
        return [i[len('test_'):] for i in test_names()]

    if args.print_tests:
        print('\n'.join(sorted(widget_names())))
        return 0

    # Disable garbage collection to avoid runtime errors.
    gc.disable()
    os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    if args.widget == 'all':
        widgets = widget_names()
        if args.start != None:
            try:
                index = widgets.index(args.start)
                widgets = widgets[index:]
            except IndexError:
                pass
        for widget in widgets:
            test(args, widget)
            gc.collect()
    else:
        test(args, args.widget)

    return 0

if __name__ == '__main__':
    sys.exit(main())
