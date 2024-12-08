"""Base data types."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseData:
    """Base data class."""

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleConfig(BaseData):
    """Base module configuration."""

    name: str = ""
    enabled: bool = True


__all__ = ["BaseData", "ModuleConfig"]
