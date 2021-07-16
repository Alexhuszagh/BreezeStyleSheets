'''
    configure
    =========

    Configure icons, stylesheets, and resource files.
'''

import glob
import json
import os

home = os.path.dirname(os.path.realpath(__file__))
# TODO(ahuszagh) Need a script to generate the qrc
#   Should be easy: styles.qss + assets.

# List of all icons to configure.
# TODO(ahuszagh) Change this to use templates
#   Should just be a list inside each key.
#       Replace ^0^ with ^foreground^, etc.
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

def configure_icons(style, color_map):
    '''Configure icons for a given style.'''

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

def configure_stylesheet(style, color_map):
    '''Configure the stylesheet for a given style.'''

    contents = open(f'{home}/template/stylesheet.qss.in').read()
    for key, color in color_map.items():
        contents = contents.replace(f'^{key}^', color)
    contents = contents.replace('^style^', style)
    with open(f'{home}/{style}/stylesheet.qss', 'w') as file:
        file.write(contents)

def configure_style(style, color_map):
    '''Configure the icons and stylesheet for a given style.'''

    os.makedirs(f'{home}/{style}', exist_ok=True)
    configure_icons(style, color_map)
    configure_stylesheet(style, color_map)

def configure(styles, resource):
    '''Configure all styles and write the files to a QRC file.'''

    for style in styles:
        # Note: we need comments for maintainability, so we
        # can annotate what works and the rationale, but
        # we don't want to prevent code from working without
        # a complex parser, so we do something very simple:
        # only remove lines starting with '//'.
        with open(f'{home}/configure/{style}.json') as file:
            lines = file.read().splitlines()
        lines = [i for i in lines if not i.strip().startswith('//')]
        color_map = json.loads('\n'.join(lines))
        configure_style(style, color_map)

if __name__ == '__main__':
    # TODO(ahuszagh) Replace with argparse values.
    # Also need to parse from JSON.
    configure(['dark'], None)
    #configure('light')
