#!/usr/bin/env python
"""
Example showing how to override the `paintEvent` and `eventFilter`
for a `QLCDNumber`, creating a visually consistent, stylish
`QLCDNumber` that supports highlighting the handle on the active
or hovered number.
"""

import sys

from example._util.qt import PyQtApplication
from example.lcd import ARGS, UNKNOWN, Qt, Ui


def main() -> None:
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)

    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("QLCDNumber")
    window.resize(400, 150)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
