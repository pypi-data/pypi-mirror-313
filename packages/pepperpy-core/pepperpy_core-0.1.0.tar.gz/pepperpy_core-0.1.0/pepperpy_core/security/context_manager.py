"""Security context manager implementation."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from .config import SecurityConfig
from .context import SecurityContext, SecurityContextManager


class GlobalSecurityContextManager(SecurityContextManager):
    """Global security context manager implementation."""

    _instance: "GlobalSecurityContextManager | None" = None
    _initialized: bool = False

    def __new__(cls) -> "GlobalSecurityContextManager":
        """Create or return singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if not cls._initialized:
                config = SecurityConfig(name="global-security-context")
                super(SecurityContextManager, cls._instance).__init__(config)
                cls._initialized = True
        return cls._instance

    def __init__(self) -> None:
        """Initialize global security context manager."""
        pass


@asynccontextmanager
async def security_context(
    context: SecurityContext,
) -> AsyncGenerator[SecurityContext, None]:
    """Context manager for security context.

    Args:
        context: Security context to set

    Yields:
        Active security context
    """
    manager = GlobalSecurityContextManager()
    await manager.initialize()

    try:
        await manager.set_context(context)
        yield context
    finally:
        await manager.clear_context()
