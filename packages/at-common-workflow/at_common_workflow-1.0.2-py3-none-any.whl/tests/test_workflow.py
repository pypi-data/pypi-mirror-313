import pytest
import asyncio
from src import Workflow, Input, Output, InputSchema, OutputSchema, \
    Context, TaskStatus, TaskProgress
from src.exceptions.workflow_exceptions import DependencyNotFoundError, CircularDependencyError

# Basic Functionality Tests
async def test_basic_workflow_execution():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"result": str})
    workflow = Workflow("test_basic", input_schema, output_schema)
    
    @workflow.task(
        name="custom_task_name",
        provides=OutputSchema({"result": str})
    )
    async def simple_task(context: 'Context'):
        context["result"] = "done"
    
    progress_events = []
    def progress_callback(progress: TaskProgress):
        progress_events.append(progress)
    
    # Create an Input instance
    input = Input({})
    output = await workflow.execute(input=input, callback=progress_callback)
    
    assert output["result"] == "done"
    assert workflow.tasks["custom_task_name"].status == TaskStatus.COMPLETED
    assert len(progress_events) == 2
    assert progress_events[0] == TaskProgress("custom_task_name", TaskStatus.RUNNING)
    assert progress_events[1] == TaskProgress("custom_task_name", TaskStatus.COMPLETED)

# Dependency Tests
async def test_workflow_dependencies():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"final": str})
    workflow = Workflow("test_deps", input_schema, output_schema)
    
    @workflow.task(name="task1", provides=OutputSchema({"data1": str}))
    async def task1(context: 'Context'):
        context["data1"] = "value1"
    
    @workflow.task(
        name="task2",
        requires=InputSchema({"data1": str}),
        provides=OutputSchema({"data2": str})
    )
    async def task2(context: 'Context'):
        data = context.get("data1")
        context["data2"] = f"{data}_processed"
    
    @workflow.task(
        name="task3",
        requires=InputSchema({"data2": str}),
        provides=OutputSchema({"final": str})
    )
    async def task3(context: 'Context'):
        data = context.get("data2")
        context["final"] = f"{data}_final"
    
    progress_events = []
    def progress_callback(progress: TaskProgress):
        progress_events.append(progress)
    
    input = Input({})
    output = await workflow.execute(input=input, callback=progress_callback)
    assert output["final"] == "value1_processed_final"

# Parallel Execution Tests
async def test_parallel_execution():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_parallel", input_schema, output_schema)
    execution_order = []
    progress_events = []
    
    @workflow.task(
        name="slow_task"
    )
    async def slow_task(context: 'Context'):
        await asyncio.sleep(0.2)
        execution_order.append("slow")
    
    @workflow.task(
        name="fast_task"
    )
    async def fast_task(context: 'Context'):
        await asyncio.sleep(0.1)
        execution_order.append("fast")
    
    def progress_callback(progress: TaskProgress):
        progress_events.append(progress)
    
    input = Input({})
    output = await workflow.execute(input=input, callback=progress_callback)
    assert execution_order == ["fast", "slow"]
    assert len(progress_events) == 4  # 2 tasks * 2 events (STARTED, COMPLETED)
    assert all(isinstance(p, TaskProgress) for p in progress_events)

# Error Handling Tests
async def test_task_failure_propagation():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_error", input_schema, output_schema)
    progress_events = []
    
    @workflow.task(name="failing_task")
    async def failing_task(context: 'Context'):
        raise ValueError("Expected failure")
    
    def progress_callback(progress: TaskProgress):
        progress_events.append(progress)
    
    input = Input({})
    with pytest.raises(ValueError, match="Expected failure"):
        output = await workflow.execute(input=input, callback=progress_callback)
    
    assert workflow.tasks["failing_task"].status == TaskStatus.FAILED
    assert len(progress_events) == 2
    assert progress_events[0] == TaskProgress("failing_task", TaskStatus.RUNNING)
    assert progress_events[1] == TaskProgress("failing_task", TaskStatus.FAILED)

async def test_invalid_dependency():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_invalid_dep", input_schema, output_schema)
    
    @workflow.task(
        name="dependent_task",
        requires=InputSchema({"nonexistent": str})
    )
    async def dependent_task(context: 'Context'):
        pass
    
    with pytest.raises(DependencyNotFoundError):
        input = Input({})
        output = await workflow.execute(input=input)

# Circular Dependency Tests
async def test_circular_dependency_detection():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_circular", input_schema, output_schema)
    
    @workflow.task(
        name="task_a",
        requires=InputSchema({"b": str}),
        provides=OutputSchema({"a": str})
    )
    async def task_a(context: 'Context'):
        pass
    
    @workflow.task(
        name="task_b",
        requires=InputSchema({"a": str}),
        provides=OutputSchema({"b": str})
    )
    async def task_b(context: 'Context'):
        pass
    
    with pytest.raises(CircularDependencyError, match="Circular dependency detected"):
        input = Input({})
        output = await workflow.execute(input=input)

# Context Access Tests
async def test_context_access_patterns():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_context_access", input_schema, output_schema)
    
    @workflow.task(
        name="writer_task",
        provides=OutputSchema({"key1": str})
    )
    async def writer_task(context: 'Context'):
        context["key1"] = "value1"
    
    @workflow.task(
        name="reader_task",
        requires=InputSchema({"key1": str})
    )
    async def reader_task(context: 'Context'):
        assert context.get("key1") == "value1"
        assert "key1" in context
        del context["key1"]
        assert "key1" not in context
    
    input = Input({})
    output = await workflow.execute(input=input)

# Non-async Function Test
async def test_non_async_function():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_non_async", input_schema, output_schema)
    
    @workflow.task(
        name="sync_task"
    )
    def sync_task(context: 'Context'):  # Not async
        pass
    
    input = Input()

    with pytest.raises(ValueError, match="must be async"):
        output = await workflow.execute(input=input)

# Multiple Tasks with Same Provides
async def test_duplicate_provides():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_duplicate", input_schema, output_schema)
    
    @workflow.task(
        name="task1",
        provides=OutputSchema({"data": str})
    )
    async def task1(context: 'Context'):
        context["data"] = "done"
    
    with pytest.raises(ValueError, match="Tasks 'task2' and 'task1' provide the same outputs"):
        @workflow.task(name="task2", provides={"data"})
        async def task2(context: 'Context'):
            pass
    
    input = Input({})
    output = await workflow.execute(input=input)

# Empty Workflow Test
async def test_empty_workflow():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_empty", input_schema, output_schema)
    input = Input({})
    output = await workflow.execute(input=input)
    assert isinstance(output, Output)

# Complex Dependency Chain
async def test_complex_dependency_chain():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"result": str})
    workflow = Workflow("test_complex", input_schema, output_schema)
    execution_order = []
    
    @workflow.task(
        name="task_a",
        provides=OutputSchema({"a": str})
    )
    async def task_a(context: 'Context'):
        execution_order.append("a")
        context["a"] = "a"
    
    @workflow.task(
        name="task_b",
        requires=InputSchema({"a": str}),
        provides=OutputSchema({"b": str})
    )
    async def task_b(context: 'Context'):
        execution_order.append("b")
        context["b"] = context.get("a") + "b"
    
    @workflow.task(
        name="task_c",
        requires=InputSchema({"b": str}),
        provides=OutputSchema({"c": str})
    )
    async def task_c(context: 'Context'):
        execution_order.append("c")
        context["c"] = context.get("b") + "c"
    
    @workflow.task(
        name="task_d",
        requires=InputSchema({"a": str, "c": str}),
        provides=OutputSchema({"result": str})
    )
    async def task_d(context: 'Context'):
        execution_order.append("d")
        context["result"] = context.get("a") + context.get("c")
    
    input = Input({})
    output = await workflow.execute(input=input)
    assert execution_order == ["a", "b", "c", "d"]
    assert output["result"] == "aabc"

# Task Timeout Test
async def test_task_timeout():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_timeout", input_schema, output_schema)
    
    @workflow.task(name="long_running_task")
    async def long_running_task(context: 'Context'):
        await asyncio.sleep(10)  # Simulate long task
    
    input = Input({})
    try:
        await asyncio.wait_for(
            workflow.execute(input=input),
            timeout=1  # Set a timeout shorter than the task's sleep duration
        )
    except asyncio.TimeoutError:
        pass  # This is expected, so we can pass here
    else:
        pytest.fail("Expected asyncio.TimeoutError was not raised")

# Task Cancellation Test
async def test_task_cancellation():
    input_schema = InputSchema({})
    output_schema = OutputSchema({})
    workflow = Workflow("test_cancel", input_schema, output_schema)
    was_cancelled = False
    
    @workflow.task(name="cancellable_task")
    async def cancellable_task(context: 'Context'):
        nonlocal was_cancelled
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            was_cancelled = True
            raise

    input = Input({})
    async def execute_workflow():
        output = await workflow.execute(input=input)

    task = asyncio.create_task(execute_workflow())
    await asyncio.sleep(0.1)
    task.cancel()
    
    with pytest.raises(asyncio.CancelledError):
        await task
    
    assert was_cancelled

async def test_preexisting_context_data():
    input_schema = InputSchema({"pre_existing": str})
    output_schema = OutputSchema({"modified": str})
    workflow = Workflow("test_preexisting", input_schema, output_schema)
      
    @workflow.task(
        name="modify_existing",
        requires=InputSchema({"pre_existing": str}),
        provides=OutputSchema({"modified": str})
    )
    async def modify_existing(context: 'Context'):
        pre_value = context.get("pre_existing")
        context["modified"] = f"{pre_value}_modified"
    
    input = Input({"pre_existing": "initial_value"})
    output = await workflow.execute(input=input)
    assert output["modified"] == "initial_value_modified"

async def test_task_with_parameters():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"result": int})
    workflow = Workflow("test_parameters", input_schema, output_schema)
    
    @workflow.task(
        parameters={"multiplier": 2}
    )
    async def parameterized_task(context: 'Context', multiplier: int):
        context["result"] = 10 * multiplier
    
    input = Input({})
    output = await workflow.execute(input=input)
    assert output["result"] == 20

async def test_multiple_parameters():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"result": str})
    workflow = Workflow("test_multi_params", input_schema, output_schema)
    
    @workflow.task(
        name="complex_params_task",
        parameters={
            "prefix": "test_",
            "suffix": "_done",
            "count": 3
        }
    )
    async def complex_params_task(context: 'Context', prefix: str, suffix: str, count: int):
        result = f"{prefix}" + "x" * count + f"{suffix}"
        context["result"] = result
    
    input = Input({})
    output = await workflow.execute(input=input)
    assert output["result"] == "test_xxx_done"

async def test_parameters_with_dependencies():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"processed": int})
    workflow = Workflow("test_params_deps", input_schema, output_schema)
    
    @workflow.task(
        name="provider_task",
        provides=OutputSchema({"initial": int}),
        parameters={"value": 5}
    )
    async def provider_task(context: 'Context', value: int):
        context["initial"] = value
    
    @workflow.task(
        name="processor_task",
        requires=InputSchema({"initial": int}),
        provides=OutputSchema({"processed": int}),
        parameters={"multiplier": 2}
    )
    async def processor_task(context: 'Context', multiplier: int):
        initial = context.get("initial")
        context["processed"] = initial * multiplier
    
    input = Input({})
    output = await workflow.execute(input=input)
    assert output["processed"] == 10

async def test_missing_parameter():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"result": str})
    workflow = Workflow("test_missing_param", input_schema, output_schema)
    
    @workflow.task(
        name="task_with_required_param",
        parameters={}
    )
    async def task_with_required_param(context: 'Context', required_param: str):
        context["result"] = required_param
    
    with pytest.raises(ValueError, match="Required parameter .* not provided"):
        input = Input({})
        _ = await workflow.execute(input=input)

async def test_parameter_type_handling():
    input_schema = InputSchema({})
    output_schema = OutputSchema({"results": dict})
    workflow = Workflow("test_param_types", input_schema, output_schema)
    
    @workflow.task(
        name="type_check_task",
        parameters={
            "int_param": 42,
            "str_param": "hello",
            "list_param": [1, 2, 3],
            "dict_param": {"key": "value"}
        }
    )
    async def type_check_task(
        context: 'Context',
        int_param: int,
        str_param: str,
        list_param: list,
        dict_param: dict
    ):
        context["results"] = {
            "int": int_param,
            "str": str_param,
            "list": list_param,
            "dict": dict_param
        }
    
    input = Input({})
    output = await workflow.execute(input=input)
    results = output["results"]
    assert isinstance(results["int"], int)
    assert isinstance(results["str"], str)
    assert isinstance(results["list"], list)
    assert isinstance(results["dict"], dict)
