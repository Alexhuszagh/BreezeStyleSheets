from typing import TYPE_CHECKING

from .cli import ARGS, COLORS, Qt

if TYPE_CHECKING:
    from PyQt6 import QtGui, QtWidgets


class Ui:
    def setup(self, window: "QtWidgets.QMainWindow") -> None:
        url = "https://github.com/Alexhuszagh/BreezeStyleSheets"
        window.setObjectName("MainWindow")
        window.resize(400, 200)
        self.central_widget = Qt.QtWidgets.QWidget(window)
        self.central_widget.setObjectName("centralwidget")
        self.layout = Qt.QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setObjectName("layout")
        self.layout.setAlignment(Qt.QtCore.Qt.AlignmentFlag.AlignLeft)
        window.setCentralWidget(self.central_widget)

        self.repository = Qt.QtWidgets.QLabel(self.central_widget)
        self.repository.setObjectName("repository")
        self.repository.setText(f"[BreezeStyleSheets]({url})")
        self.repository.setTextFormat(Qt.QtCore.Qt.TextFormat.MarkdownText)
        self.repository.setTextInteractionFlags(Qt.QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.repository.setOpenExternalLinks(True)
        self.layout.addWidget(self.repository)

        self.issues = Qt.QtWidgets.QLabel(self.central_widget)
        self.issues.setObjectName("issues")
        self.issues.setText(f"[Issues]({url}/issues)")
        self.issues.setTextFormat(Qt.QtCore.Qt.TextFormat.MarkdownText)
        self.issues.setTextInteractionFlags(Qt.QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.issues.setOpenExternalLinks(True)
        self.layout.addWidget(self.issues)

        self.pulls = Qt.QtWidgets.QLabel(self.central_widget)
        self.pulls.setObjectName("pulls")
        self.pulls.setText(f"[Pull Requests]({url}/pulls)")
        self.pulls.setTextFormat(Qt.QtCore.Qt.TextFormat.MarkdownText)
        self.pulls.setTextInteractionFlags(Qt.QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        self.pulls.setOpenExternalLinks(True)
        self.layout.addWidget(self.pulls)

        # Set the palettes.
        if ARGS.set_widget_palette:
            self.set_link_palette(self.repository)
            self.set_link_palette(self.issues)
            self.set_link_palette(self.pulls)

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
    def set_link_palette(obj: "QtWidgets.QWidget | QtWidgets.QApplication") -> None:
        """Set the palette for a link type."""

        role = Qt.QtGui.QPalette.ColorRole.Link
        color = Qt.QtGui.QColor(*COLORS.link_color)
        Ui.set_palette(obj, role, color)

        role = Qt.QtGui.QPalette.ColorRole.LinkVisited
        color = Qt.QtGui.QColor(*COLORS.link_visited_color)
        Ui.set_palette(obj, role, color)
