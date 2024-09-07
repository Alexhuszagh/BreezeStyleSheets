#!/usr/bin/env bash
# shellcheck disable=SC2086,2068
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

# we xcb installed for our headless running, so exit if we don't have it
if ! hash xvfb-run &>/dev/null; then
    >&2 echo "Do not have xvfb installed..."
    exit 1
fi

# pop them into dist since it's ignored anyway
if ! is-set PYTHON; then
    PYTHON=python
fi
frameworks=("pyqt5" "pyqt6" "pyside6")
have_pyside=$(${PYTHON} -c 'import sys; print(sys.version_info < (3, 11))')
if [[ "${have_pyside}" == "True" ]]; then
    frameworks+=("pyside2")
fi

# need to run everything in headless mode.
# note: our shared libraries can be run without issues
export QT_QPA_PLATFORM=offscreen
for script in example/*.py; do
    if [[ "${script}" == "example/advanced-dock.py" ]]; then
        continue
    fi
    for framework in "${frameworks[@]}"; do
        echo "Running '${script}' for framework '${framework}'."
        xvfb-run -a "${PYTHON}" "${script}" --qt-framework "${framework}"
    done
done

# now we need to run our tests
# NOTE: We run each test separately just because it simplifies the logic.
# Some tests don't work in headless mode so we skip them.
widgets=$(${PYTHON} -c "import os; os.chdir('test'); import ui; print(' '.join([i[5:] for i in dir(ui) if i.startswith('test_')]))")
for widget in ${widgets[@]}; do
    for framework in "${frameworks[@]}"; do
        echo "Running test for widget '${widget}' for framework '${framework}'."
        xvfb-run -a "${PYTHON}" test/ui.py --widget "${widget}" --qt-framework "${framework}"
    done
done
