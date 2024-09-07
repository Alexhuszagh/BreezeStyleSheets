/**
 *  breeze_theme
 *  ============
 *
 *  Determine if the system theme is light or dark, supporting many platforms.
 *
 *  This code has been minimally tested but should be useful on most platforms.
 *  This makes extensive use of C++17 features. On Windows, this requires adding
 *  `OleAut32.lib` and `Advapi32.lib` to the linker.
 *
 *  This currently supports:
 *  - Windows
 *  - Linux
 *
 *  Enhancements for macOS would be greatly appreciated.
 *
 *  This is subject to the following license terms:
 *
 *  darkdetect
 *  ==========
 *  https://github.com/albertosottile/darkdetect
 *
 *  Copyright (c) 2019, Alberto Sottile
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *      * Redistributions of source code must retain the above copyright
 *      notice, this list of conditions and the following disclaimer.
 *      * Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *      * Neither the name of "darkdetect" nor the
 *      names of its contributors may be used to endorse or promote products
 *      derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 *  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 *  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *  DISCLAIMED. IN NO EVENT SHALL "Alberto Sottile" BE LIABLE FOR ANY
 *  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 *  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 *  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 *  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 *  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *  Python
 *  ======
 *  https://docs.python.org/3/license.html
 *
 *  1. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and
 *     the Individual or Organization ("Licensee") accessing and otherwise using Python
 *     3.12.5 software in source or binary form and its associated documentation.
 *
 *  2. Subject to the terms and conditions of this License Agreement, PSF hereby
 *     grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
 *     analyze, test, perform and/or display publicly, prepare derivative works,
 *     distribute, and otherwise use Python 3.12.5 alone or in any derivative
 *     version, provided, however, that PSF's License Agreement and PSF's notice of
 *     copyright, i.e., "Copyright © 2001-2023 Python Software Foundation; All Rights
 *     Reserved" are retained in Python 3.12.5 alone or in any derivative version
 *     prepared by Licensee.
 *
 *  3. In the event Licensee prepares a derivative work that is based on or
 *     incorporates Python 3.12.5 or any part thereof, and wants to make the
 *     derivative work available to others as provided herein, then Licensee hereby
 *     agrees to include in any such work a brief summary of the changes made to Python
 *     3.12.5.
 *
 *  4. PSF is making Python 3.12.5 available to Licensee on an "AS IS" basis.
 *     PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED.  BY WAY OF
 *     EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND DISCLAIMS ANY REPRESENTATION OR
 *     WARRANTY OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE
 *     USE OF PYTHON 3.12.5 WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.
 *
 *  5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON 3.12.5
 *     FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS A RESULT OF
 *     MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON 3.12.5, OR ANY DERIVATIVE
 *     THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
 *
 *  6. This License Agreement will automatically terminate upon a material breach of
 *     its terms and conditions.
 *
 *  7. Nothing in this License Agreement shall be deemed to create any relationship
 *     of agency, partnership, or joint venture between PSF and Licensee.  This License
 *     Agreement does not grant permission to use PSF trademarks or trade name in a
 *     trademark sense to endorse or promote products or services of Licensee, or any
 *     third party.
 *
 *  8. By copying, installing or otherwise using Python 3.12.5, Licensee agrees
 *     to be bound by the terms and conditions of this License Agreement.
 */

#pragma once

#include <algorithm>
#include <array>
#include <cstdio>
#include <cstdint>
#include <filesystem>
#include <iostream>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

#if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)
#   include <Windows.h>
#   include <winrt/Windows.UI.ViewManagement.h>
#elif __APPLE__ || __linux__
#   include <sys/types.h>
#   include <sys/stat.h>
#   include <unistd.h>
#endif

namespace breeze_stylesheets
{
    // we need a lot of optional strings
    using _optstring = ::std::optional<::std::string>;

    /// @brief An enumeration of valid values for a theme
    enum class theme : int32_t
    {
        dark = 0,
        light = 1,
        unknown = 2,
    };

    /// @brief Determine if the color is bright as a quick estimate.
    /// @param r The red value, from [0, 255].
    /// @param g The green value, from [0, 255].
    /// @param b The blue value, from [0, 255].
    /// @return If the color is perceived as light.
    inline bool
    is_light_color(int r, int g, int b)
    {
        return (((5 * g) + (2 * r) + b) > (8 * 128));
    }

    /// @brief Split a string by a given delimiter.
    /// @param value The string to split.
    /// @param delimiter The delimiter to split on.
    /// @return The split string.
    inline ::std::vector<::std::string>
    _split(::std::string value, char delimiter)
    {
        ::std::vector<::std::string> result;
        ::std::size_t start = 0;
        auto end = value.find(delimiter);
        while (end != ::std::string::npos)
        {
            result.emplace_back(value.substr(start, end - start));
            start = end + 1;
            end = value.find(delimiter, start);
        }

        return result;
    }

    /// @brief Convert a string to lowercase, ASCII only (works for ASCII-extended scripts like UTF-8).
    /// @param c The character to transform.
    /// @return The character transformed to lowercase.
    inline char
    _to_ascii_lowercase(char c)
    {
        return (c <= 'Z' && c >= 'A') ? c - ('Z' - 'z') : c;
    }

    #if __APPLE__ || __linux__

    /// @brief Determine if the file is an executable.
    /// @param path The full path to the file.
    /// @return If the file at the path is an executable.
    inline bool
    _is_executable_file(const ::std::string &path)
    {
        struct stat sb;
        return (stat(path.c_str(), &sb) == 0) && S_ISREG(sb.st_mode) && (access(path.c_str(), X_OK) == 0);
    }

    /// @brief Determine if an executable exists along the path and return it if it does.
    ///
    /// POSIX-like operating systems don't have to worry about registered extensions like
    /// Windows does.
    ///
    /// @param name The basename of the executable to look for.
    /// @return The full path to the executable, if it exists.
    inline _optstring
    _which(const ::std::string &name)
    {
        // get our environment path, if it doesn't exist, force it on the path
        char const *const c_path = getenv("PATH");
        const ::std::string path = c_path != nullptr ? c_path : "";
        if (path.empty())
        {
            if (_is_executable_file(name))
            {
                ::std::filesystem::path full_path = name;
                return ::std::filesystem::absolute(full_path).string();
            }
            else
                return ::std::nullopt;
        }

        // have a path, split our entries and go from there
        const char pathsep = ':';
        auto paths = _split(path, pathsep);
        for (auto const &path : paths)
        {
            ::std::filesystem::path directory = path;
            auto full_path = directory / name;
            if (_is_executable_file(full_path.string()))
                return ::std::filesystem::absolute(full_path).string();
        }

        return ::std::nullopt;
    }

    /// @brief Run a given command and return the output.
    /// @param cmd The commands to run.
    /// @return The output from the command.
    ::std::tuple<_optstring, int>
    _run_command(const ::std::string &cmd)
    {
        const ::std::size_t buffer_size = 1024;
        ::std::array<char, buffer_size> buffer;
        ::std::string result;

        auto pipe = ::popen(cmd.c_str(), "r");
        if (!pipe)
            throw ::std::runtime_error("popen() failed!");
        try
        {
            while (::fgets(buffer.data(), static_cast<int>(buffer.size()), pipe) != nullptr)
            {
                result += buffer.data();
            }
            auto code = ::pclose(pipe);
            return ::std::make_tuple(result, code);
        }
        catch(...)
        {
            auto code = ::pclose(pipe);
            return ::std::make_tuple(::std::nullopt, code);
        }
    }

    #endif

    #if defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)

    using UISettings = winrt::Windows::UI::ViewManagement::UISettings;
    using UIColorType = winrt::Windows::UI::ViewManagement::UIColorType;

    // major, minor, build, platform, SP major, SP minor
    using _winversion = ::std::tuple<int32_t, int32_t, int32_t, int32_t, int32_t, int32_t>;

    /// @brief Get the error message from a code.
    /// @param code The error code, optionally from `GetLastError`.
    /// @return The descriptive message of the error code.
    inline _optstring
    _get_error(LSTATUS code)
    {
        if (code == ERROR_SUCCESS)
            return ::std::nullopt;

        LPSTR buffer = nullptr;
        auto flags = FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS;
        auto lang = MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT);
        ::std::size_t size = FormatMessageA(flags, nullptr, code, lang, reinterpret_cast<LPSTR>(&buffer), 0, nullptr);

        ::std::string message(buffer, size);
        LocalFree(buffer);
        return message;
    }

    /// @brief Get a DWORD registry key value.
    /// @param key The registry HKEY location.
    /// @param name The name of the registry value.
    /// @return The value of the registry key.
    inline DWORD
    _get_dword_key(HKEY key, const ::std::wstring &name)
    {
        DWORD size(sizeof(DWORD));
        DWORD result(0);
        auto code = ::RegQueryValueExW(key, name.c_str(), 0, nullptr, reinterpret_cast<LPBYTE>(&result), &size);
        if (code == ERROR_SUCCESS)
            return result;
        throw new ::std::runtime_error(_get_error(code).value());
    }

    /// @brief Get a string registry key value.
    /// @param key The registry HKEY location.
    /// @param name The name of the registry value.
    /// @return The value of the registry key.
    inline ::std::wstring
    _get_string_key(HKEY key, const ::std::wstring &name)
    {
        WCHAR buffer[512];
        DWORD size(sizeof(buffer));
        auto code = ::RegQueryValueExW(key, name.c_str(), 0, nullptr, reinterpret_cast<LPBYTE>(buffer), &size);
        if (code == ERROR_SUCCESS)
            return ::std::wstring(buffer);
        throw new ::std::runtime_error(_get_error(code).value());
    }

    /// @brief Open an HKEY from an initial starting point.
    /// @param initial The initial HKEY, such as HKEY_LOCAL_MACHINE.
    /// @param path The path relative to that HKEY, such as L"Software\\Microsoft".
    /// @return The opened hkey.
    inline HKEY
    _open_hkey(HKEY initial, const ::std::wstring& path)
    {
        HKEY key;
        auto code = ::RegOpenKeyExW(initial, path.c_str(), 0, KEY_READ, &key);
        if (code != EXIT_SUCCESS)
            throw new ::std::runtime_error(_get_error(code).value());
        return key;
    }

    // NOTE: Windows support is based off of:
    //  https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/ui/apply-windows-themes#know-when-dark-mode-is-enabled
    //
    // This requires linking against `Advapi32`.

    /// @brief Return info about the running version of Windows as a named tuple.
    ///
    /// The members are named: major, minor, build, platform, service_pack,
    /// service_pack_major, service_pack_minor, suite_mask, product_type and
    /// platform_version. For backward compatibility, only the first 5 items
    /// are available by indexing. All elements are numbers, except
    /// service_pack and platform_type which are strings, and platform_version
    /// which is a 3-tuple. Platform is always 2. Product_type may be 1 for a
    /// workstation, 2 for a domain controller, 3 for a server.
    /// Platform_version is a 3-tuple containing a version number that is
    /// intended for identifying the OS rather than feature detection.
    /// [clinic start generated code]*/
    ///
    /// This is taken from CPython's implementation.
    ///
    /// @return The windows version a multi-item tuple.
    inline _winversion
    _get_winversion()
    {
        // NOTE: We can't use `GetVersionExW` because this will depend on a manifest,
        // which could return 6 or 10 depending on the scenario for the major version
        // which is exactly what we **DON'T** want. We also cannot use `GetFileVersionInfoSizeExW`
        // for a library version since the build versions will differ **slightly**. Nor
        // do we want to require access to the Windows Desktop Kit for `RtlGetVersion`, so
        // the simplest solution is just to use the registry.
        HKEY current = _open_hkey(HKEY_LOCAL_MACHINE, L"Software\\Microsoft\\Windows NT\\CurrentVersion");
        HKEY platform = _open_hkey(HKEY_LOCAL_MACHINE, L"HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0");
        auto major = _get_dword_key(current, L"CurrentMajorVersionNumber");
        auto minor = _get_dword_key(current, L"CurrentMinorVersionNumber");
        auto build = _get_string_key(current, L"CurrentBuildNumber");
        auto platformId = _get_dword_key(platform, L"Platform Specific Field 1");

        // NOTE: We ignore the service pack information.
        return ::std::make_tuple(
            int32_t(major),
            int32_t(minor),
            std::stoi(build),
            int32_t(platformId),
            int32_t(0),
            int32_t(0)
        );
    }

    /// @brief Get the current system theme. This requires Windows 10+.
    /// @return The type of the system theme.
    inline ::breeze_stylesheets::theme
    get_theme()
    {
        try
        {
            HKEY key;
            auto personalize = L"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize";
            auto code = RegOpenKeyExW(HKEY_CURRENT_USER, personalize, 0, KEY_READ, &key);
            if (code != EXIT_SUCCESS)
                throw new ::std::runtime_error(_get_error(code).value());
            auto use_light = _get_dword_key(key, L"AppsUseLightTheme");
            return static_cast<::breeze_stylesheets::theme>(use_light);
        }
        catch(...)
        {
            /**
             * some headless Windows instances (e.g. GitHub Actions or Docker images) do not have this key
             * this is also not present if the user has never set the value. however, more recent Windows
             * installs will have this, starting at `10.0.10240.0`:
             *   https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/ui/apply-windows-themes#know-when-dark-mode-is-enabled
             *
             * Note that the documentation is inverted: if the foreground is light, we are using DARK mode.
             */
            auto winver = _get_winversion();
            _winversion min_version = ::std::make_tuple(10, 0, 10240, 0, 0, 0);
            if (winver < min_version)
                return theme::unknown;

            auto settings = UISettings();
            auto foreground = settings.GetColorValue(UIColorType::Foreground);
            // NOTE: a light foreground means a dark theme
            auto light_foreground = is_light_color(foreground.R, foreground.G, foreground.B);
            return light_foreground ? ::breeze_stylesheets::theme::dark : ::breeze_stylesheets::theme::light;
        }
    }

    #elif __APPLE__
    #   error "macOS not yet supported."
    #elif __linux__

    /// @brief Get the current system theme. This requires Windows 10+.
    /// @return The type of the system theme.
    inline ::breeze_stylesheets::theme
    get_theme()
    {
        if (!_which("gsettings").has_value())
            throw new ::std::runtime_error("Cannot find gsettings...");

        // using the freedesktop specifications for checking dark mode
        // this will return something like `prefer - dark`, which is the true value.
        // valid values are 'default', 'prefer-dark', 'prefer-light'.
        const ::std::string command = "gsettings get org.gnome.desktop.interface ";
        auto result = ::breeze_stylesheets::_run_command(command + "color-scheme");
        if (::std::get<1>(result) != EXIT_SUCCESS)
        {
            // NOTE: We always assume this is due to invalid key, which might not be true
            // since we don't check if gsettings exists first.
            // if not found then trying older gtk-theme method
            // this relies on the theme not lying to you : if the theme is dark, it ends in `- dark`.
            result = ::breeze_stylesheets::_run_command(command + "gtk-theme");
        }

        auto stdout = ::std::get<0>(result);
        if (::std::get<1>(result) != EXIT_SUCCESS || !stdout.has_value())
            throw new ::std::runtime_error("Unable to get response for the current system theme.");

        auto value = stdout.value();
        ::std::transform(value.begin(), value.end(), value.begin(), _to_ascii_lowercase);
        auto is_dark = value.find("-dark") != ::std::string::npos;
        return is_dark ? ::breeze_stylesheets::theme::dark : ::breeze_stylesheets::theme::light;
    }

    #else
    #   error "Have an unknown target platform: only Windows, macOS, and Linux are supported."
    #endif

    /// @brief Get if the current theme is a dark color.
    /// @return If the current theme is a dark color.
    inline bool
    is_dark()
    {
        return ::breeze_stylesheets::get_theme() == ::breeze_stylesheets::theme::dark;
    }

    /// @brief Get if the current theme is a light color.
    /// @return If the current theme is a light color.
    inline bool
    is_light()
    {
        return ::breeze_stylesheets::get_theme() == ::breeze_stylesheets::theme::light;
    }
}
