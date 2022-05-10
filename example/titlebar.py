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
    to capture titlebar and frame events. This example can also be easily
    applied to a top-level window.

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

    NOTE: you cannot correctly emulate a title bar if the desktop environment
    is Wayland, even if the app is running in X11 mode. This mostly affects
    just the top-level title bar (and subwindows almost entirely work),
    but there are a few small issues for subwindows.

    The top-level title bar can have a few issues on Wayland.
    - Cannot move the window position. This cannot be done even if you know
        the compositor (such as kwin).
    - Cannot use the menu resize due to `QWidget::mouseGrab()`.
        - This plugin supports grabbing the mouse only for popup windows
        - The window stops tracking mouse movements past a certain distance.
    - Attempting to move the window position causes global position to be wrong.
    - Wayland does not support `Stay on Top` directive.
        - qt.qpa.wayland: Wayland does not support QWindow::requestActivate()

    A few other issues exist on Wayland.
    - The menu resize has to guess the mouse position outside of the window bounds.
        - This cannot be fixed since we cannot use mouse events if the user
            is outside the main window, nor do hover events trigger.
            We cannot guess where the user left the main window, since
            `QCursor::pos` will not be updated until the user moves the
            mouse within the application, so merely resizing until the
            actual cursor is within the window won't work.
    - We cannot intercept mouse events for the menu resize outside the window.
        - This even occurs when forcing X11 on Wayland.

    On Windows, only the menu resize event fails. For the subwindow, it stops
    tracking outside of the window boundaries, and for the main window, it does
    the same, making it practically useless.

    # Testing

    The current platforms/desktop environments have been tested:
    - Gnome (X11, Wayland)
    - KDE Plasma (X11, Wayland)
    - Windows 10
'''

import enum
import os
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
parser.add_argument(
    '--default-window-frame',
    help='use the default title bars',
    action='store_true',
)
parser.add_argument(
    '--status-bar',
    help='use a top-level status bar',
    action='store_true',
)
parser.add_argument(
    '--window-help',
    help='add a top-level context help button',
    action='store_true',
)
parser.add_argument(
    '--window-shade',
    help='add a top-level shade/unshade button',
    action='store_true',
)
parser.add_argument(
    '--wayland-testing',
    help='debug with a custom titlebar on wayland',
    action='store_true',
)
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)
ICON_MAP = shared.get_icon_map(args, compat)
# 100ms between repaints, so we avoid over-repainting.
# Allows us to avoid glitchy motion during drags/
REPAINT_TIMER = 100
TRACK_TIMER = 20
CLICK_TIMER = 20
# Make the titlebar size too large, so we can get the real value with min.
TITLEBAR_HEIGHT = 2**16
# QWIDGETSIZE_MAX isn't exported, which is needed to remove fixedSize constraints.
QWIDGETSIZE_MAX = (1 << 24) - 1

# Determine the Linux display server protocol we're using.
# Use `XDG_SESSION_TYPE`, since we can override it for X11.
IS_WAYLAND = os.environ.get('XDG_SESSION_TYPE') == 'wayland'
IS_XWAYLAND = os.environ.get('XDG_SESSION_TYPE') == 'xwayland'
IS_X11 = os.environ.get('XDG_SESSION_TYPE') == 'x11'
# We can run X11 on Wayland, but this doesn't support certain
# features like mouse grabbing, so we don't use it here.
IS_TRUE_WAYLAND = 'WAYLAND_DISPLAY' in os.environ
USE_WAYLAND_FRAME = IS_WAYLAND and not args.wayland_testing

# Add a warning if we're using Wayland with a custom titlebar.
if not args.default_window_frame and USE_WAYLAND_FRAME:
    print('WARNING: Wayland does not support custom title bars.', file=sys.stderr)
    print('Applications in Wayland cannot set their own position.', file=sys.stderr)
    print('Defaulting to the system title bar instead.', file=sys.stderr)

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
TOP_EDGES = (WindowEdge.Top, WindowEdge.TopLeft, WindowEdge.TopRight)
BOTTOM_EDGES = (WindowEdge.Bottom, WindowEdge.BottomLeft, WindowEdge.BottomRight)
LEFT_EDGES = (WindowEdge.Left, WindowEdge.TopLeft, WindowEdge.BottomLeft)
RIGHT_EDGES = (WindowEdge.Right, WindowEdge.TopRight, WindowEdge.BottomRight)

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

# RESIZE HELPERS

def border_size(self):
    '''Get the size of the border, regardless if present.'''
    return QtCore.QSize(2 * self._border, 2 * self._border)

def minimized_content_size(self):
    '''Get the minimum content size of the widget.'''
    return self._titlebar_size

def minimized_size(self):
    '''Get the minimum size of the widget, with the size grips hidden.'''

    size = self.minimized_content_size
    if self._border:
        size = size + self.border_size
    return size

def minimum_size(self):
    '''Get the minimum size for the widget.'''

    size = self.minimized_size
    if getattr(self, '_sizegrip', None) is not None and self._sizegrip.isVisible():
        # Don't modify in place: percolates later.
        size = size + self._sizegrip_size

    if getattr(self, '_statusbar', None) is not None and self._statusbar.isVisible():
        size = size + self._statusbar_size

    return size

def get_larger_size(x, y):
    '''Get the larger of the two sizes, for both the height and width.'''
    return QtCore.QSize(max(x.width(), y.width()), max(x.height(), y.height()))

def set_minimum_size(self):
    '''Sets the minimum size of the window and the titlebar, with clobbering.'''

    self._old_minimum_size = self.minimumSize()
    self._titlebar.set_minimum_size()
    self._titlebar_size = self._titlebar.minimumSize()
    self.setMinimumSize(self.minimum_size)

def set_larger_minimum_size(self):
    '''Sets the minimum size of the window and the titlebar, without clobbering.'''

    if self._old_minimum_size is not None:
        self.setMinimumSize(self._old_minimum_size)
    self._titlebar.set_minimum_size()
    self._titlebar_size = self._titlebar.minimumSize()
    size = get_larger_size(self.minimum_size, self.minimumSize())
    self.setMinimumSize(size)

def move_to(self, position):
    '''Move the window to the desired position'''

    # Also updates the stored previous subwindow position, if applicable.
    # This means shading/unshading uses the new position of the window,
    # but the old sizes, rather than jump the window back.
    # NOTICE: this fails on Wayland. Worse, using `QMainWindow::move` on
    # Wayland causes the cursor position to be incorrect, causing issues
    # with other events.
    if IS_WAYLAND and self.window() == self:
        return

    self.move(position)
    rect = self._titlebar._window_rect
    if rect is not None:
        rect.moveTo(position)

def set_geometry(self, rect):
    '''Set the window geometry.'''

    # See `move_to` for documentation.
    self.resize(rect.size())
    window_rect = self._titlebar._window_rect
    if window_rect is not None:
        window_rect.setSize(rect.size())

    move_to(self, rect.topLeft())

def shade(self, size, grip_type):
    '''Shade the window, hiding the main widget and size grip.'''

    self._widget.hide()
    if getattr(self, f'_{grip_type}') is not None:
        getattr(self, f'_{grip_type}').hide()
    self.set_minimum_size()
    self.resize(size)

def unshade(self, rect, grip_type):
    '''Unshade the window, showing the main widget and size grip.'''

    self._widget.show()
    if getattr(self, f'_{grip_type}') is not None:
        getattr(self, f'_{grip_type}').show()
    self.set_larger_minimum_size()
    self.set_geometry(rect)

def start_drag(self, event, window_type):
    '''Start the window drag state.'''
    setattr(self, f'_{window_type}_drag', event.pos())

def handle_drag(self, event, window, window_type):
    '''Handle the window drag event.'''

    position = event.pos() - getattr(self, f'_{window_type}_drag')
    window.move_to(window.mapToParent(position))

def end_drag(self, window_type):
    '''End the window drag state.'''
    setattr(self, f'_{window_type}_drag', None)

def start_move(self, widget, window_type):
    '''Start the window move state.'''

    setattr(self, f'_{window_type}_move', widget)
    widget.menu_move_to(QtGui.QCursor.pos())

def handle_move(self, position, window_type):
    '''Handle the window move event.'''
    getattr(self, f'_{window_type}_move').menu_move_to(position)

def end_move(self, window_type):
    '''End the window move state.'''
    setattr(self, f'_{window_type}_move', None)

def start_resize(self, window, window_type):
    '''Start the window resize state.'''

    # NOTE: We can't use a rubber band with mouse tracking,
    # since mouse events only occurs if the user is holding
    # down the house. Simulating a mouse click isn't enough,
    # even if it sends a mouse press without a release.
    setattr(self, f'_{window_type}_resize', window)
    self.window().setCursor(compat.SizeFDiagCursor)
    self.menu_size_to(QtGui.QCursor.pos())

    # Grab the mouse so we can intercept the click event,
    # and track hover events outside the app. This doesn't
    # work on Wayland or on macOS.
    #   https://doc.qt.io/qt-5/qwidget.html#grabMouse
    if not IS_TRUE_WAYLAND and not sys.platform == 'darwin':
        self.window().grabMouse()

def handle_resize(self, position):
    '''Handle the window resize event.'''
    self.menu_size_to(position)

def end_resize(self, window_type):
    '''End the window resize state.'''

    window = getattr(self, f'_{window_type}_resize')
    if window is None:
        return

    setattr(self, f'_{window_type}_resize', None)
    window.window().unsetCursor()
    if not IS_TRUE_WAYLAND and not sys.platform == 'darwin':
        self.window().releaseMouse()

def start_frame(self, frame, window_type):
    '''Start the window frame resize state.'''
    setattr(self, f'_{window_type}_frame', frame)

def handle_frame(self, window, event, window_type):
    '''Handle the window frame resize event.'''

    # Check if use size grips, return early.
    frame = getattr(window, '_sizeframe', None)
    if frame is None:
        return
    self.frame_event(event, frame)

    # Store if the frame state is active.
    if frame.is_active and not getattr(self, f'_{window_type}_frame'):
        start_frame(self, frame, window_type)
    elif not frame.is_active and getattr(self, f'_{window_type}_frame'):
        end_frame(self, window_type)

def end_frame(self, window_type):
    '''End the window frame resize state.'''
    setattr(self, f'_{window_type}_frame', None)

# EVENT HANDLES

def window_resize_event(self, event):
    '''Ensure titlebar text elides normally.'''

    # Need to trigger the titlebar title resize. Need to handle it
    # here, since the SizeFrame resizes won't always trigger a
    # Label::resizeEvent, which can cause the text to stay elided.
    title_timer = self._titlebar._title._timer
    title_timer.start(REPAINT_TIMER)

    super(type(self), self).resizeEvent(event)


def window_show_event(self, event, grip_type):
    '''Set the minimum size policies once the widgets are shown.'''

    # Until shown, the size grip has inaccurate sizes.
    # Set the minimum size policy of the widget.
    # The show event occurs just after everything is shown,
    # so the widget sizes (and isVisible) are accurate.
    self._titlebar_size = self._titlebar.minimumSize()
    if getattr(self, f'_{grip_type}') is not None:
        grip_size = getattr(self, f'_{grip_type}').sizeHint()
        setattr(self, f'_{grip_type}_size', QtCore.QSize(0, grip_size.height()))
    size = get_larger_size(self.minimum_size, self.minimumSize())
    self.setMinimumSize(size)

    super(type(self), self).showEvent(event)

def window_mouse_double_click_event(self, event):
    '''Override the mouse double click, and don't call the press event.'''

    # By default, the flowchart for titlebar double clicks is as follows:
    #   1. If minimized, restore
    #   2. If maximized, restore
    #   3. If no state and can shade, shade
    #   4. If no state and cannot shade, maximize
    #   5. If shaded, unshade.
    widget = self._titlebar
    if not widget.underMouse() or event.button() != compat.LeftButton:
        return super(type(self), self).mouseDoubleClickEvent(event)
    if widget._is_shaded:
        widget.unshade()
    elif widget.isMinimized() or widget.isMaximized():
        widget.restore()
    elif widget._has_shade:
        widget.shade()
    else:
        widget.maximize()

def window_mouse_press_event(self, event, window, window_type):
    '''Override a mouse click on the titlebar to allow a move.'''

    widget = self._titlebar
    if widget.underMouse():
        # `self.window()._subwindow_move` cannot be set, since we're inside
        # the global event filter here. We handle conflicts here,
        # so only one of the 4 states can be set. We can't move
        # minimized widgets, so don't try.
        is_left = event.button() == compat.LeftButton
        is_minimized = self.isMinimized() and not widget._is_shaded
        has_frame = getattr(window, f'_{window_type}_frame') is not None
        if is_left and not is_minimized and not has_frame:
            start_drag(self.window(), event, window_type)
        elif event.button() == compat.RightButton:
            position = shared.single_point_global_position(args, event)
            shared.execute(args, widget._main_menu, position)
    return super(type(self), self).mousePressEvent(event)

def window_mouse_move_event(self, event, window, window_type):
    '''Reposition the window on the move event.'''

    if getattr(window, f'_{window_type}_frame') is not None:
        end_drag(window, window_type)
    if getattr(window, f'_{window_type}_drag') is not None:
        handle_drag(window, event, self, window_type)
    return super(type(self), self).mouseMoveEvent(event)

def window_mouse_release_event(self, event, window, window_type):
    '''End the drag event.'''

    end_drag(window, window_type)
    return super(type(self), self).mouseReleaseEvent(event)

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

class TitleBar(QtWidgets.QFrame):
    '''Custom instance of a QTitlebar'''

    def __init__(self, window, parent=None, flags=None):
        super().__init__(parent)

        # Get and set some properties.
        self.setProperty('isTitlebar', True)
        self._window = window
        self._window_type = 'window'
        if isinstance(self._window, SubWindow):
            self._window_type = 'subwindow'
        self._state = compat.WindowNoState
        self._window_rect = None
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
        self._layout.addWidget(self._title, 0, col, compat.AlignHCenter)
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
        if self._has_shade:
            self._unshade.hide()

        # Add in our event triggers.
        self._min.clicked.connect(self.minimize)
        self._max.clicked.connect(self.maximize)
        self._restore.clicked.connect(self.restore)
        self._close.clicked.connect(self._window.close)
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
        '''Get if the titlebar and therefore window has no state.'''
        return self._state == compat.WindowNoState

    def isMinimized(self):
        '''Get if the titlebar and therefore window is minimized.'''
        return self._state == compat.WindowMinimized

    def isMaximized(self):
        '''Get if the titlebar and therefore window is maximized.'''
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
        start_move(self.window(), self, self._window_type)

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

        window = self._window
        window.move_to(window.mapToParent(rect.topLeft()))

    def size_timer(self):
        '''Start timer to invoke menu_size.'''

        # We use a timer since the clicks on the menu can invoke the
        # MousePressEvent, which instantly cancels the size event.
        self._size_timer.start(CLICK_TIMER)

    def menu_size(self):
        '''Start a manually triggered resize event.'''

        window = self.window()
        start_resize(window, self._window, self._window_type)

    def minimize(self):
        '''Minimize the current window.'''

        if self.isNormal():
            self._window_rect = self._window.geometry()
        self.set_minimized()
        self.set_shaded()

        # Toggle state
        self._state = compat.WindowMinimized
        self._is_shaded = False
        self._window.minimize(self._window.minimized_size)

        # Toggle the menu actions
        # Minimized windows should not be movable, resizable, or minimizable.
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(False)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(False)
        self._max_action.setEnabled(True)

    def maximize(self):
        '''Maximize the current window.'''

        if self.isNormal():
            self._window_rect = self._window.geometry()
        elif self.isMinimized() and not self._is_shaded:
            self._window.unminimize()
        size = self._window.maximum_size
        rect = QtCore.QRect(0, 0, size.width(), size.height())
        self.set_maximized()
        self.set_unshaded()

        # Toggle state
        self._state = compat.WindowMaximized
        self._is_shaded = False
        self._window.maximize(rect)

        # Toggle the menu actions
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(False)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(False)

    def restore(self):
        '''Restore the current window (set to no state).'''

        if self.isMinimized() and not self._is_shaded:
            self._window.unminimize()
        self.set_restored()
        self.set_unshaded()

        # Toggle state
        self._state = compat.WindowNoState
        self._is_shaded = False
        self._window.restore(self._window_rect)

        # Toggle the menu actions
        self._restore_action.setEnabled(False)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(True)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(True)

    def shade(self):
        '''Shade the current window.'''

        # Shaded windows are treated as if they have minimized state, and
        # if the window is maximized, it sets the previous window rect
        # to the maximized geometry.
        self.set_shaded()
        self.set_minimized()

        # Toggle state
        self._state = compat.WindowMinimized
        self._is_shaded = True
        self._window_rect = self._window.geometry()
        width = self._window.width()
        height = self._window.minimized_size.height()
        self._window.shade(QtCore.QSize(width, height))

        # Toggle the menu actions
        # Shaded windows should be movable, but not resizable or minimizable.
        self._restore_action.setEnabled(True)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(False)
        self._min_action.setEnabled(False)
        self._max_action.setEnabled(True)

    def unshade(self):
        '''Unshade the current window.'''

        if self.isMinimized() and not self._is_shaded:
            self._window.unminimize()

        # If the window is minimized, it restores to the previous
        # window state and position.
        self.set_unshaded()
        self.set_restored()

        # Toggle state
        self._state = compat.WindowNoState
        self._is_shaded = False
        self._window.unshade(self._window_rect)

        # Toggle the menu actions
        # Unshaded windows have no state: they are restored.
        self._restore_action.setEnabled(False)
        self._move_action.setEnabled(True)
        self._size_action.setEnabled(True)
        self._min_action.setEnabled(True)
        self._max_action.setEnabled(True)

    def toggle_keep_above(self, checked):
        '''Toggle whether to keep the window above others.'''

        # If we have a top-level widget, changing the window
        # flags causes `setParent` to be called, causing the
        # widget to hide and then re-appear. This causes major
        # visual delay, so we just ignore the hide event, then
        # set the flags, re-show the window, and unignore hides.
        # Finally, this can change the geometry of the window,
        # so we need to store the geometry and reset it.
        if self._window.window() == self._window:
            self._window._ignore_hide = True
            rect = self.window().geometry()

        flags = self._window.windowFlags()
        if checked:
            flags |= compat.WindowStaysOnTopHint
        else:
            flags &= ~compat.WindowStaysOnTopHint
        self._window.setWindowFlags(flags)

        if self._window.window() == self._window:
            self._window._ignore_hide = False
            self.window().show()
            self.window().set_geometry(rect)

    def help(self):
        '''Enter what's this mode.'''
        QtWidgets.QWhatsThis.enterWhatsThisMode()

    # VIEW

    def set_minimized(self):
        '''Show the restore and maximize icons.'''

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

    def set_maximized(self):
        '''Show the minimize and restore icons.'''

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

    def set_restored(self):
        '''Show the minimize and maximize icons.'''

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

    def top_left(self, rect):
        '''Get the top/left position of the window in global coordinates.'''

        # Calculate the top left bounds of our window to get our frame.
        # We want our frame in global coordinates, but our window
        # might be a subwindow. If it has a parent, then it's a subwindow
        # and we need to map our coordinates.
        point = rect.topLeft()
        if self._window.window() != self._window:
            point = self._window.parent().mapToGlobal(point)

        return point

    def frame_geometry(self):
        '''Calculate the frame geometry of our window in global coordinates.'''

        rect = self._window.frameGeometry()
        return QtCore.QRect(self.top_left(rect), self._window.frameSize())

    def geometry(self):
        '''Calculate the geometry of our window in global coordinates.'''

        rect = self._window.geometry()
        return QtCore.QRect(self.top_left(rect), self._window.size())

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

    def resize(self, position, rect):
        '''Resize our window to the adjusted dimensions.'''

        # Get our new frame dimensions.
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
            point = self._window.parent().mapFromGlobal(point)
        local_rect = QtCore.QRect(point, size)

        # If we have a subwindow, need to limit to the MDI area rect.
        if self._window.window() != self._window:
            area_rect = self._window.mdiArea().contentsRect()
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

        self._window.set_geometry(local_rect)
        self._band.setGeometry(rect)

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

        self.resize(position, self._band.geometry())

    def mouse_press(self, event):
        '''Handle the mousePressEvent of the window.'''

        if event.button() == compat.LeftButton:
            position = shared.single_point_global_position(args, event)
            rect = self.frame_geometry()
            self._press_edge = self.cursor_position(position, rect)
            # We want to separately handle drags, so only
            # set this if we are pressing on the edge.
            if self._press_edge != WindowEdge.NoEdge:
                self._pressed = True
                self._band.setGeometry(self.geometry())

    def mouse_release(self, event):
        '''Handle the mouseReleaseEvent of the window.'''

        if event.button() == compat.LeftButton and self._pressed:
            self._pressed = False

    def hover_move(self, event):
        '''Handle the hoverMoveEvent of the window.'''

        position = shared.single_point_position(args, event)
        self.update_cursor(self._window.mapToGlobal(position))

class SubWindow(QtWidgets.QMdiSubWindow):
    '''Base subclass for a QMdiSubwindow.'''

    def __init__(self, parent=None, flags=QtCore.Qt.WindowType(0)):
        super().__init__(parent, flags=flags)
        super().setWidget(QtWidgets.QWidget())

class DefaultSubWindow(SubWindow):
    '''Default subwindow with a window frame.'''

    def __init__(
        self,
        parent=None,
        flags=QtCore.Qt.WindowType(0),
        sizegrip=False,
    ):
        super().__init__(parent, flags=flags)

class FramelessSubWindow(SubWindow):
    '''Custom subwindow instance without a window frame.'''

    def __init__(
        self,
        parent=None,
        flags=QtCore.Qt.WindowType(0),
        sizegrip=False,
    ):
        super().__init__(parent, flags=flags | compat.FramelessWindowHint)

        # Create our widgets. Sizeframe and sizegrip are mutually exclusive.
        self._central = QtWidgets.QFrame(super().widget())
        self._central.setLayout(QtWidgets.QVBoxLayout())
        self._titlebar = TitleBar(self, self._central, flags)
        self._widget = QtWidgets.QWidget(self._central)
        self._widget.setLayout(QtWidgets.QVBoxLayout())
        self._sizeframe = None
        self._sizegrip = None
        self._border = args.border_width
        self._titlebar_size = QtCore.QSize()
        self._sizegrip_size = QtCore.QSize()
        self._old_minimum_size = None
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
        return border_size(self)

    @property
    def minimized_content_size(self):
        '''Get the minimum content size of the widget.'''
        return minimized_content_size(self)

    @property
    def minimized_size(self):
        '''Get the minimum size of the widget, with the size grips hidden.'''
        return minimized_size(self)

    @property
    def minimum_size(self):
        '''Get the minimum size for the widget.'''
        return minimum_size(self)

    @property
    def maximum_size(self):
        '''Get the maximum size for the widget.'''
        return self.mdiArea().size()

    # RESIZE

    def move_to(self, position):
        '''Move the window to the desired position'''
        move_to(self, position)

    def set_geometry(self, rect):
        '''Set the window geometry.'''
        set_geometry(self, rect)

    def set_minimum_size(self):
        '''Sets the minimum size of the window and the titlebar, with clobbering.'''
        set_minimum_size(self)

    def set_larger_minimum_size(self):
        '''Sets the minimum size of the window and the titlebar, without clobbering.'''
        set_larger_minimum_size(self)

    def minimize(self, size):
        '''Minimize the window, hiding the main widget and size grip.'''

        self._widget.hide()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.set_minimum_size()
        self.resize(size)
        self.mdiArea().minimize(self)

    def maximize(self, rect):
        '''Maximize the window, showing the main widget and hiding size grip.'''

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.hide()
        self.set_larger_minimum_size()
        self.set_geometry(rect)

    def restore(self, rect):
        '''Restore the window, showing the main widget and size grip.'''

        self._widget.show()
        if self._sizegrip is not None:
            self._sizegrip.show()
        self.set_larger_minimum_size()
        self.set_geometry(rect)

    def shade(self, size):
        '''Shade the window, hiding the main widget and size grip.'''
        shade(self, size, 'sizegrip')

    def unshade(self, rect):
        '''Unshade the window, showing the main widget and size grip.'''
        unshade(self, rect, 'sizegrip')

    def unminimize(self):
        '''Unminimize a minimized subwindow.'''
        self.mdiArea().unminimize(self)

    # QT EVENTS

    def resizeEvent(self, event):
        '''Handle widget resize events here.'''
        window_resize_event(self, event)

    def showEvent(self, event):
        '''Set the minimum size policies once the widgets are shown.'''
        window_show_event(self, event, 'sizegrip')

    def mouseDoubleClickEvent(self, event):
        '''Override the mouse double click, and don't call the press event.'''
        window_mouse_double_click_event(self, event)

    def mousePressEvent(self, event):
        '''Override a mouse click on the titlebar to allow a move.'''
        return window_mouse_press_event(self, event, self.window(), 'subwindow')

    def mouseMoveEvent(self, event):
        '''Reposition the window on the move event.'''
        return window_mouse_move_event(self, event, self.window(), 'subwindow')

    def mouseReleaseEvent(self, event):
        '''End the drag event.'''
        return window_mouse_release_event(self, event, self.window(), 'subwindow')

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
        return self._titlebar.isMaximized()

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
    '''Base subclass for a QMainWindow.'''

    def __init__(self, parent=None, flags=QtCore.Qt.WindowType(0)):
        super().__init__(parent, flags)

        # Tracking for move and resize events.
        # Click and drag title bar move.
        self._subwindow_drag = None
        # Context menu move.
        self._subwindow_move = None
        # Context menu resize.
        self._subwindow_resize = None
        # SizeFrame resize.
        self._subwindow_frame = None

    def setup(self):
        '''Setup the main UI.'''

        subwindow_class = FramelessSubWindow
        if args.default_window_frame:
            subwindow_class = DefaultSubWindow

        self.resize(1068, 824)
        self.setWindowTitle('Custom SubWindow Style.')

        flags = compat.SubWindow
        self.area = MdiArea(self._widget)
        self.window1 = subwindow_class(flags=flags, sizegrip=True)
        self.window1.setWindowTitle('Short Title')
        self.area.addSubWindow(self.window1)
        self.table = LargeTable(self.window1.widget())
        self.window1.layout().addWidget(self.table)

        flags = compat.SubWindow
        flags |= compat.WindowContextHelpButtonHint
        flags |= compat.WindowShadeButtonHint
        self.window2 = subwindow_class(flags=flags)
        self.window2.setWindowTitle('Example of a very, very long title')
        self.area.addSubWindow(self.window2)
        self.tree = SortableTree(self.window2.widget())
        self.window2.layout().addWidget(self.tree)

        flags = compat.SubWindow
        flags |= compat.WindowShadeButtonHint
        self.window3 = subwindow_class(flags=flags, sizegrip=True)
        self.window3.setWindowTitle('Medium length title')
        self.area.addSubWindow(self.window3)
        self._widget.layout().addWidget(self.area)
        self.tab = SettingTabs(self.window3.widget())
        self.window3.layout().addWidget(self.tab)

    # PROPERTIES

    @property
    def maximum_size(self):
        '''Get the maximum size for the window.'''
        # Unused since we use the window flags anyway.
        return self.maximumSize()

    # ACTIONS

    def menu_size_to(self, point):
        '''
        Size the window so that the position is in the center bottom
        of the title bar. The position is given in global coordinates.
        '''

        window = getattr(self, '_window_resize', None)
        if window is None:
            window = self._subwindow_resize
        rect = window.geometry()
        # We add a trivial amount so we avoid a bug where we are
        # exactly on the sizegrip, which keeps us in resize mode
        # unless we do another button click, we weirdly doesn't
        # work well when simulated.
        point += QtCore.QPoint(2, 2)

        # If we have a subwindow, need to limit to the MDI area rect.
        if window.window() != window:
            point = window.parent().mapFromGlobal(point)
            area_rect = window.mdiArea().contentsRect()
            point.setX(min(point.x(), area_rect.right()))
            point.setY(min(point.y(), area_rect.bottom()))

        # Need to ensure we didn't go past the top left.
        # Don't want to shift to negative values.
        top_left = rect.topLeft()
        point.setX(max(top_left.x(), point.x()))
        point.setY(max(top_left.y(), point.y()))

        # We add a trivial amount to simplify growing the window on Wayland.
        # Wayland cannot track outside of the application.
        if IS_TRUE_WAYLAND and window.window() == window:
            point += QtCore.QPoint(16, 16)
        rect.setBottomRight(point)
        window.set_geometry(rect)

        # Ensure we trigger the elide resize timer.
        titlebar = window._titlebar
        titlebar._title._timer.start(REPAINT_TIMER)

    def resolve_state(self):
        '''Handle theoretically possible conflicts in window state.'''

        # The _drag, _move, _resize, and _frame options are
        # mutually exclusive: only one can be active at a given time.
        # Since we use timers for `_move` and `_resize`, it's **possible**
        # multiple might be active here, but it's unlikely. So, we handle
        # those cases by playing favorites. _frame > _resize > _move > _drag.
        # We deal with the window-level widgets first, then the subwindow-level
        # widgets next. We use `getattr(obj, attr, None)` for the window-level
        # widgets since they might not be present (if using Wayland).

        has_state = False
        if has_state or getattr(self, f'_window_frame', None) is not None:
            end_resize(self, 'window')
            has_state = True
        if has_state or getattr(self, f'_window_resize', None) is not None:
            end_move(self, 'window')
            has_state = True
        if has_state or getattr(self, f'_window_move', None) is not None:
            end_drag(self, 'window')
            has_state = True
        if has_state or getattr(self, f'_window_drag', None) is not None:
            end_frame(self, 'window')
            has_state = True
        if has_state or self._subwindow_frame is not None:
            end_resize(self, 'subwindow')
            has_state = True
        if has_state or self._subwindow_resize is not None:
            end_move(self, 'subwindow')
            has_state = True
        if has_state or self._subwindow_move is not None:
            end_drag(self, 'subwindow')
            has_state = True

    def move_event(self, _, event, window_type):
        '''Handle window move events.'''

        if event.type() == compat.MouseMove:
            position = shared.single_point_global_position(args, event)
            handle_move(self, position, window_type)
        elif event.type() == compat.MouseButtonPress:
            end_move(self, window_type)

    def resize_event(self, obj, event, window_type):
        '''Handle window resize events.'''

        # NOTE: If we're on Wayland, we cant' track hover events outside the
        # main widget, and we can't guess intermittently since if the mouse
        # doesn't move, we won't get an `Enter` or `HoverEnter` event, and
        # `QCursor::pos` will always be the same. What this means is we
        # can't guess where we left the, and resize until we're back
        # in the bounds.
        if event.type() in (compat.MouseMove, compat.HoverMove):
            position = shared.single_point_global_position(args, event)
            handle_resize(self, position)
        elif event.type() == compat.MouseButtonPress:
            end_resize(self, window_type)

    def frame_event(self, event, frame):
        '''Handle size adjustments using the window frame.'''

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

    # QT EVENTS

    def eventFilter(self, obj, event):
        '''Custom event filter to handle move and resize events.'''

        self.resolve_state()
        if getattr(self, '_window_move', None) is not None:
            # Cannot occur while the size frame is active.
            self.move_event(obj, event, 'window')
        elif getattr(self, '_window_resize', None) is not None:
            self.resize_event(obj, event, 'window')
        elif isinstance(obj, Window) and not obj.isMinimized():
            handle_frame(self, obj, event, 'window')
        elif self._subwindow_move is not None:
            # Cannot occur while the size frame is active.
            self.move_event(obj, event, 'subwindow')
        elif self._subwindow_resize is not None:
            self.resize_event(obj, event, 'subwindow')
        elif isinstance(obj, SubWindow) and not obj.isMinimized():
            handle_frame(self, obj, event, 'subwindow')

        return super().eventFilter(obj, event)

class DefaultWindow(Window):
    '''Default main window with a window frame.'''

    def __init__(self, parent=None, flags=QtCore.Qt.WindowType(0)):
        if args.window_help:
            flags |= compat.WindowContextHelpButtonHint
        if args.window_shade:
            flags |= compat.WindowShadeButtonHint
        super().__init__(parent, flags)

        self._central = QtWidgets.QFrame(self)
        self._layout = QtWidgets.QVBoxLayout(self._central)
        self.setCentralWidget(self._central)
        self._widget = QtWidgets.QWidget(self._central)
        self._widget.setLayout(QtWidgets.QVBoxLayout())
        self._central.layout().addWidget(self._widget, 10)

        if args.status_bar:
            self._statusbar = QtWidgets.QStatusBar(self._central)
            self.setStatusBar(self._statusbar)

        self.setup()

class FramelessWindow(Window):
    '''Main window with a custom event filter for all events.'''

    def __init__(self, parent=None, flags=QtCore.Qt.WindowType(0)):
        # On X11, the `WindowStaysOnTopHint` hint supposedly doesn't
        # work unless you bypass the window manager, but this seems
        # to no longer be true. There's major downsides to bypassing
        # the window manager, so it's not worth it anyway.
        flags |= compat.FramelessWindowHint
        if args.window_help:
            flags |= compat.WindowContextHelpButtonHint
        if args.window_shade:
            flags |= compat.WindowShadeButtonHint
        super().__init__(parent, flags)

        # Create our widgets. Sizeframe and sizegrip are mutually exclusive.
        self._central = QtWidgets.QFrame(self)
        self._layout = QtWidgets.QVBoxLayout(self._central)
        self.setCentralWidget(self._central)
        self._titlebar = TitleBar(self, self._central, flags)
        self._widget = QtWidgets.QWidget(self._central)
        self._widget.setLayout(QtWidgets.QVBoxLayout())
        self._sizeframe = None
        self._statusbar = None
        self._border = args.border_width
        self._titlebar_size = QtCore.QSize()
        self._statusbar_size = QtCore.QSize()
        self._old_minimum_size = None
        if args.status_bar:
            self._statusbar = QtWidgets.QStatusBar(self._central)
            self.setStatusBar(self._statusbar)
        else:
            self._sizeframe = SizeFrame(self, border_width=5)

        self._central.layout().setSpacing(0)
        self._central.layout().addWidget(self._titlebar, 0, compat.AlignTop)
        self._central.layout().addWidget(self._widget, 10)

        # Tracking for move and resize events.
        # Click and drag title bar move.
        self._window_drag = None
        # Context menu move.
        self._window_move = None
        # Context menu resize.
        self._window_resize = None
        # SizeFrame resize.
        self._window_frame = None

        # For toggling window flags, which calls `setParent`, hiding the window.
        # Since an immediate show causes an unminimize/re-minimize, this
        # causes a serious visual lag.
        self._ignore_hide = False

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

        self.setup()

    # HACKS

    def hide(self):
        '''Override the hide event to ignore it if desired.'''

        if self._ignore_hide:
            return
        super().hide()

    def setVisible(self, value):
        '''Override the hide event to ignore it if desired.'''

        if self._ignore_hide and not value:
            return
        super().setVisible(value)

    # PROPERTIES

    @property
    def border_size(self):
        '''Get the size of the border, regardless if present.'''
        return border_size(self)

    @property
    def minimized_content_size(self):
        '''Get the minimum content size of the widget.'''
        return minimized_content_size(self)

    @property
    def minimized_size(self):
        '''Get the minimum size of the widget, with the size grips hidden.'''
        return minimized_size(self)

    @property
    def minimum_size(self):
        '''Get the minimum size for the widget.'''
        return minimum_size(self)

    # QT-LIKE PROPERTIES

    def windowTitle(self):
        '''Get the window title from the titlebar.'''
        return self._titlebar.windowTitle()

    def setWindowTitle(self, title):
        '''Get the window title from the titlebar.'''
        self._titlebar.setWindowTitle(title)

    # RESIZE

    def move_to(self, position):
        '''Move the window to the desired position'''
        move_to(self, position)

    def set_geometry(self, rect):
        '''Set the window geometry.'''
        set_geometry(self, rect)

    def set_minimum_size(self):
        '''Sets the minimum size of the window and the titlebar, with clobbering.'''
        set_minimum_size(self)

    def set_larger_minimum_size(self):
        '''Sets the minimum size of the window and the titlebar, without clobbering.'''
        set_larger_minimum_size(self)

    def minimize(self, _):
        '''Minimize the window, using the actual OS to handle that.'''
        self.showMinimized()

    def maximize(self, _):
        '''Minimize the window, using the actual OS to handle that.'''
        self.showMaximized()

    def restore(self, _):
        '''Restore the window, showing the main widget and size grip.'''
        self.showNormal()

    def showNormal(self):
        super().showNormal()

    def shade(self, size):
        '''Shade the window, hiding the main widget and size grip.'''
        shade(self, size, 'statusbar')

    def unshade(self, rect):
        '''Unshade the window, showing the main widget and size grip.'''
        unshade(self, rect, 'statusbar')

    def unminimize(self):
        '''Unminimize a minimized window (unimplemented).'''

    # QT EVENTS

    def resizeEvent(self, event):
        '''Handle widget resize events here.'''
        window_resize_event(self, event)

    def showEvent(self, event):
        '''Set the minimum size policies once the widgets are shown.'''
        window_show_event(self, event, 'statusbar')

    def mouseDoubleClickEvent(self, event):
        '''Override the mouse double click, and don't call the press event.'''
        window_mouse_double_click_event(self, event)

    def mousePressEvent(self, event):
        '''Override a mouse click on the titlebar to allow a move.'''
        return window_mouse_press_event(self, event, self, 'window')

    def mouseMoveEvent(self, event):
        '''Reposition the window on the move event.'''
        return window_mouse_move_event(self, event, self, 'window')

    def mouseReleaseEvent(self, event):
        '''End the drag event.'''
        return window_mouse_release_event(self, event, self, 'window')

    def changeEvent(self, event):
        '''Catch state changes from outside our custom titlebar.'''

        super().changeEvent(event)

        # If we're restoring a top-level widget, need to ensure the
        # state is properly restored to the correct icons.
        if event.type() not in (compat.ActivationChange, compat.WindowStateChange):
            return

        # We have 3 states, and we can have combinations of some of them:
        #   - NoState
        #   - Minimized
        #   - Maximized
        #   - Minimized + Maximized (treat as Minimized).
        state = self.windowState()
        if state & compat.WindowMinimized:
            self._titlebar.minimize()
        elif state & compat.WindowMaximized:
            self._titlebar.maximize()
        else:
            self._titlebar.restore()

def main():
    'Application entry point'

    window_class = FramelessWindow
    # Wayland does not allow windows to reposition themselves: therefore,
    # we cannot use the custom titlebar at the application level.
    if args.default_window_frame or USE_WAYLAND_FRAME:
        window_class = DefaultWindow
    app, window = shared.setup_app(args, unknown, compat, window_class=window_class)
    app.installEventFilter(window)

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
