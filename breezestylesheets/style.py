"""A named theme with a given style."""

from dataclasses import dataclass

from .theme import Theme

__all__ = ["Style"]


@dataclass
class Style:
    """The named theme for how to style the Qt Stylesheet."""

    name: "str"
    """The name of the style."""

    theme: "Theme"
    """The theme settings for how to style the Qt Stylesheet."""
