from typing import TYPE_CHECKING

from .cli import Qt
from .slider import Slider

if TYPE_CHECKING:
    from PyQt6 import QtWidgets


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

        self.slider = Slider(self.central_widget)
        self.slider.setOrientation(Qt.QtCore.Qt.Orientation.Horizontal)
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(Qt.QtWidgets.QSlider.TickPosition.TicksAbove)
        self.slider.setObjectName("slider")
        self.layout.addWidget(self.slider)
