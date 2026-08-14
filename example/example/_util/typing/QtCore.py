# pyright: reportNoOverloadImplementation=false
"""Type definitions for QtCore consistent with PyQt6."""

from typing import ClassVar

from PyQt6.QtCore import (
    QAbstractAnimation,
    QAbstractEventDispatcher,
    QAbstractItemModel,
    QAbstractListModel,
    QAbstractNativeEventFilter,
    QAbstractProxyModel,
    QAbstractTableModel,
    QAnimationGroup,
    QBasicTimer,
    QBitArray,
    QBluetoothPermission,
    QBuffer,
    QByteArray,
    QByteArrayMatcher,
    QCalendar,
    QCalendarPermission,
    QCameraPermission,
    QCborError,
    QCborKnownTags,
    QCborSimpleType,
    QCborStreamReader,
    QCborStreamWriter,
    QChildEvent,
    QCollator,
    QCollatorSortKey,
    QCommandLineOption,
    QCommandLineParser,
    QConcatenateTablesProxyModel,
    QContactsPermission,
    QCoreApplication,
    QCryptographicHash,
    QDataStream,
    QDate,
    QDateTime,
    QDeadlineTimer,
    QDir,
    QDirIterator,
    QDynamicPropertyChangeEvent,
    QEasingCurve,
    QElapsedTimer,
    QEvent,
    QEventLoop,
    QEventLoopLocker,
    QFile,
    QFileDevice,
    QFileInfo,
    QFileSelector,
    QFileSystemWatcher,
    QGenericArgument,
    QGenericReturnArgument,
    QIdentityProxyModel,
    QIODevice,
    QIODeviceBase,
    QItemSelection,
    QItemSelectionModel,
    QItemSelectionRange,
    QJsonDocument,
    QJsonParseError,
    QJsonValue,
    QKeyCombination,
    QLibrary,
    QLibraryInfo,
    QLine,
    QLineF,
    QLocale,
    QLocationPermission,
    QLockFile,
    QLoggingCategory,
    QMargins,
    QMarginsF,
    QMessageAuthenticationCode,
    QMessageLogContext,
    QMessageLogger,
    QMetaClassInfo,
    QMetaEnum,
    QMetaMethod,
    QMetaObject,
    QMetaProperty,
    QMetaType,
    QMicrophonePermission,
    QMimeData,
    QMimeDatabase,
    QMimeType,
    QModelIndex,
    QModelRoleData,
    QModelRoleDataSpan,
    QMutex,
    QMutexLocker,
    QNativeIpcKey,
    QObject,
    QObjectCleanupHandler,
    QOperatingSystemVersion,
    QOperatingSystemVersionBase,
    QParallelAnimationGroup,
    QPauseAnimation,
    QPermission,
    QPersistentModelIndex,
    QPluginLoader,
    QPoint,
    QPointF,
    QProcess,
    QProcessEnvironment,
    QPropertyAnimation,
    QRandomGenerator,
    QReadLocker,
    QReadWriteLock,
    QRect,
    QRectF,
    QRecursiveMutex,
    QRegularExpression,
    QRegularExpressionMatch,
    QRegularExpressionMatchIterator,
    QResource,
    QRunnable,
    QSaveFile,
    QSemaphore,
    QSemaphoreReleaser,
    QSequentialAnimationGroup,
    QSettings,
    QSharedMemory,
    QSignalBlocker,
    QSignalMapper,
    QSize,
    QSizeF,
    QSocketNotifier,
    QSortFilterProxyModel,
    QStandardPaths,
    QStorageInfo,
    QStringConverter,
    QStringConverterBase,
    QStringDecoder,
    QStringEncoder,
    QStringListModel,
    QSysInfo,
    QSystemSemaphore,
    Qt,
    QTemporaryDir,
    QTemporaryFile,
    QTextBoundaryFinder,
    QTextStream,
    QTextStreamManipulator,
    QThread,
    QThreadPool,
    QTime,
    QTimeLine,
    QTimer,
    QTimerEvent,
    QTimeZone,
    QTranslator,
    QTransposeProxyModel,
    QTypeRevision,
    QUrl,
    QUrlQuery,
    QUuid,
    QVariant,
    QVariantAnimation,
    QVersionNumber,
    QWaitCondition,
    QWinEventNotifier,
    QWriteLocker,
    QXmlStreamAttribute,
    QXmlStreamAttributes,
    QXmlStreamEntityDeclaration,
    QXmlStreamEntityResolver,
    QXmlStreamNamespaceDeclaration,
    QXmlStreamNotationDeclaration,
    QXmlStreamReader,
    QXmlStreamWriter,
)

__all__ = [
    "_QtCore",
    "QAbstractAnimation",
    "QAbstractEventDispatcher",
    "QAbstractItemModel",
    "QAbstractListModel",
    "QAbstractNativeEventFilter",
    "QAbstractProxyModel",
    "QAbstractTableModel",
    "QAnimationGroup",
    "QBasicTimer",
    "QBitArray",
    "QBluetoothPermission",
    "QBuffer",
    "QByteArray",
    "QByteArrayMatcher",
    "QCalendar",
    "QCalendarPermission",
    "QCameraPermission",
    "QCborError",
    "QCborKnownTags",
    "QCborSimpleType",
    "QCborStreamReader",
    "QCborStreamWriter",
    "QChildEvent",
    "QCollator",
    "QCollatorSortKey",
    "QCommandLineOption",
    "QCommandLineParser",
    "QConcatenateTablesProxyModel",
    "QContactsPermission",
    "QCoreApplication",
    "QCryptographicHash",
    "QDataStream",
    "QDate",
    "QDateTime",
    "QDeadlineTimer",
    "QDir",
    "QDirIterator",
    "QDynamicPropertyChangeEvent",
    "QEasingCurve",
    "QElapsedTimer",
    "QEvent",
    "QEventLoop",
    "QEventLoopLocker",
    "QFile",
    "QFileDevice",
    "QFileInfo",
    "QFileSelector",
    "QFileSystemWatcher",
    "QGenericArgument",
    "QGenericReturnArgument",
    "QIdentityProxyModel",
    "QIODevice",
    "QIODeviceBase",
    "QItemSelection",
    "QItemSelectionModel",
    "QItemSelectionRange",
    "QJsonDocument",
    "QJsonParseError",
    "QJsonValue",
    "QKeyCombination",
    "QLibrary",
    "QLibraryInfo",
    "QLine",
    "QLineF",
    "QLocale",
    "QLocationPermission",
    "QLockFile",
    "QLoggingCategory",
    "QMargins",
    "QMarginsF",
    "QMessageAuthenticationCode",
    "QMessageLogContext",
    "QMessageLogger",
    "QMetaClassInfo",
    "QMetaEnum",
    "QMetaMethod",
    "QMetaObject",
    "QMetaProperty",
    "QMetaType",
    "QMicrophonePermission",
    "QMimeData",
    "QMimeDatabase",
    "QMimeType",
    "QModelIndex",
    "QModelRoleData",
    "QModelRoleDataSpan",
    "QMutex",
    "QMutexLocker",
    "QNativeIpcKey",
    "QObject",
    "QObjectCleanupHandler",
    "QOperatingSystemVersion",
    "QOperatingSystemVersionBase",
    "QParallelAnimationGroup",
    "QPauseAnimation",
    "QPermission",
    "QPersistentModelIndex",
    "QPluginLoader",
    "QPoint",
    "QPointF",
    "QProcess",
    "QProcessEnvironment",
    "QPropertyAnimation",
    "QRandomGenerator",
    "QReadLocker",
    "QReadWriteLock",
    "QRect",
    "QRectF",
    "QRecursiveMutex",
    "QRegularExpression",
    "QRegularExpressionMatch",
    "QRegularExpressionMatchIterator",
    "QResource",
    "QRunnable",
    "QSaveFile",
    "QSemaphore",
    "QSemaphoreReleaser",
    "QSequentialAnimationGroup",
    "QSettings",
    "QSharedMemory",
    "QSignalBlocker",
    "QSignalMapper",
    "QSize",
    "QSizeF",
    "QSocketNotifier",
    "QSortFilterProxyModel",
    "QStandardPaths",
    "QStorageInfo",
    "QStringConverter",
    "QStringConverterBase",
    "QStringDecoder",
    "QStringEncoder",
    "QStringListModel",
    "QSysInfo",
    "QSystemSemaphore",
    "Qt",
    "QTemporaryDir",
    "QTemporaryFile",
    "QTextBoundaryFinder",
    "QTextStream",
    "QTextStreamManipulator",
    "QThread",
    "QThreadPool",
    "QTime",
    "QTimeLine",
    "QTimer",
    "QTimerEvent",
    "QTimeZone",
    "QTranslator",
    "QTransposeProxyModel",
    "QTypeRevision",
    "QUrl",
    "QUrlQuery",
    "QUuid",
    "QVariant",
    "QVariantAnimation",
    "QVersionNumber",
    "QWaitCondition",
    "QWinEventNotifier",
    "QWriteLocker",
    "QXmlStreamAttribute",
    "QXmlStreamAttributes",
    "QXmlStreamEntityDeclaration",
    "QXmlStreamEntityResolver",
    "QXmlStreamNamespaceDeclaration",
    "QXmlStreamNotationDeclaration",
    "QXmlStreamReader",
    "QXmlStreamWriter",
]


class _QtCore:
    """Namespace-like wrapper for our static type checkers."""

    QAbstractAnimation: ClassVar["type[QAbstractAnimation]"]
    QAbstractEventDispatcher: ClassVar["type[QAbstractEventDispatcher]"]
    QAbstractItemModel: ClassVar["type[QAbstractItemModel]"]
    QAbstractListModel: ClassVar["type[QAbstractListModel]"]
    QAbstractNativeEventFilter: ClassVar["type[QAbstractNativeEventFilter]"]
    QAbstractProxyModel: ClassVar["type[QAbstractProxyModel]"]
    QAbstractTableModel: ClassVar["type[QAbstractTableModel]"]
    QAnimationGroup: ClassVar["type[QAnimationGroup]"]
    QBasicTimer: ClassVar["type[QBasicTimer]"]
    QBitArray: ClassVar["type[QBitArray]"]
    QBluetoothPermission: ClassVar["type[QBluetoothPermission]"]
    QBuffer: ClassVar["type[QBuffer]"]
    QByteArray: ClassVar["type[QByteArray]"]
    QByteArrayMatcher: ClassVar["type[QByteArrayMatcher]"]
    QCalendar: ClassVar["type[QCalendar]"]
    QCalendarPermission: ClassVar["type[QCalendarPermission]"]
    QCameraPermission: ClassVar["type[QCameraPermission]"]
    QCborError: ClassVar["type[QCborError]"]
    QCborKnownTags: ClassVar["type[QCborKnownTags]"]
    QCborSimpleType: ClassVar["type[QCborSimpleType]"]
    QCborStreamReader: ClassVar["type[QCborStreamReader]"]
    QCborStreamWriter: ClassVar["type[QCborStreamWriter]"]
    QChildEvent: ClassVar["type[QChildEvent]"]
    QCollator: ClassVar["type[QCollator]"]
    QCollatorSortKey: ClassVar["type[QCollatorSortKey]"]
    QCommandLineOption: ClassVar["type[QCommandLineOption]"]
    QCommandLineParser: ClassVar["type[QCommandLineParser]"]
    QConcatenateTablesProxyModel: ClassVar["type[QConcatenateTablesProxyModel]"]
    QContactsPermission: ClassVar["type[QContactsPermission]"]
    QCoreApplication: ClassVar["type[QCoreApplication]"]
    QCryptographicHash: ClassVar["type[QCryptographicHash]"]
    QDataStream: ClassVar["type[QDataStream]"]
    QDate: ClassVar["type[QDate]"]
    QDateTime: ClassVar["type[QDateTime]"]
    QDeadlineTimer: ClassVar["type[QDeadlineTimer]"]
    QDir: ClassVar["type[QDir]"]
    QDirIterator: ClassVar["type[QDirIterator]"]
    QDynamicPropertyChangeEvent: ClassVar["type[QDynamicPropertyChangeEvent]"]
    QEasingCurve: ClassVar["type[QEasingCurve]"]
    QElapsedTimer: ClassVar["type[QElapsedTimer]"]
    QEvent: ClassVar["type[QEvent]"]
    QEventLoop: ClassVar["type[QEventLoop]"]
    QEventLoopLocker: ClassVar["type[QEventLoopLocker]"]
    QFile: ClassVar["type[QFile]"]
    QFileDevice: ClassVar["type[QFileDevice]"]
    QFileInfo: ClassVar["type[QFileInfo]"]
    QFileSelector: ClassVar["type[QFileSelector]"]
    QFileSystemWatcher: ClassVar["type[QFileSystemWatcher]"]
    QGenericArgument: ClassVar["type[QGenericArgument]"]
    QGenericReturnArgument: ClassVar["type[QGenericReturnArgument]"]
    QIdentityProxyModel: ClassVar["type[QIdentityProxyModel]"]
    QIODevice: ClassVar["type[QIODevice]"]
    QIODeviceBase: ClassVar["type[QIODeviceBase]"]
    QItemSelection: ClassVar["type[QItemSelection]"]
    QItemSelectionModel: ClassVar["type[QItemSelectionModel]"]
    QItemSelectionRange: ClassVar["type[QItemSelectionRange]"]
    QJsonDocument: ClassVar["type[QJsonDocument]"]
    QJsonParseError: ClassVar["type[QJsonParseError]"]
    QJsonValue: ClassVar["type[QJsonValue]"]
    QKeyCombination: ClassVar["type[QKeyCombination]"]
    QLibrary: ClassVar["type[QLibrary]"]
    QLibraryInfo: ClassVar["type[QLibraryInfo]"]
    QLine: ClassVar["type[QLine]"]
    QLineF: ClassVar["type[QLineF]"]
    QLocale: ClassVar["type[QLocale]"]
    QLocationPermission: ClassVar["type[QLocationPermission]"]
    QLockFile: ClassVar["type[QLockFile]"]
    QLoggingCategory: ClassVar["type[QLoggingCategory]"]
    QMargins: ClassVar["type[QMargins]"]
    QMarginsF: ClassVar["type[QMarginsF]"]
    QMessageAuthenticationCode: ClassVar["type[QMessageAuthenticationCode]"]
    QMessageLogContext: ClassVar["type[QMessageLogContext]"]
    QMessageLogger: ClassVar["type[QMessageLogger]"]
    QMetaClassInfo: ClassVar["type[QMetaClassInfo]"]
    QMetaEnum: ClassVar["type[QMetaEnum]"]
    QMetaMethod: ClassVar["type[QMetaMethod]"]
    QMetaObject: ClassVar["type[QMetaObject]"]
    QMetaProperty: ClassVar["type[QMetaProperty]"]
    QMetaType: ClassVar["type[QMetaType]"]
    QMicrophonePermission: ClassVar["type[QMicrophonePermission]"]
    QMimeData: ClassVar["type[QMimeData]"]
    QMimeDatabase: ClassVar["type[QMimeDatabase]"]
    QMimeType: ClassVar["type[QMimeType]"]
    QModelIndex: ClassVar["type[QModelIndex]"]
    QModelRoleData: ClassVar["type[QModelRoleData]"]
    QModelRoleDataSpan: ClassVar["type[QModelRoleDataSpan]"]
    QMutex: ClassVar["type[QMutex]"]
    QMutexLocker: ClassVar["type[QMutexLocker]"]
    QNativeIpcKey: ClassVar["type[QNativeIpcKey]"]
    QObject: ClassVar["type[QObject]"]
    QObjectCleanupHandler: ClassVar["type[QObjectCleanupHandler]"]
    QOperatingSystemVersion: ClassVar["type[QOperatingSystemVersion]"]
    QOperatingSystemVersionBase: ClassVar["type[QOperatingSystemVersionBase]"]
    QParallelAnimationGroup: ClassVar["type[QParallelAnimationGroup]"]
    QPauseAnimation: ClassVar["type[QPauseAnimation]"]
    QPermission: ClassVar["type[QPermission]"]
    QPersistentModelIndex: ClassVar["type[QPersistentModelIndex]"]
    QPluginLoader: ClassVar["type[QPluginLoader]"]
    QPoint: ClassVar["type[QPoint]"]
    QPointF: ClassVar["type[QPointF]"]
    QProcess: ClassVar["type[QProcess]"]
    QProcessEnvironment: ClassVar["type[QProcessEnvironment]"]
    QPropertyAnimation: ClassVar["type[QPropertyAnimation]"]
    QRandomGenerator: ClassVar["type[QRandomGenerator]"]
    QReadLocker: ClassVar["type[QReadLocker]"]
    QReadWriteLock: ClassVar["type[QReadWriteLock]"]
    QRect: ClassVar["type[QRect]"]
    QRectF: ClassVar["type[QRectF]"]
    QRecursiveMutex: ClassVar["type[QRecursiveMutex]"]
    QRegularExpression: ClassVar["type[QRegularExpression]"]
    QRegularExpressionMatch: ClassVar["type[QRegularExpressionMatch]"]
    QRegularExpressionMatchIterator: ClassVar["type[QRegularExpressionMatchIterator]"]
    QResource: ClassVar["type[QResource]"]
    QRunnable: ClassVar["type[QRunnable]"]
    QSaveFile: ClassVar["type[QSaveFile]"]
    QSemaphore: ClassVar["type[QSemaphore]"]
    QSemaphoreReleaser: ClassVar["type[QSemaphoreReleaser]"]
    QSequentialAnimationGroup: ClassVar["type[QSequentialAnimationGroup]"]
    QSettings: ClassVar["type[QSettings]"]
    QSharedMemory: ClassVar["type[QSharedMemory]"]
    QSignalBlocker: ClassVar["type[QSignalBlocker]"]
    QSignalMapper: ClassVar["type[QSignalMapper]"]
    QSize: ClassVar["type[QSize]"]
    QSizeF: ClassVar["type[QSizeF]"]
    QSocketNotifier: ClassVar["type[QSocketNotifier]"]
    QSortFilterProxyModel: ClassVar["type[QSortFilterProxyModel]"]
    QStandardPaths: ClassVar["type[QStandardPaths]"]
    QStorageInfo: ClassVar["type[QStorageInfo]"]
    QStringConverter: ClassVar["type[QStringConverter]"]
    QStringConverterBase: ClassVar["type[QStringConverterBase]"]
    QStringDecoder: ClassVar["type[QStringDecoder]"]
    QStringEncoder: ClassVar["type[QStringEncoder]"]
    QStringListModel: ClassVar["type[QStringListModel]"]
    QSysInfo: ClassVar["type[QSysInfo]"]
    QSystemSemaphore: ClassVar["type[QSystemSemaphore]"]
    Qt: ClassVar["type[Qt]"]
    QTemporaryDir: ClassVar["type[QTemporaryDir]"]
    QTemporaryFile: ClassVar["type[QTemporaryFile]"]
    QTextBoundaryFinder: ClassVar["type[QTextBoundaryFinder]"]
    QTextStream: ClassVar["type[QTextStream]"]
    QTextStreamManipulator: ClassVar["type[QTextStreamManipulator]"]
    QThread: ClassVar["type[QThread]"]
    QThreadPool: ClassVar["type[QThreadPool]"]
    QTime: ClassVar["type[QTime]"]
    QTimeLine: ClassVar["type[QTimeLine]"]
    QTimer: ClassVar["type[QTimer]"]
    QTimerEvent: ClassVar["type[QTimerEvent]"]
    QTimeZone: ClassVar["type[QTimeZone]"]
    QTranslator: ClassVar["type[QTranslator]"]
    QTransposeProxyModel: ClassVar["type[QTransposeProxyModel]"]
    QTypeRevision: ClassVar["type[QTypeRevision]"]
    QUrl: ClassVar["type[QUrl]"]
    QUrlQuery: ClassVar["type[QUrlQuery]"]
    QUuid: ClassVar["type[QUuid]"]
    QVariant: ClassVar["type[QVariant]"]
    QVariantAnimation: ClassVar["type[QVariantAnimation]"]
    QVersionNumber: ClassVar["type[QVersionNumber]"]
    QWaitCondition: ClassVar["type[QWaitCondition]"]
    QWinEventNotifier: ClassVar["type[QWinEventNotifier]"]
    QWriteLocker: ClassVar["type[QWriteLocker]"]
    QXmlStreamAttribute: ClassVar["type[QXmlStreamAttribute]"]
    QXmlStreamAttributes: ClassVar["type[QXmlStreamAttributes]"]
    QXmlStreamEntityDeclaration: ClassVar["type[QXmlStreamEntityDeclaration]"]
    QXmlStreamEntityResolver: ClassVar["type[QXmlStreamEntityResolver]"]
    QXmlStreamNamespaceDeclaration: ClassVar["type[QXmlStreamNamespaceDeclaration]"]
    QXmlStreamNotationDeclaration: ClassVar["type[QXmlStreamNotationDeclaration]"]
    QXmlStreamReader: ClassVar["type[QXmlStreamReader]"]
    QXmlStreamWriter: ClassVar["type[QXmlStreamWriter]"]
