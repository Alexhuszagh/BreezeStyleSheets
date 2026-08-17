from typing import TYPE_CHECKING

from .cli import ARGS, Qt
from .dial import Dial

if TYPE_CHECKING:
    from .._util.typing import QtWidgets


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        window.setObjectName("MainWindow")
        window.resize(1068, 824)
        self.central_widget = Qt.QtWidgets.QWidget(window)
        self.central_widget.setObjectName("centralwidget")
        self.layout = Qt.QtWidgets.QHBoxLayout(self.central_widget)
        self.layout.setObjectName("layout")
        if not ARGS.no_align:
            self.layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignVCenter)
        window.setCentralWidget(self.central_widget)

        self.dial1 = Dial(self.central_widget)
        self.layout.addWidget(self.dial1)

        self.dial2 = Dial(self.central_widget)
        self.dial2.setNotchesVisible(True)
        self.layout.addWidget(self.dial2)

        self.dial3 = Dial(self.central_widget)
        self.dial3.setWrapping(True)
        self.layout.addWidget(self.dial3)
