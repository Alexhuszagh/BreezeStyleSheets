"""Methods and helpers for computing colors via manipulations."""

from typing import TYPE_CHECKING

import colorsys

from .pydantic.color import Color

if TYPE_CHECKING:
    from typing import Literal

    RGBA = tuple[int, int, int, float]
    """The red, green, blue, and alpha components of a color."""

    HSLA = tuple[float, float, float, float]
    """The hue, saturation, lightness, and alpha components of a color."""

    Format = Literal["RGBA", "HSLA", "hex"]
    """The valid formats to represent a color as."""


def to_rgba(value: "Color | str") -> "RGBA":
    """
    Parse a color into the RGBA components.

    Args:
        value: The color, either as a string (hex, RGB, or HSL) or a Pydantic color.

    Returns:
        The red, green, blue (from 0-255) and alpha (opacity, from 0-1) components
        of the color.
    """

    if isinstance(value, str):
        value = Color(value)
    color = value.as_rgb_tuple()
    if len(color) == 3:
        color = (*color, 1.0)
    return color


def to_hsla(value: "Color | str") -> "HSLA":
    """
    Parse a color into the HSLA components.

    Args:
        value: The color, either as a string (hex, RGB, or HSL) or a Pydantic color.

    Returns:
        The hue, saturation, lightness, and alpha (opacity) (from 0-1) components
        of the color.
    """

    if isinstance(value, str):
        value = Color(value)
    color = value.as_hsl_tuple()
    if len(color) == 3:
        color = (*color, 1.0)
    return color


def is_light(color: "Color") -> "bool":
    """
    Determine if the color is bright as a quick estimate.

    Args:
        color: The color to check.

    Returns:
        If the color is perceived as light.
    """
    r, g, b, *_ = color.as_rgb_tuple()
    return is_light_rgb(r, g, b)


def is_light_hsl(h: "float", s: "float", l: "float") -> "bool":  # noqa
    """
    Determine if the color is bright as a quick estimate from the HSL components.

    Args:
        h: The hue value, as a fraction of a degree, from [0, 1].
        s: The saturation value from [0, 1].
        l: The lightness value, from [0, 1].

    Returns:
        If the color is perceived as light.
    """
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return is_light_rgb(int(r * 255), int(g * 255), int(b * 255))


def is_light_rgb(r: "int", g: "int", b: "int") -> "bool":
    """
    Determine if the color is bright as a quick estimate from the RGB components.

    Args:
        r: The red value, from [0, 255].
        g: The green value, from [0, 255].
        b: The blue value, from [0, 255].

    Returns:
        If the color is perceived as light.
    """
    return ((5 * g) + (2 * r) + b) > (8 * 128)
