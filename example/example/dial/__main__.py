#!/usr/bin/env python
"""
Example showing how to override the `paintEvent` and `eventFilter`
for a `QDial`, creating a visually consistent, stylish `QDial` that
supports highlighting the handle on the active or hovered dial.
"""

import sys

from example._util.qt import PyQtApplication
from example.dial import ARGS, UNKNOWN, Qt, Ui


def main():
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)

    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("QDial")
    window.resize(400, 150)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
