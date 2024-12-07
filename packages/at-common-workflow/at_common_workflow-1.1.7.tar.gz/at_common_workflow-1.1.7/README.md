# Aysnc Workflow

A Python package for building and executing workflow tasks in a directed acyclic graph (DAG) pattern. This package provides a flexible framework for defining, organizing, and running dependent tasks with strong type checking and thread safety.

## Features

- Task-based workflow system with dependency management
- Async/await support for concurrent task execution 
- Thread-safe context for sharing data between tasks
- Input/output schema validation
- Progress tracking and status reporting
- Workflow serialization and deserialization
- Built-in logging
- Type checking and validation

## Installation

```bash
pip install at-common-workflow
```

## Requirements

- Python >= 3.11
- pydantic >= 2.10.0
- pytest >= 8.3.3 (for testing)

## Quick Start

Here's a simple example of creating and executing a workflow:

```python
from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.task import task
from at_common_workflow.core.io import InputSchema, OutputSchema
from at_common_workflow.core.context import Context

# Define your tasks
@task(
    name="task_a",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"a_output": str})
)
async def task_a(context: Context):
    context["a_output"] = context["input"] + "processed"

# Create a workflow
workflow = Workflow(name="my_workflow", input_schema=InputSchema({"input": str}), output_schema=OutputSchema({"a_output": str}))
workflow.add_task(task_a)

# Execute the workflow
result = await workflow.execute({"input": "test"})
print(result) # {"a_output": "test_processed"}
```

## Key Components

### Task Decorator

The `@task` decorator allows you to define workflow tasks with:
- Input/output schemas
- Task parameters
- Description
- Name

### Workflow

The `Workflow` class manages:
- Task dependencies
- Execution order
- Data flow between tasks
- Progress tracking
- Schema validation

### Context

Thread-safe dictionary for sharing data between tasks with:
- Deep copy of values
- Lock-based synchronization
- Type validation

## Advanced Features

### Progress Tracking

```python
def track_progress(progress: TaskProgress):
    print(f"Task {progress.name}: {progress.status}")

result = await workflow.execute({"input": "test"}, track_progress=track_progress)
```

### Workflow Serialization

```python
from at_common_workflow.serialization.workflow_serializer import WorkflowSerializer

serialized_workflow = WorkflowSerializer.serialize(workflow)
```

### Workflow Deserialization

```python
from at_common_workflow.serialization.workflow_serializer import WorkflowSerializer

deserialized_workflow = WorkflowSerializer.deserialize(serialized_workflow)
```

### Task Scanner

The `WorkflowScanner` class scans a directory for tasks and returns a list of task information.

```python
from at_common_workflow.core.scanner import WorkflowScanner

tasks = WorkflowScanner.scan_directory("path/to/tasks")
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions and support, please open an issue on the GitHub repository.
