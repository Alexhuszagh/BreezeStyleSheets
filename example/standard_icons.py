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
    standard_icons
    ==============

    Example overriding QCommonStyle for custom standard icons.
'''

import shared
import sys

parser = shared.create_parser()
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
ICON_MAP = shared.get_icon_map(args, compat)


def style_icon(style, icon, option=None, widget=None):
    return shared.style_icon(args, style, icon, ICON_MAP, option, widget)


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


def add_standard_button(ui, layout, icon, index):
    '''Create and add a QToolButton with a standard icon.'''

    button = QtWidgets.QToolButton(ui.centralwidget)
    setattr(ui, f'button{index}', button)
    button.setAutoRaise(True)
    button.setIcon(style_icon(button.style(), icon, widget=button))
    button.setObjectName(f'button{index}')
    layout.addWidget(button)


def add_standard_buttons(ui, page, icons):
    '''Create and add QToolButtons with standard icons to the UI.'''

    for icon_name in icons:
        icon_enum = getattr(compat, icon_name)
        icon = style_icon(page.style(), icon_enum, widget=page)
        item = QtWidgets.QListWidgetItem(icon, icon_name)
        page.addItem(item)


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

        self.tool_box = QtWidgets.QToolBox(self.centralwidget)
        self.page1 = QtWidgets.QListWidget()
        self.tool_box.addItem(self.page1, 'Overwritten Icons')
        self.layout.addWidget(self.tool_box)

        add_standard_buttons(self, self.page1, [
            'SP_ArrowLeft',
            'SP_ArrowDown',
            'SP_ArrowRight',
            'SP_ArrowUp',
            'SP_DockWidgetCloseButton',
            'SP_DialogCancelButton',
            'SP_DialogCloseButton',
            'SP_DialogDiscardButton',
            'SP_DialogHelpButton',
            'SP_DialogNoButton',
            'SP_DialogOkButton',
            'SP_DialogOpenButton',
            'SP_DialogResetButton',
            'SP_DialogSaveButton',
        ])

        self.page2 = QtWidgets.QListWidget()
        self.tool_box.addItem(self.page2, 'Default Icons')
        self.layout.addWidget(self.tool_box)

        default_icons = [
            'SP_TitleBarMinButton',
            'SP_TitleBarMenuButton',
            'SP_TitleBarMaxButton',
            'SP_TitleBarCloseButton',
            'SP_TitleBarNormalButton',
            'SP_TitleBarShadeButton',
            'SP_TitleBarUnshadeButton',
            'SP_TitleBarContextHelpButton',
            'SP_MessageBoxInformation',
            'SP_MessageBoxWarning',
            'SP_MessageBoxCritical',
            'SP_MessageBoxQuestion',
            'SP_DesktopIcon',
            'SP_TrashIcon',
            'SP_ComputerIcon',
            'SP_DriveFDIcon',
            'SP_DriveHDIcon',
            'SP_DriveCDIcon',
            'SP_DriveDVDIcon',
            'SP_DriveNetIcon',
            'SP_DirHomeIcon',
            'SP_DirOpenIcon',
            'SP_DirClosedIcon',
            'SP_DirIcon',
            'SP_DirLinkIcon',
            'SP_DirLinkOpenIcon',
            'SP_FileIcon',
            'SP_FileLinkIcon',
            'SP_FileDialogStart',
            'SP_FileDialogEnd',
            'SP_FileDialogToParent',
            'SP_FileDialogNewFolder',
            'SP_FileDialogDetailedView',
            'SP_FileDialogInfoView',
            'SP_FileDialogContentsView',
            'SP_FileDialogListView',
            'SP_FileDialogBack',
            'SP_ToolBarHorizontalExtensionButton',
            'SP_ToolBarVerticalExtensionButton',
            'SP_DialogApplyButton',
            'SP_DialogYesButton',
            'SP_ArrowBack',
            'SP_ArrowForward',
            'SP_CommandLink',
            'SP_VistaShield',
            'SP_BrowserReload',
            'SP_BrowserStop',
            'SP_MediaPlay',
            'SP_MediaStop',
            'SP_MediaPause',
            'SP_MediaSkipForward',
            'SP_MediaSkipBackward',
            'SP_MediaSeekForward',
            'SP_MediaSeekBackward',
            'SP_MediaVolume',
            'SP_MediaVolumeMuted',
            'SP_LineEditClearButton',
            'SP_DialogYesToAllButton',
            'SP_DialogNoToAllButton',
            'SP_DialogSaveAllButton',
            'SP_DialogAbortButton',
            'SP_DialogRetryButton',
            'SP_DialogIgnoreButton',
            'SP_RestoreDefaultsButton',
        ]
        # QT_VERSION is stored in 0xMMmmpp, each in 16 bit pairs.
        # Goes major, minor, patch. 393984 is "6.3.0"
        if QtCore.QT_VERSION >= 393984:
            default_icons.append('SP_TabCloseButton')
        add_standard_buttons(self, self.page2, default_icons)

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
        self.horizontalSlider.setOrientation(compat.Horizontal)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.textEdit = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName('textEdit')
        self.verticalLayout.addWidget(self.textEdit)
        self.line = QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(compat.HLine)
        self.line.setFrameShadow(compat.Sunken)
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

        self.actionAction = compat.QAction(MainWindow)
        self.actionAction.setObjectName('actionAction')
        self.actionAction_C = compat.QAction(MainWindow)
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

    app, window = shared.setup_app(args, unknown, compat, style_class=ApplicationStyle)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('Custom standard icons.')

    # Add event triggers
    ui.actionAction.triggered.connect(ui.about)
    ui.actionAction_C.triggered.connect(ui.critical)

    shared.set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)

if __name__ == '__main__':
    sys.exit(main())
