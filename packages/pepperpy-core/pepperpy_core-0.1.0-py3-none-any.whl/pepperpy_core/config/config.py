"""Core configuration module."""

from typing import Any


class Config:
    """Base configuration class."""

    def __init__(self) -> None:
        """Initialize configuration."""
        self._config: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return self._config
