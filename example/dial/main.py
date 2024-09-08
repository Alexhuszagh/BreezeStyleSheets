#!/usr/bin/env python
'''
    dial
    ====

    Sample UI widget with our dial.
'''

import sys

import dial


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        '''Setup our main window for the UI.'''

        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = dial.compat.QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = dial.compat.QtWidgets.QHBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        if not dial.args.no_align:
            self.layout.setAlignment(dial.compat.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.dial1 = dial.Dial(self.centralwidget)
        self.layout.addWidget(self.dial1)

        self.dial2 = dial.Dial(self.centralwidget)
        self.dial2.setNotchesVisible(True)
        self.layout.addWidget(self.dial2)

        self.dial3 = dial.Dial(self.centralwidget)
        self.dial3.setWrapping(True)
        self.layout.addWidget(self.dial3)


def main():
    'Application entry point'

    app, window = dial.shared.setup_app(dial.args, dial.unknown, dial.compat)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('QDial')
    window.resize(400, 150)

    dial.shared.set_stylesheet(dial.args, app, dial.compat)
    return dial.shared.exec_app(dial.args, app, window)


if __name__ == '__main__':
    sys.exit(main())
