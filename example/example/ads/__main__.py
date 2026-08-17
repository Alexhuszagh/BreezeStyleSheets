#!/usr/bin/env python
"""Simple PyQt application using the advanced-docking-system."""

import sys

from example._util.qt import PyQtApplication
from example.ads import ARGS, UNKNOWN, Qt, Ui


def main() -> None:
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)

    ui = Ui()
    ui.setup(window)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
