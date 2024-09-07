#!/usr/bin/env bash
#
# Run each configure for all supported frameworks, and store them in `dist/ci`.
# This requires the correct frameworks to be installed:
#   - PyQt5
#   - PyQt6
#   - PySide6
# And if using Python 3.10 or earlier:
#   - PySide2

set -eux pipefail

scripts_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${scripts_home}")"
mkdir -p "${project_home}/dist/ci"
cd "${project_home}"
# shellcheck source=/dev/null
. "${scripts_home}/shared.sh"

# pop them into dist since it's ignored anyway
if ! is-set PYTHON; then
    PYTHON=python
fi
frameworks=("pyqt5" "pyqt6" "pyside6")
have_pyside=$(${PYTHON} -c 'import sys; print(sys.version_info < (3, 11))')
if [[ "${have_pyside}" == "True" ]]; then
    frameworks+=("pyside2")
fi

# NOTE: We need to make sure the scripts directory is added to the path
python_home=$(${PYTHON} -c 'import site; print(site.getsitepackages()[0])')
scripts_dir="${python_home}/scripts"
uname_s="$(uname -s)"
if [[ "${uname_s}" == MINGW* ]]; then
    # want to convert C:/... to /c/...
    scripts_dir=$(echo "/$scripts_dir" | sed -e 's/\\/\//g' -e 's/://')
fi
export PATH="${scripts_dir}:${PATH}"
for framework in "${frameworks[@]}"; do
    ${PYTHON} "${project_home}/configure.py" \
        --styles=all \
        --extensions=all \
        --qt-framework "${framework}" \
        --output-dir "${project_home}/dist/ci" \
        --resource "breeze_${framework}.qrc" \
        --compiled-resource "${project_home}/dist/ci/breeze_${framework}.py"
    # this will auto-fail due to pipefail, checks the imports work
    ${PYTHON} -c "import os; os.chdir('dist/ci'); import breeze_${framework}"
done
