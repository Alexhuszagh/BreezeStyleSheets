"""The theme settings for how to style the Qt Stylesheet."""

from typing import TYPE_CHECKING, overload

from dataclasses import field

from . import color, constants
from .model import EXTENSIONS, Model, field_metadata, model
from .pydantic.color import Color, NullableColor

if TYPE_CHECKING:
    from collections.abc import Iterable

    from pathlib import Path

__all__ = ["Theme"]


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

    foreground: "Color" = field(
        metadata=field_metadata("foreground", required=True),
    )
    """The main foreground color."""

    foreground_light: "NullableColor" = field(
        metadata=field_metadata("foreground:light"),
    )
    """Lighter foreground color for selected items."""

    background: "Color" = field(
        metadata=field_metadata("background"),
    )
    """The main background color."""

    background_alternate: "NullableColor" = field(
        metadata=field_metadata("background:alternate"),
    )
    """Alternate background color for styles."""

    highlight: "Color" = field(
        metadata=field_metadata("highlight"),
    )
    """Main color to highlight widgets, such as on hover events."""

    highlight_dark: "NullableColor" = field(
        metadata=field_metadata("highlight:dark"),
    )
    """Color for selected widgets so hover events can change widget color."""

    highlight_alternate: "NullableColor" = field(
        metadata=field_metadata("highlight:alternate"),
    )
    """Alternate highlight color for hovered widgets in QAbstractItemViews."""

    midtone: "Color" = field(
        metadata=field_metadata("midtone"),
    )
    """Main midtone color, such as for borders."""

    midtone_light: "NullableColor" = field(
        metadata=field_metadata("midtone:light"),
    )
    """Lighter color for midtones, such as for certain disabled widgets."""

    midtone_dark: "NullableColor" = field(
        metadata=field_metadata("midtone:dark"),
    )
    """Darker midtone, such as for the background of QPushButton and QSlider."""

    midtone_hover: "NullableColor" = field(
        metadata=field_metadata("midtone:hover"),
    )
    """Lighter midtone for separator hover events."""

    view_checked: "Color" = field(
        metadata=field_metadata("view:checked"),
    )
    """Color for checked widgets in QAbstractItemViews."""

    view_hover: "NullableColor" = field(
        metadata=field_metadata("view:hover"),
    )
    """Hover background color in QAbstractItemViews."""

    view_corner: "NullableColor" = field(
        metadata=field_metadata("view:corner"),
    )
    """Background color for the corner widget in a QAbstractItemView."""

    view_header_border: "NullableColor" = field(
        metadata=field_metadata("view:header:border"),
    )
    """Border color between items in a QHeaderView."""

    view_header: "NullableColor" = field(
        metadata=field_metadata("view:header"),
    )
    """Background color for a QHeaderView."""

    view_border: "NullableColor" = field(
        metadata=field_metadata("view:border"),
    )
    """Border color Between items in a QAbstractItemView."""

    view_background: "NullableColor" = field(
        metadata=field_metadata("view:background"),
    )
    """Background for QAbstractItemViews."""

    toolbar_horizontal_background: "NullableColor" = field(
        metadata=field_metadata("toolbar:horizontal:background"),
    )
    """Background for a horizontal QToolBar."""

    toolbar_vertical_background: "NullableColor" = field(
        metadata=field_metadata("toolbar:vertical:background"),
    )
    """Background for a vertical QToolBar."""

    text_background: "NullableColor" = field(
        metadata=field_metadata("text:background"),
    )
    """Background for widgets with text input."""

    tab_background_selected: "NullableColor" = field(
        metadata=field_metadata("tab:background:selected"),
    )
    """Background for the currently selected tab."""

    tab_background: "NullableColor" = field(
        metadata=field_metadata("tab:background"),
    )
    """Background for non-selected tabs."""

    tree: "Color" = field(
        metadata=field_metadata("tree"),
    )
    """Color for the branch/arrow icons in a QTreeView."""

    slider_foreground: "NullableColor" = field(
        metadata=field_metadata("slider:foreground"),
    )
    """
    Color for the chunk of a QProgressBar, the active groove of a QSlider,
    and the border of a hovered QSlider handle.
    """

    slider_handle_background: "NullableColor" = field(
        metadata=field_metadata("slider:handle:background"),
    )
    """Background color for the handle of a QSlider."""

    menu_disabled_impl: "NullableColor" = field(
        metadata=field_metadata("menu:disabled"),
    )
    """Internal helper for `menu_disabled`. Do not use directly."""

    @property
    def menu_disabled(self) -> "Color":
        """Color for a disabled menubar/menu item."""
        if not self.menu_disabled_impl.is_empty:
            self.menu_disabled_impl = constants.DISABLED[self.is_dark]
        return self.menu_disabled_impl

    @menu_disabled.setter
    def menu_disabled(self, value: "NullableColor") -> "None":
        self.menu_disabled_impl = value

    checkbox_light: "NullableColor" = field(
        metadata=field_metadata("checkbox:light"),
    )
    """Color for a checked/hovered QCheckBox or QRadioButton."""

    checkbox_disabled_impl: "NullableColor" = field(
        metadata=field_metadata("checkbox:disabled"),
    )
    """Internal helper for `checkbox_disabled`. Do not use directly."""

    @property
    def checkbox_disabled(self) -> "Color":
        """Color for a disabled or unchecked/unhovered QCheckBox or QRadioButton."""
        if not self.checkbox_disabled_impl.is_empty:
            self.checkbox_disabled_impl = constants.DISABLED[self.is_dark]
        return self.checkbox_disabled_impl

    @checkbox_disabled.setter
    def checkbox_disabled(self, value: "NullableColor") -> "None":
        self.checkbox_disabled_impl = value

    scrollbar_hover: "NullableColor" = field(
        metadata=field_metadata("scrollbar:hover"),
    )
    """
    Color for the handle of a scrollbar. Due to limitations of Qt stylesheets, any
    handle of a scrollbar must be treated like it's hovered.
    """

    scrollbar_background: "NullableColor" = field(
        metadata=field_metadata("scrollbar:background"),
    )
    """Background for a non-hovered scrollbar."""

    scrollbar_background_hover: "NullableColor" = field(
        metadata=field_metadata("scrollbar:background:hover"),
    )
    """Background for a hovered scrollbar."""

    button_background: "NullableColor" = field(
        metadata=field_metadata("button:background"),
    )
    """Default background for a QPushButton."""

    button_background_pressed: "NullableColor" = field(
        metadata=field_metadata("button:background:pressed"),
    )
    """Background for a pressed QPushButton."""

    button_border: "NullableColor" = field(
        metadata=field_metadata("button:border"),
    )
    """Border for a non-hovered QPushButton."""

    button_checked: "NullableColor" = field(
        metadata=field_metadata("button:checked"),
    )
    """Background for a checked QPushButton."""

    button_disabled_impl: "NullableColor" = field(
        metadata=field_metadata("button:disabled"),
    )
    """Internal helper for `button_disabled`. Do not use directly."""

    @property
    def button_disabled(self) -> "Color":
        """Background for a disabled QPushButton, or fallthrough for disabled QWidgets."""
        if not self.button_disabled_impl.is_empty:
            self.button_disabled_impl = constants.DISABLED[self.is_dark]
        return self.button_disabled_impl

    @button_disabled.setter
    def button_disabled(self, value: "NullableColor") -> "None":
        self.button_disabled_impl = value

    close_hover: "NullableColor" = field(
        metadata=field_metadata("close:hover"),
    )
    """Color of a dock/tab close icon when hovered."""

    close_pressed: "NullableColor" = field(
        metadata=field_metadata("close:pressed"),
    )
    """Color of a dock/tab close icon when pressed."""

    dock_background: "NullableColor" = field(
        metadata=field_metadata("dock:background"),
    )
    """Default background color for QDockWidget and title."""

    dock_float: "NullableColor" = field(
        metadata=field_metadata("dock:float"),
    )
    """Color for the float icon for QDockWidgets."""

    critical_impl: "NullableColor" = field(
        metadata=field_metadata("critical"),
    )
    """Internal helper for `critical`. Do not use directly."""

    @property
    def critical(self) -> "Color":
        """Background color for the QMessageBox critical icon."""
        if not self.critical_impl.is_empty:
            self.critical_impl = constants.CRITICAL[self.is_dark]
        return self.critical_impl

    @critical.setter
    def critical(self, value: "NullableColor") -> "None":
        self.critical_impl = value

    information_impl: "NullableColor" = field(
        metadata=field_metadata("information"),
    )
    """Internal helper for `information`. Do not use directly."""

    @property
    def information(self) -> "Color":
        """Background color for the QMessageBox information icon."""
        if not self.information_impl.is_empty:
            self.information_impl = constants.INFORMATION[self.is_dark]
        return self.information_impl

    @information.setter
    def information(self, value: "NullableColor") -> "None":
        self.information_impl = value

    question_impl: "NullableColor" = field(
        metadata=field_metadata("question"),
    )
    """Internal helper for `question`. Do not use directly."""

    @property
    def question(self) -> "Color":
        """Background color for the QMessageBox question icon."""
        if not self.question_impl.is_empty:
            self.question_impl = constants.QUESTION[self.is_dark]
        return self.question_impl

    @question.setter
    def question(self, value: "NullableColor") -> "None":
        self.question_impl = value

    warning_impl: "NullableColor" = field(
        metadata=field_metadata("warning"),
    )
    """Internal helper for `warning`. Do not use directly."""

    @property
    def warning(self) -> "Color":
        """Background color for the QMessageBox warning icon."""
        if not self.warning_impl:
            self.warning_impl = constants.WARNING[self.is_dark]
        return self.warning_impl

    @warning.setter
    def warning(self, value: "NullableColor") -> "None":
        self.warning_impl = value

    ads_tab_focused: "NullableColor" = field(
        metadata=field_metadata("ads-tab:focused"),
    )
    """The background color for an Advanced Docking System Tab."""

    ads_border_focused: "NullableColor" = field(
        metadata=field_metadata("ads-border:focused"),
    )
    """The background color for an Advanced Docking System border."""

    @property
    def is_light(self) -> "bool":
        """Get if the color scheme is a light theme."""
        return color.is_light(self.background)

    @property
    def is_dark(self) -> "bool":
        """Get if the color scheme is a dark theme."""
        return not self.is_light

    @staticmethod
    def find_by_name(directory: "Path", name: "str") -> "Path | None":
        """
        Get the path to the theme file by name if found.

        If multiple themes with the same name exist, it will return a the first file
        found in an unspecified order.
        """
        icons = directory.glob(f"{name}.*")
        files = (directory / i for i in icons if i.suffix in EXTENSIONS)
        return next(files, None)

    @overload
    def get_color(self, field: "str", format: None = None) -> "str | Color": ...

    @overload
    def get_color(self, field: "str", format: "color.Format") -> "str": ...

    def get_color(self, field: "str", format: "color.Format | None" = None) -> "str | Color":
        """
        Get a single color by the field name.

        Args:
            field: The name of the field to get, such as `foreground:light`.

        Returns:
            `Color`: The color to use as the replacement.

            `str`: The hex, alpha opacity, or RGBA representation of the color.

            `""`: A value signifying no color, without a transparent replacement.

        Raises:
            `ValueError`: If the provided field name is not valid or the field is not a color.
        """

        # ensure we have our color data, for the value
        is_hex = field.endswith(":hex")
        is_opacity = not is_hex and field.endswith(":opacity")
        if is_hex:
            field = field[: -len(":hex")]
        elif is_opacity:
            field = field[: -len(":opacity")]

        # get and process our value
        value = self.get(field)
        if value != "" and not isinstance(value, Color):
            raise ValueError(f'Got an unexpected color value of "{value}" for field "{field}".')
        if value == "" and (is_hex or is_opacity):
            raise ValueError(f'Missing required color for field "{field}" with hex/opacity variant.')
        if isinstance(value, str):
            return value

        # process our hex and opacity variants
        if is_hex:
            rgb = [f"{i:02x}" for i in color.to_rgba(value)[:3]]
            return f"#{''.join(rgb)}"
        if is_opacity:
            return str(color.to_rgba(value)[3])
        if format == "RGBA":
            return value.as_rgb()
        if format == "HSLA":
            return value.as_hsl()
        if format == "hex":
            return value.as_hex(format="long")
        return value

    def _replace_by_name(self, s: "str", colors: "Iterable[str] | None" = None) -> "str":
        """Replace the placeholders in the value by string."""

        # NOTE: We expand the fields in order to have better type hinting.
        # The placeholders have a syntax like `^foreground^`.
        # To simplify the replacement process, you can specify
        # a limited subset of colors, rather than use all of them.
        if colors is None:
            colors = Theme.keys
        for key in colors:
            s = s.replace(f"^{key}^", self.get_color(key, format="RGBA"))

        return s

    def _replace_by_index(self, s: "str", colors: "Iterable[str]") -> "str":
        """Replace the placeholders in the value by string."""

        # NOTE: We expand the fields in order to have better type hinting.
        # The placeholders have a syntax like `^0^`, where
        # the is a list of valid colors and the index of
        # the color is the replacement key.
        # This is useful since we can want multiple colors
        # for the same icon (such as hovered arrows).
        for index, key in enumerate(colors):
            s = s.replace(f"^{index}^", self.get_color(key, format="RGBA"))

        return s
