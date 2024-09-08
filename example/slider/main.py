#!/usr/bin/env python
'''
    slider
    ======

    Example showing how to add ticks to a QSlider. Note that this does
    not work with stylesheets, so it's merely an example of how to
    get customized styling behavior with a QSlider.
'''

import sys

import slider


class Ui:
    '''Main class for the user interface.'''

    def setup(self, MainWindow):
        '''Setup our main window for the UI.'''

        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(1068, 824)
        self.centralwidget = slider.compat.QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.layout = slider.compat.QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout.setObjectName('layout')
        self.layout.setAlignment(slider.compat.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.slider = slider.Slider(self.centralwidget)
        self.slider.setOrientation(slider.compat.Horizontal)
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(slider.compat.TicksAbove)
        self.slider.setObjectName('slider')
        self.layout.addWidget(self.slider)


def main():
    'Application entry point'

    app, window = slider.shared.setup_app(slider.args, slider.unknown, slider.compat)

    # setup ui
    ui = Ui()
    ui.setup(window)
    window.setWindowTitle('QSlider with Ticks.')
    window.resize(400, 150)

    slider.shared.set_stylesheet(slider.args, app, slider.compat)
    return slider.shared.exec_app(slider.args, app, window)


if __name__ == '__main__':
    sys.exit(main())
