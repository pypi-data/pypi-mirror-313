"""Logging formatters."""

from typing import Any

from .exceptions import LogFormatError


class BaseFormatter:
    """Base formatter."""

    def format(self, message: str, **kwargs: Any) -> str:
        """Format message.

        Args:
            message: Message to format
            **kwargs: Format arguments

        Returns:
            Formatted message
        """
        raise NotImplementedError


class TextFormatter(BaseFormatter):
    """Text formatter."""

    def format(self, message: str, **kwargs: Any) -> str:
        """Format message as text."""
        try:
            metadata = " ".join(f"{k}={v}" for k, v in kwargs.items())
            return f"{message} {metadata}".strip()
        except Exception as e:
            raise LogFormatError(f"Failed to format message: {e}") from e


class JsonFormatter(BaseFormatter):
    """JSON formatter."""

    def format(self, message: str, **kwargs: Any) -> str:
        """Format message as JSON."""
        try:
            import json

            data = {"message": message, **kwargs}
            return json.dumps(data)
        except Exception as e:
            raise LogFormatError(f"Failed to format message: {e}") from e
