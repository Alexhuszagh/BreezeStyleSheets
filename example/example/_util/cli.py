"""Command-line parser."""

from typing import TYPE_CHECKING, Generic, Protocol, TypeVar, cast

import argparse
import os
import sys

from .stylesheet import Stylesheet

if TYPE_CHECKING:
    from breezestylesheets.constants import Framework  # type: ignore

ArgsT = TypeVar("ArgsT", bound="Args")


def _has_x11() -> bool:
    return sys.platform in ("aix", "freebsd", "linux")


class Args(Protocol):
    stylesheet: Stylesheet
    style: str
    font_size: float
    font_family: str
    scale: float
    qt_framework: "Framework"
    use_x11: bool


class Parser(Generic[ArgsT]):
    _parser: "argparse.ArgumentParser"

    def __init__(self) -> None:
        """Create an argparser with the base settings for all Qt applications."""

        parser = argparse.ArgumentParser(description="Configurations for the Qt5 application.")
        parser.add_argument(
            "--stylesheet",
            help="stylesheet name (`dark`, `light`, `native`, `auto`, ...)",
            default="native",
        )
        # Know working styles include:
        #   1. Fusion
        #   2. Windows
        parser.add_argument(
            "--style",
            help="application style (`Fusion`, `Windows`, `native`, ...)",
            default="native",
        )
        parser.add_argument(
            "--font-size",
            help="font size for the application",
            type=float,
            default=-1,
        )
        parser.add_argument(
            "--font-family",
            help="the font family",
        )
        parser.add_argument(
            "--scale",
            help="scale factor for the UI",
            type=float,
            default=1,
        )
        parser.add_argument(
            "--qt-framework",
            help=(
                "target framework to build for. Default = pyqt5. "
                "Note: building for PyQt6 requires PySide6-rcc to be installed."
            ),
            choices=["pyqt5", "pyqt6", "pyside2", "pyside6"],
            default="pyqt5",
        )

        if _has_x11():
            parser.add_argument(
                "--use-x11",
                help="force the use of x11 on compatible systems.",
                action="store_true",
            )

        self._parser = parser

    def parse(self) -> "tuple[ArgsT, list[str]]":
        """Parse the command-line arguments and hot-patch the args."""

        parsed, unknown = self._parser.parse_known_args()
        parsed.stylesheet = Stylesheet(parsed.stylesheet)
        args = cast("ArgsT", parsed)
        # Need to fix an issue on Wayland on Linux:
        #   conda-forge does not support Wayland, for who knows what reason.
        if sys.platform.lower().startswith("linux") and "CONDA_PREFIX" in os.environ:
            args.use_x11 = True
        elif not _has_x11():
            args.use_x11 = False

        if args.use_x11:
            os.environ["XDG_SESSION_TYPE"] = "x11"
            os.environ["QT_QPA_PLATFORM"] = "xcb"

        return (args, unknown)
