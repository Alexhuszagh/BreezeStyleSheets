#!/usr/bin/env bash
#
# Run our automatic code formatters.
#
# This requires black and isort to be installed.

set -eux pipefail

scripts_home="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
project_home="$(dirname "${scripts_home}")"
cd "${project_home}"

isort ./*.py example/*.py example/**/*.py
black --config pyproject.toml example/ ./*.py