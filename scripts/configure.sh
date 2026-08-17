#!/usr/bin/env bash
#
# Run each configure for all supported frameworks, and store them in `dist/ci`.
#
# This requires the correct frameworks to be installed (so we validate the framework
# is installed afterward):
#   - PyQt5
#   - PyQt6
#   - PySide6
#
# And if using Python 3.10 or earlier:
#   - PySide2
#
# Optionally, you can ensure the frameworks are installed using `INSTALLED`.

set -eux pipefail

SCRIPTS_HOME="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJECT_HOME="$(dirname "${SCRIPTS_HOME}")"
mkdir -p "${PROJECT_HOME}/dist/ci"
cd "${PROJECT_HOME}"

# pop them into dist since it's ignored anyway
if [ -z "${PYTHON+x}" ]; then
    PYTHON=python
fi
FRAMEWORKS=("pyqt5" "pyqt6" "pyside6")
HAVE_PYSIDE=$(${PYTHON} -c 'import sys; print(sys.version_info < (3, 11))')
if [[ "${HAVE_PYSIDE}" == "True" ]]; then
    FRAMEWORKS+=("pyside2")
fi

# NOTE: We need to make sure the scripts directory is added to the path
PYTHON_HOME=$(${PYTHON} -c 'import site; print(site.getsitepackages()[0])')
SCRIPTS_DIR="${PYTHON_HOME}/scripts"
UNAME_S="$(uname -s)"
if [[ "${UNAME_S}" == MINGW* ]]; then
    # want to convert C:/... to /c/...
    SCRIPTS_DIR=$(echo "/${SCRIPTS_DIR}" | sed -e 's/\\/\//g' -e 's/://')
fi
export PATH="${SCRIPTS_DIR}:${PATH}"
for framework in "${FRAMEWORKS[@]}"; do
    ${PYTHON} "${PROJECT_HOME}/configure.py" \
        --styles=all \
        --extensions=all \
        --qt-framework "${framework}" \
        --output-dir "${PROJECT_HOME}/dist/ci" \
        --resource "breeze_${framework}.qrc" \
        --compiled-resource "${PROJECT_HOME}/dist/ci/breeze_${framework}.py"
    # this will auto-fail due to pipefail, checks the imports work
    ${PYTHON} -c "import os; os.chdir('dist/ci'); import breeze_${framework}"
done
