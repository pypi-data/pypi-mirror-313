"""Metrics decorators."""

import asyncio
import functools
import time
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar, Union, cast

from .base import MetricsCollector, MetricsConfig

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")

# Tipos para funções síncronas e assíncronas
SyncFunc = Callable[P, R]
AsyncFunc = Callable[P, Coroutine[Any, Any, R]]
AnyFunc = Union[SyncFunc[P, R], AsyncFunc[P, R]]


def timing(
    collector: MetricsCollector | None = None,
) -> Callable[[AnyFunc[P, R]], AnyFunc[P, R]]:
    """Decorator to measure function execution time.

    Args:
        collector: Optional metrics collector. If not provided, a new one will be created.

    Returns:
        Decorated function
    """
    metrics = collector or MetricsCollector(MetricsConfig(name="timing-metrics"))

    def decorator(func: AnyFunc[P, R]) -> AnyFunc[P, R]:
        """Decorate function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                start_time = time.perf_counter()
                try:
                    result = await cast(AsyncFunc[P, R], func)(*args, **kwargs)
                    return result
                finally:
                    duration = time.perf_counter() - start_time
                    await metrics.collect(
                        name=f"{func.__module__}.{func.__qualname__}",
                        value=duration,
                        tags={"unit": "seconds"},
                    )

            return cast(AnyFunc[P, R], async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                start_time = time.perf_counter()
                try:
                    result = cast(SyncFunc[P, R], func)(*args, **kwargs)
                    return result
                finally:
                    duration = time.perf_counter() - start_time
                    # Criar task para coletar métricas de forma assíncrona
                    asyncio.create_task(
                        metrics.collect(
                            name=f"{func.__module__}.{func.__qualname__}",
                            value=duration,
                            tags={"unit": "seconds"},
                        )
                    )

            return cast(AnyFunc[P, R], sync_wrapper)

    return decorator


def count(
    collector: MetricsCollector | None = None,
) -> Callable[[AnyFunc[P, R]], AnyFunc[P, R]]:
    """Decorator to count function calls.

    Args:
        collector: Optional metrics collector. If not provided, a new one will be created.

    Returns:
        Decorated function
    """
    metrics = collector or MetricsCollector(MetricsConfig(name="count-metrics"))

    def decorator(func: AnyFunc[P, R]) -> AnyFunc[P, R]:
        """Decorate function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """
        counter = 0

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                nonlocal counter
                counter += 1
                try:
                    result = await cast(AsyncFunc[P, R], func)(*args, **kwargs)
                    return result
                finally:
                    await metrics.collect(
                        name=f"{func.__module__}.{func.__qualname__}",
                        value=counter,
                        tags={"type": "counter"},
                    )

            return cast(AnyFunc[P, R], async_wrapper)
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                nonlocal counter
                counter += 1
                try:
                    result = cast(SyncFunc[P, R], func)(*args, **kwargs)
                    return result
                finally:
                    # Criar task para coletar métricas de forma assíncrona
                    asyncio.create_task(
                        metrics.collect(
                            name=f"{func.__module__}.{func.__qualname__}",
                            value=counter,
                            tags={"type": "counter"},
                        )
                    )

            return cast(AnyFunc[P, R], sync_wrapper)

    return decorator
