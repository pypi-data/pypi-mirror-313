"""Cache exceptions."""

from ..exceptions import PepperpyError


class CacheError(PepperpyError):
    """Base cache error."""

    pass


class CacheConnectionError(CacheError):
    """Cache connection error."""


class CacheKeyError(CacheError):
    """Cache key error."""


class CacheValueError(CacheError):
    """Cache value error."""


__all__ = [
    "CacheError",
    "CacheConnectionError",
    "CacheKeyError",
    "CacheValueError",
]
