"""Plugin exceptions module."""

from ..exceptions import PepperpyError


class PluginError(PepperpyError):
    """Base plugin error."""

    pass


class PluginNotFoundError(PluginError):
    """Plugin not found error."""

    pass


class PluginLoadError(PluginError):
    """Plugin load error."""

    pass
