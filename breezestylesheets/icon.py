"""Icons and icon templates to include in the stylesheet resources."""

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, cast

from dataclasses import dataclass
from pathlib import Path

from .model import EXTENSIONS, Model, loads_model, model, parse_block
from .theme import Theme

if TYPE_CHECKING:
    from typing import Any, Literal, NoReturn, TypeAlias, TypedDict  # type: ignore

    from .pydantic.color import Color
    from .types import Loads

    ColorType: TypeAlias = "Color | Literal['']"
    """The valid color types."""

    IconListReplacement: TypeAlias = "Sequence[str]"
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

    IconDictReplacement: TypeAlias = "Mapping[str, IconListReplacement]"
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

    IconReplacement: TypeAlias = "IconDictReplacement | IconListReplacement"
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

    IconReplacements: TypeAlias = "Mapping[str, IconReplacement] | StandardIconReplacements"
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

    class StandardIconReplacements(TypedDict, total=False):
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

        browser_refresh: "IconReplacement"
        browser_refresh_stop: "IconReplacement"
        dialog_apply: "IconReplacement"
        dialog_ignore: "IconReplacement"
        dialog_retry: "IconReplacement"
        dialog_save_all: "IconReplacement"
        dialog_yes_to_all: "IconReplacement"
        folder_open_link: "IconReplacement"
        horizontal_extension: "IconReplacement"
        pause: "IconReplacement"
        play: "IconReplacement"
        restore_defaults: "IconReplacement"
        seek_backward: "IconReplacement"
        seek_forward: "IconReplacement"
        skip_backward: "IconReplacement"
        skip_forward: "IconReplacement"
        stop: "IconReplacement"
        tab_close: "IconReplacement"
        vertical_extension: "IconReplacement"
        vista_shield: "IconReplacement"
        volume: "IconReplacement"
        volume_muted: "IconReplacement"


REPLACEMENT_FILENAMES = [f"icon{i}" for i in EXTENSIONS]
"""The filenames for a icon replacements supported for the current extensions."""


@model
class IconTemplate(Model):
    """
    The configurations for how to replace the colors within an icon.

    This contains an icon template, the name of the icon used to
    determine icon resource path, and the color replacements for
    the template.
    """

    name: "str"
    """
    The name of the icon.

    This corresponds to the icon written to disk, with the `.svg` suffix, and
    optionally, with an extension suffix as defined in the replacements.
    """

    template: "str"
    """The raw, template SVG data of the icon."""

    replacements: "IconReplacement"
    """
    The template replacements for the icon, optionally with additional extensions defined.

    These are the replacements for the specific icon, and can be provided as a sequence
    (the color replacements for the icon placeholders, using the `^0^` syntax), or a
    map (the variants mapped to the icon placeholders).

    The mapping syntax defines 3 variants of the icon: the default (`ads_menu_button.svg`)
    icon, the icon on hover events (`ads_menu_button_hover.svg`), and the icon when pressed
    (`ads_menu_button_pressed.svg`).

    ```json
    {
        "default": ["dock:float:hex", "dock:float:opacity"],
        "hover": ["close:hover:hex", "close:hover:opacity"],
        "pressed": ["highlight:dark:hex", "highlight:dark:opacity"]
    }
    ```

    The sequence syntax only supports the default (`ads_menu_button.svg`) icon.

    ```json
    ["dock:float:hex", "dock:float:opacity"]
    ```
    """

    @staticmethod
    def find_replacements(directory: "Path") -> "Path | None":
        """
        Get the path to the icon replacements file if the directory contains icon replacements.

        If multiple valid icon replacement files exist, it will return a the first file
        found in an unspecified order.
        """
        files = (directory / i for i in directory.glob("icons.*") if i.suffix in EXTENSIONS)
        return next(files, None)

    def render(self, theme: "Theme") -> "list[Icon]":
        """
        Render the SVG icon with all placeholders replaced.

        The placeholders have a syntax like `^foreground^` (for name-based placeholders),
        or, in some cases, index-based ones like `^0^` which is the index in a list of
        valid color replacements.

        Args:
            theme: The theme with the colors for each configuration.

        Returns:
            The template SVG rendered with all placeholders replaced.
        """

        def with_ext(name: "str", ext: "str") -> "str":
            if ext == "default":
                return name
            return f"{name}_{ext}"

        result: "list[Icon]" = []
        if isinstance(self.replacements, Mapping):
            for extension, replacements in self.replacements.items():
                name = with_ext(self.name, extension)
                value = theme._replace_by_index(self.template, replacements)
                result.append(Icon(name, value))
        else:
            value = theme._replace_by_name(self.template, self.replacements)
            result.append(Icon(self.name, value))

        return result

    @staticmethod
    def _load_replacements(path: "Path") -> "IconReplacements":
        """
        Load the icon replacements from a file.

        This supports JSON, YAML, TOML, and XML file formats. A sample replacements
        document is a mapping of icon file names (without the `.svg.in` suffix) to
        their replacements:

        ```json
        {
            "ads_menu_button": {
                "default": ["dock:float:hex", "dock:float:opacity"],
                "hover": ["close:hover:hex", "close:hover:opacity"],
                "pressed": ["highlight:dark:hex", "highlight:dark:opacity"]
            },
            "ads_detach_hover": {
                "default": ["close:hover:hex", "close:hover:opacity"],
                "pressed": ["highlight:dark:hex", "highlight:dark:opacity"]
            }
        }
        ```

        Args:
            path: The path to the file to load.

        Returns:
            The loaded icon replacements.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the data.
        """
        with parse_block(path=path):
            with path.open(encoding="utf-8") as file:
                return _loads_icon_replacements(file.read(), path.suffix)

    @staticmethod
    def _loads_replacements(s: "Loads", extension: "str") -> "IconReplacements":
        """
        Load all icon replacements from a document.

        This supports JSON, YAML, TOML, and XML file formats. A sample replacements
        document is a mapping of icon file names (without the `.svg.in` suffix) to
        their replacements:

        ```json
        {
            "ads_menu_button": {
                "default": ["dock:float:hex", "dock:float:opacity"],
                "hover": ["close:hover:hex", "close:hover:opacity"],
                "pressed": ["highlight:dark:hex", "highlight:dark:opacity"]
            },
            "ads_detach_hover": {
                "default": ["close:hover:hex", "close:hover:opacity"],
                "pressed": ["highlight:dark:hex", "highlight:dark:opacity"]
            }
        }

        Args:
            s: The document data, as a string or UTF-8 encoded bytes.
            extension: The extension of the file (to determine the file type).

        Returns:
            The loaded icon replacements.

        Raises:
            `ConfigParseError`: Any errors that occur during parsing the data.
        """
        with parse_block(data=s):
            return _loads_icon_replacements(s, extension)


@dataclass
class Icon:
    """
    A fully rendered SVG icon.

    This contains the name of the icon used to determine icon resource path
    as well as the raw value (string) of the rendered SVG.
    """

    name: "str"
    """
    The name of the icon.

    This corresponds to the icon written to disk, with the `.svg` suffix, and
    optionally, with an extension suffix as defined in the replacements.
    """

    value: "str"
    """The fully rendered SVG."""


def _loads_icon_replacements(s: "Loads", extension: "str") -> "IconReplacements":
    """Load and validate the loaded icons."""

    def is_mapping_str(value: "Mapping"):
        return all(isinstance(i, str) for i in value.keys())

    def is_sequence_str(value: "Any"):
        return isinstance(value, Sequence) and all([isinstance(i, str) for i in value])

    def throw_invalid(data: "Any") -> "NoReturn":
        raise ValueError(f'Expected a mapping icon names to replacements, got "{data}".')

    # NOTE: We accept Mapping/Sequence, but `loads` with always return `dict` or `list`.
    loaded = loads_model(s, extension)
    if not isinstance(loaded, Mapping) or not is_mapping_str(loaded):
        throw_invalid(loaded)
    for value in loaded.values():
        # Mapping[str, Sequence[str]] | Sequence[str]
        if isinstance(value, Mapping):
            if not is_mapping_str(value) or not all(is_sequence_str(i) for i in value.values()):
                throw_invalid(loaded)
        elif not is_sequence_str(value):
            throw_invalid(loaded)

    return cast("IconReplacements", loaded)
