"""Task exceptions."""

from ..exceptions import PepperpyError


class TaskError(PepperpyError):
    """Base task error."""

    pass


class TaskExecutionError(TaskError):
    """Task execution error."""

    pass


class TaskNotFoundError(TaskError):
    """Task not found error."""

    pass
