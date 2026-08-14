from typing import TYPE_CHECKING

from .cli import ARGS, Qt
from .lcd import LCD

if TYPE_CHECKING:
    from PyQt6 import QtWidgets


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        window.setObjectName("MainWindow")
        window.resize(1068, 824)
        self.central_widget = Qt.QtWidgets.QWidget(window)
        self.layout = Qt.QtWidgets.QHBoxLayout(self.central_widget)
        self.layout.setSpacing(0)
        if not ARGS.no_align:
            self.layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignVCenter)
        window.setCentralWidget(self.central_widget)

        self.lcd1 = LCD(self.central_widget)
        self.lcd1.display(15)
        self.lcd1.setDigitCount(2)
        self.layout.addWidget(self.lcd1)

        self.lcd2 = LCD(self.central_widget)
        self.lcd2.display(31)
        self.lcd2.setHexMode()
        self.lcd2.setDigitCount(2)
        self.layout.addWidget(self.lcd2)

        self.lcd3 = LCD(self.central_widget)
        self.lcd3.display(15)
        self.lcd3.setSegmentStyle(Qt.QtWidgets.QLCDNumber.SegmentStyle.Outline)
        self.lcd3.setFrameShape(Qt.QtWidgets.QFrame.Shape.NoFrame)
        self.lcd3.setDigitCount(2)
        self.layout.addWidget(self.lcd3)

        self.lcd4 = LCD(self.central_widget)
        self.lcd4.display(15)
        self.lcd4.setSegmentStyle(Qt.QtWidgets.QLCDNumber.SegmentStyle.Flat)
        self.lcd4.setFrameShape(Qt.QtWidgets.QFrame.Shape.NoFrame)
        self.lcd4.setDigitCount(2)
        self.layout.addWidget(self.lcd4)
