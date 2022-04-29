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
    standard_icons
    ==============

    Example overriding QCommonStyle for custom standard icons.
'''

import argparse
import logging
import os
import sys

example_dir = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(example_dir)
dist = os.path.join(home, 'dist')

# Create our arguments.
parser = argparse.ArgumentParser(description='Configurations for the Qt5 application.')
# Know working styles include:
#   1. Fusion
#   2. Windows
parser.add_argument(
    '--style',
    help='''application style, which is different than the stylesheet''',
    default='fusion'
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
    QAction = QtGui.QAction
    Horizontal = QtCore.Qt.Orientation.Horizontal
    AlignHCenter = QtCore.Qt.AlignmentFlag.AlignHCenter
    HLine = QtWidgets.QFrame.Shape.HLine
    Sunken = QtWidgets.QFrame.Shadow.Sunken
    ReadOnly = QtCore.QFile.OpenModeFlag.ReadOnly
    Text = QtCore.QFile.OpenModeFlag.Text
    SP_ArrowBack = QtWidgets.QStyle.StandardPixmap.SP_ArrowBack
    SP_ArrowDown = QtWidgets.QStyle.StandardPixmap.SP_ArrowDown
    SP_ArrowForward = QtWidgets.QStyle.StandardPixmap.SP_ArrowForward
    SP_ArrowLeft = QtWidgets.QStyle.StandardPixmap.SP_ArrowLeft
    SP_ArrowRight = QtWidgets.QStyle.StandardPixmap.SP_ArrowRight
    SP_ArrowUp = QtWidgets.QStyle.StandardPixmap.SP_ArrowUp
    SP_BrowserReload = QtWidgets.QStyle.StandardPixmap.SP_BrowserReload
    SP_BrowserStop = QtWidgets.QStyle.StandardPixmap.SP_BrowserStop
    SP_CommandLink = QtWidgets.QStyle.StandardPixmap.SP_CommandLink
    SP_ComputerIcon = QtWidgets.QStyle.StandardPixmap.SP_ComputerIcon
    SP_CustomBase = QtWidgets.QStyle.StandardPixmap.SP_CustomBase
    SP_DesktopIcon = QtWidgets.QStyle.StandardPixmap.SP_DesktopIcon
    SP_DialogApplyButton = QtWidgets.QStyle.StandardPixmap.SP_DialogApplyButton
    SP_DialogCancelButton = QtWidgets.QStyle.StandardPixmap.SP_DialogCancelButton
    SP_DialogCloseButton = QtWidgets.QStyle.StandardPixmap.SP_DialogCloseButton
    SP_DialogDiscardButton = QtWidgets.QStyle.StandardPixmap.SP_DialogDiscardButton
    SP_DialogHelpButton = QtWidgets.QStyle.StandardPixmap.SP_DialogHelpButton
    SP_DialogNoButton = QtWidgets.QStyle.StandardPixmap.SP_DialogNoButton
    SP_DialogOkButton = QtWidgets.QStyle.StandardPixmap.SP_DialogOkButton
    SP_DialogOpenButton = QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton
    SP_DialogResetButton = QtWidgets.QStyle.StandardPixmap.SP_DialogResetButton
    SP_DialogSaveButton = QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton
    SP_DialogYesButton = QtWidgets.QStyle.StandardPixmap.SP_DialogYesButton
    SP_DirClosedIcon = QtWidgets.QStyle.StandardPixmap.SP_DirClosedIcon
    SP_DirHomeIcon = QtWidgets.QStyle.StandardPixmap.SP_DirHomeIcon
    SP_DirIcon = QtWidgets.QStyle.StandardPixmap.SP_DirIcon
    SP_DirLinkIcon = QtWidgets.QStyle.StandardPixmap.SP_DirLinkIcon
    SP_DirOpenIcon = QtWidgets.QStyle.StandardPixmap.SP_DirOpenIcon
    SP_DockWidgetCloseButton = QtWidgets.QStyle.StandardPixmap.SP_DockWidgetCloseButton
    SP_DriveCDIcon = QtWidgets.QStyle.StandardPixmap.SP_DriveCDIcon
    SP_DriveDVDIcon = QtWidgets.QStyle.StandardPixmap.SP_DriveDVDIcon
    SP_DriveFDIcon = QtWidgets.QStyle.StandardPixmap.SP_DriveFDIcon
    SP_DriveHDIcon = QtWidgets.QStyle.StandardPixmap.SP_DriveHDIcon
    SP_DriveNetIcon = QtWidgets.QStyle.StandardPixmap.SP_DriveNetIcon
    SP_FileDialogBack = QtWidgets.QStyle.StandardPixmap.SP_FileDialogBack
    SP_FileDialogContentsView = QtWidgets.QStyle.StandardPixmap.SP_FileDialogContentsView
    SP_FileDialogDetailedView = QtWidgets.QStyle.StandardPixmap.SP_FileDialogDetailedView
    SP_FileDialogEnd = QtWidgets.QStyle.StandardPixmap.SP_FileDialogEnd
    SP_FileDialogInfoView = QtWidgets.QStyle.StandardPixmap.SP_FileDialogInfoView
    SP_FileDialogListView = QtWidgets.QStyle.StandardPixmap.SP_FileDialogListView
    SP_FileDialogNewFolder = QtWidgets.QStyle.StandardPixmap.SP_FileDialogNewFolder
    SP_FileDialogStart = QtWidgets.QStyle.StandardPixmap.SP_FileDialogStart
    SP_FileDialogToParent = QtWidgets.QStyle.StandardPixmap.SP_FileDialogToParent
    SP_FileIcon = QtWidgets.QStyle.StandardPixmap.SP_FileIcon
    SP_FileLinkIcon = QtWidgets.QStyle.StandardPixmap.SP_FileLinkIcon
    SP_MediaPause = QtWidgets.QStyle.StandardPixmap.SP_MediaPause
    SP_MediaPlay = QtWidgets.QStyle.StandardPixmap.SP_MediaPlay
    SP_MediaSeekBackward = QtWidgets.QStyle.StandardPixmap.SP_MediaSeekBackward
    SP_MediaSeekForward = QtWidgets.QStyle.StandardPixmap.SP_MediaSeekForward
    SP_MediaSkipBackward = QtWidgets.QStyle.StandardPixmap.SP_MediaSkipBackward
    SP_MediaSkipForward = QtWidgets.QStyle.StandardPixmap.SP_MediaSkipForward
    SP_MediaStop = QtWidgets.QStyle.StandardPixmap.SP_MediaStop
    SP_MediaVolume = QtWidgets.QStyle.StandardPixmap.SP_MediaVolume
    SP_MediaVolumeMuted = QtWidgets.QStyle.StandardPixmap.SP_MediaVolumeMuted
    SP_MessageBoxCritical = QtWidgets.QStyle.StandardPixmap.SP_MessageBoxCritical
    SP_MessageBoxInformation = QtWidgets.QStyle.StandardPixmap.SP_MessageBoxInformation
    SP_MessageBoxQuestion = QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion
    SP_MessageBoxWarning = QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning
    SP_TitleBarCloseButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton
    SP_TitleBarContextHelpButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarContextHelpButton
    SP_TitleBarMaxButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarMaxButton
    SP_TitleBarMenuButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarMenuButton
    SP_TitleBarMinButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarMinButton
    SP_TitleBarNormalButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarNormalButton
    SP_TitleBarShadeButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarShadeButton
    SP_TitleBarUnshadeButton = QtWidgets.QStyle.StandardPixmap.SP_TitleBarUnshadeButton
    SP_ToolBarHorizontalExtensionButton = QtWidgets.QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton
    SP_ToolBarVerticalExtensionButton = QtWidgets.QStyle.StandardPixmap.SP_ToolBarVerticalExtensionButton
    SP_TrashIcon = QtWidgets.QStyle.StandardPixmap.SP_TrashIcon
    SP_VistaShield = QtWidgets.QStyle.StandardPixmap.SP_VistaShield
else:
    QAction = QtWidgets.QAction
    Horizontal = QtCore.Qt.Horizontal
    AlignHCenter = QtCore.Qt.AlignHCenter
    HLine = QtWidgets.QFrame.HLine
    Sunken = QtWidgets.QFrame.Sunken
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    SP_ArrowBack = QtWidgets.QStyle.SP_ArrowBack
    SP_ArrowDown = QtWidgets.QStyle.SP_ArrowDown
    SP_ArrowForward = QtWidgets.QStyle.SP_ArrowForward
    SP_ArrowLeft = QtWidgets.QStyle.SP_ArrowLeft
    SP_ArrowRight = QtWidgets.QStyle.SP_ArrowRight
    SP_ArrowUp = QtWidgets.QStyle.SP_ArrowUp
    SP_BrowserReload = QtWidgets.QStyle.SP_BrowserReload
    SP_BrowserStop = QtWidgets.QStyle.SP_BrowserStop
    SP_CommandLink = QtWidgets.QStyle.SP_CommandLink
    SP_ComputerIcon = QtWidgets.QStyle.SP_ComputerIcon
    SP_CustomBase = QtWidgets.QStyle.SP_CustomBase
    SP_DesktopIcon = QtWidgets.QStyle.SP_DesktopIcon
    SP_DialogApplyButton = QtWidgets.QStyle.SP_DialogApplyButton
    SP_DialogCancelButton = QtWidgets.QStyle.SP_DialogCancelButton
    SP_DialogCloseButton = QtWidgets.QStyle.SP_DialogCloseButton
    SP_DialogDiscardButton = QtWidgets.QStyle.SP_DialogDiscardButton
    SP_DialogHelpButton = QtWidgets.QStyle.SP_DialogHelpButton
    SP_DialogNoButton = QtWidgets.QStyle.SP_DialogNoButton
    SP_DialogOkButton = QtWidgets.QStyle.SP_DialogOkButton
    SP_DialogOpenButton = QtWidgets.QStyle.SP_DialogOpenButton
    SP_DialogResetButton = QtWidgets.QStyle.SP_DialogResetButton
    SP_DialogSaveButton = QtWidgets.QStyle.SP_DialogSaveButton
    SP_DialogYesButton = QtWidgets.QStyle.SP_DialogYesButton
    SP_DirClosedIcon = QtWidgets.QStyle.SP_DirClosedIcon
    SP_DirHomeIcon = QtWidgets.QStyle.SP_DirHomeIcon
    SP_DirIcon = QtWidgets.QStyle.SP_DirIcon
    SP_DirLinkIcon = QtWidgets.QStyle.SP_DirLinkIcon
    SP_DirOpenIcon = QtWidgets.QStyle.SP_DirOpenIcon
    SP_DockWidgetCloseButton = QtWidgets.QStyle.SP_DockWidgetCloseButton
    SP_DriveCDIcon = QtWidgets.QStyle.SP_DriveCDIcon
    SP_DriveDVDIcon = QtWidgets.QStyle.SP_DriveDVDIcon
    SP_DriveFDIcon = QtWidgets.QStyle.SP_DriveFDIcon
    SP_DriveHDIcon = QtWidgets.QStyle.SP_DriveHDIcon
    SP_DriveNetIcon = QtWidgets.QStyle.SP_DriveNetIcon
    SP_FileDialogBack = QtWidgets.QStyle.SP_FileDialogBack
    SP_FileDialogContentsView = QtWidgets.QStyle.SP_FileDialogContentsView
    SP_FileDialogDetailedView = QtWidgets.QStyle.SP_FileDialogDetailedView
    SP_FileDialogEnd = QtWidgets.QStyle.SP_FileDialogEnd
    SP_FileDialogInfoView = QtWidgets.QStyle.SP_FileDialogInfoView
    SP_FileDialogListView = QtWidgets.QStyle.SP_FileDialogListView
    SP_FileDialogNewFolder = QtWidgets.QStyle.SP_FileDialogNewFolder
    SP_FileDialogStart = QtWidgets.QStyle.SP_FileDialogStart
    SP_FileDialogToParent = QtWidgets.QStyle.SP_FileDialogToParent
    SP_FileIcon = QtWidgets.QStyle.SP_FileIcon
    SP_FileLinkIcon = QtWidgets.QStyle.SP_FileLinkIcon
    SP_MediaPause = QtWidgets.QStyle.SP_MediaPause
    SP_MediaPlay = QtWidgets.QStyle.SP_MediaPlay
    SP_MediaSeekBackward = QtWidgets.QStyle.SP_MediaSeekBackward
    SP_MediaSeekForward = QtWidgets.QStyle.SP_MediaSeekForward
    SP_MediaSkipBackward = QtWidgets.QStyle.SP_MediaSkipBackward
    SP_MediaSkipForward = QtWidgets.QStyle.SP_MediaSkipForward
    SP_MediaStop = QtWidgets.QStyle.SP_MediaStop
    SP_MediaVolume = QtWidgets.QStyle.SP_MediaVolume
    SP_MediaVolumeMuted = QtWidgets.QStyle.SP_MediaVolumeMuted
    SP_MessageBoxCritical = QtWidgets.QStyle.SP_MessageBoxCritical
    SP_MessageBoxInformation = QtWidgets.QStyle.SP_MessageBoxInformation
    SP_MessageBoxQuestion = QtWidgets.QStyle.SP_MessageBoxQuestion
    SP_MessageBoxWarning = QtWidgets.QStyle.SP_MessageBoxWarning
    SP_TitleBarCloseButton = QtWidgets.QStyle.SP_TitleBarCloseButton
    SP_TitleBarContextHelpButton = QtWidgets.QStyle.SP_TitleBarContextHelpButton
    SP_TitleBarMaxButton = QtWidgets.QStyle.SP_TitleBarMaxButton
    SP_TitleBarMenuButton = QtWidgets.QStyle.SP_TitleBarMenuButton
    SP_TitleBarMinButton = QtWidgets.QStyle.SP_TitleBarMinButton
    SP_TitleBarNormalButton = QtWidgets.QStyle.SP_TitleBarNormalButton
    SP_TitleBarShadeButton = QtWidgets.QStyle.SP_TitleBarShadeButton
    SP_TitleBarUnshadeButton = QtWidgets.QStyle.SP_TitleBarUnshadeButton
    SP_ToolBarHorizontalExtensionButton = QtWidgets.QStyle.SP_ToolBarHorizontalExtensionButton
    SP_ToolBarVerticalExtensionButton = QtWidgets.QStyle.SP_ToolBarVerticalExtensionButton
    SP_TrashIcon = QtWidgets.QStyle.SP_TrashIcon
    SP_VistaShield = QtWidgets.QStyle.SP_VistaShield

# Need to fix an issue on Wayland on Linux:
#   conda-forge does not support Wayland, for who knows what reason.
if sys.platform.lower().startswith('linux') and 'CONDA_PREFIX' in os.environ:
    args.use_x11 = True

if args.use_x11:
    os.environ['XDG_SESSION_TYPE'] = 'x11'


def standard_icon(widget, name):
    '''Get the close icon depending on the stylesheet.'''
    return widget.style().standardIcon(name)


def native_icon(style, icon, option=None, widget=None):
    '''Get a standard icon for the native style'''
    return style.standardIcon(icon, option, widget)


def style_icon(style, icon, option=None, widget=None):
    if args.stylesheet == 'native':
        return native_icon(style, icon, option, widget)
    return stylesheet_icon(style, icon, option, widget)


def stylesheet_icon(style, icon, option=None, widget=None):
    '''Get a standard icon for the stylesheet style'''

    if icon == SP_ArrowLeft:
        return QtGui.QIcon(f'{resource_format}left_arrow.svg')
    elif icon == SP_ArrowDown:
        return QtGui.QIcon(f'{resource_format}down_arrow.svg')
    elif icon == SP_ArrowRight:
        return QtGui.QIcon(f'{resource_format}right_arrow.svg')
    elif icon == SP_ArrowUp:
        return QtGui.QIcon(f'{resource_format}up_arrow.svg')
    elif icon == SP_DockWidgetCloseButton:
        return QtGui.QIcon(f'{resource_format}close.svg')
    elif icon == SP_DialogCancelButton:
        return QtGui.QIcon(f'{resource_format}dialog_cancel.svg')
    elif icon == SP_DialogCloseButton:
        return QtGui.QIcon(f'{resource_format}dialog_close.svg')
    elif icon == SP_DialogDiscardButton:
        return QtGui.QIcon(f'{resource_format}dialog_discard.svg')
    elif icon == SP_DialogHelpButton:
        return QtGui.QIcon(f'{resource_format}dialog_help.svg')
    elif icon == SP_DialogNoButton:
        return QtGui.QIcon(f'{resource_format}dialog_no.svg')
    elif icon == SP_DialogOkButton:
        return QtGui.QIcon(f'{resource_format}dialog_ok.svg')
    elif icon == SP_DialogOpenButton:
        return QtGui.QIcon(f'{resource_format}dialog_open.svg')
    elif icon == SP_DialogResetButton:
        return QtGui.QIcon(f'{resource_format}dialog_reset.svg')
    elif icon == SP_DialogSaveButton:
        return QtGui.QIcon(f'{resource_format}dialog_save.svg')
    return style.standardIcon(icon, option, widget)


class ApplicationStyle(QtWidgets.QCommonStyle):
    def __init__(self, style):
        super().__init__()
        self.style = style

    def __getattribute__(self, item):
        '''
        Override for standardIcon. Everything else should default to the
        system default. We cannot have `style_icon` be a member of
        `ApplicationStyle`, since this will cause an infinite recursive loop.
        '''

        if item == 'standardIcon':
            return lambda *x: style_icon(self, *x)
        return getattr(self.style, item)


def standard_button(ui, icon, index):
    '''Create a QToolButton with a standard icon.'''

    button = QtWidgets.QToolButton(ui.centralwidget)
    setattr(ui, f'button{index}', button)
    button.setAutoRaise(True)
    button.setIcon(standard_icon(button, icon))
    button.setObjectName(f'button{index}')
    ui.layout.addWidget(button)


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

        standard_button(self, SP_ArrowLeft, 0)
        standard_button(self, SP_ArrowDown, 1)
        standard_button(self, SP_ArrowRight, 2)
        standard_button(self, SP_ArrowUp, 3)
        standard_button(self, SP_DockWidgetCloseButton, 4)
        standard_button(self, SP_DialogCancelButton, 5)
        standard_button(self, SP_DialogCloseButton, 6)
        standard_button(self, SP_DialogDiscardButton, 7)
        standard_button(self, SP_DialogHelpButton, 8)
        standard_button(self, SP_DialogNoButton, 9)
        standard_button(self, SP_DialogOkButton, 10)
        standard_button(self, SP_DialogOpenButton, 11)
        standard_button(self, SP_DialogResetButton, 12)
        standard_button(self, SP_DialogSaveButton, 13)

        self.dockWidget1 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget1.setObjectName('dockWidget1')
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName('dockWidgetContents')
        self.dockWidget1.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget1)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.comboBox = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox.setObjectName('comboBox')
        self.comboBox.setEditable(True)
        self.comboBox.addItem('First')
        self.comboBox.addItem('Second')
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

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1068, 29))
        self.menubar.setObjectName('menubar')
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName('menuMenu')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.actionAction = QAction(MainWindow)
        self.actionAction.setObjectName('actionAction')
        self.actionAction_C = QAction(MainWindow)
        self.actionAction_C.setObjectName('actionAction_C')

        self.menuMenu.addAction(self.actionAction)
        self.menuMenu.addAction(self.actionAction_C)
        self.menubar.addAction(self.menuMenu.menuAction())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.menuMenu.setTitle(_translate('MainWindow', '&Menu'))
        self.actionAction.setText(_translate('MainWindow', '&Action'))
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
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv[:1] + unknown)
    window = QtWidgets.QMainWindow()

    style = QtWidgets.QStyleFactory.create(args.style)
    app.setStyle(ApplicationStyle(style))

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
    window.setWindowTitle('Custom standard icons.')

    # Add event triggers
    ui.actionAction.triggered.connect(ui.about)
    ui.actionAction_C.triggered.connect(ui.critical)

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
