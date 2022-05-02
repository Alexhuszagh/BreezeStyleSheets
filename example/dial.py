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
    dial
    ====

    Example showing how to override the `paintEvent` and `eventFilter`
    for a `QDial`, creating a visually consistent, stylish `QDial` that
    supports highlighting the handle on the active or hovered dial.
'''

import argparse
import math
import os
import sys

example_dir = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(example_dir)
dist = os.path.join(home, 'dist')

# Create our arguments.
parser = argparse.ArgumentParser(description='Configurations for the Qt5 application.')
parser.add_argument(
    '--stylesheet',
    help='''stylesheet name''',
    default='native'
)
# Know working styles include:
#   1. Fusion
#   2. Windows
parser.add_argument(
    '--style',
    help='''application style, which is different than the stylesheet''',
    default='native'
)
parser.add_argument(
    '--font-size',
    help='''font size for the application''',
    type=float,
    default=-1
)
parser.add_argument(
    '--font-family',
    help='''the font family'''
)
parser.add_argument(
    '--scale',
    help='''scale factor for the UI''',
    type=float,
    default=1,
)
parser.add_argument(
    '--pyqt6',
    help='''use PyQt6 rather than PyQt5.''',
    action='store_true'
)
parser.add_argument(
    '--use-x11',
    help='''force the use of x11 on compatible systems.''',
    action='store_true'
)
parser.add_argument(
    '--no-align',
    help='''allow larger widgets without forcing alignment.''',
    action='store_true'
)

args, unknown = parser.parse_known_args()
if args.pyqt6:
    from PyQt6 import QtCore, QtGui, QtWidgets
    QtCore.QDir.addSearchPath(args.stylesheet, f'{dist}/pyqt6/{args.stylesheet}/')
    resource_format = f'{args.stylesheet}:'
else:
    sys.path.insert(0, home)
    from PyQt5 import QtCore, QtGui, QtWidgets
    import breeze_resources
    resource_format = f':/{args.stylesheet}/'
stylesheet = f'{resource_format}stylesheet.qss'

# Compat definitions, between Qt5 and Qt6.
if args.pyqt6:
    AlignHCenter = QtCore.Qt.AlignmentFlag.AlignHCenter
    ReadOnly = QtCore.QFile.OpenModeFlag.ReadOnly
    Text = QtCore.QFile.OpenModeFlag.Text
    SolidLine = QtCore.Qt.PenStyle.SolidLine
    FlatCap = QtCore.Qt.PenCapStyle.FlatCap
    SquareCap = QtCore.Qt.PenCapStyle.SquareCap
    RoundCap = QtCore.Qt.PenCapStyle.RoundCap
    MiterJoin = QtCore.Qt.PenJoinStyle.MiterJoin
    BevelJoin = QtCore.Qt.PenJoinStyle.BevelJoin
    RoundJoin = QtCore.Qt.PenJoinStyle.RoundJoin
    SvgMiterJoin = QtCore.Qt.PenJoinStyle.SvgMiterJoin
    State_HasFocus = QtWidgets.QStyle.StateFlag.State_HasFocus
    State_Selected = QtWidgets.QStyle.StateFlag.State_Selected
    HoverEnter = QtCore.QEvent.Type.HoverEnter
    HoverMove = QtCore.QEvent.Type.HoverMove
    HoverLeave = QtCore.QEvent.Type.HoverLeave
else:
    AlignHCenter = QtCore.Qt.AlignHCenter
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    SolidLine = QtCore.Qt.SolidLine
    FlatCap = QtCore.Qt.FlatCap
    SquareCap = QtCore.Qt.SquareCap
    RoundCap = QtCore.Qt.RoundCap
    MiterJoin = QtCore.Qt.MiterJoin
    BevelJoin = QtCore.Qt.BevelJoin
    RoundJoin = QtCore.Qt.RoundJoin
    SvgMiterJoin = QtCore.Qt.SvgMiterJoin
    State_HasFocus = QtWidgets.QStyle.State_HasFocus
    State_Selected = QtWidgets.QStyle.State_Selected
    HoverEnter = QtCore.QEvent.HoverEnter
    HoverMove = QtCore.QEvent.HoverMove
    HoverLeave = QtCore.QEvent.HoverLeave

SELECTED = QtGui.QColor(61, 174, 233)
if 'dark' in args.stylesheet:
    GROOVE_BACKGROUND = QtGui.QColor(98, 101, 104)
    GROOVE_BORDER = QtGui.QColor(49, 54, 59)
    HANDLE_BACKGROUND = QtGui.QColor(29, 32, 35)
    HANDLE_BORDER = QtGui.QColor(98, 101, 104)
    NOTCH = QtGui.QColor(51, 78, 94)
elif 'light' in args.stylesheet:
    GROOVE_BACKGROUND = QtGui.QColor(106, 105, 105, 179)
    GROOVE_BORDER = QtGui.QColor(239, 240, 241)
    HANDLE_BACKGROUND = QtGui.QColor(239, 240, 241)
    HANDLE_BORDER = QtGui.QColor(106, 105, 105, 179)
    NOTCH = QtGui.QColor(61, 173, 232, 51)


def radius(dial):
    '''Get the radius of the dial.'''
    return min(dial.rect.width(), dial.rect.height()) // 2

def groove_rect(dial):
    '''Calculate the bounding rectangle for the dial groove.'''

    x0 = dial.rect.width() / 2
    y0 = dial.rect.height() / 2
    pos = dial.rect.topLeft()

    return pos.x() + x0, pos.y() + y0

def circle_percent(dial):
    '''Calculate the percentage of the dial.'''

    distance = dial.maximum - dial.minimum
    offset = dial.sliderPosition - dial.minimum

    return offset / distance

def circle_position(dial, groove_rect, position, r):
    '''Calculate the (x, y) coordinates based on the position on a circle.'''

    # Get our center and the percent we've gone alone the dial.
    center = groove_rect.center()
    x0 = center.x()
    y0 = center.y()
    distance = dial.maximum - dial.minimum
    offset = position - dial.minimum
    percent = offset / distance

    # The position of points on a circle follows. The start angle is
    # at the left (0°), and we start from the bottom. The formula
    # to get the position on a circle is:
    #   (x0 + r cos theta, y0 + r sin theta)
    #
    # However, our y point is inverted (goes from the top), so we modify it to:
    #   (x0 + r cos theta, y0 - r sin theta)
    initial = 60
    total_angle = 300
    if dial.dialWrapping:
        initial = 90
        total_angle = 360
    angle = total_angle * percent
    theta = (angle - initial) * math.pi / 180

    return x0 - r * math.cos(theta), y0 - r * math.sin(theta)

def handle_position(dial, groove_rect, r):
    '''Calculate the position of the handle.'''
    return circle_position(dial, groove_rect, dial.sliderPosition, r)

def default_pen(color, width):
    '''Create a pen with the default styles.'''
    return QtGui.QPen(color, width)

def round_pen(color, width):
    '''Create a pen with round join styles.'''
    return QtGui.QPen(color, width, SolidLine, RoundCap, RoundJoin)

def event_pos(event):
    '''Determine the event position.'''

    if args.pyqt6:
        return event.position()
    return event.posF()


class Dial(QtWidgets.QDial):
    '''QDial with a custom paint event.'''

    def __init__(self, widget=None):
        super().__init__(widget)
        if args.stylesheet == 'native':
            return

        self.installEventFilter(self)

        # Set some configuration settings, since we'll need them later.
        # No reason to recalculate them every time.
        self.font_size = self.font().pointSizeF()
        self.bd_width = 0.09 * self.font_size
        self.groove_width = 5
        self.handle_radius = self.groove_width + 3
        self.notch_start = self.groove_width + 2
        self.notch_end = self.notch_start + 2
        self.notch_width = 2
        self.groove_bd_color = GROOVE_BORDER
        self.groove_bg_color = GROOVE_BACKGROUND
        self.handle_bg_color = HANDLE_BACKGROUND
        self.handle_bd_color = HANDLE_BORDER
        self.notch_color = NOTCH
        self.selected_color = SELECTED

        # Store some state changes.
        self.groove = (0, 0)
        self.handle = (0, 0)
        self.is_hovered = False

    def paintEvent(self, event):
        '''Override the paint event to ensure the ticks are painted.'''

        if args.stylesheet == 'native':
            return super().paintEvent(event)

        painter = QtWidgets.QStylePainter(self)
        options = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(options)

        # Get our item colors. Override the color when selected/active.
        handle_bd_color = self.handle_bd_color
        mask = State_HasFocus | State_Selected
        # WindowActive
        if options.state & mask or self.is_hovered:
            handle_bd_color = self.selected_color

        # Get the groove settings: this defines the bounding rect
        # and the start and stop angles for the groove. We also
        # make the radius 20% smaller, so it fits nicely within
        # the bounding rect.
        groove_width = self.groove_width * painter.pen().widthF()
        r = radius(options) - 2 * groove_width
        gx, gy = groove_rect(options)
        self.groove = (gx, gy)
        rect = QtCore.QRectF(gx - r, gy - r, 2 * r, 2 * r)
        # The arc should be everything besides ~30° at the bottom.
        # Units are measured in 1/16th of a degree.
        start_angle = 240 * 16
        span_angle = -300 * 16
        if options.dialWrapping:
            # Have a wrapping dial: have the full circle.
            start_angle = 270 * 16
            span_angle = -360 * 16

        # Get the handle settings.
        hx, hy = handle_position(options, rect, r)
        self.handle = (hx, hy)

        # First, we draw the border for the slider.
        # This is simple, since we just add `0.09em` to the actual groove
        # width and draw it first.
        groove_bd_width = groove_width + self.bd_width
        painter.setPen(round_pen(self.groove_bd_color, groove_bd_width))
        painter.drawArc(rect, start_angle, span_angle)

        # Draw the groove for the slider. We want to stroke the groove so
        # it's quite large, and then we can create a border, etc. for it.
        groove_percent = circle_percent(options)
        groove_stop = int(groove_percent * span_angle)
        painter.setPen(round_pen(self.groove_bg_color, groove_width))
        painter.drawArc(rect, start_angle, span_angle)
        painter.setPen(round_pen(self.selected_color, groove_width))
        painter.drawArc(rect, start_angle, groove_stop)

        # Now, we need to draw the notches. We need to draw these before
        # the handle, since the handle needs to be above the notches.
        notch_step = self.notchSize() * self.singleStep()
        painter.setPen(default_pen(self.notch_color, self.notch_width))
        notch_start = r + self.notch_start
        notch_end = r + self.notch_end
        if self.notchesVisible() and notch_step != 0:
            distance = options.maximum - options.minimum
            position = 0
            # Need an inclusive range: by default dial range is 0-99, but
            # range(0, 100) is 0-99, and we need 0-100. Specially draw
            # the first and the last items.
            positions = list(range(0, distance, notch_step)) + [options.maximum]
            for position in positions:
                nx0, ny0 = circle_position(options, rect, position, notch_start)
                nx1, ny1 = circle_position(options, rect, position, notch_end)
                painter.drawLine(int(nx0), int(ny0), int(nx1), int(ny1))

        # Now, we need to draw the handle. First, we need to get the position
        # of the slider, based on the position and angle it's at.
        painter.setPen(default_pen(handle_bd_color, self.bd_width))
        painter.setBrush(QtGui.QBrush(self.handle_bg_color))
        handle_pos = QtCore.QPointF(hx, hy)
        painter.drawEllipse(handle_pos, self.handle_radius, self.handle_radius)

    def eventFilter(self, obj, event):
        '''Override the color when we have a hover event.'''

        # If the window isn't active, ignore the hover event.
        if not self.window().isActiveWindow():
            self.is_hovered = False
            return super().eventFilter(obj, event)

        # Determine if we have a hover event, and if the handle
        # is hovered or no longer hovered, change the hover state
        # and trigger a paint event. We need to trigger an immediate
        # paint event, since otherwise we might have a delay in UI change.
        #
        # We use a very mild hack: we merely calculate the bounding rect
        # for the handle, and determine if the mouse is contained in there,
        # rather than calculate if it's actually in the circle. This won't
        # matter except if the dial is scaled by a large amount.
        if event.type() == HoverEnter or event.type() == HoverMove:
            x0 = self.handle[0] - self.handle_radius
            y0 = self.handle[1] - self.handle_radius
            size = 2 * self.handle_radius
            rect = QtCore.QRectF(x0, y0, size, size)
            self.is_hovered = rect.contains(event_pos(event))
            self.repaint()
        elif event.type() == HoverLeave:
            self.is_hovered = False
            self.repaint()

        return super().eventFilter(obj, event)


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        if not args.no_align:
            self.layout.setAlignment(AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.dial1 = Dial(self.centralwidget)
        self.layout.addWidget(self.dial1)

        self.dial2 = Dial(self.centralwidget)
        self.dial2.setNotchesVisible(True)
        self.layout.addWidget(self.dial2)

        self.dial3 = Dial(self.centralwidget)
        self.dial3.setWrapping(True)
        self.layout.addWidget(self.dial3)


def main():
    'Application entry point'

    if args.scale != 1:
        os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    else:
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

    app = QtWidgets.QApplication(sys.argv[:1] + unknown)
    if args.style != 'native':
        style = QtWidgets.QStyleFactory.create(args.style)
        app.setStyle(style)

    window = QtWidgets.QMainWindow()

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('QDial')

    # use the default font size
    font = app.font()
    if args.font_size > 0:
        font.setPointSizeF(args.font_size)
    if args.font_family:
        font.setFamily(args.font_family)
    app.setFont(font)

    # setup stylesheet
    if args.stylesheet != 'native':
        file = QtCore.QFile(stylesheet)
        file.open(ReadOnly | Text)
        stream = QtCore.QTextStream(file)
        app.setStyleSheet(stream.readAll())

    # run
    window.show()
    if args.pyqt6:
        return app.exec()
    else:
        return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
