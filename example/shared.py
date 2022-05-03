'''
    shared
    ======

    Shared imports and compatibility definitions between Qt5 and Qt6.
'''

import argparse
import os
import sys

example_dir = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(example_dir)
dist = os.path.join(home, 'dist')

def create_parser():
    '''Create an argparser with the base settings for all Qt applications.'''

    parser = argparse.ArgumentParser(
        description='Configurations for the Qt5 application.'
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
    # Linux or Unix-like only.
    parser.add_argument(
        '--use-x11',
        help='''force the use of x11 on compatible systems.''',
        action='store_true'
    )

    return parser

def parse_args(parser):
    '''Parse the command-line arguments and hot-patch the args.'''

    args, unknown = parser.parse_known_args()
    # Need to fix an issue on Wayland on Linux:
    #   conda-forge does not support Wayland, for who knows what reason.
    if sys.platform.lower().startswith('linux') and 'CONDA_PREFIX' in os.environ:
        args.use_x11 = True

    if args.use_x11:
        os.environ['XDG_SESSION_TYPE'] = 'x11'

    return args, unknown

def import_qt(args):
    '''Import the Qt modules'''

    if args.pyqt6:
        from PyQt6 import QtCore, QtGui, QtWidgets
        QtCore.QDir.addSearchPath(args.stylesheet, f'{dist}/pyqt6/{args.stylesheet}/')
    else:
        sys.path.insert(0, home)
        from PyQt5 import QtCore, QtGui, QtWidgets
        import breeze_resources

    return QtCore, QtGui, QtWidgets

def get_resources(args):
    '''Get the resource format for the Qt application.'''

    if args.pyqt6:
        return f'{args.stylesheet}:'
    return f':/{args.stylesheet}/'

def get_stylesheet(resource_format):
    '''Get the path to the stylesheet.'''
    return f'{resource_format}stylesheet.qss'

def get_compat_definitions(args):
    '''Create our compatibility definitions.'''

    ns = argparse.Namespace()
    if args.pyqt6:
        from PyQt6 import QtCore, QtGui, QtWidgets

        # Modules
        ns.QtCore = QtCore
        ns.QtGui = QtGui
        ns.QtWidgets = QtWidgets

        # Scoped enums.
        ns.Orientation = QtCore.Qt.Orientation
        ns.StandardPixmap = QtWidgets.QStyle.StandardPixmap
        ns.ToolBarArea = QtCore.Qt.ToolBarArea
        ns.FrameShape = QtWidgets.QFrame.Shape
        ns.FrameShadow = QtWidgets.QFrame.Shadow
        ns.ToolButtonPopupMode = QtWidgets.QToolButton.ToolButtonPopupMode
        ns.AlignmentFlag = QtCore.Qt.AlignmentFlag
        ns.OpenModeFlag = QtCore.QFile.OpenModeFlag
        ns.TabShape = QtWidgets.QTabWidget.TabShape
        ns.ItemFlag = QtCore.Qt.ItemFlag
        ns.CheckState = QtCore.Qt.CheckState
        ns.TabPosition = QtWidgets.QTabWidget.TabPosition
        ns.EchoMode = QtWidgets.QLineEdit.EchoMode
        ns.ArrowType = QtCore.Qt.ArrowType
        ns.WindowState = QtCore.Qt.WindowState
        ns.PenStyle = QtCore.Qt.PenStyle
        ns.PenCapStyle = QtCore.Qt.PenCapStyle
        ns.PenJoinStyle = QtCore.Qt.PenJoinStyle
        ns.StateFlag = QtWidgets.QStyle.StateFlag
        ns.EventType = QtCore.QEvent.Type
        ns.ColorRole = QtGui.QPalette.ColorRole
        ns.TickPosition = QtWidgets.QSlider.TickPosition
        ns.ComplexControl = QtWidgets.QStyle.ComplexControl
        ns.SubControl = QtWidgets.QStyle.SubControl

        # QObjects
        ns.QAction = QtGui.QAction

        # Enumerations
        ns.Horizontal = ns.Orientation.Horizontal
        ns.Vertical = ns.Orientation.Vertical
        ns.AlignTop = ns.AlignmentFlag.AlignTop
        ns.AlignLeft = ns.AlignmentFlag.AlignLeft
        ns.AlignHCenter = ns.AlignmentFlag.AlignHCenter
        ns.StyledPanel = ns.FrameShape.StyledPanel
        ns.HLine = ns.FrameShape.HLine
        ns.VLine = ns.FrameShape.VLine
        ns.TopToolBarArea = ns.ToolBarArea.TopToolBarArea
        ns.Raised = ns.FrameShadow.Raised
        ns.Sunken = ns.FrameShadow.Sunken
        ns.InstantPopup = ns.ToolButtonPopupMode.InstantPopup
        ns.MenuButtonPopup = ns.ToolButtonPopupMode.MenuButtonPopup
        ns.ItemIsUserCheckable = ns.ItemFlag.ItemIsUserCheckable
        ns.ItemIsUserTristate = ns.ItemFlag.ItemIsUserTristate
        ns.Checked = ns.CheckState.Checked
        ns.Unchecked = ns.CheckState.Unchecked
        ns.PartiallyChecked = ns.CheckState.PartiallyChecked
        ns.ReadOnly = ns.OpenModeFlag.ReadOnly
        ns.Text = ns.OpenModeFlag.Text
        ns.East = ns.TabPosition.East
        ns.UpArrow = ns.ArrowType.UpArrow
        ns.Triangular = ns.TabShape.Triangular
        ns.Password = ns.EchoMode.Password
        ns.WindowMaximized = ns.WindowState.WindowMaximized
        ns.SolidLine = ns.PenStyle.SolidLine
        ns.FlatCap = ns.PenCapStyle.FlatCap
        ns.SquareCap = ns.PenCapStyle.SquareCap
        ns.RoundCap = ns.PenCapStyle.RoundCap
        ns.MiterJoin = ns.PenJoinStyle.MiterJoin
        ns.BevelJoin = ns.PenJoinStyle.BevelJoin
        ns.RoundJoin = ns.PenJoinStyle.RoundJoin
        ns.SvgMiterJoin = ns.PenJoinStyle.SvgMiterJoin
        ns.State_HasFocus = ns.StateFlag.State_HasFocus
        ns.State_Selected = ns.StateFlag.State_Selected
        ns.HoverEnter = ns.EventType.HoverEnter
        ns.HoverMove = ns.EventType.HoverMove
        ns.HoverLeave = ns.EventType.HoverLeave
        ns.PlaceholderText = ns.ColorRole.PlaceholderText
        ns.NoTicks = ns.TickPosition.NoTicks
        ns.TicksAbove = ns.TickPosition.TicksAbove
        ns.TicksBelow = ns.TickPosition.TicksBelow
        ns.TicksBothSides = ns.TickPosition.TicksBothSides
        ns.CC_Slider = ns.ComplexControl.CC_Slider
        ns.SC_SliderHandle = ns.SubControl.SC_SliderHandle
        ns.SC_SliderGroove = ns.SubControl.SC_SliderGroove
        ns.SP_ArrowBack = ns.StandardPixmap.SP_ArrowBack
        ns.SP_ArrowDown = ns.StandardPixmap.SP_ArrowDown
        ns.SP_ArrowForward = ns.StandardPixmap.SP_ArrowForward
        ns.SP_ArrowLeft = ns.StandardPixmap.SP_ArrowLeft
        ns.SP_ArrowRight = ns.StandardPixmap.SP_ArrowRight
        ns.SP_ArrowUp = ns.StandardPixmap.SP_ArrowUp
        ns.SP_BrowserReload = ns.StandardPixmap.SP_BrowserReload
        ns.SP_BrowserStop = ns.StandardPixmap.SP_BrowserStop
        ns.SP_CommandLink = ns.StandardPixmap.SP_CommandLink
        ns.SP_ComputerIcon = ns.StandardPixmap.SP_ComputerIcon
        ns.SP_CustomBase = ns.StandardPixmap.SP_CustomBase
        ns.SP_DesktopIcon = ns.StandardPixmap.SP_DesktopIcon
        ns.SP_DialogApplyButton = ns.StandardPixmap.SP_DialogApplyButton
        ns.SP_DialogCancelButton = ns.StandardPixmap.SP_DialogCancelButton
        ns.SP_DialogCloseButton = ns.StandardPixmap.SP_DialogCloseButton
        ns.SP_DialogDiscardButton = ns.StandardPixmap.SP_DialogDiscardButton
        ns.SP_DialogHelpButton = ns.StandardPixmap.SP_DialogHelpButton
        ns.SP_DialogNoButton = ns.StandardPixmap.SP_DialogNoButton
        ns.SP_DialogOkButton = ns.StandardPixmap.SP_DialogOkButton
        ns.SP_DialogOpenButton = ns.StandardPixmap.SP_DialogOpenButton
        ns.SP_DialogResetButton = ns.StandardPixmap.SP_DialogResetButton
        ns.SP_DialogSaveButton = ns.StandardPixmap.SP_DialogSaveButton
        ns.SP_DialogYesButton = ns.StandardPixmap.SP_DialogYesButton
        ns.SP_DirClosedIcon = ns.StandardPixmap.SP_DirClosedIcon
        ns.SP_DirHomeIcon = ns.StandardPixmap.SP_DirHomeIcon
        ns.SP_DirIcon = ns.StandardPixmap.SP_DirIcon
        ns.SP_DirLinkIcon = ns.StandardPixmap.SP_DirLinkIcon
        ns.SP_DirLinkOpenIcon = ns.StandardPixmap.SP_DirLinkOpenIcon
        ns.SP_DirOpenIcon = ns.StandardPixmap.SP_DirOpenIcon
        ns.SP_DockWidgetCloseButton = ns.StandardPixmap.SP_DockWidgetCloseButton
        ns.SP_DriveCDIcon = ns.StandardPixmap.SP_DriveCDIcon
        ns.SP_DriveDVDIcon = ns.StandardPixmap.SP_DriveDVDIcon
        ns.SP_DriveFDIcon = ns.StandardPixmap.SP_DriveFDIcon
        ns.SP_DriveHDIcon = ns.StandardPixmap.SP_DriveHDIcon
        ns.SP_DriveNetIcon = ns.StandardPixmap.SP_DriveNetIcon
        ns.SP_FileDialogBack = ns.StandardPixmap.SP_FileDialogBack
        ns.SP_FileDialogContentsView = ns.StandardPixmap.SP_FileDialogContentsView
        ns.SP_FileDialogDetailedView = ns.StandardPixmap.SP_FileDialogDetailedView
        ns.SP_FileDialogEnd = ns.StandardPixmap.SP_FileDialogEnd
        ns.SP_FileDialogInfoView = ns.StandardPixmap.SP_FileDialogInfoView
        ns.SP_FileDialogListView = ns.StandardPixmap.SP_FileDialogListView
        ns.SP_FileDialogNewFolder = ns.StandardPixmap.SP_FileDialogNewFolder
        ns.SP_FileDialogStart = ns.StandardPixmap.SP_FileDialogStart
        ns.SP_FileDialogToParent = ns.StandardPixmap.SP_FileDialogToParent
        ns.SP_FileIcon = ns.StandardPixmap.SP_FileIcon
        ns.SP_FileLinkIcon = ns.StandardPixmap.SP_FileLinkIcon
        ns.SP_MediaPause = ns.StandardPixmap.SP_MediaPause
        ns.SP_MediaPlay = ns.StandardPixmap.SP_MediaPlay
        ns.SP_MediaSeekBackward = ns.StandardPixmap.SP_MediaSeekBackward
        ns.SP_MediaSeekForward = ns.StandardPixmap.SP_MediaSeekForward
        ns.SP_MediaSkipBackward = ns.StandardPixmap.SP_MediaSkipBackward
        ns.SP_MediaSkipForward = ns.StandardPixmap.SP_MediaSkipForward
        ns.SP_MediaStop = ns.StandardPixmap.SP_MediaStop
        ns.SP_MediaVolume = ns.StandardPixmap.SP_MediaVolume
        ns.SP_MediaVolumeMuted = ns.StandardPixmap.SP_MediaVolumeMuted
        ns.SP_LineEditClearButton = ns.StandardPixmap.SP_LineEditClearButton
        ns.SP_DialogYesToAllButton = ns.StandardPixmap.SP_DialogYesToAllButton
        ns.SP_DialogNoToAllButton = ns.StandardPixmap.SP_DialogNoToAllButton
        ns.SP_DialogSaveAllButton = ns.StandardPixmap.SP_DialogSaveAllButton
        ns.SP_DialogAbortButton = ns.StandardPixmap.SP_DialogAbortButton
        ns.SP_DialogRetryButton = ns.StandardPixmap.SP_DialogRetryButton
        ns.SP_DialogIgnoreButton = ns.StandardPixmap.SP_DialogIgnoreButton
        ns.SP_RestoreDefaultsButton = ns.StandardPixmap.SP_RestoreDefaultsButton
        if QtCore.QT_VERSION >= 393984:
            ns.SP_TabCloseButton = ns.StandardPixmap.SP_TabCloseButton
        ns.SP_MessageBoxCritical = ns.StandardPixmap.SP_MessageBoxCritical
        ns.SP_MessageBoxInformation = ns.StandardPixmap.SP_MessageBoxInformation
        ns.SP_MessageBoxQuestion = ns.StandardPixmap.SP_MessageBoxQuestion
        ns.SP_MessageBoxWarning = ns.StandardPixmap.SP_MessageBoxWarning
        ns.SP_TitleBarCloseButton = ns.StandardPixmap.SP_TitleBarCloseButton
        ns.SP_TitleBarContextHelpButton = ns.StandardPixmap.SP_TitleBarContextHelpButton
        ns.SP_TitleBarMaxButton = ns.StandardPixmap.SP_TitleBarMaxButton
        ns.SP_TitleBarMenuButton = ns.StandardPixmap.SP_TitleBarMenuButton
        ns.SP_TitleBarMinButton = ns.StandardPixmap.SP_TitleBarMinButton
        ns.SP_TitleBarNormalButton = ns.StandardPixmap.SP_TitleBarNormalButton
        ns.SP_TitleBarShadeButton = ns.StandardPixmap.SP_TitleBarShadeButton
        ns.SP_TitleBarUnshadeButton = ns.StandardPixmap.SP_TitleBarUnshadeButton
        ns.SP_ToolBarHorizontalExtensionButton = ns.StandardPixmap.SP_ToolBarHorizontalExtensionButton
        ns.SP_ToolBarVerticalExtensionButton = ns.StandardPixmap.SP_ToolBarVerticalExtensionButton
        ns.SP_TrashIcon = ns.StandardPixmap.SP_TrashIcon
        ns.SP_VistaShield = ns.StandardPixmap.SP_VistaShield
    else:
        from PyQt5 import QtCore, QtGui, QtWidgets

        # Modules
        ns.QtCore = QtCore
        ns.QtGui = QtGui
        ns.QtWidgets = QtWidgets

        # QObjects
        ns.QAction = QtWidgets.QAction

        # Enumerations
        ns.Horizontal = QtCore.Qt.Horizontal
        ns.Vertical = QtCore.Qt.Vertical
        ns.TopToolBarArea = QtCore.Qt.TopToolBarArea
        ns.StyledPanel = QtWidgets.QFrame.StyledPanel
        ns.HLine = QtWidgets.QFrame.HLine
        ns.VLine = QtWidgets.QFrame.VLine
        ns.Raised = QtWidgets.QFrame.Raised
        ns.Sunken = QtWidgets.QFrame.Sunken
        ns.InstantPopup = QtWidgets.QToolButton.InstantPopup
        ns.MenuButtonPopup = QtWidgets.QToolButton.MenuButtonPopup
        ns.AlignTop = QtCore.Qt.AlignTop
        ns.AlignLeft = QtCore.Qt.AlignLeft
        ns.AlignHCenter = QtCore.Qt.AlignHCenter
        ns.ItemIsUserCheckable = QtCore.Qt.ItemIsUserCheckable
        ns.ItemIsUserTristate = QtCore.Qt.ItemIsUserTristate
        ns.Checked = QtCore.Qt.Checked
        ns.Unchecked = QtCore.Qt.Unchecked
        ns.PartiallyChecked = QtCore.Qt.PartiallyChecked
        ns.ReadOnly = QtCore.QFile.ReadOnly
        ns.Text = QtCore.QFile.Text
        ns.East = QtWidgets.QTabWidget.East
        ns.SP_DockWidgetCloseButton = QtWidgets.QStyle.SP_DockWidgetCloseButton
        ns.UpArrow = QtCore.Qt.UpArrow
        ns.Triangular = QtWidgets.QTabWidget.Triangular
        ns.Password = QtWidgets.QLineEdit.Password
        ns.WindowMaximized = QtCore.Qt.WindowMaximized
        ns.SolidLine = QtCore.Qt.SolidLine
        ns.FlatCap = QtCore.Qt.FlatCap
        ns.SquareCap = QtCore.Qt.SquareCap
        ns.RoundCap = QtCore.Qt.RoundCap
        ns.MiterJoin = QtCore.Qt.MiterJoin
        ns.BevelJoin = QtCore.Qt.BevelJoin
        ns.RoundJoin = QtCore.Qt.RoundJoin
        ns.SvgMiterJoin = QtCore.Qt.SvgMiterJoin
        ns.State_HasFocus = QtWidgets.QStyle.State_HasFocus
        ns.State_Selected = QtWidgets.QStyle.State_Selected
        ns.HoverEnter = QtCore.QEvent.HoverEnter
        ns.HoverMove = QtCore.QEvent.HoverMove
        ns.HoverLeave = QtCore.QEvent.HoverLeave
        ns.PlaceholderText = QtGui.QPalette.PlaceholderText
        ns.NoTicks = QtWidgets.QSlider.NoTicks
        ns.TicksAbove = QtWidgets.QSlider.TicksAbove
        ns.TicksBelow = QtWidgets.QSlider.TicksBelow
        ns.TicksBothSides = QtWidgets.QSlider.TicksBothSides
        ns.CC_Slider = QtWidgets.QStyle.CC_Slider
        ns.SC_SliderHandle = QtWidgets.QStyle.SC_SliderHandle
        ns.SC_SliderGroove = QtWidgets.QStyle.SC_SliderGroove
        ns.SP_ArrowBack = QtWidgets.QStyle.SP_ArrowBack
        ns.SP_ArrowDown = QtWidgets.QStyle.SP_ArrowDown
        ns.SP_ArrowForward = QtWidgets.QStyle.SP_ArrowForward
        ns.SP_ArrowLeft = QtWidgets.QStyle.SP_ArrowLeft
        ns.SP_ArrowRight = QtWidgets.QStyle.SP_ArrowRight
        ns.SP_ArrowUp = QtWidgets.QStyle.SP_ArrowUp
        ns.SP_BrowserReload = QtWidgets.QStyle.SP_BrowserReload
        ns.SP_BrowserStop = QtWidgets.QStyle.SP_BrowserStop
        ns.SP_CommandLink = QtWidgets.QStyle.SP_CommandLink
        ns.SP_ComputerIcon = QtWidgets.QStyle.SP_ComputerIcon
        ns.SP_CustomBase = QtWidgets.QStyle.SP_CustomBase
        ns.SP_DesktopIcon = QtWidgets.QStyle.SP_DesktopIcon
        ns.SP_DialogApplyButton = QtWidgets.QStyle.SP_DialogApplyButton
        ns.SP_DialogCancelButton = QtWidgets.QStyle.SP_DialogCancelButton
        ns.SP_DialogCloseButton = QtWidgets.QStyle.SP_DialogCloseButton
        ns.SP_DialogDiscardButton = QtWidgets.QStyle.SP_DialogDiscardButton
        ns.SP_DialogHelpButton = QtWidgets.QStyle.SP_DialogHelpButton
        ns.SP_DialogNoButton = QtWidgets.QStyle.SP_DialogNoButton
        ns.SP_DialogOkButton = QtWidgets.QStyle.SP_DialogOkButton
        ns.SP_DialogOpenButton = QtWidgets.QStyle.SP_DialogOpenButton
        ns.SP_DialogResetButton = QtWidgets.QStyle.SP_DialogResetButton
        ns.SP_DialogSaveButton = QtWidgets.QStyle.SP_DialogSaveButton
        ns.SP_DialogYesButton = QtWidgets.QStyle.SP_DialogYesButton
        ns.SP_DirClosedIcon = QtWidgets.QStyle.SP_DirClosedIcon
        ns.SP_DirHomeIcon = QtWidgets.QStyle.SP_DirHomeIcon
        ns.SP_DirIcon = QtWidgets.QStyle.SP_DirIcon
        ns.SP_DirLinkIcon = QtWidgets.QStyle.SP_DirLinkIcon
        ns.SP_DirLinkOpenIcon = QtWidgets.QStyle.SP_DirLinkOpenIcon
        ns.SP_DirOpenIcon = QtWidgets.QStyle.SP_DirOpenIcon
        ns.SP_DockWidgetCloseButton = QtWidgets.QStyle.SP_DockWidgetCloseButton
        ns.SP_DriveCDIcon = QtWidgets.QStyle.SP_DriveCDIcon
        ns.SP_DriveDVDIcon = QtWidgets.QStyle.SP_DriveDVDIcon
        ns.SP_DriveFDIcon = QtWidgets.QStyle.SP_DriveFDIcon
        ns.SP_DriveHDIcon = QtWidgets.QStyle.SP_DriveHDIcon
        ns.SP_DriveNetIcon = QtWidgets.QStyle.SP_DriveNetIcon
        ns.SP_FileDialogBack = QtWidgets.QStyle.SP_FileDialogBack
        ns.SP_FileDialogContentsView = QtWidgets.QStyle.SP_FileDialogContentsView
        ns.SP_FileDialogDetailedView = QtWidgets.QStyle.SP_FileDialogDetailedView
        ns.SP_FileDialogEnd = QtWidgets.QStyle.SP_FileDialogEnd
        ns.SP_FileDialogInfoView = QtWidgets.QStyle.SP_FileDialogInfoView
        ns.SP_FileDialogListView = QtWidgets.QStyle.SP_FileDialogListView
        ns.SP_FileDialogNewFolder = QtWidgets.QStyle.SP_FileDialogNewFolder
        ns.SP_FileDialogStart = QtWidgets.QStyle.SP_FileDialogStart
        ns.SP_FileDialogToParent = QtWidgets.QStyle.SP_FileDialogToParent
        ns.SP_FileIcon = QtWidgets.QStyle.SP_FileIcon
        ns.SP_FileLinkIcon = QtWidgets.QStyle.SP_FileLinkIcon
        ns.SP_MediaPause = QtWidgets.QStyle.SP_MediaPause
        ns.SP_MediaPlay = QtWidgets.QStyle.SP_MediaPlay
        ns.SP_MediaSeekBackward = QtWidgets.QStyle.SP_MediaSeekBackward
        ns.SP_MediaSeekForward = QtWidgets.QStyle.SP_MediaSeekForward
        ns.SP_MediaSkipBackward = QtWidgets.QStyle.SP_MediaSkipBackward
        ns.SP_MediaSkipForward = QtWidgets.QStyle.SP_MediaSkipForward
        ns.SP_MediaStop = QtWidgets.QStyle.SP_MediaStop
        ns.SP_MediaVolume = QtWidgets.QStyle.SP_MediaVolume
        ns.SP_MediaVolumeMuted = QtWidgets.QStyle.SP_MediaVolumeMuted
        ns.SP_LineEditClearButton = QtWidgets.QStyle.SP_LineEditClearButton
        ns.SP_DialogYesToAllButton = QtWidgets.QStyle.SP_DialogYesToAllButton
        ns.SP_DialogNoToAllButton = QtWidgets.QStyle.SP_DialogNoToAllButton
        ns.SP_DialogSaveAllButton = QtWidgets.QStyle.SP_DialogSaveAllButton
        ns.SP_DialogAbortButton = QtWidgets.QStyle.SP_DialogAbortButton
        ns.SP_DialogRetryButton = QtWidgets.QStyle.SP_DialogRetryButton
        ns.SP_DialogIgnoreButton = QtWidgets.QStyle.SP_DialogIgnoreButton
        ns.SP_RestoreDefaultsButton = QtWidgets.QStyle.SP_RestoreDefaultsButton
        ns.SP_MessageBoxCritical = QtWidgets.QStyle.SP_MessageBoxCritical
        ns.SP_MessageBoxInformation = QtWidgets.QStyle.SP_MessageBoxInformation
        ns.SP_MessageBoxQuestion = QtWidgets.QStyle.SP_MessageBoxQuestion
        ns.SP_MessageBoxWarning = QtWidgets.QStyle.SP_MessageBoxWarning
        ns.SP_TitleBarCloseButton = QtWidgets.QStyle.SP_TitleBarCloseButton
        ns.SP_TitleBarContextHelpButton = QtWidgets.QStyle.SP_TitleBarContextHelpButton
        ns.SP_TitleBarMaxButton = QtWidgets.QStyle.SP_TitleBarMaxButton
        ns.SP_TitleBarMenuButton = QtWidgets.QStyle.SP_TitleBarMenuButton
        ns.SP_TitleBarMinButton = QtWidgets.QStyle.SP_TitleBarMinButton
        ns.SP_TitleBarNormalButton = QtWidgets.QStyle.SP_TitleBarNormalButton
        ns.SP_TitleBarShadeButton = QtWidgets.QStyle.SP_TitleBarShadeButton
        ns.SP_TitleBarUnshadeButton = QtWidgets.QStyle.SP_TitleBarUnshadeButton
        ns.SP_ToolBarHorizontalExtensionButton = QtWidgets.QStyle.SP_ToolBarHorizontalExtensionButton
        ns.SP_ToolBarVerticalExtensionButton = QtWidgets.QStyle.SP_ToolBarVerticalExtensionButton
        ns.SP_TrashIcon = QtWidgets.QStyle.SP_TrashIcon
        ns.SP_VistaShield = QtWidgets.QStyle.SP_VistaShield

    return ns

def get_colors(args, compat):
    '''Create shared colors dependent on the stylesheet.'''

    ns = argparse.Namespace()
    ns.Selected = compat.QtGui.QColor(61, 174, 233)
    ns.PlaceholderColor = compat.QtGui.QColor(255, 0, 0)
    ns.TickColor = compat.QtGui.QColor(255, 0, 0)
    if 'dark' in args.stylesheet:
        ns.GrooveBackground = compat.QtGui.QColor(98, 101, 104)
        ns.GrooveBorder = compat.QtGui.QColor(49, 54, 59)
        ns.HandleBackground = compat.QtGui.QColor(29, 32, 35)
        ns.HandleBorder = compat.QtGui.QColor(98, 101, 104)
        ns.Notch = compat.QtGui.QColor(51, 78, 94)
        ns.PlaceholderColor = compat.QtGui.QColor(118, 121, 124)
        ns.TickColor = compat.QtGui.QColor(51, 78, 94)
    elif 'light' in args.stylesheet:
        ns.GrooveBackground = compat.QtGui.QColor(106, 105, 105, 179)
        ns.GrooveBorder = compat.QtGui.QColor(239, 240, 241)
        ns.HandleBackground = compat.QtGui.QColor(239, 240, 241)
        ns.HandleBorder = compat.QtGui.QColor(106, 105, 105, 179)
        ns.Notch = compat.QtGui.QColor(61, 173, 232, 51)
        ns.PlaceholderColor = compat.QtGui.QColor(186, 185, 184)
        ns.TickColor = compat.QtGui.QColor(61, 173, 232, 51)

    return ns

def get_icon_map(args, compat):
    '''Create a map of standard icons to resource paths.'''

    icon_map = {
        compat.SP_TitleBarMinButton: 'minimize.svg',
        compat.SP_TitleBarMenuButton: 'menu.svg',
        compat.SP_TitleBarMaxButton: 'maximize.svg',
        compat.SP_TitleBarCloseButton: 'window_close.svg',
        compat.SP_TitleBarNormalButton: 'restore.svg',
        compat.SP_TitleBarShadeButton: 'shade.svg',
        compat.SP_TitleBarUnshadeButton: 'unshade.svg',
        compat.SP_TitleBarContextHelpButton: 'help.svg',
        compat.SP_MessageBoxInformation: 'message_information.svg',
        compat.SP_MessageBoxWarning: 'message_warning.svg',
        compat.SP_MessageBoxCritical: 'message_critical.svg',
        compat.SP_MessageBoxQuestion: 'message_question.svg',
        compat.SP_DesktopIcon: 'desktop.svg',
        compat.SP_TrashIcon: 'trash.svg',
        compat.SP_ComputerIcon: 'computer.svg',
        compat.SP_DriveFDIcon: 'floppy_drive.svg',
        compat.SP_DriveHDIcon: 'hard_drive.svg',
        compat.SP_DriveCDIcon: 'disc_drive.svg',
        compat.SP_DriveDVDIcon: 'disc_drive.svg',
        compat.SP_DriveNetIcon: 'network_drive.svg',
        compat.SP_DirHomeIcon: 'home_directory.svg',
        compat.SP_DirOpenIcon: 'folder_open.svg',
        compat.SP_DirClosedIcon: 'folder.svg',
        compat.SP_DirIcon: 'folder.svg',
        compat.SP_DirLinkIcon: 'folder_link.svg',
        compat.SP_DirLinkOpenIcon: 'folder_open_link.svg',
        compat.SP_FileIcon: 'file.svg',
        compat.SP_FileLinkIcon: 'file_link.svg',
        compat.SP_FileDialogStart: 'file_dialog_start.svg',
        compat.SP_FileDialogEnd: 'file_dialog_end.svg',
        compat.SP_FileDialogToParent: 'up_arrow.svg',
        compat.SP_FileDialogNewFolder: 'folder.svg',
        compat.SP_FileDialogDetailedView: 'file_dialog_detailed.svg',
        compat.SP_FileDialogInfoView: 'file_dialog_info.svg',
        compat.SP_FileDialogContentsView: 'file_dialog_contents.svg',
        compat.SP_FileDialogListView: 'file_dialog_list.svg',
        compat.SP_FileDialogBack: 'left_arrow.svg',
        compat.SP_DockWidgetCloseButton: 'close.svg',
        compat.SP_ToolBarHorizontalExtensionButton: 'horizontal_extension.svg',
        compat.SP_ToolBarVerticalExtensionButton: 'vertical_extension.svg',
        compat.SP_DialogOkButton: 'dialog_ok.svg',
        compat.SP_DialogCancelButton: 'dialog_cancel.svg',
        compat.SP_DialogHelpButton: 'dialog_help.svg',
        compat.SP_DialogOpenButton: 'dialog_open.svg',
        compat.SP_DialogSaveButton: 'dialog_save.svg',
        compat.SP_DialogCloseButton: 'dialog_close.svg',
        compat.SP_DialogApplyButton: 'dialog_apply.svg',
        compat.SP_DialogResetButton: 'dialog_reset.svg',
        compat.SP_DialogDiscardButton: 'dialog_discard.svg',
        compat.SP_DialogYesButton: 'dialog_apply.svg',
        compat.SP_DialogNoButton: 'dialog_no.svg',
        compat.SP_ArrowUp: 'up_arrow.svg',
        compat.SP_ArrowDown: 'down_arrow.svg',
        compat.SP_ArrowLeft: 'left_arrow.svg',
        compat.SP_ArrowRight: 'right_arrow.svg',
        compat.SP_ArrowBack: 'left_arrow.svg',
        compat.SP_ArrowForward: 'right_arrow.svg',
        compat.SP_CommandLink: 'right_arrow.svg',
        compat.SP_VistaShield: 'vista_shield.svg',
        compat.SP_BrowserReload: 'browser_refresh.svg',
        compat.SP_BrowserStop: 'browser_refresh_stop.svg',
        compat.SP_MediaPlay: 'play.svg',
        compat.SP_MediaStop: 'stop.svg',
        compat.SP_MediaPause: 'pause.svg',
        compat.SP_MediaSkipForward: 'skip_backward.svg',
        compat.SP_MediaSkipBackward: 'skip_forward.svg',
        compat.SP_MediaSeekForward: 'seek_forward.svg',
        compat.SP_MediaSeekBackward: 'seek_backward.svg',
        compat.SP_MediaVolume: 'volume.svg',
        compat.SP_MediaVolumeMuted: 'volume_muted.svg',
        compat.SP_LineEditClearButton: 'clear_text.svg',
        compat.SP_DialogYesToAllButton: 'dialog_yes_to_all.svg',
        compat.SP_DialogNoToAllButton: 'dialog_no.svg',
        compat.SP_DialogSaveAllButton: 'dialog_save_all.svg',
        compat.SP_DialogAbortButton: 'dialog_cancel.svg',
        compat.SP_DialogRetryButton: 'dialog_retry.svg',
        compat.SP_DialogIgnoreButton: 'dialog_ignore.svg',
        compat.SP_RestoreDefaultsButton: 'restore_defaults.svg',
    }
    if compat.QtCore.QT_VERSION >= 393984:
        icon_map[compat.SP_TabCloseButton] = 'tab_close.svg'

    return icon_map

def setup_app(args, unknown, compat, style_class=None):
    '''Setup code for the Qt application.'''

    if args.scale != 1:
        os.environ['QT_SCALE_FACTOR'] = str(args.scale)
    else:
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

    app = compat.QtWidgets.QApplication(sys.argv[:1] + unknown)
    if args.style != 'native':
        style = compat.QtWidgets.QStyleFactory.create(args.style)
        if style_class is not None:
            style = style_class(style)
        app.setStyle(style)

    window = compat.QtWidgets.QMainWindow()

    # use the default font size
    font = app.font()
    if args.font_size > 0:
        font.setPointSizeF(args.font_size)
    if args.font_family:
        font.setFamily(args.font_family)
    app.setFont(font)

    return app, window

def exec_app(args, app, window, compat):
    '''Show and execute the Qt application.'''

    # setup stylesheet
    if args.stylesheet != 'native':
        resource_format = get_resources(args)
        stylesheet = get_stylesheet(resource_format)
        file = compat.QtCore.QFile(stylesheet)
        file.open(compat.ReadOnly | compat.Text)
        stream = compat.QtCore.QTextStream(file)
        app.setStyleSheet(stream.readAll())

    window.show()
    return execute(args, app)

def execute(args, widget):
    '''Shared code to call `exec()` on a widget.'''

    if args.pyqt6:
        return widget.exec()
    return widget.exec_()

def native_icon(style, icon, option=None, widget=None):
    '''Get a standard icon for the native style'''
    return style.standardIcon(icon, option, widget)

def stylesheet_icon(args, style, icon, icon_map, option=None, widget=None):
    '''Get a standard icon for the stylesheet style'''

    if args.pyqt6:
        from PyQt6 import QtCore, QtGui, QtWidgets
    else:
        from PyQt5 import QtCore, QtGui, QtWidgets

    path = icon_map[icon]
    resource_format = get_resources(args)
    resource = f'{resource_format}{path}'
    if QtCore.QFile.exists(resource):
        return QtGui.QIcon(resource)
    return QtWidgets.QCommonStyle.standardIcon(style, icon, option, widget)

def style_icon(args, style, icon, icon_map, option=None, widget=None):
    '''Get the stylized icon, either native or in the stylesheet.'''

    if args.stylesheet == 'native':
        return native_icon(style, icon, option, widget)
    return stylesheet_icon(args, style, icon, icon_map, option, widget)
