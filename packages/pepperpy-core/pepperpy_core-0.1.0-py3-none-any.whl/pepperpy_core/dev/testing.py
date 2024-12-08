"""Testing utilities"""

import asyncio
import functools
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T", bound=Callable[..., Any])


def async_test(func: T) -> T:
    """Decorator for async test functions"""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Run async function in event loop"""
        return asyncio.run(func(*args, **kwargs))

    return wrapper  # type: ignore


class AsyncTestCase:
    """Base class for async test cases"""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test class"""
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down test class"""
        cls.loop.close()
        asyncio.set_event_loop(None)

    def run_async(self, coro: Any) -> Any:
        """Run coroutine in test loop"""
        return self.loop.run_until_complete(coro)


def run_async(coro: Any) -> Any:
    """Run coroutine in new event loop"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)
