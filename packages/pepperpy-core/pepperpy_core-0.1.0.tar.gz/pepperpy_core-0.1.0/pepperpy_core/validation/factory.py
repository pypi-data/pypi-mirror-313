"""Validator factory implementation."""

from abc import ABC, abstractmethod
from typing import Any


class ValidatorFactory:
    """Factory for creating validators."""

    @staticmethod
    def create_schema_validator(schema_class: type[Any]) -> "SchemaValidator":
        """Create a schema validator.

        Args:
            schema_class: Schema class to validate against

        Returns:
            SchemaValidator instance
        """
        return SchemaValidator(schema_class)


class ValidationResult:
    """Validation result."""

    def __init__(self, is_valid: bool, errors: list[str] | None = None) -> None:
        self.is_valid = is_valid
        self.errors = errors or []


class BaseValidator(ABC):
    """Base validator interface."""

    @abstractmethod
    async def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Validate data."""
        pass


class SchemaValidator(BaseValidator):
    """Schema validator implementation."""

    def __init__(self, schema_class: type[Any]) -> None:
        """Initialize validator."""
        self.schema_class = schema_class

    async def validate(self, data: dict[str, Any]) -> ValidationResult:
        """Validate data against schema."""
        try:
            self.schema_class(**data)
            return ValidationResult(True)
        except Exception as e:
            return ValidationResult(False, [str(e)])
