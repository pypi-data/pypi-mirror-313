from typing import List
import os
import inspect
from pathlib import Path
from ..utils.logging import setup_logger
import importlib.util
from .task import Task

logger = setup_logger(__name__)

class TaskScanner:
    """Scanner for tasks decorated with @task in a directory."""
    
    @staticmethod
    def scan(directory: str) -> List[Task]:
        """
        Scan a directory for all functions decorated with @task and create Task objects.
        
        Args:
            directory: The directory path to scan
            
        Returns:
            List of Task objects
        
        Raises:
            FileNotFoundError: If the directory does not exist
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")
        
        tasks = []
        # Walk through all Python files in the directory
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        # Get the module name relative to the scan directory
                        rel_path = file_path.relative_to(directory_path.parent)
                        module_path = str(rel_path).replace(os.sep, '.')[:-3]
                        # Import the module dynamically
                        spec = importlib.util.spec_from_file_location(module_path, str(file_path))
                        if spec is None or spec.loader is None:
                            continue
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        # Inspect all module members
                        for name, obj in inspect.getmembers(module):
                            if inspect.isfunction(obj) and hasattr(obj, '_is_workflow_task'):
                                task = Task(
                                    name=obj._name,
                                    func=obj,
                                    description=obj._description,
                                    parameters=obj._parameters,
                                    requires=obj._requires,
                                    provides=obj._provides
                                )
                                tasks.append(task)
                                logger.debug(f"Found task: {name} in {file_path}")
                                
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {str(e)}")
                        
        return tasks