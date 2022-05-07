Issues
======

There are limitations to what can be styled with stylesheets, as well as rare bugs that prevent certain styles or widgets from rendering properly. This is a list of known issues, as well as suitable workarounds. THese issues are organized by the widget type, then the description of the properties/styles they affect.

- [QCompleter](#qcompleter)
  - [Menu Hover Background Color](#menu-hover-background-color)
- [QDial](#qdial)
  - [Custom Style](#custom-style)
- [QLCDNumber](#qlcdnumber)
  - [LCD Color](#lcd-color)
- [QMdiSubwindow](#qmdisubwindow)
  - [Title Bar Icons](#title-bar-icons)
- [QSlider](#qslider)
  - [Invisible Ticks](#invisible-ticks)
- [QTabBar](#qtabbar)
  - [Triangular Tab Color](#triangular-tab-color)
  - [Triangular Tab Hover Background Color](#triangular-tab-hover-background-color)
  - [Triangular Tab Padding](#triangular-tab-padding)
- [QTextDocument](#qtextdocument)
  - [Placeholder Text](#placeholder-text)
  - [Links](#links)
- [QToolButton](#qtoolbutton)
  - [Menu Button Padding](#menu-button-padding)
- [QWhatsThis](#qwhatsthis)
  - [Tooltip Colors](#tooltip-colors)
- [QWidget](#qwidget)
  - [Standard Icons](#standard-icons)
- [QWindow](#qwindow)
  - [Title Bar Customization](#title-bar-customization)
- [QWizard](#qwizard)
  - [Aero Style Background Color](#aero-style-background-color)

# QCompleter

### Menu Hover Background Color

`QCompleter` doesn't have a hover background color in Qt5 on the drop-down menu. This works fine in Qt6, and changing rules for `QListView` (the drop-down menu) changes the drop-down menu in Qt6, but not Qt5.

# QDial

### Custom Style

`QDial` cannot be customized via a stylesheet, which is a known bug in [QTBUG-1160](https://bugreports.qt.io/browse/QTBUG-1160). An example of how to style a `QDial` is available in [dial.py](/example/dial.py). This works out-of-the-box, and can be a drop-in replacement for `QDial`.

<img src="/assets/custom_dial.png" alt="Custom Dial" width="500" height="192"/>

# QLCDNumber

### LCD Color

The LCD display of a `QLCDNumber` cannot be customized via a stylesheet. An example of how to style a `QLCDNumber` is available in [lcd.py](/example/lcd.py). This works out-of-the-box, and can be a drop-in replacement for `QLCDNumber`.

<img src="/assets/custom_lcd.png" alt="Custom Dial" width="500" height="132"/>

# QMdiSubwindow

### Title Bar Icons

The tilebar icons (except for the menu icon) cannot be overridden in the stylesheet, which is a known bug in [QTBUG-1399](https://bugreports.qt.io/browse/QTBUG-1399). This bug has been present for ~15 years, so it is unlikely to be patched soon, if ever. For a working example on how to customize your own title bar, including icons, see [Title Bar Customization for QWindow](#title-bar-customization).

# QSlider

### Invisible Ticks

`QSlider` ticks disappear when using stylesheets, which is a known bug referenced in [QTBUG-3304](https://bugreports.qt.io/browse/QTBUG-3304) and [QTBUG-3564](https://bugreports.qt.io/browse/QTBUG-3564). An example of how to style a `QSlider` is available in [slider.py](/example/slider.py), however, this does not work with a stylesheet applied to a `QSlider`.

# QTabBar

### Triangular Tab Color

The text and border colors of a triangular `QTabBar` must be the same. This cannot be modified via a stylesheet.

### Triangular Tab Hover Background Color

Triangular tab bars do not have `:hover` pseudo-states for non-selected tabs. Only the selected tab has a `:hover` pseudo-state, defeating the purpose. This could be fixed by installing an event filter for a `HoverEnter` or `HoverMove` event.

### Triangular Tab Padding

Custom padding for triangular QTabBars on the bottom is ignored. All other tab positions work.

# QTextDocument

### Placeholder Text 

For the widgets `QTextEdit`, `QPlainTextEdit`, and `QLineEdit`, which use an internal `QTextDocument`, you can set placeholder text for when no text is present. In Qt5, this is correctly grayed out when the placeholder text is present, which is not respected in Qt6 (as of Qt version 6.3.0).

An example of a workaround [placeholder_text.py](/example/placeholder_text.py), which only works currently for Qt5 or Qt6 without a stylesheet. Using the native stylesheet shows it uses hard-coded colors for Qt6, so this is almost certainly a Qt bug. This is likely referenced in [QTBUG-92947](https://bugreports.qt.io/browse/QTBUG-92947) and [QTCREATORBUG-25444](https://bugreports.qt.io/browse/QTCREATORBUG-25444).

An example workaround setting the placeholder text at palette at the application level (for all widgets) is as follows. You can also set the placeholder text color for each individual widget.

**C++**

```cpp
#include <QApplication>
#include <QColor>
#include <QPalette>

int main(int argc, char* argv[]) 
{
    QApplication app(argc, argv);

    auto palette = app.palette();
    QColor red(255, 0, 0);
    palette.setColor(QPalette::PlaceholderText, red);
    app.setPalette(palette);

    ...

    return app.exec();
}
```

**Python**

```python
import sys
from PyQt6 import QtGui, QtWidgets

ColorRole = QtGui.QPalette.ColorRole

def main():
    app = QtWidgets.QApplication(sys.argv)

    palette = app.palette()
    red = QtGui.QColor(255, 0, 0)
    palette.setColor(ColorRole.PlaceholderText, red)
    app.setPalette(palette)

    ...

    return app.exec()
```

### Links

There is no way to set the default color of a link in a `QLabel`, `QTextEdit`, `QPlainTextEdit`, `QTextBrowser`,  `QMessageBox`, etc. There are a few possible workarounds.

One is to set the link color when setting the label text, here, setting the label text to red. This will override the default color, and you can use a theme-dependent color to ensure the links are rendered properly.

```python
label = QtWidgets.QLabel()
# Ensure it's displayed as a URL
label.setTextFormat(QtCore.Qt.TextFormat.RichText)
label.setText('<a href="https://google.com" style="color: red;">Google</a>')
```

However, this won't work with markdown input, and requires you to modify any existing text to include the styles, which is undesirable. A better solution is to set a default palette for `ColorRole.Link`.

**C++**

```cpp
#include <QApplication>
#include <QColor>
#include <QPalette>

int main(int argc, char* argv[]) 
{
    QApplication app(argc, argv);

    auto palette = app.palette();
    QColor red(255, 0, 0);
    palette.setColor(QPalette::Active, QPalette::Link, red);
    app.setPalette(palette);

    ...

    return app.exec();
}
```

**Python**

```python
import sys
from PyQt6 import QtGui, QtWidgets

ColorGroup = QtGui.QPalette.ColorGroup
ColorRole = QtGui.QPalette.ColorRole

def main():
    app = QtWidgets.QApplication(sys.argv)

    palette = app.palette()
    red = QtGui.QColor(255, 0, 0)
    palette.setColor(ColorGroup.Active, ColorRole.Link, red)
    app.setPalette(palette)

    ...

    return app.exec()
```

# QToolButton

### Menu Button Padding

`QToolButton` may have extra padding or clip the menu indicator in some cases. Auto-raised QToolButtons will clip the menu indicator, as will QToolButtons without text. Other cases will always add padding, whether there is a menu indicator or not. In order to force padding or no-padding for the menu indicator, set the Qt property of `hasMenu` to `true` or `false`. For example, to force additional padding for a menu indicator, use `button->setProperty("hasMenu", true);`.

A simple example of creating a `QToolButton` with text and with no menu drop-down is as follows:

**C++**

```cpp
#include <QApplication>
#include <QString>
#include <QToolButton>

int main(int argc, char* argv[]) 
{
    QApplication app(argc, argv);

    ... // Get our window, central widget, layout, etc.

    auto *button = new QToolButton(widget);
    button->setText(QString("Button 1"));
    button->setProperty(QString("hasMenu"), false);

    ... // Add button to layout, show window, etc.

    return app.exec();
}
```

**Python**

```python
import sys
from PyQt6 import QtGui, QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)

    ... # Get our window, central widget, layout, etc.

    button = QtWidgets.QToolButton(widget)
    button.setText('Button 1')
    button.setProperty('hasMenu', False)

    ... # Add button to layout, show window, etc.

    return app.exec()
```

### QCommandLink Icon

The default icon for `QCommandLinkButton` is platform-dependent, and depends on the standard icon `SP_CommandLink` (which cannot be specified in a stylesheet). See [Standard Icons](#standard-icons) for an explanation on how to override this standard icon.

# QWhatsThis

### Tooltip Colors

QWhatsThis uses `QPalette::toolTipText` and `QPalette::toolTipBase` for its colors: unfortunately, these are not influenced by the stylesheet. To modify these, you can change the colors for `QPalette::ToolTipBase` and `QPalette::ToolTipText`. An example can be found in [whatsthis.py](/example/whatsthis.py).

A simple example of modifying the tooltip palette for the `QWhatsThis` style is as follows:

**C++**

```cpp
#include <QApplication>
#include <QColor>
#include <QPalette>

int main(int argc, char* argv[])
{
    QApplication app(argc, argv);

    auto palette = app.palette();
    QColor green(0, 255, 0);
    QColor blue(0, 0, 255);
    palette.setColor(QPalette::ToolTipBase, green);
    palette.setColor(QPalette::ToolTipText, blue);
    app.setPalette(palette);

    ...

    return app.exec();
}
```

**Python**

```python
import sys
from PyQt6 import QtGui, QtWidgets

ColorRole = QtGui.QPalette.ColorRole

def main():
    app = QtWidgets.QApplication(sys.argv)

    palette = app.palette()
    green = QtGui.QColor(0, 255, 0)
    blue = QtGui.QColor(0, 0, 255)
    palette.setColor(ColorRole.ToolTipBase, green)
    palette.setColor(ColorRole.ToolTipText, blue)
    app.setPalette(palette)

    ...

    return app.exec()
```

![Custom Whats This](/assets/custom_whatsthis.png)

# QWidget

### Standard Icons

Certain standard icons cannot be overridden in the stylesheet, and therefore a custom style must be installed in the Qt application. The `standard-icons` [extension](/extension/README.md#standard-icons) comes with a set of custom standard icons, and the [standard_icons.py](/example/standard_icons.py) example shows a complete application for how to override the default standard icons.

A simple example of overriding the command link icon for a PyQt6 application is as follows. First, configure with the `standard-icons` extension.

```bash
python configure.py --extensions=standard-icons
```

Next, set the application stylesheet, subclass `QCommonStyle` to get custom standard icons, and install the style globally in the Qt application.

```python
from PyQt6 import QtCore, QtGui, QtWidgets

StandardPixmap = QtWidgets.QStyle.StandardPixmap
OpenModeFlag = QtCore.QFile.OpenModeFlag

# Create a map of registered icons, so we can efficiently query if we
# should override the icon or use the pre-packaged standard icons.
ICON_MAP = {
    ...
    StandardPixmap.SP_CommandLink: 'right_arrow.svg',
    ...
}

def stylesheet_icon(style, icon, option=None, widget=None):
    '''Get a standard icon for the stylesheet style'''

    # See if we've registered a custom icon in the stylesheet
    path = ICON_MAP.get(icon, None)
    if path is not None:
        resource = f'dark:{path}'
        if QtCore.QFile.exists(resource):
            return QtGui.QIcon(resource)

    # No custom icon: return the default for the style.
    return QtWidgets.QCommonStyle.standardIcon(style, icon, option, widget)


class ApplicationStyle(QtWidgets.QCommonStyle):
    def __init__(self, style):
        super().__init__()
        # Store an instance for the default style, so we can query that.
        # Avoids an infinite, recursive loop.
        self.style = style

    def __getattribute__(self, item):
        '''
        Override for standardIcon. Everything else should default to the
        system default. We cannot have `style_icon` be a member of
        `ApplicationStyle`, since this will cause an infinite recursive loop.
        '''

        if item == 'standardIcon':
            return lambda *x: stylesheet_icon(self, *x)
        return getattr(self.style, item)

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Install our custom style globally. QCommonStyle, unlike QProxyStyle,
    # actually works nicely with stylesheets. `Fusion` is available
    # on all platforms, but you can use any style you want. We
    # just need a created style, because `app.style()` will be 
    # deleted by he garbage collector.
    style = QtWidgets.QStyleFactory.create('Fusion')
    app.setStyle(ApplicationStyle(style))

    # Set our stylesheet. 
    # NOTE: this must occur after setting the application style.
    file = QtCore.QFile('dark:stylesheet.qss')
    file.open(OpenModeFlag.ReadOnly | OpenModeFlag.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())

    ...

    return app.exec()
```

<img src="/assets/custom_standard_icons.png" alt="Custom Standard Icons" width="500" height="438"/>

# QWindow

### Title Bar Customization

The system title bar cannot be customized extensively, since it depends on either the application style or the system theme for how it renders. For a comprehensive example on how to create your own, custom title bar, with fully functional minimize, maximize, shade, unshade, context help, keep above, window title, and a context menu, see [titlebar.py](/example/titlebar.py). This is a drop-in replacement for the title bar on `QMdiSubWindow` which also lets you customize the placement of where the windows minimize to, but could also be modified for `QMainWindow` or `QDialog`.

<img src="/assets/custom_titlebar.png" alt="Custom Title Bar" width="500" height="399"/>

# QWizard

### Aero Style Background Color

The background color at the top and bottom of a `QWizard` using `QWizard::AeroStyle` uses hard-coded colors for the values above and below the page. These cannot be modified, even with `QPalette`, and the solution is quite simple: use any other style other than `QWizard::AeroStyle`. Other available options include `QWizard::ModernStyle` and `QWizard::MacStyle`.

![QWizard Aero Windows](/assets/wizard_aero_windows.png)
