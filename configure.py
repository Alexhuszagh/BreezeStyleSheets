'''
    configure
    =========

    Configure icons, stylesheets, and resource files.
'''

import argparse
import glob
import json
import re
import os

home = os.path.dirname(os.path.realpath(__file__))

# Create our arguments.
parser = argparse.ArgumentParser(description='Styles to configure for a Qt application.')
parser.add_argument(
    '--styles',
    help='''comma-separate list of styles to configure. pass `all` to build all themes''',
    default='light,dark',
)
parser.add_argument(
    '--resource',
    help='''output resource file name''',
    default='custom.qrc',
)
parser.add_argument(
    '--pyqt6',
    help='''use PyQt6 rather than PyQt5.''',
    action='store_true'
)

# List of all icons to configure.
icons = {
    # Arrows
    'down_arrow': {
        'default': ['foreground:hex', 'foreground:opacity'],
        'hover': ['highlight:hex', 'highlight:opacity'],
        'disabled': ['midtone:light:hex', 'midtone:light:opacity'],
    },
    'left_arrow': {
        'default': ['foreground'],
        'disabled': ['midtone:light'],
    },
    'right_arrow': {
        'default': ['foreground'],
        'disabled': ['midtone:light'],
    },
    'up_arrow': {
        'default': ['foreground:hex', 'foreground:opacity'],
        'hover': ['highlight:hex', 'highlight:opacity'],
        'disabled': ['midtone:light:hex', 'midtone:light:opacity'],
    },
    # Abstract buttons.
    'checkbox_checked': {
        'default': ['checkbox:light'],
        'disabled': ['checkbox:disabled'],
    },
    'checkbox_indeterminate': {
        'default': ['checkbox:light'],
        'disabled': ['checkbox:disabled'],
    },
    'checkbox_unchecked': {
        'default': ['checkbox:light'],
        'disabled': ['checkbox:disabled'],
    },
    'radio_checked': {
        'default': ['checkbox:light'],
        'disabled': ['checkbox:disabled'],
    },
    'radio_unchecked': {
        'default': ['checkbox:light'],
        'disabled': ['checkbox:disabled'],
    },
    # Dock/Tab widgets
    'close': {
        'default': ['midtone:dark:hex', 'midtone:dark:opacity'],
        'hover': ['close:hover:hex', 'close:hover:opacity'],
        'pressed': ['close:pressed:hex', 'close:pressed:opacity'],
    },
    'undock': {
        'default': ['dock:float'],
    },
    'undock_hover': {
        'default': ['dock:float', 'foreground'],
    },
    # Tree views.
    'branch_open': {
        'default': ['tree:hex', 'tree:opacity'],
        'hover': ['highlight:hex', 'highlight:opacity'],
    },
    'branch_closed': {
        'default': ['tree:hex', 'tree:opacity'],
        'hover': ['highlight:hex', 'highlight:opacity'],
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
    },
    'calendar_previous': {
        'default': ['foreground'],
    },
    'transparent': {
        'default': [],
    },
    'hmovetoolbar': {
        'default': ['midtone:light'],
    },
    'vmovetoolbar': {
        'default': ['midtone:light'],
    },
    'hseptoolbar': {
        'default': ['midtone:light'],
    },
    'vseptoolbar': {
        'default': ['midtone:light'],
    },
    'sizegrip': {
        'default': ['midtone:light'],
    },
    # Dialog icons
    'dialog-cancel': {
        'default': ['foreground'],
    },
    'dialog-close': {
        'default': ['foreground'],
    },
    'dialog-ok': {
        'default': ['foreground'],
    },
    'dialog-open': {
        'default': ['foreground'],
    },
    'dialog-save': {
        'default': ['foreground'],
    },
    'dialog-reset': {
        'default': ['foreground'],
    },
    'dialog-help': {
        'default': ['foreground'],
    },
    'dialog-no': {
        'default': ['foreground'],
    },
    'dialog-discard': {
        'default': ['foreground'],
    },
    # Message icons
    'message-critical': {
        'default': ['critical', 'foreground'],
    },
    'message-information': {
        'default': ['information', 'foreground'],
    },
    'message-question': {
        'default': ['question', 'foreground'],
    },
    'message-warning': {
        'default': ['warning', 'foreground'],
    },
}

def parse_hexcolor(color):
    '''Parse a hexadecimal color.'''

    # Have a hex color: can be 6 or 8 (non-standard) items.
    color = color[1:]
    if len(color) not in (6, 8):
        raise NotImplementedError

    red = int(color[:2], 16)
    green = int(color[2:4], 16)
    blue = int(color[4:6], 16)
    alpha = 1.0
    if len(color) == 8:
        alpha = int(color[6:8], 16) / 100
    return (red, green, blue, alpha)

def parse_rgba(color):
    '''Parse an RGBA color.'''

    # Match our rgba character. Note that this is
    # First split the rgba components to get the inner stuff.
    # Both rgb() and rgba() can have or omit an alpha layer.
    rgba = re.match(r'^\s*rgba?\s*\((.*)\)\s*$', color).group(1)
    split = re.split(r'(?:\s*,\s*)|\s+', rgba)
    if len(split) not in (3, 4):
        raise NotImplementedError
    red = int(split[0])
    green = int(split[1])
    blue = int(split[2])
    alpha = 1.0
    if len(split) == 4:
        alpha = float(split[3])
    return (red, green, blue, alpha)

def parse_color(color):
    '''Parse a color into the RGBA components.'''

    if color.startswith('#'):
        return parse_hexcolor(color)
    elif color.startswith('rgb'):
        return parse_rgba(color)
    raise NotImplementedError

def replace(contents, colors, color_map):
    '''Replace all template values.'''

    for index, key in enumerate(colors):
        sub = f'^{index}^'
        # Need special handling if we have a hex or non:hex character.
        if key.endswith(':hex'):
            color = color_map[key[:-len(':hex')]]
            rgb = [f"{i:02x}" for i in parse_color(color)[:3]]
            value = f'#{"".join(rgb)}'
        elif key.endswith(':opacity'):
            color = color_map[key[:-len(':opacity')]]
            value = str(parse_color(color)[3])
        else:
            value = color_map[key]
        contents = contents.replace(sub, value)
    return contents

def configure_icons(style, color_map):
    '''Configure icons for a given style.'''

    for icon, extensions in icons.items():
        template = f'{home}/template/{icon}.svg.in'
        template_contents = open(template).read()
        for extension, colors in extensions.items():
            contents = replace(template_contents, colors, color_map)
            if extension == 'default':
                filename = f'{style_home}/{style}/{icon}.svg'
            else:
                filename = f'{style_home}/{style}/{icon}_{extension}.svg'
            with open(filename, 'w') as file:
                file.write(contents)

def configure_stylesheet(style, color_map):
    '''Configure the stylesheet for a given style.'''

    contents = open(f'{home}/template/stylesheet.qss.in').read()
    for key, color in color_map.items():
        contents = contents.replace(f'^{key}^', color)
    if args.pyqt6:
        contents = contents.replace('^style^', f'{style}:')
    else:
        contents = contents.replace('^style^', f':/{style}/')

    with open(f'{style_home}/{style}/stylesheet.qss', 'w') as file:
        file.write(contents)

def configure_style(style, color_map):
    '''Configure the icons and stylesheet for a given style.'''

    os.makedirs(f'{style_home}/{style}', exist_ok=True)
    configure_icons(style, color_map)
    configure_stylesheet(style, color_map)

def write_xml(styles, path):
    '''Simple QRC writer.'''

    # Can't be used with PyQt6.
    assert not args.pyqt6
    resources = []
    for style in styles:
        files = os.listdir(f'{style_home}/{style}')
        resources += [f'{style}/{i}' for i in files]
    with open(path, 'w') as file:
        print('<RCC>', file=file)
        print('  <qresource>', file=file)
        for resource in sorted(resources):
            print(f'    <file>{resource}</file>', file=file)
        print('  </qresource>', file=file)
        print('</RCC>', file=file)

def configure(styles, path):
    '''Configure all styles and write the files to a QRC file.'''

    for style in styles:
        # Note: we need comments for maintainability, so we
        # can annotate what works and the rationale, but
        # we don't want to prevent code from working without
        # a complex parser, so we do something very simple:
        # only remove lines starting with '//'.
        with open(f'{home}/theme/{style}.json') as file:
            lines = file.read().splitlines()
        lines = [i for i in lines if not i.strip().startswith('//')]
        color_map = json.loads('\n'.join(lines))
        configure_style(style, color_map)

    if not args.pyqt6:
        # No point generating a resource file for PyQt6,
        # since we can't use rcc6 anyway.
        write_xml(styles, path)

if __name__ == '__main__':
    args = parser.parse_args()
    styles = args.styles.split(',')
    if args.pyqt6:
        style_home = f'{home}/pyqt6'
    else:
        style_home = f'{home}'
    if args.styles == 'all':
        files = glob.glob(f'{home}/theme/*json')
        styles = [os.path.splitext(os.path.basename(i))[0] for i in files]
    configure(styles, args.resource)
