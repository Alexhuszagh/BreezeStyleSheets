from typing import Protocol
from typing_extensions import Literal, get_args

from example._util import cli
from example._util.colors import Colors
from example._util.qt import PyQt

MinimizeLocation = Literal["TopLeft", "TopRight", "BottomLeft", "BottomRight"]


class Args(cli.Args, Protocol):
    minimize_location: MinimizeLocation
    border_width: int
    default_window_frame: bool
    status_bar: bool
    window_help: bool
    window_shade: bool
    wayland_testing: bool


class Parser(cli.Parser[Args]):
    def __init__(self) -> None:
        super().__init__()
        self._parser.add_argument(
            "--minimize-location",
            help="location to minimize windows to in the MDI area",
            default="BottomLeft",
            choices=get_args(MinimizeLocation),
        )
        self._parser.add_argument(
            "--border-width",
            help="width of the subwindow borders",
            type=int,
            choices=range(0, 6),
            default=1,
        )
        self._parser.add_argument(
            "--default-window-frame",
            help="use the default title bars",
            action="store_true",
        )
        self._parser.add_argument(
            "--status-bar",
            help="use a top-level status bar",
            action="store_true",
        )
        self._parser.add_argument(
            "--window-help",
            help="add a top-level context help button",
            action="store_true",
        )
        self._parser.add_argument(
            "--window-shade",
            help="add a top-level shade/unshade button",
            action="store_true",
        )
        self._parser.add_argument(
            "--wayland-testing",
            help="debug with a custom titlebar on wayland",
            action="store_true",
        )


ARGS, UNKNOWN = Parser().parse()
COLORS = Colors.from_stylesheet(ARGS.stylesheet.name)
Qt = PyQt.from_framework(ARGS.qt_framework)
STANDARD_ICONS = Qt.standard_icons
