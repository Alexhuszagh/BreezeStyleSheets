"""A named theme with a given style."""

from typing import TYPE_CHECKING

import os
from dataclasses import dataclass

from .model import EXTENSIONS
from .theme import Theme

if TYPE_CHECKING:
    from .utils import Traversable

__all__ = ["Style"]

DEFAULT = "default"


@dataclass
class Style:
    """The named theme for how to style the Qt Stylesheet."""

    name: "str"
    """The name of the style."""

    theme: "Theme"
    """The theme settings for how to style the Qt Stylesheet."""

    @staticmethod
    def is_template(directory: "Traversable") -> bool:
        """Get if the path is a template directory."""

        from breezestylesheets.icon import IconTemplate
        from breezestylesheets.stylesheet import StyleSheetTemplate

        return directory.is_dir() and (
            StyleSheetTemplate.find(directory) is not None
            or IconTemplate.find_replacements(directory) is not None
        )

    @staticmethod
    def is_extension(directory: "Traversable") -> bool:
        """Get if the path is an extension template directory."""
        return directory.name != DEFAULT and Style.is_template(directory)

    @staticmethod
    def find_extensions(*directories: "Traversable", subset: "set[str] | None" = None) -> "list[Traversable]":
        """
        Find all extensions within the provided directory.

        This returns the full path to all extensions within the directory,
        optionally restricted to the subset, where the name can be found by
        getting the basename of it.

        Args:
            directories: The directories to search for extensions in.
            subset: An subset of extensions to find by the extension name.

        Returns:
            The full path to all found extensions within the directories.
        """

        extensions: "list[Traversable]" = []
        for directory in directories:
            extensions += [i for i in directory.iterdir() if i.is_dir() and Style.is_extension(i)]

        if subset is not None and "all" not in subset:
            extensions = [i for i in extensions if os.path.splitext(i.name)[0] in subset]

        return extensions

    @staticmethod
    def find_styles(*directories: "Traversable", subset: "set[str] | None" = None) -> "list[Traversable]":
        """
        Find all styles within the provided directory.

        This returns the full path to all styles within the directory,
        optionally restricted to the subset, where the name can be found by
        getting the basename of it.

        Args:
            directory: The directory to search for styles in.
            subset: An subset of styles to find by the style name.

        Returns:
            The path to all found styles within the directories.
        """

        styles: "list[Traversable]" = []
        for directory in directories:
            styles += [j for i in EXTENSIONS for j in directory.iterdir() if j.name.endswith(i)]

        if subset is not None and "all" not in subset:
            styles = [i for i in styles if os.path.splitext(i.name)[0] in subset]

        return styles
