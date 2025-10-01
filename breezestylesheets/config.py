'''
config

Models and helpers to load the Stylesheet configuration options.
'''

import typing
import typing_extensions
import contextlib
import io
import json
import os.path
import re
from pathlib import Path

from pydantic import AliasChoices, AliasPath, BaseModel, ConfigDict, Field, TypeAdapter
from pydantic_extra_types.color import Color
from . import color, constants, types, utils
from .exception import ConfigParseError

# NOTE: Using unions directly, rather than the `|` syntax, is needed for 3.9 support,
# with pydantic, which must resolve these hints to define the models.

__all__ = ['Theme']
# NOTE: Union is required for 3.9 support in our base models.
ColorType: 'typing.TypeAlias' = typing.Union[Color, typing.Literal[""]]
_Alias: 'typing.TypeAlias' = 'tuple[str, ...]'


def _expand_alias_choices(value: 'str') -> '_Alias':
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


class Model(BaseModel):
    '''The base model for all configuration options.'''

    model_config: typing.ClassVar[ConfigDict] = ConfigDict(
        extra='forbid',
        ignored_types=(utils.LazyAttribute,),
    )
    '''Additional parameters for how to configure Pydantic.'''

    @utils.lazy_attribute
    @classmethod
    def aliases(cls) -> 'typing.Mapping[str, str]':
        '''
        Get all aliases associated with the class.

        This caches the stored aliases for all resolved values,
        and then computes them to their desired values, allowing
        efficient lookups of instance values from the alias.

        ```python
        {
            'foreground': 'foreground',
            'fg': 'foreground',
            'fg-default': 'foreground',
            'fg.default': 'foreground',
            'fg:default': 'foreground',
            'foreground-default': 'foreground',
        }
        ```

        Returns:
            `dict`: The mapping of all the aliases to the field names.
        '''

        def to_alias(value: str | AliasChoices | AliasPath | None) -> 'list[str]':
            if isinstance(value, str):
                return [value]
            if isinstance(value, AliasChoices):
                return [i for j in value.choices for i in to_alias(j)]
            if isinstance(value, AliasPath):
                return [i for i in value.path if isinstance(i, str)]
            return []

        result: dict[str, str] = {}
        for field, info in cls.model_fields.items():
            result.setdefault(info.alias or field, field)
            for alias in to_alias(info.validation_alias):
                result.setdefault(alias, field)

        return result

    def get(self, alias: str) -> typing.Any:
        '''
        Get a single attribute by the field alias.

        Args:
            alias (`str`): The name of the alias or field to get, such as `foreground`.

        Returns:
            `Any`: The value of that field.

        Raises:
            `ValueError`: If the provided alias is not valid.
        '''
        field = self.aliases.get(alias)
        if field is None:
            raise ValueError(f'Got an unknown alias "{alias}".')
        return getattr(self, field)

    @classmethod
    def load(cls: type[typing_extensions.Self], path: 'types.PathOrStr') -> typing_extensions.Self:
        '''
        Load the stylesheet configuration settings from file.

        This adds the default configuration settings and validates
        the loaded settings are valid. This supports JSON, YAML, TOML,
        and XML file formats.

        Args:
            path (`str`, `Path`): The path to the file to load.

        Returns:
            `Model`: The loaded stylesheet configuration settings.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the configuration data.
        '''
        with _parse_block(path=path):
            with open(path, encoding='utf-8') as file:
                return cls.loads(file.read(), os.path.splitext(os.path.basename(path))[1])

    @classmethod
    def loads(
        cls: type[typing_extensions.Self], s: 'str | bytes | bytearray', extension: 'str'
    ) -> typing_extensions.Self:
        '''
        Load the stylesheet configuration settings from a document.

        This adds the default configuration settings and validates
        the loaded settings are valid. This supports JSON, YAML, TOML,
        and XML file formats.

        Args:
            s (`str`, `bytes`, `bytearray`): The document data, as a string or UTF-8 encoded bytes.
            extension (str): The extension of the file (to determine the file type).

        Returns:
            `Model`: The loaded stylesheet configuration settings.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the configuration data.
        '''
        with _parse_block(data=s):
            return cls.model_validate(_transform_nested(_loads_model(s, extension)))


class Theme(Model):
    '''
    The theme settings for how to style the Qt Stylesheet.

    The theme contains the core color data for converting a stylesheet or icon
    template into the rendered form.

    ## Example

    ```json
    {
        "foreground": "#31363b",
        "foreground:light": "#272b2f",
        "background": "#eff0f1",
        "background:alternate": "#eaebec",
        "highlight": "rgba(51, 164, 223, 0.5)",
        "highlight:dark": "rgba(45, 147, 200, 0.5)",
        "highlight:alternate": "rgba(71, 184, 243, 0.6)",
        "midtone": "#bab9b8",
        "midtone:light": "#bab9b8",
        "midtone:dark": "rgba(106, 105, 105, 0.7)",
        "midtone:hover": "#787876",
        "view:checked": "#b9dae7",
        "view:hover": "rgba(61, 173, 232, 0.2)",
        "toolbar:horizontal:background": "#eff0f1",
        "toolbar:vertical:background": "#eff0f1",
        "view:corner": "#eff0f1",
        "view:header": "#eff0f1",
        "view:header:border": "#bab9b8",
        "view:border": "#bab9b8",
        "view:background": "#eff0f1",
        "text:background": "#eff0f1",
        "tab:background:selected": "#eff0f1",
        "tab:background": "#d9d8d7",
        "tree": "#4b4b4b",
        "slider:foreground": "#3daef3",
        "slider:handle:background": "#eff0f1",
        "menu:disabled": "#bab9b8",
        "checkbox:light": "#272b2f",
        "checkbox:disabled": "#6a6e71",
        "scrollbar:hover": "rgba(51, 164, 223, 0.8)",
        "scrollbar:background": "#eff0f1",
        "scrollbar:background:hover": "#c7c7c6",
        "button:background": "#eaebec",
        "button:background:pressed": "#bedfec",
        "button:border": "#bab9b8",
        "button:checked": "#c7c7c6",
        "button:disabled": "#b4b4b4",
        "close:hover": "#31363b",
        "close:pressed": "#b33e3e",
        "dock:background": "#eaebec",
        "dock:float": "#a2a2a2",
        "critical": "#ff8c9f",
        "information": "#8cd5ff",
        "question": "#c08cff",
        "warning": "#ffff8c",
        "ads-tab:focused": "rgba(61, 173, 232, 0.2)",
        "ads-border:focused": "rgba(61, 173, 232, 0.25)"
    }
    ```
    '''

    foreground: 'Color' = Field(validation_alias=_alias_choices('foreground'))
    '''The main foreground color.'''

    foreground_light: 'ColorType' = Field(validation_alias=_alias_choices('foreground.light'))
    '''Lighter foreground color for selected items.'''

    background: 'Color' = Field(validation_alias=_alias_choices('background'))
    '''The main background color.'''

    background_alternate: 'ColorType' = Field(validation_alias=_alias_choices('background.alternate'))
    '''Alternate background color for styles.'''

    highlight: 'Color' = Field(validation_alias=_alias_choices('highlight'))
    '''Main color to highlight widgets, such as on hover events.'''

    highlight_dark: 'ColorType' = Field(validation_alias=_alias_choices('highlight.dark'))
    '''Color for selected widgets so hover events can change widget color.'''

    highlight_alternate: 'ColorType' = Field(validation_alias=_alias_choices('highlight.alternate'))
    '''Alternate highlight color for hovered widgets in QAbstractItemViews.'''

    midtone: 'Color' = Field(validation_alias=_alias_choices('midtone'))
    '''Main midtone color, such as for borders.'''

    midtone_light: 'ColorType' = Field(validation_alias=_alias_choices('midtone.light'))
    '''Lighter color for midtones, such as for certain disabled widgets.'''

    midtone_dark: 'ColorType' = Field(validation_alias=_alias_choices('midtone.dark'))
    '''Darker midtone, such as for the background of QPushButton and QSlider.'''

    midtone_hover: 'ColorType' = Field(validation_alias=_alias_choices('midtone.hover'))
    '''Lighter midtone for separator hover events.'''

    view_checked: 'Color' = Field(validation_alias=_alias_choices('view.checked'))
    '''Color for checked widgets in QAbstractItemViews.'''

    view_hover: 'ColorType' = Field(validation_alias=_alias_choices('view.hover'))
    '''Hover background color in QAbstractItemViews.'''

    view_corner: 'ColorType' = Field(validation_alias=_alias_choices('view.corner'))
    '''Background color for the corner widget in a QAbstractItemView.'''

    view_header_border: 'ColorType' = Field(validation_alias=_alias_choices('view.header.border'))
    '''Border color between items in a QHeaderView.'''

    view_header: 'ColorType' = Field(validation_alias=_alias_choices('view.header'))
    '''Background color for a QHeaderView.'''

    view_border: 'ColorType' = Field(validation_alias=_alias_choices('view.border'))
    '''Border color Between items in a QAbstractItemView.'''

    view_background: 'ColorType' = Field(validation_alias=_alias_choices('view.background'))
    '''Background for QAbstractItemViews.'''

    toolbar_horizontal_background: 'ColorType' = Field(
        validation_alias=_alias_choices('toolbar.horizontal.background'),
    )
    '''Background for a horizontal QToolBar.'''

    toolbar_vertical_background: 'ColorType' = Field(
        validation_alias=_alias_choices('toolbar.vertical.background'),
    )
    '''Background for a vertical QToolBar.'''

    text_background: 'ColorType' = Field(validation_alias=_alias_choices('text.background'))
    '''Background for widgets with text input.'''

    tab_background_selected: 'ColorType' = Field(validation_alias=_alias_choices('tab.background.selected'))
    '''Background for the currently selected tab.'''

    tab_background: 'ColorType' = Field(validation_alias=_alias_choices('tab.background'))
    '''Background for non-selected tabs.'''

    tree: 'Color' = Field(validation_alias=_alias_choices('tree'))
    '''Color for the branch/arrow icons in a QTreeView.'''

    slider_foreground: 'ColorType' = Field(validation_alias=_alias_choices('slider.foreground'))
    '''
    Color for the chunk of a QProgressBar, the active groove of a QSlider,
    and the border of a hovered QSlider handle.
    '''

    slider_handle_background: 'ColorType' = Field(validation_alias=_alias_choices('slider.handle.background'))
    '''Background color for the handle of a QSlider.'''

    menu_disabled_impl: 'ColorType' = Field(validation_alias=_alias_choices('menu.disabled'))
    '''Internal helper for `menu_disabled`. Do not use directly.'''

    @property
    def menu_disabled(self) -> 'Color':
        '''Color for a disabled menubar/menu item.'''
        if not self.menu_disabled_impl:
            self.menu_disabled_impl = constants.DISABLED[self.is_dark]
        return self.menu_disabled_impl

    @menu_disabled.setter
    def menu_disabled(self, value: 'ColorType') -> None:
        self.menu_disabled_impl = value

    checkbox_light: 'ColorType' = Field(validation_alias=_alias_choices('checkbox.light'))
    '''Color for a checked/hovered QCheckBox or QRadioButton.'''

    checkbox_disabled_impl: 'ColorType' = Field(validation_alias=_alias_choices('checkbox.disabled'))
    '''Internal helper for `checkbox_disabled`. Do not use directly.'''

    @property
    def checkbox_disabled(self) -> 'Color':
        '''Color for a disabled or unchecked/unhovered QCheckBox or QRadioButton.'''
        if not self.checkbox_disabled_impl:
            self.checkbox_disabled_impl = constants.DISABLED[self.is_dark]
        return self.checkbox_disabled_impl

    @checkbox_disabled.setter
    def checkbox_disabled(self, value: 'ColorType') -> None:
        self.checkbox_disabled_impl = value

    scrollbar_hover: 'ColorType' = Field(validation_alias=_alias_choices('scrollbar.hover'))
    '''
    Color for the handle of a scrollbar. Due to limitations of Qt stylesheets, any
    handle of a scrollbar must be treated like it's hovered.
    '''

    scrollbar_background: 'ColorType' = Field(validation_alias=_alias_choices('scrollbar.background'))
    '''Background for a non-hovered scrollbar.'''

    scrollbar_background_hover: 'ColorType' = Field(
        validation_alias=_alias_choices('scrollbar.background.hover')
    )
    '''Background for a hovered scrollbar.'''

    button_background: 'ColorType' = Field(validation_alias=_alias_choices('button.background'))
    '''Default background for a QPushButton.'''

    button_background_pressed: 'ColorType' = Field(
        validation_alias=_alias_choices('button.background.pressed')
    )
    '''Background for a pressed QPushButton.'''

    button_border: 'ColorType' = Field(validation_alias=_alias_choices('button.border'))
    '''Border for a non-hovered QPushButton.'''

    button_checked: 'ColorType' = Field(validation_alias=_alias_choices('button.checked'))
    '''Background for a checked QPushButton.'''

    button_disabled_impl: 'ColorType' = Field(validation_alias=_alias_choices('button.disabled'))
    '''Internal helper for `button_disabled`. Do not use directly.'''

    @property
    def button_disabled(self) -> 'Color':
        '''Background for a disabled QPushButton, or fallthrough for disabled QWidgets.'''
        if not self.button_disabled_impl:
            self.button_disabled_impl = constants.DISABLED[self.is_dark]
        return self.button_disabled_impl

    @button_disabled.setter
    def button_disabled(self, value: 'ColorType') -> None:
        self.button_disabled_impl = value

    close_hover: 'ColorType' = Field(validation_alias=_alias_choices('close.hover'))
    '''Color of a dock/tab close icon when hovered.'''

    close_pressed: 'ColorType' = Field(validation_alias=_alias_choices('close.pressed'))
    '''Color of a dock/tab close icon when pressed.'''

    dock_background: 'ColorType' = Field(validation_alias=_alias_choices('dock.background'))
    '''Default background color for QDockWidget and title.'''

    dock_float: 'ColorType' = Field(validation_alias=_alias_choices('dock.float'))
    '''Color for the float icon for QDockWidgets.'''

    critical_impl: 'ColorType' = Field(validation_alias=_alias_choices('critical'))
    '''Internal helper for `critical`. Do not use directly.'''

    @property
    def critical(self) -> 'Color':
        '''Background color for the QMessageBox critical icon.'''
        if not self.critical_impl:
            self.critical_impl = constants.CRITICAL[self.is_dark]
        return self.critical_impl

    @critical.setter
    def critical(self, value: 'ColorType') -> None:
        self.critical_impl = value

    information_impl: 'ColorType' = Field(validation_alias=_alias_choices('information'))
    '''Internal helper for `information`. Do not use directly.'''

    @property
    def information(self) -> 'Color':
        '''Background color for the QMessageBox information icon.'''
        if not self.information_impl:
            self.information_impl = constants.INFORMATION[self.is_dark]
        return self.information_impl

    @information.setter
    def information(self, value: 'ColorType') -> None:
        self.information_impl = value

    question_impl: 'ColorType' = Field(validation_alias=_alias_choices('question'))
    '''Internal helper for `question`. Do not use directly.'''

    @property
    def question(self) -> 'Color':
        '''Background color for the QMessageBox question icon.'''
        if not self.question_impl:
            self.question_impl = constants.QUESTION[self.is_dark]
        return self.question_impl

    @question.setter
    def question(self, value: 'ColorType') -> None:
        self.question_impl = value

    warning_impl: 'ColorType' = Field(validation_alias=_alias_choices('warning'))
    '''Internal helper for `warning`. Do not use directly.'''

    @property
    def warning(self) -> 'Color':
        '''Background color for the QMessageBox warning icon.'''
        if not self.warning_impl:
            self.warning_impl = constants.WARNING[self.is_dark]
        return self.warning_impl

    @warning.setter
    def warning(self, value: 'ColorType') -> None:
        self.warning_impl = value

    ads_tab_focused: 'ColorType' = Field(
        validation_alias=_alias_choices('ads.tab.focused', 'ads-tab:focused')
    )
    '''The background color for an Advanced Docking System Tab.'''

    ads_border_focused: 'ColorType' = Field(
        validation_alias=_alias_choices('ads.border.focused', 'ads-border:focused')
    )
    '''The background color for an Advanced Docking System border.'''

    @property
    def is_light(self) -> 'bool':
        '''Get if the color scheme is a light theme.'''
        return color.is_light(self.background)

    @property
    def is_dark(self) -> 'bool':
        '''Get if the color scheme is a dark theme.'''
        return not self.is_light

    @typing.overload
    def get_color(self, alias: str, format: None = None) -> 'str | Color': ...

    @typing.overload
    def get_color(self, alias: str, format: 'color.Format') -> 'str': ...

    def get_color(self, alias: str, format: 'color.Format | None' = None) -> 'str | Color':
        '''
        Get a single color by the alias.

        Args:
            alias (`str`): The name of the alias or field to get, such as `foreground`.

        Returns:
            `Color`: The color to use as the replacement.

            `str`: The hex, alpha opacity, or RGBA representation of the color.

            `""`: A value signifying no color, without a transparent replacement.

        Raises:
            `ValueError`: If the provided alias is not valid or the field is not a color.
        '''

        # ensure we have our color data, for the value
        is_hex = alias.endswith((':hex', '.hex', '-hex'))
        is_opacity = not is_hex and alias.endswith((':opacity', '.opacity', '-opacity'))
        if is_hex:
            alias = alias[: -len(':hex')]
        elif is_opacity:
            alias = alias[: -len(':opacity')]

        # get and process our value
        value = self.get(alias)
        if value != '' and not isinstance(value, Color):
            raise ValueError(f'Got an unexpected color value of "{value}" for alias "{alias}".')
        if value == '' and (is_hex or is_opacity):
            raise ValueError(f'Missing required color for alias "{alias}" with hex/opacity variant.')
        if isinstance(value, str):
            return value

        # process our hex and opacity variants
        if is_hex:
            rgb = [f'{i:02x}' for i in color.to_rgba(value)[:3]]
            return f'#{"".join(rgb)}'
        if is_opacity:
            return str(color.to_rgba(value)[3])
        if format == 'RGBA':
            return value.as_rgb()
        if format == 'HSLA':
            return value.as_hsl()
        if format == 'hex':
            return value.as_hex(format='long')
        return value

    def render(self, template: str, style: str) -> str:
        '''
        Render the stylesheet with all placeholders replaced.

        Args:
            template (`str`): The template stylesheet, as a single QSS document.
            style (`str`): The prefix for the style as a QT resource.

        Returns:
            `str`: The fully rendered stylesheet with all placeholders replaced.
        '''
        if not style.startswith(':/'):
            style = f':/{style}'
        if not style.endswith('/'):
            style = f'{style}/'
        return _replace_by_name(template, self).replace('^style^', style)


IconListReplacement: 'typing.TypeAlias' = 'typing.Sequence[str]'
'''
An ordered list of the index-based icon replacements.

These are used to replace indexes, such as `^0^`, with a named placeholder
which will be used when configuring the icon.

```json
["foreground", "background"]
```

These are then used to replace the specifiers in the template: for example, here `^0^` becomes
`foreground` and `^1^` becomes `background`.

```xml
<svg width="24" height="24">
  <path fill="^0^" d=..."/>
  <g transform="scale(0.5) translate(14, 20)">
    <path fill="^1^" d="..."/>
  </g>
</svg>
```
'''

IconDictReplacement: 'typing.TypeAlias' = typing.Mapping[str, IconListReplacement]
'''
A single icon replacement which replaces the icon fields with template specifiers.

This contains which contains the name of the extension(s), which can be `default`
(uses the default name) or a custom value which can be used to extend stylesheets.

```json
{
    "default": ["foreground", "background"]
}
```

These are then used to replace the specifiers in the template: for example, here `^0^` becomes
`foreground` and `^1^` becomes `background`.

```xml
<svg width="24" height="24">
  <path fill="^0^" d=..."/>
  <g transform="scale(0.5) translate(14, 20)">
    <path fill="^1^" d="..."/>
  </g>
</svg>
```
'''

IconReplacement: 'typing.TypeAlias' = typing.Union[IconDictReplacement, IconListReplacement]
'''
A single icon replacement which replaces the icon fields with template specifiers.

This contains which contains the name of the extension(s), which can be `default`
(uses the default name) or a custom value which can be used to extend stylesheets.

```json
{
    "default": ["foreground", "background"]
}
```

Or in simpler form (only supports default):

```json
["foreground", "background"]
```

These are then used to replace the specifiers in the template: for example, here `^0^` becomes
`foreground` and `^1^` becomes `background`.

```xml
<svg width="24" height="24">
  <path fill="^0^" d=..."/>
  <g transform="scale(0.5) translate(14, 20)">
    <path fill="^1^" d="..."/>
  </g>
</svg>
```
'''


class StandardIconReplacements(typing_extensions.TypedDict, total=False):
    '''
    The Qt standard icons that can be used for simple icon styling.

    The fields all correspond to the following Qt enumerated icon names:
    - browser_refresh: `SP_BrowserReload`
    - browser_refresh_stop: `SP_BrowserStop`
    - dialog_apply: `SP_DialogApplyButton`, `SP_DialogYesButton`
    - dialog_ignore: `SP_DialogIgnoreButton`
    - dialog_retry: `SP_DialogRetryButton`
    - dialog_save_all: `SP_DialogSaveAllButton`
    - dialog_yes_to_all: `SP_DialogYesToAllButton`
    - folder_open_link: `SP_DirLinkOpenIcon`
    - horizontal_extension: `SP_ToolBarHorizontalExtensionButton`
    - pause: `SP_MediaPause`
    - play: `SP_MediaPlay`
    - restore_defaults: `SP_RestoreDefaultsButton`
    - seek_backward: `SP_MediaSeekBackward`
    - seek_forward: `SP_MediaSeekForward`
    - skip_backward: `SP_MediaSkipBackward`
    - skip_forward: `SP_MediaSkipForward`
    - stop: `SP_MediaStop`
    - tab_close: `SP_TabCloseButton` (Qt 6.3+)
    - vertical_extension: `SP_ToolBarVerticalExtensionButton`
    - vista_shield: `SP_VistaShield`
    - volume: `SP_MediaVolume`
    - volume_muted: `SP_MediaVolumeMuted`
    '''

    browser_refresh: 'IconReplacement'
    browser_refresh_stop: 'IconReplacement'
    dialog_apply: 'IconReplacement'
    dialog_ignore: 'IconReplacement'
    dialog_retry: 'IconReplacement'
    dialog_save_all: 'IconReplacement'
    dialog_yes_to_all: 'IconReplacement'
    folder_open_link: 'IconReplacement'
    horizontal_extension: 'IconReplacement'
    pause: 'IconReplacement'
    play: 'IconReplacement'
    restore_defaults: 'IconReplacement'
    seek_backward: 'IconReplacement'
    seek_forward: 'IconReplacement'
    skip_backward: 'IconReplacement'
    skip_forward: 'IconReplacement'
    stop: 'IconReplacement'
    tab_close: 'IconReplacement'
    vertical_extension: 'IconReplacement'
    vista_shield: 'IconReplacement'
    volume: 'IconReplacement'
    volume_muted: 'IconReplacement'


IconReplacements: 'typing.TypeAlias' = typing.Union[
    typing.Mapping[str, IconReplacement], StandardIconReplacements
]
'''
A mapping of the icon names to their replacement definitions.

This supports the standard icons and can also be customized with your own icons.

```json
{
    "browser_refresh": {
        "default": ["foreground"]
    },
    "browser_refresh_stop": {
        "default": ["critical"]
    }
}
```

The icon replacements for how they correspond to the replaced colors is
defined in `IconReplacement` .
'''

IconReplacementsAdaptor: 'TypeAdapter[IconReplacements]' = TypeAdapter(IconReplacements)
'''A custom type validator for the icon replacements'''


def load_icon_replacements(path: types.PathOrStr) -> IconReplacements:
    '''
    Load the icon replacements from a file.

    This supports JSON, YAML, TOML, and XML file formats.

    Args:
        path (`str`, `Path`): The path to the file to load.

    Returns:
        `IconReplacements`: The loaded icon replacements.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the data.
    '''
    with _parse_block(path=path):
        with open(path, encoding='utf-8') as file:
            return loads_icon_replacements(file.read(), os.path.splitext(os.path.basename(path))[1])


def loads_icon_replacements(s: 'str | bytes | bytearray', extension: 'str') -> IconReplacements:
    '''
    Load the icon replacements from a document.

    This supports JSON, YAML, TOML, and XML file formats.

    Args:
        s (`str`, `bytes`, `bytearray`): The document data, as a string or UTF-8 encoded bytes.
            extension (str): The extension of the file (to determine the file type).

    Returns:
        `IconReplacements`: The loaded icon replacements.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the data.
    '''
    with _parse_block(data=s):
        return IconReplacementsAdaptor.validate_python(_loads_model(s, extension))


class Icon(Model):
    '''
    The configurations for how to replace the colors within an icon.

    This contains an icon template, the name of the icon used to
    determine icon resource path, and the color replacements for
    the template.
    '''

    name: str
    '''
    The name of the icon.

    This corresponds to the icon written to disk, with the `.svg` suffix, and
    optionally, with an extension suffix as defined in the replacements.
    '''

    template: str
    '''The raw, template SVG data of the icon.'''

    replacements: IconReplacement
    '''
    The template replacements for the icon, optionally with additional extensions defined.

    The replacements **MUST** be defined here, since
    '''

    def render(self, theme: 'Theme') -> typing.Mapping[str, str]:
        '''
        Render the SVG icon with all placeholders replaced.

        The placeholders have a syntax like `^foreground^` (for name-based placeholders),
        or, in some cases, index-based ones like `^0^` which is the index in a list of
        valid color replacements.

        Args:
            theme (`Theme`): The theme with the colors for each configuration.

        Returns:
            `dict`: The template SVG rendered with all placeholders replaced,
            as a mapping of the icon name and the rendered SVG.
        '''

        def with_ext(name: str, ext: str) -> str:
            if ext == 'default':
                return name
            return f'{name}_{ext}'

        result = {}
        if isinstance(self.replacements, typing.Mapping):
            for extension, replacements in self.replacements.items():
                name = with_ext(self.name, extension)
                value = _replace_by_index(self.template, theme, replacements)
                result[name] = value
        else:
            result[self.name] = _replace_by_name(self.template, theme, self.replacements)

        return result


class Template(Model):
    '''
    A theme template, containing the stylesheet and icon templates.

    This contains the data for how to render a single template,
    which may include additional extensions.
    '''

    icons: list[Icon]
    '''A list of icon templates, including their replacements.'''

    stylesheet: str
    '''
    A template stylesheet, which may be empty.

    If additional stylesheet templates exist, these will be merged into
    a single stylesheet at the end.
    '''

    @classmethod
    def from_directory(
        cls: type[typing_extensions.Self],
        directory: types.PathOrStr,
    ) -> typing_extensions.Self:
        '''
        Read the icon and stylesheet templates from a directory.

        A template directory contains the stylesheet template, icon replacement info,
        and icon templates (all are optional). A sample template directory structure is:

        ```text
        directory/
            stylesheet.qss.in
            icons.json
            branch_closed.svg.in
            branch_end_arrow.svg.in
            ...
        ```

        Our pre-built templates exist in 2 locations, relative to the project directory:
        - `/template`
        - `/extension/*` (every subdirectory in `extension`)

        Args:
            directory (`str`, `Path`): The path to the directory containing the templates.

        Returns:
            `Template`: The loaded icon and stylesheet template data.
        '''

        stylesheet = ''
        icons: list[Icon] = []
        icon_replacements: IconReplacements = {}

        directory = Path(directory)
        stylesheet_path = directory / 'stylesheet.qss.in'
        if stylesheet_path.exists():
            stylesheet = stylesheet_path.read_text(encoding='utf-8')

        icons_path = directory / 'icons.json'
        if icons_path.exists():
            icon_replacements = load_icon_replacements(icons_path)

        for file in directory.glob('*.svg.in'):
            svg = file.read_text(encoding='utf-8')
            name = file.stem.rsplit('.', maxsplit=1)[0]
            if (replacements := icon_replacements.get(name)) is None:
                keys: list[str] = re.findall(r'\^[0-9a-zA-Z_-]+\^', svg)
                replacements = [i[1:-1] for i in keys]

            icons.append(Icon(name=name, template=svg, replacements=replacements))

        return cls(icons=icons, stylesheet=stylesheet)

    def render(self, theme: 'Theme') -> None:
        '''TODO: Document and implement'''
        raise NotImplementedError('TODO')


class CommentsDecoder(json.JSONDecoder):
    '''
    A custom decoder that removes simple comments from the JSON input.

    This removes only lines starting with `//`.
    '''

    # pylint: disable-next=arguments-differ
    def decode(self, s: 'str') -> 'types.JSONValue':  # type: ignore # noqa
        '''Return the Python representation of s (a str instance containing a JSON document).'''
        lines = s.splitlines()
        lines = [i for i in lines if not i.strip().startswith('//')]
        return typing.cast('types.JSONValue', super().decode('\n'.join(lines)))


def _loads_model(s: 'str | bytes | bytearray', extension: 'str') -> types.JSONObject:
    '''Load an object from a document.'''
    value = _loads(s, extension)
    if not isinstance(value, typing.Mapping):
        raise ValueError(f'Got an invalid parsed model type of "{type(value).__name__}".')
    return typing.cast(types.JSONObject, value)


def _loads(s: 'str | bytes | bytearray', extension: 'str') -> typing.Any:
    '''Load values from a document.'''
    # NOTE: Migrate to `match` with 3.10+ support.
    if extension in ('.json', '.jsonc'):
        return _loads_json(s)
    elif extension in ('.yml', '.yaml'):
        return _loads_yaml(s)
    elif extension == '.toml':
        return _loads_toml(s)
    elif extension == '.xml':
        return _loads_xml(s)
    raise ValueError(f'Got an unknown file type of "{extension}".')


def _loads_json(s: 'str | bytes | bytearray') -> typing.Any:
    '''Load values from a JSON document.'''
    return json.loads(_decode(s), cls=CommentsDecoder)


def _loads_yaml(s: 'str | bytes | bytearray') -> typing.Any:
    '''Load values from a YAML document.'''

    # pylint: disable-next=import-error
    import yaml  # type: ignore # noqa

    return yaml.safe_load(io.StringIO(_decode(s)))


def _loads_toml(s: 'str | bytes | bytearray') -> typing.Any:
    '''Load values from a TOML document.'''

    try:
        # pylint: disable-next=import-error
        import tomllib  # type # noqa
    except ImportError:
        # pylint: disable-next=import-error
        import tomli as tomllib  # type: ignore # noqa

    return tomllib.loads(_decode(s))


def _loads_xml(s: 'str | bytes | bytearray') -> typing.Any:
    '''Load values from an XML document.'''

    # pylint: disable-next=import-error
    import xml2dict  # type: ignore # noqa

    return xml2dict.parse(_decode(s))


def _decode(s: 'str | bytes | bytearray') -> 'str':
    '''Decode the value to string as UTF-8.'''
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('utf-8')
    return s


def _transform_nested(v: 'types.JSONObject') -> 'dict[str, str]':
    '''Transform nested keys in a JSON object to `key.nested` syntax.'''

    result: dict[str, str] = {}
    for key, value in v.items():
        if not isinstance(key, str) or not isinstance(value, (str, typing.Mapping)):
            raise ValueError(f'Expected JSON value to be str or mapping, got "{type(value)}".')
        if isinstance(value, str):
            result[key] = value
        elif isinstance(value, typing.Mapping):
            nested = _transform_nested(value)
            for subkey, subvalue in nested.items():
                result[f'{key}:{subkey}'] = subvalue

    return result


@contextlib.contextmanager
def _parse_block(
    data: 'str | bytes | bytearray | None' = None,
    path: 'types.PathOrStr | None' = None,
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


def _replace_by_name(s: str, theme: 'Theme', colors: 'typing.Iterable[str] | None' = None) -> str:
    '''Replace the placeholders in the value by string.'''

    # NOTE: We expand the fields in order to have better type hinting.
    # The placeholders have a syntax like `^foreground^`.
    # To simplify the replacement process, you can specify
    # a limited subset of colors, rather than use all of them.
    if colors is None:
        colors = Theme.model_fields.keys()
    for key in colors:
        s = s.replace(f'^{key}^', theme.get_color(key, format='RGBA'))

    return s


def _replace_by_index(s: str, theme: 'Theme', colors: 'typing.Iterable[str]') -> str:
    '''Replace the placeholders in the value by string.'''

    # NOTE: We expand the fields in order to have better type hinting.
    # The placeholders have a syntax like `^0^`, where
    # the is a list of valid colors and the index of
    # the color is the replacement key.
    # This is useful since we can want multiple colors
    # for the same icon (such as hovered arrows).
    for index, key in enumerate(colors):
        s = s.replace(f'^{index}^', theme.get_color(key, format='RGBA'))

    return s
