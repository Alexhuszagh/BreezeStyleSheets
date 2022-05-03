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
    SP_DirLinkOpenIcon = QtWidgets.QStyle.StandardPixmap.SP_DirLinkOpenIcon
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
    SP_LineEditClearButton = QtWidgets.QStyle.StandardPixmap.SP_LineEditClearButton
    SP_DialogYesToAllButton = QtWidgets.QStyle.StandardPixmap.SP_DialogYesToAllButton
    SP_DialogNoToAllButton = QtWidgets.QStyle.StandardPixmap.SP_DialogNoToAllButton
    SP_DialogSaveAllButton = QtWidgets.QStyle.StandardPixmap.SP_DialogSaveAllButton
    SP_DialogAbortButton = QtWidgets.QStyle.StandardPixmap.SP_DialogAbortButton
    SP_DialogRetryButton = QtWidgets.QStyle.StandardPixmap.SP_DialogRetryButton
    SP_DialogIgnoreButton = QtWidgets.QStyle.StandardPixmap.SP_DialogIgnoreButton
    SP_RestoreDefaultsButton = QtWidgets.QStyle.StandardPixmap.SP_RestoreDefaultsButton
    if QtCore.QT_VERSION >= 393984:
        SP_TabCloseButton = QtWidgets.QStyle.StandardPixmap.SP_TabCloseButton
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
    SP_DirLinkOpenIcon = QtWidgets.QStyle.SP_DirLinkOpenIcon
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
    SP_LineEditClearButton = QtWidgets.QStyle.SP_LineEditClearButton
    SP_DialogYesToAllButton = QtWidgets.QStyle.SP_DialogYesToAllButton
    SP_DialogNoToAllButton = QtWidgets.QStyle.SP_DialogNoToAllButton
    SP_DialogSaveAllButton = QtWidgets.QStyle.SP_DialogSaveAllButton
    SP_DialogAbortButton = QtWidgets.QStyle.SP_DialogAbortButton
    SP_DialogRetryButton = QtWidgets.QStyle.SP_DialogRetryButton
    SP_DialogIgnoreButton = QtWidgets.QStyle.SP_DialogIgnoreButton
    SP_RestoreDefaultsButton = QtWidgets.QStyle.SP_RestoreDefaultsButton
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

ICON_MAP = {
    SP_TitleBarMinButton: 'minimize.svg',
    SP_TitleBarMenuButton: 'menu.svg',
    SP_TitleBarMaxButton: 'maximize.svg',
    SP_TitleBarCloseButton: 'window_close.svg',
    SP_TitleBarNormalButton: 'restore.svg',
    SP_TitleBarShadeButton: 'shade.svg',
    SP_TitleBarUnshadeButton: 'unshade.svg',
    SP_TitleBarContextHelpButton: 'help.svg',
    SP_MessageBoxInformation: 'message_information.svg',
    SP_MessageBoxWarning: 'message_warning.svg',
    SP_MessageBoxCritical: 'message_critical.svg',
    SP_MessageBoxQuestion: 'message_question.svg',
    SP_DesktopIcon: 'desktop.svg',
    SP_TrashIcon: 'trash.svg',
    SP_ComputerIcon: 'computer.svg',
    SP_DriveFDIcon: 'floppy_drive.svg',
    SP_DriveHDIcon: 'hard_drive.svg',
    SP_DriveCDIcon: 'disc_drive.svg',
    SP_DriveDVDIcon: 'disc_drive.svg',
    SP_DriveNetIcon: 'network_drive.svg',
    SP_DirHomeIcon: 'home_directory.svg',
    SP_DirOpenIcon: 'folder_open.svg',
    SP_DirClosedIcon: 'folder.svg',
    SP_DirIcon: 'folder.svg',
    SP_DirLinkIcon: 'folder_link.svg',
    SP_DirLinkOpenIcon: 'folder_open_link.svg',
    SP_FileIcon: 'file.svg',
    SP_FileLinkIcon: 'file_link.svg',
    SP_FileDialogStart: 'file_dialog_start.svg',
    SP_FileDialogEnd: 'file_dialog_end.svg',
    SP_FileDialogToParent: 'up_arrow.svg',
    SP_FileDialogNewFolder: 'folder.svg',
    SP_FileDialogDetailedView: 'file_dialog_detailed.svg',
    SP_FileDialogInfoView: 'file_dialog_info.svg',
    SP_FileDialogContentsView: 'file_dialog_contents.svg',
    SP_FileDialogListView: 'file_dialog_list.svg',
    SP_FileDialogBack: 'left_arrow.svg',
    SP_DockWidgetCloseButton: 'close.svg',
    SP_ToolBarHorizontalExtensionButton: 'horizontal_extension.svg',
    SP_ToolBarVerticalExtensionButton: 'vertical_extension.svg',
    SP_DialogOkButton: 'dialog_ok.svg',
    SP_DialogCancelButton: 'dialog_cancel.svg',
    SP_DialogHelpButton: 'dialog_help.svg',
    SP_DialogOpenButton: 'dialog_open.svg',
    SP_DialogSaveButton: 'dialog_save.svg',
    SP_DialogCloseButton: 'dialog_close.svg',
    SP_DialogApplyButton: 'dialog_apply.svg',
    SP_DialogResetButton: 'dialog_reset.svg',
    SP_DialogDiscardButton: 'dialog_discard.svg',
    SP_DialogYesButton: 'dialog_apply.svg',
    SP_DialogNoButton: 'dialog_no.svg',
    SP_ArrowUp: 'up_arrow.svg',
    SP_ArrowDown: 'down_arrow.svg',
    SP_ArrowLeft: 'left_arrow.svg',
    SP_ArrowRight: 'right_arrow.svg',
    SP_ArrowBack: 'left_arrow.svg',
    SP_ArrowForward: 'right_arrow.svg',
    SP_CommandLink: 'right_arrow.svg',
    SP_VistaShield: 'vista_shield.svg',
    SP_BrowserReload: 'browser_refresh.svg',
    SP_BrowserStop: 'browser_refresh_stop.svg',
    SP_MediaPlay: 'play.svg',
    SP_MediaStop: 'stop.svg',
    SP_MediaPause: 'pause.svg',
    SP_MediaSkipForward: 'skip_backward.svg',
    SP_MediaSkipBackward: 'skip_forward.svg',
    SP_MediaSeekForward: 'seek_forward.svg',
    SP_MediaSeekBackward: 'seek_backward.svg',
    SP_MediaVolume: 'volume.svg',
    SP_MediaVolumeMuted: 'volume_muted.svg',
    SP_LineEditClearButton: 'clear_text.svg',
    SP_DialogYesToAllButton: 'dialog_yes_to_all.svg',
    SP_DialogNoToAllButton: 'dialog_no.svg',
    SP_DialogSaveAllButton: 'dialog_save_all.svg',
    SP_DialogAbortButton: 'dialog_cancel.svg',
    SP_DialogRetryButton: 'dialog_retry.svg',
    SP_DialogIgnoreButton: 'dialog_ignore.svg',
    SP_RestoreDefaultsButton: 'restore_defaults.svg',
}
if QtCore.QT_VERSION >= 393984:
    ICON_MAP[SP_TabCloseButton] = 'tab_close.svg'


def standard_icon(widget, name):
    '''Get the close icon depending on the stylesheet.'''
    return widget.style().standardIcon(name)


def native_icon(style, icon, option=None, widget=None):
    '''Get a standard icon for the native style'''
    return style.standardIcon(icon, option, widget)


def stylesheet_icon(style, icon, option=None, widget=None):
    '''Get a standard icon for the stylesheet style'''

    path = ICON_MAP[icon]
    resource = f'{resource_format}{path}'
    if QtCore.QFile.exists(resource):
        return QtGui.QIcon(resource)
    return QtWidgets.QCommonStyle.standardIcon(style, icon, option, widget)

def style_icon(style, icon, option=None, widget=None):
    if args.stylesheet == 'native':
        return native_icon(style, icon, option, widget)
    return stylesheet_icon(style, icon, option, widget)


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
    button.setIcon(standard_icon(button, icon))
    button.setObjectName(f'button{index}')
    layout.addWidget(button)


def add_standard_buttons(ui, page, icons):
    '''Create and add QToolButtons with standard icons to the UI.'''

    for icon_name in icons:
        icon = standard_icon(page, globals()[icon_name])
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
        self.layout.setAlignment(AlignHCenter)
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
    app = QtWidgets.QApplication(sys.argv[:1] + unknown)
    window = QtWidgets.QMainWindow()

    if args.style != 'native':
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
