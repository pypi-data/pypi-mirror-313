"""Plugin system decorators"""

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def plugin(name: str) -> Callable[[type[T]], type[T]]:
    """
    Register class as plugin

    Args:
        name: Plugin identifier

    Returns:
        Callable[[Type[T]], Type[T]]: Decorator function

    """

    def decorator(cls: type[T]) -> type[T]:
        """
        Plugin registration decorator

        Args:
            cls: Class to register

        Returns:
            Type[T]: Registered class

        """
        from . import registry

        registry.register(name, cls)
        return cls

    return decorator


def hook(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Register function as plugin hook

    Args:
        name: Hook identifier

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: Decorator function

    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Hook registration decorator

        Args:
            func: Function to register

        Returns:
            Callable[..., Any]: Registered function

        """
        from . import registry

        registry.register(name, func)
        return func

    return decorator
