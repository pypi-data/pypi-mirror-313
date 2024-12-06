class WorkflowException(Exception):
    """Base exception for workflow package."""
    pass

class CircularDependencyError(WorkflowException):
    """Raised when a circular dependency is detected in the workflow."""
    pass

class DependencyNotFoundError(WorkflowException):
    """Raised when a required dependency is not found."""
    pass

class TaskExecutionError(WorkflowException):
    """Raised when a task fails to execute."""
    pass