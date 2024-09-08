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

'''
    standard_icons
    ==============

    Example overriding QCommonStyle for custom standard icons.
'''

import os
import sys

HOME = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(HOME))

import shared  # noqa  # pylint: disable=wrong-import-position,import-error

parser = shared.create_parser()
args, unknown = shared.parse_args(parser)
QtCore, QtGui, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
ICON_MAP = shared.get_icon_map(compat)


def style_icon(style, icon, option=None, widget=None):
    '''Helper to provide arguments for setting a style icon.'''
    return shared.style_icon(args, style, icon, ICON_MAP, option, widget)


class StandardIconStyle(QtWidgets.QCommonStyle):
    '''A custom application style overriding standard icons.'''

    def __init__(self, style):
        super().__init__()
        self.style = style

    def __getattribute__(self, item):
        '''
        Override for standardIcon. Everything else should default to the
        system default. We cannot have `style_icon` be a member of
        `StandardIconStyle`, since this will cause an infinite recursive loop.
        '''
        if item == 'standardIcon':
            return lambda *x: style_icon(self, *x)
        return getattr(object.__getattribute__(self, 'style'), item)


def add_standard_button(ui, layout, icon, index):
    '''Create and add a QToolButton with a standard icon.'''

    button = QtWidgets.QToolButton(ui.centralwidget)
    setattr(ui, f'button{index}', button)
    button.setAutoRaise(True)
    button.setIcon(style_icon(button.style(), icon, widget=button))
    button.setObjectName(f'button{index}')
    layout.addWidget(button)


def add_standard_buttons(ui, page, icons):
    '''Create and add QToolButtons with standard icons to the UI.'''

    _ = ui
    for icon_name in icons:
        icon_enum = getattr(compat, icon_name)
        icon = style_icon(page.style(), icon_enum, widget=page)
        item = QtWidgets.QListWidgetItem(icon, icon_name)
        page.addItem(item)
