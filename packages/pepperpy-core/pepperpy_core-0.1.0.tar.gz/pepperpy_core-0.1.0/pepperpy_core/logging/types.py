"""Logging types"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LogLevel(Enum):
    """Log level enum."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class LogRecord:
    """Log record."""

    level: LogLevel
    message: str
    logger_name: str
    module: str
    function: str
    line: int
    metadata: dict[str, Any] = field(default_factory=dict)
