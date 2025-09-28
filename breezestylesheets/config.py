'''
config

Models and helpers to load the Stylesheet configuration options.
'''

import typing
import contextlib
import io
import json
import os.path
from collections.abc import Mapping, Sequence

from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic_extra_types.color import Color
from .exception import ConfigParseError

JSONKey: 'typing.TypeAlias' = 'str'
JSONValue: 'typing.TypeAlias' = 'JSONPrimitive | JSONArray | JSONObject'
JSONPrimitive: 'typing.TypeAlias' = 'float | str | None'
JSONArray: 'typing.TypeAlias' = Sequence['JSONPrimitive | JSONArray | JSONObject']
JSONObject: 'typing.TypeAlias' = Mapping['JSONKey', 'JSONPrimitive | JSONArray | JSONObject']

__all__ = ['Config', 'load', 'loads']


def _expand_alias_choices(value: 'str') -> 'tuple[str, ...]':
    '''Expand foreground and other choices to create all permutations of our choices.'''

    # NOTE: This takes the `.` and `foreground`/`background` syntax, which expands this
    result = set()
    result.add(value)
    result.add(value.replace('foreground', 'fg'))
    result.add(value.replace('background', 'bg'))
    result.add(value.replace('alternate', 'alt'))
    updated: list[str] = []
    if '.' not in value:
        updated += [f'{i}.default' for i in result]
        updated += [f'{i}:default' for i in result]
        updated += [f'{i}-default' for i in result]
    else:
        updated += [i.replace('.', ':') for i in result]
        updated += [i.replace('.', '-') for i in result]
    result.update(updated)

    return tuple(sorted(result))


def _alias_choices(value: 'str', *extras: str) -> 'AliasChoices':
    '''Get the alias choices from the expanded values.'''
    return AliasChoices(*_expand_alias_choices(value), *extras)


class Config(BaseModel):
    '''The configuration settings for how to style the QT Stylesheet.'''

    model_config: typing.ClassVar[ConfigDict] = ConfigDict(extra='forbid')
    '''Additional parameters for how to configure Pydantic.'''

    foreground: 'Color' = Field(validation_alias=_alias_choices('foreground'))
    '''The main foreground color.'''

    # TODO: Change to prefer nested syntax. This should likely join all nested
    # fields with a period syntax to enable this format

    foreground_light: 'Color' = Field(validation_alias=_alias_choices('foreground.light'))
    '''Lighter foreground color for selected items.'''

    background: 'Color' = Field(validation_alias=_alias_choices('background'))
    '''The main background color.'''

    background_alternate: 'Color' = Field(validation_alias=_alias_choices('background.alternate'))
    '''Alternate background color for styles.'''

    highlight: 'Color' = Field(validation_alias=_alias_choices('highlight'))
    '''Main color to highlight widgets, such as on hover events.'''

    highlight_dark: 'Color' = Field(validation_alias=_alias_choices('highlight.dark'))
    '''Color for selected widgets so hover events can change widget color.'''

    highlight_alternate: 'Color' = Field(validation_alias=_alias_choices('highlight.alternate'))
    '''Alternate highlight color for hovered widgets in QAbstractItemViews.'''

    midtone: 'Color' = Field(validation_alias=_alias_choices('midtone'))
    '''Main midtone color, such as for borders.'''

    midtone_light: 'Color' = Field(validation_alias=_alias_choices('midtone.light'))
    '''Lighter color for midtones, such as for certain disabled widgets.'''

    midtone_dark: 'Color' = Field(validation_alias=_alias_choices('midtone.dark'))
    '''Darker midtone, such as for the background of QPushButton and QSlider.'''

    midtone_hover: 'Color' = Field(validation_alias=_alias_choices('midtone.hover'))
    '''Lighter midtone for separator hover events.'''

    view_checked: 'Color' = Field(validation_alias=_alias_choices('view.checked'))
    '''Color for checked widgets in QAbstractItemViews.'''

    view_hover: 'Color' = Field(validation_alias=_alias_choices('view.hover'))
    '''Hover background color in QAbstractItemViews.'''

    view_corner: 'Color' = Field(validation_alias=_alias_choices('view.corner'))
    '''Background color for the corner widget in a QAbstractItemView.'''

    view_header_border: 'Color' = Field(validation_alias=_alias_choices('view.header.border'))
    '''Border color between items in a QHeaderView.'''

    view_header: 'Color' = Field(validation_alias=_alias_choices('view.header'))
    '''Background color for a QHeaderView.'''

    view_border: 'Color' = Field(validation_alias=_alias_choices('view.border'))
    '''Border color Between items in a QAbstractItemView.'''

    view_background: 'Color' = Field(validation_alias=_alias_choices('view.background'))
    '''Background for QAbstractItemViews.'''

    toolbar_horizontal_background: 'Color' = Field(
        validation_alias=_alias_choices('toolbar.horizontal.background'),
    )
    '''Background for a horizontal QToolBar.'''

    toolbar_vertical_background: 'Color' = Field(
        validation_alias=_alias_choices('toolbar.vertical.background'),
    )
    '''Background for a vertical QToolBar.'''

    text_background: 'Color' = Field(validation_alias=_alias_choices('text.background'))
    '''Background for widgets with text input.'''

    tab_background_selected: 'Color' = Field(validation_alias=_alias_choices('tab.background.selected'))
    '''Background for the currently selected tab.'''

    tab_background: 'Color' = Field(validation_alias=_alias_choices('tab.background'))
    '''Background for non-selected tabs.'''

    tree: 'Color' = Field(validation_alias=_alias_choices('tree'))
    '''Color for the branch/arrow icons in a QTreeView.'''

    slider_foreground: 'Color' = Field(validation_alias=_alias_choices('slider.foreground'))
    '''
    Color for the chunk of a QProgressBar, the active groove of a QSlider,
    and the border of a hovered QSlider handle.
    '''

    slider_handle_background: 'Color' = Field(validation_alias=_alias_choices('slider.handle.background'))
    '''Background color for the handle of a QSlider.'''

    menu_disabled: 'Color' = Field(validation_alias=_alias_choices('menu.disabled'))
    '''Color for a disabled menubar/menu item.'''

    checkbox_light: 'Color' = Field(validation_alias=_alias_choices('checkbox.light'))
    '''Color for a checked/hovered QCheckBox or QRadioButton.'''

    checkbox_disabled: 'Color' = Field(validation_alias=_alias_choices('checkbox.disabled'))
    '''Color for a disabled or unchecked/unhovered QCheckBox or QRadioButton.'''

    scrollbar_hover: 'Color' = Field(validation_alias=_alias_choices('scrollbar.hover'))
    '''
    Color for the handle of a scrollbar. Due to limitations of Qt stylesheets, any
    handle of a scrollbar must be treated like it's hovered.
    '''

    scrollbar_background: 'Color' = Field(validation_alias=_alias_choices('scrollbar.background'))
    '''Background for a non-hovered scrollbar.'''

    scrollbar_background_hover: 'Color' = Field(validation_alias=_alias_choices('scrollbar.background.hover'))
    '''Background for a hovered scrollbar.'''

    button_background: 'Color' = Field(validation_alias=_alias_choices('button.background'))
    '''Default background for a QPushButton.'''

    button_background_pressed: 'Color' = Field(validation_alias=_alias_choices('button.background.pressed'))
    '''Background for a pressed QPushButton.'''

    button_border: 'Color' = Field(validation_alias=_alias_choices('button.border'))
    '''Border for a non-hovered QPushButton.'''

    button_disabled: 'Color' = Field(validation_alias=_alias_choices('button.disabled'))
    '''Background for a disabled QPushButton, or fallthrough for disabled QWidgets.'''

    close_hover: 'Color' = Field(validation_alias=_alias_choices('close.hover'))
    '''Color of a dock/tab close icon when hovered.'''

    close_pressed: 'Color' = Field(validation_alias=_alias_choices('close.pressed'))
    '''Color of a dock/tab close icon when pressed.'''

    dock_background: 'Color' = Field(validation_alias=_alias_choices('dock.background'))
    '''Default background color for QDockWidget and title.'''

    dock_float: 'Color' = Field(validation_alias=_alias_choices('dock.float'))
    '''Color for the float icon for QDockWidgets.'''

    critical: 'Color' = Field(validation_alias=_alias_choices('critical'))
    '''Background color for the QMessageBox critical icon.'''

    information: 'Color' = Field(validation_alias=_alias_choices('information'))
    '''Background color for the QMessageBox information icon.'''

    question: 'Color' = Field(validation_alias=_alias_choices('question'))
    '''Background color for the QMessageBox question icon.'''

    warning: 'Color' = Field(validation_alias=_alias_choices('warning'))
    '''Background color for the QMessageBox warning icon.'''

    ads_tab_focused: 'Color' = Field(validation_alias=_alias_choices('ads.tab.focused', 'ads-tab:focused'))
    '''The background color for an Advanced Docking System Tab.'''

    ads_border_focused: 'Color' = Field(
        validation_alias=_alias_choices('ads.border.focused', 'ads-border:focused')
    )
    '''The background color for an Advanced Docking System border.'''


class CommentsDecoder(json.JSONDecoder):
    '''
    A custom decoder that removes simple comments from the JSON input.

    This removes only lines starting with `//`.
    '''

    # pylint: disable-next=arguments-differ
    def decode(self, s: 'str') -> 'JSONValue':  # type: ignore # noqa
        '''Return the Python representation of s (a str instance containing a JSON document).'''
        lines = s.splitlines()
        lines = [i for i in lines if not i.strip().startswith('//')]
        return typing.cast('JSONValue', super().decode('\n'.join(lines)))


def load(path: 'str | os.PathLike[str]') -> 'Config':
    '''
    Load the stylesheet configuration settings from file.

    This adds the default configuration settings and validates
    the loaded settings are valid. This supports JSON, YAML, and
    TOML file formats.

    Args:
        path (`str`, `Path`): The path to the file to load.

    Returns:
        `Config`: The loaded stylesheet configuration settings.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the configuration data.
    '''
    with _parse_block(path=path):
        with open(path, encoding='utf-8') as file:
            return loads(file.read(), os.path.splitext(os.path.basename(path))[1])


def loads(s: 'str | bytes | bytearray', extension: 'str') -> 'Config':
    '''
    Load the stylesheet configuration settings from a document.

    This adds the default configuration settings and validates
    the loaded settings are valid. This supports JSON, YAML, and
    TOML file formats.

    Args:
        s (`str`, `bytes`, `bytearray`): The document data, as a string or UTF-8 encoded bytes.
        extension (str): The extension of the file (to determine the file type).

    Returns:
        `Config`: The loaded stylesheet configuration settings.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the configuration data.
    '''
    with _parse_block():
        # NOTE: Migrate to `match` with 3.10+ support.
        if extension in ('.json', '.jsonc'):
            return _loads_json(s)
        if extension in ('.yml', '.yaml'):
            return _loads_yaml(s)
        if extension == '.toml':
            return _loads_toml(s)
        if extension == '.xml':
            return _loads_xml(s)
        raise ValueError(f'Got an unknown file type of "{extension}".')


def _loads_json(s: 'str | bytes | bytearray') -> 'Config':
    '''
    Load the stylesheet configuration settings from a document.

    This adds the default configuration settings and validates
    the loaded settings are valid.

    Args:
        s (`str`, `bytes`, `bytearray`): The JSON document data, as a string or UTF-8 encoded bytes.

    Returns:
        `Config`: The loaded stylesheet configuration settings.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the configuration data.
    '''
    value = json.loads(_decode(s), cls=CommentsDecoder)
    return Config.model_validate(_transform_nested(value))


def _loads_yaml(s: 'str | bytes | bytearray') -> 'Config':
    '''
    Load the stylesheet configuration settings from a document.

    This adds the default configuration settings and validates
    the loaded settings are valid.

    Args:
        s (`str`, `bytes`, `bytearray`): The YAML document data, as a string or UTF-8 encoded bytes.

    Returns:
        `Config`: The loaded stylesheet configuration settings.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the configuration data.
    '''

    # pylint: disable-next=import-error
    import yaml  # type: ignore # noqa

    value = yaml.safe_load(io.StringIO(_decode(s)))
    return Config.model_validate(_transform_nested(value))


def _loads_toml(s: 'str | bytes | bytearray') -> 'Config':
    '''
    Load the stylesheet configuration settings from a document.

    This adds the default configuration settings and validates
    the loaded settings are valid.

    Args:
        s (`str`, `bytes`, `bytearray`): The TOML document data, as a string or UTF-8 encoded bytes.

    Returns:
        `Config`: The loaded stylesheet configuration settings.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the configuration data.
    '''

    try:
        # pylint: disable-next=import-error
        import tomllib  # type # noqa
    except ImportError:
        # pylint: disable-next=import-error
        import tomli as tomllib  # type: ignore # noqa

    value = tomllib.loads(_decode(s))
    return Config.model_validate(_transform_nested(value))


def _loads_xml(s: 'str | bytes | bytearray') -> 'Config':
    '''
    Load the stylesheet configuration settings from a document.

    This adds the default configuration settings and validates
    the loaded settings are valid.

    Args:
        s (`str`, `bytes`, `bytearray`): The XML document data, as a string or UTF-8 encoded bytes.

    Returns:
        `Config`: The loaded stylesheet configuration settings.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the configuration data.
    '''

    # pylint: disable-next=import-error
    import xml2dict  # type: ignore # noqa

    value = xml2dict.parse(_decode(s))
    return Config.model_validate(_transform_nested(value))


def _decode(s: 'str | bytes | bytearray') -> 'str':
    '''Decode the value to string as UTF-8.'''
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('utf-8')
    return s


def _transform_nested(v: 'JSONObject') -> 'dict[str, str]':
    '''Transform nested keys in a JSON object to `key.nested` syntax.'''

    result: dict[str, str] = {}
    for key, value in v.items():
        if not isinstance(key, str) or not isinstance(value, (str, Mapping)):
            raise ValueError(f'Expected JSON value to be str or mapping, got "{type(value)}".')
        if isinstance(value, str):
            result[key] = value
        elif isinstance(value, Mapping):
            nested = _transform_nested(value)
            for subkey, subvalue in nested.items():
                result[f'{key}:{subkey}'] = subvalue

    return result


@contextlib.contextmanager
def _parse_block(
    data: 'str | bytes | bytearray | None' = None,
    path: 'str | os.PathLike[str] | None' = None,
) -> 'typing.Iterator[None]':
    '''A helper to parse the config data within a context block.'''
    try:
        yield
    except ConfigParseError as error:
        error.path = error.path or path
        raise
    except Exception as error:
        if data is None and path is None:
            raise ValueError('Must provide either the data or the path.') from error
        if data is None:
            assert path is not None
            with open(path, encoding='utf-8') as file:
                data = file.read()
        raise ConfigParseError(str(error), data, path, error) from error
