#!/usr/bin/env python
"""Example stylizing the tooltip base and text for QWhatsThis using palettes."""

import sys

from example._util.qt import PyQtApplication
from example.whatsthis import ARGS, COLORS, UNKNOWN, Qt, Ui


def main():
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)

    palette = app.palette()
    palette.setColor(Qt.QtGui.QPalette.ColorRole.ToolTipBase, Qt.QtGui.QColor(*COLORS.tooltip_base))
    palette.setColor(Qt.QtGui.QPalette.ColorRole.ToolTipText, Qt.QtGui.QColor(*COLORS.tooltip_text))
    app.setPalette(palette)

    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("A WhatsThis dialog.")
    window.resize(1068, 824)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
