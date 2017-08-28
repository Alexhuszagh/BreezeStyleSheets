BreezeStyleSheets
=================

Breeze and BreezeDark-like stylesheets for Qt Applications.

Installation
============

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

License
=======

MIT, see [license](/LICENSE.md).

Example
=======

**Breeze/BreezeDark**

Example user interface using the Breeze and BreezeDark stylesheets side-by-side.

![BreezeDark](/assets/Breeze.gif)

Acknowledgements
================

BreezeStyleSheets is a fork of [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet).

Contact
=======

Email: ahuszagh@gmail.com  
Twitter: KardOnIce

