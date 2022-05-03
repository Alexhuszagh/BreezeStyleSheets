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
    placeholder_text
    ================

    Example showing how to style the placeholder text for QLineEdit,
    QTextEdit, and QPlainTextEdit, since in Qt6 is can be styled as
    the default text color. This seems to be an issue with palettes for
    Qt6 in `QPalette::PlaceholderText`, since both the stylesheets
    and palette edits correctly affect styles in Qt5, but not Qt6.
'''

import shared
import sys

parser = shared.create_parser()
parser.add_argument(
    '--set-app-palette',
    help='''set the placeholder text palette globally.''',
    action='store_true'
)
parser.add_argument(
    '--set-widget-palette',
    help='''set the placeholder text palette for the affected widgets.''',
    action='store_true'
)
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)


def set_palette(widget, role, color):
    '''Set the palette for the placeholder text. This only works in Qt5.'''

    palette = widget.palette()
    palette.setColor(role, color)
    widget.setPalette(palette)

def set_placeholder_palette(widget):
    set_palette(widget, compat.PlaceholderText, colors.PlaceholderColor)


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        self.layout.setAlignment(compat.AlignHCenter)
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
        if args.set_widget_palette:
            set_placeholder_palette(self.textEdit)
            set_placeholder_palette(self.plainTextEdit)
            set_placeholder_palette(self.lineEdit)

def main():
    'Application entry point'

    app, window = shared.setup_app(args, unknown, compat)
    if args.set_app_palette:
        set_placeholder_palette(app)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('Stylized Placeholder Text.')

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
