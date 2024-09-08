#!/usr/bin/env python
'''
    lcd
    ===

    Example showing how to override the `paintEvent` and `eventFilter`
    for a `QLCDNumber`, creating a visually consistent, stylish
    `QLCDNumber` that supports highlighting the handle on the active
    or hovered number.
'''

import sys

import lcd


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        '''Setup our main window for the UI.'''

        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = lcd.QtWidgets.QWidget(MainWindow)
        self.layout = lcd.QtWidgets.QHBoxLayout(self.centralwidget)
        self.layout.setSpacing(0)
        if not lcd.args.no_align:
            self.layout.setAlignment(lcd.compat.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.lcd1 = lcd.LCD(self.centralwidget)
        self.lcd1.display(15)
        self.lcd1.setDigitCount(2)
        self.layout.addWidget(self.lcd1)

        self.lcd2 = lcd.LCD(self.centralwidget)
        self.lcd2.display(31)
        self.lcd2.setHexMode()
        self.lcd2.setDigitCount(2)
        self.layout.addWidget(self.lcd2)

        self.lcd3 = lcd.LCD(self.centralwidget)
        self.lcd3.display(15)
        self.lcd3.setSegmentStyle(lcd.compat.LCDOutline)
        self.lcd3.setFrameShape(lcd.compat.NoFrame)
        self.lcd3.setDigitCount(2)
        self.layout.addWidget(self.lcd3)

        self.lcd4 = lcd.LCD(self.centralwidget)
        self.lcd4.display(15)
        self.lcd4.setSegmentStyle(lcd.compat.LCDFlat)
        self.lcd4.setFrameShape(lcd.compat.NoFrame)
        self.lcd4.setDigitCount(2)
        self.layout.addWidget(self.lcd4)


def main():
    'Application entry point'

    app, window = lcd.shared.setup_app(lcd.args, lcd.unknown, lcd.compat)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('QLCDNumber')
    window.resize(400, 150)

    lcd.shared.set_stylesheet(lcd.args, app, lcd.compat)
    return lcd.shared.exec_app(lcd.args, app, window)


if __name__ == '__main__':
    sys.exit(main())
