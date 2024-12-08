"""Validation level definitions."""

from enum import Enum


class ValidationLevel(Enum):
    """Validation level enum."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
