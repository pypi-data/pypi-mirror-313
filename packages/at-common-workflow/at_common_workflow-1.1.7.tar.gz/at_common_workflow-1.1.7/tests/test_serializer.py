import pytest
from at_common_workflow.core.serializer import WorkflowSerializer, TaskSerializer
from at_common_workflow.core.workflow import Workflow
from at_common_workflow.core.task import task
from at_common_workflow.core.context import Context
from at_common_workflow.core.schema import InputSchema, OutputSchema, Input
import tempfile
import os
import json

# Helper task for testing
@task(
    name="test_task",
    description="A test task",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"output": str})
)
async def sample_task(context: Context):
    context["output"] = f"Processed: {context['input']}"

@task(
    name="task1",
    requires=InputSchema({"input": str}),
    provides=OutputSchema({"intermediate": str})
)
async def first_task(context: Context):
    context["intermediate"] = f"First: {context['input']}"

@task(
    name="task2",
    requires=InputSchema({"intermediate": str}),
    provides=OutputSchema({"output": str})
)
async def second_task(context: Context):
    context["output"] = f"Second: {context['intermediate']}"

def test_serialize_task():
    task_instance = sample_task
    workflow = Workflow(
        name="test_workflow",
        description="test_workflow",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
    )
    workflow.add_task(task_instance)
    
    serialized = TaskSerializer.serialize_task(workflow.tasks["test_task"])
    
    assert serialized["callable_module"] == sample_task.__module__
    assert serialized["callable_name"] == "sample_task"

def test_serialize_deserialize_type():
    test_types = [str, int, float, bool, list, dict]
    
    for type_obj in test_types:
        serialized = WorkflowSerializer.serialize_type(type_obj)
        deserialized = WorkflowSerializer.deserialize_type(serialized)
        assert deserialized == type_obj

def test_serialize_deserialize_schema():
    schema = {
        "str_field": str,
        "int_field": int,
        "bool_field": bool
    }
    
    serialized = WorkflowSerializer.serialize_schema(schema)
    deserialized = WorkflowSerializer.deserialize_schema(serialized)
    
    assert deserialized == schema

def test_save_load_workflow():
    workflow = Workflow(
        name="test_workflow",
        description="test_workflow",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
    )
    workflow.add_task(sample_task)
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        try:
            # Save workflow
            WorkflowSerializer.save_workflow(workflow, tmp.name)
            
            # Load workflow
            loaded_workflow = WorkflowSerializer.load_workflow(tmp.name)
            
            # Verify loaded workflow
            assert loaded_workflow.name == workflow.name
            assert loaded_workflow.input_schema == workflow.input_schema
            assert loaded_workflow.output_schema == workflow.output_schema
            assert "test_task" in loaded_workflow.tasks
            
            loaded_task = loaded_workflow.tasks["test_task"]
            assert loaded_task.name == "test_task"
            assert loaded_task.description == "A test task"
            assert loaded_task.requires == InputSchema({"input": str})
            assert loaded_task.provides == OutputSchema({"output": str})
        finally:
            os.unlink(tmp.name)

def test_invalid_type_deserialization():
    with pytest.raises(ValueError):
        WorkflowSerializer.deserialize_type("invalid_type")

@pytest.mark.asyncio
async def test_deserialized_workflow_execution():
    workflow = Workflow(
        name="test_workflow",
        description="test_workflow",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
    )
    workflow.add_task(sample_task)
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        try:
            # Save and reload workflow
            WorkflowSerializer.save_workflow(workflow, tmp.name)
            loaded_workflow = WorkflowSerializer.load_workflow(tmp.name)
            
            # Execute loaded workflow with Input instance
            result = await loaded_workflow.execute(Input({"input": "test"}))
            
            assert result["output"] == "Processed: test"
        finally:
            os.unlink(tmp.name)

def test_serialize_workflow_with_parameters():
    @task(
        name="param_task",
        parameters={"multiplier": 2},
        requires=InputSchema({"number": int}),
        provides=OutputSchema({"result": int})
    )
    async def task_with_params(context: Context, multiplier: int):
        context["result"] = context["number"] * multiplier
    
    workflow = Workflow(
        name="param_workflow",
        description="test_workflow",
        input_schema=InputSchema({"number": int}),
        output_schema=OutputSchema({"result": int})
    )
    workflow.add_task(task_with_params)
    
    serialized = WorkflowSerializer.serialize_workflow(workflow)
    
    # Find the task with the name "param_task"
    param_task = next((task for task in serialized["tasks"] if task["callable_name"] == "task_with_params"), None)
    assert param_task is not None
    assert param_task["callable_name"] == "task_with_params"

def test_malformed_json():
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        try:
            # Write invalid JSON
            tmp.write(b"{invalid json}")
            tmp.flush()
            
            with pytest.raises(json.JSONDecodeError):
                WorkflowSerializer.load_workflow(tmp.name)
        finally:
            os.unlink(tmp.name)

def test_serialize_task_with_none_parameters():
    @task(
        name="none_param_task",
        parameters=None,
        requires=InputSchema({"input": str}),
        provides=OutputSchema({"output": str})
    )
    async def task_with_none_params(context: Context):
        context["output"] = context["input"]
    
    workflow = Workflow(
        name="test_workflow",
        description="test_workflow",
        input_schema=InputSchema({}),
        output_schema=OutputSchema({})
    )
    workflow.add_task(task_with_none_params)
    
    serialized = TaskSerializer.serialize_task(workflow.tasks["none_param_task"])
    assert serialized["callable_name"] == "task_with_none_params"

def test_serialize_complex_nested_parameters():
    complex_params = {
        "nested": {
            "value": 42,
            "list": [1, 2, 3],
            "dict": {"key": "value"}
        },
        "array": [{"a": 1}, {"b": 2}]
    }
    
    @task(
        name="complex_param_task",
        parameters=complex_params,
        requires=InputSchema({"input": dict}),
        provides=OutputSchema({"output": dict})
    )
    async def task_with_complex_params(context: Context):
        pass
    
    workflow = Workflow(
        name="test_workflow",
        description="test_workflow",
        input_schema=InputSchema({}),
        output_schema=OutputSchema({})
    )
    workflow.add_task(task_with_complex_params)
    
    serialized = TaskSerializer.serialize_task(workflow.tasks["complex_param_task"])
    assert serialized["callable_name"] == "task_with_complex_params"

def test_load_nonexistent_workflow():
    with pytest.raises(FileNotFoundError):
        WorkflowSerializer.load_workflow("nonexistent_file.json")

def test_load_function_errors():
    with pytest.raises(ValueError):
        TaskSerializer.load_function("nonexistent_module", "nonexistent_function")
    
    with pytest.raises(ValueError):
        TaskSerializer.load_function("os", "nonexistent_function")

@pytest.mark.asyncio
async def test_workflow_with_multiple_tasks():
    workflow = Workflow(
        name="multi_task_workflow",
        description="multi_task_workflow",
        input_schema=InputSchema({"input": str}),
        output_schema=OutputSchema({"output": str})
    )
    workflow.add_task(first_task)
    workflow.add_task(second_task)
    
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        try:
            WorkflowSerializer.save_workflow(workflow, tmp.name)
            loaded_workflow = WorkflowSerializer.load_workflow(tmp.name)
            
            assert len(loaded_workflow.tasks) == 2
            assert "task1" in loaded_workflow.tasks
            assert "task2" in loaded_workflow.tasks
            
            result = await loaded_workflow.execute(Input({"input": "test"}))
            assert result["output"] == "Second: First: test"
        finally:
            os.unlink(tmp.name)

def test_serialize_type_edge_cases():
    # Test None type serialization
    serialized = WorkflowSerializer.serialize_type(type(None))
    assert serialized == "NoneType"
    
    # Test custom class type
    class CustomType:
        pass
    
    serialized_custom = WorkflowSerializer.serialize_type(CustomType)
    assert isinstance(serialized_custom, str)

def test_deserialize_invalid_schema():
    invalid_schema = {"field": "InvalidType"}
    with pytest.raises(ValueError, match="Unknown type: InvalidType"):
        WorkflowSerializer.deserialize_schema(invalid_schema)

def test_workflow_serialization_with_empty_tasks():
    workflow = Workflow(
        name="empty_workflow",
        description="empty_workflow",
        input_schema=InputSchema({}),
        output_schema=OutputSchema({})
    )
    
    serialized = WorkflowSerializer.serialize_workflow(workflow)
    assert serialized["tasks"] == []  # Check for an empty list
    assert serialized["name"] == "empty_workflow"
    assert serialized["input_schema"] == {}
    assert serialized["output_schema"] == {}
