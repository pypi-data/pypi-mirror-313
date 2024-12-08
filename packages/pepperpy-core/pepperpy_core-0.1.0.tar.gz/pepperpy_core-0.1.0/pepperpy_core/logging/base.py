"""Base logging implementation."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class LogLevel(str, Enum):
    """Log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class BaseLogger(ABC):
    """Base logger interface."""

    @abstractmethod
    def log(self, level: LogLevel, message: str, **kwargs: Any) -> None:
        """Log message.

        Args:
            level: Log level
            message: Log message
            **kwargs: Additional log data
        """
        pass

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.log(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.log(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.log(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.log(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self.log(LogLevel.CRITICAL, message, **kwargs)
