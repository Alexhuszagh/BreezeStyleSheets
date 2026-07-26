#!/usr/bin/env bash
#
# Run our code linters, including type checking.
# Since we have 0 dependencies other than basic parsers, we don't use security checks in CI.

set -eux pipefail

SCRIPTS_HOME="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJECT_HOME="$(dirname "${SCRIPTS_HOME}")"
cd "${PROJECT_HOME}"

uvx --from poethepoet poe lint
uvx --from poethepoet poe type
