"""
A set of pre-defined colors for our examples.

These are meant to display visual clarity, not be
used in actual code.
"""

from typing import TypeVar
from typing_extensions import TypeAlias

from functools import cached_property

from breezestylesheets.detect import SystemTheme  # type: ignore

_RGBA: TypeAlias = "tuple[int, int, int, int]"
_ColorsT = TypeVar("_ColorsT", bound="Colors")


class Colors:
    """A preset library of colors to stylize elements based on the stylesheet."""

    theme: SystemTheme
    """The luminosity of the stylesheet, or null if not known."""

    def __init__(self, theme: SystemTheme) -> None:
        self.theme = theme

    @classmethod
    def from_stylesheet(cls: "type[_ColorsT]", stylesheet: str) -> _ColorsT:
        if stylesheet.startswith("dark"):
            return cls(SystemTheme.DARK)
        if stylesheet.startswith("light"):
            return cls(SystemTheme.LIGHT)
        return cls(SystemTheme.UNKNOWN)

    @cached_property
    def background(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (49, 54, 59, 255)
        if self.theme == SystemTheme.LIGHT:
            return (239, 240, 241, 255)
        return (255, 255, 0, 255)

    @cached_property
    def foreground(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (239, 240, 241, 255)
        if self.theme == SystemTheme.LIGHT:
            return (49, 54, 59, 255)
        return (0, 255, 255, 255)

    @cached_property
    def selected(self) -> _RGBA:
        return (61, 174, 233, 255)

    @cached_property
    def placeholder_color(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (118, 121, 124, 255)
        if self.theme == SystemTheme.LIGHT:
            return (186, 185, 184, 255)
        return (255, 0, 0, 255)

    @cached_property
    def tick_color(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (51, 78, 94, 255)
        if self.theme == SystemTheme.LIGHT:
            return (61, 173, 232, 51)
        return (255, 0, 0, 255)

    @cached_property
    def tooltip_base(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (49, 54, 59, 255)
        if self.theme == SystemTheme.LIGHT:
            return (49, 54, 59, 255)
        return (0, 255, 0, 255)

    @cached_property
    def tooltip_text(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (239, 240, 241, 255)
        if self.theme == SystemTheme.LIGHT:
            return (49, 54, 59, 255)
        return (0, 0, 255, 255)

    @cached_property
    def mid_tone(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (118, 121, 124, 255)
        if self.theme == SystemTheme.LIGHT:
            return (186, 185, 184, 255)
        return (127, 127, 127, 255)

    @cached_property
    def view_background(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (29, 32, 35, 255)
        if self.theme == SystemTheme.LIGHT:
            return (239, 240, 241, 255)
        return (0, 0, 0, 255)

    @cached_property
    def tab_background(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (44, 48, 52, 255)
        if self.theme == SystemTheme.LIGHT:
            return (217, 216, 215, 255)
        return (0, 0, 0, 255)

    @cached_property
    def highlight_dark(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (42, 121, 163, 255)
        if self.theme == SystemTheme.LIGHT:
            return (45, 147, 200, 127)
        return (255, 0, 0, 255)

    @cached_property
    def groove_background(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (98, 101, 104, 255)
        if self.theme == SystemTheme.LIGHT:
            return (106, 105, 105, 179)
        return (255, 0, 0, 255)

    @cached_property
    def groove_border(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (49, 54, 59, 255)
        if self.theme == SystemTheme.LIGHT:
            return (239, 240, 241, 255)
        return (255, 0, 0, 255)

    @cached_property
    def handle_background(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (29, 32, 35, 255)
        if self.theme == SystemTheme.LIGHT:
            return (239, 240, 241, 255)
        return (255, 0, 0, 255)

    @cached_property
    def handle_border(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (98, 101, 104, 255)
        if self.theme == SystemTheme.LIGHT:
            return (106, 105, 105, 179)
        return (255, 0, 0, 255)

    @cached_property
    def notch(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (51, 78, 94, 255)
        if self.theme == SystemTheme.LIGHT:
            return (61, 173, 232, 51)
        return (61, 173, 232, 51)

    @cached_property
    def link_color(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (88, 166, 255, 255)
        if self.theme == SystemTheme.LIGHT:
            return (70, 132, 204, 255)
        return (204, 70, 200, 255)

    @cached_property
    def link_visited_color(self) -> _RGBA:
        if self.theme == SystemTheme.DARK:
            return (255, 88, 250, 255)
        if self.theme == SystemTheme.LIGHT:
            return (204, 70, 200, 255)
        return (204, 70, 200, 255)
