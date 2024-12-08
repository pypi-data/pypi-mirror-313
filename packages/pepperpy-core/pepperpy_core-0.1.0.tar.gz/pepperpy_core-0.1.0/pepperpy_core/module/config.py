"""Module configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class ModuleConfig(BaseConfigData):
    """Module configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
