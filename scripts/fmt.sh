#!/usr/bin/env bash
#
# Run our automatic code formatters.
#
# This requires black and isort to be installed.

set -eux pipefail

SCRIPTS_HOME="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJECT_HOME="$(dirname "${SCRIPTS_HOME}")"
cd "${PROJECT_HOME}"

uvx --from poethepoet poe fmt
