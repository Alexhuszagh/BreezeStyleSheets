"""
Utilities to processing [resources] embedded within stylesheets, including
the compression of these resources.

[resources]: https://doc.qt.io/qt-6/resources.html
"""

from typing import TYPE_CHECKING, ClassVar

import ast
import binascii
import gzip
import lzma
import re
import shutil
import subprocess
import zlib
from dataclasses import dataclass
from pathlib import Path

from .exception import InvalidFrameworkError, RccNotFoundError, ResourceCompileError
from .utils import xml_escape

if TYPE_CHECKING:
    from .constants import Compression, Framework

__all__ = ["Compiler"]


def _compress(
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
        v1 = _compress(code, "qt_resource_struct_v1", compression=compression)
        v2 = _compress(v1, "qt_resource_struct_v2", compression=compression)
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

    framework: "Framework"
    """
    The Qt framework to target.

    Valid frameworks are:
    - pyqt5
    - pyqt6
    - pyside2
    - pyside6
    """

    rcc: "Path | str | None" = None
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

    def get_rcc(self) -> "Path":
        """
        Get resource compiler (RCC) required the provided framework.

        Returns:
            The path to the Qt resource compiler.
        """

        if self.rcc is not None:
            rcc = self.rcc
        elif self.framework in ("pyqt6", "pyside6"):
            rcc = "pyside6-rcc"
        elif self.framework == "pyqt5":
            rcc = "pyrcc5"
        elif self.framework == "pyside2":
            rcc = "pyside2-rcc"
        else:
            raise InvalidFrameworkError(self.framework)

        command = shutil.which(rcc)
        if command is None:
            raise RccNotFoundError(rcc, self.framework)

        return Path(command)

    def compress(self, path: "Path") -> "None":
        """
        Compress the data within a Qt resource Python source code file.

        Args:
            path: The path of the Python file to compress the resources in.

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
        """  # ruff: ignore[line-too-long]

        # want to minimize the file size, let's use custom gzip compression
        code = path.read_text(encoding="utf-8")
        if self.compression != "default":
            code = code.replace("import QtCore", f"import QtCore\nimport {self.compression}", 1)
        # NOTE: these should never be none or we have an error
        code = _compress(code, "qt_resource_data", compression=self.compression)
        code = _compress(code, "qt_resource_name", compression=self.compression)
        code = _compress(code, "qt_resource_struct", compression=self.compression)

        path.write_text(code, encoding="utf-8")

    def fix_imports(self, path: "Path") -> "None":
        """
        Fix imports after using PySide6-rcc to compile for PyQt6.

        `PyQt6` does not contain a resource compiler, preferring native Python data
        packaging, which produces suboptimal results and large distribution sizes.
        A much simpler approach is to use `PySide6`'s resource compiler and fix the
        imports.

        Args:
            path: The path of the Python file to containing the resources in.
        """

        if self.framework != "pyqt6":
            return
        text = path.read_text(encoding="utf-8")
        text = text.replace("PySide6", "PyQt6", 1)
        path.write_text(text, encoding="utf-8")

    def compile(self, qrc: "Path", dst: "Path") -> "None":
        """
        Compile a Qt resource [Collection File] to a resource.

        This invokes the Qt resource compiler and patches the compression
        for more optimal compression.

        [Collection File]: https://doc.qt.io/qt-6/resources.html

        Args:
            qrc: The path to the input QRC file.
            dst: The path to the compiled resource.
        """

        # build our command and compile the file
        rcc = self.get_rcc()
        command: list[str] = [str(rcc), str(qrc), "-o", str(dst)]
        if self.compression != "default":
            command.append("-no-compress")

        try:
            subprocess.check_output(
                command,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                shell=False,
            )
            self.fix_imports(dst)
            self.compress(dst)
        except subprocess.CalledProcessError as error:
            raise ResourceCompileError(rcc, qrc, self.framework, error) from error

    def to_qrc(self, directory: "Path") -> "str":
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

        # NOTE: Use the regular glob so we can get it relative_to
        globbed = (j.relative_to(directory) for i in self.EXTENSIONS for j in directory.rglob(f"*{i}"))
        normalized = (i.as_posix() for i in globbed)
        escaped = (xml_escape(i) for i in normalized)
        files = [f"    <file>{i}</file>" for i in escaped]

        return "\n".join(["<RCC>", "  <qresource>", *files, "  </qresource>", "</RCC>"])
