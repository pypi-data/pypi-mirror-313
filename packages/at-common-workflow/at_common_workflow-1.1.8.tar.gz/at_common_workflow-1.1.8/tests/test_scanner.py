from at_common_workflow.core.scanner import TaskScanner
import tempfile
import os

def test_scanner():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test module file
        with open(os.path.join(tmpdir, "test_module.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema

@task(
    name="test_task",
    description="Test task",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"output": str})
)
async def test_task(context: Context):
    context["output"] = f"Processed: {context['input']}"
""")

        # Scan the directory
        tasks = TaskScanner.scan(tmpdir)
        
        assert len(tasks) == 1
        task_info = tasks[0]
        assert task_info["name"] == "test_task"
        assert task_info["description"] == "Test task"
        assert len(task_info["requires"]) == 1
        assert len(task_info["provides"]) == 1

def test_scanner_empty_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create an empty Python file
        with open(os.path.join(tmpdir, "empty.py"), "w") as f:
            f.write("")
        
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 0

def test_scanner_syntax_error():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create file with syntax error
        with open(os.path.join(tmpdir, "syntax_error.py"), "w") as f:
            f.write("""
                def invalid python:
                    print("This is invalid syntax")
            """)
        
        # Should not raise exception, but log error
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 0

def test_scanner_non_task_functions():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "regular_functions.py"), "w") as f:
            f.write("""
                def normal_function():
                    pass
                
                async def async_function():
                    pass
            """)
        
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 0

def test_scanner_nested_directories():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create nested directory structure
        nested_dir = os.path.join(tmpdir, "nested", "dir")
        os.makedirs(nested_dir)
        
        # Create task in nested directory
        with open(os.path.join(nested_dir, "nested_task.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema

@task(
    name="nested_task",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"output": str})
)
async def nested_task(context: Context):
    context["output"] = context["input"]
""".strip())
        
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 1
        assert tasks[0]["name"] == "nested_task"

def test_scanner_multiple_tasks():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "multiple_tasks.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema

@task(
    name="task1",
    requires=InputSchema({"input1": str}),
    provides=OutputSchema({"output1": str})
)
async def task1(context: Context):
    context["output1"] = context["input1"]

@task(
    name="task2",
    requires=InputSchema({"input2": int}),
    provides=OutputSchema({"output2": int})
)
async def task2(context: Context):
    context["output2"] = context["input2"]
            """)
        
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 2
        task_names = {t["name"] for t in tasks}
        assert task_names == {"task1", "task2"}

def test_scanner_missing_attributes():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "missing_attrs.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task()  # No attributes specified
async def minimal_task(context: Context):
    pass
            """)
        
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 1
        task_info = tasks[0]
        assert task_info["name"] == "minimal_task"
        assert task_info["requires"] == []
        assert task_info["provides"] == []

def test_scanner_invalid_type_annotations():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "invalid_types.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema
from typing import Any

@task(
    name="invalid_types_task",
    requires=InputSchema({"input": Any}),
    provides=OutputSchema({"output": Any})
)
async def invalid_types_task(context: Context):
    pass
            """)
        
        tasks = TaskScanner.scan(tmpdir)
        assert len(tasks) == 1
        task_info = tasks[0]
        assert task_info["requires"][0]["type"] == "Any"
        assert task_info["provides"][0]["type"] == "Any"

def test_load_existing_task():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test module file
        with open(os.path.join(tmpdir, "test_module.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema

@task(
    name="test_task",
    description="Test task",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"output": str})
)
async def test_task(context: Context):
    context["output"] = f"Processed: {context['input']}"
""")

        # Load the task
        task = TaskScanner.load("test_task", tmpdir)
        
        assert task is not None
        assert task.name == "test_task"
        assert task.description == "Test task"
        assert task.requires == {"input": str}
        assert task.provides == {"output": str}
        assert callable(task.func)

def test_load_nonexistent_task():
    with tempfile.TemporaryDirectory() as tmpdir:
        task = TaskScanner.load("nonexistent_task", tmpdir)
        assert task is None

def test_load_from_nested_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_dir = os.path.join(tmpdir, "nested", "dir")
        os.makedirs(nested_dir)
        
        with open(os.path.join(nested_dir, "nested_task.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema

@task(
    name="nested_task",
    description="Nested task",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"output": str})
)
async def nested_task(context: Context):
    context["output"] = context["input"]
""")

        task = TaskScanner.load("nested_task", tmpdir)
        assert task is not None
        assert task.name == "nested_task"
        assert task.description == "Nested task"

def test_load_with_syntax_error():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "bad_syntax.py"), "w") as f:
            f.write("""
                def invalid python:
                    print("This is invalid syntax")
            """)
            
        task = TaskScanner.load("any_task", tmpdir)
        assert task is None

def test_load_with_multiple_tasks_same_name():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two files with tasks of the same name
        with open(os.path.join(tmpdir, "task1.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task(name="duplicate_task")
async def task1(context: Context):
    pass
""")
        
        with open(os.path.join(tmpdir, "task2.py"), "w") as f:
            f.write("""
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context

@task(name="duplicate_task")
async def task2(context: Context):
    pass
""")

        # Should return the first task found
        task = TaskScanner.load("duplicate_task", tmpdir)
        assert task is not None
        assert task.name == "duplicate_task"