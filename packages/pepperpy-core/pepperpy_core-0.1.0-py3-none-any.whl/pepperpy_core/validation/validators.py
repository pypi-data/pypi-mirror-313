"""Common validators."""

import re
from dataclasses import dataclass
from typing import Any

from .base import ValidationResult, Validator
from .level import ValidationLevel


@dataclass
class RegexValidator(Validator):
    """Regex validator."""

    pattern: str
    message: str | None = None
    level: ValidationLevel = ValidationLevel.ERROR

    async def validate(self, value: Any) -> ValidationResult:
        """Validate value against regex pattern."""
        if not isinstance(value, str):
            return ValidationResult(
                valid=False,
                message=f"Expected string, got {type(value).__name__}",
                level=self.level,
                metadata={"actual_type": type(value).__name__},
            )

        is_valid = bool(re.match(self.pattern, value))
        return ValidationResult(
            valid=is_valid,
            message=self.message or f"Value does not match pattern: {self.pattern}",
            level=self.level,
            metadata={"pattern": self.pattern},
        )


@dataclass
class LengthValidator(Validator):
    """Length validator."""

    min_length: int | None = None
    max_length: int | None = None
    level: ValidationLevel = ValidationLevel.ERROR

    async def validate(self, value: Any) -> ValidationResult:
        """Validate value length."""
        try:
            length = len(value)
            metadata = {"length": length}

            if self.min_length is not None and length < self.min_length:
                return ValidationResult(
                    valid=False,
                    message=f"Length {length} is below minimum of {self.min_length}",
                    level=self.level,
                    metadata=metadata,
                )

            if self.max_length is not None and length > self.max_length:
                return ValidationResult(
                    valid=False,
                    message=f"Length {length} is above maximum of {self.max_length}",
                    level=self.level,
                    metadata=metadata,
                )

            return ValidationResult(
                valid=True, level=ValidationLevel.INFO, metadata=metadata
            )

        except TypeError:
            return ValidationResult(
                valid=False,
                message=f"Value of type {type(value).__name__} does not support length check",
                level=self.level,
            )


@dataclass
class TypeValidator(Validator):
    """Type validator."""

    expected_type: type | tuple[type, ...]
    level: ValidationLevel = ValidationLevel.ERROR

    async def validate(self, value: Any) -> ValidationResult:
        """Validate value type."""
        is_valid = isinstance(value, self.expected_type)
        metadata = {
            "expected_type": str(self.expected_type),
            "actual_type": type(value).__name__,
        }

        return ValidationResult(
            valid=is_valid,
            message=f"Expected type {self.expected_type}, got {type(value).__name__}",
            level=self.level,
            metadata=metadata,
        )
