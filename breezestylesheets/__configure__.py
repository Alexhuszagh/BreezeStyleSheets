"""Configure icons, stylesheets, and resource files."""

from typing import TYPE_CHECKING, cast

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from breezestylesheets import __author__, __credits__, __license__, __version__, __version_info__, utils
from breezestylesheets.exception import RccNotFoundError, ResourceCompileError
from breezestylesheets.resources import Compiler
from breezestylesheets.style import Style
from breezestylesheets.stylesheet import StyleSheetTemplate
from breezestylesheets.theme import Theme

if TYPE_CHECKING:
    from typing import Literal, Protocol

    from breezestylesheets.resources import Compression

PACKAGE_DIR = utils.package_dir()
PROJECT_DIR = utils.project_dir()
DIST_DIR = PROJECT_DIR / "dist"
RESOURCES_DIR = PROJECT_DIR / "resources"
TEMPLATE_DIR = PACKAGE_DIR / "template"
THEME_DIR = PACKAGE_DIR / "theme"
DEFAULT = "default"

if TYPE_CHECKING:

    class Args(Protocol):
        styles: "list[Path]"
        extensions: "list[Path]"
        resource: "Path"
        no_qrc: "bool"
        output_dir: "Path"
        framework: Literal["pyqt5", "pyqt6", "pyside2", "pyside6"]
        rcc: "str | None"
        compiled: "Path | None"
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
        default=Path("breeze.qrc"),
        dest="resource",
        type=Path,
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
        "--framework",
        "--qt-framework",
        help=(
            "target framework to build for. Default = pyqt5. "
            "Note: building for PyQt6 requires PySide6-rcc to be installed."
        ),
        choices=["pyqt5", "pyqt6", "pyside2", "pyside6"],
        default="pyqt5",
        dest="framework",
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
        type=Path,
        dest="compiled",
    )
    parser.add_argument(
        "--use-default-compression",
        help="use the default Qt compression rather than the more efficient custom compression.",
        action="store_true",
    )

    def split(value: "list[str] | str") -> "set[str]":
        if isinstance(value, list):
            return {j for i in value for j in split(i)}
        return {i for i in map(str.strip, value.split(",")) if i}

    parsed = parser.parse_args(argv)
    parsed.styles = Style.find_styles(THEME_DIR, subset=split(parsed.styles))
    parsed.extensions = Style.find_extensions(TEMPLATE_DIR, subset=split(parsed.extensions))

    args = cast("Args", parsed)
    if not args.resource.is_absolute():
        args.resource = args.output_dir / args.resource
    if args.compiled is not None and not args.compiled.is_absolute():
        args.compiled = RESOURCES_DIR / args.compiled

    # NOTE: Change to `is_relative_to` on Python 3.9+
    try:
        _ = args.output_dir.relative_to(PACKAGE_DIR)
        raise AssertionError
    except ValueError:
        pass
    except AssertionError:
        raise ValueError("Cannot configure the resources within the package.") from None

    return args


def compile_resource(compiler: "Compiler", qrc: "Path", dst: "Path") -> "None":
    """Compile our resource file to a standalone Python file."""

    try:
        compiler.compile(qrc, dst)
    except ResourceCompileError as error:
        inner = cast("subprocess.CalledProcessError", error.inner)
        if b"File does not exist" in inner.stderr:
            print('ERROR: Ensure qrc file exists or deselect "no-qrc" option!', file=sys.stderr)
        else:
            print(f'ERROR: Got an unknown error of "{inner.stderr.decode("utf-8")}"!', file=sys.stderr)
        raise SystemExit from error
    except RccNotFoundError as error:
        if compiler.rcc:
            print("ERROR: rcc path invalid!", file=sys.stderr)
        else:
            print("ERROR: Ensure rcc executable exists for chosen framework!", file=sys.stderr)
        print(
            "Required rcc for PyQt5: pyrcc5",
            "Required rcc for PySide6 & PyQt6: pyside6-rcc",
            "Required rcc for PySide2: pyside2-rcc",
            "",
            "if using venv, activate it or provide path to rcc.",
            sep="\n",
            file=sys.stderr,
        )
        raise SystemExit from error


def configure(args: "Args") -> "None":
    """Configure all styles and write the files to a QRC file."""

    to_clean = list(args.output_dir.rglob("*.svg")) + list(args.output_dir.rglob("*.qss"))
    for file in to_clean:
        file.unlink()

    styles = [Style(i.stem, Theme.load(i)) for i in args.styles]
    compression: "Compression" = "default" if args.use_default_compression else "lzma"
    compiler = Compiler(framework=args.framework, rcc=args.rcc, compression=compression)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    template = StyleSheetTemplate.from_directories(TEMPLATE_DIR / DEFAULT, *args.extensions)
    for style in styles:
        output = args.output_dir / style.name
        output.mkdir(parents=True, exist_ok=True)
        stylesheet = template.render(style)
        (output / "stylesheet.qss").write_text(stylesheet.value, encoding="utf-8")
        for icon in stylesheet.icons:
            (output / f"{icon.name}.svg").write_text(icon.value, encoding="utf-8")

    # Create aliases for our light-blue and dark-blue styles to light and dark.
    # Only create aliases if light-blue and/or dark-blue are to be built.
    aliases = {i.stem for i in args.styles} & set(Compiler.ALIASES)
    for theme in aliases:
        source = args.output_dir / theme / "stylesheet.qss"
        destination = args.output_dir / Compiler.ALIASES[theme] / "stylesheet.qss"
        destination.parent.mkdir(exist_ok=True)
        shutil.copy2(source, destination)

    # Create and compile our resource files.
    if args.no_qrc:
        return
    args.resource.write_text(compiler.to_qrc(args.output_dir), encoding="utf-8")

    if args.compiled is not None:
        compile_resource(compiler, args.resource, args.compiled)


def main(argv: "list[str] | None" = None):
    """Configuration entry point"""
    configure(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
