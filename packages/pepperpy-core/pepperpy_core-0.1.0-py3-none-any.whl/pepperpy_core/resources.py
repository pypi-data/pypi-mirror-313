"""Resource management module."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pepperpy_core.exceptions.resource import ResourceError


@dataclass
class ResourceConfig:
    """Resource configuration."""

    name: str
    path: str | Path
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResourceInfo:
    """Resource information."""

    name: str
    path: Path
    size: int
    metadata: dict[str, Any] = field(default_factory=dict)


class ResourceManager:
    """Resource manager implementation."""

    def __init__(self) -> None:
        """Initialize resource manager."""
        self._resources: dict[str, ResourceInfo] = {}
        self._initialized: bool = False

    def initialize(self) -> None:
        """Initialize resource manager."""
        if self._initialized:
            return
        self._initialized = True

    def cleanup(self) -> None:
        """Cleanup resource manager."""
        if not self._initialized:
            return
        self._resources.clear()
        self._initialized = False

    def get_resource(self, name: str) -> ResourceInfo | None:
        """Get resource information.

        Args:
            name: Resource name

        Returns:
            Resource information if found, None otherwise

        Raises:
            ResourceError: If resource manager not initialized
        """
        if not self._initialized:
            raise ResourceError("Resource manager not initialized")
        return self._resources.get(name)

    def add_resource(
        self, name: str, path: str | Path, metadata: dict[str, Any] | None = None
    ) -> ResourceInfo:
        """Add resource.

        Args:
            name: Resource name
            path: Resource path
            metadata: Resource metadata

        Returns:
            Resource information

        Raises:
            ResourceError: If resource manager not initialized or resource already exists
        """
        if not self._initialized:
            raise ResourceError("Resource manager not initialized")

        if name in self._resources:
            raise ResourceError(f"Resource {name} already exists")

        path_obj = Path(path)
        if not path_obj.exists():
            raise ResourceError(f"Resource path {path} does not exist")

        info = ResourceInfo(
            name=name,
            path=path_obj,
            size=path_obj.stat().st_size,
            metadata=metadata or {},
        )
        self._resources[name] = info
        return info

    def remove_resource(self, name: str) -> None:
        """Remove resource.

        Args:
            name: Resource name

        Raises:
            ResourceError: If resource manager not initialized or resource not found
        """
        if not self._initialized:
            raise ResourceError("Resource manager not initialized")

        if name not in self._resources:
            raise ResourceError(f"Resource {name} not found")

        del self._resources[name]

    def list_resources(self) -> list[ResourceInfo]:
        """List all resources.

        Returns:
            List of resource information

        Raises:
            ResourceError: If resource manager not initialized
        """
        if not self._initialized:
            raise ResourceError("Resource manager not initialized")
        return list(self._resources.values())
