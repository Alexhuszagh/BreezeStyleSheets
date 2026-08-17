from example._util import cli
from example._util.colors import Colors
from example._util.qt import PyQt

ARGS, UNKNOWN = cli.Parser[cli.Args]().parse()
COLORS = Colors.from_stylesheet(ARGS.stylesheet.name)
Qt = PyQt.from_framework(ARGS.qt_framework)
