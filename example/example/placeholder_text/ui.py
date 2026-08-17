from typing import TYPE_CHECKING

from .cli import ARGS, COLORS, Qt

if TYPE_CHECKING:
    from PyQt6 import QtGui, QtWidgets


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        window.setObjectName("MainWindow")
        self.central_widget = Qt.QtWidgets.QWidget(window)
        self.central_widget.setObjectName("centralwidget")
        self.layout = Qt.QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setObjectName("layout")
        self.layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignHCenter)
        window.setCentralWidget(self.central_widget)

        self.text_edit = Qt.QtWidgets.QTextEdit(self.central_widget)
        self.text_edit.setObjectName("textEdit")
        self.text_edit.setPlaceholderText("Placeholder Text")
        self.layout.addWidget(self.text_edit)

        self.plain_text_edit = Qt.QtWidgets.QPlainTextEdit(self.central_widget)
        self.plain_text_edit.setObjectName("plainTextEdit")
        self.plain_text_edit.setPlaceholderText("Placeholder Text")
        self.layout.addWidget(self.plain_text_edit)

        self.line_edit = Qt.QtWidgets.QLineEdit(self.central_widget)
        self.line_edit.setObjectName("lineEdit")
        self.line_edit.setPlaceholderText("Placeholder Text")
        self.layout.addWidget(self.line_edit)

        if ARGS.set_widget_palette:
            self.set_placeholder_palette(self.text_edit)
            self.set_placeholder_palette(self.plain_text_edit)
            self.set_placeholder_palette(self.line_edit)

    @staticmethod
    def set_palette(
        obj: "QtWidgets.QWidget | QtWidgets.QApplication",
        role: "QtGui.QPalette.ColorRole",
        color: "QtGui.QColor",
    ):
        """Set the palette for a widget/application."""
        palette = obj.palette()
        palette.setColor(role, color)
        obj.setPalette(palette)

    @staticmethod
    def set_placeholder_palette(obj: "QtWidgets.QWidget | QtWidgets.QApplication") -> None:
        """Set the palette for the placeholder text. This only works in Qt5."""
        role = Qt.QtGui.QPalette.ColorRole.PlaceholderText
        color = Qt.QtGui.QColor(*COLORS.placeholder_color)
        Ui.set_palette(obj, role, color)
