"""Logging handlers."""

from dataclasses import dataclass, field
from typing import Any, TextIO

from .types import LogLevel, LogRecord


@dataclass
class HandlerConfig:
    """Handler configuration."""

    name: str = ""
    level: LogLevel = LogLevel.INFO
    format: str = "%(levelname)s: %(message)s"
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseHandler:
    """Base logging handler."""

    def __init__(self, config: HandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            config: Handler configuration
        """
        self.config = config or HandlerConfig()

    def emit(self, record: LogRecord) -> None:
        """Emit log record."""
        raise NotImplementedError


class StreamHandler(BaseHandler):
    """Stream handler implementation."""

    def __init__(self, stream: TextIO, config: HandlerConfig | None = None) -> None:
        """Initialize handler.

        Args:
            stream: Output stream
            config: Handler configuration
        """
        super().__init__(config)
        self.stream = stream

    def emit(self, record: LogRecord) -> None:
        """Emit log record."""
        try:
            message = self.format(record)
            self.stream.write(message + "\n")
            self.stream.flush()
        except Exception as e:
            # Avoid recursion if error occurs during logging
            print(f"Error in log handler: {e}", file=self.stream)

    def format(self, record: LogRecord) -> str:
        """Format log record.

        Args:
            record: Log record

        Returns:
            Formatted message
        """
        return self.config.format % {
            "levelname": record.level.name,
            "message": record.message,
            "logger": record.logger_name,
            "module": record.module,
            "function": record.function,
            "line": record.line,
            **record.metadata,
        }
