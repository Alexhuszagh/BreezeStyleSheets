"""
Configurable Breeze and BreezeDark-like stylesheets for Qt Applications.

BreezeStyleSheets is a set of beautiful light and dark stylesheets that
render consistently across platforms, including high DPI screens. Each
stylesheet is generated from a theme file and can be extended with a
extension system, simplifying the generation custom stylesheets for your
application. The stylesheets are comprehensively tested with most Qt
widgets and widget properties, providing a consistent, stylish feel on
any platform, including different operating systems, desktop environments,
and Qt versions.
"""

__version__ = "0.2.0"
__version_info__ = (0, 2, 0)
__author__ = "Alex Huszagh <ahuszagh@gmail.com>"
__credits__ = "Colin Duquesnoy"
__license__ = "MIT"

from .icon import Icon, IconTemplate
from .style import Style
from .stylesheet import StyleSheet, StyleSheetTemplate
from .theme import Theme

# TODO: Import `Theme` and define an `apply` here
# That will call `Theme.apply` which will require the Qt app
#   This will have many arguments which will define the
#   platform-specific patches
