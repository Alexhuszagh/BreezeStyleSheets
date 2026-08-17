#!/usr/bin/env python
"""Simple PyQt application without branches for our QTreeViews."""

import sys

from example._util.qt import PyQtApplication
from example.branchless import ARGS, UNKNOWN, Qt, get_treeviews
from example.widgets import Ui


def main() -> "None":
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

    # add object names to all the widgets so we don't have to recreate a UI
    for tree in get_treeviews(window):
        tree.setObjectName("branchless")

    ARGS.stylesheet.apply(Qt)
    PyQtApplication(app).start(window)


if __name__ == "__main__":
    sys.exit(main())
