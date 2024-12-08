"""Registry type definitions"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Registration:
    """Component registration data"""

    name: str
    component_type: type[Any]
    factory: Callable[..., Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RegistryEntry:
    """Registry entry data"""

    name: str
    component_type: type[Any]
    factory: Callable[..., Any]
    metadata: dict[str, Any] = field(default_factory=dict)
