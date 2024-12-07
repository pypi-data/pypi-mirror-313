from typing import Dict, Any
import json
import importlib
from .workflow import Workflow
from .task import Task, TaskFunction
from .schema import InputSchema, OutputSchema

class TaskSerializer:
    """Handles serialization and deserialization of individual tasks."""
    
    @staticmethod
    def serialize_task(task: Task) -> Dict[str, Any]:
        """Convert a Task instance to a serializable dictionary."""
        return {
            'callable_module': task.func.__module__,
            'callable_name': task.func.__name__
        }

    @staticmethod
    def load_function(module_path: str, func_name: str) -> TaskFunction:
        """Dynamically import and return a function."""
        try:
            module = importlib.import_module(module_path)
            return getattr(module, func_name)
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Could not load function {func_name} from module {module_path}: {str(e)}")

    @staticmethod
    def deserialize_task(data: Dict[str, Any]) -> Task:
        """Create a Task instance from serialized data."""
        func = TaskSerializer.load_function(data['callable_module'], data['callable_name'])
        
        # Get task decorator metadata directly from function attributes
        if not hasattr(func, '_is_workflow_task'):
            raise ValueError(f"Function {func.__name__} is not properly decorated with @task")
            
        return Task(
            name=func._name,
            description=func._description,
            func=func,
            parameters=func._parameters,
            requires=func._requires,
            provides=func._provides
        )

class WorkflowSerializer:
    """Handles serialization and deserialization of workflows."""
    
    @staticmethod
    def serialize_type(type_obj):
        """Convert a type object to a serializable string representation."""
        return type_obj.__name__

    @staticmethod
    def deserialize_type(type_str):
        """Convert a type string back to a type object."""
        type_mapping = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'None': type(None)
        }
        type_obj = type_mapping.get(type_str)
        if type_obj is None:
            raise ValueError(f"Unknown type: {type_str}")
        return type_obj

    @staticmethod
    def serialize_schema(schema):
        """Convert a schema dictionary to a serializable format."""
        return {key: WorkflowSerializer.serialize_type(value) 
                for key, value in schema.items()}

    @staticmethod
    def deserialize_schema(schema_data):
        """Convert serialized schema data back to a schema dictionary."""
        return {key: WorkflowSerializer.deserialize_type(value) 
                for key, value in schema_data.items()}

    @staticmethod
    def serialize_workflow(workflow: Workflow) -> Dict[str, Any]:
        """Convert a Workflow instance to a serializable dictionary."""
        return {
            'name': workflow.name,
            'description': workflow.description,
            'tasks': [
                TaskSerializer.serialize_task(task)
                for task in workflow.tasks.values()
            ],
            'input_schema': WorkflowSerializer.serialize_schema(workflow.input_schema),
            'output_schema': WorkflowSerializer.serialize_schema(workflow.output_schema)
        }

    @staticmethod
    def deserialize_workflow(data: Dict[str, Any]) -> Workflow:
        """Create a Workflow instance from serialized data."""
        input_schema = InputSchema(
            WorkflowSerializer.deserialize_schema(data['input_schema'])
        )
        output_schema = OutputSchema(
            WorkflowSerializer.deserialize_schema(data['output_schema'])
        )
        
        workflow = Workflow(
            name=data['name'],
            description=data['description'],
            input_schema=input_schema,
            output_schema=output_schema
        )
        
        seen_task_names = set()
        for task_data in data['tasks']:
            task = TaskSerializer.deserialize_task(task_data)
            if task.name in seen_task_names:
                raise ValueError(f"Duplicate task name found during deserialization: {task.name}")
            seen_task_names.add(task.name)
            workflow.tasks[task.name] = task
        
        return workflow

    @staticmethod
    def save_workflow(workflow: Workflow, filepath: str) -> None:
        """Save workflow to a JSON file."""
        serialized = WorkflowSerializer.serialize_workflow(workflow)
        with open(filepath, 'w') as f:
            json.dump(serialized, f, indent=2)

    @staticmethod
    def load_workflow(filepath: str) -> Workflow:
        """Load workflow from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return WorkflowSerializer.deserialize_workflow(data)

    @staticmethod
    def _get_type_name(type_obj: type) -> str:
        """Convert a type object to its string representation."""
        return type_obj.__name__

    @staticmethod
    def _get_type_from_name(type_name: str) -> type:
        """Convert a type name string back to its type object."""
        type_mapping = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'dict': dict,
            'list': list,
        }
        if type_name not in type_mapping:
            raise ValueError(f"Unsupported type: {type_name}")
        return type_mapping[type_name]