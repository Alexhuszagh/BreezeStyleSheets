#!/usr/bin/env python

import os
import shutil
import subprocess
import sys

tests = os.path.dirname(os.path.realpath(__file__))
home = os.path.dirname(tests)
dist = os.path.join(home, 'dist')
distbak = os.path.join(home, 'dist.bak')

def configure(*args):
    '''Run the configure styles command.'''
    subprocess.run([
        sys.executable,
        "configure.py",
        "--clean",
        *args,
    ], check=True)

def qrc(*args):
    return os.path.join(dist, "qrc", *args)

def pyqt6(*args):
    return os.path.join(dist, "pyqt6", *args)

def main():
    '''Check all configure options.'''

    # first, backup our old dist dir if it exists.
    dist_exists = os.path.exists(dist)
    if dist_exists:
        os.rename(dist, distbak)

    try:
        # test various configure options
        os.chdir(home)

        # test a custom QRC name, and only having the light styles, no extensions.
        configure("--styles=light", "--resource=custom.qrc")
        assert os.path.exists(qrc("custom.qrc"))
        assert not os.path.exists(qrc("breeze.qrc"))
        assert os.path.exists(qrc("light", "file.svg"))
        assert not os.path.exists(qrc("light", "pause.svg"))
        assert not os.path.exists(qrc("dark"))
        assert not os.path.exists(qrc("dark-green"))
        assert not os.path.exists(pyqt6())

        # test the default
        configure()
        assert os.path.exists(qrc("breeze.qrc"))
        assert os.path.exists(qrc("dark", "file.svg"))
        assert os.path.exists(qrc("light", "file.svg"))
        assert not os.path.exists(qrc("light", "pause.svg"))
        assert not os.path.exists(qrc("dark-green"))
        assert not os.path.exists(pyqt6())

        # test with a custom theme
        configure("--styles=dark-green")
        assert os.path.exists(qrc("breeze.qrc"))
        assert os.path.exists(qrc("dark-green", "file.svg"))
        assert not os.path.exists(qrc("dark-green", "pause.svg"))
        assert not os.path.exists(qrc("dark"))
        assert not os.path.exists(qrc("light"))
        assert not os.path.exists(pyqt6())

        # test without QRC resources or pyqt6
        configure("--no-qrc")
        assert not os.path.exists(dist)

        # test with pyqt6 only
        configure("--no-qrc", "--pyqt6")
        assert os.path.exists(pyqt6("dark", "file.svg"))
        assert os.path.exists(pyqt6("light", "file.svg"))
        assert not os.path.exists(pyqt6("light", "pause.svg"))
        assert not os.path.exists(pyqt6("dark-green"))
        assert not os.path.exists(qrc())

        # test with qrc and pyqt6
        configure("--pyqt6")
        assert os.path.exists(qrc("dark", "file.svg"))
        assert os.path.exists(qrc("light", "file.svg"))
        assert not os.path.exists(qrc("light", "pause.svg"))
        assert os.path.exists(pyqt6("dark", "file.svg"))
        assert os.path.exists(pyqt6("light", "file.svg"))
        assert not os.path.exists(pyqt6("light", "pause.svg"))

        # test with some extensions
        configure("--pyqt6", "--extensions=all")
        assert os.path.exists(qrc("dark", "file.svg"))
        assert os.path.exists(qrc("light", "file.svg"))
        assert os.path.exists(qrc("light", "pause.svg"))
        assert os.path.exists(pyqt6("dark", "file.svg"))
        assert os.path.exists(pyqt6("light", "file.svg"))
        assert os.path.exists(pyqt6("light", "pause.svg"))

    finally:
        # clean and restore our original dist settings.
        if os.path.exists(dist):
            shutil.rmtree(dist)
        if dist_exists:
            os.rename(distbak, dist)

if __name__ == '__main__':
    sys.exit(main())
