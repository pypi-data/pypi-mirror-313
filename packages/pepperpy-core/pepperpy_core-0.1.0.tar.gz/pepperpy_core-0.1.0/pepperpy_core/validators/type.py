"""Type validator implementation."""

from typing import Any

from .base import BaseValidator


class TypeValidator(BaseValidator):
    """Type validator."""

    def __init__(self, expected_type: type[Any], message: str | None = None) -> None:
        """Initialize validator.

        Args:
            expected_type: Expected type
            message: Custom validation message
        """
        super().__init__(message)
        self._expected_type = expected_type

    async def validate(self, value: Any) -> bool:
        """Validate value type.

        Args:
            value: Value to validate

        Returns:
            True if type matches, False otherwise
        """
        return isinstance(value, self._expected_type)
