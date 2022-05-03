Extensions
==========

Extensions enable the creation of stylesheets using the same, customizable themes of the original stylesheet. This both allows refining the generated stylesheet and supporting third-party Qt extensions/widgets.

Extensions are optionally added to the generated stylesheets, allowing you to extend existing stylesheets to support third-party extensions and optional features.

Furthermore, this simplifies making local, application-specific changes, without having to deal with merge conflicts when fetching updates.

# Pre-Packaged Extensions

### Advanced Docking System

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

### QDockWidget Tooltips

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

### Standard Icons

This extension adds a complete set of standard icons to override the Qt defaults. Please reference [standard_icons.py](/example/standard_icons.py) for an example of how to override these icons. These cannot be overwritten solely using a stylesheet, so you must provide your own subclass of `QCommonStyle` and override the `standardIcon` method.

In order to use this extension, configure with:

```bash
python configure.py --extensions=standard-icons
```

The following is a 1:1 mapping of the standard icon enumerated name and the icon names:

```json
{
    "SP_TitleBarMinButton": "minimize.svg",
    "SP_TitleBarMenuButton": "menu.svg",
    "SP_TitleBarMaxButton": "maximize.svg",
    "SP_TitleBarCloseButton": "window_close.svg",
    "SP_TitleBarNormalButton": "restore.svg",
    "SP_TitleBarShadeButton": "shade.svg",
    "SP_TitleBarUnshadeButton": "unshade.svg",
    "SP_TitleBarContextHelpButton": "help.svg",
    "SP_MessageBoxInformation": "message_information.svg",
    "SP_MessageBoxWarning": "message_warning.svg",
    "SP_MessageBoxCritical": "message_critical.svg",
    "SP_MessageBoxQuestion": "message_question.svg",
    "SP_DesktopIcon": "desktop.svg",
    "SP_TrashIcon": "trash.svg",
    "SP_ComputerIcon": "computer.svg",
    "SP_DriveFDIcon": "floppy_drive.svg",
    "SP_DriveHDIcon": "hard_drive.svg",
    "SP_DriveCDIcon": "disc_drive.svg",
    "SP_DriveDVDIcon": "disc_drive.svg",
    "SP_DriveNetIcon": "network_drive.svg",
    "SP_DirHomeIcon": "home_directory.svg",
    "SP_DirOpenIcon": "folder_open.svg",
    "SP_DirClosedIcon": "folder.svg",
    "SP_DirIcon": "folder.svg",
    "SP_DirLinkIcon": "folder_link.svg",
    "SP_DirLinkOpenIcon": "folder_open_link.svg",
    "SP_FileIcon": "file.svg",
    "SP_FileLinkIcon": "file_link.svg",
    "SP_FileDialogStart": "file_dialog_start.svg",
    "SP_FileDialogEnd": "file_dialog_end.svg",
    "SP_FileDialogToParent": "up_arrow.svg",
    "SP_FileDialogNewFolder": "folder.svg",
    "SP_FileDialogDetailedView": "file_dialog_detailed.svg",
    "SP_FileDialogInfoView": "file_dialog_info.svg",
    "SP_FileDialogContentsView": "file_dialog_contents.svg",
    "SP_FileDialogListView": "file_dialog_list.svg",
    "SP_FileDialogBack": "left_arrow.svg",
    "SP_DockWidgetCloseButton": "close.svg",
    "SP_ToolBarHorizontalExtensionButton": "horizontal_extension.svg",
    "SP_ToolBarVerticalExtensionButton": "vertical_extension.svg",
    "SP_DialogOkButton": "dialog_ok.svg",
    "SP_DialogCancelButton": "dialog_cancel.svg",
    "SP_DialogHelpButton": "dialog_help.svg",
    "SP_DialogOpenButton": "dialog_open.svg",
    "SP_DialogSaveButton": "dialog_save.svg",
    "SP_DialogCloseButton": "dialog_close.svg",
    "SP_DialogApplyButton": "dialog_apply.svg",
    "SP_DialogResetButton": "dialog_reset.svg",
    "SP_DialogDiscardButton": "dialog_discard.svg",
    "SP_DialogYesButton": "dialog_apply.svg",
    "SP_DialogNoButton": "dialog_no.svg",
    "SP_ArrowUp": "up_arrow.svg",
    "SP_ArrowDown": "down_arrow.svg",
    "SP_ArrowLeft": "left_arrow.svg",
    "SP_ArrowRight": "right_arrow.svg",
    "SP_ArrowBack": "left_arrow.svg",
    "SP_ArrowForward": "right_arrow.svg",
    "SP_CommandLink": "right_arrow.svg",
    "SP_VistaShield": "vista_shield.svg",
    "SP_BrowserReload": "browser_refresh.svg",
    "SP_BrowserStop": "browser_refresh_stop.svg",
    "SP_MediaPlay": "play.svg",
    "SP_MediaStop": "stop.svg",
    "SP_MediaPause": "pause.svg",
    "SP_MediaSkipForward": "skip_backward.svg",
    "SP_MediaSkipBackward": "skip_forward.svg",
    "SP_MediaSeekForward": "seek_forward.svg",
    "SP_MediaSeekBackward": "seek_backward.svg",
    "SP_MediaVolume": "volume.svg",
    "SP_MediaVolumeMuted": "volume_muted.svg",
    "SP_LineEditClearButton": "clear_text.svg",
    "SP_DialogYesToAllButton": "dialog_yes_to_all.svg",
    "SP_DialogNoToAllButton": "dialog_no.svg",
    "SP_DialogSaveAllButton": "dialog_save_all.svg",
    "SP_DialogAbortButton": "dialog_cancel.svg",
    "SP_DialogRetryButton": "dialog_retry.svg",
    "SP_DialogIgnoreButton": "dialog_ignore.svg",
    "SP_RestoreDefaultsButton": "restore_defaults.svg",
    // NOTE: Only available in Qt 6.3+
    "SP_TabCloseButton": "tab_close.svg"
}
```

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
