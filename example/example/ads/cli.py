from typing import Protocol

from example._util import cli
from example._util.colors import Colors
from example._util.qt import PyQt


class Args(cli.Args, Protocol):
    use_internal: bool
    focus_highlighting: bool


class Parser(cli.Parser[Args]):
    def __init__(self) -> None:
        super().__init__()
        self._parser.add_argument(
            "--use-internal",
            help="use the dock manager internal stylesheet.",
            action="store_true",
        )
        # https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System/blob/master/doc/user-guide.md#configuration-flags
        self._parser.add_argument(
            "--focus-highlighting",
            help="use the focus highlighting (and other configuration flags).",
            action="store_true",
        )


ARGS, UNKNOWN = Parser().parse()
COLORS = Colors.from_stylesheet(ARGS.stylesheet.name)
Qt = PyQt.from_framework(ARGS.qt_framework)
