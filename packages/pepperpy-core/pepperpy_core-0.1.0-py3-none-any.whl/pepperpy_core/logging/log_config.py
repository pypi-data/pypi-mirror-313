"""Logging configuration module."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class LogConfig(BaseConfigData):
    """Logging configuration."""

    # Required fields from BaseConfigData
    name: str = field(default="")  # Required but needs a default for dataclass

    # Optional fields with defaults
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    datefmt: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if not self.name.strip():
            raise ValueError("name must not be empty")

    def get_config(self) -> dict[str, Any]:
        """Get configuration dictionary."""
        config = {
            "name": self.name,
            "level": self.level,
            "format": self.format,
            "metadata": self.metadata,
        }
        if self.datefmt is not None:
            config["datefmt"] = self.datefmt
        return config


__all__ = ["LogConfig"]
