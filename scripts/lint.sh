#!/usr/bin/env bash
#
# Run our code linters, including type checking.
# Since we have 0 dependencies, we don't use securit checks.

set -eux pipefail

scripts_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${scripts_home}")"
cd "${project_home}"
# shellcheck source=/dev/null
. "${scripts_home}/shared.sh"

# run our python lint checks
# unless we manually provide an override, use whatever's
# on the path by default.
if ! is-set PYTHON; then
    pylint ./*.py example/*.py example/**/*.py
    pyright example/breeze_theme.py
    flake8
else
    ${PYTHON} -m pylint ./*.py example/*.py example/**/*.py
    ${PYTHON} -m pyright example/breeze_theme.py
    ${PYTHON} -m flake8
fi
