"""Security decorators."""

import functools
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar, cast

from .context_manager import GlobalSecurityContextManager

P = ParamSpec("P")
R = TypeVar("R")
AsyncFunc = Callable[P, Coroutine[Any, Any, R]]
SyncFunc = Callable[P, R]


def require_auth() -> Callable[[AsyncFunc[P, R]], AsyncFunc[P, R]]:
    """Require authentication decorator.

    Returns:
        Decorated function
    """

    def decorator(func: AsyncFunc[P, R]) -> AsyncFunc[P, R]:
        """Decorate function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrap function call.

            Args:
                *args: Function arguments
                **kwargs: Function keyword arguments

            Returns:
                Function result

            Raises:
                RuntimeError: If not authenticated
            """
            manager = GlobalSecurityContextManager()
            context = await manager.get_context()
            if not context:
                raise RuntimeError("Authentication required")
            return await func(*args, **kwargs)

        return cast(AsyncFunc[P, R], wrapper)

    return decorator


def require_roles(
    *roles: str,
) -> Callable[[AsyncFunc[P, R]], AsyncFunc[P, R]]:
    """Require roles decorator.

    Args:
        *roles: Required roles

    Returns:
        Decorated function
    """

    def decorator(func: AsyncFunc[P, R]) -> AsyncFunc[P, R]:
        """Decorate function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrap function call.

            Args:
                *args: Function arguments
                **kwargs: Function keyword arguments

            Returns:
                Function result

            Raises:
                RuntimeError: If required roles not present
            """
            manager = GlobalSecurityContextManager()
            context = await manager.get_context()
            if not context:
                raise RuntimeError("Authentication required")
            if not all(role in context.roles for role in roles):
                raise RuntimeError("Required roles not present")
            return await func(*args, **kwargs)

        return cast(AsyncFunc[P, R], wrapper)

    return decorator


def require_permissions(
    *permissions: str,
) -> Callable[[AsyncFunc[P, R]], AsyncFunc[P, R]]:
    """Require permissions decorator.

    Args:
        *permissions: Required permissions

    Returns:
        Decorated function
    """

    def decorator(func: AsyncFunc[P, R]) -> AsyncFunc[P, R]:
        """Decorate function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrap function call.

            Args:
                *args: Function arguments
                **kwargs: Function keyword arguments

            Returns:
                Function result

            Raises:
                RuntimeError: If required permissions not present
            """
            manager = GlobalSecurityContextManager()
            context = await manager.get_context()
            if not context:
                raise RuntimeError("Authentication required")
            if not all(perm in context.permissions for perm in permissions):
                raise RuntimeError("Required permissions not present")
            return await func(*args, **kwargs)

        return cast(AsyncFunc[P, R], wrapper)

    return decorator
