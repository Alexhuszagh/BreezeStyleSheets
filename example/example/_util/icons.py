"""Standard and custom icons."""

from typing import TYPE_CHECKING

from .qt import PyQt

if TYPE_CHECKING:
    from .typing import QtWidgets


def get_standard_icons(qt: PyQt) -> "dict[QtWidgets.QStyle.StandardPixmap, str]":
    """Create a map of standard icons to resource paths."""

    icon_map = {
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarMinButton: "minimize.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarMenuButton: "menu.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarMaxButton: "maximize.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton: "window_close.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarNormalButton: "restore.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarShadeButton: "shade.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarUnshadeButton: "unshade.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TitleBarContextHelpButton: "help.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MessageBoxInformation: "message_information.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MessageBoxWarning: "message_warning.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MessageBoxCritical: "message_critical.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion: "message_question.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DesktopIcon: "desktop.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_TrashIcon: "trash.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ComputerIcon: "computer.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DriveFDIcon: "floppy_drive.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DriveHDIcon: "hard_drive.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DriveCDIcon: "disc_drive.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DriveDVDIcon: "disc_drive.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DriveNetIcon: "network_drive.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DirHomeIcon: "home_directory.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DirOpenIcon: "folder_open.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DirClosedIcon: "folder.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DirIcon: "folder.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DirLinkIcon: "folder_link.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DirLinkOpenIcon: "folder_open_link.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileIcon: "file.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileLinkIcon: "file_link.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogStart: "file_dialog_start.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogEnd: "file_dialog_end.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogToParent: "up_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogNewFolder: "folder.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogDetailedView: "file_dialog_detailed.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogInfoView: "file_dialog_info.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogContentsView: "file_dialog_contents.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogListView: "file_dialog_list.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_FileDialogBack: "left_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DockWidgetCloseButton: "close.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton: "horizontal_extension.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ToolBarVerticalExtensionButton: "vertical_extension.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogOkButton: "dialog_ok.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogCancelButton: "dialog_cancel.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogHelpButton: "dialog_help.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogOpenButton: "dialog_open.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogSaveButton: "dialog_save.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogCloseButton: "dialog_close.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogApplyButton: "dialog_apply.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogResetButton: "dialog_reset.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogDiscardButton: "dialog_discard.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogYesButton: "dialog_apply.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogNoButton: "dialog_no.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowUp: "up_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowDown: "down_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowLeft: "left_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowRight: "right_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowBack: "left_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_ArrowForward: "right_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_CommandLink: "right_arrow.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_VistaShield: "vista_shield.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_BrowserReload: "browser_refresh.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_BrowserStop: "browser_refresh_stop.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaPlay: "play.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaStop: "stop.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaPause: "pause.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaSkipForward: "skip_backward.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaSkipBackward: "skip_forward.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaSeekForward: "seek_forward.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaSeekBackward: "seek_backward.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaVolume: "volume.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_MediaVolumeMuted: "volume_muted.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_LineEditClearButton: "clear_text.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogYesToAllButton: "dialog_yes_to_all.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogNoToAllButton: "dialog_no.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogSaveAllButton: "dialog_save_all.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogAbortButton: "dialog_cancel.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogRetryButton: "dialog_retry.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_DialogIgnoreButton: "dialog_ignore.svg",
        qt.QtWidgets.QStyle.StandardPixmap.SP_RestoreDefaultsButton: "restore_defaults.svg",
    }
    if qt.version > (6, 3, 0):
        icon_map[qt.QtWidgets.QStyle.StandardPixmap.SP_TabCloseButton] = "tab_close.svg"

    return icon_map
