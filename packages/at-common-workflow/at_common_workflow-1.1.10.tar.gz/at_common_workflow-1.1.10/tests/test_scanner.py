import pytest
from pathlib import Path
import tempfile
from at_common_workflow import TaskScanner, InputSchema, OutputSchema

# Helper function to create test files
def create_test_file(directory: Path, filename: str, content: str) -> Path:
    file_path = directory / filename
    file_path.write_text(content)
    return file_path

@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

def test_basic_task_scanning(temp_directory):
    # Create a test file with a task
    task_file_content = '''
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task(
    name="test_task",
    requires={"input": str},
    provides={"output": str}
)
async def test_task(context: Context):
    context["output"] = context["input"]
'''
    create_test_file(temp_directory, "test_tasks.py", task_file_content)
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 1
    assert tasks[0].name == "test_task"
    assert "input" in tasks[0].requires
    assert "output" in tasks[0].provides

def test_nested_directory_scanning(temp_directory):
    # Create nested directory structure
    nested_dir = temp_directory / "nested" / "deeper"
    nested_dir.mkdir(parents=True)
    
    task_file_content = '''
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task(name="nested_task")
async def nested_task(context: Context):
    pass
'''
    create_test_file(nested_dir, "nested_tasks.py", task_file_content)
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 1
    assert tasks[0].name == "nested_task"

def test_multiple_tasks_in_file(temp_directory):
    task_file_content = '''
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task(name="task1")
async def task1(context: Context):
    pass

@task(name="task2")
async def task2(context: Context):
    pass
'''
    create_test_file(temp_directory, "multiple_tasks.py", task_file_content)
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 2
    task_names = {task.name for task in tasks}
    assert task_names == {"task1", "task2"}

def test_non_python_files(temp_directory):
    # Create non-Python files
    create_test_file(temp_directory, "not_a_task.txt", "Some text")
    create_test_file(temp_directory, "also_not_a_task.json", "{}")
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 0

def test_python_file_without_tasks(temp_directory):
    file_content = '''
def regular_function():
    pass

class RegularClass:
    pass
'''
    create_test_file(temp_directory, "no_tasks.py", file_content)
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 0

def test_invalid_python_file(temp_directory):
    # Create a Python file with syntax error
    create_test_file(temp_directory, "invalid.py", "this is not valid python code")
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 0

def test_task_attributes(temp_directory):
    task_file_content = '''
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task(
    name="attribute_test",
    description="Test task description",
    parameters={
        "param":"value"
    },
    requires={"input": str},
    provides={"output": int}
)
async def attribute_test(context: Context, param:str):
    pass
'''
    create_test_file(temp_directory, "task_attributes.py", task_file_content)
    
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 1
    task = tasks[0]
    
    assert task.name == "attribute_test"
    assert task.description == "Test task description"
    assert len(task.parameters) == 1
    assert task.parameters[0].name == "param"
    assert task.parameters[0].value == "value"
    assert task.parameters[0].type == str
    assert isinstance(task.requires, InputSchema)
    assert isinstance(task.provides, OutputSchema)
    assert task.requires == InputSchema({"input": str})
    assert task.provides == OutputSchema({"output": int})

def test_scan_empty_directory(temp_directory):
    tasks = TaskScanner.scan(str(temp_directory))
    assert len(tasks) == 0

def test_scan_nonexistent_directory():
    with pytest.raises(FileNotFoundError):
        TaskScanner.scan("/nonexistent/directory")
