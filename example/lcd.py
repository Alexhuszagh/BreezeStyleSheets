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

import math
import shared
import sys

parser = shared.create_parser()
parser.add_argument(
    '--no-align',
    help='''allow larger widgets without forcing alignment.''',
    action='store_true'
)
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)

class LCD(QtWidgets.QLCDNumber):
    '''QLCDNumber with a custom palette.'''

    def __init__(self, widget=None):
        super().__init__(widget)
        self.setContentsMargins(1, 1, 1, 1)
        if args.stylesheet == 'native':
            return

        # The color of the non-flat LCD numbers is still controlled
        # via the `color` stylesheet attribute.
        r, g, b, a = colors.HighLightDark.getRgb()
        color = (r, g, b, a / 255)
        self.setStyleSheet(f'QLCDNumber {{ color: rgba{color}; }}')

        palette = self.palette()
        palette.setColor(compat.WindowPalette, colors.Background)
        palette.setColor(compat.LightPalette, colors.Selected)
        palette.setColor(compat.DarkPalette, colors.Notch)
        self.setPalette(palette)

class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.layout.setSpacing(0)
        if not args.no_align:
            self.layout.setAlignment(compat.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.lcd1 = LCD(self.centralwidget)
        self.lcd1.display(15)
        self.lcd1.setDigitCount(2)
        self.layout.addWidget(self.lcd1)

        self.lcd2 = LCD(self.centralwidget)
        self.lcd2.display(31)
        self.lcd2.setHexMode()
        self.lcd2.setDigitCount(2)
        self.layout.addWidget(self.lcd2)

        self.lcd3 = LCD(self.centralwidget)
        self.lcd3.display(15)
        self.lcd3.setSegmentStyle(compat.LCDOutline)
        self.lcd3.setFrameShape(compat.NoFrame)
        self.lcd3.setDigitCount(2)
        self.layout.addWidget(self.lcd3)

        self.lcd4 = LCD(self.centralwidget)
        self.lcd4.display(15)
        self.lcd4.setSegmentStyle(compat.LCDFlat)
        self.lcd4.setFrameShape(compat.NoFrame)
        self.lcd4.setDigitCount(2)
        self.layout.addWidget(self.lcd4)


def main():
    'Application entry point'

    app, window = shared.setup_app(args, unknown, compat)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('QLCDNumber')

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
