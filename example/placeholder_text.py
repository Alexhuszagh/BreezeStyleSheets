#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) <2013-2014> <Colin Duquesnoy>
# Modified by Alex Huszagh
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
    placeholder_text
    ================

    Example showing how to style the placeholder text for QLineEdit,
    QTextEdit, and QPlainTextEdit, since in Qt6 is can be styled as
    the default text color. This seems to be an issue with palettes for
    Qt6 in `QPalette::PlaceholderText`, since both the stylesheets
    and palette edits correctly affect styles in Qt5, but not Qt6.
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
parser.add_argument(
    '--set-palette',
    help='''set the placeholder text palette.''',
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
    PlaceholderText = QtGui.QPalette.ColorRole.PlaceholderText
    WindowText = QtGui.QPalette.ColorRole.WindowText
else:
    AlignHCenter = QtCore.Qt.AlignHCenter
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    PlaceholderText = QtGui.QPalette.PlaceholderText
    WindowText = QtGui.QPalette.WindowText

PLACEHOLDER = QtGui.QColor(78, 79, 79, 100)

def set_palette(widget, role, color):
    '''Set the palette for the placeholder text. This only works in Qt5.'''

    palette = widget.palette();
    palette.setColor(role, color)
    widget.setPalette(palette);

def set_placeholder_palette(widget):
    set_palette(widget, PlaceholderText, PLACEHOLDER)


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

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName('textEdit')
        self.textEdit.setPlaceholderText('Placeholder Text')
        self.layout.addWidget(self.textEdit)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName('plainTextEdit')
        self.plainTextEdit.setPlaceholderText('Placeholder Text')
        self.layout.addWidget(self.plainTextEdit)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName('lineEdit')
        self.lineEdit.setPlaceholderText('Placeholder Text')
        self.layout.addWidget(self.lineEdit)

        # Set the palettes.
        if args.set_palette:
            set_placeholder_palette(self.textEdit)
            set_placeholder_palette(self.plainTextEdit)
            set_placeholder_palette(self.lineEdit)

    def style_text(self, widget, text):
        if text:
            set_text_palette(widget)
        else:
            set_notext_palette(widget)


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
    window.setWindowTitle('Stylized Placeholder Text.')

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
