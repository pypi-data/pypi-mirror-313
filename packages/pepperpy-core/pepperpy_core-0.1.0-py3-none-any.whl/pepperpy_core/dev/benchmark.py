"""Benchmark utilities."""

from typing import Any, Protocol, TypeVar


class LoggerProtocol(Protocol):
    """Protocol for logger interface."""

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        ...


T = TypeVar("T")


class Benchmark:
    """Benchmark utility class."""

    def __init__(self, logger: LoggerProtocol | None = None) -> None:
        """Initialize benchmark.

        Args:
            logger: Optional logger instance
        """
        self.logger = logger

    def log_result(self, message: str, **kwargs: Any) -> None:
        """Log benchmark result.

        Args:
            message: Message to log
            **kwargs: Additional log data
        """
        if self.logger is not None:
            self.logger.info(message, **kwargs)

    # Rest of the class implementation...
