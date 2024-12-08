"""Regex validator implementation."""

import re
from typing import Any

from .base import BaseValidator


class RegexValidator(BaseValidator):
    """Regex validator."""

    def __init__(self, pattern: str, message: str | None = None) -> None:
        """Initialize validator.

        Args:
            pattern: Regex pattern
            message: Custom validation message
        """
        super().__init__(message)
        self._pattern = re.compile(pattern)

    async def validate(self, value: Any) -> bool:
        """Validate value matches pattern.

        Args:
            value: Value to validate

        Returns:
            True if matches pattern, False otherwise
        """
        if not isinstance(value, str):
            return False
        return bool(self._pattern.match(value))
