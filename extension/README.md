Extensions
==========

Extensions enable the creation of stylesheets using the same, customizable themes of the original stylesheet. This both allows refining the generated stylesheet and supporting third-party Qt plugins/widgets.

Extensions are optionally added to the generated stylesheets, allowing you to extend existing stylesheets to support third-party plugins and optional features.

Furthermore, this simplifies making local, application-specific changes, without having to deal with merge conflicts when fetching updates.

# Pre-Packaged Extensions

**Advanced Docking System**

This extension adds support for the [Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System). This comes with styles for the dock manager to create a consistent theme between the main stylesheet and the docking system.

In order to use this extension, configure with:

```bash
python configure.py --extensions=advanced-docking-system
```

And make sure to [disable](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System/blob/master/doc/user-guide.md#disabling-the-internal-style-sheet) the internal stylesheet in the dock manager.

<figure>
    <img 
        alt="Advanced Docking System View 1"
        src="/assets/advanced_docking_system1.png" 
        title="AdvancedDockingSystem1" 
    />
</figure>

<figure>
    <img 
        alt="Advanced Docking System View 2"
        src="/assets/advanced_docking_system2.png" 
        title="AdvancedDockingSystem2" 
    />
</figure>

<figure>
    <img 
        alt="Advanced Docking System View 3"
        src="/assets/advanced_docking_system3.png" 
        title="AdvancedDockingSystem3" 
    />
</figure>

<figure>
    <img 
        alt="Advanced Docking System View 4"
        src="/assets/advanced_docking_system4.png" 
        title="AdvancedDockingSystem4" 
    />
</figure>

**QDockWidget Tooltips**

This extension adds tooltips to QDockWidget's float and close buttons.

In order to use this extension, configure with:

```bash
python configure.py --extensions=dock-tooltips
```

<figure>
    <img 
        alt="Dock Tooltips"
        src="/assets/dock_tooltips.png" 
        title="DockTooltips" 
    />
</figure>

# Creating Extensions

Creating extensions extends the existing stylesheet configurations, and adds custom rules to the stylesheet, which can then be configured for all themes. This supports custom icons, rules, and more.

Each extension is added as a folder in [extension](/extension), with a template stylesheet file named `stylesheet.qss.in`. Additional icons can be added as SVG template files (with the extension `svg.in`), and icon styling rules in `icons.json`.

**Simple Example**

For example, to add tooltips to a `QDockWidget`, create a `stylesheet.qss.in`  in the directory `extension/tooltips` with the following contents:

```css
QAbstractButton#qt_dockwidget_closebutton
{
    qproperty-toolTip: "Close";
}

QAbstractButton#qt_dockwidget_floatbutton
{
    qproperty-toolTip: "Detach";
}
```

To build the stylesheet with the extension, run:

```bash
python configure.py --extensions=tooltips
```

**Icons Example**

For a more complex example, let's consider a third-party extension of a `QPushButton` with the object name `customButton`, which has a configurable icon. First, create a directory named `extension/custom-button`.

Next, let's create an SVG template for the icon, at `icon.svg.in`:

```svg
<svg width="405" height="290">
  <g transform="scale(5)">
    <rect fill="^0^" x="36" width="3" height="17"/>
    <rect fill="^0^" x="66" y="29.75" height="2" width="15"/>
  </g>
</svg>
```

Here, `^0^` signifies index-based replacement, so we must define an entry in 
`icons.json` to specify how we should do the replacement.

```json
{
    "icon": {
        "default": ["foreground"],
        "hover": ["highlight"]
    }
}
```

Index-based replacement allows us to create more than 1 icon from a single template, with different colors. Here, this would create `icon.svg` with the theme's foreground color, and `icon_hover.svg` with the theme's highlight color.

Next, we want to add the rules to use these icons in the stylesheet:

```css
QPushButton#customButton
{
    qproperty-icon: url(:/dark/icon.svg);
}

QPushButton#customButton:hover
{
    qproperty-icon: url(:/dark/icon_hover.svg);
}
```

To build the stylesheet with the extension, run:

```bash
python configure.py --extensions=custom-button
```
