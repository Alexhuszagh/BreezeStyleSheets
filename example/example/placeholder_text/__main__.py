#!/usr/bin/env python
"""
Demo of using placeholder text.

Example showing how to style the placeholder text for QLineEdit,
QTextEdit, and QPlainTextEdit, since in Qt6 is can be styled as
the default text color. This seems to be an issue with palettes for
Qt6 in `QPalette::PlaceholderText`, since both the stylesheets
and palette edits correctly affect styles in Qt5, but not Qt6.
"""

import sys

from example._util.qt import PyQtApplication
from example.placeholder_text import ARGS, UNKNOWN, Qt, Ui


def main() -> None:
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)
    if ARGS.set_app_palette:
        Ui.set_placeholder_palette(app)

    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("Placeholder text")
    window.resize(1068, 824)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
