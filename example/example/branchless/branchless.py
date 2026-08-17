from collections.abc import Iterable
from typing import TYPE_CHECKING

from pathlib import Path

from .cli import ARGS, Qt

if TYPE_CHECKING:
    from example._util.typing import QtCore, QtWidgets

BRANCHLESS_DIR = Path(__file__).absolute().parent


def set_stylesheet(app: "QtWidgets.QApplication") -> "None":
    """Set the application stylesheet."""

    if ARGS.stylesheet.name != "native":
        ext_path = BRANCHLESS_DIR / "stylesheet.qss.in"
        stylesheet = ARGS.stylesheet.read(Qt)
        stylesheet += "\n" + ext_path.read_text(encoding="utf-8")
        app.setStyleSheet(stylesheet)


def get_treeviews(parent: "QtCore.QObject", depth: "int" = 1000) -> "Iterable[QtWidgets.QTreeView]":
    """Recursively get all tree views."""

    for child in parent.children():
        if isinstance(child, Qt.QtWidgets.QTreeView):
            yield child
        elif depth > 0:
            yield from get_treeviews(child, depth - 1)
