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
    test
    ====

    Test styles of a single widget.
'''

import argparse
import os
import random
import sys
import time

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
parser.add_argument(
    '--scale',
    help='''scale factor for the UI''',
    type=float,
    default=1,
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
    *args,
    exlusive=False,
    checked=False,
    checkable=True,
    enabled=True,
):
    '''Helper to simplify creating abstract buttons.'''

    inst = cls(*args, parent)
    inst.setAutoExclusive(exlusive)
    inst.setCheckable(checkable)
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
    os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    if args.style != 'native':
        style = QtWidgets.QStyleFactory.create(args.style)
        QtWidgets.QApplication.setStyle(style)
    app = QtWidgets.QApplication(argv[:1] + unknown)

    # use the default font size
    font = app.font()
    if args.font_size > 0:
        font.setPointSizeF(args.font_size)
    if args.font_family:
        font.setFamily(args.font_family)
    app.setFont(font)

    # setup stylesheet
    if args.stylesheet != 'native':
        file = QtCore.QFile(f':/{args.stylesheet}.qss')
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(file)
        app.setStyleSheet(stream.readAll())

    # Setup the main window.
    window = QtWidgets.QMainWindow()
    window.setWindowTitle('Sample single widget application.')
    window.resize(args.width, args.height)
    widget = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
    scroll.setWidgetResizable(True)

    # Load the correct widget.
    layout_type = 'vertical'
    if args.widget == 'progress_bar_horizontal':
        child = []
        bar1 = QtWidgets.QProgressBar(widget)
        bar1.setProperty('value', 0)
        child.append(bar1)
        bar2 = QtWidgets.QProgressBar(widget)
        bar2.setProperty('value', 24)
        child.append(bar2)
        bar3 = QtWidgets.QProgressBar(widget)
        bar3.setProperty('value', 99)
        child.append(bar3)
        bar4 = QtWidgets.QProgressBar(widget)
        bar4.setProperty('value', 100)
        child.append(bar4)
    elif args.widget == 'progress_bar_vertical':
        layout_type = 'horizontal'
        child = []
        bar1 = QtWidgets.QProgressBar(widget)
        bar1.setOrientation(QtCore.Qt.Vertical)
        bar1.setProperty('value', 0)
        child.append(bar1)
        bar2 = QtWidgets.QProgressBar(widget)
        bar2.setOrientation(QtCore.Qt.Vertical)
        bar2.setProperty('value', 24)
        child.append(bar2)
        bar3 = QtWidgets.QProgressBar(widget)
        bar3.setOrientation(QtCore.Qt.Vertical)
        bar3.setProperty('value', 99)
        child.append(bar3)
        bar4 = QtWidgets.QProgressBar(widget)
        bar4.setOrientation(QtCore.Qt.Vertical)
        bar4.setProperty('value', 100)
        child.append(bar4)
    elif args.widget == 'slider_horizontal':
        child = QtWidgets.QSlider(widget)
        child.setOrientation(QtCore.Qt.Horizontal)
    elif args.widget == 'slider_vertical':
        layout_type = 'horizontal'
        child = QtWidgets.QSlider(widget)
        child.setOrientation(QtCore.Qt.Vertical)
    elif args.widget == 'splitter_horizontal':
        layout_type = 'vertical'
        child = QtWidgets.QSplitter(widget)
        raise NotImplementedError
    elif args.widget == 'splitter_vertical':
        layout_type = 'horizontal'
        child = QtWidgets.QSplitter(widget)
        child.setOrientation(QtCore.Qt.Vertical)
        raise NotImplementedError
    elif args.widget == 'menu':
        child = QtWidgets.QMenuBar(window)
        child.setGeometry(QtCore.QRect(0, 0, args.width, int(1.5 * font.pointSize())))
        menu = QtWidgets.QMenu('Main Menu', child)
        menu.addAction(QtWidgets.QAction('&Action 1', window))
        menu.addAction(QtWidgets.QAction('&Action 2', window))
        submenu = QtWidgets.QMenu('Sub Menu', menu)
        submenu.addAction(QtWidgets.QAction('&Action 3', window))
        action1 = QtWidgets.QAction('&Action 4', window)
        action1.setCheckable(True)
        submenu.addAction(action1)
        menu.addAction(submenu.menuAction())
        action2 = QtWidgets.QAction('&Action 5', window)
        action2.setCheckable(True)
        action2.setChecked(True)
        menu.addSeparator()
        menu.addAction(action2)
        action3 = QtWidgets.QAction('&Action 6', window)
        action3.setCheckable(True)
        menu.addAction(action3)
        icon = QtGui.QIcon(':/dark/close.svg')
        menu.addAction(QtWidgets.QAction(icon, '&Action 7', window))
        menu.addAction(QtWidgets.QAction(icon, '&Action 8', window))
        submenu.addAction(QtWidgets.QAction(icon, '&Action 9', window))
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
        child = []
        combo1 = QtWidgets.QComboBox(widget)
        combo1.addItem('Item 1')
        combo1.addItem('Item 2')
        child.append(combo1)
        combo2 = QtWidgets.QComboBox(widget)
        combo2.addItem('Very Very Long Item 1')
        combo2.addItem('Very Very Long Item 2')
        child.append(combo2)
    elif args.widget == 'tab_widget_top':
        child = QtWidgets.QTabWidget(widget)
        child.setTabPosition(QtWidgets.QTabWidget.North)
        child.addTab(QtWidgets.QWidget(), 'Tab 1')
        child.addTab(QtWidgets.QWidget(), 'Tab 2')
        child.addTab(QtWidgets.QWidget(), 'Tab 3')
    elif args.widget == 'tab_widget_left':
        child = QtWidgets.QTabWidget(widget)
        child.setTabPosition(QtWidgets.QTabWidget.West)
        child.addTab(QtWidgets.QWidget(), 'Tab 1')
        child.addTab(QtWidgets.QWidget(), 'Tab 2')
        child.addTab(QtWidgets.QWidget(), 'Tab 3')
    elif args.widget == 'tab_widget_right':
        child = QtWidgets.QTabWidget(widget)
        child.setTabPosition(QtWidgets.QTabWidget.East)
        child.addTab(QtWidgets.QWidget(), 'Tab 1')
        child.addTab(QtWidgets.QWidget(), 'Tab 2')
        child.addTab(QtWidgets.QWidget(), 'Tab 3')
    elif args.widget == 'tab_widget_bottom':
        child = QtWidgets.QTabWidget(widget)
        child.setTabPosition(QtWidgets.QTabWidget.South)
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
        child = []
        dock1 = QtWidgets.QDockWidget('&Dock widget 1', window)
        dock2 = QtWidgets.QDockWidget('&Dock widget 2', window)
        window.addDockWidget(QtCore.Qt.DockWidgetArea(QtCore.Qt.LeftDockWidgetArea), dock1)
        window.addDockWidget(QtCore.Qt.DockWidgetArea(QtCore.Qt.LeftDockWidgetArea), dock2)
        window.tabifyDockWidget(dock1, dock2)
    elif args.widget == 'radio':
        child = []
        child.append(abstract_button(QtWidgets.QRadioButton, widget))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, checked=True))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, enabled=False))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, checked=True, enabled=False))
        child.append(abstract_button(QtWidgets.QRadioButton, widget, 'With Text'))
    elif args.widget == 'checkbox':
        child = []
        child.append(abstract_button(QtWidgets.QCheckBox, widget))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=True))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=QtCore.Qt.PartiallyChecked))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, enabled=False))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=True, enabled=False))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, checked=QtCore.Qt.PartiallyChecked, enabled=False))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, 'With Text'))
        child.append(abstract_button(QtWidgets.QCheckBox, widget, 'With Large Text'))
        checkbox_font = app.font()
        checkbox_font.setPointSizeF(50.0)
        child[-1].setFont(checkbox_font)
    elif args.widget == 'table':
        child = QtWidgets.QTableWidget(widget)
        child.setColumnCount(2)
        child.setRowCount(4)
        item = QtWidgets.QTableWidgetItem('Row 1')
        child.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Row 2')
        child.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem('Row 3')
        child.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem('Row 4')
        child.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem('Column 1')
        child.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Column 2')
        child.setHorizontalHeaderItem(1, item)
    elif args.widget == 'sortable_table':
        child = QtWidgets.QTableWidget(widget)
        child.setSortingEnabled(True)
        child.setColumnCount(2)
        child.setRowCount(4)
        item = QtWidgets.QTableWidgetItem('Row 1')
        child.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Row 2')
        child.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem('Row 3')
        child.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem('Row 4')
        child.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem('Column 1')
        child.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Column 2')
        child.setHorizontalHeaderItem(1, item)
    elif args.widget == 'list':
        child = QtWidgets.QListWidget(widget)
        for index in range(10):
            item = QtWidgets.QListWidgetItem(f'Item {index + 1}')
            item.setTextAlignment(random.choice([QtCore.Qt.AlignLeft, QtCore.Qt.AlignRight, QtCore.Qt.AlignHCenter]))
            child.addItem(item)
        icon = QtGui.QIcon(':/dark/close.svg')
        for index in range(10):
            item = QtWidgets.QListWidgetItem(icon, f'Item {index + 1}')
            item.setTextAlignment(random.choice([QtCore.Qt.AlignLeft, QtCore.Qt.AlignRight, QtCore.Qt.AlignHCenter]))
            child.addItem(item)
    elif args.widget == 'scrollbar_vertical':
        child = QtWidgets.QListWidget(widget)
        for index in range(100):
            child.addItem(QtWidgets.QListWidgetItem(f'Item {index + 1}'))
    elif args.widget == 'scrollbar_horizontal':
        child = QtWidgets.QTableWidget(widget)
        child.setColumnCount(100)
        child.setRowCount(1)
        item = QtWidgets.QTableWidgetItem(f'Row 1')
        child.setVerticalHeaderItem(0, item)
        for index in range(100):
            item = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
            child.setHorizontalHeaderItem(index, item)
    elif args.widget == 'toolbar':
        child = QtWidgets.QToolBar('Toolbar')
        child.setOrientation(QtCore.Qt.Vertical)
        child.setGeometry(QtCore.QRect(0, 0, args.width, int(1.5 * font.pointSize())))
        child.addAction('&Action 1')
        child.addAction('&Action 2')
        child.addAction('&Action 3')
        icon = QtGui.QIcon(':/dark/close.svg')
        child.addAction(icon, '&Action 4')
        window.addToolBar(child)
    elif args.widget == 'toolbutton':
        layout_type = 'horizontal'
        child = [
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
            QtWidgets.QToolButton(widget),
        ]
        window.setTabOrder(child[0], child[1])
        window.setTabOrder(child[1], child[2])
        window.setTabOrder(child[2], child[3])
        window.setTabOrder(child[3], child[4])
        window.setTabOrder(child[4], child[5])
        window.setTabOrder(child[5], child[6])
        window.setTabOrder(child[6], child[7])
        child[0].setText('Simple ToolButton')
        child[1].setText('Action Toolbutton')
        child[2].setText('Menu Toolbutton')
        child[3].setText('Instant Toolbutton')
        child[1].addActions([
            QtWidgets.QAction('&Action 5', window),
            QtWidgets.QAction('&Action 6', window),
        ])
        child[2].setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        child[2].addActions([
            QtWidgets.QAction('&Action 9', window),
            QtWidgets.QAction('&Action 10', window),
        ])
        child[3].setPopupMode(QtWidgets.QToolButton.InstantPopup)
        child[3].addActions([
            QtWidgets.QAction('&Action 11', window),
            QtWidgets.QAction('&Action 12', window),
        ])
        child[4].setArrowType(QtCore.Qt.LeftArrow)
        child[5].setArrowType(QtCore.Qt.RightArrow)
        child[6].setArrowType(QtCore.Qt.UpArrow)
        child[7].setArrowType(QtCore.Qt.DownArrow)
        icon = QtGui.QIcon(':/dark/close.svg')
        child[8].setIcon(icon)
    elif args.widget == 'pushbutton':
        layout_type = 'horizontal'
        child = []
        child.append(abstract_button(QtWidgets.QPushButton, widget, 'Button 1', checked=True))
        child.append(abstract_button(QtWidgets.QPushButton, widget, 'Button 2', enabled=False))
        child.append(abstract_button(QtWidgets.QPushButton, widget, 'Button 3', checkable=False))
        icon = QtGui.QIcon(':/dark/close.svg')
        child.append(abstract_button(QtWidgets.QPushButton, widget, icon, 'Button 4', checkable=False))
    elif args.widget == 'tree':
        child = []
        tree1 = QtWidgets.QTreeWidget(widget)
        tree1.setHeaderLabel('Tree 1')
        item1 = QtWidgets.QTreeWidgetItem(tree1, ['Row 1'])
        item2 = QtWidgets.QTreeWidgetItem(tree1, ['Row 2'])
        item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])
        item4 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.2'])
        item5 = QtWidgets.QTreeWidgetItem(item4, ['Row 2.2.1'])
        item6 = QtWidgets.QTreeWidgetItem(item5, ['Row 2.2.1.1'])
        item7 = QtWidgets.QTreeWidgetItem(item5, ['Row 2.2.1.2'])
        item8 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.3'])
        item9 = QtWidgets.QTreeWidgetItem(tree1, ['Row 3'])
        item10 = QtWidgets.QTreeWidgetItem(item9, ['Row 3.1'])
        item11 = QtWidgets.QTreeWidgetItem(tree1, ['Row 4'])
        child.append(tree1)
        tree2 = QtWidgets.QTreeWidget(widget)
        tree2.setHeaderLabel('Tree 2')
        tree2.header().setSectionsClickable(True)
        item12 = QtWidgets.QTreeWidgetItem(tree2, ['Row 1', 'Column 2', 'Column 3'])
        child.append(tree2)
    elif args.widget == 'view_scrollarea':
        # For us to have both scrollbars visible.
        child = QtWidgets.QTableWidget(widget)
        child.setColumnCount(100)
        child.setRowCount(100)
        for index in range(100):
            row = QtWidgets.QTableWidgetItem(f'Row {index + 1}')
            child.setVerticalHeaderItem(0, row)
            column = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
            child.setHorizontalHeaderItem(index, column)
    elif args.widget == 'widget_scrollarea':
        child = QtWidgets.QProgressBar(widget)
        child.setProperty('value', 24)
        window.resize(30, 30)
    elif args.widget == 'frame':
        child = []
        text = QtWidgets.QTextEdit()
        text.setPlainText('Hello world\nTesting lines')
        child.append(text)
        table = QtWidgets.QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(5)
        child.append(table)
    elif args.widget == 'groupbox':
        child = []
        child.append(QtWidgets.QGroupBox('Groupbox 1', widget))
        checkable = QtWidgets.QGroupBox('Groupbox 2', widget)
        checkable.setCheckable(True)
        child.append(checkable)
        vbox = QtWidgets.QVBoxLayout(checkable)
        vbox.setAlignment(QtCore.Qt.AlignHCenter)
        vbox.addWidget(QtWidgets.QLineEdit('Sample Label'))
    elif args.widget == 'toolbox':
        # Test alignment with another item, in a vertical layout.
        child = []
        child.append(QtWidgets.QGroupBox('Groupbox', widget))
        child.append(QtWidgets.QGroupBox('Really, really long groupbox', widget))
        toolbox = QtWidgets.QToolBox(widget)
        child.append(toolbox)
        page1 = QtWidgets.QWidget()
        toolbox.addItem(page1, 'Page 1')
        page2 = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(page2)
        vbox.addWidget(QtWidgets.QLabel('Sample Label'))
        toolbox.addItem(page2, 'Page 2')
        page3 = QtWidgets.QWidget()
        toolbox.addItem(page3, 'Really, really long page 3')
    elif args.widget == 'menubutton':
        child = QtWidgets.QToolButton(widget)
        child.setText('Menu Toolbutton')
        child.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        child.addActions([
            QtWidgets.QAction('&Action 9', window),
            QtWidgets.QAction('&Action 10', window),
        ])
    elif args.widget == 'tooltip':
        child = QtWidgets.QPushButton('Sample Label')
        child.setToolTip('Sample Tooltip')
    elif args.widget == 'splashscreen':
        # This doesn't work with a central widget.
        # Handle the run here.
        pixmap = QtGui.QPixmap('assets/Yellowstone.jpg')
        size = app.screens()[0].size()
        scaled = pixmap.scaled(size, QtCore.Qt.KeepAspectRatio)
        splash = QtWidgets.QSplashScreen(scaled)
        splash.show()
        time.sleep(5)
        splash.finish(window)
        window.show()
        return app.exec()
    elif args.widget == 'calendar':
        child = QtWidgets.QCalendarWidget(widget)
        child.setGridVisible(True)
    else:
        raise NotImplementedError

    # Add the widgets to the layout.
    widget_layout = layout[layout_type]()
    if args.compress:
        widget_layout.addStretch(1)
        add_widgets(widget_layout, child)
        widget_layout.addStretch(1)
    else:
        add_widgets(widget_layout, child)
    if args.alignment is not None:
        widget_layout.setAlignment(alignment[args.alignment])
    widget.setLayout(widget_layout)
    scroll.setWidget(widget)
    window.setCentralWidget(scroll)

    # run
    window.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
