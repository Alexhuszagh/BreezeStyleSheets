from typing import Protocol

from example._util import cli
from example._util.colors import Colors
from example._util.qt import PyQt


class Args(cli.Args, Protocol):
    set_app_palette: bool
    set_widget_palette: bool


class Parser(cli.Parser[Args]):
    def __init__(self) -> None:
        super().__init__()
        self._parser.add_argument(
            "--set-app-palette",
            help="set the placeholder text palette globally.",
            action="store_true",
        )
        # https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System/blob/master/doc/user-guide.md#configuration-flags
        self._parser.add_argument(
            "--set-widget-palette",
            help="set the placeholder text palette for the affected widgets.",
            action="store_true",
        )


ARGS, UNKNOWN = Parser().parse()
COLORS = Colors.from_stylesheet(ARGS.stylesheet.name)
Qt = PyQt.from_framework(ARGS.qt_framework)
