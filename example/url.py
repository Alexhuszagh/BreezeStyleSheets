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
    url
    ===

    Example showing how to style URLs, since the color of the links
    cannot be modified in stylesheets.
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

def set_link_palette(widget):
    set_palette(widget, compat.Link, colors.LinkColor)
    set_palette(widget, compat.LinkVisited, colors.LinkVisitedColor)


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        url = 'https://github.com/Alexhuszagh/BreezeStyleSheets'
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(400, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        self.layout.setAlignment(compat.AlignLeft)
        MainWindow.setCentralWidget(self.centralwidget)

        self.repository = QtWidgets.QLabel(self.centralwidget)
        self.repository.setObjectName('repository')
        self.repository.setText(f'[BreezeStyleSheets]({url})')
        self.repository.setTextFormat(compat.MarkdownText)
        self.repository.setTextInteractionFlags(compat.TextBrowserInteraction)
        self.repository.setOpenExternalLinks(True)
        self.layout.addWidget(self.repository)

        self.issues = QtWidgets.QLabel(self.centralwidget)
        self.issues.setObjectName('issues')
        self.issues.setText(f'[Issues]({url}/issues)')
        self.issues.setTextFormat(compat.MarkdownText)
        self.issues.setTextInteractionFlags(compat.TextBrowserInteraction)
        self.issues.setOpenExternalLinks(True)
        self.layout.addWidget(self.issues)

        self.pulls = QtWidgets.QLabel(self.centralwidget)
        self.pulls.setObjectName('pulls')
        self.pulls.setText(f'[Pull Requests]({url}/pulls)')
        self.pulls.setTextFormat(compat.MarkdownText)
        self.pulls.setTextInteractionFlags(compat.TextBrowserInteraction)
        self.pulls.setOpenExternalLinks(True)
        self.layout.addWidget(self.pulls)

        # Set the palettes.
        if args.set_widget_palette:
            set_link_palette(self.repository)
            set_link_palette(self.issues)
            set_link_palette(self.pulls)

def main():
    'Application entry point'

    app, window = shared.setup_app(args, unknown, compat)
    if args.set_app_palette:
        set_link_palette(app)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('Stylized URL colors.')

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
