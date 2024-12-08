"""Logger implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseData
from .exceptions import LoggingError
from .formatters import BaseFormatter, TextFormatter


@dataclass
class LoggerConfig(BaseData):
    """Logger configuration."""

    name: str = ""
    enabled: bool = True
    level: str = "INFO"
    formatter: BaseFormatter = field(default_factory=TextFormatter)


class Logger:
    """Logger implementation."""

    def __init__(self, config: LoggerConfig) -> None:
        """Initialize logger."""
        self.config = config

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """Log message."""
        if not self.config.enabled:
            return

        try:
            formatted = self.config.formatter.format(
                message,
                level=level,
                logger=self.config.name,
                **{**self.config.metadata, **kwargs},
            )
            print(formatted)
        except Exception as e:
            raise LoggingError(f"Failed to log message: {e}") from e
