#!/usr/bin/env python
"""Simple example showing numerous built-in widgets."""

import sys

from example._util.qt import PyQtApplication
from example.widgets import ARGS, UNKNOWN, Qt, Ui


def main() -> None:
    app, window = Qt.create_application(ARGS, UNKNOWN)
    ARGS.stylesheet.load(Qt)

    ui = Ui()
    ui.setup(window)
    window.resize(1068, 824)

    ui.bt_delay_popup.addActions([ui.action_action, ui.action_action_c])
    ui.bt_instant_popup.addActions([ui.action_action, ui.action_action_c])
    ui.bt_menu_button_popup.addActions([ui.action_action, ui.action_action_c])
    window.setWindowTitle("Sample BreezeStyleSheets application.")

    ui.action_action.triggered.connect(ui.about)
    ui.action_action_c.triggered.connect(ui.critical)

    window.tabifyDockWidget(ui.dock_widget1, ui.dock_widget2)

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
