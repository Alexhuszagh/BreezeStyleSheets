# pyright: reportNoOverloadImplementation=false
"""Type definitions for QtGui consistent with PyQt6."""

from typing import ClassVar

from PyQt6.QtGui import (
    QAbstractFileIconProvider,
    QAbstractTextDocumentLayout,
    QAction,
    QActionEvent,
    QActionGroup,
    QBackingStore,
    QBitmap,
    QBrush,
    QChildWindowEvent,
    QClipboard,
    QCloseEvent,
    QColor,
    QColorConstants,
    QColorSpace,
    QColorTransform,
    QConicalGradient,
    QContextMenuEvent,
    QCursor,
    QDesktopServices,
    QDoubleValidator,
    QDrag,
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QDropEvent,
    QEnterEvent,
    QEventPoint,
    QExposeEvent,
    QFileOpenEvent,
    QFileSystemModel,
    QFocusEvent,
    QFont,
    QFontDatabase,
    QFontInfo,
    QFontMetrics,
    QFontMetricsF,
    QGlyphRun,
    QGradient,
    QGuiApplication,
    QHelpEvent,
    QHideEvent,
    QHoverEvent,
    QIcon,
    QIconDragEvent,
    QIconEngine,
    QImage,
    QImageIOHandler,
    QImageReader,
    QImageWriter,
    QInputDevice,
    QInputEvent,
    QInputMethod,
    QInputMethodEvent,
    QInputMethodQueryEvent,
    QIntValidator,
    QKeyEvent,
    QKeySequence,
    QLinearGradient,
    QMatrix2x2,
    QMatrix2x3,
    QMatrix2x4,
    QMatrix3x2,
    QMatrix3x3,
    QMatrix3x4,
    QMatrix4x2,
    QMatrix4x3,
    QMatrix4x4,
    QMouseEvent,
    QMoveEvent,
    QMovie,
    QNativeGestureEvent,
    QOffscreenSurface,
    QOpenGLContext,
    QOpenGLContextGroup,
    QPagedPaintDevice,
    QPageLayout,
    QPageRanges,
    QPageSize,
    QPaintDevice,
    QPaintDeviceWindow,
    QPaintEngine,
    QPaintEngineState,
    QPainter,
    QPainterPath,
    QPainterPathStroker,
    QPaintEvent,
    QPalette,
    QPdfWriter,
    QPen,
    QPicture,
    QPixelFormat,
    QPixmap,
    QPixmapCache,
    QPlatformSurfaceEvent,
    QPointerEvent,
    QPointingDevice,
    QPointingDeviceUniqueId,
    QPolygon,
    QPolygonF,
    QQuaternion,
    QRadialGradient,
    QRasterWindow,
    QRawFont,
    QRegion,
    QRegularExpressionValidator,
    QResizeEvent,
    QRgba64,
    QScreen,
    QScrollEvent,
    QScrollPrepareEvent,
    QSessionManager,
    QShortcut,
    QShortcutEvent,
    QShowEvent,
    QSinglePointEvent,
    QStandardItem,
    QStandardItemModel,
    QStaticText,
    QStatusTipEvent,
    QStyleHints,
    QSurface,
    QSurfaceFormat,
    QSyntaxHighlighter,
    QTabletEvent,
    QTextBlock,
    QTextBlockFormat,
    QTextBlockGroup,
    QTextBlockUserData,
    QTextCharFormat,
    QTextCursor,
    QTextDocument,
    QTextDocumentFragment,
    QTextDocumentWriter,
    QTextFormat,
    QTextFragment,
    QTextFrame,
    QTextFrameFormat,
    QTextImageFormat,
    QTextInlineObject,
    QTextItem,
    QTextLayout,
    QTextLength,
    QTextLine,
    QTextList,
    QTextListFormat,
    QTextObject,
    QTextObjectInterface,
    QTextOption,
    QTextTable,
    QTextTableCell,
    QTextTableCellFormat,
    QTextTableFormat,
    QTouchEvent,
    QTransform,
    QUndoCommand,
    QUndoGroup,
    QUndoStack,
    QValidator,
    QVector2D,
    QVector3D,
    QVector4D,
    QWhatsThisClickedEvent,
    QWheelEvent,
    QWindow,
    QWindowStateChangeEvent,
)

__all__ = [
    "_QtGui",
    "QAbstractFileIconProvider",
    "QAbstractTextDocumentLayout",
    "QAction",
    "QActionEvent",
    "QActionGroup",
    "QBackingStore",
    "QBitmap",
    "QBrush",
    "QChildWindowEvent",
    "QClipboard",
    "QCloseEvent",
    "QColor",
    "QColorConstants",
    "QColorSpace",
    "QColorTransform",
    "QConicalGradient",
    "QContextMenuEvent",
    "QCursor",
    "QDesktopServices",
    "QDoubleValidator",
    "QDrag",
    "QDragEnterEvent",
    "QDragLeaveEvent",
    "QDragMoveEvent",
    "QDropEvent",
    "QEnterEvent",
    "QEventPoint",
    "QExposeEvent",
    "QFileOpenEvent",
    "QFileSystemModel",
    "QFocusEvent",
    "QFont",
    "QFontDatabase",
    "QFontInfo",
    "QFontMetrics",
    "QFontMetricsF",
    "QGlyphRun",
    "QGradient",
    "QGuiApplication",
    "QHelpEvent",
    "QHideEvent",
    "QHoverEvent",
    "QIcon",
    "QIconDragEvent",
    "QIconEngine",
    "QImage",
    "QImageIOHandler",
    "QImageReader",
    "QImageWriter",
    "QInputDevice",
    "QInputEvent",
    "QInputMethod",
    "QInputMethodEvent",
    "QInputMethodQueryEvent",
    "QIntValidator",
    "QKeyEvent",
    "QKeySequence",
    "QLinearGradient",
    "QMatrix2x2",
    "QMatrix2x3",
    "QMatrix2x4",
    "QMatrix3x2",
    "QMatrix3x3",
    "QMatrix3x4",
    "QMatrix4x2",
    "QMatrix4x3",
    "QMatrix4x4",
    "QMouseEvent",
    "QMoveEvent",
    "QMovie",
    "QNativeGestureEvent",
    "QOffscreenSurface",
    "QOpenGLContext",
    "QOpenGLContextGroup",
    "QPageLayout",
    "QPageRanges",
    "QPageSize",
    "QPagedPaintDevice",
    "QPaintDevice",
    "QPaintDeviceWindow",
    "QPaintEngine",
    "QPaintEngineState",
    "QPaintEvent",
    "QPainter",
    "QPainterPath",
    "QPainterPathStroker",
    "QPalette",
    "QPdfWriter",
    "QPen",
    "QPicture",
    "QPixelFormat",
    "QPixmap",
    "QPixmapCache",
    "QPlatformSurfaceEvent",
    "QPointerEvent",
    "QPointingDevice",
    "QPointingDeviceUniqueId",
    "QPolygon",
    "QPolygonF",
    "QQuaternion",
    "QRadialGradient",
    "QRasterWindow",
    "QRawFont",
    "QRegion",
    "QRegularExpressionValidator",
    "QResizeEvent",
    "QRgba64",
    "QScreen",
    "QScrollEvent",
    "QScrollPrepareEvent",
    "QSessionManager",
    "QShortcut",
    "QShortcutEvent",
    "QShowEvent",
    "QSinglePointEvent",
    "QStandardItem",
    "QStandardItemModel",
    "QStaticText",
    "QStatusTipEvent",
    "QStyleHints",
    "QSurface",
    "QSurfaceFormat",
    "QSyntaxHighlighter",
    "QTabletEvent",
    "QTextBlock",
    "QTextBlockFormat",
    "QTextBlockGroup",
    "QTextBlockUserData",
    "QTextCharFormat",
    "QTextCursor",
    "QTextDocument",
    "QTextDocumentFragment",
    "QTextDocumentWriter",
    "QTextFormat",
    "QTextFragment",
    "QTextFrame",
    "QTextFrameFormat",
    "QTextImageFormat",
    "QTextInlineObject",
    "QTextItem",
    "QTextLayout",
    "QTextLength",
    "QTextLine",
    "QTextList",
    "QTextListFormat",
    "QTextObject",
    "QTextObjectInterface",
    "QTextOption",
    "QTextTable",
    "QTextTableCell",
    "QTextTableCellFormat",
    "QTextTableFormat",
    "QTouchEvent",
    "QTransform",
    "QUndoCommand",
    "QUndoGroup",
    "QUndoStack",
    "QValidator",
    "QVector2D",
    "QVector3D",
    "QVector4D",
    "QWhatsThisClickedEvent",
    "QWheelEvent",
    "QWindow",
    "QWindowStateChangeEvent",
]


class _QtGui:
    """Namespace-like wrapper for our static type checkers."""

    QAbstractFileIconProvider: ClassVar["type[QAbstractFileIconProvider]"]
    QAbstractTextDocumentLayout: ClassVar["type[QAbstractTextDocumentLayout]"]
    QAction: ClassVar["type[QAction]"]
    QActionEvent: ClassVar["type[QActionEvent]"]
    QActionGroup: ClassVar["type[QActionGroup]"]
    QBackingStore: ClassVar["type[QBackingStore]"]
    QBitmap: ClassVar["type[QBitmap]"]
    QBrush: ClassVar["type[QBrush]"]
    QChildWindowEvent: ClassVar["type[QChildWindowEvent]"]
    QClipboard: ClassVar["type[QClipboard]"]
    QCloseEvent: ClassVar["type[QCloseEvent]"]
    QColor: ClassVar["type[QColor]"]
    QColorConstants: ClassVar["type[QColorConstants]"]
    QColorSpace: ClassVar["type[QColorSpace]"]
    QColorTransform: ClassVar["type[QColorTransform]"]
    QConicalGradient: ClassVar["type[QConicalGradient]"]
    QContextMenuEvent: ClassVar["type[QContextMenuEvent]"]
    QCursor: ClassVar["type[QCursor]"]
    QDesktopServices: ClassVar["type[QDesktopServices]"]
    QDoubleValidator: ClassVar["type[QDoubleValidator]"]
    QDrag: ClassVar["type[QDrag]"]
    QDragEnterEvent: ClassVar["type[QDragEnterEvent]"]
    QDragLeaveEvent: ClassVar["type[QDragLeaveEvent]"]
    QDragMoveEvent: ClassVar["type[QDragMoveEvent]"]
    QDropEvent: ClassVar["type[QDropEvent]"]
    QEnterEvent: ClassVar["type[QEnterEvent]"]
    QEventPoint: ClassVar["type[QEventPoint]"]
    QExposeEvent: ClassVar["type[QExposeEvent]"]
    QFileOpenEvent: ClassVar["type[QFileOpenEvent]"]
    QFileSystemModel: ClassVar["type[QFileSystemModel]"]
    QFocusEvent: ClassVar["type[QFocusEvent]"]
    QFont: ClassVar["type[QFont]"]
    QFontDatabase: ClassVar["type[QFontDatabase]"]
    QFontInfo: ClassVar["type[QFontInfo]"]
    QFontMetrics: ClassVar["type[QFontMetrics]"]
    QFontMetricsF: ClassVar["type[QFontMetricsF]"]
    QGlyphRun: ClassVar["type[QGlyphRun]"]
    QGradient: ClassVar["type[QGradient]"]
    QGuiApplication: ClassVar["type[QGuiApplication]"]
    QHelpEvent: ClassVar["type[QHelpEvent]"]
    QHideEvent: ClassVar["type[QHideEvent]"]
    QHoverEvent: ClassVar["type[QHoverEvent]"]
    QIcon: ClassVar["type[QIcon]"]
    QIconDragEvent: ClassVar["type[QIconDragEvent]"]
    QIconEngine: ClassVar["type[QIconEngine]"]
    QImage: ClassVar["type[QImage]"]
    QImageIOHandler: ClassVar["type[QImageIOHandler]"]
    QImageReader: ClassVar["type[QImageReader]"]
    QImageWriter: ClassVar["type[QImageWriter]"]
    QInputDevice: ClassVar["type[QInputDevice]"]
    QInputEvent: ClassVar["type[QInputEvent]"]
    QInputMethod: ClassVar["type[QInputMethod]"]
    QInputMethodEvent: ClassVar["type[QInputMethodEvent]"]
    QInputMethodQueryEvent: ClassVar["type[QInputMethodQueryEvent]"]
    QIntValidator: ClassVar["type[QIntValidator]"]
    QKeyEvent: ClassVar["type[QKeyEvent]"]
    QKeySequence: ClassVar["type[QKeySequence]"]
    QLinearGradient: ClassVar["type[QLinearGradient]"]
    QMatrix2x2: ClassVar["type[QMatrix2x2]"]
    QMatrix2x3: ClassVar["type[QMatrix2x3]"]
    QMatrix2x4: ClassVar["type[QMatrix2x4]"]
    QMatrix3x2: ClassVar["type[QMatrix3x2]"]
    QMatrix3x3: ClassVar["type[QMatrix3x3]"]
    QMatrix3x4: ClassVar["type[QMatrix3x4]"]
    QMatrix4x2: ClassVar["type[QMatrix4x2]"]
    QMatrix4x3: ClassVar["type[QMatrix4x3]"]
    QMatrix4x4: ClassVar["type[QMatrix4x4]"]
    QMouseEvent: ClassVar["type[QMouseEvent]"]
    QMoveEvent: ClassVar["type[QMoveEvent]"]
    QMovie: ClassVar["type[QMovie]"]
    QNativeGestureEvent: ClassVar["type[QNativeGestureEvent]"]
    QOffscreenSurface: ClassVar["type[QOffscreenSurface]"]
    QOpenGLContext: ClassVar["type[QOpenGLContext]"]
    QOpenGLContextGroup: ClassVar["type[QOpenGLContextGroup]"]
    QPageLayout: ClassVar["type[QPageLayout]"]
    QPageRanges: ClassVar["type[QPageRanges]"]
    QPageSize: ClassVar["type[QPageSize]"]
    QPagedPaintDevice: ClassVar["type[QPagedPaintDevice]"]
    QPaintDevice: ClassVar["type[QPaintDevice]"]
    QPaintDeviceWindow: ClassVar["type[QPaintDeviceWindow]"]
    QPaintEngine: ClassVar["type[QPaintEngine]"]
    QPaintEngineState: ClassVar["type[QPaintEngineState]"]
    QPaintEvent: ClassVar["type[QPaintEvent]"]
    QPainter: ClassVar["type[QPainter]"]
    QPainterPath: ClassVar["type[QPainterPath]"]
    QPainterPathStroker: ClassVar["type[QPainterPathStroker]"]
    QPalette: ClassVar["type[QPalette]"]
    QPdfWriter: ClassVar["type[QPdfWriter]"]
    QPen: ClassVar["type[QPen]"]
    QPicture: ClassVar["type[QPicture]"]
    QPixelFormat: ClassVar["type[QPixelFormat]"]
    QPixmap: ClassVar["type[QPixmap]"]
    QPixmapCache: ClassVar["type[QPixmapCache]"]
    QPlatformSurfaceEvent: ClassVar["type[QPlatformSurfaceEvent]"]
    QPointerEvent: ClassVar["type[QPointerEvent]"]
    QPointingDevice: ClassVar["type[QPointingDevice]"]
    QPointingDeviceUniqueId: ClassVar["type[QPointingDeviceUniqueId]"]
    QPolygon: ClassVar["type[QPolygon]"]
    QPolygonF: ClassVar["type[QPolygonF]"]
    QQuaternion: ClassVar["type[QQuaternion]"]
    QRadialGradient: ClassVar["type[QRadialGradient]"]
    QRasterWindow: ClassVar["type[QRasterWindow]"]
    QRawFont: ClassVar["type[QRawFont]"]
    QRegion: ClassVar["type[QRegion]"]
    QRegularExpressionValidator: ClassVar["type[QRegularExpressionValidator]"]
    QResizeEvent: ClassVar["type[QResizeEvent]"]
    QRgba64: ClassVar["type[QRgba64]"]
    QScreen: ClassVar["type[QScreen]"]
    QScrollEvent: ClassVar["type[QScrollEvent]"]
    QScrollPrepareEvent: ClassVar["type[QScrollPrepareEvent]"]
    QSessionManager: ClassVar["type[QSessionManager]"]
    QShortcut: ClassVar["type[QShortcut]"]
    QShortcutEvent: ClassVar["type[QShortcutEvent]"]
    QShowEvent: ClassVar["type[QShowEvent]"]
    QSinglePointEvent: ClassVar["type[QSinglePointEvent]"]
    QStandardItem: ClassVar["type[QStandardItem]"]
    QStandardItemModel: ClassVar["type[QStandardItemModel]"]
    QStaticText: ClassVar["type[QStaticText]"]
    QStatusTipEvent: ClassVar["type[QStatusTipEvent]"]
    QStyleHints: ClassVar["type[QStyleHints]"]
    QSurface: ClassVar["type[QSurface]"]
    QSurfaceFormat: ClassVar["type[QSurfaceFormat]"]
    QSyntaxHighlighter: ClassVar["type[QSyntaxHighlighter]"]
    QTabletEvent: ClassVar["type[QTabletEvent]"]
    QTextBlock: ClassVar["type[QTextBlock]"]
    QTextBlockFormat: ClassVar["type[QTextBlockFormat]"]
    QTextBlockGroup: ClassVar["type[QTextBlockGroup]"]
    QTextBlockUserData: ClassVar["type[QTextBlockUserData]"]
    QTextCharFormat: ClassVar["type[QTextCharFormat]"]
    QTextCursor: ClassVar["type[QTextCursor]"]
    QTextDocument: ClassVar["type[QTextDocument]"]
    QTextDocumentFragment: ClassVar["type[QTextDocumentFragment]"]
    QTextDocumentWriter: ClassVar["type[QTextDocumentWriter]"]
    QTextFormat: ClassVar["type[QTextFormat]"]
    QTextFragment: ClassVar["type[QTextFragment]"]
    QTextFrame: ClassVar["type[QTextFrame]"]
    QTextFrameFormat: ClassVar["type[QTextFrameFormat]"]
    QTextImageFormat: ClassVar["type[QTextImageFormat]"]
    QTextInlineObject: ClassVar["type[QTextInlineObject]"]
    QTextItem: ClassVar["type[QTextItem]"]
    QTextLayout: ClassVar["type[QTextLayout]"]
    QTextLength: ClassVar["type[QTextLength]"]
    QTextLine: ClassVar["type[QTextLine]"]
    QTextList: ClassVar["type[QTextList]"]
    QTextListFormat: ClassVar["type[QTextListFormat]"]
    QTextObject: ClassVar["type[QTextObject]"]
    QTextObjectInterface: ClassVar["type[QTextObjectInterface]"]
    QTextOption: ClassVar["type[QTextOption]"]
    QTextTable: ClassVar["type[QTextTable]"]
    QTextTableCell: ClassVar["type[QTextTableCell]"]
    QTextTableCellFormat: ClassVar["type[QTextTableCellFormat]"]
    QTextTableFormat: ClassVar["type[QTextTableFormat]"]
    QTouchEvent: ClassVar["type[QTouchEvent]"]
    QTransform: ClassVar["type[QTransform]"]
    QUndoCommand: ClassVar["type[QUndoCommand]"]
    QUndoGroup: ClassVar["type[QUndoGroup]"]
    QUndoStack: ClassVar["type[QUndoStack]"]
    QValidator: ClassVar["type[QValidator]"]
    QVector2D: ClassVar["type[QVector2D]"]
    QVector3D: ClassVar["type[QVector3D]"]
    QVector4D: ClassVar["type[QVector4D]"]
    QWhatsThisClickedEvent: ClassVar["type[QWhatsThisClickedEvent]"]
    QWheelEvent: ClassVar["type[QWheelEvent]"]
    QWindow: ClassVar["type[QWindow]"]
    QWindowStateChangeEvent: ClassVar["type[QWindowStateChangeEvent]"]
