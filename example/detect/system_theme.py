'''
    system_theme
    ============

    Get the current system them information. This is adapted from darkdetect
    and is subject to the license terms below:
        https://github.com/albertosottile/darkdetect

    The files have been modified to be merged into a single file. This is
    distributed under a 3-clause BSD license. On Windows, the fallback
    path for the theme detection requires the `winrt-Windows.UI.ViewManagement`
    and `winrt-Windows.UI` libraries installed.

    darkdetect
    ==========
    https://github.com/albertosottile/darkdetect

    Copyright (c) 2019, Alberto Sottile
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
        * Neither the name of "darkdetect" nor the
        names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL "Alberto Sottile" BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# pylint: disable=import-error,no-member

import typing
import ctypes
import ctypes.util
import enum
import os
import platform
import shutil
import signal
import subprocess
import sys
from pathlib import Path

CallbackFn: typing.TypeAlias = typing.Callable[['Theme'], None]
ThemeFn: typing.TypeAlias = typing.Callable[[], 'Theme']
ListenerFn: typing.TypeAlias = typing.Callable[[CallbackFn], None]


class Theme(enum.IntEnum):
    '''The list of valid themes.'''

    DARK = 0
    LIGHT = 1
    UNKNOWN = 2

    @staticmethod
    def from_string(value: str | None) -> 'Theme':
        '''Initialize the enumeration from value.'''

        # NOTE: This is for Py3.10 and earlier support.
        if value is None or not value:
            return Theme.UNKNOWN
        value = value.lower()
        if value == 'dark':
            return Theme.DARK
        if value == 'light':
            return Theme.LIGHT
        raise ValueError(f'Got an invalid theme value of "{value}".')

    def to_string(self) -> str:
        '''Serialize the theme to string.'''

        # NOTE: This is for Py3.10 and earlier support.
        if self == Theme.DARK:
            return 'Dark'
        if self == Theme.LIGHT:
            return 'Light'
        if self == Theme.UNKNOWN:
            return 'Unknown'
        raise ValueError(f'Got an invalid theme value of "{self}".')


def is_light_color(r: int, g: int, b: int) -> bool:
    '''
    Determine if the color is bright as a quick estimate from RGB.

    Args:
        r: The red value, from [0, 255].
        g: The green value, from [0, 255].
        b: The blue value, from [0, 255].

    Returns:
        If the color is perceived as light.
    '''
    return ((5 * g) + (2 * r) + b) > (8 * 128)


# region windows


def _get_theme_windows() -> Theme:
    '''Get the current theme, as light or dark, for the system on Windows.'''

    from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx  # pyright: ignore[reportAttributeAccessIssue]

    # In HKEY_CURRENT_USER, get the Personalisation Key.
    try:
        key = OpenKey(HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize')
        # In the Personalisation Key, get the AppsUseLightTheme subkey. This returns a tuple.
        # The first item in the tuple is the result we want (0 or 1 indicating Dark Mode or Light Mode); the
        # other value is the type of subkey e.g. DWORD, QWORD, String, etc.
        use_light = QueryValueEx(key, 'AppsUseLightTheme')[0]
    except FileNotFoundError:
        # some headless Windows instances (e.g. GitHub Actions or Docker images) do not have this key
        # this is also not present if the user has never set the value. however, more recent Windows
        # installs will have this, starting at `10.0.10240.0`:
        #   https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/ui/apply-windows-themes#know-when-dark-mode-is-enabled  # noqa  # pylint: disable=line-too-long
        #
        # Note that the documentation is inverted: if the foreground is light, we are using DARK mode.
        winver = sys.getwindowsversion()  # pyright: ignore[reportAttributeAccessIssue]
        if winver[:4] < (10, 0, 10240, 0):
            return Theme.UNKNOWN
        try:
            # NOTE: This only works if we have the `winrt-Windows.UI.ViewManagement`
            # and `winrt-Windows.UI` dependencies installed.
            from winrt.windows.ui import viewmanagement  # pyright: ignore[reportMissingImports]

            settings = viewmanagement.UISettings()
            foreground = settings.get_color_value(viewmanagement.UIColorType.FOREGROUND)
            use_light = int(not is_light_color(foreground.r, foreground.g, foreground.b))
        except Exception:
            return Theme.UNKNOWN

    if use_light == 0:
        return Theme.DARK
    if use_light == 1:
        return Theme.LIGHT
    return Theme.UNKNOWN


def _listener_windows(callback: CallbackFn) -> None:
    '''Register an event listener for dark/light theme changes.'''

    import ctypes.wintypes  # pyright: ignore[reportMissingImports]  # pylint: disable=redefined-outer-name

    global _advapi32

    if _advapi32 is None:
        _advapi32 = _initialize_advapi32()
    advapi32 = _advapi32
    assert advapi32 is not None

    hkey = ctypes.wintypes.HKEY()
    advapi32.RegOpenKeyExA(
        ctypes.wintypes.HKEY(0x80000001),  # HKEY_CURRENT_USER
        ctypes.wintypes.LPCSTR(b'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize'),
        ctypes.wintypes.DWORD(),
        ctypes.wintypes.DWORD(0x00020019),  # KEY_READ
        ctypes.byref(hkey),
    )

    size = ctypes.wintypes.DWORD(ctypes.sizeof(ctypes.wintypes.DWORD))
    query_last_value = ctypes.wintypes.DWORD()
    query_value = ctypes.wintypes.DWORD()
    advapi32.RegQueryValueExA(
        hkey,
        ctypes.wintypes.LPCSTR(b'AppsUseLightTheme'),
        ctypes.wintypes.LPDWORD(),
        ctypes.wintypes.LPDWORD(),
        ctypes.cast(ctypes.byref(query_last_value), ctypes.wintypes.LPBYTE),
        ctypes.byref(size),
    )

    while True:
        advapi32.RegNotifyChangeKeyValue(
            hkey,
            ctypes.wintypes.BOOL(True),
            ctypes.wintypes.DWORD(0x00000004),  # REG_NOTIFY_CHANGE_LAST_SET
            ctypes.wintypes.HANDLE(None),
            ctypes.wintypes.BOOL(False),
        )
        advapi32.RegQueryValueExA(
            hkey,
            ctypes.wintypes.LPCSTR(b'AppsUseLightTheme'),
            ctypes.wintypes.LPDWORD(),
            ctypes.wintypes.LPDWORD(),
            ctypes.cast(ctypes.byref(query_value), ctypes.wintypes.LPBYTE),
            ctypes.byref(size),
        )
        if query_last_value.value != query_value.value:
            query_last_value.value = query_value.value
            callback(Theme.LIGHT if query_value.value else Theme.DARK)


def _initialize_advapi32() -> ctypes.CDLL:
    '''Initialize our advapi32 library.'''

    import ctypes.wintypes  # pyright: ignore[reportMissingImports]  # pylint: disable=redefined-outer-name

    advapi32 = ctypes.windll.advapi32  # pyright: ignore[reportAttributeAccessIssue]

    # LSTATUS RegOpenKeyExA(
    #     HKEY hKey,
    #     LPCSTR lpSubKey,
    #     DWORD ulOptions,
    #     REGSAM samDesired,
    #     PHKEY phkResult
    # );
    advapi32.RegOpenKeyExA.argtypes = (
        ctypes.wintypes.HKEY,
        ctypes.wintypes.LPCSTR,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.DWORD,
        ctypes.POINTER(ctypes.wintypes.HKEY),
    )
    advapi32.RegOpenKeyExA.restype = ctypes.wintypes.LONG

    # LSTATUS RegQueryValueExA(
    #     HKEY hKey,
    #     LPCSTR lpValueName,
    #     LPDWORD lpReserved,
    #     LPDWORD lpType,
    #     LPBYTE lpData,
    #     LPDWORD lpcbData
    # );
    advapi32.RegQueryValueExA.argtypes = (
        ctypes.wintypes.HKEY,
        ctypes.wintypes.LPCSTR,
        ctypes.wintypes.LPDWORD,
        ctypes.wintypes.LPDWORD,
        ctypes.wintypes.LPBYTE,
        ctypes.wintypes.LPDWORD,
    )
    advapi32.RegQueryValueExA.restype = ctypes.wintypes.LONG

    # LSTATUS RegNotifyChangeKeyValue(
    #     HKEY hKey,
    #     WINBOOL bWatchSubtree,
    #     DWORD dwNotifyFilter,
    #     HANDLE hEvent,
    #     WINBOOL fAsynchronous
    # );
    advapi32.RegNotifyChangeKeyValue.argtypes = (
        ctypes.wintypes.HKEY,
        ctypes.wintypes.BOOL,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.BOOL,
    )
    advapi32.RegNotifyChangeKeyValue.restype = ctypes.wintypes.LONG

    return advapi32


_advapi32: typing.Optional['ctypes.CDLL'] = None

# endregion

# region macos


def _macos_supported_version() -> bool:
    '''Determine if we use a support macOS version.'''

    # NOTE: This is typically 10.14.2 or 12.3
    sysver = platform.mac_ver()[0]
    major = int(sysver.split('.')[0])
    if major < 10:
        return False
    if major >= 11:
        return True

    # have a macOS10 version
    minor = int(sysver.split('.')[1])
    return minor >= 14


def _get_theme_macos() -> Theme:
    '''Get the current theme, as light or dark, for the system on macOS.'''

    # old macOS versions were always light
    if not _macos_supported_version():
        return Theme.LIGHT

    # NOTE: This can segfault on M1 and M2 Macs on Big Sur 11.4+. So, we also
    # try reading directly using subprocess. Specifically, it's documented that
    # if dark mode is set, this command returns `Dark`, otherwise it returns
    # that the key pair doesn't exist.
    try:
        command = ['defaults', 'read', '-globalDomain', 'AppleInterfaceStyle']
        process = subprocess.run(command, capture_output=True, check=True)
        try:
            result = process.stdout.decode('utf-8').strip()
            return Theme.DARK if result == 'Dark' else Theme.LIGHT
        except UnicodeDecodeError:
            return Theme.LIGHT
    except subprocess.CalledProcessError as error:
        # If this keypair does not exist, then it's a specific error because the style
        # hasn't been set before, so then it specifically is a light theme. this can
        # affect no-UI systems like CI.
        not_exist = b'does not exist' in error.stderr
        any_app = b'kCFPreferencesAnyApplication' in error.stderr
        interface_style = b'AppleInterfaceStyle' in error.stderr
        if not_exist and any_app and interface_style:
            return Theme.LIGHT

    # NOTE: We do this so we don't need imports at the global level.
    try:
        # macOS Big Sur+ use "a built-in dynamic linker cache of all system-provided libraries"
        objc = ctypes.cdll.LoadLibrary('libobjc.dylib')
    except OSError:
        # revert to full path for older OS versions and hardened programs
        obc_name = ctypes.util.find_library('objc')
        assert obc_name is not None
        objc = ctypes.cdll.LoadLibrary(obc_name)

    # See https://docs.python.org/3/library/ctypes.html#function-prototypes for arguments description
    msg_prototype = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
    msg = msg_prototype(('objc_msgSend', objc), ((1, '', None), (1, '', None), (1, '', None)))
    auto_release_pool = _get_class(objc, 'NSAutoreleasePool')
    user_defaults = _get_class(objc, 'NSUserDefaults')
    ns_string = _get_class(objc, 'NSString')

    pool = msg(auto_release_pool, _register_name(objc, 'alloc'))
    pool = msg(pool, _register_name(objc, 'init'))
    std_user_defaults = msg(user_defaults, _register_name(objc, 'standardUserDefaults'))

    key = msg(ns_string, _register_name(objc, "stringWithUTF8String:"), _as_utf8('AppleInterfaceStyle'))
    appearance_ns = msg(std_user_defaults, _register_name(objc, 'stringForKey:'), ctypes.c_void_p(key))
    appearance_c = msg(appearance_ns, _register_name(objc, 'UTF8String'))

    out = ctypes.string_at(appearance_c) if appearance_c is not None else None
    msg(pool, _register_name(objc, 'release'))

    return Theme.from_string(out.decode('utf-8')) if out is not None else Theme.LIGHT


def _as_utf8(value: bytes | str) -> bytes:
    '''Encode a value to UTF-8'''
    return value if isinstance(value, bytes) else value.encode('utf-8')


def _register_name(objc: ctypes.CDLL, name: bytes | str) -> None:
    '''Register a name within our DLLs.'''
    return objc.sel_registerName(_as_utf8(name))


def _get_class(objc: ctypes.CDLL, name: bytes | str) -> 'ctypes._NamedFuncPointer':
    '''Get a class by the registered name.'''
    return objc.objc_getClass(_as_utf8(name))


def _listener_macos(callback: CallbackFn) -> None:
    '''Register an event listener for dark/light theme changes.'''

    try:
        from Foundation import (  # noqa # pyright: ignore[reportMissingImports] # pylint: disable
            NSKeyValueObservingOptionNew as _,
        )
    except (ImportError, ModuleNotFoundError) as error:
        raise RuntimeError('Missing the required Foundation modules: cannot listen.') from error

    # now need to register a child event
    path = Path(__file__)
    command = [sys.executable, '-c', f'import {path.stem} as theme; theme._listen_child_macos()']
    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        cwd=path.parent,
    ) as process:
        for line in typing.cast(str, process.stdout):
            callback(Theme.from_string(line.strip()))


def _listen_child_macos() -> None:
    '''Create a confole event loop listing the macOS events.'''

    # NOTE: We do this so we don't need imports at the global level.
    try:
        from Foundation import (  # pyright: ignore[reportMissingImports]
            NSKeyValueChangeNewKey,
            NSKeyValueObservingOptionNew,
            NSObject,
            NSUserDefaults,
        )
        from PyObjCTools import AppHelper  # pyright: ignore[reportMissingImports]
    except ModuleNotFoundError as error:
        raise RuntimeError('Missing the required Foundation modules: cannot listen.') from error

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    class Observer(NSObject):
        '''Custom namespace key observer.'''

        def observeValueForKeyPath_ofObject_change_context_(  # pylint: disable=invalid-name
            self, path, obj, changeDescription, context
        ):
            '''Observe our key to detect the light/dark status.'''
            _ = path
            _ = obj
            _ = context
            result = changeDescription[NSKeyValueChangeNewKey]
            try:
                value = 'Light' if result is None else result
                print(value, flush=True)
            except IOError:
                os._exit(1)

    # keep a reference alive after installing
    observer = Observer.new()
    defaults = NSUserDefaults.standardUserDefaults()
    defaults.addObserver_forKeyPath_options_context_(
        observer,
        'AppleInterfaceStyle',
        NSKeyValueObservingOptionNew,
        0,
    )

    AppHelper.runConsoleEventLoop()


# endregion

# region linux


def _get_theme_linux() -> Theme:
    '''Get the current theme, as light or dark, for the system on Linux OSes.'''

    try:
        _, stdout = _get_gsettings_schema()
    except Exception:
        return Theme.LIGHT

    # we have a string, now remove start and end quote
    value = stdout.lower().strip()[1:-1]
    return Theme.DARK if '-dark' in value.lower() else Theme.LIGHT


def _listener_linux(callback: CallbackFn) -> None:
    '''Register an event listener for dark/light theme changes.'''

    gsettings = _get_gsettings()
    schema, _ = _get_gsettings_schema()
    command = [gsettings, 'monitor', 'org.gnome.desktop.interface', schema]
    # this has rhe same restrictions as above
    with subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True) as process:
        for line in typing.cast(str, process.stdout):
            value = line.removeprefix(f"{schema}: '").removesuffix("'")
            callback(Theme.DARK if '-dark' in value.lower() else Theme.LIGHT)


def _get_gsettings_schema() -> tuple[str, str]:
    '''Get the schema to use when monitoring via gsettings.'''
    # This follows the gsettings followed here:
    #   https://github.com/GNOME/gsettings-desktop-schemas/blob/master/schemas/org.gnome.desktop.interface.gschema.xml.in  # noqa  # pylint: disable=line-too-long

    gsettings = _get_gsettings()
    command = [gsettings, 'get', 'org.gnome.desktop.interface']
    # using the freedesktop specifications for checking dark mode
    # this will return something like `prefer-dark`, which is the true value.
    #   valid values are 'default', 'prefer-dark', 'prefer-light'.
    process = subprocess.run(command + ['color-scheme'], capture_output=True, check=False)
    if process.returncode == 0:
        return ('color-scheme', process.stdout.decode('utf-8'))
    if b'No such key' not in process.stderr:
        raise RuntimeError('Unable to get our color-scheme from our gsettings.')

    # if not found then trying older gtk-theme method
    # this relies on the theme not lying to you: if the theme is dark, it ends in `-dark`.
    process = subprocess.run(command + ['gtk-theme'], capture_output=True, check=True)
    return ('gtk-theme', process.stdout.decode('utf-8'))


def _get_gsettings() -> str:
    '''Get the gsettings tool to determine the theme color.'''

    # NOTE: gsettings means GNU, it is desktop-environment generic.

    global _gsettings

    if _gsettings is None:
        _gsettings = shutil.which('gsettings')
    if _gsettings is None:
        raise RuntimeError('Unable to find gsettings to determine if dark mode is used.')
    return _gsettings


_gsettings: str | None = None

# endregion

# region dummy


def _get_theme_dummy() -> Theme:
    '''Get the current theme, as light or dark, for the system (always unknown).'''
    return Theme.UNKNOWN


def _listener_dummy(callback: CallbackFn) -> None:
    '''Register an event listener for dark/light theme changes (always unimplemented).'''
    _ = callback


# endregion


def get_theme() -> Theme:
    '''Get the current theme, as light or dark, for the system.'''
    return _get_theme()


def is_dark() -> bool:
    '''Get if the current theme is a dark color.'''
    return get_theme() == Theme.DARK


def is_light() -> bool:
    '''Get if the current theme is a light color.'''
    return get_theme() == Theme.LIGHT


def listener(callback: CallbackFn) -> None:
    '''Register an event listener for dark/light theme changes.'''
    _listener(callback)


def register_functions() -> tuple[ThemeFn, ListenerFn]:
    '''Register our global functions for our themes and listeners.'''

    if sys.platform == 'darwin':
        return (_get_theme_macos, _listener_macos)
    if sys.platform == 'win32' and platform.release().isdigit() and int(platform.release()) >= 10:
        # Checks if running Windows 10 version 10.0.14393 (Anniversary Update) OR HIGHER.
        # The getwindowsversion method returns a tuple. The third item is the build number
        # that we can use to check if the user has a new enough version of Windows.
        winver = int(platform.version().split('.')[2])
        if winver >= 14393:
            return (_get_theme_windows, _listener_windows)
        return (_get_theme_dummy, _listener_dummy)
    if sys.platform == "linux":
        return (_get_theme_linux, _listener_linux)
    return (_get_theme_dummy, _listener_dummy)


# register these callbacks once
_get_theme, _listener = register_functions()
