#!/usr/bin/env bash
#
# Use scripts to check if the theme determination works.

set -eux pipefail

ci_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${ci_home}")"
cd "${project_home}/example"

if [[ ! -v PYTHON ]]; then
    PYTHON=python
fi
theme=$("${PYTHON}" -c "import breeze_theme; print(breeze_theme.get_theme())")
if [[ "${theme}" != Theme.* ]]; then
    >&2 echo "Unable to get the correct theme."
    exit 1
fi
"${PYTHON}" -c "import breeze_theme; print(breeze_theme.is_light())"
"${PYTHON}" -c "import breeze_theme; print(breeze_theme.is_dark())"
