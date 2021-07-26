BreezeStyleSheets
=================

Configurable Breeze and BreezeDark-like stylesheets for Qt Applications.

This stylesheet aims to be similar across all platforms, and provide a nice UI for different DPIs (as determined by the default font size, or using the screen scale factor). This is currently under work for scaling to multiple different DPIs and font sizes.

**Table of Contents**

- [Gallery](#gallery)
- [Customization](#customization)
- [Installing](#installing)
  - [CMake Installation](#cmake-installation)
  - [QMake Installation](#qmake-installation)
  - [PyQt5 Installation](#pyqt5-installation)
  - [PyQt6 Installation](#pyqt6-installation)
- [Features](#features)
- [Limitations](#limitations)
- [Debugging](#debugging)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

# Gallery

**Breeze/BreezeDark**

Example user interface using the Breeze and BreezeDark stylesheets side-by-side.

![BreezeDark](/assets/Breeze.gif)

For an extensive view of screenshots of the theme, see the [gallery](assets/gallery.md).

# Customization

It's easy to design your own themes using `configure.py`. First, add the styles you want into [theme](/theme/), then run configure with a list of styles you want to include.

**Theme**

Here is a sample theme, with the color descriptions annotated. Please note that although there are nearly 40 possibilities, for most applications, you should use less than 20, and ~10 different hues.

```jsonc
// NOTE: This is a custom JSON file, where lines leading
// with `//` are removed. No other comments are valid.
{
    // Main foreground color.
    "foreground": "#eff0f1",
    // Lighter foreground color for selected items.
    "foreground-light": "#ffffff",
    // Main background color.
    "background": "#31363b",
    // Alternate background color for styles.
    "background:alternate": "#31363b",
    // Main color to highlight widgets, such as on hover events.
    "highlight": "#3daee9",
    // Color for selected widgets so hover events can change widget color.
    "highlight:dark": "#2a79a3",
    // Alternate highlight color for hovered widgets in QAbstractItemViews.
    "highlight:alternate": "#369cd1",
    // Main midtone color, such as for borders.
    "midtone": "#76797c",
    // Lighter color for midtones, such as for certain disabled widgets.
    "midtone:light": "#b0b0b0",
    // Darker midtone, such as for the background of QPushButton and QSlider.
    "midtone:dark": "#626568",
    // Lighter midtone for separator hover events.
    "midtone:hover": "#8a8d8f",
    // Color for checked widgets in QAbstractItemViews.
    "view:checked": "#334e5e",
    // Hover background color in QAbstractItemViews.
    // This should be fairly transparent.
    "view:hover": "rgba(61, 173, 232, 0.1)",
    // Background for a horizontal QToolBar.
    "toolbar:horizontal:background": "#31363b",
    // Background for a vertical QToolBar.
    "toolbar:vertical:background": "#31363b",
    // Background color for the corner widget in a QAbstractItemView.
    "view:corner": "#31363b",
    // Border color between items in a QHeaderView.
    "view:header:border": "#76797c",
    // Background color for a QHeaderView.
    "view:header": "#31363b",
    // Border color Between items in a QAbstractItemView.
    "view:border": "#31363b",
    // Background for QAbstractItemViews.
    "view:background": "#1d2023",
    // Background for widgets with text input.
    "text:background": "#1d2023",
    // Background for the currently selected tab.
    "tab:background:selected": "#31363b",
    // Background for non-selected tabs.
    "tab:background": "#2c3034",
    // Color for the branch/arrow icons in a QTreeView.
    "tree": "#afafaf",
    // Color for the chunk of a QProgressBar, the active groove
    // of a QSlider, and the border of a hovered QSlider handle.
    "slider:foreground": "#3daee9",
    // Background color for the handle of a QSlider.
    "slider:handle:background": "#1d2023",
    // Color for a disabled menubar/menu item.
    "menu:disabled": "#76797c",
    // Color for a checked/hovered QCheckBox or QRadioButton.
    "checkbox:light": "#58d3ff",
    // Color for a disabled or unchecked/unhovered QCheckBox or QRadioButton.
    "checkbox:disabled": "#c8c9ca",
    // Color for the handle of a scrollbar. Due to limitations of 
    // Qt stylesheets, any handle of a scrollbar must be treated
    // like it's hovered.
    "scrollbar:hover": "#3daee9",
    // Background for a non-hovered scrollbar.
    "scrollbar:background": "#1d2023",
    // Background for a hovered scrollbar.
    "scrollbar:background:hover": "#76797c",
    // Default background for a QPushButton.
    "button:background": "#31363b",
    // Background for a pressed QPushButton.
    "button:background:pressed": "#454a4f",
    // Border for a non-hovered QPushButton.
    "button:border": "#76797c",
    // Background for a disabled QPushButton, or fallthrough
    // for disabled QWidgets.
    "button:disabled": "#454545",
    // Color of a dock/tab close icon when hovered.
    "close:hover": "#b37979",
    // Color of a dock/tab close icon when pressed.
    "close:pressed": "#b33e3e",
    // Default background color for QDockWidget and title.
    "dock:background": "#31363b",
    // Color for the float icon for QDockWidgets.
    "dock:float": "#a2a2a2",
    // Background color for the QMessageBox critical icon.
    "critical": "#80404a",
    // Background color for the QMessageBox information icon.
    "information": "#406880",
    // Background color for the QMessageBox question icon.
    "question": "#634d80",
    // Background color for the QMessageBox warning icon.
    "warning": "#99995C"
}
```

Once you've saved your custom theme, you can then build the stylesheet, icons, and resource file with:

```bash
python configure.py --styles=dark,light,<custom> --resource custom.qrc
```

Then, you can use `custom.qrc`, along with the generated icons and stylesheets in each folder, in place of `breeze.qrc` for any style.

The `--styles` command flag takes a comma-separated list of values, or `all`, which will configure every theme present in the [themes](/theme) directory.

**Generating Colors**

As a reference point, see the pre-generated [themes](/theme). In general, to create a good theme, modify only the highlight colors (blues, greens, purples) to a new color, such that the saturation and lightness stay the same (only the hue changes). For example, the color `rgba(51, 164, 223, 0.5)` becomes `rgba(164, 51, 223, 0.5)`.

**Extensions**

We also allow customizable extensions to extend the default stylesheets with additional style rules, using the colors defined in your theme. This also enables the integration of third-party Qt plugins/widgets into the generated stylesheets.

For example, to configure with extensions for the [Advanced Docking System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System), run:

```bash
python configure.py --extensions=advanced-docking-system --resource custom.qrc
```

Like with styles, `--extensions` takes a comma-separated list of values, or `all`, which will add every extension present in the [extensions](/extension) directory. For a detailed introduction to creating your own extensions, see the extensions [tutorial](/extension/README.md).

# Installing

Here are detailed instructions on how to install Breeze Style Sheets for a variety of build systems and programming languages.

## Configuring

By default, BreezeStyleSheets comes with the `dark` and `light` themes pre-built. In order to build all pre-packaged themes, run:


```bash
python configure.py --styles=all --extensions=all --resource breeze.qrc
```

All generated themes will be in the [dist](/dist) subdirectory.

## CMake Installation

Using CMake, you can download, configure, and compile the resources as part part of the build process. The following configurations are provided by @ruilvo. First, save the following as `BreezeThemes.cmake`

```cmake
# Setup Qt: this works with both Qt5 and Qt6
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(
  QT NAMES Qt6 Qt5
  COMPONENTS Core
  REQUIRED)
find_package(
  Qt${QT_VERSION_MAJOR}
  COMPONENTS ${AE_REQUIRED_QT_COMPONENTS}
  REQUIRED)
# -------------------

# Get Python to compile the stylesheets.
# Fetch the repository, configure, compile the stylesheets.
find_package(Python COMPONENTS Interpreter)

include(FetchContent)

set(FETCHCONTENT_QUIET
    OFF
    CACHE BOOL "Silence fetch content" FORCE)

FetchContent_Declare(
  breeze_stylesheets
  GIT_REPOSITORY https://github.com/Alexhuszagh/BreezeStyleSheets.git
  GIT_TAG origin/master
  GIT_PROGRESS ON
  USES_TERMINAL_DOWNLOAD TRUE)

FetchContent_GetProperties(breeze_stylesheets)
if(NOT breeze_stylesheets_POPULATED)
  FetchContent_Populate(breeze_stylesheets)

  add_library(breeze_themes STATIC "${breeze_stylesheets_SOURCE_DIR}/dist/breeze_themes.qrc")

  add_custom_target(
    run_python_breeze ALL
    COMMAND ${Python_EXECUTABLE} configure.py --extensions=<EXTENSIONS>
            --styles=<STYLES> --resource breeze_themes.qrc
    WORKING_DIRECTORY ${breeze_stylesheets_SOURCE_DIR}
    BYPRODUCTS "${breeze_stylesheets_SOURCE_DIR}/dist/breeze_themes.qrc"
    COMMENT "Generating themes")

  add_dependencies(breeze_themes run_python_breeze)
endif()
```

Next, make sure the path to `breeze_themes.cmake` is in your module search [path](https://cgold.readthedocs.io/en/latest/tutorials/cmake-sources/includes.html), and add the following to your CMakeLists.txt:

```cmake
include(BreezeThemes)

add_executable(myapp WIN32 MACOSX_BUNDLE "main.cpp")
target_link_libraries(myapp PRIVATE Qt${QT_VERSION_MAJOR}::Widgets breeze_themes)
```

And then in your application start point, add the following:

```cpp
int main()
{
    // ...
    QApplication app(argc, argv);

    // Need to initialize the resource, since we're using an external
    // build system and this isn't automatically handled by CMake.
    Q_INIT_RESOURCE(breeze_themes);
    QFile file(":/dark-green/stylesheet.qss");
    file.open(QFile::ReadOnly | QFile::Text);
    QTextStream stream(&file);
    app.setStyleSheet(stream.readAll());

    // ...
}
```

## QMake Installation

Copy the contents of the `dist` subdirectory into your project directory and add the qrc file to your project file.

For example:

```qmake
TARGET = app
SOURCES = main.cpp
RESOURCES = breeze.qrc
```

To load the stylesheet in C++, load the file using QFile and read the data. For example, to load BreezeDark, run:

```cpp

#include <QApplication>
#include <QFile>
#include <QTextStream>


int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // set stylesheet
    QFile file(":/dark/stylesheet.qss");
    file.open(QFile::ReadOnly | QFile::Text);
    QTextStream stream(&file);
    app.setStyleSheet(stream.readAll());

    // code goes here

    return app.exec();
}
```

## PyQt5 Installation

To compile the stylesheet for use with PyQt5, compile with the following command `pyrcc5 dist/breeze.qrc -o breeze_resources.py`. `breeze_resources.py` now contains all the stylesheet data. To load and set the stylesheet in a PyQt5 application, import `breeze_resources`, load the file using QFile and read the data. For example, to load BreezeDark, run:


```python

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
import breeze_resources


def main():
    app = QtWidgets.QApplication(sys.argv)

    # set stylesheet
    file = QFile(":/dark/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    # code goes here

    app.exec_()
```

## PyQt6 Installation

Since [pyrcc](https://www.riverbankcomputing.com/pipermail/pyqt/2020-September/043209.html) is no longer being maintained, using local Python paths is the preferable solution. For a detailed description on how to package these resources, see this StackOverflow [answer](https://stackoverflow.com/a/20885799/4131059).

First, package your code using setuptools. Make sure `zip_safe` is off, so we can properly load the files from a search path, and include the necessary package directories to your `MANIFEST.in` file.

```python
from setuptools import setup

setup(
    # Either option is valid here.
    #   Either use `package_data` with enumerating the values, or
    #   set `include_package_data=True`.
    include_package_data=True,
    package_data={
        'breeze_theme': ['dist/*'],
    },
    zip_safe=False,
)
```

Then, you can import the resources as follows:

```python
import importlib.resources
from Qt6 import QtWidgets, QtCore
from Qt6.QtCore import QFile, QTextStream


def main():
    app = QtWidgets.QApplication(sys.argv)

    # set stylesheet
    # Note that the search path name must be the theme name.
    #   dark => dark, light => light, dark-purple => dark-purple, ...
    breeze_theme = importlib_resources.files('breeze_theme.dark')
    QtCore.QDir.addSearchPath('dark', breeze_theme)
    file = QFile("dark:stylesheet.qss")
    file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    # code goes here

    app.exec()
```

# Features

- Complete stylesheet for all Qt widgets, including esoteric widgets like `QCalendarWidget`.
- Customizable, beautiful light and dark themes.
- Cross-platform icon packs for standard icons.
- Extensible stylesheets: add your own plugins or rules and automatically configure them using the same configuration syntax.

# Limitations

There are some limitations of using Qt stylesheets in general, which cannot be solved by stylesheets. To get more fine-grained style control, you should subclass `QCommonStyle`:

```c++
class ApplicationStyle: public QCommonStyle
{
    ...
}
```

An extensive reference can be found [here](https://doc.qt.io/qt-5/style-reference.html). A reference of QStyle, and the default styles Qt provides can be found [here](https://doc.qt.io/qt-5/qstyle.html).

The limitations of stylesheets include:

- Scaling icons with the theme size.
- QToolButton cannot control the icon size without also affecting the arrow size.
- Close and dock float icon sizes scale poorly with font size.

# Debugging

Have an issue with the styles? Here's a few suggestions, prior to filing a bug report:

- Modified the application font? Make sure you do **before** setting the application stylesheet.
- Modified the application style? Make sure you do **before** you creating a `QApplication instance`.

# License

MIT, see [license](/LICENSE.md).

# Contributing

To configure the assets and the stylesheets, run `configure.py`. To compile the assets and stylesheets for Python, run `pyrcc5 breeze.qrc -o breeze_resources.py`.

In order to test your changes, first run the tests using the appropriate widget in `test.py` (see the options for `stylesheet`, `widget`, `font-size`, and `font-family`), and then run the tests with the complete UI in `example.py`. If the widget you fixed the style for does not exist in `example.py`, please add it.

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in BreezeStyleSheets by you shall be licensed under the MIT license without any additional terms or conditions.

# Acknowledgements

BreezeStyleSheets is a fork of [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet). Some of the icons are modified from [Material UI](https://github.com/google/material-design-icons) (which uses an Apache 2.0 license), and are redistributed under the MIT license.

# Contact

Email: ahuszagh@gmail.com  
Twitter: KardOnIce
