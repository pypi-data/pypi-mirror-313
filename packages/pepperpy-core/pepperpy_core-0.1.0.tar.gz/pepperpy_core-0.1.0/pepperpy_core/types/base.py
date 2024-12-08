"""Base type definitions."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseData:
    """Base class for configuration data."""

    name: str = ""
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModuleConfig(BaseData):
    """Base class for module configuration."""

    pass


# JSON-compatible type definitions
JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]
JsonDict = dict[str, JsonValue]

__all__ = [
    "BaseData",
    "ModuleConfig",
    "JsonPrimitive",
    "JsonValue",
    "JsonDict",
]
