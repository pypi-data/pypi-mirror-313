"""Registry configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class RegistryConfig(BaseConfigData):
    """Registry configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    case_sensitive: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
