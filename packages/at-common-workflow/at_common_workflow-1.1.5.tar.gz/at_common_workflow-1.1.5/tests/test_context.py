import pytest
from at_common_workflow.core.context import Context
from threading import Thread, Event
import time

def test_context_basic_operations():
    context = Context()
    
    # Test empty context
    assert len(context) == 0
    assert not context
    
    # Test basic set/get
    context["key"] = "value"
    assert context["key"] == "value"
    assert len(context) == 1
    assert bool(context) is True

def test_context_deep_copy_operations():
    context = Context()
    
    # Test nested dictionary
    nested_dict = {
        "level1": {
            "level2": {
                "level3": [1, 2, {"a": "b"}]
            }
        }
    }
    
    context["nested"] = nested_dict
    retrieved = context["nested"]
    
    # Modify original data
    nested_dict["level1"]["level2"]["level3"][2]["a"] = "modified"
    
    # Verify context maintains original value
    assert context["nested"]["level1"]["level2"]["level3"][2]["a"] == "b"
    
    # Verify retrieved data is independent
    retrieved["level1"]["level2"]["level3"][2]["a"] = "changed"
    assert context["nested"]["level1"]["level2"]["level3"][2]["a"] == "b"

def test_context_concurrent_access():
    context = Context()
    event = Event()
    errors = []
    
    def writer(id: int):
        try:
            for i in range(100):
                context[f"writer{id}_{i}"] = {"value": i}
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)
    
    def reader(id: int):
        try:
            while not event.is_set():
                keys = list(context.keys())
                for key in keys:
                    if key in context:
                        value = context[key]
                        assert isinstance(value, dict)
                        assert "value" in value
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)

    # Create multiple readers and writers
    writers = [Thread(target=writer, args=(i,)) for i in range(3)]
    readers = [Thread(target=reader, args=(i,)) for i in range(3)]
    
    # Start all threads
    for t in readers + writers:
        t.start()
    
    # Wait for writers to complete
    for w in writers:
        w.join()
    
    # Signal readers to stop and wait for them
    event.set()
    for r in readers:
        r.join()
    
    assert not errors, f"Encountered errors: {errors}"

def test_context_dictionary_methods():
    context = Context()
    
    # Test setdefault
    value = context.setdefault("key1", {"default": "value"})
    assert value == {"default": "value"}
    assert context["key1"] == {"default": "value"}
    
    # Test get with default
    assert context.get("nonexistent", "default") == "default"
    
    # Test pop
    context["temp"] = "temp_value"
    assert context.pop("temp") == "temp_value"
    assert "temp" not in context
    
    # Test update
    context.update({"a": 1, "b": [1, 2, 3]})
    assert context["a"] == 1
    assert context["b"] == [1, 2, 3]

def test_context_type_validation():
    context = Context()
    
    # Test invalid key types
    invalid_keys = [123, 1.23, True, None, ["list"], {"dict": "value"}]
    
    for invalid_key in invalid_keys:
        with pytest.raises(TypeError, match="Key must be a string"):
            context[invalid_key] = "value"
            
        with pytest.raises(TypeError, match="Key must be a string"):
            _ = context[invalid_key]
            
        with pytest.raises(TypeError, match="Key must be a string"):
            invalid_key in context

def test_context_clear_and_bulk_operations():
    context = Context()
    
    # Populate with data
    initial_data = {
        "str_key": "string",
        "list_key": [1, 2, 3],
        "dict_key": {"nested": "value"},
        "tuple_key": (1, 2, 3)
    }
    
    context.update(initial_data)
    assert len(context) == len(initial_data)
    
    # Test clear
    context.clear()
    assert len(context) == 0
    
    # Test bulk update with nested structures
    complex_data = {
        "complex": {
            "list": [{"a": 1}, {"b": 2}],
            "tuple": (1, 2, {"c": 3}),
            "set": {1, 2, 3}
        }
    }
    
    context.update(complex_data)
    assert context["complex"]["list"][0]["a"] == 1
    
    # Modify original data to verify deep copy
    complex_data["complex"]["list"][0]["a"] = 999
    assert context["complex"]["list"][0]["a"] == 1
