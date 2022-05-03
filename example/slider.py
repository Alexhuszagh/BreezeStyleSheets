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
    slider
    ======

    Example showing how to add ticks to a QSlider. Note that this does
    not work with stylesheets, so it's merely an example of how to
    get customized styling behavior with a QSlider.
'''

import argparse
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
    Horizontal = QtCore.Qt.Orientation.Horizontal
    NoTicks = QtWidgets.QSlider.TickPosition.NoTicks
    TicksAbove = QtWidgets.QSlider.TickPosition.TicksAbove
    TicksBelow = QtWidgets.QSlider.TickPosition.TicksBelow
    TicksBothSides = QtWidgets.QSlider.TickPosition.TicksBothSides
    CC_Slider = QtWidgets.QStyle.ComplexControl.CC_Slider
    SC_SliderHandle = QtWidgets.QStyle.SubControl.SC_SliderHandle
    SC_SliderGroove = QtWidgets.QStyle.SubControl.SC_SliderGroove
else:
    AlignHCenter = QtCore.Qt.AlignHCenter
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    Horizontal = QtCore.Qt.Horizontal
    NoTicks = QtWidgets.QSlider.NoTicks
    TicksAbove = QtWidgets.QSlider.TicksAbove
    TicksBelow = QtWidgets.QSlider.TicksBelow
    TicksBothSides = QtWidgets.QSlider.TicksBothSides
    CC_Slider = QtWidgets.QStyle.CC_Slider
    SC_SliderHandle = QtWidgets.QStyle.SC_SliderHandle
    SC_SliderGroove = QtWidgets.QStyle.SC_SliderGroove

TICK_COLOR = QtGui.QColor(255, 0, 0)
if 'dark' in args.stylesheet:
    TICK_COLOR = QtGui.QColor(51, 78, 94)
elif 'light' in args.stylesheet:
    TICK_COLOR = QtGui.QColor(61, 173, 232, 51)


class Slider(QtWidgets.QSlider):
    '''QSlider with a custom paint event.'''

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def paintEvent(self, event):
        '''Override the paint event to ensure the ticks are painted.'''

        painter = QtWidgets.QStylePainter(self)
        options = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(options)

        style = self.style()
        handle = style.subControlRect(CC_Slider, options, SC_SliderHandle, self)

        interval = self.tickInterval() or self.pageStep()
        position = self.tickPosition()
        if position != NoTicks and interval != 0:
            minimum = self.minimum()
            maximum = self.maximum()
            painter.setPen(TICK_COLOR)
            for i in range(minimum, maximum + interval, interval):
                percent = (i - minimum) / (maximum - minimum + 1) + 0.005
                width = (self.width() - handle.width()) + handle.width() / 2
                x = int(percent * width)
                h = 4
                if position == TicksBothSides or position == TicksAbove:
                    y = self.rect().top()
                    painter.drawLine(x, y, x, y + h)
                if position == TicksBothSides or position == TicksBelow:
                    y = self.rect().bottom()
                    painter.drawLine(x, y, x, y - h)

        options.subControls = SC_SliderGroove
        painter.drawComplexControl(CC_Slider, options)

        options.subControls = SC_SliderHandle
        painter.drawComplexControl(CC_Slider, options)


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        self.layout.setAlignment(AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.slider = Slider(self.centralwidget)
        self.slider.setOrientation(Horizontal)
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(TicksAbove)
        self.slider.setObjectName('slider')
        self.layout.addWidget(self.slider)


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
    window.setWindowTitle('QSlider with Ticks.')

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
