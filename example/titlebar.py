#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) <2022-Present> <Alex Huszagh>
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
    titlebar
    ========

    A full-featured, custom titlebar for a subwindow in an MDI area. This
    uses a frameless window hint with a custom titlebar, and event filter
    to capture titlebar and frame events. This example can also be easily applied to a top-level window.

    The custom titlebar supports the following:
      - Title text
      - Title bar with menu, help, min, max, restore, close, shade, and unshade.
        - Help, shade, and unshade are optional.
        - Menu contains restore, min, max, move, resize, stay on top, and close.
      - Custom window minimization.
        - Minimized windows can be placed in any corner.
        - Windows reposition on resize events to avoid truncating windows.
      - Dynamically toggle window state to keep windows above others.
      - Drag titlebar to move window
      - Double click titlebar to change window state.
        - Restores if maximized or minimized.
        - Shades or unshades if in normal state and applicable.
        - Otherwise, maximizes window.
      - Context menu move and resize events.
        - Click "Size" to resize from the bottom right based on cursor.
        - Click "Move" to move bottom-center of titlebar to cursor.
      - Drag to resize on window border with or without size grips.
        - If the window contains size grips, use the default behavior.
        - Otherwise, monitor mouse and hover events on window border.
          - If hovering over window border, draw appropriate resize cursor.
          - If clicked on window border, enter resize mode.
          - Click again to exit resize mode.
      - Custom border width for a window outline.

    The following Qt properties ensure proper styling of the UI:
      - `isTitlebar`: should be set on the title bar. ensures all widgets
            in the title bar have the correct background.
      - `isWindow`: set on the window to ensure there is no default border.
      - `hasWindowFrame`: set on a window with a border to draw the frame.

    The widget choice is very deliberate: any modifications can cause
    unexpected changes. `TitleBar` must be a `QFrame` so the background
    is filled, but must have a `NoFrame` shape. The window frame should
    have `NoFrame` without a border, but should be a `Box` with a border.
    Any other more elaborate style, like a `Panel`, won't be rendered
    correctly.
'''

import enum
import shared
import sys

from pathlib import Path

parser = shared.create_parser()
parser.add_argument(
    '--minimize-location',
    help='location to minimize windows to in the MDI area',
    default='BottomLeft',
    choices=['TopLeft', 'TopRight', 'BottomLeft', 'BottomRight'],
)
parser.add_argument(
    '--border-width',
    help='width of the subwindow borders',
    type=int,
    choices=range(0, 6),
    default=1,
)
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)
ICON_MAP = shared.get_icon_map(args, compat)
# 100ms between repaints, so we avoid over-repainting.
# Allows us to avoid glitchy motion during drags/
REPAINT_TIMER = 100
CLICK_TIMER = 20
# Make the titlebar size too large, so we can get the real value with min.
TITLEBAR_HEIGHT = 2**16

class MinimizeLocation(enum.IntEnum):
    '''Location where to place minimized widgets.'''

    TopLeft = 0
    TopRight = 1
    BottomLeft = 2
    BottomRight = 3

class WindowEdge(enum.IntEnum):
    '''Enumerations for window edge positions.'''

    NoEdge = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    TopLeft = 5
    TopRight = 6
    BottomLeft = 7
    BottomRight = 8

MINIMIZE_LOCATION = getattr(MinimizeLocation, args.minimize_location)

def standard_icon(widget, icon):
    '''Get a standard icon.'''
    return shared.standard_icon(args, widget, icon, ICON_MAP)

def menu_icon(widget):
    '''Get the menu icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarMenuButton)

def minimize_icon(widget):
    '''Get the minimize icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarMinButton)

def maximize_icon(widget):
    '''Get the maximize icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarMaxButton)

def restore_icon(widget):
    '''Get the restore icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarNormalButton)

def help_icon(widget):
    '''Get the help icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarContextHelpButton)

def shade_icon(widget):
    '''Get the shade icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarShadeButton)

def unshade_icon(widget):
    '''Get the unshade icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarUnshadeButton)

def close_icon(widget):
    '''Get the close icon depending on the stylesheet.'''
    return standard_icon(widget, compat.SP_TitleBarCloseButton)

def transparent_icon(widget):
    '''Create a transparent icon.'''
    return QtGui.QIcon()

def action(text, parent=None, icon=None, checkable=None):
    '''Create a custom QAction.'''

    value = compat.QAction(text, parent)
    if icon is not None:
        value.setIcon(icon)
    if checkable is not None:
        value.setCheckable(checkable)

    return value

def size_greater(x, y):
    '''Compare 2 sizes, determining if any bounds of x are greater than y.'''
    return x.width() > y.width() or x.height() > y.height()

def size_less(x, y):
    '''Compare 2 sizes, determining if any bounds of x are less than y.'''
    return x.width() < y.width() or x.height() < y.height()

# UI WIDGETS
# These are just to populate the views: these could be anything.

class LargeTable(QtWidgets.QTableWidget):
    '''Table with a large number of elements.'''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(100)
        self.setRowCount(100)
        for index in range(100):
            row = QtWidgets.QTableWidgetItem(f'Row {index + 1}')
            self.setVerticalHeaderItem(index, row)
            column = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
            self.setHorizontalHeaderItem(index, column)

class SortableTree(QtWidgets.QTreeWidget):
    '''Tree with checkboxes and a sort indicator on the header.'''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.item0 = QtWidgets.QTreeWidgetItem(self)
        self.item1 = QtWidgets.QTreeWidgetItem(self)
        self.item2 = QtWidgets.QTreeWidgetItem(self.item1)
        self.item2.setText(0, 'subitem')
        self.item3 = QtWidgets.QTreeWidgetItem(self.item2, ['Row 2.1'])
        self.item3.setFlags(self.item3.flags() | compat.ItemIsUserCheckable)
        self.item3.setCheckState(0, compat.Unchecked)
        self.item4 = QtWidgets.QTreeWidgetItem(self.item2, ['Row 2.2'])
        self.item5 = QtWidgets.QTreeWidgetItem(self.item4, ['Row 2.2.1'])
        self.item6 = QtWidgets.QTreeWidgetItem(self.item5, ['Row 2.2.1.1'])
        self.item7 = QtWidgets.QTreeWidgetItem(self.item5, ['Row 2.2.1.2'])
        self.item3.setFlags(self.item7.flags() | compat.ItemIsUserCheckable)
        self.item7.setCheckState(0, compat.Checked)
        self.item8 = QtWidgets.QTreeWidgetItem(self.item2, ['Row 2.3'])
        self.item8.setFlags(self.item8.flags() | compat.ItemIsUserTristate)
        self.item8.setCheckState(0, compat.PartiallyChecked)
        self.item9 = QtWidgets.QTreeWidgetItem(self, ['Row 3'])
        self.item10 = QtWidgets.QTreeWidgetItem(self.item9, ['Row 3.1'])
        self.item11 = QtWidgets.QTreeWidgetItem(self, ['Row 4'])

        self.headerItem().setText(0, 'qdz')
        self.setSortingEnabled(False)
        self.topLevelItem(0).setText(0, 'qzd')
        self.topLevelItem(1).setText(0, 'effefe')
        self.setSortingEnabled(True)

class SettingTabs(QtWidgets.QTabWidget):
    '''Sample setting widget with a tab view.'''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setTabPosition(compat.North)
        self.general = QtWidgets.QWidget()
        self.addTab(self.general, 'General')
        self.addTab(QtWidgets.QWidget(), 'Colors')
        self.general_layout = QtWidgets.QGridLayout(self.general)
        self.general_layout.setColumnStretch(3, 10)
        for row in range(1, 10):
            self.general_layout.setRowStretch(row, 1)
        self.general_layout.setRowStretch(7, 10)

        # Add the data folder hboxlayout
        self.general_layout.addWidget(QtWidgets.QLabel('Data Folder'), 0, 0)
        self.data_folder = QtWidgets.QLineEdit(str(Path.home()))
        self.general_layout.addWidget(self.data_folder, 0, 1, 1, 3)
        self.file_dialog = QtWidgets.QPushButton('...', checkable=False)
        self.general_layout.addWidget(self.file_dialog, 0, 4)
        self.file_dialog.clicked.connect(self.launch_filedialog)

        # Add default font.
        app = QtWidgets.QApplication.instance()
        self.general_layout.addWidget(QtWidgets.QLabel('Default Font'), 1, 0)
        self.font_value = QtWidgets.QLineEdit(app.font().family())
        self.general_layout.addWidget(self.font_value, 1, 1, 1, 3)
        self.font_dialog = QtWidgets.QPushButton('...', checkable=False)
        self.general_layout.addWidget(self.font_dialog, 1, 4)
        self.font_dialog.clicked.connect(lambda _: self.launch_fontdialog(self.font_value))

        # Add item label font
        self.general_layout.addWidget(QtWidgets.QLabel('Item Label Font'), 2, 0)
        self.item_label_value = QtWidgets.QLineEdit(app.font().family())
        self.general_layout.addWidget(self.item_label_value, 2, 1, 1, 3)
        self.item_label_dialog = QtWidgets.QPushButton('...', checkable=False)
        self.general_layout.addWidget(self.item_label_dialog, 2, 4)
        self.item_label_dialog.clicked.connect(lambda _: self.launch_fontdialog(self.item_label_value))

        # Add the "Show Grid" QCheckbox.
        self.grid = QtWidgets.QCheckBox('Show grid', self.general)
        self.general_layout.addWidget(self.grid, 3, 2, 1, 1)

        # Grid square size.
        self.grid_size = QtWidgets.QLabel('Grid Square Size', self.general)
        self.general_layout.addWidget(self.grid_size, 4, 0, 1, 2)
        self.grid_spin = QtWidgets.QSpinBox(self.general)
        self.grid_spin.setValue(16)
        self.general_layout.addWidget(self.grid_spin, 4, 2, 1, 1)

        # Add units of measurement
        self.units = QtWidgets.QLabel('Default length unit of measurement', self.general)
        self.general_layout.addWidget(self.units, 5, 0, 1, 2)
        self.units_combo = QtWidgets.QComboBox()
        self.units_combo.addItem('Inches')
        self.units_combo.addItem('Foot')
        self.units_combo.addItem('Meter')
        self.general_layout.addWidget(self.units_combo, 5, 2, 1, 1)

        # Add the alignment options
        self.align_combo = QtWidgets.QComboBox()
        self.align_combo.addItem('Align Top')
        self.align_combo.addItem('Align Bottom')
        self.align_combo.addItem('Align Left')
        self.align_combo.addItem('Align Right')
        self.align_combo.addItem('Align Center')
        self.general_layout.addWidget(self.align_combo, 6, 0, 1, 2)
        self.word_wrap = QtWidgets.QCheckBox('Word Wrap', self.general)
        self.general_layout.addWidget(self.word_wrap, 6, 2, 1, 1)

    def launch_filedialog(self):
        '''Launch the file dialog and store the folder.'''

        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(compat.Directory)
        dialog.setOption(compat.FileDontUseNativeDialog)
        dialog.setDirectory(self.data_folder.text())
        if shared.execute(args, dialog):
            self.data_folder.setText(dialog.selectedFiles()[0])

    def launch_fontdialog(self, edit):
        initial = QtGui.QFont()
        initial.setFamily(edit.text())
        font, ok = QtWidgets.QFontDialog.getFont(initial)
        if ok:
            edit.setText(font.family())

# WINDOW WIDGETS

class Label(QtWidgets.QLabel):
    '''Custom QLabel-like class that allows text elision.'''

    def __init__(
        self,
        text='',
        parent=None,
        elide=compat.ElideNone,
        width_cb=None,
    ):
        super().__init__(text, parent)
        self._text = text
        self._elide = elide
        self._width_cb = width_cb
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.elide)

    def text(self):
        '''Get the internal text for the label.'''
        return self._text

    def setText(self, text):
        '''Override the set text event to store the text internally.'''

        # Need to set the text first, otherwise
        # the `width()` might be too small.
        self._text = text
        super().setText(text)
        self.elide()

    def elideMode(self):
        '''Get the elide mode for the label.'''
        return self._elide

    def setElideMode(self, elide):
        self._elide = elide

    def elide(self):
        '''Elide the text in the QLabel.'''

        # The width estimate might not be valid: check the callback.
        width = self.width()
        if self._width_cb is not None:
            width = self._width_cb()

        metrics = QtGui.QFontMetrics(self.font())
        elided = metrics.elidedText(self._text, self._elide, width)
        super().setText(elided)

class TitleButton(QtWidgets.QToolButton):
    '''An icon-only button, without borders, for the titlebar.'''

    def __init__(self, icon, parent=None):
        super().__init__()
        self.setIcon(icon)
        self.setAutoRaise(True)

class Titlebar(QtWidgets.QFrame):
    '''Custom instance of a QTitlebar'''

    def __init__(self, subwindow, parent=None, flags=None):
        super().__init__(parent)

        # Get and set some properties.
        self.setProperty('isTitlebar', True)
        self._subwindow = subwindow
        self._state = compat.WindowNoState
        self._subwindow_rect = None
        self._has_help = False
        self._has_shade = False
        self._is_shaded = False
        self._has_shown = False
        self._title_column = None
        self._move_timer = QtCore.QTimer()
        self._move_timer.setSingleShot(True)
        self._move_timer.timeout.connect(self.menu_move)
        self._size_timer = QtCore.QTimer()
        self._size_timer.setSingleShot(True)
        self._size_timer.timeout.connect(self.menu_size)
        if flags is not None:
            self._has_help = bool(flags & compat.WindowContextHelpButtonHint)
            self._has_shade = bool(flags & compat.WindowShadeButtonHint)

        # Create our widgets.
        self._layout = QtWidgets.QGridLayout(self)
        self._menu = TitleButton(menu_icon(self))
        self._title = Label('', self, compat.ElideRight, self.title_width)
        self._min = TitleButton(minimize_icon(self))
        self._max = TitleButton(maximize_icon(self))
        self._restore= TitleButton(restore_icon(self))
        self._close = TitleButton(close_icon(self))
        if self._has_help:
            self._help = TitleButton(help_icon(self))
        if self._has_shade:
            self._shade = TitleButton(shade_icon(self))
            self._unshade = TitleButton(unshade_icon(self))

        # Add actions to our menu.
        self._menu.setPopupMode(compat.InstantPopup)
        self._main_menu = menu = QtWidgets.QMenu(self)
        self._restore_action = action('&Restore', self, restore_icon(self))
        self._restore_action.triggered.connect(self.restore)
        self._move_action = action('&Move', self, transparent_icon(self))
        self._move_action.triggered.connect(self.move_timer)
        self._size_action = action('&Size', self, transparent_icon(self))
        self._size_action.triggered.connect(self.size_timer)
        self._min_action = action('Mi&nimize', self, minimize_icon(self))
        self._min_action.triggered.connect(self.minimize)
        self._max_action = action('Ma&ximize', self, maximize_icon(self))
        self._max_action.triggered.connect(self.maximize)
        self._top_action = action('Stay on &Top', self, checkable=True)
        self._top_action.toggled.connect(self.toggle_keep_above)
        self._close_action = action('&Close', self, close_icon(self))
        self._close_action.triggered.connect(self._subwindow.close)
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
        self._layout.addWidget(self._title, 0, col, compat.AlignHCenter)
        self._layout.setColumnStretch(col, 1)
        self._title_column = col
        col += 1
        if self._has_help:
            self._layout.addWidget(self._help, 0, col)
            col += 1
        self._layout.addWidget(self._min, 0, col)
        col += 1
        self._layout.addWidget(self._max, 0, col)
        col += 1
        if self._has_shade:
            self._layout.addWidget(self._shade, 0, col)
            col += 1
        self._layout.addWidget(self._close, 0, col)
        self._restore.hide()
        if self._has_shade:
            self._unshade.hide()

        # Add in our event triggers.
        self._min.clicked.connect(self.minimize)
        self._max.clicked.connect(self.maximize)
        self._restore.clicked.connect(self.restore)
        self._close.clicked.connect(self._subwindow.close)
        if self._has_help:
            self._help.clicked.connect(self.help)
        if self._has_shade:
            self._shade.clicked.connect(self.shade)
            self._unshade.clicked.connect(self.unshade)

    # PROPERTIES

    @property
    def minimum_width(self):
        '''Get the height (in pixels) for the minimum title bar width.'''

        app = QtWidgets.QApplication.instance()
        icon_width = self._menu.iconSize().width()
        font_size = app.font().pointSizeF()

        # We can have 4-6 icons, which with padding means we need
        # room for at least 10 characters.
        return 6 * icon_width + int(16 * font_size)

    @property
    def minimum_height(self):
        '''Get the height (in pixels) for the minimum title bar height.'''
        return TITLEBAR_HEIGHT

    @property
    def minimum_size(self):
        '''Get the minimum dimensions for the title bar.'''
        return QtCore.QSize(self.minimum_width, self.minimum_height)

    def title_width(self):
        '''Get the width of the title based on the grid layout.'''
        return self._layout.cellRect(0, self._title_column).width()

    # QT-LIKE PROPERTIES

    def windowTitle(self):
        '''Get the titlebar's window title.'''
        return self._title.text()

    def setWindowTitle(self, title):
        '''Get the titlebar's window title.'''
        self._title.setText(title)

    def isNormal(self):
        '''Get if the titlebar and therefore subwindow has no state.'''
        return self._state == compat.WindowNoState

    def isMinimized(self):
        '''Get if the titlebar and therefore subwindow is minimized.'''
        return self._state == compat.WindowMinimized

    def isMaximized(self):
        '''Get if the titlebar and therefore subwindow is maximized.'''
        return self._state == compat.WindowMaximized

    # QT EVENTS

    def showEvent(self, event):
        '''Set the minimum size policies once the widgets are shown.'''

        global TITLEBAR_HEIGHT
        if not self._has_shown:
            TITLEBAR_HEIGHT = min(self.height(), TITLEBAR_HEIGHT)
            self._has_shown = True

        # Set some size policies.
        self.setMinimumSize(self.minimum_width, self.minimum_height)

        super().showEvent(event)

    # ACTIONS

    def set_minimum_size(self):
        '''Set the minimum size of the titlebar.'''
        self.setMinimumSize(self.minimum_width, self.minimum_height)

    def move_timer(self):
        '''Start timer to invoke menu_move.'''

        # We use a timer since the clicks on the menu can invoke the
        # MousePressEvent, which instantly cancels the move event.
        self._move_timer.start(CLICK_TIMER)

    def menu_move(self):
        '''Start a manually trigger move.'''
        self.window().start_move(self)

    def menu_move_to(self, global_position):
        '''
        Move the subwindow so that the position is in the center bottom
        of the title bar. The position is given in global coordinates.
        '''

        # Move it so the position is right below the bottom and the center.
        position = self.mapFromGlobal(global_position)
        rect = self.geometry()
        x = position.x() - rect.width() // 2
        y = position.y()
        rect.moveBottomLeft(QtCore.QPoint(x, y))

        window = self._subwindow
        window.move_to(window.mapToParent(rect.topLeft()))

    def size_timer(self):
        '''Start timer to invoke menu_size.'''

        # We use a timer since the clicks on the menu can invoke the
        # MousePressEvent, which instantly cancels the size event.
        self._size_timer.start(CLICK_TIMER)

    def menu_size(self):
        '''Start a manually triggered resize event.'''
        self.window().start_resize(self)

    def menu_size_to(self, global_position):
        '''
        Size the subwindow so that the position is in the center bottom
        of the title bar. The position is given in global coordinates.
        '''

        window = self._subwindow
        position = self.mapFromGlobal(global_position)
        rect = window.geometry()
        rect.setBottomRight(window.mapToParent(position))
        window.resize(rect.size())

        # Ensure we trigger the elide resize timer.
        self._title._timer.start(REPAINT_TIMER)

    def minimize(self):
        '''Minimize the current subwindow.'''

        if self.isNormal():
            self._subwindow_rect = self._subwindow.geometry()
        self.set_minimized()
        self.set_shaded()

        # Toggle state
        self._state = compat.WindowMinimized
        self._is_shaded = False
        self._subwindow.minimize(self._subwindow.minimized_size)

        # Toggle the menu actions
        # Minimized windows should not be movable, resizable, or minimizable.
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(False)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(False)
        self._max_action.setEnabled(True)

        self._subwindow.mdiArea().minimize(self._subwindow)

    def maximize(self):
        '''Maximize the current subwindow.'''

        if self.isNormal():
            self._subwindow_rect = self._subwindow.geometry()
        elif self.isMinimized() and not self._is_shaded:
            self._subwindow.mdiArea().unminimize(self._subwindow)
        size = self._subwindow.maximum_size
        rect = QtCore.QRect(0, 0, size.width(), size.height())
        self.set_maximized()
        self.set_unshaded()

        # Toggle state
        self._state = compat.WindowMaximized
        self._is_shaded = False
        self._subwindow.maximize(rect)

        # Toggle the menu actions
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(False)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(False)

    def restore(self):
        '''Restore the current subwindow (set to no state).'''

        if self.isMinimized() and not self._is_shaded:
            self._subwindow.mdiArea().unminimize(self._subwindow)
        self.set_restored()
        self.set_unshaded()

        # Toggle state
        self._state = compat.WindowNoState
        self._is_shaded = False
        self._subwindow.restore(self._subwindow_rect)

        # Toggle the menu actions
        self._restore_action.setEnabled(False)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(True)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(True)

    def shade(self):
        '''Shade the current subwindow.'''

        # Shaded windows are treated as if they have minimized state, and
        # if the window is maximized, it sets the previous subwindow rect
        # to the maximized geometry.
        self.set_shaded()
        self.set_minimized()

        # Toggle state
        self._state = compat.WindowMinimized
        self._is_shaded = True
        self._subwindow_rect = self._subwindow.geometry()
        width = self._subwindow.width()
        height = self._subwindow.minimized_size.height()
        self._subwindow.shade(QtCore.QSize(width, height))

        # Toggle the menu actions
        # Shaded windows should be movable, but not resizable or minimizable.
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(False)
        self._max_action.setEnabled(True)

    def unshade(self):
        '''Unshade the current subwindow.'''

        if self.isMinimized() and not self._is_shaded:
            self._subwindow.mdiArea().unminimize(self._subwindow)

        # If the window is minimized, it restores to the previous
        # window state and position.
        self.set_unshaded()
        self.set_restored()

        # Toggle state
        self._state = compat.WindowNoState
        self._is_shaded = False
        self._subwindow.unshade(self._subwindow_rect)

        # Toggle the menu actions
        # Unshaded windows have no state: they are restored.
        self._restore_action.setEnabled(False)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(True)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(True)

    def toggle_keep_above(self, checked):
        '''Toggle whether to keep the window above others.'''
        self._subwindow.setWindowFlag(compat.WindowStaysOnTopHint, checked)

    def help(self):
        '''Enter what's this mode.'''
        QtWidgets.QWhatsThis.enterWhatsThisMode()

    # VIEW

    def set_minimized(self):
        '''Show the restore and maximize icons.'''

        if self.isNormal():
            # Restore hidden, minimize + maximize shown
            self._layout.replaceWidget(self._min, self._restore)
            self._restore.show()
            self._min.hide()
        elif self.isMinimized():
            return
        else:
            # Maximize hidden, minimize + restore shown
            self._layout.replaceWidget(self._restore, self._max)
            self._layout.replaceWidget(self._min, self._restore)
            self._max.show()
            self._min.hide()

    def set_maximized(self):
        '''Show the minimize and restore icons.'''

        if self.isNormal():
            # Restore hidden, minimize + maximize shown
            self._layout.replaceWidget(self._max, self._restore)
            self._restore.show()
            self._max.hide()
        elif self.isMinimized():
            # Minimize hidden, restore + maximize shown
            self._layout.replaceWidget(self._restore, self._min)
            self._layout.replaceWidget(self._max, self._restore)
            self._min.show()
            self._max.hide()

    def set_restored(self):
        '''Show the minimize and maximize icons.'''

        if self.isNormal():
            return
        elif self.isMinimized():
            # Minimize hidden, restore + maximize shown
            self._layout.replaceWidget(self._restore, self._min)
            self._min.show()
            self._restore.hide()
        else:
            # Maximize hidden, minimize + restore shown
            self._layout.replaceWidget(self._restore, self._max)
            self._max.show()
            self._restore.hide()

    def set_shaded(self):
        '''Show the unshade icon (and hide the shade icon).'''

        if self._has_shade and not (self.isMinimized() or self._is_shaded):
            self._layout.replaceWidget(self._shade, self._unshade)
            self._shade.hide()
            self._unshade.show()

    def set_unshaded(self):
        '''Show the shade icon (and hide the unshade icon).'''

        if self._has_shade and (self.isMinimized() or self._is_shaded):
            self._layout.replaceWidget(self._unshade, self._shade)
            self._unshade.hide()
            self._shade.show()


class SizeFrame(QtCore.QObject):
    '''An invisible frame for resizing events around a window.'''

    def __init__(self, window=None, border_width=3):
        super().__init__(window)

        self._window = window
        self._border_width = border_width
        self._band = QtWidgets.QRubberBand(compat.RubberBandRectangle)

        self._pressed = False
        self._cursor = None
        self._press_edge = WindowEdge.NoEdge
        self._move_edge = WindowEdge.NoEdge

        self._window.setMouseTracking(True)
        self._window.setWindowFlag(compat.FramelessWindowHint, True)
        self._window.setAttribute(compat.WA_Hover)

    @property
    def is_active(self):
        '''Get if the SizeFrame resize event is active.'''
        return self._pressed

    def is_on_top(self, pos, rect):
        '''Determine if the cursor is on the top of the widget.'''
        return (
            pos.x() >= rect.x() + self._border_width and
            pos.x() <= rect.x() + rect.width() - self._border_width and
            pos.y() >= rect.y() and
            pos.y() <= rect.y() + self._border_width
        )

    def is_on_bottom(self, pos, rect):
        '''Determine if the cursor is on the bottom of the widget.'''
        return (
            pos.x() >= rect.x() + self._border_width and
            pos.x() <= rect.x() + rect.width() - self._border_width and
            pos.y() >= rect.y() + rect.height() - self._border_width and
            pos.y() <= rect.y() + rect.height()
        )

    def is_on_left(self, pos, rect):
        '''Determine if the cursor is on the left of the widget.'''
        return (
            pos.x() >= rect.x() - self._border_width and
            pos.x() <= rect.x() + self._border_width and
            pos.y() >= rect.y() + self._border_width and
            pos.y() <= rect.y() + rect.height() - self._border_width
        )

    def is_on_right(self, pos, rect):
        '''Determine if the cursor is on the right of the widget.'''
        return (
            pos.x() >= rect.x() + rect.width() - self._border_width and
            pos.x() <= rect.x() + rect.width() and
            pos.y() >= rect.y() + self._border_width and
            pos.y() <= rect.y() + rect.height() - self._border_width
        )

    def is_on_top_left(self, pos, rect):
        '''Determine if the cursor is on the top left of the widget.'''
        return (
            pos.x() >= rect.x() and
            pos.x() <= rect.x() + self._border_width and
            pos.y() >= rect.y() and
            pos.y() <= rect.y() + self._border_width
        )

    def is_on_top_right(self, pos, rect):
        '''Determine if the cursor is on the top right of the widget.'''
        return (
            pos.x() >= rect.x() + rect.width() - self._border_width and
            pos.x() <= rect.x() + rect.width() and
            pos.y() >= rect.y() and
            pos.y() <= rect.y() + self._border_width
        )

    def is_on_bottom_left(self, pos, rect):
        '''Determine if the cursor is on the bottom left of the widget.'''
        return (
            pos.x() >= rect.x() and
            pos.x() <= rect.x() + self._border_width and
            pos.y() >= rect.y() + rect.height() - self._border_width and
            pos.y() <= rect.y() + rect.height()
        )

    def is_on_bottom_right(self, pos, rect):
        '''Determine if the cursor is on the bottom right of the widget.'''
        return (
            pos.x() >= rect.x() + rect.width() - self._border_width and
            pos.x() <= rect.x() + rect.width() and
            pos.y() >= rect.y() + rect.height() - self._border_width and
            pos.y() <= rect.y() + rect.height()
        )

    def cursor_position(self, pos, rect):
        '''Calculate the cursor position inside the window.'''

        if self.is_on_left(pos, rect):
            return WindowEdge.Left
        elif self.is_on_right(pos, rect):
            return WindowEdge.Right
        elif self.is_on_bottom(pos, rect):
            return WindowEdge.Bottom
        elif self.is_on_top(pos, rect):
            return WindowEdge.Top
        elif self.is_on_bottom_left(pos, rect):
            return WindowEdge.BottomLeft
        elif self.is_on_bottom_right(pos, rect):
            return WindowEdge.BottomRight
        elif self.is_on_top_right(pos, rect):
            return WindowEdge.TopRight
        elif self.is_on_top_left(pos, rect):
            return WindowEdge.TopLeft

        return WindowEdge.NoEdge

    def top_left(self):
        '''Get the top/left position of the window in global coordinates.'''

        # Calculate the top left bounds of our window to get our frame.
        # We want our frame in global coordinates, but our window
        # might be a subwindow. If it has a parent, then it's a subwindow
        # and we need to map our coordinates.
        point = QtCore.QPoint(self._window.x(), self._window.y())
        if self._window.parent() is not None:
            point = self._window.parent().mapToGlobal(point)

        return point

    def frame_geometry(self):
        '''Calculate the frame geometry of our window  in global coordinates.'''
        return QtCore.QRect(self.top_left(), self._window.frameSize())

    def update_cursor(self, position):
        '''Update the cursor shape depending on the cursor position.'''

        if self._window.isMaximized() or self._window.isFullScreen():
            self.unset_cursor()
            return

        if self._pressed:
            return

        rect = self.frame_geometry()
        self._move_edge = self.cursor_position(position, rect)
        if self._move_edge == WindowEdge.NoEdge:
            self.unset_cursor()
            return
        if self._move_edge in (WindowEdge.Top, WindowEdge.Bottom):
            self._cursor = compat.SizeVerCursor
        elif self._move_edge in (WindowEdge.Left, WindowEdge.Right):
            self._cursor = compat.SizeHorCursor
        elif self._move_edge in (WindowEdge.TopLeft, WindowEdge.BottomRight):
            self._cursor = compat.SizeFDiagCursor
        elif self._move_edge in (WindowEdge.TopRight, WindowEdge.BottomLeft):
            self._cursor = compat.SizeBDiagCursor

        self._window.setCursor(self._cursor)

    def unset_cursor(self):
        '''Unset the custom cursor.'''

        if self._cursor:
            self._window.unsetCursor()
        self._cursor = None

    def enter(self, event):
        '''Handle the enterEvent of the window.'''

        position = shared.single_point_position(args, event)
        self.update_cursor(self._window.mapToGlobal(position))

    def leave(self, event):
        '''Handle the leaveEvent of the window.'''

        if not self._pressed:
            self.unset_cursor()

    def mouse_move(self, event):
        '''Handle the mouseMoveEvent of the window.'''

        position = shared.single_point_global_position(args, event)
        if not self._pressed:
            self.update_cursor(position)
            return

        # Get our new frame dimensions.
        rect = self._band.frameGeometry()
        if self._press_edge == WindowEdge.NoEdge:
            return
        elif self._press_edge == WindowEdge.Top:
            rect.setTop(position.y())
        elif self._press_edge == WindowEdge.Bottom:
            rect.setBottom(position.y())
        elif self._press_edge == WindowEdge.Left:
            rect.setLeft(position.x())
        elif self._press_edge == WindowEdge.Right:
            rect.setRight(position.x())
        elif self._press_edge == WindowEdge.TopLeft:
            rect.setTopLeft(position)
        elif self._press_edge == WindowEdge.TopRight:
            rect.setTopRight(position)
        elif self._press_edge == WindowEdge.BottomLeft:
            rect.setBottomLeft(position)
        elif self._press_edge == WindowEdge.BottomRight:
            rect.setBottomRight(position)

        if rect.width() < self._window.minimumWidth():
            rect.setLeft(self._window.x())
        if rect.height() < self._window.minimumHeight():
            rect.setTop(self._window.y())
        self._window.setGeometry(rect)
        self._band.setGeometry(rect)

    def mouse_press(self, event):
        '''Handle the mousePressEvent of the window.'''

        if event.button() == compat.LeftButton:
            position = shared.single_point_global_position(args, event)
            rect = self.frame_geometry()
            self._press_edge = self.cursor_position(position, rect)
            # We want to separately hand drags, so only
            # set this if we are pressing on the edge.
            if self._press_edge != WindowEdge.NoEdge:
                self._pressed = True
                self._band.setGeometry(rect)

    def mouse_release(self, event):
        '''Handle the mouseReleaseEvent of the window.'''

        if event.button() == compat.LeftButton:
            self._pressed = False

    def hover_move(self, event):
        '''Handle the hoverMoveEvent of the window.'''

        position = shared.single_point_position(args, event)
        self.update_cursor(self._window.mapToGlobal(position))

class SubWindow(QtWidgets.QMdiSubWindow):
    '''Custom subwindow instance'''

    def __init__(
        self,
        parent=None,
        flags=QtCore.Qt.WindowType(0),
        sizegrip=False,
    ):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | flags)
        super().setWidget(QtWidgets.QWidget())

        # Create our widgets. Sizeframe and sizegrip are mutually exclusive.
        self._central = QtWidgets.QFrame(super().widget())
        self._central.setLayout(QtWidgets.QVBoxLayout())
        self._titlebar = Titlebar(self, self._central, flags)
        self._widget = QtWidgets.QWidget(self._central)
        self._widget.setLayout(QtWidgets.QVBoxLayout())
        self._sizeframe = None
        self._sizegrip = None
        self._border = args.border_width
        self._titlebar_size = QtCore.QSize()
        self._sizegrip_size = QtCore.QSize()
        if sizegrip:
            self._sizegrip = QtWidgets.QSizeGrip(self._central)
        else:
            self._sizeframe = SizeFrame(self, border_width=5)

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
        bottom_right = compat.AlignBottom | compat.AlignRight
        super().layout().setSpacing(0)
        super().layout().addWidget(self._central, 10)
        self._central.layout().setSpacing(0)
        self._central.layout().addWidget(self._titlebar, 0, compat.AlignTop)
        self._central.layout().addWidget(self._widget, 10)
        if self._sizegrip is not None:
            self._central.layout().addWidget(self._sizegrip, 0, bottom_right)

        # Set the border properties.
        self._central.layout().setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        self._central.setProperty('isWindow', True)
        if self._border > 0:
            self._central.setProperty('windowFrame', min(self._border, 5))
            self._central.setFrameShape(compat.Box)
            self._central.setFrameShadow(compat.Raised)

        # Ensure our titlebar gets highest priority.
        self._titlebar.raise_()
        self._widget.lower()

    # PROPERTIES

    @property
    def border_size(self):
        '''Get the size of the border, regardless if present.'''
        return QtCore.QSize(2 * self._border, 2 * self._border)

    @property
    def minimized_content_size(self):
        '''Get the minimum content size of the widget.'''
        return self._titlebar_size
        size = self._titlebar_size
        if self._border:
            size = size + self.border_size
        return size

    @property
    def minimized_size(self):
        '''Get the minimum size of the widget, with the size grips hidden.'''

        size = self.minimized_content_size
        if self._border:
            size = size + self.border_size
        return size

    @property
    def minimum_size(self):
        '''Get the minimum size for the widget.'''

        size = self.minimized_size
        if self._sizegrip is not None and self._sizegrip.isVisible():
            # Don't modify in place: percolates later.
            size = size + self._sizegrip_size
        return size

    @property
    def maximum_size(self):
        '''Get the maximum size for the widget.'''
        return self.mdiArea().size()

    # RESIZE

    def move_to(self, position):
        '''Move the window to the desired position'''

        # Also updates the stored previous subwindow position, if applicable.
        # This means shading/unshading uses the new position of the window,
        # but the old sizes, rather than jump the window back.
        self.move(position)
        rect = self._titlebar._subwindow_rect
        if rect is not None:
            rect.moveTo(position)

    def set_minimum_size(self):
        '''Sets the minimum size of the window and the titlebar.'''

        self._titlebar.set_minimum_size()
        self._titlebar_size = self._titlebar.minimumSize()
        self.setMinimumSize(self.minimum_size)

    def minimize(self, size):
        '''Minimize the window, hiding the main widget and size grip.'''

        self._widget.hide()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.set_minimum_size()
        self.resize(size)

    def maximize(self, rect):
        '''Maximize the window, showing the main widget and hiding size grip.'''

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.set_minimum_size()
        self.setGeometry(rect)

    def restore(self, rect):
        '''Restore the window, showing the main widget and size grip.'''

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.show()
        self.set_minimum_size()
        self.setGeometry(rect)

    def shade(self, size):
        '''Shade the window, hiding the main widget and size grip.'''

        self._widget.hide()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.set_minimum_size()
        self.resize(size)

    def unshade(self, rect):
        '''Unshade the window, showing the main widget and size grip.'''

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.show()
        self.set_minimum_size()
        self.setGeometry(rect)

    # QT EVENTS

    def resizeEvent(self, event):
        '''Handle widget resize events here.'''

        # Need to trigger the titlebar title resize. Need to handle it
        # here, since the SizeFrame resizes won't always trigger a
        # Label::resizeEvent, which can cause the text to stay elided.
        title_timer = self._titlebar._title._timer
        title_timer.start(REPAINT_TIMER)

        super().resizeEvent(event)

    def showEvent(self, event):
        '''Set the minimum size policies once the widgets are shown.'''

        # Until shown, the size grip has inaccurate sizes.
        # Set the minimum size policy of the widget.
        # The show event occurs just after everything is shown,
        # so the widget sizes (and isVisible) are accurate.
        self._titlebar_size = self._titlebar.minimumSize()
        if self._sizegrip is not None:
            sizegrip_size = self._sizegrip.sizeHint()
            self._sizegrip_size = QtCore.QSize(0, sizegrip_size.height())
        self.setMinimumSize(self.minimum_size)

        super().showEvent(event)

    def mouseDoubleClickEvent(self, event):
        '''Override the mouse double click, and don't call the press event.'''

        # By default, the flowchart for titlebar double clicks is as follows:
        #   1. If minimized, restore
        #   2. If maximized, restore
        #   3. If no state and can shade, shade
        #   4. If no state and cannot shade, maximize
        #   5. If shaded, unshade.
        widget = self._titlebar
        if not widget.underMouse() or event.button() != compat.LeftButton:
            return super().mouseDoubleClickEvent(event)
        if widget._is_shaded:
            widget.unshade()
        elif widget.isMinimized() or widget.isMaximized():
            widget.restore()
        elif widget._has_shade:
            widget.shade()
        else:
            widget.maximize()

    def mousePressEvent(self, event):
        '''Override a mouse click on the titlebar to allow a move.'''

        widget = self._titlebar
        window = self.window()
        if widget.underMouse():
            # `self.window()._move` cannot be set, since we're inside
            # the global event filter here. We handle conflicts here,
            # so only one of the 4 states can be set. We can't move
            # minimized widgets, so don't try.
            is_left = event.button() == compat.LeftButton
            is_minimized = self.isMinimized() and not self._titlebar._is_shaded
            has_frame = window._frame is not None
            if is_left and not is_minimized and not has_frame:
                self.window().start_drag(event)
            elif event.button() == compat.RightButton:
                position = shared.single_point_global_position(args, event)
                shared.execute(args, widget._main_menu, position)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        '''Reposition the window on the move event.'''

        window = self.window()
        if window._frame is not None:
            window.end_drag()
        if window._drag is not None:
            self.window().handle_drag(self, event)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        '''End the drag event.'''

        self.window().end_drag()
        return super().mouseReleaseEvent(event)

    # QT-LIKE PROPERTIES

    def windowTitle(self):
        '''Get the window title from the titlebar.'''
        return self._titlebar.windowTitle()

    def setWindowTitle(self, title):
        '''Get the window title from the titlebar.'''
        self._titlebar.setWindowTitle(title)

    def layout(self):
        '''Get the subwindow layout (mapped to self._widget)'''
        return self._widget.layout()

    def setLayout(self, layout):
        '''Set the subwindow layout (mapped to self._widget)'''
        self._widget.setLayout(layout)

    def widget(self):
        '''Get the subwindow widget (mapped to self._widget)'''
        return self._widget

    def setWidget(self, widget):
        '''Set the subwindow widget (mapped to self._widget)'''

        super().layout().replaceWidget(self._widget, widget)
        self._widget = widget

    def isMinimized(self):
        '''Overload since we use a custom minimized for our subwindow.'''
        return self._titlebar.isMinimized()

    def isMaximized(self):
        '''Overload since we use a custom maximized for our subwindow.'''
        return self._titlebar.isMaximized() or super().isMaximized()

class MdiArea(QtWidgets.QMdiArea):
    '''Override the QMdiArea for window minimization and background color.'''

    def __init__(self, parent=None, location=MINIMIZE_LOCATION):
        super().__init__(parent)
        self._minimized = []
        self._location = location
        self._timer = QtCore.QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.move_minimized)

        # Set the background color
        background = self.background()
        background.setColor(colors.ViewBackground)
        self.setBackground(background)

    def resizeEvent(self, event):
        '''Handle moving minimized windows without glitchy motion.'''

        self._timer.start(REPAINT_TIMER)
        super().resizeEvent(event)

    def minimize(self, subwindow):
        '''Minimize a subwindow and reposition it.'''

        self._minimized.append(subwindow)
        self.move_minimized()

    def unminimize(self, subwindow):
        '''Unminimize a subwindow.'''

        self._minimized.remove(subwindow)
        self.move_minimized()

    def move_minimized(self):
        '''Move the minimized windows.'''

        # No need to set the geometry of our minimized windows.
        if not self._minimized:
            return

        # Get the geometry of the elements, and calculate the windows per row.
        window = self._minimized[0]
        has_border = any(i._border for i in self._minimized)
        size = window.minimized_content_size
        if has_border:
            size = size + window.border_size
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
            new_column = lambda p: QtCore.QPoint(left_x, p.y() + height)
            shift_row = lambda p, w: p + QtCore.QPoint(w, 0)
        elif self._location == MinimizeLocation.TopRight:
            point = QtCore.QPoint(right_x, top_y)
            new_column = lambda p: QtCore.QPoint(right_x, p.y() + height)
            shift_row = lambda p, w: p - QtCore.QPoint(w, 0)
        elif self._location == MinimizeLocation.BottomLeft:
            point = QtCore.QPoint(left_x, bottom_y)
            new_column = lambda p: QtCore.QPoint(left_x, p.y() - height)
            shift_row = lambda p, w: p + QtCore.QPoint(w, 0)
        else:
            point = QtCore.QPoint(right_x, bottom_y)
            new_column = lambda p: QtCore.QPoint(right_x, p.y() - height)
            shift_row = lambda p, w: p - QtCore.QPoint(w, 0)

        # Now, need to place them accordingly.
        # Need to handle unshifts, if they occur, due to the
        for index in range(len(self._minimized)):
            # Calculate our new column, only storing if it is a new column.
            window = self._minimized[index]
            is_new_column = index % row_count == 0
            if index != 0 and is_new_column:
                point = new_column(point)

            window.move(point)
            point = shift_row(point, width)

class Window(QtWidgets.QMainWindow):
    '''Main window with a custom event filter for all events.'''

    def __init__(self, parent=None, flags=QtCore.Qt.WindowType(0)):
        super().__init__(parent, flags)

        self.centralwidget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.resize(1068, 824)
        self.setWindowTitle('Custom SubWindow Style.')

        flags = compat.SubWindow
        flags |= compat.FramelessWindowHint
        self.area = MdiArea(self.centralwidget)
        self.window1 = SubWindow(flags=flags, sizegrip=True)
        self.window1.setWindowTitle('Short Title')
        self.area.addSubWindow(self.window1)
        self.table = LargeTable(self.window1.widget())
        self.window1.layout().addWidget(self.table)

        flags = compat.SubWindow
        flags |= compat.WindowContextHelpButtonHint
        flags |= compat.WindowShadeButtonHint
        flags |= compat.FramelessWindowHint
        self.window2 = SubWindow(flags=flags)
        self.window2.setWindowTitle('Example of a very, very long title')
        self.area.addSubWindow(self.window2)
        self.tree = SortableTree(self.window2.widget())
        self.window2.layout().addWidget(self.tree)

        flags = compat.SubWindow
        flags |= compat.WindowShadeButtonHint
        flags |= compat.FramelessWindowHint
        self.window3 = SubWindow(flags=flags, sizegrip=True)
        self.window3.setWindowTitle('Medium length title')
        self.area.addSubWindow(self.window3)
        self.layout.addWidget(self.area)
        self.tab = SettingTabs(self.window3.widget())
        self.window3.layout().addWidget(self.tab)

        # Tracking for move and resize events.
        # Click and drag title bar move.
        self._drag = None
        # Context menu move.
        self._move = None
        # Context menu resize.
        self._resize = None
        # SizeFrame resize.
        self._frame = None

    def set_cursor(self, cursor):
        '''Temporarily set the application cursor to the override cursor.'''

        app = QtWidgets.QApplication.instance()
        app.setOverrideCursor(QtGui.QCursor(cursor))

    def restore_cursor(self):
        '''Restore the overridden cursor.'''

        app = QtWidgets.QApplication.instance()
        app.restoreOverrideCursor()

    def start_drag(self, event):
        '''Start the drag state.'''
        self._drag = event.pos()

    def handle_drag(self, subwindow, event):
        '''Handle the drag event.'''
        subwindow.move_to(subwindow.mapToParent(event.pos() - self._drag))

    def end_drag(self):
        '''End the drag state.'''
        self._drag = None

    def start_move(self, widget):
        '''Start the move state.'''

        self._move = widget
        self._move.menu_move_to(QtGui.QCursor.pos())

    def handle_move(self, obj, event):
        '''Handle the move event.'''

        position = shared.single_point_global_position(args, event)
        self._move.menu_move_to(position)

    def end_move(self):
        '''End the move state.'''
        self._move = None

    def start_resize(self, widget):
        '''Start the resize state.'''

        self._resize = widget
        self.set_cursor(compat.SizeFDiagCursor)
        self._resize.menu_size_to(QtGui.QCursor.pos())

    def handle_resize(self, obj, event):
        '''Handle the resize event.'''

        position = shared.single_point_global_position(args, event)
        self._resize.menu_size_to(position)

    def end_resize(self):
        '''End the resize state.'''

        if self._resize is not None:
            self._resize = None
            self.restore_cursor()

    def start_frame(self, subwindow):
        '''Start the frame resize state.'''
        self._frame = subwindow

    def handle_frame(self, obj, event):
        '''Handle the frame resize event.'''
        self.window_frame_event(obj, event)

    def end_frame(self):
        '''End the frame resize state.'''
        self._frame = None

    def resolve_window_state(self):
        '''Handle theoretically possible conflicts in window state.'''

        # The _drag, _move, _resize, and _frame options are
        # mutually exclusive: only one can be active at a given time.
        # Since we use timers for `_move` and `_resize`, it's **possible**
        # multiple might be active here, but it's unlikely. So, we handle
        # those cases by playing favorites. _frame > _resize > _move > _drag.
        if self._frame is not None:
            self.end_resize()
        if self._resize is not None:
            self.end_move()
        if self._move is not None:
            self.end_drag()

    def window_move_event(self, obj, event):
        '''Handle window move events.'''

        if event.type() == compat.MouseMove:
            self.handle_move(obj, event)
        elif event.type() == compat.MouseButtonPress:
            self.end_move()

    def window_resize_event(self, obj, event):
        '''Handle window resize events.'''

        if event.type() == compat.MouseMove:
            self.handle_resize(obj, event)
        elif event.type() == compat.MouseButtonPress:
            self.end_resize()

    def window_frame_event(self, subwindow, event):
        '''Handle size adjustments using the window frame.'''

        frame = subwindow._sizeframe
        # Uses size grips, return early.
        if frame is None:
            return

        # No position for the event: we don't use it.
        if event.type() in (compat.Enter, compat.HoverEnter):
            frame.enter(event)
        elif event.type() in (compat.Leave, compat.HoverLeave):
            frame.leave(event)
        elif event.type() == compat.MouseMove:
            frame.mouse_move(event)
        elif event.type() == compat.MouseButtonPress:
            frame.mouse_press(event)
        elif event.type() == compat.MouseButtonRelease:
            frame.mouse_release(event)
        elif event.type() == compat.HoverMove:
            frame.hover_move(event)

        # Store if the frame state is active.
        if frame.is_active:
            self.start_frame(frame)
        else:
            self.end_frame()

    def eventFilter(self, obj, event):
        '''Custom event filter to handle move and resize events.'''

        self.resolve_window_state()
        if self._move is not None:
            # Cannot occur while the size frame is active.
            self.window_move_event(obj, event)
        elif self._resize is not None:
            self.window_resize_event(obj, event)
        elif isinstance(obj, SubWindow) and not obj.isMinimized():
            self.handle_frame(obj, event)

        return super().eventFilter(obj, event)

    def enterEvent(self, event):
        '''Reset the resize mouse on an enter event.'''

        if self._resize is not None:
            self.set_cursor(compat.SizeFDiagCursor)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        '''Reset the resize mouse on an enter event.'''

        if self._resize is not None:
            self.restore_cursor()
        return super().leaveEvent(event)

def main():
    'Application entry point'

    app, window = shared.setup_app(args, unknown, compat, window_class=Window)
    app.installEventFilter(window)

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
