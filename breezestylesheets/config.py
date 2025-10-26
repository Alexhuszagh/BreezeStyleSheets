"""
config

Models and helpers to load the Stylesheet configuration options.
"""

import typing
import os.path
import re
from collections import abc as typing_abc
from dataclasses import field
from pathlib import Path

from . import constants, color, types
from .pydantic.color import Color, NullableColor
from .model import Model, field_metadata, loads_model, model, parse_block

if typing.TYPE_CHECKING:
    import typing_extensions as typing_ext

# NOTE: Using unions directly, rather than the `|` syntax, is needed for 3.9 support,
# with pydantic, which must resolve these hints to define the models.

__all__ = ['Theme', 'Template']
# NOTE: Union is required for 3.9 support in our base models.
ColorType: 'typing.TypeAlias' = typing.Union[Color, typing.Literal[""]]


@model
class Theme(Model):
    """
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
    """

    foreground: 'Color' = field(metadata=field_metadata('foreground', required=True))
    """The main foreground color."""

    foreground_light: 'NullableColor' = field(metadata=field_metadata('foreground:light'))
    """Lighter foreground color for selected items."""

    background: 'Color' = field(metadata=field_metadata('background'))
    """The main background color."""

    background_alternate: 'NullableColor' = field(metadata=field_metadata('background:alternate'))
    """Alternate background color for styles."""

    highlight: 'Color' = field(metadata=field_metadata('highlight'))
    """Main color to highlight widgets, such as on hover events."""

    highlight_dark: 'NullableColor' = field(metadata=field_metadata('highlight:dark'))
    """Color for selected widgets so hover events can change widget color."""

    highlight_alternate: 'NullableColor' = field(metadata=field_metadata('highlight:alternate'))
    """Alternate highlight color for hovered widgets in QAbstractItemViews."""

    midtone: 'Color' = field(metadata=field_metadata('midtone'))
    """Main midtone color, such as for borders."""

    midtone_light: 'NullableColor' = field(metadata=field_metadata('midtone:light'))
    """Lighter color for midtones, such as for certain disabled widgets."""

    midtone_dark: 'NullableColor' = field(metadata=field_metadata('midtone:dark'))
    """Darker midtone, such as for the background of QPushButton and QSlider."""

    midtone_hover: 'NullableColor' = field(metadata=field_metadata('midtone:hover'))
    """Lighter midtone for separator hover events."""

    view_checked: 'Color' = field(metadata=field_metadata('view:checked'))
    """Color for checked widgets in QAbstractItemViews."""

    view_hover: 'NullableColor' = field(metadata=field_metadata('view:hover'))
    """Hover background color in QAbstractItemViews."""

    view_corner: 'NullableColor' = field(metadata=field_metadata('view:corner'))
    """Background color for the corner widget in a QAbstractItemView."""

    view_header_border: 'NullableColor' = field(metadata=field_metadata('view:header:border'))
    """Border color between items in a QHeaderView."""

    view_header: 'NullableColor' = field(metadata=field_metadata('view:header'))
    """Background color for a QHeaderView."""

    view_border: 'NullableColor' = field(metadata=field_metadata('view:border'))
    """Border color Between items in a QAbstractItemView."""

    view_background: 'NullableColor' = field(metadata=field_metadata('view:background'))
    """Background for QAbstractItemViews."""

    toolbar_horizontal_background: 'NullableColor' = field(
        metadata=field_metadata('toolbar:horizontal:background'),
    )
    """Background for a horizontal QToolBar."""

    toolbar_vertical_background: 'NullableColor' = field(
        metadata=field_metadata('toolbar:vertical:background'),
    )
    """Background for a vertical QToolBar."""

    text_background: 'NullableColor' = field(metadata=field_metadata('text:background'))
    """Background for widgets with text input."""

    tab_background_selected: 'NullableColor' = field(metadata=field_metadata('tab:background:selected'))
    """Background for the currently selected tab."""

    tab_background: 'NullableColor' = field(metadata=field_metadata('tab:background'))
    """Background for non-selected tabs."""

    tree: 'Color' = field(metadata=field_metadata('tree'))
    """Color for the branch/arrow icons in a QTreeView."""

    slider_foreground: 'NullableColor' = field(metadata=field_metadata('slider:foreground'))
    """
    Color for the chunk of a QProgressBar, the active groove of a QSlider,
    and the border of a hovered QSlider handle.
    """

    slider_handle_background: 'NullableColor' = field(metadata=field_metadata('slider:handle:background'))
    """Background color for the handle of a QSlider."""

    menu_disabled_impl: 'NullableColor' = field(metadata=field_metadata('menu:disabled'))
    """Internal helper for `menu_disabled`. Do not use directly."""

    @property
    def menu_disabled(self) -> 'Color':
        """Color for a disabled menubar/menu item."""
        if not self.menu_disabled_impl.is_empty:
            self.menu_disabled_impl = constants.DISABLED[self.is_dark]
        return self.menu_disabled_impl

    @menu_disabled.setter
    def menu_disabled(self, value: 'NullableColor') -> None:
        self.menu_disabled_impl = value

    checkbox_light: 'NullableColor' = field(metadata=field_metadata('checkbox:light'))
    """Color for a checked/hovered QCheckBox or QRadioButton."""

    checkbox_disabled_impl: 'NullableColor' = field(metadata=field_metadata('checkbox:disabled'))
    """Internal helper for `checkbox_disabled`. Do not use directly."""

    @property
    def checkbox_disabled(self) -> 'Color':
        """Color for a disabled or unchecked/unhovered QCheckBox or QRadioButton."""
        if not self.checkbox_disabled_impl.is_empty:
            self.checkbox_disabled_impl = constants.DISABLED[self.is_dark]
        return self.checkbox_disabled_impl

    @checkbox_disabled.setter
    def checkbox_disabled(self, value: 'NullableColor') -> None:
        self.checkbox_disabled_impl = value

    scrollbar_hover: 'NullableColor' = field(metadata=field_metadata('scrollbar:hover'))
    """
    Color for the handle of a scrollbar. Due to limitations of Qt stylesheets, any
    handle of a scrollbar must be treated like it's hovered.
    """

    scrollbar_background: 'NullableColor' = field(metadata=field_metadata('scrollbar:background'))
    """Background for a non-hovered scrollbar."""

    scrollbar_background_hover: 'NullableColor' = field(
        metadata=field_metadata('scrollbar:background:hover'),
    )
    """Background for a hovered scrollbar."""

    button_background: 'NullableColor' = field(metadata=field_metadata('button:background'))
    """Default background for a QPushButton."""

    button_background_pressed: 'NullableColor' = field(
        metadata=field_metadata('button:background:pressed')
    )
    """Background for a pressed QPushButton."""

    button_border: 'NullableColor' = field(metadata=field_metadata('button:border'))
    """Border for a non-hovered QPushButton."""

    button_checked: 'NullableColor' = field(metadata=field_metadata('button:checked'))
    """Background for a checked QPushButton."""

    button_disabled_impl: 'NullableColor' = field(metadata=field_metadata('button:disabled'))
    """Internal helper for `button_disabled`. Do not use directly."""

    @property
    def button_disabled(self) -> 'Color':
        """Background for a disabled QPushButton, or fallthrough for disabled QWidgets."""
        if not self.button_disabled_impl.is_empty:
            self.button_disabled_impl = constants.DISABLED[self.is_dark]
        return self.button_disabled_impl

    @button_disabled.setter
    def button_disabled(self, value: 'NullableColor') -> None:
        self.button_disabled_impl = value

    close_hover: 'NullableColor' = field(metadata=field_metadata('close:hover'))
    """Color of a dock/tab close icon when hovered."""

    close_pressed: 'NullableColor' = field(metadata=field_metadata('close:pressed'))
    """Color of a dock/tab close icon when pressed."""

    dock_background: 'NullableColor' = field(metadata=field_metadata('dock:background'))
    """Default background color for QDockWidget and title."""

    dock_float: 'NullableColor' = field(metadata=field_metadata('dock:float'))
    """Color for the float icon for QDockWidgets."""

    critical_impl: 'NullableColor' = field(metadata=field_metadata('critical'))
    """Internal helper for `critical`. Do not use directly."""

    @property
    def critical(self) -> 'Color':
        """Background color for the QMessageBox critical icon."""
        if not self.critical_impl.is_empty:
            self.critical_impl = constants.CRITICAL[self.is_dark]
        return self.critical_impl

    @critical.setter
    def critical(self, value: 'NullableColor') -> None:
        self.critical_impl = value

    information_impl: 'NullableColor' = field(metadata=field_metadata('information'))
    """Internal helper for `information`. Do not use directly."""

    @property
    def information(self) -> 'Color':
        """Background color for the QMessageBox information icon."""
        if not self.information_impl.is_empty:
            self.information_impl = constants.INFORMATION[self.is_dark]
        return self.information_impl

    @information.setter
    def information(self, value: 'NullableColor') -> None:
        self.information_impl = value

    question_impl: 'NullableColor' = field(metadata=field_metadata('question'))
    """Internal helper for `question`. Do not use directly."""

    @property
    def question(self) -> 'Color':
        """Background color for the QMessageBox question icon."""
        if not self.question_impl.is_empty:
            self.question_impl = constants.QUESTION[self.is_dark]
        return self.question_impl

    @question.setter
    def question(self, value: 'NullableColor') -> None:
        self.question_impl = value

    warning_impl: 'NullableColor' = field(metadata=field_metadata('warning'))
    """Internal helper for `warning`. Do not use directly."""

    @property
    def warning(self) -> 'Color':
        """Background color for the QMessageBox warning icon."""
        if not self.warning_impl:
            self.warning_impl = constants.WARNING[self.is_dark]
        return self.warning_impl

    @warning.setter
    def warning(self, value: 'NullableColor') -> None:
        self.warning_impl = value

    ads_tab_focused: 'NullableColor' = field(metadata=field_metadata('ads-tab:focused'))
    """The background color for an Advanced Docking System Tab."""

    ads_border_focused: 'NullableColor' = field(metadata=field_metadata('ads-border:focused'))
    """The background color for an Advanced Docking System border."""

    @property
    def is_light(self) -> 'bool':
        """Get if the color scheme is a light theme."""
        return color.is_light(self.background)

    @property
    def is_dark(self) -> 'bool':
        """Get if the color scheme is a dark theme."""
        return not self.is_light

    @typing.overload
    def get_color(self, alias: str, format: None = None) -> 'str | Color': ...

    @typing.overload
    def get_color(self, alias: str, format: 'color.Format') -> 'str': ...

    def get_color(self, alias: str, format: 'color.Format | None' = None) -> 'str | Color':
        """
        Get a single color by the alias.

        Args:
            alias (`str`): The name of the alias or field to get, such as `foreground`.

        Returns:
            `Color`: The color to use as the replacement.

            `str`: The hex, alpha opacity, or RGBA representation of the color.

            `""`: A value signifying no color, without a transparent replacement.

        Raises:
            `ValueError`: If the provided alias is not valid or the field is not a color.
        """

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
        """
        Render the stylesheet with all placeholders replaced.

        Args:
            template (`str`): The template stylesheet, as a single QSS document.
            style (`str`): The prefix for the style as a QT resource.

        Returns:
            `str`: The fully rendered stylesheet with all placeholders replaced.
        """
        if not style.startswith(':/'):
            style = f':/{style}'
        if not style.endswith('/'):
            style = f'{style}/'
        result = _replace_by_name(template, self).replace('^style^', style)
        if re.search(r'\^[A-Za-z0-9]+(?:[.:-][A-Za-z0-9]+)*\^', result) is not None:
            msg = 'Did not replace all value placeholders: ensure the theme is properly configured.'
            raise ValueError(msg)

        return result


IconListReplacement: 'typing.TypeAlias' = 'typing_abc.Sequence[str]'
"""
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
"""

IconDictReplacement: 'typing.TypeAlias' = typing_abc.Mapping[str, IconListReplacement]
"""
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
"""

IconReplacement: 'typing.TypeAlias' = typing.Union[IconDictReplacement, IconListReplacement]
"""
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
"""


class StandardIconReplacements(typing.TypedDict, total=False):
    """
    The Qt standard icons that can be used for simple icon styling.

    The fields all correspond to the following Qt enumerated icon names,
    defined under [QStyle](https://doc.qt.io/qt-6/qstyle.html):
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
    """

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
    typing_abc.Mapping[str, IconReplacement], StandardIconReplacements
]
"""
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
"""


def load_icon_replacements(path: types.PathOrStr) -> IconReplacements:
    """
    Load the icon replacements from a file.

    This supports JSON, YAML, TOML, and XML file formats.

    Args:
        path (`str`, `Path`): The path to the file to load.

    Returns:
        `IconReplacements`: The loaded icon replacements.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the data.
    """
    with parse_block(path=path):
        with open(path, encoding='utf-8') as file:
            return _loads_icon_replacements(file.read(), os.path.splitext(os.path.basename(path))[1])


def loads_icon_replacements(s: 'str | bytes | bytearray', extension: 'str') -> IconReplacements:
    """
    Load the icon replacements from a document.

    This supports JSON, YAML, TOML, and XML file formats.

    Args:
        s (`str`, `bytes`, `bytearray`): The document data, as a string or UTF-8 encoded bytes.
            extension (str): The extension of the file (to determine the file type).

    Returns:
        `IconReplacements`: The loaded icon replacements.

    Raises:
        `ConfigParseError`: Any errors that occur during parsing the data.
    """
    with parse_block(data=s):
        return _loads_icon_replacements(s, extension)


def _loads_icon_replacements(s: 'str | bytes | bytearray', extension: 'str') -> IconReplacements:
    """Load and validate the loaded icons."""

    def is_mapping_str(value: typing_abc.Mapping):
        return all([isinstance(i, str) for i in value.keys()])

    def is_sequence_str(value: typing.Any):
        return isinstance(value, typing_abc.Sequence) and all([isinstance(i, str) for i in value])

    def throw_invalid(data: typing.Any) -> typing.NoReturn:
        raise ValueError(f'Expected a mapping icon names to replacements, got "{data}".')

    # NOTE: We accept Mapping/Sequence, but `loads` with always return `dict` or `list`.
    loaded = loads_model(s, extension)
    if not isinstance(loaded, typing_abc.Mapping) or not is_mapping_str(loaded):
        throw_invalid(loaded)
    for value in loaded.values():
        # Mapping[str, Sequence[str]] | Sequence[str]
        if isinstance(value, typing_abc.Mapping):
            if not is_mapping_str(value) or not all([is_sequence_str(i) for i in value.values()]):
                throw_invalid(loaded)
        elif not is_sequence_str(value):
            throw_invalid(loaded)

    return typing.cast(IconReplacements, loaded)


@model
class Icon(Model):
    """
    The configurations for how to replace the colors within an icon.

    This contains an icon template, the name of the icon used to
    determine icon resource path, and the color replacements for
    the template.
    """

    name: str
    """
    The name of the icon.

    This corresponds to the icon written to disk, with the `.svg` suffix, and
    optionally, with an extension suffix as defined in the replacements.
    """

    template: str
    """The raw, template SVG data of the icon."""

    replacements: IconReplacement
    """
    The template replacements for the icon, optionally with additional extensions defined.

    The replacements **MUST** be defined here, since
    """

    def render(self, theme: 'Theme') -> typing_abc.Mapping[str, str]:
        """
        Render the SVG icon with all placeholders replaced.

        The placeholders have a syntax like `^foreground^` (for name-based placeholders),
        or, in some cases, index-based ones like `^0^` which is the index in a list of
        valid color replacements.

        Args:
            theme (`Theme`): The theme with the colors for each configuration.

        Returns:
            `dict`: The template SVG rendered with all placeholders replaced,
            as a mapping of the icon name and the rendered SVG.
        """

        def with_ext(name: str, ext: str) -> str:
            if ext == 'default':
                return name
            return f'{name}_{ext}'

        result = {}
        if isinstance(self.replacements, typing_abc.Mapping):
            for extension, replacements in self.replacements.items():
                name = with_ext(self.name, extension)
                value = _replace_by_index(self.template, theme, replacements)
                result[name] = value
        else:
            result[self.name] = _replace_by_name(self.template, theme, self.replacements)

        return result


@model
class Template(Model):
    """
    A theme template, containing the stylesheet and icon templates.

    This contains the data for how to render a single template,
    which may include additional extensions.

    The template defines placeholders, such as `^foreground^`,
    which are then replaced by the values specified in the `Theme`.

    ```css
    QToolTip
    {
        /* 0.2ex is the smallest value that's not ignored on Windows. */
        border: 0.04em solid ^foreground^;
        background-image: none;
        background-color: ^background^;
        alternate-background-color: ^background:alternate^;
        color: ^foreground^;
        padding: 0.1em;
        opacity: 200;
    }
    ```

    Similarly, icons will define index-based (`^0^`) or name-based
    placeholders `^foreground^` like above.
    """

    icons: list[Icon]
    """A list of icon templates, including their replacements."""

    stylesheet: str
    """
    A template stylesheet, which may be empty.

    If additional stylesheet templates exist, these will be merged into
    a single stylesheet at the end.
    """

    @classmethod
    def from_directory(
        cls: type['typing_ext.Self'],
        directory: types.PathOrStr,
    ) -> 'typing_ext.Self':
        """
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
        """

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

    @classmethod
    def from_directories(
        cls: type['typing_ext.Self'],
        *directories: types.PathOrStr,
    ) -> 'typing_ext.Self':
        """
        Read the icon and stylesheet templates from multiple directories and merge them.

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
            directories (`str`, `Path`): The paths to the directories containing the templates.

        Returns:
            `Template`: The loaded and merged icon and stylesheet template data.
        """
        templates = [cls.from_directory(i) for i in directories]
        return cls.join(*templates)

    @classmethod
    def join(
        cls: type['typing_ext.Self'],
        *templates: 'typing_ext.Self',
    ) -> 'typing_ext.Self':
        """
        Join multiple templates into a single template.

        This merges all the relevant stylesheets and icons for each template
        into a single template.

        Args:
            templates (`Template`): The templates to merge.

        Returns:
            `Template`: The merged templates.
        """
        icons = [i for j in templates for i in j.icons]
        stylesheet = '\n'.join([i.stylesheet for i in templates])
        return cls(icons=icons, stylesheet=stylesheet)

    def render(self, theme: 'Theme') -> None:
        """TODO: Document and implement"""
        raise NotImplementedError('TODO')


def _replace_by_name(s: str, theme: 'Theme', colors: 'typing.Iterable[str] | None' = None) -> str:
    """Replace the placeholders in the value by string."""

    # NOTE: We expand the fields in order to have better type hinting.
    # The placeholders have a syntax like `^foreground^`.
    # To simplify the replacement process, you can specify
    # a limited subset of colors, rather than use all of them.
    if colors is None:
        colors = Theme.keys
    for key in colors:
        # TODO: This is wrong, we don't have the fields correctly mapped
        s = s.replace(f'^{key}^', theme.get_color(key, format='RGBA'))

    return s


def _replace_by_index(s: str, theme: 'Theme', colors: 'typing.Iterable[str]') -> str:
    """Replace the placeholders in the value by string."""

    # NOTE: We expand the fields in order to have better type hinting.
    # The placeholders have a syntax like `^0^`, where
    # the is a list of valid colors and the index of
    # the color is the replacement key.
    # This is useful since we can want multiple colors
    # for the same icon (such as hovered arrows).
    for index, key in enumerate(colors):
        s = s.replace(f'^{index}^', theme.get_color(key, format='RGBA'))

    return s
