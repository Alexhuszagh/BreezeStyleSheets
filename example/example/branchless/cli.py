from example._util import cli
from example._util.qt import PyQt

ARGS, UNKNOWN = cli.Parser[cli.Args]().parse()
Qt = PyQt.from_framework(ARGS.qt_framework)
