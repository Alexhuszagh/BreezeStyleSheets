from typing import TYPE_CHECKING, cast
from typing_extensions import override

import math

from .cli import ARGS, COLORS, Qt

if TYPE_CHECKING:
    from .._util.typing import QtCore, QtGui, QtWidgets


def radius(dial: "QtWidgets.QStyleOptionSlider") -> int:
    """Get the radius of the dial."""
    return min(dial.rect.width(), dial.rect.height()) // 2


def groove_rect(dial: "QtWidgets.QStyleOptionSlider") -> "tuple[float, float]":
    """Calculate the bounding rectangle for the dial groove."""

    x0 = dial.rect.width() / 2
    y0 = dial.rect.height() / 2
    pos = dial.rect.topLeft()

    return (pos.x() + x0, pos.y() + y0)


def circle_percent(dial: "QtWidgets.QStyleOptionSlider") -> float:
    """Calculate the percentage of the dial."""

    distance = dial.maximum - dial.minimum
    offset = dial.sliderPosition - dial.minimum

    return offset / distance


def circle_position(
    dial: "QtWidgets.QStyleOptionSlider",
    rect: "QtCore.QRectF",
    position: int,
    r: float,
) -> "tuple[float, float]":
    """Calculate the (x, y) coordinates based on the position on a circle."""

    # Get our center and the percent we've gone alone the dial.
    center = rect.center()
    x0 = center.x()
    y0 = center.y()
    distance = dial.maximum - dial.minimum
    offset = position - dial.minimum
    percent = offset / distance

    # The position of points on a circle follows. The start angle is
    # at the left (0°), and we start from the bottom. The formula
    # to get the position on a circle is:
    #   (x0 + r cos theta, y0 + r sin theta)
    #
    # However, our y point is inverted (goes from the top), so we modify it to:
    #   (x0 + r cos theta, y0 - r sin theta)
    initial = 60
    total_angle = 300
    if dial.dialWrapping:
        initial = 90
        total_angle = 360
    angle = total_angle * percent
    theta = (angle - initial) * math.pi / 180

    return (x0 - r * math.cos(theta), y0 - r * math.sin(theta))


def handle_position(
    dial: "QtWidgets.QStyleOptionSlider",
    rect: "QtCore.QRectF",
    r: float,
) -> "tuple[float, float]":
    """Calculate the position of the handle."""
    return circle_position(dial, rect, dial.sliderPosition, r)


def default_pen(color: "QtGui.QColor", width: float) -> "QtGui.QPen":
    """Create a pen with the default styles."""
    return Qt.QtGui.QPen(color, width)


def round_pen(color: "QtGui.QColor", width: float) -> "QtGui.QPen":
    """Create a pen with round join styles."""
    return Qt.QtGui.QPen(
        color,
        width,
        Qt.QtCore.Qt.PenStyle.SolidLine,
        Qt.QtCore.Qt.PenCapStyle.RoundCap,
        Qt.QtCore.Qt.PenJoinStyle.RoundJoin,
    )


def event_pos(event: "QtGui.QHoverEvent") -> "QtCore.QPointF":
    """Determine the event position."""

    if Qt.version >= (6, 0, 0):
        return event.position()
    return event.posF()  # type: ignore


class Dial(Qt.QtWidgets.QDial):
    """QDial with a custom paint event."""

    def __init__(self, widget: "QtWidgets.QWidget | None" = None) -> None:
        super().__init__(widget)
        if ARGS.stylesheet.name == "native":
            return

        self.installEventFilter(self)

        # Set some configuration settings, since we'll need them later.
        # No reason to recalculate them every time.
        self.font_size = self.font().pointSizeF()
        self.bd_width = 0.09 * self.font_size
        self.groove_width = 5
        self.handle_radius = self.groove_width + 3
        self.notch_start = self.groove_width + 2
        self.notch_end = self.notch_start + 2
        self.notch_width = 2
        self.groove_bd_color = Qt.QtGui.QColor(*COLORS.groove_border)
        self.groove_bg_color = Qt.QtGui.QColor(*COLORS.groove_background)
        self.handle_bg_color = Qt.QtGui.QColor(*COLORS.handle_background)
        self.handle_bd_color = Qt.QtGui.QColor(*COLORS.handle_border)
        self.notch_color = Qt.QtGui.QColor(*COLORS.notch)
        self.selected_color = Qt.QtGui.QColor(*COLORS.selected)

        # Store some state changes.
        self.groove = (0.0, 0.0)
        self.handle = (0.0, 0.0)
        self.is_hovered = False

    @override
    def paintEvent(self, pe: "QtGui.QPaintEvent | None") -> None:
        """Override the paint event to ensure the ticks are painted."""

        if ARGS.stylesheet.name == "native":
            return super().paintEvent(pe)

        painter = Qt.QtWidgets.QStylePainter(self)
        options = Qt.QtWidgets.QStyleOptionSlider()
        self.initStyleOption(options)

        # Get our item colors. Override the color when selected/active.
        handle_bd_color = self.handle_bd_color
        mask = Qt.QtWidgets.QStyle.StateFlag.State_HasFocus | Qt.QtWidgets.QStyle.StateFlag.State_Selected
        # WindowActive
        if options.state & mask or self.is_hovered:
            handle_bd_color = self.selected_color

        # Get the groove settings: this defines the bounding rect
        # and the start and stop angles for the groove. We also
        # make the radius 20% smaller, so it fits nicely within
        # the bounding rect.
        groove_width = self.groove_width * painter.pen().widthF()
        r = radius(options) - 2 * groove_width
        gx, gy = groove_rect(options)
        self.groove = (gx, gy)
        rect = Qt.QtCore.QRectF(gx - r, gy - r, 2 * r, 2 * r)
        # The arc should be everything besides ~30° at the bottom.
        # Units are measured in 1/16th of a degree.
        start_angle = 240 * 16
        span_angle = -300 * 16
        if options.dialWrapping:
            # Have a wrapping dial: have the full circle.
            start_angle = 270 * 16
            span_angle = -360 * 16

        # Get the handle settings.
        hx, hy = handle_position(options, rect, r)
        self.handle = (hx, hy)

        # First, we draw the border for the slider.
        # This is simple, since we just add `0.09em` to the actual groove
        # width and draw it first.
        groove_bd_width = groove_width + self.bd_width
        painter.setPen(round_pen(self.groove_bd_color, groove_bd_width))
        painter.drawArc(rect, start_angle, span_angle)

        # Draw the groove for the slider. We want to stroke the groove so
        # it's quite large, and then we can create a border, etc. for it.
        groove_percent = circle_percent(options)
        groove_stop = int(groove_percent * span_angle)
        painter.setPen(round_pen(self.groove_bg_color, groove_width))
        painter.drawArc(rect, start_angle, span_angle)
        painter.setPen(round_pen(self.selected_color, groove_width))
        painter.drawArc(rect, start_angle, groove_stop)

        # Now, we need to draw the notches. We need to draw these before
        # the handle, since the handle needs to be above the notches.
        notch_step = self.notchSize() * self.singleStep()
        painter.setPen(default_pen(self.notch_color, self.notch_width))
        notch_start = r + self.notch_start
        notch_end = r + self.notch_end
        if self.notchesVisible() and notch_step != 0:
            distance = options.maximum - options.minimum
            position = 0
            # Need an inclusive range: by default dial range is 0-99, but
            # range(0, 100) is 0-99, and we need 0-100. Specially draw
            # the first and the last items.
            positions = list(range(0, distance, notch_step)) + [options.maximum]
            for position in positions:
                nx0, ny0 = circle_position(options, rect, position, notch_start)
                nx1, ny1 = circle_position(options, rect, position, notch_end)
                painter.drawLine(int(nx0), int(ny0), int(nx1), int(ny1))

        # Now, we need to draw the handle. First, we need to get the position
        # of the slider, based on the position and angle it's at.
        painter.setPen(default_pen(handle_bd_color, self.bd_width))
        painter.setBrush(Qt.QtGui.QBrush(self.handle_bg_color))
        handle_pos = Qt.QtCore.QPointF(hx, hy)
        painter.drawEllipse(handle_pos, self.handle_radius, self.handle_radius)

        return None

    @override
    def eventFilter(self, a0: "QtCore.QObject | None", a1: "QtCore.QEvent | None") -> bool:
        """Override the color when we have a hover event."""

        obj = a0
        event = a1

        # If the window isn't active, ignore the hover event.
        window = self.window()
        if window is None or not window.isActiveWindow():
            self.is_hovered = False
            return super().eventFilter(obj, event)
        if event is None:
            return super().eventFilter(obj, event)

        # Determine if we have a hover event, and if the handle
        # is hovered or no longer hovered, change the hover state
        # and trigger a paint event. We need to trigger an immediate
        # paint event, since otherwise we might have a delay in UI change.
        #
        # We use a very mild hack: we merely calculate the bounding rect
        # for the handle, and determine if the mouse is contained in there,
        # rather than calculate if it's actually in the circle. This won't
        # matter except if the dial is scaled by a large amount.
        if event.type() in (Qt.QtCore.QEvent.Type.HoverEnter, Qt.QtCore.QEvent.Type.HoverMove):
            x0 = self.handle[0] - self.handle_radius
            y0 = self.handle[1] - self.handle_radius
            size = 2 * self.handle_radius
            rect = Qt.QtCore.QRectF(x0, y0, size, size)
            self.is_hovered = rect.contains(event_pos(cast("QtGui.QHoverEvent", event)))
            self.repaint()
        elif event.type() == Qt.QtCore.QEvent.Type.HoverLeave:
            self.is_hovered = False
            self.repaint()

        return super().eventFilter(obj, event)
