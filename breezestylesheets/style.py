"""A named theme with a given style."""

import os
from dataclasses import dataclass
from pathlib import Path

from .model import EXTENSIONS
from .theme import Theme

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
    def is_template(directory: "Path") -> bool:
        """Get if the path is a template directory."""

        from breezestylesheets.icon import IconTemplate
        from breezestylesheets.stylesheet import StyleSheetTemplate

        return os.path.isdir(directory) and (
            StyleSheetTemplate.find(directory) is not None
            or IconTemplate.find_replacements(directory) is not None
        )

    @staticmethod
    def is_extension(directory: "Path") -> bool:
        """Get if the path is an extension template directory."""
        return directory.name != DEFAULT and Style.is_template(directory)

    @staticmethod
    def find_extensions(*directories: "Path", subset: "set[str] | None" = None) -> "list[Path]":
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

        extensions: "list[Path]" = []
        for directory in directories:
            extensions += [i for i in directory.absolute().iterdir() if i.is_dir() and Style.is_extension(i)]

        if subset is not None and "all" not in subset:
            extensions = [i for i in extensions if i.stem in subset]

        return extensions

    @staticmethod
    def find_styles(*directories: "Path", subset: "set[str] | None" = None) -> "list[Path]":
        """
        Find all styles within the provided directory.

        This returns the full path to all styles within the directory,
        optionally restricted to the subset, where the name can be found by
        getting the basename of it.

        Args:
            directory: The directory to search for styles in.
            subset: An subset of styles to find by the style name.

        Returns:
            The full path to all found styles within the directories.
        """

        styles: "list[Path]" = []
        for directory in directories:
            styles += [j for i in EXTENSIONS for j in directory.absolute().glob(f"*{i}")]

        if subset is not None and "all" not in subset:
            styles = [i for i in styles if i.stem in subset]

        return styles
