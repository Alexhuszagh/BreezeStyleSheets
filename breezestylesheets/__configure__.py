'''
configure

Configure icons, stylesheets, and resource files.
'''

# TODO: Change to use the version dynamically
# TODO: HERE!
import typing
import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

# TODO: Add more loaders
from breezestylesheets import Theme, __version__
from breezestylesheets import config as _config  # TODO: Fix the name and imports
from breezestylesheets import exception, resources, types, utils

# TODO: Make this `py39` compatible

home_dir = utils.project_dir()
dist_dir = os.path.join(home_dir, 'dist')
resources_dir = os.path.join(home_dir, 'resources')
template_dir = os.path.join(home_dir, 'template')
theme_dir = os.path.join(home_dir, 'theme')
extension_dir = os.path.join(home_dir, 'extension')


class Config(typing.TypedDict):
    # TODO: Remove this
    themes: dict[str, Theme]
    templates: list[_config.Template]
    no_qrc: bool
    resource: types.PathOrStr


def parse_args(argv=None):
    '''Parse the command-line options.'''

    parser = argparse.ArgumentParser(description='Styles to configure for a Qt application.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument(
        '--styles',
        help='comma-separate list of styles to configure. pass `all` to build all themes',
        default='light-blue,dark-blue',
    )
    parser.add_argument(
        '--extensions',
        help='comma-separate list of styles to configure. pass `all` to build all themes',
        default='',
    )
    parser.add_argument(
        '--resource',
        help='output qrc resource file name',
        default='breeze.qrc',
    )
    parser.add_argument(
        '--no-qrc',
        help='do not build QRC resources.',
        action='store_true',
    )
    parser.add_argument(
        '--output-dir',
        help='the default output directory path',
        default=Path(dist_dir),
        type=Path,
    )
    parser.add_argument(
        '--qt-framework',
        help=(
            'target framework to build for. Default = pyqt5. '
            'Note: building for PyQt6 requires PySide6-rcc to be installed.'
        ),
        choices=['pyqt5', 'pyqt6', 'pyside2', 'pyside6'],
        default='pyqt5',
    )
    parser.add_argument(
        '--clean', help='clean dist directory prior to configuring themes.', action='store_true'
    )
    parser.add_argument(
        '--rcc',
        help=(
            'path to the rcc executable. '
            'Overrides rcc of chosen framework. '
            'Only use if system cannot find the rcc exe.'
        ),
    )
    parser.add_argument(
        '--compiled-resource',
        help='output compiled python resource file.',
    )
    parser.add_argument(
        '--use-default-compression',
        help='use the default Qt compression rather than the more efficient custom compression.',
        action='store_true',
    )
    args = parser.parse_args(argv)
    parse_styles(args)
    parse_extensions(args)

    return args


def split_csv(string: str) -> list[str]:
    '''Split a list of values provided as comma-separated values.'''

    values = map(str.strip, string.split(','))
    return [i for i in values if i]


def parse_styles(args):
    '''Parse a list of valid styles.'''

    values = split_csv(args.styles)
    if 'all' in values:
        files = glob.glob(f'{theme_dir}/*json')
        values = [os.path.splitext(os.path.basename(i))[0] for i in files]
    args.styles = values


def parse_extensions(args):
    '''Parse a list of valid extensions.'''

    values = split_csv(args.extensions)
    if 'all' in values:
        values = []
        for dirname in os.listdir(extension_dir):
            ext = f'{extension_dir}/{dirname}'
            ext_files = ('stylesheet.qss.in', 'icons.json')
            paths = [f'{ext}/{i}' for i in ext_files]
            if os.path.isdir(ext) and any(os.path.exists(i) for i in paths):
                values.append(dirname)

    args.extensions = values


def configure_icons(config: Config, style, qt_dist):
    '''Configure icons for a given style.'''

    theme = config['themes'][style]
    for template in config['templates']:
        for icon in template.icons:
            rendered = icon.render(theme)
            for name, svg in rendered.items():
                filename = f'{qt_dist}/{style}/{name}.svg'
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(svg)


def configure_stylesheet(config: Config, style, qt_dist, style_prefix):
    '''Configure the stylesheet for a given style.'''

    theme = config['themes'][style]
    stylesheet = '\n'.join([i.stylesheet for i in config['templates']])
    stylesheet = theme.render(stylesheet, style_prefix)

    with open(f'{qt_dist}/{style}/stylesheet.qss', 'w', encoding='utf-8') as file:
        file.write(stylesheet)


def configure_style(config: Config, style, qt_dist):
    '''Configure the icons and stylesheet for a given style.'''

    def configure_qt(qt_dist, style_prefix):
        os.makedirs(f'{qt_dist}/{style}', exist_ok=True)
        # Need to pass the qt_dist dir.
        configure_icons(config, style, qt_dist)
        configure_stylesheet(config, style, qt_dist, style_prefix)

    # Need to replace the URL paths for loading icons/
    # assets. This uses the resource system, AKA,
    # `url(:/dark/path/to/resource)`.
    if not config['no_qrc']:
        configure_qt(qt_dist, f':/{style}/')


def write_qrc(config: Config, qt_dist: types.PathOrStr) -> None:
    '''Simple QRC writer.'''

    # NOTE: We also want to create aliases for light-blue and dark-blue from our
    # light and dark. See:
    #   https://github.com/Alexhuszagh/BreezeStyleSheets/pull/101#issuecomment-2336476041
    resources = []
    for style in config['themes'].keys():
        files = os.listdir(f'{qt_dist}/{style}')
        resources += [f'{style}/{i}' for i in files]
    if 'dark-blue' in config['themes'].keys():
        resources.append('dark/stylesheet.qss')
    if 'light-blue' in config['themes'].keys():
        resources.append('light/stylesheet.qss')

    qrc_path = config['resource']
    if not os.path.isabs(qrc_path):
        qrc_path = f'{qt_dist}/{qrc_path}'
    with open(qrc_path, 'w', encoding='utf-8') as file:
        print('<RCC>', file=file)
        print('  <qresource>', file=file)
        for resource in sorted(resources):
            # TODO: Need to escape the resources here!
            print(f'    <file>{resource}</file>', file=file)
        print('  </qresource>', file=file)
        print('</RCC>', file=file)


def compile_resource(args: argparse.Namespace) -> None:
    '''Compile our resource file to a standalone Python file.'''

    resource_path: str = args.resource
    compiled_resource_path: str = args.compiled_resource
    if not os.path.isabs(resource_path):
        resource_path = f'{args.output_dir}/{resource_path}'
    if not os.path.isabs(compiled_resource_path):
        compiled_resource_path = f'{resources_dir}/{compiled_resource_path}'

    compression: resources.Compression = 'lzma'
    if not args.use_default_compression:
        compression = 'default'
    try:
        resources.compile(
            qrc=resource_path,
            dst=compiled_resource_path,
            framework=args.qt_framework,
            rcc=args.rcc,
            compression=compression,
        )
    except exception.ResourceCompileError as error:
        inner = typing.cast('subprocess.CalledProcessError', error.inner)
        if b'File does not exist' in inner.stderr:
            print('ERROR: Ensure qrc file exists or deselect "no-qrc" option!', file=sys.stderr)
        else:
            print(f'ERROR: Got an unknown error of "{inner.stderr.decode("utf-8")}"!', file=sys.stderr)
        raise SystemExit from error
    except exception.RccNotFoundError as error:
        if args.rcc:
            print('ERROR: rcc path invalid!', file=sys.stderr)
        else:
            print('ERROR: Ensure rcc executable exists for chosen framework!', file=sys.stderr)
        print(
            'Required rcc for PyQt5: pyrcc5',
            'Required rcc for PySide6 & PyQt6: PySide6-rcc',
            'Required rcc for PySide2: PySide2-rcc',
            '',
            'if using venv, activate it or provide path to rcc.',
            sep='\n',
            file=sys.stderr,
        )
        raise SystemExit from error


def configure(args: argparse.Namespace) -> None:
    '''Configure all styles and write the files to a QRC file.'''

    if args.clean:
        shutil.rmtree(args.output_dir, ignore_errors=True)

    # Need to convert our styles accordingly.
    # TODO: Add hints, can remove them later
    config: Config = {'themes': {}, 'templates': [], 'no_qrc': args.no_qrc, 'resource': args.resource}
    # TODO: Fix this!
    config['templates'].append(_config.Template.from_directory(template_dir))
    for style in args.styles:
        config['themes'][style] = Theme.load(f'{theme_dir}/{style}.json')
    for extension in args.extensions:
        config['templates'].append(_config.Template.from_directory(f'{extension_dir}/{extension}'))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for style in config['themes']:
        configure_style(config, style, str(args.output_dir))

    # Create aliases for our light-blue and dark-blue styles to light and dark.
    # Only create aliases if light-blue and/or dark-blue are to be built.
    aliases = set(args.styles) & {'dark-blue', 'light-blue'}
    for theme in aliases:
        source = args.output_dir / theme / 'stylesheet.qss'
        destination = args.output_dir / theme.split('-')[0] / 'stylesheet.qss'
        destination.parent.mkdir(exist_ok=True)
        shutil.copy2(source, destination)

    # Create and compile our resource files.
    if not args.no_qrc:
        write_qrc(config, str(args.output_dir))
    if args.compiled_resource is not None:
        compile_resource(args)


def main(argv: 'list[str] | None' = None):
    '''Configuration entry point'''
    configure(parse_args(argv))


if __name__ == '__main__':
    sys.exit(main())
