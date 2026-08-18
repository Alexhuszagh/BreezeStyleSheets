"""Project paths."""

from collections.abc import Iterator
from typing import IO, Protocol, cast

import os
import sys
from pathlib import Path

if sys.version_info >= (3, 9, 0):
    from importlib.resources import files


try:
    from importlib.resources.abc import Traversable  # type: ignore
except ImportError:
    # NOTE: Although it says `Traversable` was added to `importlib.resources.abc` in
    # 3.9, it's not actually necessarily defined event in 3.10. Just define the
    # identical protocol, since `files` still works, until we get to a version
    # (3.12) where we can guarantee it works.
    class Traversable(Protocol):  # type: ignore
        def iterdir(self) -> "Iterator[Traversable]": ...
        def read_bytes(self) -> "bytes": ...
        def read_text(self, encoding: "str | None" = None) -> "str": ...
        def is_dir(self) -> "bool": ...
        def is_file(self) -> "bool": ...
        def joinpath(self, *descendants: "str | os.PathLike[str]") -> "Traversable": ...
        def __truediv__(self, child: "str | os.PathLike[str]") -> "Traversable": ...
        def open(self, mode: "str" = "r", *args, **kwargs) -> IO: ...
        @property
        def name(self) -> str: ...


def package_dir() -> "Path":  # TODO: REMOVE AND TESTS ONLY
    """Get the directory containing the current package."""
    return Path(__file__).parent.parent


def project_dir() -> "Path":  # TODO: REMOVE AND TESTS ONLY
    """Get the directory containing the current project."""
    return package_dir().parent


def module() -> str:
    """Get the name of the top-level module of this package."""
    return __name__.split(".", maxsplit=1)[0]


if sys.version_info >= (3, 9, 0):

    def resource_dir() -> "Traversable":
        """Get a traversable object to access the files of the current package."""
        return cast("Traversable", files(module()))

else:

    def resource_dir() -> "Traversable":
        """Get a traversable object to access the files of the current package."""
        try:
            return Path(__file__).parent.parent
        except (NameError, TypeError):
            raise RuntimeError("Unable to extract resources: is the project potentially zipped?") from None


def theme_dir() -> "Traversable":
    """Get a traversable object to access all the custom themes."""
    return resource_dir() / "theme"


def template_dir() -> "Traversable":
    """Get a traversable object to access all the custom templates."""
    return resource_dir() / "template"
