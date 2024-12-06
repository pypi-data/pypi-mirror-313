import pytest
import os
from pathlib import Path
from src.core.scanner import WorkflowScanner
from src.core.io import InputSchema, OutputSchema
from src import Workflow
import tempfile

# Test task definitions
@pytest.fixture
def test_tasks_dir(tmp_path):
    """Create a temporary directory with test task files."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    
    # Create a test module with decorated tasks
    task_file = tasks_dir / "test_tasks.py"
    task_file.write_text("""
from src import Workflow
from src.core.io import InputSchema, OutputSchema
from typing import Any

workflow = Workflow("test_workflow", InputSchema({}), OutputSchema({}))

@workflow.task(
    provides=OutputSchema({"output1": str})
)
async def workflow_task1(context):
    context["output1"] = "test1"

@workflow.task(
    requires=InputSchema({"input": int}),
    provides=OutputSchema({"output2": int}),
    parameters={"multiplier": 2}
)
async def workflow_task2(context, multiplier: int = 2):
    context["output2"] = 42 * multiplier

def regular_function():
    pass
""")
    
    return tasks_dir

async def test_scan_directory(test_tasks_dir):
    """Test scanning a directory for workflow tasks."""
    tasks = WorkflowScanner.scan_directory(str(test_tasks_dir))
    print(tasks)
    assert len(tasks) == 2
    
    # Verify first task
    task1 = next(t for t in tasks if t["name"] == "workflow_task1")
    assert task1["parameters"] == []
    assert task1["requires"] == []
    assert task1["provides"] == [{"name": "output1", "type": "str"}]
    
    # Verify second task
    task2 = next(t for t in tasks if t["name"] == "workflow_task2")
    assert len(task2["parameters"]) == 1
    assert task2["parameters"][0] == {"name": "multiplier", "type": "int", "value": 2}
    assert task2["requires"] == [{"name": "input", "type": "int"}]
    assert task2["provides"] == [{"name": "output2", "type": "int"}]

def test_scan_empty_directory(tmp_path):
    """Test scanning an empty directory."""
    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 0

def test_scan_directory_with_errors(tmp_path):
    """Test scanning a directory with invalid Python files."""
    invalid_file = tmp_path / "invalid.py"
    invalid_file.write_text("this is not valid python code")
    
    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 0

def test_scan_nested_directories(tmp_path):
    """Test scanning nested directories for tasks."""
    # Create nested directory structure
    nested_dir = tmp_path / "nested" / "tasks"
    nested_dir.mkdir(parents=True)
    
    task_file = nested_dir / "nested_task.py"
    task_file.write_text("""
def workflow_task(context):
    pass
workflow_task._is_workflow_task = True
workflow_task._requires = {}
workflow_task._provides = {}
workflow_task._parameters = {}
""")
    
    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 1
    assert tasks[0]["name"] == "workflow_task"

def test_type_conversion():
    """Test type string conversion utility."""
    from inspect import Parameter
    
    # Test empty parameter
    assert WorkflowScanner._get_type_str(Parameter.empty) == "Any"
    
    # Test basic types
    assert WorkflowScanner._get_type_str(str) == "str"
    assert WorkflowScanner._get_type_str(int) == "int"
    assert WorkflowScanner._get_type_str(float) == "float"
    assert WorkflowScanner._get_type_str(bool) == "bool"
    assert WorkflowScanner._get_type_str(list) == "list"
    assert WorkflowScanner._get_type_str(dict) == "dict"

def test_scan_directory_with_non_python_files(tmp_path, monkeypatch):
    """Test scanning a directory containing non-Python files."""
    # Add the temp directory to Python path
    monkeypatch.syspath_prepend(str(tmp_path))
    
    # Create a text file
    text_file = tmp_path / "test.txt"
    text_file.write_text("This is a text file")
    
    # Create a Python file with a task
    py_file = tmp_path / "task.py"
    py_file.write_text("""
def workflow_task(context):
    pass
workflow_task._is_workflow_task = True
workflow_task._requires = {}
workflow_task._provides = {}
workflow_task._parameters = {}
""")
    
    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 1
    assert tasks[0]["name"] == "workflow_task"

def test_scan_directory_with_multiple_files(tmp_path):
    """Test scanning a directory with multiple Python files."""
    # Create first file with tasks
    file1 = tmp_path / "tasks1.py"
    file1.write_text("""
def task1(context):
    pass
task1._is_workflow_task = True
task1._requires = {}
task1._provides = {"output1": str}
task1._parameters = {}

def task2(context):
    pass
task2._is_workflow_task = True
task2._requires = {"input1": int}
task2._provides = {"output2": int}
task2._parameters = {}
""")

    # Create second file with tasks
    file2 = tmp_path / "tasks2.py"
    file2.write_text("""
def task3(context):
    pass
task3._is_workflow_task = True
task3._requires = {}
task3._provides = {"output3": float}
task3._parameters = {"param1": 1.0}
""")

    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 3
    task_names = {t["name"] for t in tasks}
    assert task_names == {"task1", "task2", "task3"}

def test_scan_directory_with_docstrings():
    """Test scanning tasks with docstrings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        task_file = Path(tmpdir) / "tasks.py"
        task_file.write_text("""
def documented_task(context):
    \"\"\"This is a test docstring.\"\"\"
    pass
documented_task._is_workflow_task = True
documented_task._requires = {}
documented_task._provides = {}
documented_task._parameters = {}
documented_task._description = "Custom description"
""")

        tasks = WorkflowScanner.scan_directory(tmpdir)
        assert len(tasks) == 1
        assert tasks[0]["description"] == "Custom description"

def test_scan_directory_with_complex_types():
    """Test scanning tasks with complex type annotations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        task_file = Path(tmpdir) / "tasks.py"
        task_file.write_text("""
from typing import List, Dict, Optional

def complex_task(context):
    pass
complex_task._is_workflow_task = True
complex_task._requires = {"list_input": list, "dict_input": dict}
complex_task._provides = {"output": dict}
complex_task._parameters = {"complex_param": {"key": "value"}}
""")

        tasks = WorkflowScanner.scan_directory(tmpdir)
        assert len(tasks) == 1
        task = tasks[0]
        assert task["requires"] == [
            {"name": "list_input", "type": "list"},
            {"name": "dict_input", "type": "dict"}
        ]
        assert task["provides"] == [{"name": "output", "type": "dict"}]

def test_scan_directory_with_syntax_errors(tmp_path):
    """Test scanning files with syntax errors."""
    # Create file with valid task
    valid_file = tmp_path / "valid.py"
    valid_file.write_text("""
def valid_task(context):
    pass
valid_task._is_workflow_task = True
valid_task._requires = {}
valid_task._provides = {}
valid_task._parameters = {}
""")

    # Create file with syntax error
    invalid_file = tmp_path / "invalid.py"
    invalid_file.write_text("""
def invalid_task(context):
    this is not valid python
    pass
invalid_task._is_workflow_task = True
""")

    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 1
    assert tasks[0]["name"] == "valid_task"

def test_scan_directory_with_import_errors(tmp_path):
    """Test scanning files with import errors."""
    task_file = tmp_path / "tasks.py"
    task_file.write_text("""
from nonexistent_module import NonexistentClass

def task_with_imports(context):
    pass
task_with_imports._is_workflow_task = True
task_with_imports._requires = {}
task_with_imports._provides = {}
task_with_imports._parameters = {}
""")

    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    assert len(tasks) == 0

def test_scan_directory_with_duplicate_task_names(tmp_path):
    """Test scanning directory with duplicate task names in different files."""
    file1 = tmp_path / "tasks1.py"
    file1.write_text("""
def duplicate_task(context):
    pass
duplicate_task._is_workflow_task = True
duplicate_task._requires = {}
duplicate_task._provides = {"output1": str}
duplicate_task._parameters = {}
""")

    file2 = tmp_path / "tasks2.py"
    file2.write_text("""
def duplicate_task(context):
    pass
duplicate_task._is_workflow_task = True
duplicate_task._requires = {}
duplicate_task._provides = {"output2": str}
duplicate_task._parameters = {}
""")

    tasks = WorkflowScanner.scan_directory(str(tmp_path))
    # Both tasks should be included as they're in different files
    assert len(tasks) == 2
    outputs = {t["provides"][0]["name"] for t in tasks if t["name"] == "duplicate_task"}
    assert outputs == {"output1", "output2"}

def test_scan_directory_with_empty_metadata():
    """Test scanning tasks with empty metadata attributes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        task_file = Path(tmpdir) / "tasks.py"
        task_file.write_text("""
def minimal_task(context):
    pass
minimal_task._is_workflow_task = True
""")

        tasks = WorkflowScanner.scan_directory(tmpdir)
        assert len(tasks) == 1
        task = tasks[0]
        assert task["requires"] == []
        assert task["provides"] == []
        assert task["parameters"] == []
        assert task["description"] == "" 