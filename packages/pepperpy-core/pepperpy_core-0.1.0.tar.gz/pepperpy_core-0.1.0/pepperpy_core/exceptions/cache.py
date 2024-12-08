"""Cache exceptions."""

from .base import PepperpyError


class CacheError(PepperpyError):
    """Base cache error."""

    pass


class CacheInitializationError(CacheError):
    """Cache initialization error."""

    pass


class CacheConnectionError(CacheError):
    """Cache connection error."""

    pass


class CacheOperationError(CacheError):
    """Cache operation error."""

    pass
