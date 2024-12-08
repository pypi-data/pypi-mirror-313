"""Module exceptions."""

from ..exceptions import PepperpyError


class ModuleError(PepperpyError):
    """Base module error."""

    pass


class ModuleInitializationError(ModuleError):
    """Module initialization error."""

    pass


class ModuleNotFoundError(ModuleError):
    """Module not found error."""

    pass
