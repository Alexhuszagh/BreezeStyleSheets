"""
Utilities to processing [resources] embedded within stylesheets, including
the compression of these resources.

[resources]: https://doc.qt.io/qt-6/resources.html
"""

from typing import TYPE_CHECKING, ClassVar

import ast
import binascii
import glob
import gzip
import lzma
import os
import re
import shutil
import subprocess
import zlib
from dataclasses import dataclass

from .exception import InvalidFrameworkError, RccNotFoundError, ResourceCompileError
from .utils import xml_escape

if TYPE_CHECKING:
    from .constants import Compression, Framework
    from .style import Style
    from .stylesheet import StyleSheetTemplate
    from .types import PathOrStr


def compress_resource(
    code: "str",
    resource: "str",
    compression: "Compression | None" = "lzma",
) -> "str":
    """
    Extract data from a Qt resource, then replace the data with compress values.

    Note that the default input compresses per file, and uses null delimiters, such
    as `\\x00\\x00\\x00\\x9c` between entries for each file, which is not consistent.
    For the best compression and performance, the input data should be uncompressed
    and then the output will be optimally compressed over all files.

    Args:
        code: The code to extract the resource from.

        resource: The name of the resource to extract and replace.

        compression: The compression of the replaced resource data.
            Valid compression values are:
            - zlib
            - lzma
            - gzip
            - default (use the default Qt compression)

    Returns:
        The Python code with the resource replaced with the new compression level.

    ## Example

    A sample Python resource input file will have the following structure:

    ```python
    from PyQt5 import QtCore

    qt_resource_data = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v1 = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v2 = b"\\xFD\\x37\\x7A..."

    qt_version = [int(v) for v in QtCore.qVersion().split('.')]
    if qt_version < [5, 8, 0]:
        rcc_version = 1
        qt_resource_struct = qt_resource_struct_v1
    else:
        rcc_version = 2
        qt_resource_struct = qt_resource_struct_v2

    def qInitResources():
        QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    def qCleanupResources():
        QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    qInitResources()
    ```

    In order to handle our own compression, we replace this data with `_` underscore variants, having
    the initial data be compressed and decompressing it to the raw data on the fly:

    ```python
    from PyQt5 import QtCore
    import lzma

    _qt_resource_data = b"\\xFD\\x37\\x7A..."
    qt_resource_data = lzma.decompress(_qt_resource_data)

    _qt_resource_struct_v1 = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v1 = lzma.decompress(_qt_resource_struct_v1)

    _qt_resource_struct_v2 = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v2 = lzma.decompress(_qt_resource_struct_v2)

    qt_version = [int(v) for v in QtCore.qVersion().split('.')]
    if qt_version < [5, 8, 0]:
        rcc_version = 1
        qt_resource_struct = qt_resource_struct_v1
    else:
        rcc_version = 2
        qt_resource_struct = qt_resource_struct_v2

    def qInitResources():
        QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    def qCleanupResources():
        QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    qInitResources()
    ```
    """

    # no changes, uses the initial data
    if compression in (None, "default"):
        return code

    # first, get and compress our data
    # this pattern is always safe since there will never be any internal `"`
    # characters due to how compilation/quoting is done, even escaped ones.
    pattern = rf'(?P<prefix>{resource}\s*=\s*)(?P<data>b".*?")'
    match = re.search(pattern, code, flags=re.DOTALL)
    if match is None and resource == "qt_resource_struct":
        # NOTE: some older versions use v1/v2 structs
        v1 = compress_resource(code, "qt_resource_struct_v1", compression=compression)
        v2 = compress_resource(v1, "qt_resource_struct_v2", compression=compression)
        return v2
    if match is None:
        raise ValueError(f'Unable to extract resource with prefix "{resource}".')

    # read the input and compress it to the output.
    initial: bytes = ast.literal_eval(match.group("data"))
    if compression == "zlib":
        compressed = zlib.compress(initial)
    elif compression == "lzma":
        compressed = lzma.compress(initial)
    elif compression == "gzip":
        compressed = gzip.compress(initial)
    else:
        compressed = initial

    # NOTE: to avoid any issues with `"` or `'` characters, we always escape it
    hexlified = binascii.hexlify(compressed).decode("ascii").upper()
    escaped = "".join([f"\\x{hexlified[i : i + 2]}" for i in range(0, len(hexlified), 2)])
    replaced = f"{resource} = _{resource}"
    if compression != "default":
        replaced = f"{resource} = {compression}.decompress(_{resource})"
    replacement = f'_{resource} = b"{escaped}"\n{replaced}\n'

    return code[: match.start()] + replacement + code[match.end() + 1 :]


def compress(
    path: "PathOrStr",
    compression: "Compression | None" = "lzma",
) -> "None":
    """
    Compress the data within a Qt resource Python source code file.

    Args:
        path: The path of the Python file to compress the resources in.

        compression: The compression of the replaced resource data.
            Valid compression values are:
            - zlib
            - lzma
            - gzip
            - default (use the default Qt compression)

    ## Example

    A sample Python resource input file will have the following structure:

    ```python
    from PyQt5 import QtCore

    qt_resource_data = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v1 = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v2 = b"\\xFD\\x37\\x7A..."

    qt_version = [int(v) for v in QtCore.qVersion().split('.')]
    if qt_version < [5, 8, 0]:
        rcc_version = 1
        qt_resource_struct = qt_resource_struct_v1
    else:
        rcc_version = 2
        qt_resource_struct = qt_resource_struct_v2

    def qInitResources():
        QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    def qCleanupResources():
        QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    qInitResources()
    ```

    In order to handle our own compression, we replace this data with `_` underscore variants, having
    the initial data be compressed and decompressing it to the raw data on the fly:

    ```python
    from PyQt5 import QtCore
    import lzma

    _qt_resource_data = b"\\xFD\\x37\\x7A..."
    qt_resource_data = lzma.decompress(_qt_resource_data)

    _qt_resource_struct_v1 = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v1 = lzma.decompress(_qt_resource_struct_v1)

    _qt_resource_struct_v2 = b"\\xFD\\x37\\x7A..."
    qt_resource_struct_v2 = lzma.decompress(_qt_resource_struct_v2)

    qt_version = [int(v) for v in QtCore.qVersion().split('.')]
    if qt_version < [5, 8, 0]:
        rcc_version = 1
        qt_resource_struct = qt_resource_struct_v1
    else:
        rcc_version = 2
        qt_resource_struct = qt_resource_struct_v2

    def qInitResources():
        QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    def qCleanupResources():
        QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

    qInitResources()
    ```
    """

    # want to minimize the file size, let's use custom gzip compression
    with open(path, encoding="utf-8") as file:
        code = file.read()
    code = code.replace("import QtCore", "import QtCore\nimport lzma", 1)
    # NOTE: these should never be none or we have an error
    code = compress_resource(code, "qt_resource_data", compression=compression)
    code = compress_resource(code, "qt_resource_name", compression=compression)
    code = compress_resource(code, "qt_resource_struct", compression=compression)

    with open(path, "w", encoding="utf-8") as file:
        file.write(code)


def fix_imports(path: "PathOrStr", framework: "Framework") -> "None":
    """
    Fix imports after using PySide6-rcc to compile for PyQt6.

    `PyQt6` does not contain a resource compiler, preferring native Python data
    packaging, which produces suboptimal results and large distribution sizes.
    A much simpler approach is to use `PySide6`'s resource compiler and fix the
    imports.

    Args:
        path: The path of the Python file to containing the resources in.

        framework: The Qt framework to target.
            Valid frameworks are:
            - pyqt5
            - pyqt6
            - pyside2
            - pyside6
    """

    if framework != "pyqt6":
        return
    with open(path, encoding="utf-8") as file:
        text = file.read()
    text = text.replace("PySide6", "PyQt6", 1)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def compile(
    qrc: "PathOrStr",
    dst: "PathOrStr",
    framework: "Framework",
    *,
    rcc: "PathOrStr | None" = None,
    compression: "Compression | None" = "lzma",
) -> "None":
    """
    Compile a Qt resource [Collection File] to a resource.

    This invokes the Qt resource compiler and patches the compression
    for more optimal compression.

    [Collection File]: https://doc.qt.io/qt-6/resources.html

    Args:
        qrc: The path to the input QRC file.

        dst: The path to the compiled resource.

        framework: The Qt framework to target.
            Valid frameworks are:
            - pyqt5
            - pyqt6
            - pyside2
            - pyside6

        rcc: The path to the Qt resource compiler.

        compression: The compression of the replaced resource data.
            If not using the default or no compression, we optimize the generated
            resource using a custom compression that compresses over all files,
            rather than per-file, producing much smaller resource files.

            Valid compression values are:
            - zlib
            - lzma
            - gzip
            - default (use the default Qt compression)
    """

    if rcc is None:
        rcc = get_rcc(framework)
    elif shutil.which(rcc) is None:
        raise RccNotFoundError(rcc, framework)

    # build our command and compile the file
    command: list[str] = [str(rcc), str(qrc), "-o", str(dst)]
    if compression != "default":
        command.append("-no-compress")

    try:
        subprocess.check_output(
            command,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            shell=False,
        )
        fix_imports(dst, framework)
        compress(dst, compression=compression)
    except subprocess.CalledProcessError as error:
        raise ResourceCompileError(rcc, qrc, framework, error) from error


def get_rcc(framework: "Framework") -> "PathOrStr":
    """
    Get resource compiler (RCC) required the provided framework.

    Args:
        framework: The Qt framework to target.
            Valid frameworks are:
            - pyqt5
            - pyqt6
            - pyside2
            - pyside6

    Returns:
        The path to the Qt resource compiler.
    """

    if framework in ("pyqt6", "pyside6"):
        rcc = "pyside6-rcc"
    elif framework == "pyqt5":
        rcc = "pyrcc5"
    elif framework == "pyside2":
        rcc = "pyside2-rcc"
    else:
        raise InvalidFrameworkError(framework)

    command = shutil.which(rcc)
    if command is None:
        raise RccNotFoundError(rcc, framework)

    return command


@dataclass
class Compiler:
    """
    The configuration of a compiling resource files.

    This is used for the configuration scripts **only**: any runtime
    theme configuration will use dynamic resources already loaded
    which will not require compilation.
    """

    # NOTE: `kw_only` is 3.10+

    ALIASES: "ClassVar[dict[str, str]]" = {
        "dark-blue": "dark",
        "light-blue": "light",
    }
    """Legacy style names for backwards compatibility, as a map of the new to the old name."""

    EXTENSIONS: "ClassVar[tuple[str, ...]]" = (".qss", ".svg")
    """The file extensions of all configured resources."""

    styles: "list[Style]"
    """
    A mapping of the resource style names to the themes.

    This maps the names, for when the resources are configured, to the
    paths of the resources, so the compiler can convert them to Qt
    resources.
    """

    template: "StyleSheetTemplate"
    """
    The stylesheet and icon templates to configure.

    The template defines placeholders, such as `^foreground^`,
    which are then replaced by the values specified in the `Theme`.

    These can be loaded from one or more directories.
    """

    framework: "Framework"
    """
    The Qt framework to target.

    Valid frameworks are:
    - pyqt5
    - pyqt6
    - pyside2
    - pyside6
    """

    qrc: "PathOrStr | None" = None
    """
    The path to the Qt Resource Collection File ([.qrc]) to write.

    If the value is None, do not write (or build) a Qt Resource Collection
    File ([.qrc]).

    These enumerates the files within a compiled resource to be used
    as inputs to the resource compiler.

    [.qrc]: https://doc.qt.io/qt-6/resources.html#qt-resource-collection-file-qrc
    """

    rcc: "PathOrStr | None" = None
    """The path to the Qt resource compiler."""

    compression: "Compression | None" = None
    """
    The compression of the replaced resource data.

    If not using the default or no compression, we optimize the generated
    resource using a custom compression that compresses over all files,
    rather than per-file, producing much smaller resource files.

    Valid compression values are:
    - zlib
    - lzma
    - gzip
    - default (use the default Qt compression)
    """

    # TODO:
    #   How can I configure this without a QRC?
    #   Default to the current directory...
    #   Output is configurable but should default to the current directory...
    #   Document all these functions
    #   Needs to configure for all styles...
    def configure(self, output: "PathOrStr") -> None:
        pass

    def compile(self) -> "None":
        raise NotImplementedError("TODO")

    def to_qrc(self, directory: "PathOrStr") -> "str":
        """
        Create a Qt Resource Collection File ([.qrc]) from the contents of the directory.

        These enumerates all files, including in subdirectories, within the configured directory
        to generate the ([.qrc]), which is returned as a raw XML string. This handles XML escaping
        of any invalid characters in the filename.

        [.qrc]: https://doc.qt.io/qt-6/resources.html#qt-resource-collection-file-qrc

        Args:
            directory: The directory which to enumerate files in.

        Returns:
            The QRC file as a raw XML string.
        """

        globbed = (j for i in self.EXTENSIONS for j in glob.glob(f"**/*{i}", root_dir=directory))
        normalized = (i.replace(os.sep, "/") for i in globbed)
        escaped = (xml_escape(i) for i in normalized)
        files = [f"    <file>{i}</file>" for i in escaped]

        return "\n".join(["<RCC>", "  <qresource>", *files, "  </qresource>", "</RCC>"])
