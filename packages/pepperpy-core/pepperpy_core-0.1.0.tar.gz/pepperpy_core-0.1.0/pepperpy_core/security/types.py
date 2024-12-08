"""Security types."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AuthType(Enum):
    """Authentication type."""

    BASIC = "basic"
    TOKEN = "token"
    OAUTH = "oauth"
    CUSTOM = "custom"


@dataclass
class AuthContext:
    """Authentication context."""

    auth_type: AuthType
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthToken:
    """Authentication token."""

    value: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthUser:
    """Authenticated user."""

    username: str
    metadata: dict[str, Any] = field(default_factory=dict)
    token: AuthToken | None = None
