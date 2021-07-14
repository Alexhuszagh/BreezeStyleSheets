'''
    configure
    =========

    Configure the assets and stylesheets.
'''

import glob
import os

home = os.path.dirname(os.path.realpath(__file__))
# TODO(ahuszagh) Need configure for the stylesheets.
# TODO(ahuszagh) Need configure for the assets.
# TODO(ahuszagh) Need a script to generate the qrc
#   Should be easy: styles.qss + assets.

# Assets should be easy.

colors_map = {
    'light': {},
    'dark': {
        'foreground': '#eff0f1',
        'background': '#31363b',
        'hover': '#3daee9',
        'hover_light': '#58d3ff',
        # Going to need more than 1 disabled.
        'disabled': '#b0b0b0',
        'disabled_light': '#c8c9ca',
        # Single-use colors.
        'close': '#626568',
        'close_hover': '#b37979',
        'close_pressed': '#b33e3e',
        'undock': '#a2a2a2',
    },
}

assets = {
    # Arrows
    'down_arrow': {
        'default': ['foreground'],
        'hover': ['hover'],
        'disabled': ['disabled'],
    },
    'left_arrow': {
        'default': ['foreground'],
        'disabled': ['disabled'],
    },
    'right_arrow': {
        'default': ['foreground'],
        'disabled': ['disabled'],
    },
    'up_arrow': {
        'default': ['foreground'],
        'hover': ['hover'],
        'disabled': ['disabled'],
    },
    # Abstract buttons.
    'checkbox_checked': {
        'default': ['hover_light'],
        'disabled': ['disabled_light'],
    },
    'checkbox_indeterminate': {
        'default': ['hover_light'],
        'disabled': ['disabled_light'],
    },
    'checkbox_unchecked': {
        'default': ['hover_light'],
        'disabled': ['disabled_light'],
    },
    'radio_checked': {
        'default': ['hover_light'],
        'disabled': ['disabled_light'],
    },
    'radio_unchecked': {
        'default': ['hover_light'],
        'disabled': ['disabled_light'],
    },
    # Dock/Tab widgets
    'close': {
        'default': ['close'],
        'hover': ['close_hover'],
        'pressed': ['close_pressed'],
    },
    'undock': {
        'default': ['undock'],
    },
    'undock_hover': {
        'default': ['undock', 'foreground'],
    },
    # TODO(ahuszagh) Add more widgets here...
}

def replace(contents, colors, color_map):
    '''Replace all template values.'''

    for index, color in enumerate(colors):
        sub = f'^{index}^'
        contents = contents.replace(sub, color_map[color])
    return contents

def configure(style):
    '''Configure for a given style.'''

    color_map = colors_map[style]
    for base_image, extensions in assets.items():
        template = f'{home}/assets/{base_image}.svg.in'
        template_contents = open(template).read()
        for extension, colors in extensions.items():
            contents = replace(template_contents, colors, color_map)
            if extension == 'default':
                filename = f'{home}/{style}/{base_image}.svg'
            else:
                filename = f'{home}/{style}/{base_image}_{extension}.svg'
            with open(filename, 'w') as file:
                file.write(contents)

if __name__ == '__main__':
    configure('dark')
    #configure('light')
