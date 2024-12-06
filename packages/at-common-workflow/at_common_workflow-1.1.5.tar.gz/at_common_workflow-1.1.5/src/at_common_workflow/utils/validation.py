from typing import Dict, Set
from ..core.task import Task
from ..exceptions.workflow_exceptions import CircularDependencyError, DependencyNotFoundError
from ..core.context import Context
from ..core.schema import Input, Output

def validate_dag(tasks: Dict[str, Task], context: Context) -> None:
    """Validate that the workflow forms a valid DAG based on data dependencies."""
    # Track all available data keys from tasks and context
    available_keys: Set[str] = set()
    
    # Track which tasks provide which keys
    key_providers: Dict[str, Set[str]] = {}
    
    # Add keys from existing context data
    with context._lock:
        available_keys.update(context.keys())
    
    # Add keys provided by tasks and check for multiple providers
    for task_name, task in tasks.items():
        for key in task.provides.keys():
            if key not in key_providers:
                key_providers[key] = set()
            key_providers[key].add(task_name)
            if len(key_providers[key]) > 1:
                raise ValueError(f"Multiple tasks {key_providers[key]} provide the same output key: {key}")
        available_keys.update(task.provides.keys())
    
    # Check that all required keys will be provided
    for task_name, task in tasks.items():
        missing_keys = set(task.requires.keys()) - available_keys
        if missing_keys:
            raise DependencyNotFoundError(
                f"Task '{task_name}' requires keys {missing_keys} which are not provided by any task",
                missing_keys
            )
    
    # Check for circular dependencies
    visited: Set[str] = set()
    temp: Set[str] = set()
    
    def visit(task_name: str) -> None:
        if task_name in temp:
            raise CircularDependencyError(f"Circular dependency detected involving {task_name}")
        if task_name in visited:
            return
        
        temp.add(task_name)
        task = tasks[task_name]
        # Find all tasks that provide the required keys
        for req_key in task.requires:
            for dep_name, dep_task in tasks.items():
                if req_key in dep_task.provides:
                    visit(dep_name)
        temp.remove(task_name)
        visited.add(task_name)
    
    for task_name in tasks:
        visit(task_name)

def validate_schema(data: Dict, schema: Dict, data_type: str) -> None:
    """Validate data against a schema.
    
    Args:
        data: The input/output data to validate
        schema: The schema to validate against
        data_type: String indicating "input" or "output" for error messages
    """
    if not isinstance(data, (Input, Output)):
        raise ValueError(f"{data_type} must be an instance of {data_type.title()} class")

    # Check for missing required keys
    missing_keys = set(schema.keys()) - set(data.keys())
    if missing_keys:
        raise ValueError(f"Missing required {data_type} keys: {missing_keys}")

    # Validate existing keys and types
    for key, value in data.items():
        if key not in schema:
            raise ValueError(f"{data_type.title()} key '{key}' is not defined in the {data_type} schema")
        if not isinstance(value, schema[key]):
            raise ValueError(f"{data_type.title()} value for key '{key}' is not of the correct type. Expected {schema[key]}, got {type(value)}")