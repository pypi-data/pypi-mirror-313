from typing import *
from functools import lru_cache, cached_property
from itertools import groupby

from django.utils.module_loading import import_string


__all__ = (
    'Numeric',
    'cached_import_string',
    'autoimport',
    'sort_and_group',
    'importable_prop',
    'KwargsInjector',
)

T = TypeVar('T')
Numeric = Union[SupportsInt, SupportsFloat]


@lru_cache
def cached_import_string(path: Optional[str] = None):
    if path is None:
        return None

    return import_string(path)


def sort_and_group(
    items: Iterable[T],
    key: Optional[Callable[[T], Any]] = None,
):
    return groupby(sorted(items, key=key), key=key)


def autoimport(value):
    return cached_import_string(value) if isinstance(value, str) else value


class importable_prop(cached_property):
    def __init__(self, default: T = None):
        super().__init__(lambda _: autoimport(default))

    def __set__(self, instance, value: Any) -> None:
        cache = instance.__dict__
        cache[self.attrname] = autoimport(value)


class KwargsInjector:
    def __init__(self, **kwargs):
        cls = self.__class__

        for key, value in kwargs.items():
            if not hasattr(cls, key):
                raise TypeError(
                    "%s() received an invalid keyword %r."
                    "only accepts arguments that are already "
                    "attributes of the class." % (cls.__name__, key)
                )

            if value is None:
                continue

            setattr(self, key, value)
