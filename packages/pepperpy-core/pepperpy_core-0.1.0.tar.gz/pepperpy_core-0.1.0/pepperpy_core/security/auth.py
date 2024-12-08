"""Authentication module implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule
from .config import SecurityConfig


@dataclass
class AuthInfo:
    """Authentication information."""

    user_id: str
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AuthManager(BaseModule[SecurityConfig]):
    """Authentication manager implementation."""

    def __init__(self) -> None:
        """Initialize authentication manager."""
        config = SecurityConfig(name="auth-manager")
        super().__init__(config)
        self._auth_info: AuthInfo | None = None

    async def _setup(self) -> None:
        """Setup authentication manager."""
        self._auth_info = None

    async def _teardown(self) -> None:
        """Teardown authentication manager."""
        self._auth_info = None

    async def authenticate(self, auth_info: AuthInfo) -> None:
        """Authenticate user.

        Args:
            auth_info: Authentication information
        """
        if not self.is_initialized:
            await self.initialize()
        self._auth_info = auth_info

    async def get_current_user(self) -> AuthInfo | None:
        """Get current authenticated user.

        Returns:
            Current user information if authenticated, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        return self._auth_info

    async def get_stats(self) -> dict[str, Any]:
        """Get authentication statistics.

        Returns:
            Authentication statistics
        """
        if not self.is_initialized:
            await self.initialize()
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "is_authenticated": self._auth_info is not None,
            "user_id": self._auth_info.user_id if self._auth_info else None,
            "roles_count": len(self._auth_info.roles) if self._auth_info else 0,
            "permissions_count": len(self._auth_info.permissions)
            if self._auth_info
            else 0,
        }
