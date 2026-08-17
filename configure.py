#!/usr/bin/env python
"""
Configure icons, stylesheets, and resource files.

This is a high-level script meant for the CMake configuration system
or to be used when not distributed as a package.
"""

import sys

from breezestylesheets import __configure__ as configure

__author__ = configure.__author__
__credits__ = configure.__credits__
__license__ = configure.__license__
__version__ = configure.__version__
__version_info__ = configure.__version_info__

if __name__ == "__main__":
    sys.exit(configure.main())
