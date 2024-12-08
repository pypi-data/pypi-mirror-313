"""Cache types."""

from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    """Cache entry."""

    key: str
    value: Any
    expires_at: float
