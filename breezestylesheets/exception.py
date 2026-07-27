"""Custom exception types."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from .constants import Framework
    from .types import Loads


class BreezeStyleSheetError(Exception):
    """The base exception type for all errors."""

    message: "str"
    """The descriptive error message of the exception."""

    def __init__(self, message: "str") -> "None":
        """
        Args:
            message: The descriptive error message of the exception.
        """
        super().__init__(message)
        self.message = message


class ParseError(BreezeStyleSheetError):
    """Exceptions that occur when parsing data."""

    data: "Loads"
    """The input data provided to the parser."""

    path: "Path | None"
    """The path to the input file that caused the error, if parsing from file."""

    inner: "Exception | None"
    """The exception that caused the parse error, if applicable."""

    def __init__(
        self,
        message: "str",
        data: "Loads",
        path: "Path | None" = None,
        inner: "Exception | None" = None,
    ) -> "None":
        """
        Args:
            message: The descriptive error message of the exception.
            data: The input data provided to the parser.
            path: The path to the input file that caused the error, if parsing from file.
            inner: The exception that caused the parse error, if applicable.
        """
        super().__init__(message)
        self.message = message
        self.data = data
        self.path = path
        self.inner = inner


class ConfigError(BreezeStyleSheetError):
    """The base exception for all config errors."""


class ConfigParseError(ParseError, ConfigError):
    """Exceptions that occur when parsing configuration data."""


class InvalidFrameworkError(BreezeStyleSheetError):
    """An exception that occurs when the provided framework is unknown."""

    # NOTE: This is unknown so it's not a valid `Framework` type.
    framework: "str"
    """The name of the provided Qt framework."""

    def __init__(self, framework: "str") -> "None":
        super().__init__(f'Got an unsupported Qt framework of "{framework}".')
        self.framework = framework


class ResourceError(BreezeStyleSheetError):
    """The base exception for all Qt resource errors."""


class RccNotFoundError(ResourceError):
    """An exception that occurs when the Qt resource compiler cannot be found."""

    rcc: "Path | str"
    """The name or path to the Qt resource compiler."""

    framework: "Framework"
    """The name of the provided Qt framework."""

    def __init__(self, rcc: "Path | str", framework: "Framework") -> "None":
        super().__init__(f'Unable to find a suitable "{rcc}" executable for framework "{framework}".')
        self.rcc = rcc
        self.framework = framework


class ResourceCompileError(ResourceError):
    """An exception that occurs when there is an external error compiling the Qt resources."""

    rcc: "Path | str"
    """The name or path to the Qt resource compiler."""

    qrc: "Path"
    """The path to the input QRC file."""

    framework: "Framework"
    """The name of the provided Qt framework."""

    inner: "Exception"
    """The exception that caused the compilation error."""

    def __init__(
        self,
        rcc: "Path | str",
        qrc: "Path",
        framework: "Framework",
        inner: "Exception",
    ) -> "None":
        super().__init__(
            f'Unable to find a compile the QRC file "{qrc}" using resource'
            f' compiler "{rcc}" for framework "{framework}".'
        )
        self.rcc = rcc
        self.qrc = qrc
        self.framework = framework
        self.inner = inner
