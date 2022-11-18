#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) <2022-Present> <Alex Huszagh>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys

HOME = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(HOME))

import widgets
import shared

parser = shared.create_parser()
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
ICON_MAP = shared.get_icon_map(args, compat)


def set_stylesheet(args, app, compat):
    '''Set the application stylesheet.'''

    if args.stylesheet != 'native':
        resource_format = shared.get_resources(args)
        qt_path = shared.get_stylesheet(resource_format)
        ext_path = os.path.join(HOME, 'stylesheet.qss.in')
        stylesheet = shared.read_qtext_file(qt_path, compat)
        stylesheet += '\n' + open(ext_path, 'r').read()
        app.setStyleSheet(stylesheet)


def get_treeviews(parent, depth=1000):
    for child in parent.children():
        if isinstance(child, QtWidgets.QTreeView):
            yield child
        elif depth > 0:
            yield from get_treeviews(child, depth - 1)


def main():
    'Application entry point'

    # this is mostly a hack to get simplify using the same UI but with
    # minimal additions to modify the stylesheet
    app, window = shared.setup_app(args, unknown, compat)

    # setup ui
    ui = widgets.Ui()
    ui.setup(window)
    ui.bt_delay_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    ui.bt_instant_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    ui.bt_menu_button_popup.addActions([
        ui.actionAction,
        ui.actionAction_C
    ])
    window.setWindowTitle('Sample BreezeStyleSheets application.')

    # Add event triggers
    ui.actionAction.triggered.connect(ui.about)
    ui.actionAction_C.triggered.connect(ui.critical)

    # tabify dock widgets to show bug #6
    window.tabifyDockWidget(ui.dockWidget1, ui.dockWidget2)

    # add object names to all the widgets so we don't have to recreate a UI
    for tree in get_treeviews(window):
        tree.setObjectName("branchless")

    set_stylesheet(args, app, compat)
    return shared.exec_app(args, app, window, compat)


if __name__ == '__main__':
    sys.exit(main())
