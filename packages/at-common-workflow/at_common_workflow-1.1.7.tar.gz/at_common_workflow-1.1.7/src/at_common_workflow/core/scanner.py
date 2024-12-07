from typing import List, Dict, Any
import os
import inspect
from pathlib import Path
from ..utils.logging import setup_logger
import importlib.util
from .task import Task
from .serializer import WorkflowSerializer

logger = setup_logger(__name__)

class TaskScanner:
    """Scanner for tasks decorated with @task in a directory."""
    
    @staticmethod
    def scan(directory: str) -> List[Dict[str, Any]]:
        """
        Scan a directory for all functions decorated with @task and serialize them.
        
        Args:
            directory: The directory path to scan
            
        Returns:
            List of serialized task definitions
        """
        tasks = []
        directory_path = Path(directory)
        
        # Walk through all Python files in the directory
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    try:
                        # Get the module name relative to the scan directory
                        rel_path = file_path.relative_to(directory_path.parent)
                        module_path = str(rel_path).replace(os.sep, '.')[:-3]  # Remove .py
                        
                        # Import the module dynamically
                        spec = importlib.util.spec_from_file_location(module_path, str(file_path))
                        if spec is None or spec.loader is None:
                            continue
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Inspect all module members
                        for name, obj in inspect.getmembers(module):
                            if inspect.isfunction(obj) and hasattr(obj, '_is_workflow_task'):
                                task_info = TaskScanner._serialize_task(obj)
                                tasks.append(task_info)
                                logger.debug(f"Found task: {name} in {file_path}")
                                
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {str(e)}")
                        
        return tasks

    @staticmethod
    def _serialize_task(func) -> Dict[str, Any]:
        """
        Serialize a single task function into the required format.
        """
        # Validate task decoration and create Task instance using TaskSerializer's approach
        if not hasattr(func, '_is_workflow_task'):
            raise ValueError(f"Function {func.__name__} is not properly decorated with @task")
            
        task = Task(
            name=getattr(func, '_name', func.__name__),
            description=getattr(func, '_description', None) or func.__doc__ or "",
            func=func,
            parameters=getattr(func, '_parameters', {}),
            requires=getattr(func, '_requires', {}),
            provides=getattr(func, '_provides', {})
        )

        # Add additional scanning-specific information
        sig = inspect.signature(func)
        param_list = []
        for name, param in sig.parameters.items():
            if name == 'context':  # Skip context parameter
                continue
                
            param_info = {
                "name": name,
                "type": WorkflowSerializer.serialize_type(param.annotation),
            }
            
            if name in task.parameters:
                param_info["value"] = task.parameters[name]
                
            param_list.append(param_info)

        # Combine the basic task info with scanning-specific details
        return {
            "name": task.name,
            "description": task.description,
            "parameters": param_list,
            "requires": [
                {"name": key, "type": WorkflowSerializer.serialize_type(type_)}
                for key, type_ in task.requires.items()
            ],
            "provides": [
                {"name": key, "type": WorkflowSerializer.serialize_type(type_)}
                for key, type_ in task.provides.items()
            ]
        }