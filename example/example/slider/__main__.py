#!/usr/bin/env python
"""
Example showing how to add ticks to a QSlider. Note that this does
not work with stylesheets, so it's merely an example of how to
get customized styling behavior with a QSlider.
"""

import sys

from example._util.qt import PyQtApplication
from example.slider import ARGS, UNKNOWN, Qt, Ui


def main():
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)

    ui = Ui()
    ui.setup(window)
    window.setWindowTitle("QSlider with Ticks.")
    window.resize(400, 150)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
