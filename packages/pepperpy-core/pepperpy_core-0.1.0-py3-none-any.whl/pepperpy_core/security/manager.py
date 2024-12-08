"""Security manager module."""

from abc import ABC, abstractmethod

from pydantic import BaseModel

from .config import SecurityConfig
from .types import AuthToken, AuthUser


class SecurityManager(ABC):
    """Abstract security manager."""

    def __init__(self, config: SecurityConfig) -> None:
        """Initialize security manager.

        Args:
            config: Security configuration
        """
        self.config = config
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize security manager."""
        if self._initialized:
            return
        self._initialized = True

    async def cleanup(self) -> None:
        """Cleanup security manager."""
        if not self._initialized:
            return
        self._initialized = False

    @abstractmethod
    async def authenticate(self, credentials: BaseModel) -> AuthToken:
        """Authenticate user with credentials.

        Args:
            credentials: User credentials

        Returns:
            Authentication token
        """
        pass

    @abstractmethod
    async def validate_token(self, token: AuthToken) -> AuthUser | None:
        """Validate authentication token.

        Args:
            token: Authentication token

        Returns:
            Authenticated user if token is valid, None otherwise
        """
        pass
