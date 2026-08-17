#!/usr/bin/env bash
#
# Use scripts to check if the theme determination works.

set -eux pipefail

SCRIPTS_HOME="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJECT_HOME="$(dirname "${SCRIPTS_HOME}")"
cd "${PROJECT_HOME}"

if [ -z "${PYTHON+x}" ]; then
    PYTHON=python
fi
# Check the import first, then calling the function for easier debugging.
${PYTHON} -c "import breezestylesheets"
theme=$(${PYTHON} -c "from breezestylesheets import detect; print(detect.get_theme())")
if [[ ! "${theme}" =~ ^[0-9]+$ ]] && [[ "${theme}" != SystemTheme.* ]]; then
    >&2 echo "Unable to get the correct theme."
    exit 1
fi
${PYTHON} -c "from breezestylesheets import detect; print(detect.is_light())"
${PYTHON} -c "from breezestylesheets import detect; print(detect.is_dark())"
