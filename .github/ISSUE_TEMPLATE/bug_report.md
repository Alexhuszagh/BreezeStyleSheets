---
name: Bug report
about: Create a report to help us improve.
title: "[BUG]"
labels: bug
assignees: Alexhuszagh

---

## Description

Please include a clear and concise description of the bug. Although very unlikely due to the nature of the project, if the bug includes a security vulnerability, please privately report the issue to the [maintainer](mailto:ahuszagh@gmail.com).

## Prerequisites

If applicable to the issue, here are a few things you should provide to help me understand the issue:

- Qt version: [5, 6]
- Extension: [Advanced Docking System, ...]
- Theme: [Dark, Light, Dark-Purple, ...]

## Test case

Please provide a short, complete (with widgets, etc) test case for
the issue, showing clearly the expected and obtained results.

Example test case:

```python
import sys
from PyQt6 import QtCore, QtGui, QtWidgets

QtCore.QDir.addSearchPath('dark', f'dist/pyqt6/dark/')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file = QtCore.QFile('dark:stylesheet.qss')
    file.open(
        QtCore.QFile.OpenModeFlag.ReadOnly | 
        QtCore.QFile.OpenModeFlag.Text
    )
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())

    dialog = QtWidgets.QFileDialog()
    dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
    dialog.exec()

    app.quit()
```
