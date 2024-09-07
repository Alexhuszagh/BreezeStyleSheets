#!/usr/bin/env bash
#
# Run our code linters, including type checking.
# Since we have 0 dependencies, we don't use securit checks.

set -eux pipefail

scripts_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${scripts_home}")"
cd "${project_home}"

# run our python lint checks
pylint ./*.py example/*.py example/**/*.py
pyright example/breeze_theme.py
flake8

# run our C++ lint checks