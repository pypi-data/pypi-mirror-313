"""Base exceptions for pepperpy-core."""


class PepperpyError(Exception):
    """Base exception for all pepperpy errors."""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        """Initialize exception.

        Args:
            message: Error message
            cause: Original exception that caused this error
        """
        super().__init__(message)
        self.cause = cause


class ConfigError(PepperpyError):
    """Configuration error."""

    pass


class ValidationError(PepperpyError):
    """Validation error."""

    pass


class ResourceError(PepperpyError):
    """Resource error."""

    pass


class StateError(PepperpyError):
    """State error."""

    pass


class InitializationError(PepperpyError):
    """Initialization error."""

    pass
