from typing import List, Set, Any, TypeVar, Callable, ParamSpec, get_type_hints
import asyncio
from ..utils.logging import setup_logger
from .context import Context
import inspect
from functools import wraps
from .io import InputSchema, OutputSchema
from enum import Enum
from dataclasses import dataclass

logger = setup_logger(__name__)

P = ParamSpec('P')
T = TypeVar('T')

class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class TaskProgress:
    """Represents the progress status of a task in the workflow."""
    name: str
    status: TaskStatus

# Type definitions
TaskParameters = dict[str, Any]
TaskFunction = Callable[['Context'], Any]

def normalize_task_function(func: Callable[P, T]) -> Callable[P, T]:
    """Normalize and validate a task function."""
    
    @wraps(func)
    async def wrapper(context: Context, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(f"Task function '{func.__name__}' must be async")
            
        # Validate type hints
        hints = get_type_hints(func)
        if 'context' not in hints or not issubclass(hints['context'], Context):
            raise ValueError(f"Task function '{func.__name__}' must have 'context: Context' as first parameter")
            
        # Validate return type is None (tasks shouldn't return values, they should modify context)
        if hints.get('return') is not None:
            raise ValueError(f"Task function '{func.__name__}' should not return any value")
            
        return await func(context, **kwargs)
        
    return wrapper

class Task:
    """Represents a single task in the workflow."""
    def __init__(
        self,
        name: str,
        func: TaskFunction,
        description: str,
        parameters: TaskParameters,
        requires: InputSchema,
        provides: OutputSchema
    ):
        self.name: str = name
        self.description: str = description
        self.func: TaskFunction = normalize_task_function(func)
        self.parameters: TaskParameters = parameters
        self.requires: InputSchema = requires
        self.provides: OutputSchema = provides
        self.status: TaskStatus = TaskStatus.PENDING
    
    async def execute(self, context: Context) -> None:
        """Execute the task function."""
        try:
            self.status = TaskStatus.RUNNING
            logger.info(f"Starting task: {self.name}")
            
            if not asyncio.iscoroutinefunction(self.func):
                raise ValueError(f"Task {self.name} must be an async function")
            
            sig = inspect.signature(self.func)
            for param_name, param in sig.parameters.items():
                if param_name not in ['self', 'context']:  # Skip self and context parameters
                    if param.default == inspect.Parameter.empty and param_name not in self.parameters:
                        raise ValueError(f"Required parameter '{param_name}' not provided for task '{self.name}'")
            
            await self.func(context, **self.parameters)
            
            self.status = TaskStatus.COMPLETED
            logger.info(f"Completed task: {self.name}")
            
        except Exception as e:
            self.status = TaskStatus.FAILED
            logger.error(f"Task {self.name} failed: {str(e)}")
            raise