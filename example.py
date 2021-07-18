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
    example
    =======
'''

import argparse
import logging
import os
import sys

home = os.path.dirname(os.path.realpath(__file__))

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

args, unknown = parser.parse_known_args()
if args.pyqt6:
    from PyQt6 import QtCore, QtGui, QtWidgets
    QtCore.QDir.addSearchPath(args.stylesheet, f'{home}/pyqt6/{args.stylesheet}/')
    stylesheet = f'{args.stylesheet}:stylesheet.qss'
else:
    from PyQt5 import QtCore, QtGui, QtWidgets
    import breeze_resources
    stylesheet = f':/{args.stylesheet}/stylesheet.qss'

# Compat definitions, between Qt5 and Qt6.
if args.pyqt6:
    QAction = QtGui.QAction
    Horizontal = QtCore.Qt.Orientation.Horizontal
    Vertical = QtCore.Qt.Orientation.Vertical
    TopToolBarArea = QtCore.Qt.ToolBarArea.TopToolBarArea
    StyledPanel = QtWidgets.QFrame.Shape.StyledPanel
    HLine = QtWidgets.QFrame.Shape.HLine
    VLine = QtWidgets.QFrame.Shape.VLine
    Raised = QtWidgets.QFrame.Shadow.Raised
    Sunken = QtWidgets.QFrame.Shadow.Sunken
    InstantPopup = QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup
    MenuButtonPopup = QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup
    AlignTop = QtCore.Qt.AlignmentFlag.AlignTop
    ItemIsUserCheckable = QtCore.Qt.ItemFlag.ItemIsUserCheckable
    ItemIsUserTristate = QtCore.Qt.ItemFlag.ItemIsUserTristate
    Checked = QtCore.Qt.CheckState.Checked
    Unchecked = QtCore.Qt.CheckState.Unchecked
    PartiallyChecked = QtCore.Qt.CheckState.PartiallyChecked
    ReadOnly = QtCore.QFile.OpenModeFlag.ReadOnly
    Text = QtCore.QFile.OpenModeFlag.Text
    East = QtWidgets.QTabWidget.TabPosition.East
else:
    QAction = QtWidgets.QAction
    Horizontal = QtCore.Qt.Horizontal
    Vertical = QtCore.Qt.Vertical
    TopToolBarArea = QtCore.Qt.TopToolBarArea
    StyledPanel = QtWidgets.QFrame.StyledPanel
    HLine = QtWidgets.QFrame.HLine
    VLine = QtWidgets.QFrame.VLine
    Raised = QtWidgets.QFrame.Raised
    Sunken = QtWidgets.QFrame.Sunken
    InstantPopup = QtWidgets.QToolButton.InstantPopup
    MenuButtonPopup = QtWidgets.QToolButton.MenuButtonPopup
    AlignTop = QtCore.Qt.AlignTop
    ItemIsUserCheckable = QtCore.Qt.ItemIsUserCheckable
    ItemIsUserTristate = QtCore.Qt.ItemIsUserTristate
    Checked = QtCore.Qt.Checked
    Unchecked = QtCore.Qt.Unchecked
    PartiallyChecked = QtCore.Qt.PartiallyChecked
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    East = QtWidgets.QTabWidget.East


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(East)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName('tabWidget')
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName('tab')
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName('gridLayout')
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName('groupBox')
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.toolBox = QtWidgets.QToolBox(self.groupBox)
        self.toolBox.setObjectName('toolBox')
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 718, 227))
        self.page.setObjectName('page')
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_4.setObjectName('gridLayout_4')
        self.lineEdit = QtWidgets.QLineEdit(self.page)
        self.lineEdit.setObjectName('lineEdit')
        self.gridLayout_4.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.toolBox.addItem(self.page, '')
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 718, 227))
        self.page_2.setObjectName('page_2')
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_5.setObjectName('gridLayout_5')
        self.listWidget = QtWidgets.QListWidget(self.page_2)
        self.listWidget.setObjectName('listWidget')
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout_5.addWidget(self.listWidget, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_2, '')
        self.verticalLayout_3.addWidget(self.toolBox)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab)
        self.tabWidget_2.setObjectName('tabWidget_2')
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName('tab_3')
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_6.setObjectName('gridLayout_6')
        self.checkableButton = QtWidgets.QPushButton(self.tab_3)
        self.checkableButton.setCheckable(True)
        self.checkableButton.setChecked(True)
        self.checkableButton.setObjectName('checkableButton')
        self.gridLayout_6.addWidget(self.checkableButton, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        self.pushButton.setObjectName('pushButton')
        self.pushButton.setToolTip('Sample Tooltip1')
        self.gridLayout_6.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setObjectName('pushButton_5')
        self.gridLayout_6.addWidget(self.pushButton_5, 2, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_3, '')
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName('tab_5')
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_7.setObjectName('gridLayout_7')
        self.tableWidget = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget.setObjectName('tableWidget')
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayout_7.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_5, '')
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName('tab_4')
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_4)
        self.calendar = QtWidgets.QCalendarWidget(self.tab_4)
        self.calendar.setGridVisible(True)
        self.verticalLayout_6.addWidget(self.calendar)
        self.tabWidget_2.addTab(self.tab_4, '')
        self.tab_5v2 = QtWidgets.QWidget()
        self.tab_5v2.setObjectName('tab_5v2')
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_5v2)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_5v2)
        self.tableWidget_2.setColumnCount(100)
        self.tableWidget_2.setRowCount(1)
        item = QtWidgets.QTableWidgetItem(f'Row 1')
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        for index in range(100):
            item = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
            self.tableWidget_2.setHorizontalHeaderItem(index, item)
        self.verticalLayout_7.addWidget(self.tableWidget_2)
        self.tabWidget_2.addTab(self.tab_5v2, '')
        self.tab_6v2 = QtWidgets.QWidget()
        self.tab_6v2.setObjectName('tab_6v2')
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_6v2)
        splitter = QtWidgets.QSplitter(self.tab_6v2)
        splitter.addWidget(QtWidgets.QListWidget(self.tab_6v2))
        tree = QtWidgets.QTreeWidget(self.tab_6v2)
        item_12 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
        splitter.addWidget(tree)
        splitter.addWidget(QtWidgets.QTextEdit(self.tab_6v2))
        self.verticalLayout_8.addWidget(splitter)
        self.tabWidget_2.addTab(self.tab_6v2, '')
        self.gridLayout.addWidget(self.tabWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, '')
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName('tab_2')
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName('gridLayout_2')
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName('groupBox_2')
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName('label')
        self.verticalLayout_4.addWidget(self.label)
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName('radioButton')
        self.verticalLayout_4.addWidget(self.radioButton)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName('checkBox')
        self.verticalLayout_4.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_2.setTristate(True)
        self.checkBox_2.setObjectName('checkBox_2')
        self.verticalLayout_4.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_3.setEnabled(False)
        self.checkBox_3.setObjectName('checkBox_3')
        self.verticalLayout_4.addWidget(self.checkBox_3)
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox_2)
        self.treeWidget.setObjectName('treeWidget')
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2.setText(0, 'subitem')
        item_3 = QtWidgets.QTreeWidgetItem(item_2, ['Row 2.1'])
        item_3.setFlags(item_3.flags() | ItemIsUserCheckable)
        item_3.setCheckState(0, Unchecked)
        item_4 = QtWidgets.QTreeWidgetItem(item_2, ['Row 2.2'])
        item_5 = QtWidgets.QTreeWidgetItem(item_4, ['Row 2.2.1'])
        item_6 = QtWidgets.QTreeWidgetItem(item_5, ['Row 2.2.1.1'])
        item_7 = QtWidgets.QTreeWidgetItem(item_5, ['Row 2.2.1.2'])
        item_3.setFlags(item_7.flags() | ItemIsUserCheckable)
        item_7.setCheckState(0, Checked)
        item_8 = QtWidgets.QTreeWidgetItem(item_2, ['Row 2.3'])
        item_8.setFlags(item_8.flags() | ItemIsUserTristate)
        item_8.setCheckState(0, PartiallyChecked)
        item_9 = QtWidgets.QTreeWidgetItem(self.treeWidget, ['Row 3'])
        item_10 = QtWidgets.QTreeWidgetItem(item_9, ['Row 3.1'])
        item_11 = QtWidgets.QTreeWidgetItem(self.treeWidget, ['Row 4'])
        self.verticalLayout_4.addWidget(self.treeWidget)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.tab_3v2 = QtWidgets.QWidget()
        self.tab_3v2.setObjectName('tab_3v2')
        self.gridLayout_3v2 = QtWidgets.QGridLayout(self.tab_3v2)
        self.gridLayout_3v2.setObjectName('gridLayout_3v2')
        self.groupBox_3v2 = QtWidgets.QGroupBox(self.tab_3v2)
        self.groupBox_3v2.setObjectName('groupBox_3v2')
        self.verticalLayout_4v2 = QtWidgets.QVBoxLayout(self.groupBox_3v2)
        self.verticalLayout_4v2.setObjectName('verticalLayout_4v2')
        self.tabBar = QtWidgets.QTabBar(self.tab_3v2)
        self.gridLayout_3v2.setObjectName('tabBar')
        self.tabBar.addTab('TabBar Tab 1')
        self.tabBar.addTab('TabBar Tab 2')
        self.tabBar.addTab('TabBar Tab 3')
        self.verticalLayout_4v2.addWidget(self.tabBar, 0, AlignTop)
        self.gridLayout_3v2.addWidget(self.groupBox_3v2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, '')
        self.tabWidget.addTab(self.tab_3v2, '')
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName('pushButton_2')
        self.pushButton_2.setToolTip('Sample Tooltip2')
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.bt_delay_popup = QtWidgets.QToolButton(self.centralwidget)
        self.bt_delay_popup.setObjectName('bt_delay_popup')
        self.horizontalLayout.addWidget(self.bt_delay_popup)
        self.bt_instant_popup = QtWidgets.QToolButton(self.centralwidget)
        self.bt_instant_popup.setPopupMode(InstantPopup)
        self.bt_instant_popup.setObjectName('bt_instant_popup')
        self.horizontalLayout.addWidget(self.bt_instant_popup)
        self.bt_menu_button_popup = QtWidgets.QToolButton(self.centralwidget)
        self.bt_menu_button_popup.setPopupMode(MenuButtonPopup)
        self.bt_menu_button_popup.setObjectName('bt_menu_button_popup')
        self.horizontalLayout.addWidget(self.bt_menu_button_popup)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(VLine)
        self.line_2.setFrameShadow(Sunken)
        self.line_2.setObjectName('line_2')
        self.horizontalLayout.addWidget(self.line_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setObjectName('pushButton_3')
        self.pushButton_3.setToolTip('Sample Tooltip3')
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName('doubleSpinBox')
        self.horizontalLayout.addWidget(self.doubleSpinBox)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setPopupMode(InstantPopup)
        self.toolButton.setObjectName('toolButton')
        self.horizontalLayout.addWidget(self.toolButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1068, 29))
        self.menubar.setObjectName('menubar')
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName('menuMenu')
        self.menuSubmenu_2 = QtWidgets.QMenu(self.menuMenu)
        self.menuSubmenu_2.setObjectName('menuSubmenu_2')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget1 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget1.setObjectName('dockWidget1')
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName('dockWidgetContents')
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.comboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox.setObjectName('comboBox')
        self.comboBox.setEditable(True)
        self.comboBox.addItem('')
        self.comboBox.addItem('')
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalSlider = QtWidgets.QSlider(self.dockWidgetContents)
        self.horizontalSlider.setOrientation(Horizontal)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.textEdit = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName('textEdit')
        self.verticalLayout.addWidget(self.textEdit)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(HLine)
        self.line.setFrameShadow(Sunken)
        self.line.setObjectName('line')
        self.verticalLayout.addWidget(self.line)
        self.progressBar = QtWidgets.QProgressBar(self.dockWidgetContents)
        self.progressBar.setProperty('value', 24)
        self.progressBar.setObjectName('progressBar')
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.frame = QtWidgets.QFrame(self.dockWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, 100))
        self.frame.setFrameShape(StyledPanel)
        self.frame.setFrameShadow(Raised)
        self.frame.setLineWidth(3)
        self.frame.setObjectName('frame')
        self.verticalLayout_2.addWidget(self.frame)
        self.dockWidget1.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget1)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName('toolBar')
        MainWindow.addToolBar(TopToolBarArea, self.toolBar)
        self.dockWidget2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget2.setObjectName('dockWidget2')
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName('dockWidgetContents_2')
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        self.gridLayout_3.setObjectName('gridLayout_3')
        self.verticalSlider = QtWidgets.QSlider(self.dockWidgetContents_2)
        self.verticalSlider.setOrientation(Vertical)
        self.verticalSlider.setObjectName('verticalSlider')
        self.gridLayout_3.addWidget(self.verticalSlider, 0, 0, 1, 1)
        self.dockWidget2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget2)
        self.actionAction = QAction(MainWindow)
        self.actionAction.setObjectName('actionAction')
        self.actionSub_menu = QAction(MainWindow)
        self.actionSub_menu.setObjectName('actionSub_menu')
        self.actionAction_C = QAction(MainWindow)
        self.actionAction_C.setObjectName('actionAction_C')
        self.menuSubmenu_2.addAction(self.actionSub_menu)
        self.menuSubmenu_2.addAction(self.actionAction_C)
        self.menuMenu.addAction(self.actionAction)
        self.menuMenu.addAction(self.menuSubmenu_2.menuAction())
        self.menubar.addAction(self.menuMenu.menuAction())
        self.toolBar.addAction(self.actionAction)
        self.toolBar.addAction(self.actionSub_menu)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.checkableButton)
        MainWindow.setTabOrder(self.checkableButton, self.pushButton_5)
        MainWindow.setTabOrder(self.pushButton_5, self.tabWidget_2)
        MainWindow.setTabOrder(self.tabWidget_2, self.tableWidget)
        MainWindow.setTabOrder(self.tableWidget, self.radioButton)
        MainWindow.setTabOrder(self.radioButton, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.checkBox_2)
        MainWindow.setTabOrder(self.checkBox_2, self.treeWidget)
        MainWindow.setTabOrder(self.treeWidget, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.bt_delay_popup)
        MainWindow.setTabOrder(self.bt_delay_popup, self.bt_instant_popup)
        MainWindow.setTabOrder(self.bt_instant_popup, self.bt_menu_button_popup)
        MainWindow.setTabOrder(self.bt_menu_button_popup, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.doubleSpinBox)
        MainWindow.setTabOrder(self.doubleSpinBox, self.toolButton)
        MainWindow.setTabOrder(self.toolButton, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.horizontalSlider)
        MainWindow.setTabOrder(self.horizontalSlider, self.textEdit)
        MainWindow.setTabOrder(self.textEdit, self.verticalSlider)
        MainWindow.setTabOrder(self.verticalSlider, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.listWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.groupBox.setTitle(_translate('MainWindow', 'ToolBox'))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate('MainWindow', 'Page 1'))
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(1)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(2)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(3)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(4)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(5)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(6)
        item.setText(_translate('MainWindow', 'New Item'))
        item = self.listWidget.item(7)
        item.setText(_translate('MainWindow', 'New Item'))
        self.listWidget.setSortingEnabled(True)
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate('MainWindow', 'Page 2'))
        self.checkableButton.setText(_translate('MainWindow', 'Checkable button'))
        self.pushButton.setText(_translate('MainWindow', 'PushButton'))
        self.pushButton_5.setText(_translate('MainWindow', 'PushButton'))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate('MainWindow', 'Tab 1'))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate('MainWindow', 'New Row'))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate('MainWindow', 'New Row'))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate('MainWindow', 'New Row'))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate('MainWindow', 'New Row'))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate('MainWindow', 'New Column'))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate('MainWindow', 'New Column 2'))
        self.tableWidget.setSortingEnabled(True)
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate('MainWindow', 'Page'))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate('MainWindow', 'Tab 2'))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5v2), _translate('MainWindow', 'Tab 3'))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6v2), _translate('MainWindow', 'Tab 4'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate('MainWindow', 'Tab 1'))
        self.groupBox_2.setTitle(_translate('MainWindow', 'GroupBox'))
        self.label.setText(_translate('MainWindow', 'TextLabel'))
        self.radioButton.setText(_translate('MainWindow', 'RadioB&utton'))
        self.checkBox.setText(_translate('MainWindow', 'CheckBox'))
        self.checkBox_2.setText(_translate('MainWindow', 'CheckBox Tristate'))
        self.checkBox_3.setText(_translate('MainWindow', 'CheckBox Disabled'))
        self.treeWidget.headerItem().setText(0, _translate('MainWindow', 'qdz'))
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate('MainWindow', 'qzd'))
        self.treeWidget.topLevelItem(1).setText(0, _translate('MainWindow', 'effefe'))
        self.treeWidget.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate('MainWindow', 'Tab 2'))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3v2), _translate('MainWindow', 'Tab 3'))
        self.groupBox_3v2.setTitle(_translate('MainWindow', 'GroupBox v2'))
        self.pushButton_2.setText(_translate('MainWindow', 'PushButton'))
        self.bt_delay_popup.setText(_translate('MainWindow', 'Delayed popup  '))
        self.bt_instant_popup.setText(_translate('MainWindow', 'Instant popup'))
        self.bt_menu_button_popup.setText(_translate('MainWindow', 'MenuButtonPopup'))
        self.pushButton_3.setText(_translate('MainWindow', 'Disabled'))
        self.toolButton.setText(_translate('MainWindow', '...'))
        self.menuMenu.setTitle(_translate('MainWindow', '&Menu'))
        self.menuSubmenu_2.setTitle(_translate('MainWindow', '&Submenu 2'))
        self.dockWidget1.setWindowTitle(_translate('MainWindow', '&Dock widget 1'))
        self.comboBox.setItemText(0, _translate('MainWindow', 'Item 0'))
        self.comboBox.setItemText(1, _translate('MainWindow', 'Item 2'))
        self.toolBar.setWindowTitle(_translate('MainWindow', 'toolBar'))
        self.dockWidget2.setWindowTitle(_translate('MainWindow', 'Dock widget &2'))
        self.actionAction.setText(_translate('MainWindow', '&Action'))
        self.actionSub_menu.setText(_translate('MainWindow', '&Action B'))
        self.actionSub_menu.setToolTip(_translate('MainWindow', 'submenu'))
        self.actionAction_C.setText(_translate('MainWindow', 'Action &C'))

    def about(self):
        QtWidgets.QMessageBox.aboutQt(self.centralwidget, 'About Menu')

    def critical(self):
        QtWidgets.QMessageBox.critical(self.centralwidget, 'Error', 'Critical Error')


def main():
    'Application entry point'

    if args.scale != 1:
        os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    else:
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    if args.style != 'native':
        style = QtWidgets.QStyleFactory.create(args.style)
        QtWidgets.QApplication.setStyle(style)
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv[:1] + unknown)
    window = QtWidgets.QMainWindow()

     # use the default font size
    font = app.font()
    if args.font_size > 0:
        font.setPointSizeF(args.font_size)
    if args.font_family:
        font.setFamily(args.font_family)
    app.setFont(font)

    # setup ui
    ui = Ui()
    ui.setup(window)
    ui.bt_delay_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    ui.bt_instant_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    ui.bt_menu_button_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    window.setWindowTitle('Sample BreezeStyleSheets application.')

    # Add event triggers
    ui.actionAction.triggered.connect(ui.about)
    ui.actionAction_C.triggered.connect(ui.critical)

    # tabify dock widgets to show bug #6
    window.tabifyDockWidget(ui.dockWidget1, ui.dockWidget2)

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
