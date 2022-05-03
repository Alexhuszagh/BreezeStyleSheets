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
    whatsthis
    =========

    Example showing how to style the tooltip base and text for QWhatsThis,
    since it cannot be modified via stylesheets.
'''

import shared
import sys

parser = shared.create_parser()
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)


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

        self.toolbar = QtWidgets.QToolBar('Toolbar')
        self.toolbar.setOrientation(compat.Vertical)
        self.action = compat.QAction('&Action 1', MainWindow)
        self.action.setWhatsThis('Example action')
        self.toolbar.addAction(self.action)
        self.toolbar.addAction(QtWidgets.QWhatsThis.createAction(self.toolbar))
        MainWindow.addToolBar(compat.TopToolBarArea, self.toolbar)


def main():
    'Application entry point'

    app, window = shared.setup_app(args, unknown, compat)

    palette = app.palette()
    palette.setColor(compat.ToolTipBase, colors.ToolTipBase)
    palette.setColor(compat.ToolTipText, colors.ToolTipText)
    app.setPalette(palette)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('Stylized QWhatsThis.')

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
