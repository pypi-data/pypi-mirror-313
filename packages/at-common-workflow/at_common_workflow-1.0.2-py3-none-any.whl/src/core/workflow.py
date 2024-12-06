from typing import Dict, List, Set, Callable
import asyncio
from .io import InputSchema, OutputSchema, Input, Output
from .task import Task, TaskStatus, TaskProgress, TaskParameters, TaskFunction
from .context import Context
from ..utils.validation import validate_dag, validate_schema
from ..utils.logging import setup_logger
import inspect

logger = setup_logger(__name__)

class Workflow:
    """Manages the execution of tasks in a directed acyclic graph (DAG).
    
    Attributes:
        name: Unique identifier for the workflow
        tasks: Dictionary of tasks keyed by task name
        input_schema: Schema defining required workflow inputs
        output_schema: Schema defining expected workflow outputs
    """
    def __init__(self, name: str, input_schema: InputSchema, output_schema: OutputSchema):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.input_schema = input_schema
        self.output_schema = output_schema
        logger.info(f"Created workflow: {name}")
    
    def task(
        self,
        *,  # Force keyword arguments
        name: str | None = None,
        description: str | None = None,
        requires: InputSchema | None = None,
        provides: OutputSchema | None = None,
        parameters: TaskParameters | None = None,
    ) -> callable:
        """Decorator to register a task in the workflow."""
        def decorator(func: TaskFunction) -> callable:
            task_name = name or func.__name__
            
            if task_name in self.tasks:
                raise ValueError(f"Task '{task_name}' already exists")
                
            task = Task(
                name=task_name,
                func=func,
                description=description or func.__doc__ or "",
                requires=requires or InputSchema({}),
                provides=provides or OutputSchema({}),
                parameters=parameters or {}
            )
            
            # Check for duplicate outputs
            for existing_task in self.tasks.values():
                duplicate_outputs = set(task.provides) & set(existing_task.provides)
                if duplicate_outputs:
                    raise ValueError(
                        f"Tasks '{task.name}' and '{existing_task.name}' "
                        f"provide the same outputs: {duplicate_outputs}"
                    )
            
            # Add metadata to the function for scanner detection
            func._is_workflow_task = True
            func._name = task_name
            func._description = task.description
            func._requires = task.requires
            func._provides = task.provides
            func._parameters = task.parameters
            
            self.tasks[task_name] = task
            logger.debug(f"Registered task: {task_name}")
            return func
            
        return decorator
    
    def _get_ready_tasks(self, context: Context, completed: Set[str]) -> List[Task]:
        """Get tasks whose dependencies are satisfied."""
        ready = []
        for task in self.tasks.values():
            # Check if task is pending
            if task.status != TaskStatus.PENDING:
                continue
                
            # Get all provided data keys from completed tasks AND existing context data
            available_data = set(context.keys())
            for completed_task in self.tasks.values():
                if completed_task.name in completed:
                    available_data.update(completed_task.provides.keys())
                    
            # Check if all required data is available
            if set(task.requires.keys()).issubset(available_data):
                ready.append(task)
                
        return ready
    
    async def execute(self, input: Input, callback: Callable[[TaskProgress], None] | None = None) -> Output:
        """Execute the workflow and report progress through callback if provided."""
        logger.info(f"Starting workflow execution: {self.name}")

        validate_schema(input, self.input_schema, "input")
        context = Context()
        context.update(input)

        validate_dag(self.tasks, context)
        completed_tasks: Set[str] = set()
        
        while len(completed_tasks) < len(self.tasks):
            ready_tasks = self._get_ready_tasks(context, completed_tasks)
            if not ready_tasks:
                remaining = [t.name for t in self.tasks.values() 
                           if t.status != TaskStatus.COMPLETED]
                logger.error(f"No tasks ready to execute. Remaining: {remaining}")
                raise RuntimeError(f"No tasks ready to execute. Remaining: {remaining}")
            
            # Report starting tasks
            for task in ready_tasks:
                if callback:
                    callback(TaskProgress(task.name, TaskStatus.RUNNING))
            
            try:
                tasks = [task.execute(context) for task in ready_tasks]
                await asyncio.gather(*tasks)
                
                # Report completed tasks
                for task in ready_tasks:
                    task.status = TaskStatus.COMPLETED
                    completed_tasks.add(task.name)
                    if callback:
                        callback(TaskProgress(task.name, TaskStatus.COMPLETED))
                
            except Exception as e:
                # Report failed tasks
                for task in ready_tasks:
                    if task.status != TaskStatus.COMPLETED:
                        task.status = TaskStatus.FAILED
                        if callback:
                            callback(TaskProgress(task.name, TaskStatus.FAILED))
                raise
        
        output = Output()
        for key, value in context.items():
            if key in self.output_schema:
                output[key] = value

        validate_schema(output, self.output_schema, "output")
        logger.info(f"Completed workflow execution: {self.name}")
        return output