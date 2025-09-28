'''
color

Methods and helpers for computing colors via manipulations.
'''

import colorsys

from pydantic_extra_types.color import Color


def is_light(color: Color) -> bool:
    '''
    Determine if the color is bright as a quick estimate.

    Args:
        color (`Color`): The color to check.

    Returns:
        `bool`: If the color is perceived as light.
    '''
    r, g, b, *_ = color.as_rgb_tuple()
    return is_light_rgb(r, g, b)


def is_light_hsl(h: float, s: float, l: float) -> bool:  # noqa
    '''
    Determine if the color is bright as a quick estimate from the HSL components.

    Args:
        h: The hue value, as a fraction of a degree, from [0, 1].
        s: The saturation value from [0, 1].
        l: The lightness value, from [0, 1].

    Returns:
        `bool`: If the color is perceived as light.
    '''
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return is_light_rgb(int(r * 255), int(g * 255), int(b * 255))


def is_light_rgb(r: int, g: int, b: int) -> bool:
    '''
    Determine if the color is bright as a quick estimate from the RGB components.

    Args:
        r: The red value, from [0, 255].
        g: The green value, from [0, 255].
        b: The blue value, from [0, 255].

    Returns:
        `bool`: If the color is perceived as light.
    '''
    return ((5 * g) + (2 * r) + b) > (8 * 128)
