#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) <2021> <Alex Huszagh>
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

import argparse
import os
import sys

example_dir = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(example_dir)

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
    '--use-internal',
    help='''use the dock manager internal stylesheet.''',
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
    QtCore.QDir.addSearchPath(args.stylesheet, f'{home}/pyqt6/{args.stylesheet}/')
    stylesheet = f'{args.stylesheet}:stylesheet.qss'
else:
    sys.path.insert(0, home)
    from PyQt5 import QtCore, QtGui, QtWidgets
    import breeze_resources
    stylesheet = f':/{args.stylesheet}/stylesheet.qss'

from PyQtAds import QtAds

# Compat definitions, between Qt5 and Qt6.
if args.pyqt6:
    AlignTop = QtCore.Qt.AlignmentFlag.AlignTop
    AlignLeft = QtCore.Qt.AlignmentFlag.AlignLeft
    ReadOnly = QtCore.QFile.OpenModeFlag.ReadOnly
    Text = QtCore.QFile.OpenModeFlag.Text
    WindowMaximized = QtCore.Qt.WindowState.WindowMaximized
else:
    AlignTop = QtCore.Qt.AlignTop
    AlignLeft = QtCore.Qt.AlignLeft
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    WindowMaximized = QtCore.Qt.WindowMaximized

# Need to fix an issue on Wayland on Linux:
#   conda-forge does not support Wayland, for who knows what reason.
if sys.platform.lower().startswith('linux') and 'CONDA_PREFIX' in os.environ:
    args.use_x11 = True

if args.use_x11:
    os.environ['XDG_SESSION_TYPE'] = 'x11'

def main():
    'Application entry point'

    if args.scale != 1:
        os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    else:
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    if args.style != 'native':
        style = QtWidgets.QStyleFactory.create(args.style)
        QtWidgets.QApplication.setStyle(style)

    app = QtWidgets.QApplication(sys.argv[:1] + unknown)
    window = QtWidgets.QMainWindow()

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

    # setup the dock manager
    window.setObjectName('MainWindow')
    window.resize(1068, 824)
    widget = QtWidgets.QWidget(window)
    window.setCentralWidget(widget)
    dock_manager = QtAds.CDockManager(window)

    # add widgets to the dock manager
    label_widget = QtAds.CDockWidget('Dock')
    label = QtWidgets.QLabel('Some label')
    label_widget.setWidget(label)
    dock_area = dock_manager.setCentralWidget(label_widget)
    dock_area.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

    list_widget = QtAds.CDockWidget('List')
    lst = QtWidgets.QListWidget()
    for index in range(10):
        lst.addItem(QtWidgets.QListWidgetItem(f'Item {index + 1}'))
    list_widget.setWidget(lst)
    list_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
    dock_manager.addDockWidget(QtAds.DockWidgetArea.LeftDockWidgetArea, list_widget, dock_area)

    table_widget = QtAds.CDockWidget('Table')
    table = QtWidgets.QTableWidget()
    # make sure we have both scroll areas active.
    table.setColumnCount(40)
    table.setRowCount(40)
    table_widget.setWidget(table)
    table_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
    dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, table_widget, dock_area)

    if not args.use_internal:
        dock_manager.setStyleSheet('')

    # run
    window.setWindowState(WindowMaximized)
    window.show()
    if args.pyqt6:
        return app.exec()
    else:
        return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
