#!/usr/bin/env python
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

import sys

import titlebar

# Add a warning if we're using Wayland with a custom titlebar.
if not titlebar.args.default_window_frame and titlebar.USE_WAYLAND_FRAME:
    print('WARNING: Wayland does not support custom title bars.', file=sys.stderr)
    print('Applications in Wayland cannot set their own position.', file=sys.stderr)
    print('Defaulting to the system title bar instead.', file=sys.stderr)


class DefaultWindow(titlebar.Window):
    '''Default main window with a window frame.'''

    def __init__(self, parent=None, flags=titlebar.QtCore.Qt.WindowType(0)):
        if titlebar.args.window_help:
            flags |= titlebar.compat.WindowContextHelpButtonHint
        if titlebar.args.window_shade:
            flags |= titlebar.compat.WindowShadeButtonHint
        super().__init__(parent, flags)

        self._central = titlebar.QtWidgets.QFrame(self)
        self._layout = titlebar.QtWidgets.QVBoxLayout(self._central)
        self.setCentralWidget(self._central)
        self._widget = titlebar.QtWidgets.QWidget(self._central)
        self._widget.setLayout(titlebar.QtWidgets.QVBoxLayout())
        self._central.layout().addWidget(self._widget, 10)

        if titlebar.args.status_bar:
            self._statusbar = titlebar.QtWidgets.QStatusBar(self._central)
            self.setStatusBar(self._statusbar)

        self.setup()


def main():
    'Application entry point'

    window_class = titlebar.FramelessWindow
    # Wayland does not allow windows to reposition themselves: therefore,
    # we cannot use the custom titlebar at the application level.
    if titlebar.args.default_window_frame or titlebar.USE_WAYLAND_FRAME:
        window_class = DefaultWindow
    app, window = titlebar.shared.setup_app(
        titlebar.args, titlebar.unknown, titlebar.compat, window_class=window_class
    )
    app.installEventFilter(window)

    titlebar.shared.set_stylesheet(titlebar.args, app, titlebar.compat)
    return titlebar.shared.exec_app(titlebar.args, app, window)


if __name__ == '__main__':
    sys.exit(main())
