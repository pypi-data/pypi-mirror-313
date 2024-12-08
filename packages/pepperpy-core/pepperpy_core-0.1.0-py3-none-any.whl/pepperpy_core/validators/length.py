"""Length validator implementation."""

from typing import Any

from .base import BaseValidator


class LengthValidator(BaseValidator):
    """Length validator."""

    def __init__(
        self,
        min_length: int | None = None,
        max_length: int | None = None,
        message: str | None = None,
    ) -> None:
        """Initialize validator.

        Args:
            min_length: Minimum length
            max_length: Maximum length
            message: Custom validation message
        """
        super().__init__(message)
        self._min_length = min_length
        self._max_length = max_length

    async def validate(self, value: Any) -> bool:
        """Validate value length.

        Args:
            value: Value to validate

        Returns:
            True if length is valid, False otherwise
        """
        try:
            length = len(value)
        except TypeError:
            return False

        if self._min_length is not None and length < self._min_length:
            return False
        if self._max_length is not None and length > self._max_length:
            return False
        return True
