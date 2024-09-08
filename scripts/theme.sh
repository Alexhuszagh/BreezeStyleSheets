#!/usr/bin/env bash
#
# Use scripts to check if the theme determination works.

set -eux pipefail

scripts_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${scripts_home}")"
cd "${project_home}/example/detect"
# shellcheck source=/dev/null
. "${scripts_home}/../shared.sh"

if ! is-set PYTHON; then
    PYTHON=python
fi
# Check the import first, then calling the function for easier debugging.
${PYTHON} -c "import system_theme"
theme=$(${PYTHON} -c "import system_theme; print(system_theme.get_theme())")
if [[ "${theme}" != Theme.* ]]; then
    >&2 echo "Unable to get the correct theme."
    exit 1
fi
${PYTHON} -c "import system_theme; print(system_theme.is_light())"
${PYTHON} -c "import system_theme; print(system_theme.is_dark())"
