# Async Workflow Management System

A robust, asynchronous workflow management system for Python that enables the creation and execution of complex task dependencies using a Directed Acyclic Graph (DAG) approach.

## Features

- Asynchronous task execution with asyncio
- Thread-safe context management for data sharing between tasks
- Automatic dependency resolution and validation
- Circular dependency detection
- Parallel execution of independent tasks
- Comprehensive error handling and logging
- Type-safe data management
- Task status tracking
- Resource cleanup management
- Workflow serialization and deserialization
- Progress tracking with task status updates

## Installation

Clone the repository and install the package:

```bash
git clone <repository-url>
cd async-workflow
pip install -r requirements.txt
```

## Quick Start

Here's a simple example of how to use the workflow system:

```python
from src import Workflow, Context

# Create a context and workflow
context = Context()
workflow = Workflow("example_workflow", context)

# Define tasks with dependencies
@workflow.task(provides=["data1"])
async def task1(context):
    context.set("data1", "Hello")

@workflow.task(requires=["data1"], provides=["data2"])
async def task2(context):
    data = context.get("data1")
    context.set("data2", f"{data} World!")

# Execute the workflow
import asyncio
await workflow.execute()
result = context.get("data2")  # "Hello World!"
```

## Task Dependencies

Tasks can specify their dependencies using `requires` and `provides` parameters:

```python
@workflow.task(
    requires=["input_data"],  # Data required by this task
    provides=["output_data"]  # Data provided by this task
)
async def process_data(context):
    data = context.get("input_data")
    result = do_something(data)
    context.set("output_data", result)
```

## Context Management

The Context class provides thread-safe data management:

```python
context.set("key", value)      # Store data
value = context.get("key")     # Retrieve data
context.delete("key")          # Remove data
context.clear()                # Clear all data
```

## Error Handling

The system includes built-in error handling for common scenarios:

- `CircularDependencyError`: Raised when circular dependencies are detected
- `DependencyNotFoundError`: Raised when required data isn't provided by any task
- `TaskExecutionError`: Raised when a task fails to execute
- `WorkflowException`: Base exception class for workflow-related errors

## Testing

Run the test suite using pytest:

```bash
pytest tests/
```

## Advanced Features

### Parallel Execution

Tasks without interdependencies are automatically executed in parallel:

```python
@workflow.task()
async def slow_task(context):
    await asyncio.sleep(2)
    context.set("slow", "done")

@workflow.task()
async def fast_task(context):
    await asyncio.sleep(1)
    context.set("fast", "done")
```

### Resource Management

Use context managers for automatic resource cleanup:

```python
async with Workflow("managed_workflow") as workflow:
    # Define tasks
    # Execute workflow
    # Resources automatically cleaned up after execution
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License


## Contact
