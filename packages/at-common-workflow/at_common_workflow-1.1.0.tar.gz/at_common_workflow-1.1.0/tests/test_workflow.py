import pytest
from src.core.workflow import Workflow
from src.core.io import InputSchema, OutputSchema, Input
from src.core.task import task, TaskStatus, TaskProgress
from src.core.context import Context
import time, asyncio
from src.exceptions.workflow_exceptions import DependencyNotFoundError

# Helper tasks for testing
@task(
    name="task_a",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"a_output": str})
)
async def task_a(context: Context):
    context["a_output"] = context["input"] + "_a"

@task(
    name="task_b",
    requires=InputSchema({"a_output": str}),
    provides=OutputSchema({"b_output": str})
)
async def task_b(context: Context):
    context["b_output"] = context["a_output"] + "_b"

@task(
    name="task_c",
    requires=InputSchema({"b_output": str}),
    provides=OutputSchema({"output": str})
)
async def task_c(context: Context):
    context["output"] = context["b_output"] + "_c"

# Test Cases

@pytest.mark.asyncio
async def test_linear_dependency_chain():
    """Test tasks executing in correct order based on dependencies."""
    workflow = Workflow(
        "linear_chain",
        InputSchema({"input": str}),
        OutputSchema({"output": str})
    )
    
    workflow.add_task(task_c)  # Add in reverse order to test dependency resolution
    workflow.add_task(task_b)
    workflow.add_task(task_a)
    
    result = await workflow.execute(Input({"input": "start"}))
    assert result["output"] == "start_a_b_c"

@pytest.mark.asyncio
async def test_missing_required_task():
    """Test error when dependency chain is broken."""
    workflow = Workflow(
        "missing_dep",
        InputSchema({"input": str}),
        OutputSchema({"output": str})
    )
    
    workflow.add_task(task_c)
    workflow.add_task(task_a)
    # Deliberately skip task_b
    
    with pytest.raises(DependencyNotFoundError) as exc_info:
        await workflow.execute(Input({"input": "start"}))
    
    # Verify the error message
    assert "Task 'task_c' requires keys {'b_output'}" in str(exc_info.value)
    assert "which are not provided by any task" in str(exc_info.value)

@pytest.mark.asyncio
async def test_task_error_handling():
    """Test proper error handling when a task fails."""
    @task(
        name="failing_task",
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"output": str})
    )
    async def failing_task(context: Context):
        raise ValueError("Task failed deliberately")

    workflow = Workflow(
        "error_handling",
        InputSchema({"input": str}),
        OutputSchema({"output": str})
    )
    workflow.add_task(failing_task)

    progress_events = []
    def track_progress(progress):
        progress_events.append((progress.name, progress.status))

    with pytest.raises(ValueError):
        await workflow.execute(Input({"input": "start"}), track_progress)
    
    assert any(status == TaskStatus.FAILED for _, status in progress_events)

@pytest.mark.asyncio
async def test_concurrent_task_execution():
    """Test multiple tasks executing concurrently when possible."""
    @task(
        name="parallel_1",
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"out1": str})
    )
    async def parallel_1(context: Context):
        await asyncio.sleep(0.1)
        context["out1"] = context["input"] + "_1"

    @task(
        name="parallel_2",
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"out2": str})
    )
    async def parallel_2(context: Context):
        await asyncio.sleep(0.1)
        context["out2"] = context["input"] + "_2"

    @task(
        name="final",
        requires=InputSchema({"out1": str, "out2": str}),
        provides=OutputSchema({"output": str})
    )
    async def final(context: Context):
        context["output"] = f"{context['out1']}_{context['out2']}"

    workflow = Workflow(
        "concurrent",
        InputSchema({"input": str}),
        OutputSchema({"output": str})
    )
    
    workflow.add_task(parallel_1)
    workflow.add_task(parallel_2)
    workflow.add_task(final)

    start_time = time.time()
    result = await workflow.execute(Input({"input": "start"}))
    duration = time.time() - start_time

    # Should take ~0.1s, not ~0.2s if truly parallel
    assert duration < 0.15
    assert "start_1" in result["output"]
    assert "start_2" in result["output"]

@pytest.mark.asyncio
async def test_schema_validation():
    workflow = Workflow(
        "validation_test",
        InputSchema({"input": str}),
        OutputSchema({"output": str})
    )

    # Test duplicate task names
    @task(name="same_name")
    async def task1(context: Context):
        pass

    @task(name="same_name")
    async def task2(context: Context):
        pass

    workflow.add_task(task1)
    with pytest.raises(ValueError):
        workflow.add_task(task2)

    # Test invalid input schema
    with pytest.raises(Exception):
        await workflow.execute({"wrong_input": "value"})

@pytest.mark.asyncio
async def test_input_output_schema_validation():
    """Test validation of input and output schemas."""
    workflow = Workflow(
        "schema_validation",
        InputSchema({"input": int}),  # Expect integer input
        OutputSchema({"output": str})
    )
    
    @task(
        name="type_conversion",
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"output": str})
    )
    async def convert_task(context: Context):
        context["output"] = str(context["input"])
    
    workflow.add_task(convert_task)
    
    # Test wrong input type - updated to expect ValueError
    with pytest.raises(ValueError, match="Input value for key 'input' is not of the correct type"):
        await workflow.execute(Input({"input": "not_an_integer"}))
    
    # Test missing required input
    with pytest.raises(ValueError, match="Missing required input keys"):
        await workflow.execute(Input({"wrong_key": 42}))
    
    # Test successful type conversion
    result = await workflow.execute(Input({"input": 42}))
    assert result["output"] == "42"

@pytest.mark.asyncio
async def test_detailed_progress_tracking():
    """Test detailed progress tracking through callbacks."""
    workflow = Workflow(
        "progress_test",
        InputSchema({"input": str}),
        OutputSchema({"output": str})
    )
    
    workflow.add_task(task_a)
    workflow.add_task(task_b)
    workflow.add_task(task_c)
    
    progress_log = []
    def track_progress(progress: TaskProgress):
        progress_log.append((progress.name, progress.status))
    
    result = await workflow.execute(Input({"input": "start"}), track_progress)
    
    # Verify progress sequence
    assert any(name == "task_a" and status == TaskStatus.RUNNING for name, status in progress_log)
    assert any(name == "task_a" and status == TaskStatus.COMPLETED for name, status in progress_log)
    assert any(name == "task_b" and status == TaskStatus.RUNNING for name, status in progress_log)
    assert any(name == "task_b" and status == TaskStatus.COMPLETED for name, status in progress_log)
    assert any(name == "task_c" and status == TaskStatus.RUNNING for name, status in progress_log)
    assert any(name == "task_c" and status == TaskStatus.COMPLETED for name, status in progress_log)