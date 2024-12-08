"""Task configuration module."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class TaskConfig(BaseConfigData):
    """Task configuration."""

    name: str
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
