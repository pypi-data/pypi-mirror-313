"""Security configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class SecurityConfig(BaseConfigData):
    """Security configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    strict_mode: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
