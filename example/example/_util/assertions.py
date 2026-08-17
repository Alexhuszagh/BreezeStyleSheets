"""Miscellaneous runtime assertions."""

from typing import TypeVar

_T = TypeVar("_T")


def nonnull(value: _T | None) -> _T:
    """Assert the value is not null."""
    assert value is not None
    return value
