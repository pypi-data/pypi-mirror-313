"""Base validator implementation."""

from abc import ABC, abstractmethod
from typing import Any


class BaseValidator(ABC):
    """Base validator class."""

    def __init__(self, message: str | None = None) -> None:
        """Initialize validator.

        Args:
            message: Custom validation message
        """
        self._message = message

    @abstractmethod
    async def validate(self, value: Any) -> bool:
        """Validate value.

        Args:
            value: Value to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    @property
    def message(self) -> str | None:
        """Get validation message."""
        return self._message
