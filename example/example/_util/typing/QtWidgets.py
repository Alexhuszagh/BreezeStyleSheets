# pyright: reportNoOverloadImplementation=false
"""Type definitions for QtWidgets consistent with PyQt6."""

from typing import ClassVar

from PyQt6.QtWidgets import (
    QAbstractButton,
    QAbstractGraphicsShapeItem,
    QAbstractItemDelegate,
    QAbstractItemView,
    QAbstractScrollArea,
    QAbstractSlider,
    QAbstractSpinBox,
    QApplication,
    QBoxLayout,
    QButtonGroup,
    QCalendarWidget,
    QCheckBox,
    QColorDialog,
    QColumnView,
    QComboBox,
    QCommandLinkButton,
    QCommonStyle,
    QCompleter,
    QDataWidgetMapper,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDialog,
    QDialogButtonBox,
    QDockWidget,
    QDoubleSpinBox,
    QErrorMessage,
    QFileDialog,
    QFileIconProvider,
    QFocusFrame,
    QFontComboBox,
    QFontDialog,
    QFormLayout,
    QFrame,
    QGesture,
    QGestureEvent,
    QGestureRecognizer,
    QGraphicsAnchor,
    QGraphicsAnchorLayout,
    QGraphicsBlurEffect,
    QGraphicsColorizeEffect,
    QGraphicsDropShadowEffect,
    QGraphicsEffect,
    QGraphicsEllipseItem,
    QGraphicsGridLayout,
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsLayout,
    QGraphicsLayoutItem,
    QGraphicsLinearLayout,
    QGraphicsLineItem,
    QGraphicsObject,
    QGraphicsOpacityEffect,
    QGraphicsPathItem,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QGraphicsProxyWidget,
    QGraphicsRectItem,
    QGraphicsRotation,
    QGraphicsScale,
    QGraphicsScene,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneDragDropEvent,
    QGraphicsSceneEvent,
    QGraphicsSceneHelpEvent,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
    QGraphicsSceneMoveEvent,
    QGraphicsSceneResizeEvent,
    QGraphicsSceneWheelEvent,
    QGraphicsSimpleTextItem,
    QGraphicsTextItem,
    QGraphicsTransform,
    QGraphicsView,
    QGraphicsWidget,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QItemDelegate,
    QItemEditorCreatorBase,
    QItemEditorFactory,
    QKeySequenceEdit,
    QLabel,
    QLayout,
    QLayoutItem,
    QLCDNumber,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPanGesture,
    QPinchGesture,
    QPlainTextDocumentLayout,
    QPlainTextEdit,
    QProgressBar,
    QProgressDialog,
    QProxyStyle,
    QPushButton,
    QRadioButton,
    QRubberBand,
    QScrollArea,
    QScrollBar,
    QScroller,
    QScrollerProperties,
    QSizeGrip,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QSplashScreen,
    QSplitter,
    QSplitterHandle,
    QStackedLayout,
    QStackedWidget,
    QStatusBar,
    QStyle,
    QStyledItemDelegate,
    QStyleFactory,
    QStyleHintReturn,
    QStyleHintReturnMask,
    QStyleHintReturnVariant,
    QStyleOption,
    QStyleOptionButton,
    QStyleOptionComboBox,
    QStyleOptionComplex,
    QStyleOptionDockWidget,
    QStyleOptionFocusRect,
    QStyleOptionFrame,
    QStyleOptionGraphicsItem,
    QStyleOptionGroupBox,
    QStyleOptionHeader,
    QStyleOptionHeaderV2,
    QStyleOptionMenuItem,
    QStyleOptionProgressBar,
    QStyleOptionRubberBand,
    QStyleOptionSizeGrip,
    QStyleOptionSlider,
    QStyleOptionSpinBox,
    QStyleOptionTab,
    QStyleOptionTabBarBase,
    QStyleOptionTabWidgetFrame,
    QStyleOptionTitleBar,
    QStyleOptionToolBar,
    QStyleOptionToolBox,
    QStyleOptionToolButton,
    QStyleOptionViewItem,
    QStylePainter,
    QSwipeGesture,
    QSystemTrayIcon,
    QTabBar,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTableWidgetSelectionRange,
    QTabWidget,
    QTapAndHoldGesture,
    QTapGesture,
    QTextBrowser,
    QTextEdit,
    QTimeEdit,
    QToolBar,
    QToolBox,
    QToolButton,
    QToolTip,
    QTreeView,
    QTreeWidget,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
    QUndoView,
    QVBoxLayout,
    QWhatsThis,
    QWidget,
    QWidgetAction,
    QWidgetItem,
    QWizard,
    QWizardPage,
)

__all__ = [
    "_QtWidgets",
    "QAbstractButton",
    "QAbstractGraphicsShapeItem",
    "QAbstractItemDelegate",
    "QAbstractItemView",
    "QAbstractScrollArea",
    "QAbstractSlider",
    "QAbstractSpinBox",
    "QApplication",
    "QBoxLayout",
    "QButtonGroup",
    "QCalendarWidget",
    "QCheckBox",
    "QColorDialog",
    "QColumnView",
    "QComboBox",
    "QCommandLinkButton",
    "QCommonStyle",
    "QCompleter",
    "QDataWidgetMapper",
    "QDateEdit",
    "QDateTimeEdit",
    "QDial",
    "QDialog",
    "QDialogButtonBox",
    "QDockWidget",
    "QDoubleSpinBox",
    "QErrorMessage",
    "QFileDialog",
    "QFileIconProvider",
    "QFocusFrame",
    "QFontComboBox",
    "QFontDialog",
    "QFormLayout",
    "QFrame",
    "QGesture",
    "QGestureEvent",
    "QGestureRecognizer",
    "QGraphicsAnchor",
    "QGraphicsAnchorLayout",
    "QGraphicsBlurEffect",
    "QGraphicsColorizeEffect",
    "QGraphicsDropShadowEffect",
    "QGraphicsEffect",
    "QGraphicsEllipseItem",
    "QGraphicsGridLayout",
    "QGraphicsItem",
    "QGraphicsItemGroup",
    "QGraphicsLayout",
    "QGraphicsLayoutItem",
    "QGraphicsLinearLayout",
    "QGraphicsLineItem",
    "QGraphicsObject",
    "QGraphicsOpacityEffect",
    "QGraphicsPathItem",
    "QGraphicsPixmapItem",
    "QGraphicsPolygonItem",
    "QGraphicsProxyWidget",
    "QGraphicsRectItem",
    "QGraphicsRotation",
    "QGraphicsScale",
    "QGraphicsScene",
    "QGraphicsSceneContextMenuEvent",
    "QGraphicsSceneDragDropEvent",
    "QGraphicsSceneEvent",
    "QGraphicsSceneHelpEvent",
    "QGraphicsSceneHoverEvent",
    "QGraphicsSceneMouseEvent",
    "QGraphicsSceneMoveEvent",
    "QGraphicsSceneResizeEvent",
    "QGraphicsSceneWheelEvent",
    "QGraphicsSimpleTextItem",
    "QGraphicsTextItem",
    "QGraphicsTransform",
    "QGraphicsView",
    "QGraphicsWidget",
    "QGridLayout",
    "QGroupBox",
    "QHBoxLayout",
    "QHeaderView",
    "QInputDialog",
    "QItemDelegate",
    "QItemEditorCreatorBase",
    "QItemEditorFactory",
    "QKeySequenceEdit",
    "QLabel",
    "QLayout",
    "QLayoutItem",
    "QLCDNumber",
    "QLineEdit",
    "QListView",
    "QListWidget",
    "QListWidgetItem",
    "QMainWindow",
    "QMdiArea",
    "QMdiSubWindow",
    "QMenu",
    "QMenuBar",
    "QMessageBox",
    "QPanGesture",
    "QPinchGesture",
    "QPlainTextDocumentLayout",
    "QPlainTextEdit",
    "QProgressBar",
    "QProgressDialog",
    "QProxyStyle",
    "QPushButton",
    "QRadioButton",
    "QRubberBand",
    "QScrollArea",
    "QScrollBar",
    "QScroller",
    "QScrollerProperties",
    "QSizeGrip",
    "QSizePolicy",
    "QSlider",
    "QSpacerItem",
    "QSpinBox",
    "QSplashScreen",
    "QSplitter",
    "QSplitterHandle",
    "QStackedLayout",
    "QStackedWidget",
    "QStatusBar",
    "QStyle",
    "QStyledItemDelegate",
    "QStyleFactory",
    "QStyleHintReturn",
    "QStyleHintReturnMask",
    "QStyleHintReturnVariant",
    "QStyleOption",
    "QStyleOptionButton",
    "QStyleOptionComboBox",
    "QStyleOptionComplex",
    "QStyleOptionDockWidget",
    "QStyleOptionFocusRect",
    "QStyleOptionFrame",
    "QStyleOptionGraphicsItem",
    "QStyleOptionGroupBox",
    "QStyleOptionHeader",
    "QStyleOptionHeaderV2",
    "QStyleOptionMenuItem",
    "QStyleOptionProgressBar",
    "QStyleOptionRubberBand",
    "QStyleOptionSizeGrip",
    "QStyleOptionSlider",
    "QStyleOptionSpinBox",
    "QStyleOptionTab",
    "QStyleOptionTabBarBase",
    "QStyleOptionTabWidgetFrame",
    "QStyleOptionTitleBar",
    "QStyleOptionToolBar",
    "QStyleOptionToolBox",
    "QStyleOptionToolButton",
    "QStyleOptionViewItem",
    "QStylePainter",
    "QSwipeGesture",
    "QSystemTrayIcon",
    "QTabBar",
    "QTableView",
    "QTableWidget",
    "QTableWidgetItem",
    "QTableWidgetSelectionRange",
    "QTabWidget",
    "QTapAndHoldGesture",
    "QTapGesture",
    "QTextBrowser",
    "QTextEdit",
    "QTimeEdit",
    "QToolBar",
    "QToolBox",
    "QToolButton",
    "QToolTip",
    "QTreeView",
    "QTreeWidget",
    "QTreeWidgetItem",
    "QTreeWidgetItemIterator",
    "QUndoView",
    "QVBoxLayout",
    "QWhatsThis",
    "QWidget",
    "QWidgetAction",
    "QWidgetItem",
    "QWizard",
    "QWizardPage",
]


class _QtWidgets:
    """Namespace-like wrapper for our static type checkers."""

    QAbstractButton: ClassVar["type[QAbstractButton]"]
    QAbstractGraphicsShapeItem: ClassVar["type[QAbstractGraphicsShapeItem]"]
    QAbstractItemDelegate: ClassVar["type[QAbstractItemDelegate]"]
    QAbstractItemView: ClassVar["type[QAbstractItemView]"]
    QAbstractScrollArea: ClassVar["type[QAbstractScrollArea]"]
    QAbstractSlider: ClassVar["type[QAbstractSlider]"]
    QAbstractSpinBox: ClassVar["type[QAbstractSpinBox]"]
    QApplication: ClassVar["type[QApplication]"]
    QBoxLayout: ClassVar["type[QBoxLayout]"]
    QButtonGroup: ClassVar["type[QButtonGroup]"]
    QCalendarWidget: ClassVar["type[QCalendarWidget]"]
    QCheckBox: ClassVar["type[QCheckBox]"]
    QColorDialog: ClassVar["type[QColorDialog]"]
    QColumnView: ClassVar["type[QColumnView]"]
    QComboBox: ClassVar["type[QComboBox]"]
    QCommandLinkButton: ClassVar["type[QCommandLinkButton]"]
    QCommonStyle: ClassVar["type[QCommonStyle]"]
    QCompleter: ClassVar["type[QCompleter]"]
    QDataWidgetMapper: ClassVar["type[QDataWidgetMapper]"]
    QDateEdit: ClassVar["type[QDateEdit]"]
    QDateTimeEdit: ClassVar["type[QDateTimeEdit]"]
    QDial: ClassVar["type[QDial]"]
    QDialog: ClassVar["type[QDialog]"]
    QDialogButtonBox: ClassVar["type[QDialogButtonBox]"]
    QDockWidget: ClassVar["type[QDockWidget]"]
    QDoubleSpinBox: ClassVar["type[QDoubleSpinBox]"]
    QErrorMessage: ClassVar["type[QErrorMessage]"]
    QFileDialog: ClassVar["type[QFileDialog]"]
    QFileIconProvider: ClassVar["type[QFileIconProvider]"]
    QFocusFrame: ClassVar["type[QFocusFrame]"]
    QFontComboBox: ClassVar["type[QFontComboBox]"]
    QFontDialog: ClassVar["type[QFontDialog]"]
    QFormLayout: ClassVar["type[QFormLayout]"]
    QFrame: ClassVar["type[QFrame]"]
    QGesture: ClassVar["type[QGesture]"]
    QGestureEvent: ClassVar["type[QGestureEvent]"]
    QGestureRecognizer: ClassVar["type[QGestureRecognizer]"]
    QGraphicsAnchor: ClassVar["type[QGraphicsAnchor]"]
    QGraphicsAnchorLayout: ClassVar["type[QGraphicsAnchorLayout]"]
    QGraphicsBlurEffect: ClassVar["type[QGraphicsBlurEffect]"]
    QGraphicsColorizeEffect: ClassVar["type[QGraphicsColorizeEffect]"]
    QGraphicsDropShadowEffect: ClassVar["type[QGraphicsDropShadowEffect]"]
    QGraphicsEffect: ClassVar["type[QGraphicsEffect]"]
    QGraphicsEllipseItem: ClassVar["type[QGraphicsEllipseItem]"]
    QGraphicsGridLayout: ClassVar["type[QGraphicsGridLayout]"]
    QGraphicsItem: ClassVar["type[QGraphicsItem]"]
    QGraphicsItemGroup: ClassVar["type[QGraphicsItemGroup]"]
    QGraphicsLayout: ClassVar["type[QGraphicsLayout]"]
    QGraphicsLayoutItem: ClassVar["type[QGraphicsLayoutItem]"]
    QGraphicsLinearLayout: ClassVar["type[QGraphicsLinearLayout]"]
    QGraphicsLineItem: ClassVar["type[QGraphicsLineItem]"]
    QGraphicsObject: ClassVar["type[QGraphicsObject]"]
    QGraphicsOpacityEffect: ClassVar["type[QGraphicsOpacityEffect]"]
    QGraphicsPathItem: ClassVar["type[QGraphicsPathItem]"]
    QGraphicsPixmapItem: ClassVar["type[QGraphicsPixmapItem]"]
    QGraphicsPolygonItem: ClassVar["type[QGraphicsPolygonItem]"]
    QGraphicsProxyWidget: ClassVar["type[QGraphicsProxyWidget]"]
    QGraphicsRectItem: ClassVar["type[QGraphicsRectItem]"]
    QGraphicsRotation: ClassVar["type[QGraphicsRotation]"]
    QGraphicsScale: ClassVar["type[QGraphicsScale]"]
    QGraphicsScene: ClassVar["type[QGraphicsScene]"]
    QGraphicsSceneContextMenuEvent: ClassVar["type[QGraphicsSceneContextMenuEvent]"]
    QGraphicsSceneDragDropEvent: ClassVar["type[QGraphicsSceneDragDropEvent]"]
    QGraphicsSceneEvent: ClassVar["type[QGraphicsSceneEvent]"]
    QGraphicsSceneHelpEvent: ClassVar["type[QGraphicsSceneHelpEvent]"]
    QGraphicsSceneHoverEvent: ClassVar["type[QGraphicsSceneHoverEvent]"]
    QGraphicsSceneMouseEvent: ClassVar["type[QGraphicsSceneMouseEvent]"]
    QGraphicsSceneMoveEvent: ClassVar["type[QGraphicsSceneMoveEvent]"]
    QGraphicsSceneResizeEvent: ClassVar["type[QGraphicsSceneResizeEvent]"]
    QGraphicsSceneWheelEvent: ClassVar["type[QGraphicsSceneWheelEvent]"]
    QGraphicsSimpleTextItem: ClassVar["type[QGraphicsSimpleTextItem]"]
    QGraphicsTextItem: ClassVar["type[QGraphicsTextItem]"]
    QGraphicsTransform: ClassVar["type[QGraphicsTransform]"]
    QGraphicsView: ClassVar["type[QGraphicsView]"]
    QGraphicsWidget: ClassVar["type[QGraphicsWidget]"]
    QGridLayout: ClassVar["type[QGridLayout]"]
    QGroupBox: ClassVar["type[QGroupBox]"]
    QHBoxLayout: ClassVar["type[QHBoxLayout]"]
    QHeaderView: ClassVar["type[QHeaderView]"]
    QInputDialog: ClassVar["type[QInputDialog]"]
    QItemDelegate: ClassVar["type[QItemDelegate]"]
    QItemEditorCreatorBase: ClassVar["type[QItemEditorCreatorBase]"]
    QItemEditorFactory: ClassVar["type[QItemEditorFactory]"]
    QKeySequenceEdit: ClassVar["type[QKeySequenceEdit]"]
    QLabel: ClassVar["type[QLabel]"]
    QLayout: ClassVar["type[QLayout]"]
    QLayoutItem: ClassVar["type[QLayoutItem]"]
    QLCDNumber: ClassVar["type[QLCDNumber]"]
    QLineEdit: ClassVar["type[QLineEdit]"]
    QListView: ClassVar["type[QListView]"]
    QListWidget: ClassVar["type[QListWidget]"]
    QListWidgetItem: ClassVar["type[QListWidgetItem]"]
    QMainWindow: ClassVar["type[QMainWindow]"]
    QMdiArea: ClassVar["type[QMdiArea]"]
    QMdiSubWindow: ClassVar["type[QMdiSubWindow]"]
    QMenu: ClassVar["type[QMenu]"]
    QMenuBar: ClassVar["type[QMenuBar]"]
    QMessageBox: ClassVar["type[QMessageBox]"]
    QPanGesture: ClassVar["type[QPanGesture]"]
    QPinchGesture: ClassVar["type[QPinchGesture]"]
    QPlainTextDocumentLayout: ClassVar["type[QPlainTextDocumentLayout]"]
    QPlainTextEdit: ClassVar["type[QPlainTextEdit]"]
    QProgressBar: ClassVar["type[QProgressBar]"]
    QProgressDialog: ClassVar["type[QProgressDialog]"]
    QProxyStyle: ClassVar["type[QProxyStyle]"]
    QPushButton: ClassVar["type[QPushButton]"]
    QRadioButton: ClassVar["type[QRadioButton]"]
    QRubberBand: ClassVar["type[QRubberBand]"]
    QScrollArea: ClassVar["type[QScrollArea]"]
    QScrollBar: ClassVar["type[QScrollBar]"]
    QScroller: ClassVar["type[QScroller]"]
    QScrollerProperties: ClassVar["type[QScrollerProperties]"]
    QSizeGrip: ClassVar["type[QSizeGrip]"]
    QSizePolicy: ClassVar["type[QSizePolicy]"]
    QSlider: ClassVar["type[QSlider]"]
    QSpacerItem: ClassVar["type[QSpacerItem]"]
    QSpinBox: ClassVar["type[QSpinBox]"]
    QSplashScreen: ClassVar["type[QSplashScreen]"]
    QSplitter: ClassVar["type[QSplitter]"]
    QSplitterHandle: ClassVar["type[QSplitterHandle]"]
    QStackedLayout: ClassVar["type[QStackedLayout]"]
    QStackedWidget: ClassVar["type[QStackedWidget]"]
    QStatusBar: ClassVar["type[QStatusBar]"]
    QStyle: ClassVar["type[QStyle]"]
    QStyledItemDelegate: ClassVar["type[QStyledItemDelegate]"]
    QStyleFactory: ClassVar["type[QStyleFactory]"]
    QStyleHintReturn: ClassVar["type[QStyleHintReturn]"]
    QStyleHintReturnMask: ClassVar["type[QStyleHintReturnMask]"]
    QStyleHintReturnVariant: ClassVar["type[QStyleHintReturnVariant]"]
    QStyleOption: ClassVar["type[QStyleOption]"]
    QStyleOptionButton: ClassVar["type[QStyleOptionButton]"]
    QStyleOptionComboBox: ClassVar["type[QStyleOptionComboBox]"]
    QStyleOptionComplex: ClassVar["type[QStyleOptionComplex]"]
    QStyleOptionDockWidget: ClassVar["type[QStyleOptionDockWidget]"]
    QStyleOptionFocusRect: ClassVar["type[QStyleOptionFocusRect]"]
    QStyleOptionFrame: ClassVar["type[QStyleOptionFrame]"]
    QStyleOptionGraphicsItem: ClassVar["type[QStyleOptionGraphicsItem]"]
    QStyleOptionGroupBox: ClassVar["type[QStyleOptionGroupBox]"]
    QStyleOptionHeader: ClassVar["type[QStyleOptionHeader]"]
    QStyleOptionHeaderV2: ClassVar["type[QStyleOptionHeaderV2]"]
    QStyleOptionMenuItem: ClassVar["type[QStyleOptionMenuItem]"]
    QStyleOptionProgressBar: ClassVar["type[QStyleOptionProgressBar]"]
    QStyleOptionRubberBand: ClassVar["type[QStyleOptionRubberBand]"]
    QStyleOptionSizeGrip: ClassVar["type[QStyleOptionSizeGrip]"]
    QStyleOptionSlider: ClassVar["type[QStyleOptionSlider]"]
    QStyleOptionSpinBox: ClassVar["type[QStyleOptionSpinBox]"]
    QStyleOptionTab: ClassVar["type[QStyleOptionTab]"]
    QStyleOptionTabBarBase: ClassVar["type[QStyleOptionTabBarBase]"]
    QStyleOptionTabWidgetFrame: ClassVar["type[QStyleOptionTabWidgetFrame]"]
    QStyleOptionTitleBar: ClassVar["type[QStyleOptionTitleBar]"]
    QStyleOptionToolBar: ClassVar["type[QStyleOptionToolBar]"]
    QStyleOptionToolBox: ClassVar["type[QStyleOptionToolBox]"]
    QStyleOptionToolButton: ClassVar["type[QStyleOptionToolButton]"]
    QStyleOptionViewItem: ClassVar["type[QStyleOptionViewItem]"]
    QStylePainter: ClassVar["type[QStylePainter]"]
    QSwipeGesture: ClassVar["type[QSwipeGesture]"]
    QSystemTrayIcon: ClassVar["type[QSystemTrayIcon]"]
    QTabBar: ClassVar["type[QTabBar]"]
    QTableView: ClassVar["type[QTableView]"]
    QTableWidget: ClassVar["type[QTableWidget]"]
    QTableWidgetItem: ClassVar["type[QTableWidgetItem]"]
    QTableWidgetSelectionRange: ClassVar["type[QTableWidgetSelectionRange]"]
    QTabWidget: ClassVar["type[QTabWidget]"]
    QTapAndHoldGesture: ClassVar["type[QTapAndHoldGesture]"]
    QTapGesture: ClassVar["type[QTapGesture]"]
    QTextBrowser: ClassVar["type[QTextBrowser]"]
    QTextEdit: ClassVar["type[QTextEdit]"]
    QTimeEdit: ClassVar["type[QTimeEdit]"]
    QToolBar: ClassVar["type[QToolBar]"]
    QToolBox: ClassVar["type[QToolBox]"]
    QToolButton: ClassVar["type[QToolButton]"]
    QToolTip: ClassVar["type[QToolTip]"]
    QTreeView: ClassVar["type[QTreeView]"]
    QTreeWidget: ClassVar["type[QTreeWidget]"]
    QTreeWidgetItem: ClassVar["type[QTreeWidgetItem]"]
    QTreeWidgetItemIterator: ClassVar["type[QTreeWidgetItemIterator]"]
    QUndoView: ClassVar["type[QUndoView]"]
    QVBoxLayout: ClassVar["type[QVBoxLayout]"]
    QWhatsThis: ClassVar["type[QWhatsThis]"]
    QWidget: ClassVar["type[QWidget]"]
    QWidgetAction: ClassVar["type[QWidgetAction]"]
    QWidgetItem: ClassVar["type[QWidgetItem]"]
    QWizard: ClassVar["type[QWizard]"]
    QWizardPage: ClassVar["type[QWizardPage]"]
