# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

### Added

- Detection of system theme (light or dark mode).
- Support for PySide2 and PySide6 frameworks (from [Inverted-E]).
- Support for flat groupboxes.
- Advanced Docking System styling.
- Examples for title bars, standard icon overrides, LCD displays, and more.
- Configurable stylesheets via themes.
- Custom extension support, such as the advanced docking system.
- Compile Qt resource files (from [chaosink]).
- Documented support for CMake builds (from [ruilvo]).
- Add additional alternate themes for common styles (from [Inverted-E]).
- Add additional a red theme (from [Inverted-E]).
- Compress resource files by default.

### Changed

- Stylesheets to match KDE-like Breeze and Breeze dark themes.
- Icons to match KDE-like Breeze and Breeze dark themes.
- Make `dark` and `light` aliases for `dark-blue` and `light-blue`, respectively.

### Deprecated

### Removed

- Old PyQt6 packaging system to match the standard Qt5 and Qt6 approach using resource compilers (from [Inverted-E]).
- The `--no-qrc` flag when configuring stylesheets due to the new RCC system (from [Inverted-E]).
- The QRC dist files due to the new RCC system (from [Inverted-E]).

### Fixed

- Documentation for CMake installation.
- QTableWidget::indicator size to match other checkboxes (from [Inverted-E]).
- Menu bar hover styling.
- Qt6 support.
- Branch indicators for QTreeView and QTreeWidget (from [eblade]).

<!-- Unused Sections -->
<!-- ### Security -->

<!-- Initial release

## [0.0.1] - 2024-09-08

- Initial release
-->

<!-- Links -->
[Keep A Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html

<!-- Versions -->
[Unreleased]: https://github.com/Author/Repository/compare/v0.0.2...HEAD
<!-- [0.0.1]: https://github.com/Author/Repository/releases/tag/v0.0.1 -->

<!-- Contributors -->
[Inverted-E]: https://github.com/Inverted-E/
[eblade]: https://github.com/eblade/
[chaosink]: https://github.com/chaosink/
[ruilvo]: https://github.com/ruilvo/
