"""A lazy attribute type."""

from collections.abc import Callable
from typing import Generic, TypeVar

_T = TypeVar("_T")
_C = TypeVar("_C")


class LazyAttribute(Generic[_C, _T]):
    """
    A lazily-computed attribute, which caches the stored value.

    This computes the value on the first call, and on all subsequent calls it
    uses the cached value.
    """

    __slots__ = ("get", "value")
    get: "Callable[[type[_C]], _T]"
    value: "_T | None"

    def __init__(self, get: "Callable[[type[_C]], _T]") -> "None":
        if isinstance(get, classmethod):
            get = get.__func__
        self.get = get
        self.value = None

    def __get__(self, instance: "_C | None", owner: "type[_C]") -> "_T":
        _ = instance
        if self.value is None:
            self.value = self.get(owner)
        return self.value


# NOTE: An alias since it will be used as a function-like object
lazy_attribute = LazyAttribute
