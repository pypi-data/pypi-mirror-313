import pytest
from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.schema import InputSchema, OutputSchema, Input
from at_common_workflow.core.task import task, TaskStatus, TaskProgress, TaskParameter, Task
from at_common_workflow.core.context import Context
import time, asyncio
from at_common_workflow.exceptions.workflow_exceptions import DependencyNotFoundError, CircularDependencyError, TaskExecutionError

# Helper tasks for testing
@task(
    name="task_a",
    requires={"input": str},
    provides={"a_output": str}
)
async def task_a(context: Context):
    context["a_output"] = context["input"] + "_a"

@task(
    name="task_b",
    requires={"a_output": str},
    provides={"b_output": str}
)
async def task_b(context: Context):
    context["b_output"] = context["a_output"] + "_b"

@task(
    name="task_c",
    requires={"b_output": str},
    provides={"output": str}
)
async def task_c(context: Context):
    context["output"] = context["b_output"] + "_c"

# Test Cases

@pytest.mark.asyncio
async def test_linear_dependency_chain():
    """Test tasks executing in correct order based on dependencies."""
    workflow = Workflow(
        name="linear_chain",
        description="linear_chain",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
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
        name="missing_dep",
        description="missing_dep",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
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
        description="failing_task",
        requires={"input": str},
        provides={"output": str}
    )
    async def failing_task(context: Context):
        raise ValueError("Task failed deliberately")

    workflow = Workflow(
        name="error_handling",
        description="error_handling",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
    )
    workflow.add_task(failing_task)

    progress_events = []
    def track_progress(progress):
        progress_events.append((progress.name, progress.status))

    # Update the expected exception type to TaskExecutionError
    with pytest.raises(TaskExecutionError):
        await workflow.execute(Input({"input": "start"}), track_progress)
    
    assert any(status == TaskStatus.FAILED for _, status in progress_events)

@pytest.mark.asyncio
async def test_concurrent_task_execution():
    """Test multiple tasks executing concurrently when possible."""
    @task(
        name="parallel_1",
        requires={"input": str},
        provides={"out1": str}
    )
    async def parallel_1(context: Context):
        await asyncio.sleep(0.1)
        context["out1"] = context["input"] + "_1"

    @task(
        name="parallel_2",
        requires={"input": str},
        provides={"out2": str}
    )
    async def parallel_2(context: Context):
        await asyncio.sleep(0.1)
        context["out2"] = context["input"] + "_2"

    @task(
        name="final",
        requires={"out1": str, "out2": str},
        provides={"output": str}
    )
    async def final(context: Context):
        context["output"] = f"{context['out1']}_{context['out2']}"

    workflow = Workflow(
        name="concurrent",
        description="concurrent",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
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
        name="validation_test",
        description="validation_test",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
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
        name="schema_validation",
        description="schema_validation",
        input_schema=InputSchema({"input": int}),  # Expect integer input
        output_schema=OutputSchema({"output": str})
    )
    
    @task(
        name="type_conversion",
        requires={"input": int},
        provides={"output": str}
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
        name="progress_test",
        description="progress_test",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
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

@pytest.mark.asyncio
async def test_workflow_circular_dependency():
    """Test detection of circular dependencies."""
    @task(
        name="task_a",
        requires={"b_output": str},
        provides={"a_output": str}
    )
    async def task_a(context: Context):
        context["a_output"] = f"A processed {context['b_output']}"

    @task(
        name="task_b",
        requires={"a_output": str},
        provides={"b_output": str}
    )
    async def task_b(context: Context):
        context["b_output"] = f"B processed {context['a_output']}"

    workflow = Workflow(
        name="circular_workflow",
        description="circular_workflow",
        input_schema=InputSchema({}),
        output_schema=OutputSchema({"final_output": str})
    )
    
    workflow.add_task(task_a)
    workflow.add_task(task_b)
    
    with pytest.raises(CircularDependencyError, match="Circular dependency detected"):
        await workflow.execute(Input({}))

@pytest.mark.asyncio
async def test_workflow_partial_failure_recovery():
    """Test workflow behavior when some tasks fail but others can continue."""
    @task(
        name="independent_task_1",
        requires={"input": str},
        provides={"output1": str}
    )
    async def task1(context: Context):
        context["output1"] = f"Success: {context['input']}"

    @task(
        name="failing_task",
        requires={"input": str},
        provides={"failed_output": str}
    )
    async def task2(context: Context):
        raise ValueError("Intentional failure")

    @task(
        name="independent_task_2",
        requires={"input": str},
        provides={"output2": str}
    )
    async def task3(context: Context):
        context["output2"] = f"Also success: {context['input']}"

    workflow = Workflow(
        name="partial_failure_workflow",
        description="partial_failure_workflow",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output1": str, "output2": str})
    )
    
    workflow.add_task(task1)
    workflow.add_task(task2)
    workflow.add_task(task3)
    
    # Update the expected exception type to TaskExecutionError
    with pytest.raises(TaskExecutionError):
        await workflow.execute(Input({"input": "test"}))
    
    # Verify that the successful tasks completed
    assert workflow.tasks["independent_task_1"].status == TaskStatus.COMPLETED
    assert workflow.tasks["independent_task_2"].status == TaskStatus.COMPLETED
    assert workflow.tasks["failing_task"].status == TaskStatus.FAILED

@pytest.mark.asyncio
async def test_add_task_with_instance():
    """Test adding tasks using Task instances directly."""
    async def math_task(context: Context, multiplier: int):
        context["result"] = context["number"] * multiplier

    task_instance = Task(
        name="math_task",
        func=math_task,
        description="Math operation",
        parameters=[TaskParameter(name="multiplier", type=int, value=2)],
        requires=InputSchema({"number": int}),
        provides=OutputSchema({"result": int})
    )

    workflow = Workflow(
        name="math_workflow",
        description="math_workflow",
        input_schema=InputSchema({"number": int}),
        output_schema=OutputSchema({"result": int})
    )

    # Add task using Task instance
    workflow.add_task(task_instance)
    
    # Execute workflow
    result = await workflow.execute(Input({"number": 5}))
    assert result["result"] == 10

@pytest.mark.asyncio
async def test_mixed_task_addition():
    """Test workflow with both Task instances and decorated functions."""
    # Create a Task instance
    async def first_operation(context: Context):
        context["intermediate"] = context["input"] * 2

    task1 = Task(
        name="first_task",
        func=first_operation,
        description="First operation",
        parameters=[],
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"intermediate": int})
    )

    # Create a decorated task
    @task(
        name="second_task",
        requires={"intermediate": int},
        provides={"output": int}
    )
    async def second_operation(context: Context):
        context["output"] = context["intermediate"] + 1

    workflow = Workflow(
        name="mixed_workflow",
        description="mixed_workflow",
        input_schema=InputSchema({"input": int}),
        output_schema=OutputSchema({"output": int})
    )

    # Add both types of tasks
    workflow.add_task(task1)
    workflow.add_task(second_operation)

    # Execute workflow
    result = await workflow.execute(Input({"input": 5}))
    assert result["output"] == 11  # (5 * 2) + 1

@pytest.mark.asyncio
async def test_add_task_validation():
    """Test validation when adding tasks to workflow."""
    workflow = Workflow(
        name="validation_workflow",
        description="validation_workflow",
        input_schema=InputSchema({"input": int}),
        output_schema=OutputSchema({"output": int})
    )

    # Test adding non-task, non-decorated function
    async def invalid_func(context: Context):
        pass
    
    with pytest.raises(ValueError, match="Function must be decorated with @task"):
        workflow.add_task(invalid_func)

    # Test adding task with duplicate name
    task1 = Task(
        name="duplicate_task",
        func=lambda ctx: None,
        description="First task",
        parameters=[],
        requires=InputSchema({}),
        provides=OutputSchema({})
    )
    
    task2 = Task(
        name="duplicate_task",
        func=lambda ctx: None,
        description="Second task",
        parameters=[],
        requires=InputSchema({}),
        provides=OutputSchema({})
    )
    
    workflow.add_task(task1)
    with pytest.raises(ValueError, match="Task 'duplicate_task' already exists"):
        workflow.add_task(task2)

@pytest.mark.asyncio
async def test_add_task_duplicate_outputs():
    """Test validation of duplicate outputs between tasks."""
    workflow = Workflow(
        name="duplicate_outputs",
        description="duplicate_outputs",
        input_schema=InputSchema({"input": int}),
        output_schema=OutputSchema({"result": int})
    )

    # Create two tasks that provide the same output
    task1 = Task(
        name="first_provider",
        func=lambda ctx: None,
        description="First provider",
        parameters=[],
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"result": int})
    )
    
    task2 = Task(
        name="second_provider",
        func=lambda ctx: None,
        description="Second provider",
        parameters=[],
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"result": int})
    )
    
    workflow.add_task(task1)
    with pytest.raises(ValueError, match="provide the same outputs"):
        workflow.add_task(task2)

@pytest.mark.asyncio
async def test_add_task_complex_parameters():
    """Test adding tasks with complex parameter configurations."""
    workflow = Workflow(
        name="complex_params",
        description="complex_params",
        input_schema=InputSchema({"input": dict}),
        output_schema=OutputSchema({"output": dict})
    )

    async def complex_task(context: Context, config: dict, options: list):
        pass

    task_instance = Task(
        name="complex_task",
        func=complex_task,
        description="Complex parameter task",
        parameters=[
            TaskParameter(name="config", type=dict, value={"key": "value"}),
            TaskParameter(name="options", type=list, value=[1, 2, 3])
        ],
        requires=InputSchema({"input": dict}),
        provides=OutputSchema({"output": dict})
    )

    workflow.add_task(task_instance)
    assert "complex_task" in workflow.tasks
    assert len(workflow.tasks["complex_task"].parameters) == 2

@pytest.mark.asyncio
async def test_add_task_inheritance():
    """Test adding tasks that inherit from Task class."""
    class CustomTask(Task):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.custom_attribute = "custom"

    async def custom_func(context: Context):
        context["output"] = context["input"] * 2

    custom_task = CustomTask(
        name="custom_task",
        func=custom_func,
        description="Custom task implementation",
        parameters=[],
        requires=InputSchema({"input": int}),
        provides=OutputSchema({"output": int})
    )

    workflow = Workflow(
        name="inheritance_workflow",
        description="inheritance_workflow",
        input_schema=InputSchema({"input": int}),
        output_schema=OutputSchema({"output": int})
    )

    workflow.add_task(custom_task)
    assert isinstance(workflow.tasks["custom_task"], CustomTask)
    assert workflow.tasks["custom_task"].custom_attribute == "custom"

    result = await workflow.execute(Input({"input": 5}))
    assert result["output"] == 10

@pytest.mark.asyncio
async def test_add_task_none_parameters():
    """Test adding tasks with None parameters."""
    workflow = Workflow(
        name="none_params",
        description="none_params",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
    )

    # Create task with no parameters
    async def simple_task(context: Context):
        context["output"] = context["input"].upper()

    task_instance = Task(
        name="simple_task",
        func=simple_task,
        description="Simple task",
        parameters=None,  # Test None parameters
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"output": str})
    )

    workflow.add_task(task_instance)
    result = await workflow.execute(Input({"input": "test"}))
    assert result["output"] == "TEST"