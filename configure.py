#!/usr/bin/env python
'''
configure

Configure icons, stylesheets, and resource files.
'''

import sys

from breezestylesheets import __configure__ as configure

__version__ = configure.__version__

if __name__ == '__main__':
    sys.exit(configure.main())
