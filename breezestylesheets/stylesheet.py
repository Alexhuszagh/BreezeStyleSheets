"""Style sheet and style sheet templates to configure templates from themes."""

from typing import TYPE_CHECKING, cast

import re
from dataclasses import dataclass

from .icon import Icon, IconTemplate
from .model import Model, model
from .style import Style

if TYPE_CHECKING:
    from typing import Self

    from pathlib import Path

    from .icon import IconReplacement, IconReplacements

__all__ = ["StyleSheet", "StyleSheetTemplate"]

TEMPLATE_FILENAME = "stylesheet.qss.in"
"""The filename for a stylesheet template."""


@model
class StyleSheetTemplate(Model):
    """
    A stylesheet template, containing the stylesheet and icon templates.

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

    icons: "list[IconTemplate]"
    """A list of icon templates, including their replacements."""

    stylesheet: "str"
    """
    A template stylesheet, which may be empty.

    If additional stylesheet templates exist, these will be merged into
    a single stylesheet at the end.
    """

    @staticmethod
    def find(directory: "Path") -> "Path | None":
        """Get the path to the template file if the directory contains stylesheet templates."""
        path = directory / TEMPLATE_FILENAME
        if path.exists():
            return path

    @classmethod
    def from_directory(cls: "type[Self]", directory: "Path") -> "Self":
        """
        Read the icon and stylesheet templates from a directory.

        A template directory contains the stylesheet template, icon replacement info,
        and icon templates (all are optional). A sample template directory structure is:

        ```text
        directory/
            stylesheet.qss.in
            icons.json
            svg/
                branch_closed.svg.in
                branch_end_arrow.svg.in
            ...
        ```

        Our builtin templates exist within the `template/` directory, relative to the
        package directory. Additional templates can be added to custom directories
        (by default, the `extension` directory relative to the project root when using
        the `configure` script). The icons file must be on of the support types (such
        as JSON, TOML, YAML, or XML).

        Args:
            directory: The path to the directory containing the templates.

        Returns:
            The loaded icon and stylesheet template data.
        """

        stylesheet = ""
        stylesheet_path = cls.find(directory)
        if stylesheet_path is not None:
            stylesheet = stylesheet_path.read_text(encoding="utf-8")

        icon_replacements: "IconReplacements" = {}
        icons_path = IconTemplate.find_replacements(directory)
        if icons_path is not None:
            icon_replacements = IconTemplate._load_replacements(icons_path)

        icons: "list[IconTemplate]" = []
        for file in directory.glob("svg/*.svg.in"):
            svg = file.read_text(encoding="utf-8")
            name = file.stem.rsplit(".", maxsplit=1)[0]
            replacements = cast("IconReplacement", icon_replacements.get(name))
            if replacements is None:
                keys: list[str] = re.findall(r"\^[0-9a-zA-Z_-]+\^", svg)
                replacements = [i[1:-1] for i in keys]

            icons.append(IconTemplate(name=name, template=svg, replacements=replacements))

        return cls(icons=icons, stylesheet=stylesheet)

    @classmethod
    def from_directories(cls: "type[Self]", *directories: "Path") -> "Self":
        """
        Read the icon and stylesheet templates from multiple directories and merge them.

        A template directory contains the stylesheet template, icon replacement info,
        and icon templates (all are optional). A sample template directory structure is:

        ```text
        directory/
            stylesheet.qss.in
            icons.json
            svg/
                branch_closed.svg.in
                branch_end_arrow.svg.in
            ...
        ```

        Our builtin templates exist within the `template/` directory, relative to the
        package directory. Additional templates can be added to custom directories
        (by default, the `extension` directory relative to the project root when using
        the `configure` script). The icons file must be on of the support types (such
        as JSON, TOML, YAML, or XML).

        Args:
            directories: The paths to the directories containing the templates.

        Returns:
            The loaded and merged icon and stylesheet template data.
        """
        templates = [cls.from_directory(i) for i in directories]
        return cls.join(*templates)

    @classmethod
    def join(cls: "type[Self]", *templates: "Self") -> "Self":
        """
        Join multiple templates into a single template.

        This merges all the relevant stylesheets and icons for each template
        into a single template.

        Args:
            templates: The templates to merge.

        Returns:
            The merged templates.
        """
        icons = [i for j in templates for i in j.icons]
        stylesheet = "\n".join([i.stylesheet for i in templates])
        return cls(icons=icons, stylesheet=stylesheet)

    def render(self, style: "Style", relative_to: "str | None" = ":/") -> "StyleSheet":
        """
        Render the stylesheet template and all icons.

        If the stylesheet is meant to meant to be compiled as a Qt [resource]
        (in a `.qrc` file), then the icons and other resources will be prefixed
        with the prefix `:/`. Otherwise, the stylesheet is assumed to be loaded
        from the local filesystem and will use relative paths.

        ```qss
        QWidget
        {
            /* Qt resource */
            dialog-cancel-icon: url(:/dark-blue/dialog_cancel.svg);
            /* Relative path */
            dialog-cancel-icon: url(dark-blue/dialog_cancel.svg);
        }
        ```

        ## Caveats

        SVG icons **must** be written to disk and do not support inline base64 data.
        For example, applying this stylesheet will not load any icons.

        ```qss
        QWidget {
            dialog-cancel-icon: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0...);
        }
        ```

        [resource]: https://doc.qt.io/qt-6/resources.html

        Args:
            style: The named theme with the colors for each configuration.
            relative_to: The path all URIs (for example, for icons) in the stylesheet
                will be relative to. If `:/`, then it is a Qt [resource].

        Returns:
            The fully rendered theme and icons with all placeholders replaced.
        """

        icons = [i for j in self.icons for i in j.render(style.theme)]

        style_name = style.name
        assert "/" not in style_name and "\\" not in style_name
        if relative_to is not None:
            style_name = f"{relative_to}{style_name}"
        if not style_name.endswith("/"):
            style_name = f"{style_name}/"

        stylesheet = style.theme._replace_by_name(self.stylesheet).replace("^style^", style_name)
        if re.search(r"\^[A-Za-z0-9]+(?:[.:-][A-Za-z0-9]+)*\^", stylesheet) is not None:
            raise ValueError("Unable to replace all placeholders: please validate the style.")

        return StyleSheet(icons, stylesheet)


@dataclass
class StyleSheet:
    """
    A fully-rendered, containing the stylesheet and icon templates.

    ```css
    QToolTip
    {
        /* 0.2ex is the smallest value that's not ignored on Windows. */
        border: 0.04em solid #eff0f1;
        background-image: none;
        background-color: #31363b;
        alternate-background-color: #31363b;
        color: #eff0f1;
        padding: 0.1em;
        opacity: 200;
    }
    ```
    """

    icons: "list[Icon]"
    """A list of icons, including their replacements."""

    value: "str"
    """
    A template stylesheet, which may be empty.

    If additional stylesheet templates exist, these will be merged into
    a single stylesheet at the end.
    """
