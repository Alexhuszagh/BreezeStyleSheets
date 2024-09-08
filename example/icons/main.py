#!/usr/bin/env python
'''
    standard_icons
    ==============

    Example overriding QCommonStyle for custom standard icons.
'''

import sys

import standard


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):  # pylint: disable=too-many-statements
        '''Setup our main window for the UI.'''

        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = standard.compat.QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = standard.compat.QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        self.layout.setAlignment(standard.compat.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.tool_box = standard.compat.QtWidgets.QToolBox(self.centralwidget)
        self.page1 = standard.compat.QtWidgets.QListWidget()
        self.tool_box.addItem(self.page1, 'Overwritten Icons')
        self.layout.addWidget(self.tool_box)

        standard.add_standard_buttons(
            self,
            self.page1,
            [
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
            ],
        )

        self.page2 = standard.QtWidgets.QListWidget()
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
        if standard.compat.QT_VERSION >= (6, 3, 0):
            default_icons.append('SP_TabCloseButton')
        standard.add_standard_buttons(self, self.page2, default_icons)

        self.dockWidget1 = standard.compat.QtWidgets.QDockWidget(MainWindow)
        self.dockWidget1.setObjectName('dockWidget1')
        self.dockWidgetContents = standard.compat.QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName('dockWidgetContents')
        self.dockWidget1.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(standard.compat.QtCore.Qt.DockWidgetArea(1), self.dockWidget1)

        self.verticalLayout_2 = standard.compat.QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.verticalLayout = standard.compat.QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.comboBox = standard.compat.QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox.setObjectName('comboBox')
        self.comboBox.setEditable(True)
        self.comboBox.addItem('First')
        self.comboBox.addItem('Second')
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalSlider = standard.compat.QtWidgets.QSlider(self.dockWidgetContents)
        self.horizontalSlider.setOrientation(standard.compat.Horizontal)
        self.horizontalSlider.setObjectName('horizontalSlider')
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.textEdit = standard.compat.QtWidgets.QTextEdit(self.dockWidgetContents)
        self.textEdit.setObjectName('textEdit')
        self.verticalLayout.addWidget(self.textEdit)
        self.line = standard.compat.QtWidgets.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(standard.compat.HLine)
        self.line.setFrameShadow(standard.compat.Sunken)
        self.line.setObjectName('line')
        self.verticalLayout.addWidget(self.line)
        self.progressBar = standard.compat.QtWidgets.QProgressBar(self.dockWidgetContents)
        self.progressBar.setProperty('value', 24)
        self.progressBar.setObjectName('progressBar')
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.menubar = standard.compat.QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(standard.compat.QtCore.QRect(0, 0, 1068, 29))
        self.menubar.setObjectName('menubar')
        self.menuMenu = standard.compat.QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName('menuMenu')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = standard.compat.QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        MainWindow.setStatusBar(self.statusbar)

        self.actionAction = standard.compat.QAction(MainWindow)
        self.actionAction.setObjectName('actionAction')
        self.actionAction_C = standard.compat.QAction(MainWindow)
        self.actionAction_C.setObjectName('actionAction_C')

        self.menuMenu.addAction(self.actionAction)
        self.menuMenu.addAction(self.actionAction_C)
        self.menubar.addAction(self.menuMenu.menuAction())
        standard.compat.QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        '''Retranslate our UI after initializing some of our base modules.'''

        _translate = standard.compat.QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'MainWindow'))
        self.menuMenu.setTitle(_translate('MainWindow', '&Menu'))
        self.actionAction.setText(_translate('MainWindow', '&Action'))
        self.actionAction_C.setText(_translate('MainWindow', 'Action &C'))

    def about(self):
        '''Load our Qt about window.'''
        standard.compat.QtWidgets.QMessageBox.aboutQt(self.centralwidget, 'About Menu')

    def critical(self):
        '''Launch a critical message box.'''
        standard.compat.QtWidgets.QMessageBox.critical(self.centralwidget, 'Error', 'Critical Error')


def main():
    'Application entry point'

    app, window = standard.shared.setup_app(
        standard.args, standard.unknown, standard.compat, style_class=standard.StandardIconStyle
    )

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('Custom standard icons.')

    # Add event triggers
    ui.actionAction.triggered.connect(ui.about)
    ui.actionAction_C.triggered.connect(ui.critical)

    standard.shared.set_stylesheet(standard.args, app, standard.compat)
    return standard.shared.exec_app(standard.args, app, window)


if __name__ == '__main__':
    sys.exit(main())
