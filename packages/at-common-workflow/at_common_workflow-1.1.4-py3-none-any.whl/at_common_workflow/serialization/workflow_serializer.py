from typing import Dict, Any
import json
import importlib
from ..core.workflow import Workflow
from ..core.task import Task, TaskFunction
from ..core.io import InputSchema, OutputSchema

class WorkflowSerializer:
    """Handles serialization and deserialization of workflows using dynamic imports."""
    
    @staticmethod
    def serialize_task(task: Task) -> Dict[str, Any]:
        """Convert a Task instance to a serializable dictionary."""
        return {
            'name': task.name,
            'description': task.description,
            'parameters': task.parameters,
            'requires': {k: v.__name__ for k, v in task.requires.items()},
            'provides': {k: v.__name__ for k, v in task.provides.items()},
            'status': task.status.value,
            'callable_module': task.func.__module__,
            'callable_name': task.func.__name__
        }

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
        return type_mapping.get(type_str)

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
            'tasks': {
                name: WorkflowSerializer.serialize_task(task)
                for name, task in workflow.tasks.items()
            },
            'input_schema': WorkflowSerializer.serialize_schema(workflow.input_schema),
            'output_schema': WorkflowSerializer.serialize_schema(workflow.output_schema)
        }

    @staticmethod
    def save_workflow(workflow: Workflow, filepath: str) -> None:
        """Save workflow to a JSON file."""
        serialized = WorkflowSerializer.serialize_workflow(workflow)
        with open(filepath, 'w') as f:
            json.dump(serialized, f, indent=2)

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
        func = WorkflowSerializer.load_function(data['callable_module'], data['callable_name'])
        
        # Convert type names back to actual types
        type_mapping = {
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'dict': dict,
            'list': list
            # Add more types as needed
        }
        
        requires = InputSchema({
            k: type_mapping[v] for k, v in data['requires'].items()
        })
        provides = OutputSchema({
            k: type_mapping[v] for k, v in data['provides'].items()
        })
        
        task = Task(
            name=data['name'],
            description=data['description'],
            func=func,
            parameters=data['parameters'],
            requires=requires,
            provides=provides
        )
        return task

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
            input_schema=input_schema,
            output_schema=output_schema
        )
        
        for task_name, task_data in data['tasks'].items():
            task = WorkflowSerializer.deserialize_task(task_data)
            workflow.tasks[task_name] = task
        
        return workflow

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
            # Add more types as needed
        }
        if type_name not in type_mapping:
            raise ValueError(f"Unsupported type: {type_name}")
        return type_mapping[type_name]