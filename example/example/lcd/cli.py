from typing import Protocol

from example._util import cli
from example._util.colors import Colors
from example._util.qt import PyQt


class Args(cli.Args, Protocol):
    no_align: bool


class Parser(cli.Parser[Args]):
    def __init__(self) -> None:
        super().__init__()
        self._parser.add_argument(
            "--no-align",
            help="allow larger widgets without forcing alignment.",
            action="store_true",
        )


ARGS, UNKNOWN = Parser().parse()
COLORS = Colors.from_stylesheet(ARGS.stylesheet.name)
Qt = PyQt.from_framework(ARGS.qt_framework)
