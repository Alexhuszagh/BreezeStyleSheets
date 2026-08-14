from typing import TYPE_CHECKING

from .cli import ARGS, Qt

if TYPE_CHECKING:
    import PySide6QtAds as QtAds  # type: ignore
    from PyQt6 import QtWidgets
elif ARGS.qt_framework == "pyqt6":
    import PyQt6Ads as QtAds
elif ARGS.qt_framework == "pyside6":
    import PySide6QtAds as QtAds
else:
    raise ValueError('Only the Qt frameworks "pyqt6" and "pyside6" are supported.')


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        # setup the dock manager
        window.setObjectName("MainWindow")
        window.resize(1068, 824)
        widget = Qt.QtWidgets.QWidget(window)
        window.setCentralWidget(widget)

        if ARGS.focus_highlighting:
            QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.FocusHighlighting, True)

        dock_manager = QtAds.CDockManager(window)

        # add widgets to the dock manager
        label_widget = QtAds.CDockWidget("Dock")
        label = Qt.QtWidgets.QLabel("Some label")
        label_widget.setWidget(label)
        dock_area = dock_manager.setCentralWidget(label_widget)
        dock_area.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

        list_widget = QtAds.CDockWidget("List")
        lst = Qt.QtWidgets.QListWidget()
        for index in range(10):
            lst.addItem(Qt.QtWidgets.QListWidgetItem(f"Item {index + 1}"))
        list_widget.setWidget(lst)
        min_size_hint = QtAds.CDockWidget.eMinimumSizeHintMode.MinimumSizeHintFromDockWidget
        list_widget.setMinimumSizeHintMode(min_size_hint)
        dock_manager.addDockWidget(QtAds.DockWidgetArea.LeftDockWidgetArea, list_widget, dock_area)

        table_widget = QtAds.CDockWidget("Table")
        table = Qt.QtWidgets.QTableWidget()
        # make sure we have both scroll areas active.
        table.setColumnCount(40)
        table.setRowCount(40)
        table_widget.setWidget(table)
        table_widget.setMinimumSizeHintMode(min_size_hint)
        dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, table_widget, dock_area)

        tab_widget = QtAds.CDockWidget("Tab Widget")
        tab = Qt.QtWidgets.QTabWidget()
        tab.setTabPosition(Qt.QtWidgets.QTabWidget.TabPosition.North)
        tab.addTab(Qt.QtWidgets.QWidget(), "Tab 1")
        tab.addTab(Qt.QtWidgets.QWidget(), "Tab 2")
        tab.addTab(Qt.QtWidgets.QWidget(), "Tab 3")
        tab_widget.setWidget(tab)
        tab_widget.setMinimumSizeHintMode(min_size_hint)
        dock_manager.addDockWidget(QtAds.DockWidgetArea.BottomDockWidgetArea, tab_widget, dock_area)

        if not ARGS.use_internal:
            dock_manager.setStyleSheet("")

        window.setWindowState(Qt.QtCore.Qt.WindowState.WindowMaximized)
