"""Base configuration types."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseConfigData:
    """Base configuration data."""

    # Required fields
    name: str

    # Optional fields
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration data."""
        pass

    def get_stats(self) -> dict[str, Any]:
        """Get configuration statistics."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }
