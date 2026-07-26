"""A named theme with a given style."""

from typing import TYPE_CHECKING

import os
from dataclasses import dataclass

from .theme import Theme

if TYPE_CHECKING:
    from .types import PathOrStr

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
    def is_template(directory: "PathOrStr") -> bool:
        """Get if the path is a template directory."""

        from breezestylesheets.icon import IconTemplate
        from breezestylesheets.stylesheet import StyleSheetTemplate

        return os.path.isdir(directory) and (
            StyleSheetTemplate.get_template_file(directory) is not None
            or IconTemplate.get_replacements_file(directory) is not None
        )

    @staticmethod
    def is_extension(directory: "PathOrStr") -> bool:
        """Get if the path is an extension template directory."""
        return os.path.basename(directory) != DEFAULT and Style.is_template(directory)
