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
    lcd
    ===

    Example showing how to override the `paintEvent` and `eventFilter`
    for a `QLCDNumber`, creating a visually consistent, stylish
    `QLCDNumber` that supports highlighting the handle on the active
    or hovered number.
'''

import os
import sys

EXAMPLE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(EXAMPLE))

import shared  # noqa  # pylint: disable=wrong-import-position,import-error

parser = shared.create_parser()
parser.add_argument(
    '--no-align', help='''allow larger widgets without forcing alignment.''', action='store_true'
)
args, unknown = shared.parse_args(parser)
_, __, QtWidgets = shared.import_qt(args)
compat = shared.get_compat_definitions(args)
colors = shared.get_colors(args, compat)


class LCD(QtWidgets.QLCDNumber):
    '''QLCDNumber with a custom palette.'''

    def __init__(self, widget=None):
        super().__init__(widget)
        self.setContentsMargins(1, 1, 1, 1)
        if args.stylesheet == 'native':
            return

        # The color of the non-flat LCD numbers is still controlled
        # via the `color` stylesheet attribute.
        r, g, b, a = colors.HighLightDark.getRgb()
        color = (r, g, b, a / 255)
        self.setStyleSheet(f'QLCDNumber {{ color: rgba{color}; }}')

        palette = self.palette()
        palette.setColor(compat.WindowPalette, colors.Background)
        palette.setColor(compat.LightPalette, colors.Selected)
        palette.setColor(compat.DarkPalette, colors.Notch)
        self.setPalette(palette)
