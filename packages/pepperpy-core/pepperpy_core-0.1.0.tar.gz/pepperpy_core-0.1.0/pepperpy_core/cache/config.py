"""Cache configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class CacheConfig(BaseConfigData):
    """Cache configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    ttl: int = 3600  # Time to live in seconds
    max_size: int = 1000  # Maximum number of items
    eviction_policy: str = "lru"  # Least recently used
    metadata: dict[str, Any] = field(default_factory=dict)
