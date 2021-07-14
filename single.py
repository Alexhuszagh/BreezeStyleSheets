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
    single
    ======

    Test styles of a single widget.
'''

import argparse
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import breeze_resources

# Create our arguments.
parser = argparse.ArgumentParser(description='Configurations for the Qt5 application.')
parser.add_argument(
    '--widget',
    help='''widget to test'''
)
parser.add_argument(
    '--stylesheet',
    help='''stylesheet name''',
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
    '--width',
    help='''the window width''',
    type=int,
    default=1068,
)
parser.add_argument(
    '--height',
    help='''the window height''',
    type=int,
    default=824,
)
parser.add_argument(
    '--alignment',
    help='''the layout alignment''',
)
parser.add_argument(
    '--compress',
    help='''add stretch on both sides''',
    action='store_true',
)

layout = {
    'vertical': QtWidgets.QVBoxLayout,
    'horizontal': QtWidgets.QHBoxLayout,
}

alignment = {
    'top': QtCore.Qt.AlignTop,
    'vcenter': QtCore.Qt.AlignVCenter,
    'bottom': QtCore.Qt.AlignBottom,
    'left': QtCore.Qt.AlignLeft,
    'hcenter': QtCore.Qt.AlignHCenter,
    'right': QtCore.Qt.AlignRight,
    'center': QtCore.Qt.AlignCenter,
}

def add_widgets(layout, children):
    '''Add 1 or more widgets to the layout.'''

    if isinstance(children, list):
        for child in children:
            layout.addWidget(child)
    else:
        layout.addWidget(children)

def abstract_button(
    cls,
    parent=None,
    exlusive=False,
    checked=False,
    enabled=True,
):
    '''Helper to simplify creating abstract buttons.'''

    inst = cls(parent)
    inst.setAutoExclusive(exlusive)
    if isinstance(checked, bool):
        inst.setChecked(checked)
    else:
        inst.setTristate(True)
        inst.setCheckState(checked)
    inst.setEnabled(enabled)
    return inst

def main(argv=None):
    'Application entry point'

    args, unknown = parser.parse_known_args(argv)
    app = QtWidgets.QApplication(argv[:1] + unknown)
    window = QtWidgets.QMainWindow()
    window.setWindowTitle('Sample single widget application.')
    window.resize(args.width, args.height)
    widget = QtWidgets.QWidget(window)

    # setup stylesheet
    if args.stylesheet != 'native':
        file = QtCore.QFile(f':/{args.stylesheet}.qss')
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(file)
        app.setStyleSheet(stream.readAll())

    # use the default font size
    font = app.font()
    if args.font_size > 0:
        font.setPointSizeF(args.font_size)
    if args.font_family:
        font.setFamily(args.font_family)
    app.setFont(font)

    # Load the correct widget.
    layout_type = 'vertical'
    if args.widget == 'progress_bar_horizontal':
        child = QtWidgets.QProgressBar(widget)
        child.setProperty('value', 24)
    elif args.widget == 'progress_bar_vertical':
        layout_type = 'horizontal'
        child = QtWidgets.QProgressBar(widget)
        child.setOrientation(QtCore.Qt.Vertical)
        child.setProperty('value', 24)
    if args.widget == 'slider_horizontal':
        child = QtWidgets.QSlider(widget)
        child.setOrientation(QtCore.Qt.Horizontal)
    elif args.widget == 'slider_vertical':
        layout_type = 'horizontal'
        child = QtWidgets.QSlider(widget)
        child.setOrientation(QtCore.Qt.Vertical)
    #if args.widget == 'splitter_horizontal':
    #    layout_type = 'vertical'
    #    child = QtWidgets.QSplitter(widget)
    #elif args.widget == 'splitter_vertical':
    #    layout_type = 'horizontal'
    #    child = QtWidgets.QSplitter(widget)
    #    child.setOrientation(QtCore.Qt.Vertical)
    elif args.widget == 'menu':
        child = QtWidgets.QMenuBar(window)
        child.setGeometry(QtCore.QRect(0, 0, args.width, int(1.5 * font.pointSize())))
        menu = QtWidgets.QMenu('Main Menu', child)
        menu.addAction(QtWidgets.QAction('&Action 1', window))
        menu.addAction(QtWidgets.QAction('&Action 2', window))
        submenu = QtWidgets.QMenu('Sub Menu', menu)
        submenu.addAction(QtWidgets.QAction('&Action 3', window))
        menu.addAction(submenu.menuAction())
        child.addAction(menu.menuAction())
        window.setMenuBar(child)
    elif args.widget == 'status_bar':
        child = QtWidgets.QStatusBar(window)
        window.setStatusBar(child)
    elif args.widget == 'spinbox':
        layout_type = 'horizontal'
        child = QtWidgets.QSpinBox(window)
        child.setValue(10);
    elif args.widget == 'double_spinbox':
        layout_type = 'horizontal'
        child = QtWidgets.QDoubleSpinBox(window)
        child.setValue(10.5);
    elif args.widget == 'combobox':
        layout_type = 'horizontal'
        child = QtWidgets.QComboBox(widget)
        child.addItem('Item 1')
        child.addItem('Item 2')
    elif args.widget == 'tab_widget':
        child = QtWidgets.QTabWidget(widget)
        child.addTab(QtWidgets.QWidget(), 'Tab 1')
        child.addTab(QtWidgets.QWidget(), 'Tab 2')
        child.addTab(QtWidgets.QWidget(), 'Tab 3')
    elif args.widget == 'closable_tab_widget':
        child = QtWidgets.QTabWidget(widget)
        child.setTabPosition(QtWidgets.QTabWidget.East)
        child.setTabsClosable(True)
        child.addTab(QtWidgets.QWidget(), 'Tab 1')
        child.addTab(QtWidgets.QWidget(), 'Tab 2')
        child.addTab(QtWidgets.QWidget(), 'Tab 3')
    elif args.widget == 'dock':
        child = [
            QtWidgets.QDockWidget(window),
            QtWidgets.QDockWidget(window),
        ]
    elif args.widget == 'radio':
        child = []
        child.append(abstract_button(QtWidgets.QRadioButton, widget))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, checked=True))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, enabled=False))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, checked=True, enabled=False))
    elif args.widget == 'checkbox':
        child = []
        child.append(abstract_button(QtWidgets.QCheckBox, widget))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=True))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=QtCore.Qt.PartiallyChecked))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, enabled=False))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=True, enabled=False))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=QtCore.Qt.PartiallyChecked, enabled=False))
    elif args.widget == 'menu_checkbox':
        child = QtWidgets.QMenuBar(window)
        child.setGeometry(QtCore.QRect(0, 0, args.width, int(1.5 * font.pointSize())))
        menu = QtWidgets.QMenu('Main Menu', child)
        action1 = QtWidgets.QAction('&Action 1', window)
        action1.setCheckable(True)
        menu.addAction(action1)
        action2 = QtWidgets.QAction('&Action 2', window)
        action2.setCheckable(True)
        action2.setChecked(True)
        menu.addAction(action2)
        submenu = QtWidgets.QMenu('Sub Menu', menu)
        action3 = QtWidgets.QAction('&Action 3', window)
        action3.setCheckable(True)
        submenu.addAction(action3)
        menu.addAction(submenu.menuAction())
        child.addAction(menu.menuAction())
        window.setMenuBar(child)

    widget_layout = layout[layout_type](widget)
    if args.compress:
        widget_layout.addStretch(1)
        add_widgets(widget_layout, child)
        widget_layout.addStretch(1)
    else:
        add_widgets(widget_layout, child)
    if args.alignment is not None:
        widget_layout.setAlignment(alignment[args.alignment])
    window.setCentralWidget(widget)

    # run
    window.show()
    app.exec_()

if __name__ == '__main__':
    main(sys.argv)
