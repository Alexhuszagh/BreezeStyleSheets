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
parser = argparse.ArgumentParser(description='Configurations for the Qt application.')
parser.add_argument(
    '--widget',
    help='widget to test. can provide `all` to test all widgets',
    default='all'
)
parser.add_argument(
    '--stylesheet',
    help='stylesheet name (`dark`, `light`, `native`, ...)',
    default='native'
)
# Know working styles include:
#   1. Fusion
#   2. Windows
parser.add_argument(
    '--style',
    help='application style (`Fusion`, `Windows`, `native`, ...)',
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
    QUndoGroup = QtGui.QUndoGroup
    QUndoStack = QtGui.QUndoStack
    QUndoCommand = QtGui.QUndoCommand
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
    ToolButtonIconOnly = QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly
    ToolButtonTextOnly = QtCore.Qt.ToolButtonStyle.ToolButtonTextOnly
    ToolButtonTextBesideIcon = QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon
    ToolButtonTextUnderIcon = QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon
    ToolButtonFollowStyle = QtCore.Qt.ToolButtonStyle.ToolButtonFollowStyle
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
    DockWidgetVerticalTitleBar = QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar
    AnyFile = QtWidgets.QFileDialog.FileMode.AnyFile
    ExistingFile = QtWidgets.QFileDialog.FileMode.ExistingFile
    Directory = QtWidgets.QFileDialog.FileMode.Directory
    DontUseNativeDialog = QtWidgets.QFileDialog.Option.DontUseNativeDialog
    NoButtons = QtWidgets.QFontDialog.FontDialogOption.NoButtons
    ShowAlphaChannel = QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel
    ColorNoButtons = QtWidgets.QColorDialog.ColorDialogOption.NoButtons
    ColorDontUseNativeDialog = QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog
    FontDontUseNativeDialog = QtWidgets.QFontDialog.FontDialogOption.DontUseNativeDialog
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
    Network = QtWidgets.QFileIconProvider.IconType.Network
    TopToBottom = QtWidgets.QProgressBar.Direction.TopToBottom
    BottomToTop = QtWidgets.QProgressBar.Direction.BottomToTop
    DotLine = QtCore.Qt.PenStyle.DotLine
    NoEcho = QtWidgets.QLineEdit.EchoMode.NoEcho
    Password = QtWidgets.QLineEdit.EchoMode.Password
    PasswordEchoOnEdit = QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit
    LCDOutline = QtWidgets.QLCDNumber.SegmentStyle.Outline
    LCDFlat = QtWidgets.QLCDNumber.SegmentStyle.Flat
    PlainText = QtCore.Qt.TextFormat.PlainText
    RichText = QtCore.Qt.TextFormat.RichText
    AutoText = QtCore.Qt.TextFormat.AutoText
    MarkdownText = QtCore.Qt.TextFormat.MarkdownText
    TextSelectableByMouse = QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
    TextEditorInteraction = QtCore.Qt.TextInteractionFlag.TextEditorInteraction
    RubberBandLine = QtWidgets.QRubberBand.Shape.Line
    RubberBandRectangle = QtWidgets.QRubberBand.Shape.Rectangle
    NoTicks = QtWidgets.QSlider.TickPosition.NoTicks
    TicksBothSides = QtWidgets.QSlider.TickPosition.TicksBothSides
    TicksAbove = QtWidgets.QSlider.TickPosition.TicksAbove
    TicksBelow = QtWidgets.QSlider.TickPosition.TicksBelow
    TicksLeft = QtWidgets.QSlider.TickPosition.TicksLeft
    TicksRight = QtWidgets.QSlider.TickPosition.TicksRight
    IntInput = QtWidgets.QInputDialog.InputMode.IntInput
    DoubleInput = QtWidgets.QInputDialog.InputMode.DoubleInput
    UseListViewForComboBoxItems = QtWidgets.QInputDialog.InputDialogOption.UseListViewForComboBoxItems
    InputNoButtons = QtWidgets.QInputDialog.InputDialogOption.NoButtons
    QFileSystemModel = QtGui.QFileSystemModel
    NoFrame = QtWidgets.QFrame.Shape.NoFrame
    Box = QtWidgets.QFrame.Shape.Box
    Panel = QtWidgets.QFrame.Shape.Panel
    StyledPanel = QtWidgets.QFrame.Shape.StyledPanel
    HLine = QtWidgets.QFrame.Shape.HLine
    VLine = QtWidgets.QFrame.Shape.VLine
    WinPanel = QtWidgets.QFrame.Shape.WinPanel
    Shadow_Mask = QtWidgets.QFrame.StyleMask.Shadow_Mask
    Shape_Mask = QtWidgets.QFrame.StyleMask.Shape_Mask
    Plain = QtWidgets.QFrame.Shadow.Plain
    Raised = QtWidgets.QFrame.Shadow.Raised
    Sunken = QtWidgets.QFrame.Shadow.Sunken
    Rounded = QtWidgets.QTabWidget.TabShape.Rounded
    Triangular = QtWidgets.QTabWidget.TabShape.Triangular
    LeftSide = QtWidgets.QTabBar.ButtonPosition.LeftSide
    RightSide = QtWidgets.QTabBar.ButtonPosition.RightSide
    ClassicStyle = QtWidgets.QWizard.WizardStyle.ClassicStyle
    ModernStyle = QtWidgets.QWizard.WizardStyle.ModernStyle
    MacStyle = QtWidgets.QWizard.WizardStyle.MacStyle
    AeroStyle = QtWidgets.QWizard.WizardStyle.AeroStyle
    HaveHelpButton = QtWidgets.QWizard.WizardOption.HaveHelpButton
    WatermarkPixmap = QtWidgets.QWizard.WizardPixmap.WatermarkPixmap
    LogoPixmap = QtWidgets.QWizard.WizardPixmap.LogoPixmap
    BannerPixmap = QtWidgets.QWizard.WizardPixmap.BannerPixmap
    BackgroundPixmap = QtWidgets.QWizard.WizardPixmap.BackgroundPixmap
else:
    QUndoGroup = QtWidgets.QUndoGroup
    QUndoStack = QtWidgets.QUndoStack
    QUndoCommand = QtWidgets.QUndoCommand
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
    ToolButtonIconOnly = QtCore.Qt.ToolButtonIconOnly
    ToolButtonTextOnly = QtCore.Qt.ToolButtonTextOnly
    ToolButtonTextBesideIcon = QtCore.Qt.ToolButtonTextBesideIcon
    ToolButtonTextUnderIcon = QtCore.Qt.ToolButtonTextUnderIcon
    ToolButtonFollowStyle = QtCore.Qt.ToolButtonFollowStyle
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
    DockWidgetVerticalTitleBar = QtWidgets.QDockWidget.DockWidgetVerticalTitleBar
    AnyFile = QtWidgets.QFileDialog.AnyFile
    ExistingFile = QtWidgets.QFileDialog.ExistingFile
    Directory = QtWidgets.QFileDialog.Directory
    DontUseNativeDialog = QtWidgets.QFileDialog.DontUseNativeDialog
    NoButtons = QtWidgets.QFontDialog.NoButtons
    ShowAlphaChannel = QtWidgets.QColorDialog.ShowAlphaChannel
    ColorNoButtons = QtWidgets.QColorDialog.NoButtons
    ColorDontUseNativeDialog = QtWidgets.QColorDialog.DontUseNativeDialog
    FontDontUseNativeDialog = QtWidgets.QFontDialog.DontUseNativeDialog
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
    Network = QtWidgets.QFileIconProvider.Network
    TopToBottom = QtWidgets.QProgressBar.TopToBottom
    BottomToTop = QtWidgets.QProgressBar.BottomToTop
    DotLine = QtCore.Qt.DotLine
    NoEcho = QtWidgets.QLineEdit.NoEcho
    Password = QtWidgets.QLineEdit.Password
    PasswordEchoOnEdit = QtWidgets.QLineEdit.PasswordEchoOnEdit
    LCDOutline = QtWidgets.QLCDNumber.Outline
    LCDFlat = QtWidgets.QLCDNumber.Flat
    PlainText = QtCore.Qt.PlainText
    RichText = QtCore.Qt.RichText
    AutoText = QtCore.Qt.AutoText
    MarkdownText = QtCore.Qt.MarkdownText
    TextSelectableByMouse = QtCore.Qt.TextSelectableByMouse
    TextEditorInteraction = QtCore.Qt.TextEditorInteraction
    RubberBandLine = QtWidgets.QRubberBand.Line
    RubberBandRectangle = QtWidgets.QRubberBand.Rectangle
    NoTicks = QtWidgets.QSlider.NoTicks
    TicksBothSides = QtWidgets.QSlider.TicksBothSides
    TicksAbove = QtWidgets.QSlider.TicksAbove
    TicksBelow = QtWidgets.QSlider.TicksBelow
    TicksLeft = QtWidgets.QSlider.TicksLeft
    TicksRight = QtWidgets.QSlider.TicksRight
    IntInput = QtWidgets.QInputDialog.IntInput
    DoubleInput = QtWidgets.QInputDialog.DoubleInput
    UseListViewForComboBoxItems = QtWidgets.QInputDialog.UseListViewForComboBoxItems
    InputNoButtons = QtWidgets.QInputDialog.NoButtons
    QFileSystemModel = QtWidgets.QFileSystemModel
    NoFrame = QtWidgets.QFrame.NoFrame
    Box = QtWidgets.QFrame.Box
    Panel = QtWidgets.QFrame.Panel
    StyledPanel = QtWidgets.QFrame.StyledPanel
    HLine = QtWidgets.QFrame.HLine
    VLine = QtWidgets.QFrame.VLine
    WinPanel = QtWidgets.QFrame.WinPanel
    Shadow_Mask = QtWidgets.QFrame.Shadow_Mask
    Shape_Mask = QtWidgets.QFrame.Shape_Mask
    Plain = QtWidgets.QFrame.Plain
    Raised = QtWidgets.QFrame.Raised
    Sunken = QtWidgets.QFrame.Sunken
    Rounded = QtWidgets.QTabWidget.Rounded
    Triangular = QtWidgets.QTabWidget.Triangular
    LeftSide = QtWidgets.QTabBar.LeftSide
    RightSide = QtWidgets.QTabBar.RightSide
    ClassicStyle = QtWidgets.QWizard.ClassicStyle
    ModernStyle = QtWidgets.QWizard.ModernStyle
    MacStyle = QtWidgets.QWizard.MacStyle
    AeroStyle = QtWidgets.QWizard.AeroStyle
    HaveHelpButton = QtWidgets.QWizard.HaveHelpButton
    WatermarkPixmap = QtWidgets.QWizard.WatermarkPixmap
    LogoPixmap = QtWidgets.QWizard.LogoPixmap
    BannerPixmap = QtWidgets.QWizard.BannerPixmap
    BackgroundPixmap = QtWidgets.QWizard.BackgroundPixmap

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

def get_standard_icon(widget, pixmap, name):
    '''Get a standard icon depending on the stylesheet.'''

    if args.stylesheet == 'native':
        return widget.style().standardIcon(pixmap)
    return QtGui.QIcon(f'{resource_format}{name}.svg')

def close_icon(widget):
    '''Get the close icon depending on the stylesheet.'''
    return get_standard_icon(widget, SP_DockWidgetCloseButton, 'close')

def reset_icon(widget):
    '''Get the reset icon depending on the stylesheet.'''
    return get_standard_icon(widget, SP_DialogResetButton, 'dialog_reset')

def next_icon(widget):
    '''Get the next icon depending on the stylesheet.'''
    return get_standard_icon(widget, SP_ArrowRight, 'right_arrow')

def previous_icon(widget):
    '''Get the previous icon depending on the stylesheet.'''
    return get_standard_icon(widget, SP_ArrowLeft, 'left_arrow')

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

def test_progressbar_inverted(widget, *_):
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
    for bar in child:
        bar.setInvertedAppearance(True)

    return child

def test_progressbar_text(widget, *_):
    layout_type = 'horizontal'
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
    for bar in child:
        bar.setTextDirection(TopToBottom)
        bar.setOrientation(Vertical)

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

def test_tick_slider(widget, *_):
    child = QtWidgets.QSlider(widget)
    child.setOrientation(Horizontal)
    child.setTickInterval(5)
    child.setTickPosition(TicksAbove)

    return child

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

def test_large_handle_splitter(widget, *_):
    child = QtWidgets.QSplitter(widget)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())
    child.setHandleWidth(child.handleWidth() * 5)

    return child

def test_nocollapsible_splitter(widget, *_):
    child = QtWidgets.QSplitter(widget)
    child.addWidget(QtWidgets.QListWidget())
    child.addWidget(QtWidgets.QTreeWidget())
    child.addWidget(QtWidgets.QTextEdit())
    child.setChildrenCollapsible(False)

    return child

def test_rubber_band(widget, *_):
    return [
        QtWidgets.QRubberBand(RubberBandLine, widget),
        QtWidgets.QRubberBand(RubberBandRectangle, widget),
    ]

def test_plain_text_edit(widget, *_):
    child = [
        QtWidgets.QPlainTextEdit('Edit 1', widget),
        QtWidgets.QPlainTextEdit('Edit 2', widget),
        QtWidgets.QPlainTextEdit('Edit 3', widget),
        QtWidgets.QPlainTextEdit('Edit 4', widget),
        QtWidgets.QPlainTextEdit('Edit 5', widget),
    ]
    child[1].setBackgroundVisible(True)
    child[2].setCenterOnScroll(True)
    child[3].setCursorWidth(5)
    child[3].setPlaceholderText('Placeholder Text')
    child[4].setReadOnly(True)

    return child

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

def _menu(window, font, width):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addAction(QAction('&Action 1', window))
    menu.addAction(QAction('&Action 2', window))
    child.addAction(menu.menuAction())
    window.setMenuBar(child)

    return child, menu

def test_native_menu(_, window, font, width, *__):
    child, _ = _menu(window, font, width)
    child.setNativeMenuBar(True)

    return child

def test_popup_menu(_, window, font, width, *__):
    child, _ = _menu(window, font, width)
    child.setDefaultUp(True)

    return child

def test_tearoff_menu(_, window, font, width, *__):
    child, menu = _menu(window, font, width)
    menu.setTearOffEnabled(True)

    return child

def test_icon_menu(widget, window, font, width, *_):
    child, menu = _menu(window, font, width)
    menu.setIcon(close_icon(widget))

    return child

def test_collapsible_separators_menu(_, window, font, width, *__):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    menu.addSeparator()
    menu.addAction(QAction('&Action 1', window))
    menu.addSeparator()
    menu.addSeparator()
    menu.addAction(QAction('&Action 2', window))
    menu.addSeparator()
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setSeparatorsCollapsible(True)

    return child

def test_tooltips_menu(widget, window, font, width, *_):
    child = QtWidgets.QMenuBar(window)
    child.setGeometry(QtCore.QRect(0, 0, width, int(1.5 * font.pointSize())))
    menu = QtWidgets.QMenu('Main Menu', child)
    action1 = QAction('&Action 1', window)
    action1.setToolTip('Action 1')
    menu.addAction(action1)
    action2 = QAction('&Action 2', window)
    action2.setToolTip('Action 1')
    menu.addAction(action2)
    child.addAction(menu.menuAction())
    window.setMenuBar(child)
    menu.setToolTipsVisible(True)

    return child

def test_mdi_area(widget, *_):
    child = QtWidgets.QMdiArea(widget)
    child.addSubWindow(QtWidgets.QMdiSubWindow())
    child.addSubWindow(QtWidgets.QMdiSubWindow())

    return child

def test_statusbar(_, window, *__):
    child = QtWidgets.QStatusBar(window)
    window.setStatusBar(child)

    return child

def test_no_sizegrip_statusbar(_, window, *__):
    child = QtWidgets.QStatusBar(window)
    child.setSizeGripEnabled(False)
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
    spin2.setPrefix('$')
    spin2.setSuffix('%')
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
    spin2.setPrefix('$')
    spin2.setSuffix('%')
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
    combo3.lineEdit().setPlaceholderText('Placeholder')
    child.append(combo3)
    combo4 = QtWidgets.QComboBox(widget)
    combo4.addItem('Item 1')
    combo4.addItem('Item 2')
    combo4.addItem('Item 3')
    combo4.addItem('Item 4')
    combo4.addItem('Item 5')
    combo4.addItem('Item 6')
    combo4.setMaxVisibleItems(5)
    child.append(combo4)

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

def test_autohide_tabwidget(widget, *_):
    child = []

    item1 = QtWidgets.QTabWidget(widget)
    item1.setTabPosition(North)
    item1.addTab(QtWidgets.QWidget(), 'Tab 1')
    item1.setTabBarAutoHide(True)
    child.append(item1)

    item2 = _test_tabwidget(widget, East)
    item2.setTabBarAutoHide(True)
    child.append(item2)

    return child

def test_nonexpanding_tabwidget(widget, *_):
    child = _test_tabwidget(widget, North)
    child.tabBar().setExpanding(False)

    return child

def test_movable_tabwidget(widget, *_):
    child = _test_tabwidget(widget, North)
    child.tabBar().setMovable(True)

    return child

def test_closable_tabwidget_top(widget, *_):
    child = _test_tabwidget(widget, North)
    child.setTabsClosable(True)

    return child

def test_closable_tabwidget_right(widget, *_):
    child = _test_tabwidget(widget, East)
    child.setTabsClosable(True)

    return child

def test_use_scroll_tabwidget(widget, *_):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(North)
    for i in range(1, 100):
        child.addTab(QtWidgets.QWidget(), f'Tab {i}')
    child.setUsesScrollButtons(True)

    return child

def test_no_scroll_tabwidget(widget, *_):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(North)
    for i in range(1, 100):
        child.addTab(QtWidgets.QWidget(), f'Tab {i}')
    child.setUsesScrollButtons(False)

    return child

def test_rounded_tabwidget_north(widget, *_):
    child = _test_tabwidget(widget, North)
    child.setTabShape(Rounded)

    return child

def test_triangle_tabwidget_north(widget, *_):
    child = _test_tabwidget(widget, North)
    child.setTabShape(Triangular)

    return child

def test_rounded_tabwidget_east(widget, *_):
    child = _test_tabwidget(widget, East)
    child.setTabShape(Rounded)

    return child

def test_triangle_tabwidget_east(widget, *_):
    child = _test_tabwidget(widget, East)
    child.setTabShape(Triangular)

    return child

def test_rounded_tabwidget_west(widget, *_):
    child = _test_tabwidget(widget, West)
    child.setTabShape(Rounded)

    return child

def test_triangle_tabwidget_west(widget, *_):
    child = _test_tabwidget(widget, West)
    child.setTabShape(Triangular)

    return child

def test_rounded_tabwidget_south(widget, *_):
    child = _test_tabwidget(widget, South)
    child.setTabShape(Rounded)

    return child

def test_triangle_tabwidget_south(widget, *_):
    child = _test_tabwidget(widget, South)
    child.setTabShape(Triangular)

    return child

def test_button_position_tabwidget(widget, *_):
    child = QtWidgets.QTabWidget(widget)
    child.setTabPosition(North)
    for i in range(1, 10):
        child.addTab(QtWidgets.QWidget(), f'Tab {i}')
        if i % 2 == 0:
            side = LeftSide
        else:
            side = RightSide
        child.tabBar().setTabButton(i - 1, side, QtWidgets.QWidget(widget))
    child.setUsesScrollButtons(True)

    return child

def test_text_browser(widget, *_):
    child = QtWidgets.QTextBrowser(widget)
    child.setOpenExternalLinks(True)
    child.setMarkdown('[QTextBrowser](https://doc.qt.io/qt-5/qtextbrowser.html)')

    return child

def test_dock(_, window, *__):
    dock1 = QtWidgets.QDockWidget('&Dock widget 1', window)
    dock1.setFeatures(AllDockWidgetFeatures)
    dock2 = QtWidgets.QDockWidget('&Dock widget 2', window)
    dock2.setFeatures(AllDockWidgetFeatures)
    dock3 = QtWidgets.QDockWidget('&Dock widget 3', window)
    dock3.setFeatures(DockWidgetVerticalTitleBar)
    window.addDockWidget(LeftDockWidgetArea, dock1)
    window.addDockWidget(LeftDockWidgetArea, dock2)
    window.addDockWidget(LeftDockWidgetArea, dock3)
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

def test_nocorner_table(widget, *_):
    child = test_table(widget)
    child.setCornerButtonEnabled(False)

    return child

def test_nogrid_table(widget, *_):
    child = test_table(widget)
    child.setShowGrid(False)

    return child

def test_gridstyle_table(widget, *_):
    child = test_table(widget)
    child.setGridStyle(DotLine)

    return child

def test_nohighlight_header_view(widget, *_):
    child = test_table(widget)
    header = child.horizontalHeader()
    header.setHighlightSections(False)

    return child

def test_movable_header_view(widget, *_):
    child = test_table(widget)
    header = child.horizontalHeader()
    header.setSectionsMovable(True)

    return child

def test_noclick_header_view(widget, *_):
    child = test_table(widget)
    header = child.horizontalHeader()
    header.setSectionsClickable(False)

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

def test_sortable_list(widget, *_):
    child = QtWidgets.QListWidget(widget)
    child.setSortingEnabled(True)
    for index in range(10):
        item = QtWidgets.QListWidgetItem(f'Item {index + 1}')
        child.addItem(item)

    return child

def test_key_sequence_edit(widget, *_):
    return QtWidgets.QKeySequenceEdit(widget)

def test_completer(widget, *_):
    child = QtWidgets.QLineEdit(widget)
    completer = QtWidgets.QCompleter(['Fruit', 'Fruits Basket', 'Fruba'])
    child.setCompleter(completer)

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
    toolbar1.setMovable(False)
    window.addToolBar(TopToolBarArea, toolbar1)

    toolbar2 = QtWidgets.QToolBar('Toolbar')
    toolbar2.setOrientation(Vertical)
    toolbar2.addAction('&Action 1')
    action2 = QAction('&Action 2', window)
    action2.setStatusTip('Status tip')
    action2.setWhatsThis('Example action')
    toolbar2.addAction(action2)
    toolbar2.addSeparator()
    toolbar2.addAction('&Action 3')
    toolbar2.addAction('&Action 3 Really Long Name')
    toolbar2.addAction(QtWidgets.QWhatsThis.createAction(toolbar2))
    icon = close_icon(toolbar2)
    toolbar2.addAction(icon, '&Action 4')
    toolbar2.setFloatable(True)
    toolbar2.setMovable(True)
    window.addToolBar(LeftToolBarArea, toolbar2)

    statusbar = QtWidgets.QStatusBar(window)
    window.setStatusBar(statusbar)

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

def test_raised_toolbutton(widget, window, *_):
    layout_type = 'horizontal'
    child = [
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
        QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    child[0].setArrowType(LeftArrow)
    child[1].setArrowType(RightArrow)
    child[2].setArrowType(UpArrow)
    child[3].setArrowType(DownArrow)
    for item in child:
        item.setAutoRaise(True)

    return child, layout_type

def test_toolbutton_style(widget, window, *_):
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
        QtWidgets.QToolButton(widget),
    ]
    window.setTabOrder(child[0], child[1])
    window.setTabOrder(child[1], child[2])
    window.setTabOrder(child[2], child[3])
    window.setTabOrder(child[3], child[4])
    window.setTabOrder(child[4], child[5])
    window.setTabOrder(child[5], child[6])
    window.setTabOrder(child[6], child[7])
    window.setTabOrder(child[7], child[8])
    window.setTabOrder(child[8], child[9])
    child[0].setText('Button 1')
    child[1].setText('Button 2')
    child[2].setText('Button 3')
    child[3].setText('Button 4')
    child[4].setText('Button 5')
    child[5].setText('Button 6')
    child[6].setText('Button 7')
    child[7].setText('Button 8')
    child[8].setText('Button 9')
    child[9].setText('Button 10')
    child[0].setToolButtonStyle(ToolButtonIconOnly)
    child[1].setToolButtonStyle(ToolButtonTextOnly)
    child[2].setToolButtonStyle(ToolButtonTextBesideIcon)
    child[3].setToolButtonStyle(ToolButtonTextUnderIcon)
    child[4].setToolButtonStyle(ToolButtonFollowStyle)
    child[5].setToolButtonStyle(ToolButtonIconOnly)
    child[6].setToolButtonStyle(ToolButtonTextOnly)
    child[7].setToolButtonStyle(ToolButtonTextBesideIcon)
    child[8].setToolButtonStyle(ToolButtonTextUnderIcon)
    child[9].setToolButtonStyle(ToolButtonFollowStyle)
    icon = close_icon(widget)
    for item in child:
        item.setIcon(icon)
    for item in child[5:]:
        item.setAutoRaise(True)

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
    flat = QtWidgets.QPushButton('Flat')
    flat.setFlat(True)
    child.append(flat)
    auto_default = QtWidgets.QPushButton('Auto Default')
    auto_default.setAutoDefault(True)
    child.append(auto_default)

    return child, layout_type

def test_column_view(widget, *_):
    child = QtWidgets.QColumnView(widget)
    model = QFileSystemModel(widget)
    model.setRootPath('/')
    child.setModel(model)
    child.setResizeGripsVisible(True)

    return child

def test_nosizegrip_column_view(widget, *_):
    child = QtWidgets.QColumnView(widget)
    model = QFileSystemModel(widget)
    model.setRootPath('/')
    child.setModel(model)
    child.setResizeGripsVisible(False)

    return child

def test_comprehensive_frame(widget, *_):
    child = [
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
        QtWidgets.QFrame(widget),
    ]
    child[0].setFrameShape(NoFrame)
    child[1].setFrameShape(Box)
    child[2].setFrameShape(Panel)
    child[3].setFrameShape(StyledPanel)
    child[4].setFrameShape(HLine)
    child[5].setFrameShape(VLine)
    child[6].setFrameShape(WinPanel)
    child[7].setFrameStyle(Shadow_Mask)
    child[8].setFrameStyle(Shape_Mask)
    child[9].setFrameShadow(Plain)
    child[10].setFrameShadow(Raised)
    child[11].setFrameShadow(Sunken)
    for item in child[7:]:
        item.setFrameShape(StyledPanel)

    return child

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

def test_sortable_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setObjectName('treeWidget')
    item_0 = QtWidgets.QTreeWidgetItem(tree)
    item_1 = QtWidgets.QTreeWidgetItem(tree)
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
    item_9 = QtWidgets.QTreeWidgetItem(tree, ['Row 3'])
    item_10 = QtWidgets.QTreeWidgetItem(item_9, ['Row 3.1'])
    item_11 = QtWidgets.QTreeWidgetItem(tree, ['Row 4'])

    tree.headerItem().setText(0, 'qdz')
    tree.setSortingEnabled(False)
    tree.topLevelItem(0).setText(0, 'qzd')
    tree.topLevelItem(1).setText(0, 'effefe')
    tree.setSortingEnabled(True)

    return tree

def test_hidden_header_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])

    tree.setHeaderHidden(True)

    return tree

def test_indented_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1', 'Row 2.2'])

    tree.setIndentation(tree.indentation() * 2)
    tree.setColumnCount(2)
    tree.setColumnWidth(0, tree.columnWidth(0) * 2)
    tree.setColumnWidth(1, tree.columnWidth(1) * 2)

    return tree3

def test_all_focus_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1', 'Row 2.2'])

    tree.setAllColumnsShowFocus(True)
    tree.setColumnCount(2)

    return tree

def test_nonexpandable_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])

    tree.setItemsExpandable(False)

    return tree

def test_undecorated_tree(widget, *_):
    tree = QtWidgets.QTreeWidget(widget)
    tree.setHeaderLabel('Tree 1')
    item1 = QtWidgets.QTreeWidgetItem(tree, ['Row 1'])
    item2 = QtWidgets.QTreeWidgetItem(tree, ['Row 2'])
    item3 = QtWidgets.QTreeWidgetItem(item2, ['Row 2.1'])

    tree.setRootIsDecorated(False)

    return tree

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
    flat = QtWidgets.QGroupBox('Groupbox 3', widget)
    flat.setFlat(True)
    child.append(flat)

    return child

def test_dial(widget, *_):
    child = [
        QtWidgets.QDial(widget),
        QtWidgets.QDial(widget)
    ]
    child[1].setNotchesVisible(True)
    for item in child:
        item.setMinimum(0)
        item.setMaximum(100)
        item.setValue(30)

    return child

def test_command_link(widget, *_):
    child = QtWidgets.QWidget(widget)
    layout = QtWidgets.QVBoxLayout()
    layout.addStretch(1)
    next = QtWidgets.QCommandLinkButton('Next', 'Go next', widget)
    next.setIcon(next_icon(next))
    layout.addWidget(next)
    previous = QtWidgets.QCommandLinkButton('Previous', 'Go previous', widget)
    previous.setFlat(True)
    previous.setIcon(previous_icon(previous))
    layout.addWidget(previous)
    layout.addWidget(QtWidgets.QCommandLinkButton('Text Only', widget))
    layout.addStretch(1)

    child.setLayout(layout)

    return child

def test_lineedit(widget, *_):
    return QtWidgets.QLineEdit('Sample label', widget)

def test_placeholder_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setPlaceholderText('Placeholder')

    return child

def test_readonly_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setReadOnly(True)

    return child

def test_noframe_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setFrame(False)

    return child

def test_noecho_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setEchoMode(NoEcho)

    return child

def test_password_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setEchoMode(Password)

    return child

def test_password_edit_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setEchoMode(PasswordEchoOnEdit)

    return child

def test_clear_lineedit(widget, *_):
    child = QtWidgets.QLineEdit('Sample label', widget)
    child.setClearButtonEnabled(True)

    return child

def test_label(widget, *_):
    return QtWidgets.QLabel('Sample label')

def test_indented_label(widget, *_):
    child = QtWidgets.QLabel('Sample label')
    child.setIndent(50)

    return child

def test_markdown_label(widget, *_):
    child = [
        QtWidgets.QLabel(),
        QtWidgets.QLabel(),
    ]
    child[0].setText('[BreezeStyleSheets](https://github.com/Alexhuszagh/BreezeStyleSheets)')
    child[0].setOpenExternalLinks(True)
    child[1].setText('# Sample Header\n- Bullet 1\n- Bullet 2')

    for item in child:
        item.setTextFormat(MarkdownText)

    return child

def test_selectable_label(widget, *_):
    child = QtWidgets.QLabel('Selectable label')
    child.setTextInteractionFlags(TextSelectableByMouse)

    return child

def test_editable_label(widget, *_):
    child = QtWidgets.QLabel('Editable label')
    child.setTextInteractionFlags(TextEditorInteraction)

    return child

def test_font_combobox(widget, *_):
    return QtWidgets.QFontComboBox(widget)

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

def test_nogrid_calendar(widget, *_):
    child = QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(False)

    return child

def test_nonavigation_calendar(widget, *_):
    child = QtWidgets.QCalendarWidget(widget)
    child.setGridVisible(True)
    child.setNavigationBarVisible(False)

    return child

def test_time_edit(widget, *_):
    return QtWidgets.QTimeEdit(widget)

def test_date_edit(widget, *_):
    return QtWidgets.QDateEdit(widget)

def test_datetime_edit(widget, *_):
    return QtWidgets.QDateTimeEdit(widget)

def test_popup_datetime_edit(widget, *_):
    child = QtWidgets.QDateTimeEdit(widget)
    child.setCalendarPopup(True)

    return child

def test_formats_datetime_edit(widget, *_):
    child = [
        QtWidgets.QDateTimeEdit(widget),
        QtWidgets.QDateTimeEdit(widget),
    ]
    child[0].setDisplayFormat('dd.MM.yyyy')
    child[1].setDisplayFormat('MMM d yy')

    return child

def test_undo_group(widget, *_):
    group = QUndoGroup(widget)
    child = QtWidgets.QUndoView(group, widget)
    child.setEmptyLabel('New')
    child.setCleanIcon(reset_icon(widget))

    stack1 = QUndoStack(widget)
    stack1.push(QUndoCommand('Action 1'))
    stack1.push(QUndoCommand('Action 2'))
    group.addStack(stack1)

    stack2 = QUndoStack(widget)
    stack2.push(QUndoCommand('Action 3'))
    stack2.push(QUndoCommand('Action 4'))
    group.addStack(stack2)

    group.setActiveStack(stack1)

    return child

def test_undo_stack(widget, *_):
    stack = QUndoStack(widget)
    child = QtWidgets.QUndoView(stack, widget)
    child.setEmptyLabel('New')
    child.setCleanIcon(reset_icon(widget))
    stack.push(QUndoCommand('Action 1'))
    stack.push(QUndoCommand('Action 2'))
    stack.push(QUndoCommand('Action 3'))
    stack.push(QUndoCommand('Action 4'))
    stack.push(QUndoCommand('Action 5'))

    return child

def test_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    return child

def test_hex_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setHexMode()
    return child

def test_outline_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setSegmentStyle(LCDOutline)
    return child

def test_flat_lcd_number(widget, *_):
    child = QtWidgets.QLCDNumber(3, widget)
    child.display(15)
    child.setSegmentStyle(LCDFlat)
    return child

def test_file_icon_provider(widget, *_):
    child = QtWidgets.QPushButton()
    provider = QtWidgets.QFileIconProvider()
    child.setIcon(provider.icon(Network))

    return child

def test_dialog(_, window, *__):
    dialog = QtWidgets.QDialog(window)
    execute(dialog)

    return None, None, False, True

def test_modal_dialog(_, window, *__):
    dialog = QtWidgets.QDialog(window)
    dialog.setModal(True)
    execute(dialog)

    return None, None, False, True

def test_sizegrip_dialog(_, window, *__):
    dialog = QtWidgets.QDialog(window)
    dialog.setSizeGripEnabled(True)
    execute(dialog)

    return None, None, False, True

def test_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial)

    return None, None, False, True

def test_alpha_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial, options=ShowAlphaChannel)

    return None, None, False, True

def test_nobuttons_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial, options=ColorNoButtons)

    return None, None, False, True

def test_qt_colordialog(*_):
    initial = QtGui.QColor()
    QtWidgets.QColorDialog.getColor(initial, options=ColorDontUseNativeDialog)

    return None, None, False, True

def test_fontdialog(*_):
    initial = QtGui.QFont()
    QtWidgets.QFontDialog.getColor(initial)

    return None, None, False, True

def test_nobuttons_fontdialog(*_):
    initial = QtGui.QFont()
    QtWidgets.QFontDialog.getFont(initial, options=NoButtons)

    return None, None, False, True

def test_qt_fontdialog(*_):
    initial = QtGui.QFont()
    QtWidgets.QFontDialog.getFont(initial, options=FontDontUseNativeDialog)

    return None, None, False, True

def test_filedialog(_, window, *__):
    dialog = QtWidgets.QFileDialog(window)
    dialog.setFileMode(Directory)
    execute(dialog)

    return None, None, False, True

def test_qt_filedialog(_, window, *__):
    dialog = QtWidgets.QFileDialog(window)
    dialog.setOption(DontUseNativeDialog)
    execute(dialog)

    return None, None, False, True

def test_error_message(widget, *_):
    dialog = QtWidgets.QErrorMessage(widget)
    dialog.showMessage('Error message')
    execute(dialog)

    return None, None, False, True

def test_progress_dialog(_, window, __, ___, ____, app):
    dialog = QtWidgets.QProgressDialog('Text', 'Cancel', 0, 100, window)
    dialog.setMinimumDuration(0)
    dialog.show()
    for i in range(1, 101):
        dialog.setValue(i)
        app.processEvents()
        time.sleep(0.02)
        if dialog.wasCanceled():
            break
    dialog.close()

    return None, None, False, True

def test_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    execute(dialog)

    return None, None, False, True

def test_int_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setInputMode(IntInput)
    execute(dialog)

    return None, None, False, True

def test_double_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setInputMode(DoubleInput)
    execute(dialog)

    return None, None, False, True

def test_combobox_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(['Item 1', 'Item 2'])
    execute(dialog)

    return None, None, False, True

def test_list_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(['Item 1', 'Item 2'])
    dialog.setOption(UseListViewForComboBoxItems)
    execute(dialog)

    return None, None, False, True

def test_nobuttons_input_dialog(_, window, *__):
    dialog = QtWidgets.QInputDialog(window)
    dialog.setComboBoxItems(['Item 1', 'Item 2'])
    dialog.setOption(InputNoButtons)
    execute(dialog)

    return None, None, False, True

def _wizard(widget):
    wizard = QtWidgets.QWizard()

    intro = QtWidgets.QWizardPage()
    intro.setTitle('Introduction')
    intro_label = QtWidgets.QLabel('Some very long text to simulate wrapping of the UI when displayed, because this needs to be done.')
    intro_label.setWordWrap(True)
    intro_layout = QtWidgets.QVBoxLayout()
    intro_layout.addWidget(intro_label)
    intro.setLayout(intro_layout)
    intro.setPixmap(WatermarkPixmap, close_icon(widget).pixmap(50, 50))
    wizard.addPage(intro)

    registration = QtWidgets.QWizardPage()
    registration.setTitle('Registration')
    registration_label = QtWidgets.QLabel('Please register your copy.')
    registration_label.setWordWrap(True)
    registration_layout = QtWidgets.QVBoxLayout()
    registration_layout.addWidget(registration_label)
    registration.setLayout(registration_layout)
    registration.setPixmap(LogoPixmap, close_icon(widget).pixmap(200, 200))
    wizard.addPage(registration)

    conclusion = QtWidgets.QWizardPage()
    conclusion.setTitle('Conclusion')
    conclusion_label = QtWidgets.QLabel('Congratulations on your purchase.')
    conclusion_label.setWordWrap(True)
    conclusion_layout = QtWidgets.QVBoxLayout()
    conclusion_layout.addWidget(conclusion_label)
    conclusion.setLayout(conclusion_layout)
    conclusion.setPixmap(BannerPixmap, close_icon(widget).pixmap(50, 50))
    conclusion.setPixmap(BackgroundPixmap, close_icon(widget).pixmap(50, 50))
    wizard.addPage(conclusion)

    wizard.setOption(HaveHelpButton)

    wizard.setWindowTitle('Simple Wizard Example')

    return wizard

def test_wizard(widget, *_):
    wizard = _wizard(widget)
    execute(wizard)

    return None, None, False, True

def test_classic_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(ClassicStyle)
    execute(wizard)

    return None, None, False, True

def test_modern_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(ModernStyle)
    execute(wizard)

    return None, None, False, True

def test_mac_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(MacStyle)
    execute(wizard)

    return None, None, False, True

def test_aero_wizard(widget, *_):
    wizard = _wizard(widget)
    wizard.setWizardStyle(AeroStyle)
    execute(wizard)

    return None, None, False, True

def test_system_tray(widget, window, *_):
    dialog = QtWidgets.QErrorMessage(widget)
    dialog.showMessage('Error message')

    tray = QtWidgets.QSystemTrayIcon()
    icon = close_icon(widget)
    tray.setIcon(icon)
    tray.show()
    tray.setToolTip('Sample tray icon')

    execute(dialog)

    return None, None, False, True

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

def test_horizontal_buttons(widget, *_):
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

def test_vertical_buttons(widget, *_):
    child = []
    child.append(QtWidgets.QTextEdit(widget))
    container = QtWidgets.QWidget(widget)
    hbox = QtWidgets.QHBoxLayout(container)
    hbox.addWidget(QtWidgets.QPushButton('Delete'))
    hbox.addWidget(QtWidgets.QPushButton('Complete'))
    child.append(container)
    child.append(QtWidgets.QLineEdit(widget))
    dialog = QtWidgets.QDialogButtonBox(Vertical, widget)
    dialog.addButton('Yes', YesRole)
    dialog.addButton('Really really really long', YesRole)
    dialog.addButton(DialogOk)
    dialog.addButton(DialogCancel)
    dialog.setCenterButtons(True)
    child.append(dialog)

    return child

def test_stacked_widget(widget, *_):
    child = QtWidgets.QStackedWidget(widget)
    child.addWidget(QtWidgets.QLabel('Label 1'))
    child.addWidget(QtWidgets.QLabel('Label 2'))
    child.addWidget(QtWidgets.QLabel('Label 3'))
    child.addWidget(QtWidgets.QLabel('Label 4'))
    child.setCurrentIndex(2)

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

    # Set the app style.
    if args.style != 'native':
        style = QtWidgets.QStyleFactory.create(args.style)
        app.setStyle(style)

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
