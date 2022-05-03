#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) <2021-Present> <Alex Huszagh>
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
    advanced-dock
    =============

    Simple PyQt application using the advanced-docking-system.
'''

import shared
import sys

parser = shared.create_parser()
parser.add_argument(
    '--use-internal',
    help='''use the dock manager internal stylesheet.''',
    action='store_true'
)
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)

from PyQtAds import QtAds


def main():
    'Application entry point'

    app, window = shared.setup_app(args, unknown, compat)

    # setup the dock manager
    window.setObjectName('MainWindow')
    window.resize(1068, 824)
    widget = QtWidgets.QWidget(window)
    window.setCentralWidget(widget)
    dock_manager = QtAds.CDockManager(window)

    DockArea = QtAds.DockWidgetArea

    # add widgets to the dock manager
    label_widget = QtAds.CDockWidget('Dock')
    label = QtWidgets.QLabel('Some label')
    label_widget.setWidget(label)
    dock_area = dock_manager.setCentralWidget(label_widget)
    dock_area.setAllowedAreas(DockArea.OuterDockAreas)

    list_widget = QtAds.CDockWidget('List')
    lst = QtWidgets.QListWidget()
    for index in range(10):
        lst.addItem(QtWidgets.QListWidgetItem(f'Item {index + 1}'))
    list_widget.setWidget(lst)
    list_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
    dock_manager.addDockWidget(DockArea.LeftDockWidgetArea, list_widget, dock_area)

    table_widget = QtAds.CDockWidget('Table')
    table = QtWidgets.QTableWidget()
    # make sure we have both scroll areas active.
    table.setColumnCount(40)
    table.setRowCount(40)
    table_widget.setWidget(table)
    table_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
    dock_manager.addDockWidget(DockArea.RightDockWidgetArea, table_widget, dock_area)

    if not args.use_internal:
        dock_manager.setStyleSheet('')

    # run
    window.setWindowState(compat.WindowMaximized)
    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
