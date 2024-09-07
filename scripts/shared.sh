#!/usr/bin/env bash
# Shared logic for our bash scripts.

# We have to use this because macOS does not have bash 4.2 support.
is-set()
{
    declare -p "${1}" &>/dev/null
}
