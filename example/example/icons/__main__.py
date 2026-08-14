#!/usr/bin/env python
"""Example overriding QCommonStyle for custom standard icons."""

import sys

from example._util.qt import PyQtApplication
from example.icons import ARGS, UNKNOWN, Qt, StandardIconStyle, Ui


def main():
    app, window = Qt.create_application(ARGS, UNKNOWN, style_class=StandardIconStyle)
    ARGS.stylesheet.load(Qt)

    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("Custom standard icons.")

    ui.action_action.triggered.connect(ui.about)
    ui.action_action_c.triggered.connect(ui.critical)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
