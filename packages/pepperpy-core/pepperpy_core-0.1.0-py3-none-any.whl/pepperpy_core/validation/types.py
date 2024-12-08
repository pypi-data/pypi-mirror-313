"""Validation types."""

from dataclasses import dataclass, field

from ..base import BaseData
from ..types import JsonDict

__all__ = ["ValidationData", "ValidationResult"]


@dataclass
class ValidationData(BaseData):
    """Validation configuration data."""

    max_errors: int = 10
    stop_on_error: bool = False
    enabled: bool = True


@dataclass
class ValidationResult:
    """Validation result."""

    is_valid: bool
    errors: list[str]
    metadata: JsonDict = field(default_factory=dict)
