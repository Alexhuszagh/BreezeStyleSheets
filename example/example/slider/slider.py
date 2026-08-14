"""
Example showing how to add ticks to a QSlider. Note that this does
not work with stylesheets, so it's merely an example of how to
get customized styling behavior with a QSlider.
"""

from typing import TYPE_CHECKING
from typing_extensions import override

from .cli import COLORS, Qt

if TYPE_CHECKING:
    from .._util.typing import QtGui


class Slider(Qt.QtWidgets.QSlider):
    """QSlider with a custom paint event."""

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    @override
    def paintEvent(self, ev: "QtGui.QPaintEvent | None") -> None:
        """Override the paint event to ensure the ticks are painted."""

        painter = Qt.QtWidgets.QStylePainter(self)
        options = Qt.QtWidgets.QStyleOptionSlider()
        self.initStyleOption(options)

        style = self.style()
        assert style is not None
        handle = style.subControlRect(
            Qt.QtWidgets.QStyle.ComplexControl.CC_Slider,
            options,
            Qt.QtWidgets.QStyle.SubControl.SC_SliderHandle,
            self,
        )

        interval = self.tickInterval() or self.pageStep()
        position = self.tickPosition()
        if position != Qt.QtWidgets.QSlider.TickPosition.NoTicks and interval != 0:
            minimum = self.minimum()
            maximum = self.maximum()
            painter.setPen(Qt.QtGui.QColor(*COLORS.tick_color))
            for i in range(minimum, maximum + interval, interval):
                percent = (i - minimum) / (maximum - minimum + 1) + 0.005
                width = (self.width() - handle.width()) + handle.width() / 2
                x = int(percent * width)
                h = 4
                both = Qt.QtWidgets.QSlider.TickPosition.TicksBothSides
                above = Qt.QtWidgets.QSlider.TickPosition.TicksAbove
                below = Qt.QtWidgets.QSlider.TickPosition.TicksBelow
                if position in (both, above):
                    y = self.rect().top()
                    painter.drawLine(x, y, x, y + h)
                if position in (both, below):
                    y = self.rect().bottom()
                    painter.drawLine(x, y, x, y - h)

        options.subControls = Qt.QtWidgets.QStyle.SubControl.SC_SliderGroove
        painter.drawComplexControl(Qt.QtWidgets.QStyle.ComplexControl.CC_Slider, options)

        options.subControls = Qt.QtWidgets.QStyle.SubControl.SC_SliderHandle
        painter.drawComplexControl(Qt.QtWidgets.QStyle.ComplexControl.CC_Slider, options)
