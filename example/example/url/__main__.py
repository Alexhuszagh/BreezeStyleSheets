#!/usr/bin/env python
"""Example stylizing URLs using palettes."""

import sys

from example._util.qt import PyQtApplication
from example.url import ARGS, UNKNOWN, Qt, Ui


def main():
    "Application entry point"

    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)
    if ARGS.set_app_palette:
        Ui.set_link_palette(app)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("Stylized URL colors.")
    window.resize(200, 100)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
