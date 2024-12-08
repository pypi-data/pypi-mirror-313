"""Logging manager module."""

from typing import Any

from .log_config import LogConfig


class LogManager:
    """Logging manager."""

    def __init__(self, config: LogConfig) -> None:
        """Initialize logging manager.

        Args:
            config: Logging configuration
        """
        self.config = config

    def get_config(self) -> dict[str, Any]:
        """Get logging configuration.

        Returns:
            Logging configuration dictionary
        """
        return self.config.get_config()
