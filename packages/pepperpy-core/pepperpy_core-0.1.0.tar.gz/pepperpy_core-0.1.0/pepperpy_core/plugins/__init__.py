"""Plugin system for extending functionality"""

from importlib import import_module
from typing import Any


class PluginRegistry:
    """Registry for plugin management"""

    def __init__(self):
        self._plugins: dict[str, Any] = {}

    def register(self, name: str, plugin: Any) -> None:
        """Register plugin"""
        self._plugins[name] = plugin

    def get(self, name: str) -> Any:
        """Get registered plugin"""
        return self._plugins[name]

    def load_from_path(self, path: str) -> None:
        """Load plugins from path"""
        module = import_module(path)
        if hasattr(module, "register_plugins"):
            module.register_plugins(self)


registry = PluginRegistry()
