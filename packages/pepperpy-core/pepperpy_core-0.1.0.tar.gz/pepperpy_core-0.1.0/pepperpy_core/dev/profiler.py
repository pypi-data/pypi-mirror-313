"""Development profiler utilities."""

import cProfile
import pstats
from collections.abc import Callable
from pathlib import Path
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class Profiler:
    """Code profiler implementation."""

    def __init__(self, output_dir: str | Path = "profiles") -> None:
        """Initialize profiler.

        Args:
            output_dir: Directory to store profile results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self._profiler = cProfile.Profile()
        self._stats: pstats.Stats | None = None

    def start(self) -> None:
        """Start profiling."""
        self._profiler.enable()

    def stop(self) -> None:
        """Stop profiling."""
        self._profiler.disable()
        self._stats = pstats.Stats(self._profiler)

    def save(self, name: str) -> None:
        """Save profile results.

        Args:
            name: Profile name

        Raises:
            RuntimeError: If profiler not stopped
        """
        if self._stats is None:
            raise RuntimeError("Profiler not stopped")

        # Converter o caminho de saída para Path
        output_file = self.output_dir / f"{name}.prof"
        self._stats.dump_stats(str(output_file))

    def print_stats(self, limit: int = 20) -> None:
        """Print profile statistics.

        Args:
            limit: Maximum number of entries to print
        """
        if self._stats is None:
            raise RuntimeError("Profiler not stopped")

        self._stats.sort_stats("cumulative")
        self._stats.print_stats(limit)

    def profile(self, func: Callable[P, R]) -> Callable[P, R]:
        """Profile function decorator.

        Args:
            func: Function to profile

        Returns:
            Decorated function
        """

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self.start()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                self.stop()
                self.print_stats()

        return wrapper
