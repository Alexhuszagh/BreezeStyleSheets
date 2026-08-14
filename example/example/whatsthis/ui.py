from typing import TYPE_CHECKING

from .cli import Qt

if TYPE_CHECKING:
    from PyQt6 import QtWidgets


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        window.setObjectName("MainWindow")
        self.central_widget = Qt.QtWidgets.QWidget(window)
        self.central_widget.setObjectName("centralwidget")
        self.layout = Qt.QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setObjectName("layout")
        self.layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignHCenter)
        window.setCentralWidget(self.central_widget)

        self.toolbar = Qt.QtWidgets.QToolBar("Toolbar")
        self.toolbar.setOrientation(Qt.QtCore.Qt.Orientation.Vertical)
        self.action = Qt.QtGui.QAction("&Action 1", window)
        self.action.setWhatsThis("Example action")
        self.toolbar.addAction(self.action)
        self.toolbar.addAction(Qt.QtWidgets.QWhatsThis.createAction(self.toolbar))
        window.addToolBar(Qt.QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolbar)
