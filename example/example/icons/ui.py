from typing import TYPE_CHECKING, cast

from example._util.style import style_icon
from .cli import ARGS, STANDARD_ICONS, Qt

if TYPE_CHECKING:
    from .._util.typing import QtWidgets


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        window.setObjectName("MainWindow")
        window.resize(1068, 824)
        self.central_widget = Qt.QtWidgets.QWidget(window)
        self.central_widget.setObjectName("centralwidget")
        self.layout = Qt.QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setObjectName("layout")
        self.layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignHCenter)
        window.setCentralWidget(self.central_widget)

        self.tool_box = Qt.QtWidgets.QToolBox(self.central_widget)
        self.page1 = Qt.QtWidgets.QListWidget()
        self.tool_box.addItem(self.page1, "Overwritten Icons")
        self.layout.addWidget(self.tool_box)

        self._add_standard_buttons(
            self.page1,
            [
                "SP_ArrowLeft",
                "SP_ArrowDown",
                "SP_ArrowRight",
                "SP_ArrowUp",
                "SP_DockWidgetCloseButton",
                "SP_DialogCancelButton",
                "SP_DialogCloseButton",
                "SP_DialogDiscardButton",
                "SP_DialogHelpButton",
                "SP_DialogNoButton",
                "SP_DialogOkButton",
                "SP_DialogOpenButton",
                "SP_DialogResetButton",
                "SP_DialogSaveButton",
            ],
        )

        self.page2 = Qt.QtWidgets.QListWidget()
        self.tool_box.addItem(self.page2, "Default Icons")
        self.layout.addWidget(self.tool_box)

        default_icons = [
            "SP_TitleBarMinButton",
            "SP_TitleBarMenuButton",
            "SP_TitleBarMaxButton",
            "SP_TitleBarCloseButton",
            "SP_TitleBarNormalButton",
            "SP_TitleBarShadeButton",
            "SP_TitleBarUnshadeButton",
            "SP_TitleBarContextHelpButton",
            "SP_MessageBoxInformation",
            "SP_MessageBoxWarning",
            "SP_MessageBoxCritical",
            "SP_MessageBoxQuestion",
            "SP_DesktopIcon",
            "SP_TrashIcon",
            "SP_ComputerIcon",
            "SP_DriveFDIcon",
            "SP_DriveHDIcon",
            "SP_DriveCDIcon",
            "SP_DriveDVDIcon",
            "SP_DriveNetIcon",
            "SP_DirHomeIcon",
            "SP_DirOpenIcon",
            "SP_DirClosedIcon",
            "SP_DirIcon",
            "SP_DirLinkIcon",
            "SP_DirLinkOpenIcon",
            "SP_FileIcon",
            "SP_FileLinkIcon",
            "SP_FileDialogStart",
            "SP_FileDialogEnd",
            "SP_FileDialogToParent",
            "SP_FileDialogNewFolder",
            "SP_FileDialogDetailedView",
            "SP_FileDialogInfoView",
            "SP_FileDialogContentsView",
            "SP_FileDialogListView",
            "SP_FileDialogBack",
            "SP_ToolBarHorizontalExtensionButton",
            "SP_ToolBarVerticalExtensionButton",
            "SP_DialogApplyButton",
            "SP_DialogYesButton",
            "SP_ArrowBack",
            "SP_ArrowForward",
            "SP_CommandLink",
            "SP_VistaShield",
            "SP_BrowserReload",
            "SP_BrowserStop",
            "SP_MediaPlay",
            "SP_MediaStop",
            "SP_MediaPause",
            "SP_MediaSkipForward",
            "SP_MediaSkipBackward",
            "SP_MediaSeekForward",
            "SP_MediaSeekBackward",
            "SP_MediaVolume",
            "SP_MediaVolumeMuted",
            "SP_LineEditClearButton",
            "SP_DialogYesToAllButton",
            "SP_DialogNoToAllButton",
            "SP_DialogSaveAllButton",
            "SP_DialogAbortButton",
            "SP_DialogRetryButton",
            "SP_DialogIgnoreButton",
            "SP_RestoreDefaultsButton",
        ]
        if Qt.version >= (6, 3, 0):
            default_icons.append("SP_TabCloseButton")
        self._add_standard_buttons(self.page2, default_icons)

        self.dock_widget1 = Qt.QtWidgets.QDockWidget(window)
        self.dock_widget1.setObjectName("dockWidget1")
        self.dock_widget_contents = Qt.QtWidgets.QWidget()
        self.dock_widget_contents.setObjectName("dockWidgetContents")
        self.dock_widget1.setWidget(self.dock_widget_contents)
        window.addDockWidget(Qt.QtCore.Qt.DockWidgetArea(1), self.dock_widget1)

        self.vertical_layout_2 = Qt.QtWidgets.QVBoxLayout(self.dock_widget_contents)
        self.vertical_layout_2.setObjectName("verticalLayout_2")
        self.vertical_layout = Qt.QtWidgets.QVBoxLayout()
        self.vertical_layout.setObjectName("verticalLayout")
        self.combo_box = Qt.QtWidgets.QComboBox(self.dock_widget_contents)
        self.combo_box.setObjectName("comboBox")
        self.combo_box.setEditable(True)
        self.combo_box.addItem("First")
        self.combo_box.addItem("Second")
        self.vertical_layout.addWidget(self.combo_box)
        self.horizontal_slider = Qt.QtWidgets.QSlider(self.dock_widget_contents)
        self.horizontal_slider.setOrientation(Qt.QtCore.Qt.Orientation.Horizontal)
        self.horizontal_slider.setObjectName("horizontalSlider")
        self.vertical_layout.addWidget(self.horizontal_slider)
        self.text_edit = Qt.QtWidgets.QTextEdit(self.dock_widget_contents)
        self.text_edit.setObjectName("textEdit")
        self.vertical_layout.addWidget(self.text_edit)
        self.line = Qt.QtWidgets.QFrame(self.dock_widget_contents)
        self.line.setFrameShape(Qt.QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(Qt.QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.vertical_layout.addWidget(self.line)
        self.progress_bar = Qt.QtWidgets.QProgressBar(self.dock_widget_contents)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progressBar")
        self.vertical_layout.addWidget(self.progress_bar)
        self.vertical_layout_2.addLayout(self.vertical_layout)

        self.menubar = Qt.QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(Qt.QtCore.QRect(0, 0, 1068, 29))
        self.menubar.setObjectName("menubar")
        self.menu_menu = Qt.QtWidgets.QMenu(self.menubar)
        self.menu_menu.setObjectName("menuMenu")
        window.setMenuBar(self.menubar)
        self.statusbar = Qt.QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        self.action_action = Qt.QtGui.QAction(window)
        self.action_action.setObjectName("actionAction")
        self.action_action_c = Qt.QtGui.QAction(window)
        self.action_action_c.setObjectName("actionAction_C")

        self.menu_menu.addAction(self.action_action)
        self.menu_menu.addAction(self.action_action_c)
        self.menubar.addAction(self.menu_menu.menuAction())
        Qt.QtCore.QMetaObject.connectSlotsByName(window)

        self.retranslate_ui(window)

    def retranslate_ui(self, window: "QtWidgets.QMainWindow") -> None:
        """Retranslate our UI after initializing some of our base modules."""

        _translate = Qt.QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_menu.setTitle(_translate("MainWindow", "&Menu"))
        self.action_action.setText(_translate("MainWindow", "&Action"))
        self.action_action_c.setText(_translate("MainWindow", "Action &C"))

    def about(self) -> None:
        Qt.QtWidgets.QMessageBox.aboutQt(self.central_widget, "About Menu")

    def critical(self) -> None:
        Qt.QtWidgets.QMessageBox.critical(self.central_widget, "Error", "Critical Error")

    def _add_standard_button(self, layout: "QtWidgets.QLayout", name: str, index: int) -> None:
        """Create and add a QToolButton with a standard icon."""

        button = Qt.QtWidgets.QToolButton(self.central_widget)
        setattr(self, f"button{index}", button)
        button.setAutoRaise(True)

        style = button.style()
        assert style is not None
        pixmap = getattr(Qt.QtWidgets.QStyle.StandardPixmap, name)
        pixmap = cast("QtWidgets.QStyle.StandardPixmap", pixmap)
        icon = style_icon(style, Qt, STANDARD_ICONS, ARGS, pixmap, widget=button)

        button.setIcon(icon)
        button.setObjectName(f"button{index}")
        layout.addWidget(button)

    def _add_standard_buttons(self, page: "QtWidgets.QListWidget", names: "list[str]") -> None:
        """Create and add QToolButtons with standard icons to the UI."""

        style = page.style()
        assert style is not None
        for name in names:
            pixmap = getattr(Qt.QtWidgets.QStyle.StandardPixmap, name)
            pixmap = cast("QtWidgets.QStyle.StandardPixmap", pixmap)
            icon = style_icon(style, Qt, STANDARD_ICONS, ARGS, pixmap, widget=page)
            item = Qt.QtWidgets.QListWidgetItem(icon, name)
            page.addItem(item)
