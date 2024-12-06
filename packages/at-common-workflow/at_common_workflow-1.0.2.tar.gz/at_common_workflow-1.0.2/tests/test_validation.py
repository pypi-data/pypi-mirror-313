import pytest
from src import CircularDependencyError, DependencyNotFoundError
from src.utils.validation import validate_dag
from src.core.task import Task, TaskParameters
from src.core.context import Context
from src.core.io import Input, Output, InputSchema, OutputSchema
from src.utils.validation import validate_schema

def test_validate_complex_dag():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),
        "task2": Task(name="task2", description="task2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str}), provides=OutputSchema({"data2": str})),
        "task3": Task(name="task3", description="task3 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data2": str}), provides=OutputSchema({"data3": str})),
        "task4": Task(name="task4", description="task4 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str, "data3": str}), provides=OutputSchema({}))
    }
    
    validate_dag(tasks, context)

def test_validate_self_dependency():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str}), provides=OutputSchema({"data1": str}))
    }
    
    with pytest.raises(CircularDependencyError):
        validate_dag(tasks, context)

def test_validate_multiple_dependencies():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"nonexistent1": str, "nonexistent2": str}), provides=OutputSchema({}))
    }
    
    with pytest.raises(DependencyNotFoundError) as exc:
        validate_dag(tasks, context)
    # Should mention both missing dependencies in error message
    assert "nonexistent1" in str(exc.value)
    assert "nonexistent2" in str(exc.value)

def test_validate_circular_dependency_complex():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),
        "task2": Task(name="task2", description="task2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str, "data4": str}), provides=OutputSchema({"data2": str})),
        "task3": Task(name="task3", description="task3 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data2": str}), provides=OutputSchema({"data3": str})),
        "task4": Task(name="task4", description="task4 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data3": str}), provides=OutputSchema({"data4": str}))
    }
    
    with pytest.raises(CircularDependencyError):
        validate_dag(tasks, context)

def test_validate_empty_tasks():
    context = Context()
    validate_dag({}, context)

def test_validate_no_dependencies():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),
        "task2": Task(name="task2", description="task2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data2": str})),
        "task3": Task(name="task3", description="task3 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data3": str}))
    }
    
    validate_dag(tasks, context)

def test_validate_multiple_providers():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),
        "task2": Task(name="task2", description="task2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),  # Multiple tasks provide same data
        "task3": Task(name="task3", description="task3 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str}), provides=OutputSchema({}))
    }
    
    with pytest.raises(ValueError) as exc:
        validate_dag(tasks, context)

def test_validate_complex_circular():
    def task_func(context): pass
    context = Context()
    tasks = {
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),
        "task2": Task(name="task2", description="task2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data3": str}), provides=OutputSchema({"data2": str})),
        "task3": Task(name="task3", description="task3 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data2": str}), provides=OutputSchema({"data3": str})),
        "task4": Task(name="task4", description="task4 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str, "data2": str}), provides=OutputSchema({}))
    }
    
    with pytest.raises(CircularDependencyError):
        validate_dag(tasks, context)

def test_validate_disconnected_components():
    def task_func(context): pass
    context = Context()
    tasks = {
        # Component 1
        "task1": Task(name="task1", description="task1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data1": str})),
        "task2": Task(name="task2", description="task2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data1": str}), provides=OutputSchema({"data2": str})),
        # Component 2 (disconnected)
        "task3": Task(name="task3", description="task3 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"data3": str})),
        "task4": Task(name="task4", description="task4 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"data3": str}), provides=OutputSchema({"data4": str}))
    }
    
    validate_dag(tasks, context)

def test_validate_complex_branching():
    def task_func(context): pass
    context = Context()
    tasks = {
        "root": Task(name="root", description="root description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({}), provides=OutputSchema({"root_data": str})),
        "branch1_1": Task(name="branch1_1", description="branch1_1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"root_data": str}), provides=OutputSchema({"b1_data": str})),
        "branch1_2": Task(name="branch1_2", description="branch1_2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"b1_data": str}), provides=OutputSchema({"b1_final": str})),
        "branch2_1": Task(name="branch2_1", description="branch2_1 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"root_data": str}), provides=OutputSchema({"b2_data": str})),
        "branch2_2": Task(name="branch2_2", description="branch2_2 description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"b2_data": str}), provides=OutputSchema({"b2_final": str})),
        "merger": Task(name="merger", description="merger description", func=task_func, parameters=TaskParameters({}), requires=InputSchema({"b1_final": str, "b2_final": str}), provides=OutputSchema({"final": str}))
    }
    
    validate_dag(tasks, context)

def test_validate_schema_valid_input():
    input = Input({"name": "test", "age": 25})
    schema = {"name": str, "age": int}
    validate_schema(input, schema, "input")

def test_validate_schema_valid_output():
    output = Output({"result": "success", "count": 42})
    schema = {"result": str, "count": int}
    validate_schema(output, schema, "output")

def test_validate_schema_invalid_type():
    input = Input({"name": 123})
    schema = {"name": str}
    
    with pytest.raises(ValueError) as exc:
        validate_schema(input, schema, "input")
    assert "not of the correct type" in str(exc.value)

def test_validate_schema_missing_keys():
    output = Output({"partial": "data"})
    schema = {"partial": str, "missing": int}
    
    with pytest.raises(ValueError) as exc:
        validate_schema(output, schema, "output")
    assert "Missing required output keys" in str(exc.value)

def test_validate_schema_extra_keys():
    input = Input({"defined": "value", "extra": "not_in_schema"})
    schema = {"defined": str}
    
    with pytest.raises(ValueError) as exc:
        validate_schema(input, schema, "input")
    assert "is not defined in the input schema" in str(exc.value)

def test_validate_schema_invalid_input_type():
    invalid = {"not": "an_input_object"}  # Plain dict instead of Input
    schema = {"not": str}
    
    with pytest.raises(ValueError) as exc:
        validate_schema(invalid, schema, "input")
    assert "must be an instance of Input class" in str(exc.value)