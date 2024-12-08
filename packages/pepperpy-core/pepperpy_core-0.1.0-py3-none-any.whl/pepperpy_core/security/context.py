"""Security context implementation."""

from dataclasses import dataclass, field
from typing import Any

from ..module import BaseModule
from .config import SecurityConfig


@dataclass
class SecurityContext:
    """Security context data."""

    user_id: str | None = None
    roles: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class SecurityContextManager(BaseModule[SecurityConfig]):
    """Security context manager implementation."""

    def __init__(self) -> None:
        """Initialize security context manager."""
        config = SecurityConfig(name="security-context")
        super().__init__(config)
        self._context: SecurityContext | None = None

    async def _setup(self) -> None:
        """Setup security context."""
        self._context = None

    async def _teardown(self) -> None:
        """Teardown security context."""
        self._context = None

    async def get_context(self) -> SecurityContext | None:
        """Get current security context.

        Returns:
            Current security context if set, None otherwise
        """
        if not self.is_initialized:
            await self.initialize()
        return self._context

    async def set_context(self, context: SecurityContext) -> None:
        """Set security context.

        Args:
            context: Security context to set
        """
        if not self.is_initialized:
            await self.initialize()
        self._context = context

    async def clear_context(self) -> None:
        """Clear security context."""
        if not self.is_initialized:
            await self.initialize()
        self._context = None

    async def get_stats(self) -> dict[str, Any]:
        """Get security context statistics.

        Returns:
            Security context statistics
        """
        if not self.is_initialized:
            await self.initialize()
        return {
            "name": self.config.name,
            "enabled": self.config.enabled,
            "strict_mode": self.config.strict_mode,
            "has_context": self._context is not None,
            "user_id": self._context.user_id if self._context else None,
            "roles_count": len(self._context.roles) if self._context else 0,
            "permissions_count": len(self._context.permissions) if self._context else 0,
        }
