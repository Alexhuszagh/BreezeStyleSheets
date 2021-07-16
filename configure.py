'''
    configure
    =========

    Configure icons, stylesheets, and resource files.
'''

import glob
import os

home = os.path.dirname(os.path.realpath(__file__))
# TODO(ahuszagh) Need a script to generate the qrc
#   Should be easy: styles.qss + assets.

# Assets should be easy.

colors_map = {
    'light': {},
    'dark': {
        # Might want to change the icon names as well to include the color changes.
        #   First we need to stabilize the names.
        # Main theme colors.
        # -----------------
        # Note: these colors are inversed for light
        # themes.
        'foreground': '#eff0f1',
        'foreground-light': '#ffffff',
        'background': '#31363b',
        'alternate-background': '#3b4045',
        'background-light': '#454a4f',
        'highlight': '#3daee9',
        'highlight-light': '#58d3ff',
        'highlight-dark': '#2a79a3',
        'alternate-hover': '#369cd1',
        'midtone': '#76797c',
        'midtone-light': '#b0b0b0',
        'midtone-dark': '#626568',
        'midtone:hover': '#8a8d8f', #9ea0a3
        'view:border': '#3A3939',
        'view:checked': '#334e5e',
        'view:hover': 'rgba(61, 173, 232, 0.1)',
        'view:background': '#232629',
        'tab:background': '#54575B',
        'tree': '#afafaf',
        'checkbox:disabled': '#c8c9ca',
        'button:disabled': '#454545',
        'close:hover': '#b37979',
        'close:pressed': '#b33e3e',
        'dock:float': '#a2a2a2',
    },
}

icons = {
    # Arrows
    'down_arrow': {
        'default': ['foreground'],
        'hover': ['highlight'],
        'disabled': ['midtone-light'],
    },
    'left_arrow': {
        'default': ['foreground'],
        'disabled': ['midtone-light'],
    },
    'right_arrow': {
        'default': ['foreground'],
        'disabled': ['midtone-light'],
    },
    'up_arrow': {
        'default': ['foreground'],
        'hover': ['highlight'],
        'disabled': ['midtone-light'],
    },
    # Abstract buttons.
    'checkbox_checked': {
        'default': ['highlight-light'],
        'disabled': ['checkbox:disabled'],
    },
    'checkbox_indeterminate': {
        'default': ['highlight-light'],
        'disabled': ['checkbox:disabled'],
    },
    'checkbox_unchecked': {
        'default': ['highlight-light'],
        'disabled': ['checkbox:disabled'],
    },
    'radio_checked': {
        'default': ['highlight-light'],
        'disabled': ['checkbox:disabled'],
    },
    'radio_unchecked': {
        'default': ['highlight-light'],
        'disabled': ['checkbox:disabled'],
    },
    # Dock/Tab widgets
    'close': {
        'default': ['midtone-dark'],
        'hover': ['close:hover'],
        'pressed': ['close:pressed'],
    },
    'undock': {
        'default': ['dock:float'],
    },
    'undock_hover': {
        'default': ['dock:float', 'foreground'],
    },
    # Tree views.
    'branch_open': {
        'default': ['tree'],
        'hover': ['highlight'],
    },
    'branch_closed': {
        'default': ['tree'],
        'hover': ['highlight'],
    },
    'branch_end': {
        'default': ['tree'],
    },
    'branch_end_arrow': {
        'default': ['tree'],
    },
    'branch_more': {
        'default': ['tree'],
    },
    'branch_more_arrow': {
        'default': ['tree'],
    },
    'vline': {
        'default': ['tree'],
    },
    'calendar_next': {
        'default': ['foreground'],
        'hover': ['highlight'],
    },
    'calendar_previous': {
        'default': ['foreground'],
        'hover': ['highlight'],
    },
    'transparent': {
        'default': [],
    },
    'hmovetoolbar': {
        'default': ['midtone-light'],
    },
    'vmovetoolbar': {
        'default': ['midtone-light'],
    },
    'hseptoolbar': {
        'default': ['midtone-light'],
    },
    'vseptoolbar': {
        'default': ['midtone-light'],
    },
    'sizegrip': {
        'default': ['midtone-light'],
    }
}

def replace(contents, colors, color_map):
    '''Replace all template values.'''

    for index, color in enumerate(colors):
        sub = f'^{index}^'
        contents = contents.replace(sub, color_map[color])
    return contents

def configure_icons(style):
    '''Configure icons for a given style.'''

    color_map = colors_map[style]
    for icon, extensions in icons.items():
        template = f'{home}/template/{icon}.svg.in'
        template_contents = open(template).read()
        for extension, colors in extensions.items():
            contents = replace(template_contents, colors, color_map)
            if extension == 'default':
                filename = f'{home}/{style}/{icon}.svg'
            else:
                filename = f'{home}/{style}/{icon}_{extension}.svg'
            with open(filename, 'w') as file:
                file.write(contents)

def configure_stylesheet(style):
    '''Configure the stylesheet for a given style.'''

    color_map = colors_map[style]
    contents = open(f'{home}/template/stylesheet.qss.in').read()
    for key, color in color_map.items():
        contents = contents.replace(f'^{key}^', color)
    contents = contents.replace('^style^', style)
    with open(f'{home}/{style}/stylesheet.qss', 'w') as file:
        file.write(contents)

def configure_style(style):
    '''Configure the icons and stylesheet for a given style.'''

    os.makedirs(f'{home}/{style}', exist_ok=True)
    configure_icons(style)
    configure_stylesheet(style)

def configure(styles, resource):
    '''Configure all styles and write the files to a QRC file.'''

    for style in styles:
        configure_style(style)

if __name__ == '__main__':
    # TODO(ahuszagh) Replace with argparse values.
    # Also need to parse from JSON.
    configure(['dark'], None)
    #configure('light')
