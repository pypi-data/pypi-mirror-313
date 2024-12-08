class WorkflowException(Exception):
    """Base exception for workflow package.
    
    All custom exceptions in the workflow package should inherit from this class
    to allow for consistent error handling and categorization.
    """
    pass

class CircularDependencyError(WorkflowException):
    """Raised when a circular dependency is detected in the workflow.
    
    This occurs when tasks form a dependency cycle, where task A depends on task B,
    which depends on task A (directly or indirectly).
    
    Attributes:
        task_name (str): The name of the task where the circular dependency was detected
    """
    def __init__(self, task_name: str):
        self.task_name = task_name
        super().__init__(f"Circular dependency detected involving task '{task_name}'")

class DependencyNotFoundError(WorkflowException):
    """Raised when a required dependency is not found.
    
    This occurs when a task requires input that no other task provides.
    
    Attributes:
        task_name (str): The name of the task with missing dependencies
        missing_keys (set[str]): The set of required keys that are missing
    """
    def __init__(self, task_name: str, missing_keys: set[str]):
        self.task_name = task_name
        self.missing_keys = missing_keys
        super().__init__(
            f"Task '{task_name}' requires keys {missing_keys} which are not provided by any task"
        )

class TaskExecutionError(WorkflowException):
    """Raised when a task fails to execute.
    
    This is typically raised when a task encounters an error during execution,
    wrapping the original exception with additional context.
    
    Attributes:
        task_name (str): The name of the failed task
        original_error (Exception): The original exception that caused the failure
    """
    def __init__(self, task_name: str, original_error: Exception):
        self.task_name = task_name
        self.original_error = original_error
        super().__init__(f"Task '{task_name}' failed: {str(original_error)}")