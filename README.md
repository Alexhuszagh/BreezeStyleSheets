BreezeStyleSheets
=================

Breeze and BreezeDark-like stylesheets for Qt Applications.

This stylesheet aims to be similar across all platforms, and provide a nice UI for different DPIs (as determined by the default font size, or using the screen scale factor). This is currently under work for scaling to multiple different DPIs and font sizes.

The current status of the migration is:

- Change all `ex` widths to `em` ☐
- Ensure individual tests for all widgets ☐
- Port all the changes made to the dark stylesheet to light ☐

# C++ Installation

Copy `breeze.qrc`, `dark.qss`, `light.qss` and the `dark` and `light` folders into your project directory and add the qrc file to your project file.

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
    QFile file(":/dark.qss");
    file.open(QFile::ReadOnly | QFile::Text);
    QTextStream stream(&file);
    app.setStyleSheet(stream.readAll());

    // code goes here

    return app.exec();
}
```

# PyQt5 Installation

To compile the stylesheet for use with PyQt5, compile with the following command `pyrcc5 breeze.qrc -o breeze_resources.py`, and import the stylesheets. Afterwards, to load the stylesheet in Python, load the file using QFile and read the data. For example, to load BreezeDark, run:


```python

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
import breeze_resources


def main():
    app = QtWidgets.QApplication(sys.argv)

    # set stylesheet
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    # code goes here

    app.exec_()
```

# License

MIT, see [license](/LICENSE.md).

# Example

**Breeze/BreezeDark**

Example user interface using the Breeze and BreezeDark stylesheets side-by-side.

![BreezeDark](/assets/Breeze.gif)

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

- Non-border item underlying, such as seen in Breeze. The box model will not affect the placement of the underline, not even with style on the element itself, the `::title` subcontrol, or any other attempts.
- Scaling icons with the theme size.
- QToolButton cannot have center-aligned text.
- The branch indicators on QTreeViews don't scale.

# Debugging

Have an issue with the styles? Here's a few suggestions, prior to filing a bug report:

- Modified the application font? Make sure you do **before** setting the application stylesheet.
- Modified the application style? Make sure you do **before** you creating a `QApplication instance`.

# Contributing

To configure the assets and the stylesheets, run `configure.py`. To compile the assets and stylesheets for Python, run `pyrcc5 breeze.qrc -o breeze_resources.py`.

In order to test your changes, first run the tests using the appropriate widget in `single.py` (see the options for `stylesheet`, `widget`, `font-size`, and `font-family`), and then run the tests with the complete UI in `example.py`. If the widget you fixed the style for does not exist in `example.py`, please add it.

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in BreezeStyleSheets by you shall be licensed under the MIT license without any additional terms or conditions.

# Acknowledgements

BreezeStyleSheets is a fork of [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet).

# Contact

Email: ahuszagh@gmail.com  
Twitter: KardOnIce

