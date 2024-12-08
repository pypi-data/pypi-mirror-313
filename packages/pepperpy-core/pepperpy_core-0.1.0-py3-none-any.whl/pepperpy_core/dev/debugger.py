"""Debugger utilities."""

from typing import Any, Protocol, TypeVar


class LoggerProtocol(Protocol):
    """Protocol for logger interface."""

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        ...


T = TypeVar("T")


class Debugger:
    """Debugger utility class."""

    def __init__(self, logger: LoggerProtocol | None = None) -> None:
        """Initialize debugger.

        Args:
            logger: Optional logger instance
        """
        self.logger = logger

    def log_debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message.

        Args:
            message: Message to log
            **kwargs: Additional log data
        """
        if self.logger is not None:
            self.logger.debug(message, **kwargs)

    def debug_call(self, func_name: str, *args: Any, **kwargs: Any) -> None:
        """Log function call debug information.

        Args:
            func_name: Function name
            *args: Function arguments
            **kwargs: Function keyword arguments
        """
        if self.logger is not None:
            self.logger.debug(
                f"Calling {func_name}",
                args=args,
                kwargs=kwargs,
            )

    def debug_result(self, func_name: str, result: Any) -> None:
        """Log function result debug information.

        Args:
            func_name: Function name
            result: Function result
        """
        if self.logger is not None:
            self.logger.debug(
                f"Result from {func_name}",
                result=result,
            )

    def debug_error(self, func_name: str, error: Exception) -> None:
        """Log function error debug information.

        Args:
            func_name: Function name
            error: Exception that occurred
        """
        if self.logger is not None:
            self.logger.debug(
                f"Error in {func_name}",
                error=str(error),
                error_type=type(error).__name__,
            )
