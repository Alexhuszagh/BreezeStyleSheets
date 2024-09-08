#!/usr/bin/env bash
#
# Run our automatic code formatters.
#
# This requires black and isort to be installed.

set -eux pipefail

scripts_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${scripts_home}")"
cd "${project_home}"
# shellcheck source=/dev/null
. "${scripts_home}/shared.sh"

# unless we manually provide an override, use whatever's
# on the path by default.
if ! is-set PYTHON; then
    isort ./*.py example/*.py example/**/*.py
    black --config pyproject.toml example/ ./*.py
else
    ${PYTHON} -m isort ./*.py example/*.py example/**/*.py
    ${PYTHON} -m black --config pyproject.toml example/ ./*.py
fi
