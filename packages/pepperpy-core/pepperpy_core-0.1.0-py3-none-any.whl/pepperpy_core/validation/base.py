"""Base validation types."""

from dataclasses import dataclass, field
from typing import Any

from .level import ValidationLevel


@dataclass
class ValidationResult:
    """Validation result."""

    valid: bool
    level: ValidationLevel = ValidationLevel.INFO
    message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Validator:
    """Base validator interface."""

    async def validate(self, value: Any) -> ValidationResult:
        """Validate a single value."""
        raise NotImplementedError

    async def validate_many(self, values: list[Any]) -> list[ValidationResult]:
        """Validate multiple values."""
        return [await self.validate(value) for value in values]
