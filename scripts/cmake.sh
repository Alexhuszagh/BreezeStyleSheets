#!/usr/bin/env bash
#
# Run custom CMake build script which auto-downloads,
# builds, and then uses the compiled code in an application.
#
#   ```bash
#   sudo apt-get update
#   sudo apt-get install xvfb
#   sudo apt-get install build-essential libgl1-mesa-dev libgstreamer-gl1.0-0 libpulse-dev \
#       libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
#       libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 \
#       libxcb-xinerama0 libxcb1 libxkbcommon-dev libxkbcommon-x11-0 libxcb-xkb-dev cmake
#   sudo apt install qt6-base-dev qtbase5-dev libqt5svg5-dev qt6-svg-dev
#   ```

set -eux pipefail

SCRIPTS_HOME="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJECT_HOME="$(dirname "${SCRIPTS_HOME}")"
BUILD_DIR="${PROJECT_HOME}/dist/build"

mkdir -p "${BUILD_DIR}/"{qt5,qt6}

# we xcb installed for our headless running, so exit if we don't have it
if ! hash xvfb-run &>/dev/null; then
    >&2 echo "Do not have xvfb installed..."
fi

# first, try Qt5
# NOTE: Since we're using `-e`, we need to specially
# capture the error code immediately.
export QT_QPA_PLATFORM=offscreen
cd "${BUILD_DIR}/qt5"
cmake "${PROJECT_HOME}/example/cpp/cmake" -D QT_VERSION=Qt5
make -j
if hash xvfb-run &>/dev/null; then
    timeout 1 xvfb-run -a ./testing || error_code=$?
    if [[ "${error_code}" != 124 ]]; then
        exit "${error_code}"
    fi
fi

# first, try Qt6
cd "${BUILD_DIR}/qt6"
cmake "${PROJECT_HOME}/example/cpp/cmake" -D QT_VERSION=Qt6
make -j
if hash xvfb-run &>/dev/null; then
    timeout 1 xvfb-run -a ./testing || error_code=$?
    if [[ "${error_code}" != 124 ]]; then
        exit "${error_code}"
    fi
fi
