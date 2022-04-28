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
import gc
import os
import random
import sys
import time

tests_dir = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(tests_dir)
dist = os.path.join(home, 'dist')

# Create our arguments.
parser = argparse.ArgumentParser(description='Configurations for the Qt5 application.')
parser.add_argument(
    '--widget',
    help='widget to test. can provide `all` to test all',
    default='all'
)
parser.add_argument(
    '--stylesheet',
    help='stylesheet name',
    default='native'
)
# Know working styles include:
#   1. Fusion
#   2. Windows
parser.add_argument(
    '--style',
    help='application style, which is different than the stylesheet',
    default='native'
)
parser.add_argument(
    '--font-size',
    help='font size for the application',
    type=float,
    default=-1
)
parser.add_argument(
    '--font-family',
    help='the font family'
)
parser.add_argument(
    '--width',
    help='the window width',
    type=int,
    default=1068,
)
parser.add_argument(
    '--height',
    help='the window height',
    type=int,
    default=824,
)
parser.add_argument(
    '--alignment',
    help='the layout alignment',
)
parser.add_argument(
    '--compress',
    help='add stretch on both sides',
    action='store_true',
)
parser.add_argument(
    '--scale',
    help='scale factor for the UI',
    type=float,
    default=1,
)
parser.add_argument(
    '--pyqt6',
    help='use PyQt6 rather than PyQt5.',
    action='store_true'
)
parser.add_argument(
    '--use-x11',
    help='force the use of x11 on compatible systems.',
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
    AlignTop = QtCore.Qt.AlignmentFlag.AlignTop
    AlignVCenter = QtCore.Qt.AlignmentFlag.AlignVCenter
    AlignBottom = QtCore.Qt.AlignmentFlag.AlignBottom
    AlignLeft = QtCore.Qt.AlignmentFlag.AlignLeft
    AlignHCenter = QtCore.Qt.AlignmentFlag.AlignHCenter
    AlignRight = QtCore.Qt.AlignmentFlag.AlignRight
    AlignCenter = QtCore.Qt.AlignmentFlag.AlignCenter
    Horizontal = QtCore.Qt.Orientation.Horizontal
    Vertical = QtCore.Qt.Orientation.Vertical
    ScrollBarAsNeeded = QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
    ReadOnly = QtCore.QFile.OpenModeFlag.ReadOnly
    Text = QtCore.QFile.OpenModeFlag.Text
    KeepAspectRatio = QtCore.Qt.AspectRatioMode.KeepAspectRatio
    MenuButtonPopup = QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup
    InstantPopup = QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup
    Checked = QtCore.Qt.CheckState.Checked
    Unchecked = QtCore.Qt.CheckState.Unchecked
    PartiallyChecked = QtCore.Qt.CheckState.PartiallyChecked
    ItemIsUserCheckable = QtCore.Qt.ItemFlag.ItemIsUserCheckable
    ItemIsUserTristate = QtCore.Qt.ItemFlag.ItemIsUserTristate
    LeftArrow = QtCore.Qt.ArrowType.LeftArrow
    RightArrow = QtCore.Qt.ArrowType.RightArrow
    UpArrow = QtCore.Qt.ArrowType.UpArrow
    DownArrow = QtCore.Qt.ArrowType.DownArrow
    TopToolBarArea = QtCore.Qt.ToolBarArea.TopToolBarArea
    LeftToolBarArea = QtCore.Qt.ToolBarArea.LeftToolBarArea
    LeftDockWidgetArea = QtCore.Qt.DockWidgetArea.LeftDockWidgetArea
    North = QtWidgets.QTabWidget.TabPosition.North
    West = QtWidgets.QTabWidget.TabPosition.West
    East = QtWidgets.QTabWidget.TabPosition.East
    South = QtWidgets.QTabWidget.TabPosition.South
    Ok = QtWidgets.QMessageBox.StandardButton.Ok
    Cancel = QtWidgets.QMessageBox.StandardButton.Cancel
    Close = QtWidgets.QMessageBox.StandardButton.Close
    Open = QtWidgets.QMessageBox.StandardButton.Open
    Reset = QtWidgets.QMessageBox.StandardButton.Reset
    Save = QtWidgets.QMessageBox.StandardButton.Save
    SaveAll = QtWidgets.QMessageBox.StandardButton.SaveAll
    RestoreDefaults = QtWidgets.QMessageBox.StandardButton.RestoreDefaults
    Yes = QtWidgets.QMessageBox.StandardButton.Yes
    Help = QtWidgets.QMessageBox.StandardButton.Help
    No = QtWidgets.QMessageBox.StandardButton.No
    Apply = QtWidgets.QMessageBox.StandardButton.Apply
    Discard = QtWidgets.QMessageBox.StandardButton.Discard
    Critical = QtWidgets.QMessageBox.Icon.Critical
    Information = QtWidgets.QMessageBox.Icon.Information
    NoIcon = QtWidgets.QMessageBox.Icon.NoIcon
    Question = QtWidgets.QMessageBox.Icon.Question
    Warning = QtWidgets.QMessageBox.Icon.Warning
    YesRole = QtWidgets.QDialogButtonBox.ButtonRole.YesRole
    DialogOk = QtWidgets.QDialogButtonBox.StandardButton.Ok
    DialogCancel = QtWidgets.QDialogButtonBox.StandardButton.Cancel
    DockWidgetClosable = QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable
    DockWidgetFloatable = QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable
    DockWidgetMovable = QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable
    AllDockWidgetFeatures = DockWidgetClosable | DockWidgetFloatable | DockWidgetMovable
    AnyFile = QtWidgets.QFileDialog.FileMode.AnyFile
    ExistingFile = QtWidgets.QFileDialog.FileMode.ExistingFile
    Directory = QtWidgets.QFileDialog.FileMode.Directory
    ExistingFiles = QtWidgets.QFileDialog.FileMode.ExistingFiles
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
    SP_DialogAbortButton = QtWidgets.QStyle.StandardPixmap.SP_DialogAbortButton
    SP_DialogApplyButton = QtWidgets.QStyle.StandardPixmap.SP_DialogApplyButton
    SP_DialogCancelButton = QtWidgets.QStyle.StandardPixmap.SP_DialogCancelButton
    SP_DialogCloseButton = QtWidgets.QStyle.StandardPixmap.SP_DialogCloseButton
    SP_DialogDiscardButton = QtWidgets.QStyle.StandardPixmap.SP_DialogDiscardButton
    SP_DialogHelpButton = QtWidgets.QStyle.StandardPixmap.SP_DialogHelpButton
    SP_DialogIgnoreButton = QtWidgets.QStyle.StandardPixmap.SP_DialogIgnoreButton
    SP_DialogNoButton = QtWidgets.QStyle.StandardPixmap.SP_DialogNoButton
    SP_DialogNoToAllButton = QtWidgets.QStyle.StandardPixmap.SP_DialogNoToAllButton
    SP_DialogOkButton = QtWidgets.QStyle.StandardPixmap.SP_DialogOkButton
    SP_DialogOpenButton = QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton
    SP_DialogResetButton = QtWidgets.QStyle.StandardPixmap.SP_DialogResetButton
    SP_DialogRetryButton = QtWidgets.QStyle.StandardPixmap.SP_DialogRetryButton
    SP_DialogSaveAllButton = QtWidgets.QStyle.StandardPixmap.SP_DialogSaveAllButton
    SP_DialogSaveButton = QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton
    SP_DialogYesButton = QtWidgets.QStyle.StandardPixmap.SP_DialogYesButton
    SP_DialogYesToAllButton = QtWidgets.QStyle.StandardPixmap.SP_DialogYesToAllButton
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
    SP_LineEditClearButton = QtWidgets.QStyle.StandardPixmap.SP_LineEditClearButton
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
    SP_RestoreDefaultsButton = QtWidgets.QStyle.StandardPixmap.SP_RestoreDefaultsButton
    SP_TabCloseButton = QtWidgets.QStyle.StandardPixmap.SP_TabCloseButton
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
    AlignTop = QtCore.Qt.AlignTop
    AlignVCenter = QtCore.Qt.AlignVCenter
    AlignBottom = QtCore.Qt.AlignBottom
    AlignLeft = QtCore.Qt.AlignLeft
    AlignHCenter = QtCore.Qt.AlignHCenter
    AlignRight = QtCore.Qt.AlignRight
    AlignCenter = QtCore.Qt.AlignCenter
    Horizontal = QtCore.Qt.Horizontal
    Vertical = QtCore.Qt.Vertical
    ScrollBarAsNeeded = QtCore.Qt.ScrollBarAsNeeded
    ReadOnly = QtCore.QFile.ReadOnly
    Text = QtCore.QFile.Text
    KeepAspectRatio = QtCore.Qt.KeepAspectRatio
    MenuButtonPopup = QtWidgets.QToolButton.MenuButtonPopup
    InstantPopup = QtWidgets.QToolButton.InstantPopup
    Checked = QtCore.Qt.Checked
    Unchecked = QtCore.Qt.Unchecked
    PartiallyChecked = QtCore.Qt.PartiallyChecked
    ItemIsUserCheckable = QtCore.Qt.ItemIsUserCheckable
    ItemIsUserTristate = QtCore.Qt.ItemIsUserTristate
    LeftArrow = QtCore.Qt.LeftArrow
    RightArrow = QtCore.Qt.RightArrow
    UpArrow = QtCore.Qt.UpArrow
    DownArrow = QtCore.Qt.DownArrow
    TopToolBarArea = QtCore.Qt.TopToolBarArea
    LeftToolBarArea = QtCore.Qt.LeftToolBarArea
    LeftDockWidgetArea = QtCore.Qt.LeftDockWidgetArea
    North = QtWidgets.QTabWidget.North
    West = QtWidgets.QTabWidget.West
    East = QtWidgets.QTabWidget.East
    South = QtWidgets.QTabWidget.South
    Ok = QtWidgets.QMessageBox.Ok
    Cancel = QtWidgets.QMessageBox.Cancel
    Close = QtWidgets.QMessageBox.Close
    Open = QtWidgets.QMessageBox.Open
    Reset = QtWidgets.QMessageBox.Reset
    Save = QtWidgets.QMessageBox.Save
    SaveAll = QtWidgets.QMessageBox.SaveAll
    RestoreDefaults = QtWidgets.QMessageBox.RestoreDefaults
    Yes = QtWidgets.QMessageBox.Yes
    Help = QtWidgets.QMessageBox.Help
    No = QtWidgets.QMessageBox.No
    Apply = QtWidgets.QMessageBox.Apply
    Discard = QtWidgets.QMessageBox.Discard
    Critical = QtWidgets.QMessageBox.Critical
    Information = QtWidgets.QMessageBox.Information
    NoIcon = QtWidgets.QMessageBox.NoIcon
    Question = QtWidgets.QMessageBox.Question
    Warning = QtWidgets.QMessageBox.Warning
    YesRole = QtWidgets.QDialogButtonBox.YesRole
    DialogOk = QtWidgets.QDialogButtonBox.Ok
    DialogCancel = QtWidgets.QDialogButtonBox.Cancel
    AllDockWidgetFeatures = QtWidgets.QDockWidget.AllDockWidgetFeatures
    AnyFile = QtWidgets.QFileDialog.AnyFile
    ExistingFile = QtWidgets.QFileDialog.ExistingFile
    Directory = QtWidgets.QFileDialog.Directory
    ExistingFiles = QtWidgets.QFileDialog.ExistingFiles
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
    SP_DialogAbortButton = QtWidgets.QStyle.SP_DialogAbortButton
    SP_DialogApplyButton = QtWidgets.QStyle.SP_DialogApplyButton
    SP_DialogCancelButton = QtWidgets.QStyle.SP_DialogCancelButton
    SP_DialogCloseButton = QtWidgets.QStyle.SP_DialogCloseButton
    SP_DialogDiscardButton = QtWidgets.QStyle.SP_DialogDiscardButton
    SP_DialogHelpButton = QtWidgets.QStyle.SP_DialogHelpButton
    SP_DialogIgnoreButton = QtWidgets.QStyle.SP_DialogIgnoreButton
    SP_DialogNoButton = QtWidgets.QStyle.SP_DialogNoButton
    SP_DialogNoToAllButton = QtWidgets.QStyle.SP_DialogNoToAllButton
    SP_DialogOkButton = QtWidgets.QStyle.SP_DialogOkButton
    SP_DialogOpenButton = QtWidgets.QStyle.SP_DialogOpenButton
    SP_DialogResetButton = QtWidgets.QStyle.SP_DialogResetButton
    SP_DialogRetryButton = QtWidgets.QStyle.SP_DialogRetryButton
    SP_DialogSaveAllButton = QtWidgets.QStyle.SP_DialogSaveAllButton
    SP_DialogSaveButton = QtWidgets.QStyle.SP_DialogSaveButton
    SP_DialogYesButton = QtWidgets.QStyle.SP_DialogYesButton
    SP_DialogYesToAllButton = QtWidgets.QStyle.SP_DialogYesToAllButton
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
    SP_LineEditClearButton = QtWidgets.QStyle.SP_LineEditClearButton
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
    SP_RestoreDefaultsButton = QtWidgets.QStyle.SP_RestoreDefaultsButton
    SP_TabCloseButton = QtWidgets.QStyle.SP_TabCloseButton
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

layout = {
    'vertical': QtWidgets.QVBoxLayout,
    'horizontal': QtWidgets.QHBoxLayout,
}

alignment = {
    'top': AlignTop,
    'vcenter': AlignVCenter,
    'bottom': AlignBottom,
    'left': AlignLeft,
    'hcenter': AlignHCenter,
    'right': AlignRight,
    'center': AlignCenter,
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

def splash_timer(splash, window):
    '''Non-block timer for a splashscreen.'''

    splash.finish(window)
    window.show()

def execute(obj):
    '''Execute Qt object, wrapper for PyQt5 and PyQt6.'''

    if args.pyqt6:
        return obj.exec()
    else:
        return obj.exec_()

def close_icon(widget):
    '''Get the close icon depending on the stylesheet.'''

    if args.stylesheet == 'native':
        return widget.style().standardIcon(SP_DockWidgetCloseButton)
    return QtGui.QIcon(f'{resource_format}close.svg')

def test_progressbar_horizontal(widget, *_):
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

    return child

def test_progressbar_vertical(widget, *_):
    layout_type = 'horizontal'
    child = []
    bar1 = QtWidgets.QProgressBar(widget)
    bar1.setOrientation(Vertical)
    bar1.setProperty('value', 0)
    child.append(bar1)
    bar2 = QtWidgets.QProgressBar(widget)
    bar2.setOrientation(Vertical)
    bar2.setProperty('value', 24)
    child.append(bar2)
    bar3 = QtWidgets.QProgressBar(widget)
    bar3.setOrientation(Vertical)
    bar3.setProperty('value', 99)
    child.append(bar3)
    bar4 = QtWidgets.QProgressBar(widget)
    bar4.setOrientation(Vertical)
    bar4.setProperty('value', 100)
    child.append(bar4)

    return child, layout_type

def test_slider_horizontal(widget, *_):
    child = QtWidgets.QSlider(widget)
    child.setOrientation(Horizontal)

    return child

def test_slider_vertical(widget, *_):
    layout_type = 'horizontal'
    child = QtWidgets.QSlider(widget)
    child.setOrientation(Vertical)

    return child, layout_type

def test_splitter_horizontal(widget, *_):
    child = QtWidgets.QSplitter(widget)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())

    return child

def test_splitter_vertical(widget, *_):
    layout_type = 'horizontal'
    child = QtWidgets.QSplitter(widget)
    child.setOrientation(Vertical)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())

    return child, layout_type

def test_menu(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addAction(QAction('&Action 1', window))
    menu.addAction(QAction('&Action 2', window))
    submenu = QtWidgets.QMenu('Sub Menu', menu)
    submenu.addAction(QAction('&Action 3', window))
    action1 = QAction('&Action 4', window)
    action1.setCheckable(True)
    submenu.addAction(action1)
    menu.addAction(submenu.menuAction())
    action2 = QAction('&Action 5', window)
    action2.setCheckable(True)
    action2.setChecked(True)
    menu.addSeparator()
    menu.addAction(action2)
    action3 = QAction('&Action 6', window)
    action3.setCheckable(True)
    menu.addAction(action3)
    icon = close_icon(menu)
    menu.addAction(QAction(icon, '&Action 7', window))
    menu.addAction(QAction(icon, '&Action 8', window))
    submenu.addAction(QAction(icon, '&Action 9', window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return child

def test_statusbar(_, window, *__):
    child = QtWidgets.QStatusBar(window)
    window.setStatusBar(child)

    return child

def test_spinbox(widget, *_):
    layout_type = 'horizontal'
    child = []
    spin1 = QtWidgets.QSpinBox(widget)
    spin1.setValue(10)
    child.append(spin1)
    spin2 = QtWidgets.QSpinBox(widget)
    spin2.setValue(10)
    spin2.setEnabled(False)
    child.append(spin2)

    return child, layout_type

def test_double_spinbox(widget, *_):
    layout_type = 'horizontal'
    child = []
    spin1 = QtWidgets.QDoubleSpinBox(widget)
    spin1.setValue(10.5)
    child.append(spin1)
    spin2 = QtWidgets.QDoubleSpinBox(widget)
    spin2.setValue(10.5)
    spin2.setEnabled(False)
    child.append(spin2)

    return child, layout_type

def test_combobox(widget, *_):
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
    combo3 = QtWidgets.QComboBox(widget)
    combo3.setEditable(True)
    combo3.addItem('Edit 1')
    combo3.addItem('Edit 2')
    child.append(combo3)

    return child, layout_type

def _test_tabwidget(widget, position):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(position)
    child.addTab(QtWidgets.QWidget(), 'Tab 1')
    child.addTab(QtWidgets.QWidget(), 'Tab 2')
    child.addTab(QtWidgets.QWidget(), 'Tab 3')

    return child

def test_tabwidget_top(widget, *_):
    return _test_tabwidget(widget, North)

def test_tabwidget_left(widget, *_):
    return _test_tabwidget(widget, West)

def test_tabwidget_right(widget, *_):
    return _test_tabwidget(widget, East)

def test_tabwidget_bottom(widget, *_):
    return _test_tabwidget(widget, South)

def test_closable_tabwidget_top(widget, *_):
    child = _test_tabwidget(widget, North)
    child.setTabsClosable(True)

    return child

def test_closable_tabwidget_right(widget, *_):
    child = _test_tabwidget(widget, East)
    child.setTabsClosable(True)

    return child

def test_dock(_, window, *__):
    dock1 = QtWidgets.QDockWidget('&Dock widget 1', window)
    dock1.setFeatures(AllDockWidgetFeatures)
    dock2 = QtWidgets.QDockWidget('&Dock widget 2', window)
    dock2.setFeatures(AllDockWidgetFeatures)
    window.addDockWidget(LeftDockWidgetArea, dock1)
    window.addDockWidget(LeftDockWidgetArea, dock2)
    window.tabifyDockWidget(dock1, dock2)

def test_radio(widget, *_):
    child = []
    widget_type = QtWidgets.QRadioButton
    child.append(abstract_button(widget_type, widget))
    child.append(abstract_button(widget_type, widget, checked=True))
    child.append(abstract_button(widget_type, widget, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=True, enabled=False))
    child.append(abstract_button(widget_type, widget, 'With Text'))

    return child

def test_checkbox(widget, _, __, ___, ____, app):
    child = []
    widget_type = QtWidgets.QCheckBox
    child.append(abstract_button(widget_type, widget))
    child.append(abstract_button(widget_type, widget, checked=True))
    child.append(abstract_button(widget_type, widget, checked=PartiallyChecked))
    child.append(abstract_button(widget_type, widget, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=True, enabled=False))
    child.append(abstract_button(widget_type, widget, checked=PartiallyChecked, enabled=False))
    child.append(abstract_button(widget_type, widget, 'With Text'))
    child.append(abstract_button(widget_type, widget, 'With Large Text'))
    checkbox_font = app.font()
    checkbox_font.setPointSizeF(50.0)
    child[-1].setFont(checkbox_font)

    return child

def test_table(widget, *_):
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

    return child

def test_sortable_table(widget, *_):
    child = test_table(widget)
    child.setSortingEnabled(True)

    return child

def test_list(widget, *_):
    alignments = [AlignLeft, AlignRight, AlignHCenter]
    child = QtWidgets.QListWidget(widget)
    for index in range(10):
        item = QtWidgets.QListWidgetItem(f'Item {index + 1}')
        item.setTextAlignment(random.choice(alignments))
        child.addItem(item)
    icon = close_icon(child)
    for index in range(10):
        item = QtWidgets.QListWidgetItem(icon, f'Item {index + 1}')
        item.setTextAlignment(random.choice(alignments))
        child.addItem(item)

    return child

def test_scrollbar_vertical(widget, *_):
    child = QtWidgets.QListWidget(widget)
    for index in range(100):
        child.addItem(QtWidgets.QListWidgetItem(f'Item {index + 1}'))

    return child

def test_scrollbar_horizontal(widget, *_):
    child = QtWidgets.QTableWidget(widget)
    child.setColumnCount(100)
    child.setRowCount(1)
    item = QtWidgets.QTableWidgetItem(f'Row 1')
    child.setVerticalHeaderItem(0, item)
    for index in range(100):
        item = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
        child.setHorizontalHeaderItem(index, item)

    return child

def test_toolbar(_, window, *__):
    toolbar1 = QtWidgets.QToolBar('Toolbar')
    toolbar1.addAction('&Action 1')
    toolbar1.addAction('&Action 2')
    toolbar1.addSeparator()
    toolbar1.addAction('&Action 3')
    toolbar1.addAction('&Action 3 Really Long Name')
    icon = close_icon(toolbar1)
    toolbar1.addAction(icon, '&Action 4')
    window.addToolBar(TopToolBarArea, toolbar1)

    toolbar2 = QtWidgets.QToolBar('Toolbar')
    toolbar2.setOrientation(Vertical)
    toolbar2.addAction('&Action 1')
    toolbar2.addAction('&Action 2')
    toolbar2.addSeparator()
    toolbar2.addAction('&Action 3')
    toolbar2.addAction('&Action 3 Really Long Name')
    icon = close_icon(toolbar2)
    toolbar2.addAction(icon, '&Action 4')
    window.addToolBar(LeftToolBarArea, toolbar2)

    return None, None

def test_toolbutton(widget, window, *_):
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
        QAction('&Action 5', window),
        QAction('&Action 6', window),
    ])
    child[2].setPopupMode(MenuButtonPopup)
    child[2].addActions([
        QAction('&Action 9', window),
        QAction('&Action 10', window),
    ])
    child[3].setPopupMode(InstantPopup)
    child[3].addActions([
        QAction('&Action 11', window),
        QAction('&Action 12', window),
    ])
    child[4].setArrowType(LeftArrow)
    child[5].setArrowType(RightArrow)
    child[6].setArrowType(UpArrow)
    child[7].setArrowType(DownArrow)
    icon = close_icon(widget)
    child[8].setIcon(icon)

    return child, layout_type

def test_pushbutton(widget, *_):
    layout_type = 'horizontal'
    child = []
    widget_type = QtWidgets.QPushButton
    child.append(abstract_button(widget_type, widget, 'Button 1', checked=True))
    child.append(abstract_button(widget_type, widget, 'Button 2', enabled=False))
    child.append(abstract_button(widget_type, widget, 'Button 3', checkable=False))
    icon = close_icon(widget)
    child.append(abstract_button(widget_type, widget, icon, 'Button 4', checkable=False))

    return child, layout_type

def test_tree(widget, *_):
    child = []
    tree1 = QtWidgets.QTreeWidget(widget)
    tree1.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree1, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree1, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])
    item3.setFlags(item3.flags() | ItemIsUserCheckable)
    item3.setCheckState(0, Unchecked)
    item4 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.2'])
    item5 = QtWidgets.QTreeWidgetItem(item4, ['Row 2.2.1'])
    item6 = QtWidgets.QTreeWidgetItem(item5, ['Row 2.2.1.1'])
    item7 = QtWidgets.QTreeWidgetItem(item5, ['Row 2.2.1.2'])
    item7.setFlags(item7.flags() | ItemIsUserCheckable)
    item7.setCheckState(0, Checked)
    item8 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.3'])
    item8.setFlags(item8.flags() | ItemIsUserTristate)
    item8.setCheckState(0, PartiallyChecked)
    item9 = QtWidgets.QTreeWidgetItem(tree1, ['Row 3'])
    item10 = QtWidgets.QTreeWidgetItem(item9, ['Row 3.1'])
    item11 = QtWidgets.QTreeWidgetItem(tree1, ['Row 4'])
    child.append(tree1)
    tree2 = QtWidgets.QTreeWidget(widget)
    tree2.setHeaderLabel('Tree 2')
    tree2.header().setSectionsClickable(True)
    item12 = QtWidgets.QTreeWidgetItem(tree2, ['Row 1', 'Column 2', 'Column 3'])
    child.append(tree2)

    return child

def test_view_scrollarea(widget, *_):
    # For us to have both scrollbars visible.
    child = QtWidgets.QTableWidget(widget)
    child.setColumnCount(100)
    child.setRowCount(100)
    for index in range(100):
        row = QtWidgets.QTableWidgetItem(f'Row {index + 1}')
        child.setVerticalHeaderItem(0, row)
        column = QtWidgets.QTableWidgetItem(f'Column {index + 1}')
        child.setHorizontalHeaderItem(index, column)

    return child

def test_widget_scrollarea(widget, window, *_):
    child = QtWidgets.QProgressBar(widget)
    child.setProperty('value', 24)
    window.resize(30, 30)

    return child

def test_frame(widget, *_):
    child = []
    text = QtWidgets.QTextEdit()
    text.setPlainText('Hello world\nTesting lines')
    child.append(text)
    table = QtWidgets.QTableWidget()
    table.setColumnCount(5)
    table.setRowCount(5)
    child.append(table)

    return child

def test_groupbox(widget, *_):
    child = []
    child.append(QtWidgets.QGroupBox('Groupbox 1', widget))
    checkable = QtWidgets.QGroupBox('Groupbox 2', widget)
    checkable.setCheckable(True)
    child.append(checkable)
    vbox = QtWidgets.QVBoxLayout(checkable)
    vbox.setAlignment(AlignHCenter)
    vbox.addWidget(QtWidgets.QLineEdit('Sample Label'))

    return child

def test_toolbox(widget, *_):
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

    return child

def test_menubutton(widget, window, *_):
    child = QtWidgets.QToolButton(widget)
    child.setText('Menu Toolbutton')
    child.setPopupMode(MenuButtonPopup)
    child.addActions([
        QAction('&Action 9', window),
        QAction('&Action 10', window),
    ])

    return child

def test_tooltip(widget, *_):
    child = QtWidgets.QPushButton('Sample Label')
    child.setToolTip('Sample Tooltip')

    return child

def test_splashscreen(_, window, __, ___, ____, app):
    pixmap = QtGui.QPixmap('assets/Yellowstone.jpg')
    size = app.screens()[0].size()
    scaled = pixmap.scaled(size, KeepAspectRatio)
    splash = QtWidgets.QSplashScreen(scaled)
    splash.show()
    QtCore.QTimer.singleShot(2000, lambda: splash_timer(splash, window))

    return None, None, False

def test_calendar(widget, *_):
    child = QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(True)

    return child

def _test_standard_button(window, app, button):
    message = QtWidgets.QMessageBox(window)
    message.addButton(button)
    execute(message)

def test_ok_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Ok)
    return None, None, False, True

def test_cancel_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Cancel)
    return None, None, False, True

def test_close_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Close)
    return None, None, False, True

def test_open_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Open)
    return None, None, False, True

def test_reset_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Reset)
    return None, None, False, True

def test_save_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Save)
    return None, None, False, True

def test_saveall_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, SaveAll)
    return None, None, False, True

def test_restoredefaults_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, RestoreDefaults)
    return None, None, False, True

def test_yes_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Yes)
    return None, None, False, True

def test_help_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Help)
    return None, None, False, True

def test_no_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, No)
    return None, None, False, True

def test_apply_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Apply)
    return None, None, False, True

def test_discard_button(_, window, __, ___, ____, app):
    _test_standard_button(window, app, Discard)
    return None, None, False, True

def _test_standard_icon(window, app, icon):
    message = QtWidgets.QMessageBox(window)
    message.setIcon(icon)
    execute(message)

def test_critical_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, Critical)
    return None, None, False, True

def test_info_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, Information)
    return None, None, False, True

def test_no_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, NoIcon)
    return None, None, False, True

def test_question_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, Question)
    return None, None, False, True

def test_warning_icon(_, window, __, ___, ____, app):
    _test_standard_icon(window, app, Warning)
    return None, None, False, True

def test_multiple_buttons(widget, *_):
    child = []
    child.append(QtWidgets.QTextEdit(widget))
    container = QtWidgets.QWidget(widget)
    hbox = QtWidgets.QHBoxLayout(container)
    hbox.addWidget(QtWidgets.QPushButton('Delete'))
    hbox.addWidget(QtWidgets.QPushButton('Complete'))
    child.append(container)
    child.append(QtWidgets.QLineEdit(widget))
    dialog = QtWidgets.QDialogButtonBox(Horizontal, widget)
    dialog.addButton('Yes', YesRole)
    dialog.addButton('Really really really long', YesRole)
    dialog.addButton(DialogOk)
    dialog.addButton(DialogCancel)
    child.append(dialog)

    return child

def test_disabled_menu(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addAction(QAction('&Action 1', window))
    menu.addAction(QAction('&Action 2', window))
    submenu = QtWidgets.QMenu('Sub Menu', menu)
    submenu.addAction(QAction('&Action 3', window))
    action1 = QAction('&Action 4', window)
    action1.setCheckable(True)
    action1.setEnabled(False)
    submenu.addAction(action1)
    menu.addAction(submenu.menuAction())
    action2 = QAction('&Action 5', window)
    action2.setCheckable(True)
    action2.setChecked(True)
    menu.addSeparator()
    menu.addAction(action2)
    action3 = QAction('&Action 6', window)
    action3.setCheckable(True)
    menu.addAction(action3)
    icon = close_icon(menu)
    menu.addAction(QAction(icon, '&Action 7', window))
    menu.addAction(QAction(icon, '&Action 8', window))
    menu.actions()[2].setEnabled(False)
    submenu.addAction(QAction(icon, '&Action 9', window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return child

def test_disabled_menubar(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setEnabled(False)

    return child

def test_issue25(widget, window, font, width, *_):

    def launch_filedialog(folder):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(Directory)
        if execute(dialog):
            folder.setText(dialog.selectedFiles()[0])

    def launch_fontdialog(value):
        initial = QtGui.QFont()
        initial.setFamily(value.text())
        font, ok = QtWidgets.QFontDialog.getFont(initial)
        if ok:
            value.setText(font.family())

    # Attempt to recreate the UI present here:
    #   https://github.com/Alexhuszagh/BreezeStyleSheets/issues/25#issue-1187193418
    dialog = QtWidgets.QDialog(window)
    dialog.resize(args.width // 2, args.height // 2)

    # Add the QTabWidget
    child = QtWidgets.QTabWidget(dialog)
    child.setTabPosition(North)
    general = QtWidgets.QWidget()
    child.addTab(general, 'General')
    child.addTab(QtWidgets.QWidget(), 'Colors')
    layout = QtWidgets.QVBoxLayout(general)
    layout.setAlignment(AlignVCenter)

    # Add the data folder hboxlayout
    data = QtWidgets.QWidget()
    layout.addWidget(data)
    data_layout = QtWidgets.QHBoxLayout(data)
    data_layout.addWidget(QtWidgets.QLabel('Data Folder'))
    data_folder = QtWidgets.QLineEdit('Data')
    data_layout.addWidget(data_folder)
    file_dialog = QtWidgets.QPushButton('...', checkable=False)
    data_layout.addWidget(file_dialog)
    file_dialog.clicked.connect(lambda _: launch_filedialog(data_folder))

    # Add the "Show Grid" QCheckbox.
    checkbox = QtWidgets.QCheckBox
    layout.addWidget(abstract_button(checkbox, general, 'Show grid'))

    # Grid square size.
    grid_size = QtWidgets.QWidget()
    layout.addWidget(grid_size)
    grid_size_layout = QtWidgets.QHBoxLayout(grid_size)
    grid_size_layout.addWidget(QtWidgets.QLabel('Grid Square Size'))
    spin = QtWidgets.QSpinBox(grid_size)
    spin.setValue(16)
    grid_size_layout.addWidget(spin)

    # Add units of measurement
    units = QtWidgets.QWidget()
    layout.addWidget(units)
    units_layout = QtWidgets.QHBoxLayout(units)
    units_layout.addWidget(QtWidgets.QLabel('Default length unit of measurement'))
    units_combo = QtWidgets.QComboBox()
    units_combo.addItem('Inches')
    units_combo.addItem('Foot')
    units_combo.addItem('Meter')
    units_layout.addWidget(units_combo)

    # Add default font.
    font = QtWidgets.QWidget()
    layout.addWidget(font)
    font_layout = QtWidgets.QHBoxLayout(font)
    font_layout.addWidget(QtWidgets.QLabel('Default Font'))
    font_value = QtWidgets.QLineEdit('Abcdef')
    font_layout.addWidget(font_value)
    font_dialog = QtWidgets.QPushButton('...', checkable=False)
    font_layout.addWidget(font_dialog)
    font_dialog.clicked.connect(lambda _: launch_fontdialog(font_value))
    font_layout.addStretch(1)

    # Add the alignment options
    alignment = QtWidgets.QWidget()
    layout.addWidget(alignment)
    alignment_layout = QtWidgets.QHBoxLayout(alignment)
    align_combo = QtWidgets.QComboBox()
    align_combo.addItem('Align Top')
    align_combo.addItem('Align Bottom')
    align_combo.addItem('Align Left')
    align_combo.addItem('Align Right')
    align_combo.addItem('Align Center')
    alignment_layout.addWidget(align_combo)
    alignment_layout.addWidget(abstract_button(checkbox, general, 'Word Wrap'))
    alignment_layout.addStretch(1)

    # Add item label font
    item_label = QtWidgets.QWidget()
    layout.addWidget(item_label)
    item_label_layout = QtWidgets.QHBoxLayout(item_label)
    item_label_layout.addWidget(QtWidgets.QLabel('Item Label Font'))
    item_label_value = QtWidgets.QLineEdit('Abcdef')
    item_label_layout.addWidget(item_label_value)
    item_label_dialog = QtWidgets.QPushButton('...', checkable=False)
    item_label_layout.addWidget(item_label_dialog)
    item_label_dialog.clicked.connect(lambda _: launch_fontdialog(item_label_value))
    item_label_layout.addStretch(1)

    # Need to add the Ok/Cancel standard buttons.
    dialog_box = QtWidgets.QDialogButtonBox(Horizontal, general)
    layout.addWidget(dialog_box)
    dialog_box.addButton(DialogOk)
    dialog_box.addButton(DialogCancel)

    execute(dialog)

    return None, None, False, True

def test_issue28(_, window, *__):
    dialog = QtWidgets.QFileDialog(window)
    dialog.setFileMode(Directory)
    execute(dialog)

    return None, None, False, True


def test(args, qtargv, test_widget):
    '''Test a single widget.'''

    app = QtWidgets.QApplication(qtargv)

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

    # Setup the main window.
    window = QtWidgets.QMainWindow()
    window.setWindowTitle('Sample single widget application.')
    window.resize(args.width, args.height)
    widget = QtWidgets.QWidget()
    scroll = QtWidgets.QScrollArea()
    scroll.setHorizontalScrollBarPolicy(ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(ScrollBarAsNeeded)
    scroll.setWidgetResizable(True)

    # Get the correct parameters for our test widget.
    try:
        function = globals()[f'test_{test_widget}']
    except KeyError:
        raise NotImplementedError(f'test for {test_widget} not implemented')
    result = function(widget, window, font, args.width, args.height, app)
    child = []
    layout_type = 'vertical'
    show_window = True
    quit = False
    if result and isinstance(result, list):
        # Have a single value passed as a list
        child = result
    elif isinstance(result, tuple):
        child = result[0]
    else:
        child = result
    if isinstance(result, tuple) and len(result) >= 2:
        layout_type = result[1]
    if isinstance(result, tuple) and len(result) >= 3:
        show_window = result[2]
    if isinstance(result, tuple) and len(result) >= 4:
        quit = result[3]

    # Add the widgets to the layout.
    if layout_type is not None and child is not None:
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
    if show_window:
        window.show()
    if quit:
        return app.quit()
    return execute(app)

def main():
    'Application entry point'

    # Disable garbage collection to avoid runtime errors.
    gc.disable()
    os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    if args.style != 'native':
        style = QtWidgets.QStyleFactory.create(args.style)
        QtWidgets.QApplication.setStyle(style)
    if args.widget == 'all':
        all_tests = [i for i in globals().keys() if i.startswith('test_')]
        all_widgets = [i[len('test_'):] for i in all_tests]
        for widget in all_widgets:
            test(args, sys.argv[:1] + unknown, widget)
            gc.collect()
    else:
        test(args, sys.argv[:1] + unknown, args.widget)

    return 0

if __name__ == '__main__':
    sys.exit(main())
