"""Plugin configuration module."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class PluginConfig(BaseConfigData):
    """Plugin configuration."""

    # Optional fields with defaults
    enabled: bool = True
    auto_load: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    # Required fields from BaseConfigData
    name: str = field(default="")  # Required but needs a default for dataclass
    paths: list[str] = field(default_factory=list)  # Required but needs a default

    def validate(self) -> None:
        """Validate configuration."""
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if not self.paths:
            raise ValueError("paths must not be empty")
        if not all(path.strip() for path in self.paths):
            raise ValueError("paths must not contain empty strings")

    def get_config(self) -> dict[str, Any]:
        """Get configuration dictionary."""
        return {
            "name": self.name,
            "paths": self.paths,
            "enabled": self.enabled,
            "auto_load": self.auto_load,
            "metadata": self.metadata,
        }


__all__ = ["PluginConfig"]
