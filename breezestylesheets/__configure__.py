"""Configure icons, stylesheets, and resource files."""

from typing import TYPE_CHECKING, cast

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from breezestylesheets import (
    __author__,
    __credits__,
    __license__,
    __version__,
    __version_info__,
    resources,
    utils,
)
from breezestylesheets.exception import RccNotFoundError, ResourceCompileError
from breezestylesheets.model import EXTENSIONS
from breezestylesheets.style import Style
from breezestylesheets.stylesheet import StyleSheetTemplate
from breezestylesheets.theme import Theme

if TYPE_CHECKING:
    from typing import Literal, Protocol

    from breezestylesheets.types import PathOrStr

PACKAGE_DIR = utils.package_dir()
PROJECT_DIR = utils.project_dir()
DIST_DIR = PROJECT_DIR / "dist"
RESOURCES_DIR = PROJECT_DIR / "resources"
TEMPLATE_DIR = PACKAGE_DIR / "template"
THEME_DIR = PACKAGE_DIR / "theme"
DEFAULT = "default"

if TYPE_CHECKING:

    class Args(Protocol):
        styles: "list[str]"
        extensions: "list[str]"
        resource: "str"
        no_qrc: "bool"
        output_dir: "Path"
        qt_framework: Literal["pyqt5", "pyqt6", "pyside2", "pyside6"]
        clean: "bool"
        rcc: "str | None"
        compiled: "str | None"
        use_default_compression: "bool"


def parse_args(argv: "list[str] | None" = None) -> "Args":
    """Parse the command-line options."""

    parser = argparse.ArgumentParser(description="Styles to configure for a Qt application.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--styles",
        "--themes",
        help="the themes to configure. pass `all` to build all themes",
        dest="styles",
        default=["light-blue", "dark-blue"],
        nargs="*",
    )
    parser.add_argument(
        "--extensions",
        help="comma-separate list of styles to configure. pass `all` to build all extensions",
        nargs="*",
        default=[],
    )
    parser.add_argument(
        "--qrc",
        "--resource",
        "--resource-collection-file",
        help="output qrc resource file name",
        default="breeze.qrc",
        dest="resource",
    )
    parser.add_argument(
        "--no-qrc",
        help="do not build QRC resources.",
        action="store_true",
    )
    parser.add_argument(
        "--output",
        "--output-dir",
        help="the directory where to store the configured styles",
        default=DIST_DIR / "styles",
        dest="output_dir",
        type=Path,
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
    parser.add_argument(
        "--clean",
        help="clean dist directory prior to configuring themes.",
        action="store_true",
    )
    parser.add_argument(
        "--rcc",
        help=(
            "path to the rcc executable. "
            "Overrides rcc of chosen framework. "
            "Only use if system cannot find the rcc executable."
        ),
    )
    parser.add_argument(
        "--compiled",
        "--compiled-resource",
        help="output compiled python resource file.",
        dest="compiled",
    )
    parser.add_argument(
        "--use-default-compression",
        help="use the default Qt compression rather than the more efficient custom compression.",
        action="store_true",
    )
    args = cast("Args", parser.parse_args(argv))
    parse_styles(args)
    parse_extensions(args)

    return args


def split_csv(value: "list[str] | str") -> "list[str]":
    """Split a list of values provided as comma-separated values."""
    if isinstance(value, list):
        return [j for i in value for j in split_csv(i)]
    values = map(str.strip, value.split(","))
    return [i for i in values if i]


def parse_styles(args: "Args") -> None:
    """Parse a list of valid styles."""

    values = split_csv(args.styles)
    if "all" in values:
        values = [j.stem for i in EXTENSIONS for j in THEME_DIR.glob(f"*{i}")]
    args.styles = values


def parse_extensions(args: "Args") -> None:
    """Parse a list of valid extensions."""

    values = split_csv(args.extensions)
    if "all" in values:
        directories = (i for i in TEMPLATE_DIR.iterdir() if i.is_dir())
        values = [i.stem for i in directories if Style.is_extension(i)]

    args.extensions = values


def configure_style(config: "resources.Compiler", style: "Style", directory: "Path") -> "None":
    """Configure the icons and stylesheet for a given style."""

    output = directory / style.name
    output.mkdir(parents=True, exist_ok=True)

    stylesheet = config.template.render(style)
    (output / "stylesheet.qss").write_text(stylesheet.value, encoding="utf-8")
    for icon in stylesheet.icons:
        (output / f"{icon.name}.svg").write_text(icon.value, encoding="utf-8")


def write_qrc(config: "resources.Compiler", qt_dist: "PathOrStr") -> "None":
    """Simple QRC writer."""

    if config.qrc is None:
        return

    qrc_path = config.qrc
    if not os.path.isabs(qrc_path):
        qrc_path = f"{qt_dist}/{qrc_path}"
    Path(qrc_path).write_text(config.to_qrc(qt_dist), encoding="utf-8")


def compile_resource(args: "Args", config: "resources.Compiler") -> "None":
    """Compile our resource file to a standalone Python file."""

    assert args.compiled is not None

    resource_path = args.resource
    compiled_resource_path = args.compiled
    if not os.path.isabs(resource_path):
        resource_path = f"{args.output_dir}/{resource_path}"
    if not os.path.isabs(compiled_resource_path):
        compiled_resource_path = f"{RESOURCES_DIR}/{compiled_resource_path}"

    compression: resources.Compression = "lzma"
    if not args.use_default_compression:
        compression = "default"
    try:
        resources.compile(
            qrc=resource_path,
            dst=compiled_resource_path,
            framework=args.qt_framework,
            rcc=args.rcc,
            compression=compression,
        )
    except ResourceCompileError as error:
        inner = cast("subprocess.CalledProcessError", error.inner)
        if b"File does not exist" in inner.stderr:
            print('ERROR: Ensure qrc file exists or deselect "no-qrc" option!', file=sys.stderr)
        else:
            print(f'ERROR: Got an unknown error of "{inner.stderr.decode("utf-8")}"!', file=sys.stderr)
        raise SystemExit from error
    except RccNotFoundError as error:
        if args.rcc:
            print("ERROR: rcc path invalid!", file=sys.stderr)
        else:
            print("ERROR: Ensure rcc executable exists for chosen framework!", file=sys.stderr)
        print(
            "Required rcc for PyQt5: pyrcc5",
            "Required rcc for PySide6 & PyQt6: PySide6-rcc",
            "Required rcc for PySide2: PySide2-rcc",
            "",
            "if using venv, activate it or provide path to rcc.",
            sep="\n",
            file=sys.stderr,
        )
        raise SystemExit from error


def configure(args: "Args") -> "None":
    """Configure all styles and write the files to a QRC file."""

    if args.output_dir.is_relative_to(PACKAGE_DIR):
        raise ValueError("Cannot configure the resources within the package.")

    if args.clean:
        shutil.rmtree(args.output_dir, ignore_errors=True)

    # Need to convert our styles accordingly.
    styles = [Style(i, Theme.load(f"{THEME_DIR}/{i}.json")) for i in args.styles]
    template_dirs = [TEMPLATE_DIR / DEFAULT] + [TEMPLATE_DIR / i for i in args.extensions]
    qrc = args.resource if not args.no_qrc else None
    compression = "default" if not args.use_default_compression else "lzma"
    config = resources.Compiler(
        styles=styles,
        template=StyleSheetTemplate.from_directories(*template_dirs),
        framework=args.qt_framework,
        qrc=qrc,
        rcc=args.rcc,
        compression=compression,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for style in styles:
        configure_style(config, style, args.output_dir)

    # Create aliases for our light-blue and dark-blue styles to light and dark.
    # Only create aliases if light-blue and/or dark-blue are to be built.
    aliases = set(args.styles) & set(resources.Compiler.ALIASES)
    for theme in aliases:
        source = args.output_dir / theme / "stylesheet.qss"
        destination = args.output_dir / resources.Compiler.ALIASES[theme] / "stylesheet.qss"
        destination.parent.mkdir(exist_ok=True)
        shutil.copy2(source, destination)

    # Create and compile our resource files.
    if not args.no_qrc:
        write_qrc(config, str(args.output_dir))
    if args.compiled is not None:
        compile_resource(args, config)


def main(argv: "list[str] | None" = None):
    """Configuration entry point"""
    configure(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
