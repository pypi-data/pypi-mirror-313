"""Logging exceptions."""

from ..exceptions import PepperpyError


class LoggingError(PepperpyError):
    """Base logging error."""


class LogConfigError(LoggingError):
    """Logging configuration error."""


class LogHandlerError(LoggingError):
    """Logging handler error."""


class LogFormatError(LoggingError):
    """Logging format error."""


__all__ = [
    "LoggingError",
    "LogConfigError",
    "LogHandlerError",
    "LogFormatError",
]
