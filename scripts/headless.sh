#!/usr/bin/env bash
# shellcheck disable=SC2086,2068
#
# Run each configure for all supported frameworks, and store them in `dist/ci`.
#
# This requires the correct frameworks to be installed:
#   - PyQt5
#   - PyQt6
#   - PySide6
#
# And if using Python 3.10 or earlier:
#   - PySide2
#
# On Ubuntu, this requires the following install logic:
#
#   ```bash
#   python -m pip install --upgrade pip
#   pip install PySide2 PySide6 PyQt5 PyQt6
#   sudo apt-get update
#   sudo apt-get install xvfb
#   sudo apt-get install build-essential libgl1-mesa-dev libgstreamer-gl1.0-0 libpulse-dev \
#       libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
#       libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 \
#       libxcb-xinerama0 libxcb1 libxkbcommon-dev libxkbcommon-x11-0 libxcb-xkb-dev
#   ```

set -eux pipefail

SCRIPTS_HOME="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJECT_HOME="$(dirname "${SCRIPTS_HOME}")"
mkdir -p "${PROJECT_HOME}/dist/ci"
cd "${PROJECT_HOME}"

# we xcb installed for our headless running, so exit if we don't have it
if ! hash xvfb-run &>/dev/null; then
    >&2 echo "Do not have xvfb installed..."
    exit 1
fi

# pop them into dist since it's ignored anyway
if [ -z "${PYTHON+x}" ]; then
    PYTHON=python
fi
FRAMEWORKS=()
HAVE_PYQT5=$(${PYTHON} -c 'import importlib.util; print(importlib.util.find_spec("PyQt5") is not None)')
if [[ "${HAVE_PYQT5}" == "True" ]]; then
    FRAMEWORKS+=("pyqt5")
fi
HAVE_PYQT6=$(${PYTHON} -c 'import importlib.util; print(importlib.util.find_spec("PyQt6") is not None)')
if [[ "${HAVE_PYQT6}" == "True" ]]; then
    FRAMEWORKS+=("pyqt6")
fi
HAVE_PYSIDE2=$(${PYTHON} -c 'import importlib.util; print(importlib.util.find_spec("PySide2") is not None)')
if [[ "${HAVE_PYSIDE2}" == "True" ]]; then
    FRAMEWORKS+=("pyside2")
fi
HAVE_PYSIDE6=$(${PYTHON} -c 'import importlib.util; print(importlib.util.find_spec("PySide6") is not None)')
if [[ "${HAVE_PYSIDE6}" == "True" ]]; then
    FRAMEWORKS+=("pyside6")
fi

if [ ${#FRAMEWORKS[@]} -eq 0 ]; then
    >&2 echo "Unable to find any installed Python Qt frameworks..."
    exit 1
fi


# need to run everything in headless mode.
# note: our shared libraries can be run without issues
export QT_QPA_PLATFORM=offscreen
export PYTHONPATH="$(realpath example):$(realpath .)"
for script in example/example/*/__main__.py; do
    if [[ "${script}" == *"/ads/"* ]]; then
        continue
    fi
    for framework in "${FRAMEWORKS[@]}"; do
        echo "Running '${script}' for framework '${framework}'."
        xvfb-run -a "${PYTHON}" "${script}" --qt-framework "${framework}" --stylesheet dark
    done
done

# ensure that our styles compressed properly
# if they didn't, Qt could segfault on initialization
# if a style doesn't exist, it simply won't be read
# which is fine
export QT_QPA_PLATFORM=offscreen
STYLES=("dark-red" "dark-blue" "dark-purple" "dark-green" "light-red" "light-blue" "light-purple" "light-green")
for framework in "${FRAMEWORKS[@]}"; do
    for style in "${STYLES[@]}"; do
        echo "Running widgets test for framework '${framework}' an style '${style}'."
        xvfb-run -a "${PYTHON}" "example/example/widgets/__main__.py" --qt-framework "${framework}" --stylesheet "${style}"
    done
done

# now we need to run our tests
# NOTE: We run each test separately just because it simplifies the logic.
# Some tests don't work in headless mode so we skip them.
export PYTHONPATH="${PYTHONPATH}:$(realpath example/test)"
widgets=$(${PYTHON} -c "import os; os.chdir('example/test'); import ui; print(' '.join([i[5:] for i in dir(ui) if i.startswith('test_')]))")
for widget in ${widgets[@]}; do
    for framework in "${FRAMEWORKS[@]}"; do
        echo "Running test for widget '${widget}' for framework '${framework}'."
        xvfb-run -a "${PYTHON}" example/test/ui.py --widget "${widget}" --qt-framework "${framework}" --stylesheet dark
    done
done
