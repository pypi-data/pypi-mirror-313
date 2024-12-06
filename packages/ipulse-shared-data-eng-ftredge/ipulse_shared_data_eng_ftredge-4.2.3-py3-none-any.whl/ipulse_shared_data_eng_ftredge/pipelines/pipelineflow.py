""" Shared pipeline configuration utility. """
import uuid
from typing import List, Optional, Dict, Union, Callable
from enum import Enum
from contextlib import contextmanager
from functools import wraps

from ipulse_shared_base_ftredge import (DataActionType, DataSourceType, DatasetScope)



class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class PipelineTask:
    """
    Represents a single task in a pipeline.
    """
    def __init__(
        self,
        n: str,
        a: Optional[DataActionType] = None,
        s: Optional[DataSourceType] = None,
        d: Optional[DataSourceType] = None,
        scope: Optional[DatasetScope] = None,
        dependencies: Optional[List[str]] = None,
        enabled: bool = True,
        config: Optional[Dict] = None
    ):
        """
        Initialize a PipelineTask.
        :param n: Name of the task.
        :param s: Source of data for the task.
        :param a: Action to perform.
        :param d: Destination for the task output.
        :param scope: Scope of the dataset being processed.
        :param dependencies: List of task names that this task depends on.
        :param config: Task-specific configuration.
        :param enabled: Whether the task is enabled.
        """
        self.id=uuid.uuid4()
        self.name = n
        self.action = a
        self.source = s
        self.destination = d
        self.data_scope = scope
        self.dependencies = dependencies or []
        self.config = config or {}
        self.enabled = enabled
        self.status = TaskStatus.PENDING
        self.completed = False  # Tracks whether the step is completed
        self.pipeline_flow = None  # Reference to the parent PipelineFlow

    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """
        Associate the task with a pipeline flow.
        :param pipeline_flow: The parent PipelineFlow.
        """
        self.pipeline_flow = pipeline_flow

    def validate(self) -> bool:
        """
        Ensure the task is enabled and all dependencies are completed.
        :param pipeline_flow: The PipelineFlow instance managing tasks.
        :return: True if the task is ready to execute; otherwise, raise an exception.
        """
        if not self.enabled:
            return False
        for dependency in self.dependencies:
            dep_task = self.pipeline_flow.get_step(dependency)
            if not dep_task.completed:
                raise ValueError(f"Dependency '{dependency}' for task '{self.name}' is not completed.")
        return True

    def complete(self):
        """
        Mark the task as completed.
        """
        self.completed = True


    def __str__(self):
        parts = [self.name]
        if self.action:
            parts.append(self.action.value)
        if self.source:
            parts.append(f"from {self.source.value}")
        if self.destination:
            parts.append(f"to {self.destination.value}")
        if self.data_scope:
            parts.append(f"scope={self.data_scope.value}")
        return " :: ".join(parts)

class PipelineLoopGroup:
    """
    Represents a group of tasks that execute iteratively, with unique name enforcement.
    """

    def __init__(self, 
                name: str,
                tasks: List[Union['PipelineTask', 'PipelineLoopGroup']],
                enabled: bool = True,
                dependencies: Optional[List[str]] = None,
                iteration_start: int = 0,
                iteration_end: Optional[int] = None):
        """
        Initialize the PipelineLoopGroup.
        :param name: Name of the loop group.
        :param tasks: List of PipelineTask or nested PipelineLoopGroup.
        """
        self.name = name
        self.enabled=enabled
        self.tasks: Dict[str, Union['PipelineTask', 'PipelineLoopGroup']] = {}
        self.dependencies = dependencies or []
        self.completed = False  # Tracks whether the group is completed
        self.pipeline_flow = None  # Reference to the parent PipelineFlow
        self.current_iteration = iteration_start
        self.iteration_end = iteration_end
        self.iterations_started = iteration_start
        self.iterations_completed = iteration_start
        self.iteration_end = iteration_end
        for task in tasks:
            if task.name in self.tasks:
                raise ValueError(f"Task or group with name '{task.name}' already exists in group '{self.name}'.")
            self.tasks[task.name] = task

    @property
    def progress_percentage(self) -> float:
        """
        Compute the progress percentage for iterations.
        :return: Progress as a float percentage.
        """
        if self.iteration_end is None or self.iteration_end == 0:
            return 0.0
        return (self.iterations_completed / self.iteration_end) * 100

    
    def set_pipeline_flow(self, pipeline_flow: 'PipelineFlow'):
        """
        Associate the loop group with a pipeline flow and propagate to all tasks.
        :param pipeline_flow: The parent PipelineFlow.
        """
        self.pipeline_flow = pipeline_flow
        for task in self.tasks.values():
            if isinstance(task, PipelineTask):
                task.set_pipeline_flow(pipeline_flow)
            elif isinstance(task, PipelineLoopGroup):
                task.set_pipeline_flow(pipeline_flow)

    def get_task(self, name: str):
        """
        Retrieve a task or nested group by name.
        :param name: Name of the task or group to retrieve.
        :return: Task or group with the given name.
        :raises KeyError: If no task or group exists with the given name.
        """
        if name not in self.tasks:
            raise KeyError(f"Task or group with name '{name}' not found in {self.name}.")
        return self.tasks[name]
    

    def validate(self) -> bool:
        """
        Ensure the task is enabled and all dependencies are completed.
        :param pipeline_flow: The PipelineFlow instance managing tasks.
        :return: True if the task is ready to execute; otherwise, raise an exception.
        """
        if not self.enabled:
            return False
        for dependency in self.dependencies:
            dep_task = self.pipeline_flow.get_step(dependency)
            if not dep_task.completed:
                raise ValueError(f"Dependency '{dependency}' for task '{self.name}' is not completed.")
        return True
    
    def set_iterations(self, iteration_end: int):
        """
        Dynamically set the number of iterations for the loop group.
        :param iteration_end: The total number of expected iterations.
        """
        self.iteration_end = iteration_end

    def start_iteration(self):
        """
        Start a new iteration. Increment the iterations started count.
        """
        if self.iteration_end is not None and self.iterations_started >= self.iteration_end:
            raise ValueError("Cannot start a new iteration. Iteration count already reached its limit.")
        self.iterations_started += 1

    def complete_iteration(self):
        """
        Complete the current iteration. Increment the iterations completed count.
        Mark the loop group as completed if all iterations are finished.
        """
        if self.iterations_completed < self.iterations_started:
            self.iterations_completed += 1

        if self.iteration_end is not None and self.iterations_completed >= self.iteration_end:
            self.completed = True

    def complete(self):
        """
        Mark the loop group as completed if all enabled tasks within the group and iterations are completed.
        """
        if self.iteration_end is not None and self.current_iteration >= self.iteration_end:
            self.completed = True
        else:
            # Check if all tasks are completed
            if all(
                (task.completed if isinstance(task, PipelineTask) else task.completed)
                for task in self.tasks.values()
                if (task.enabled if isinstance(task, PipelineTask) else True)
            ):
                self.completed = True

    def __str__(self):
        completed_tasks = sum(
            1
            for task in self.tasks.values()
            if (task.completed if isinstance(task, PipelineTask) else task.completed)
        )
        total_tasks = len(self.tasks)
        iteration_progress = (
            f"Iterations Started: {self.iterations_started}, Completed: {self.iterations_completed}/{self.iteration_end}"
            if self.iteration_end
            else f"Current Iterations Started: {self.iterations_started}, Completed: {self.iterations_completed} (Total unknown)"
        )
        progress_percent = f"Progress: {self.progress_percentage:.2f}%" if self.iteration_end else ""
        header = (
            f"[{self.name} :: {iteration_progress} :: {progress_percent} :: Completed Tasks: {completed_tasks}/{total_tasks} :: Status={'✔' if self.completed else '✖'}]"
        )
        inner_flow = "\n".join(str(task) for task in self.tasks.values())
        return f"{header}\n{inner_flow}"


class PipelineFlow:
    """
    Enhanced Pipeline configuration utility with unique name enforcement.
    """

    def __init__(self, base_context_name:str):
        self.steps: Dict[str, Union['PipelineTask', 'PipelineLoopGroup']] = {}
        self.base_context=base_context_name

    def add_step(self, step: Union['PipelineTask', 'PipelineLoopGroup']):
        """
        Add a step which is a PipelineTask or PipelineLoopGroup to the pipeline.
        :param task_or_group: Single PipelineTask or PipelineLoopGroup.
        """
        if step.name in self.steps:
            raise ValueError(f"Step (Task, Group etc) with name '{step.name}' already exists in the pipeline.")
        self.steps[step.name] = step
        step.set_pipeline_flow(self)  # Associate the step with this pipeline flow

    def get_step(self, name: str) -> Union['PipelineTask', 'PipelineLoopGroup']:
        """
        Retrieve a task or group by name, searching recursively through all groups.
        :param name: Name of the task or group to retrieve.
        :return: Task or group with the given name.
        :raises KeyError: If no task or group exists with the given name.
        """
        # First, check top-level steps
        if name in self.steps:
            return self.steps[name]

        # Then, recursively check inside groups
        for step in self.steps.values():
            if isinstance(step, PipelineLoopGroup):
                try:
                    return step.get_task(name)  # Recursively search in the group
                except KeyError:
                    continue

        raise KeyError(f"Task or group with name '{name}' not found in pipeline.")
    
        # Add context management for tasks
    @contextmanager
    def task_context(self, task: PipelineTask):
        """
        Context manager for tasks to handle status changes.
        """
        task.status = TaskStatus.RUNNING
        try:
            yield
            task.status = TaskStatus.COMPLETED 
        except Exception:
            task.status = TaskStatus.FAILED
            raise
    
    def get_dependent_tasks(self, task: PipelineTask) -> List[PipelineTask]:
        return [self.get_step(dep) for dep in task.dependencies]
    
    def validate_dependencies(self, task: PipelineTask) -> bool:
        return all(dep.completed for dep in self.get_dependent_tasks(task))
    
    def get_progress(self) -> dict:
        return {
            "total_tasks": len(self.steps),
            "completed": sum(1 for t in self.steps.values() if t.completed),
            "failed": sum(1 for t in self.steps.values() 
                        if not t.completed and t.enabled)
        }
    
    def get_pipeline_flow(self) -> str:
        """
        Generate a string representation of the pipeline flow, including only enabled tasks.
        :return: String representing the pipeline flow.
        """

        def _generate_flow(task_or_group, indent=0):
            if isinstance(task_or_group, PipelineTask):
                if not task_or_group.enabled:
                    return ""  # Skip disabled tasks
                status = "✔" if task_or_group.completed else "✖"
                return f"{' ' * indent}>> {str(task_or_group)} [status={status}]"
            elif isinstance(task_or_group, PipelineLoopGroup):
                if not task_or_group.enabled:
                    return ""  # Skip disabled groups
                iteration_status = (
                    f"Iterations Started: {task_or_group.iterations_started}, Completed: {task_or_group.iterations_completed}/{task_or_group.iteration_end}"
                    if task_or_group.iteration_end
                    else f"Current Iterations: {task_or_group.iterations_started}, Completed: {task_or_group.iterations_completed} (Total unknown)"
                )
                header = f"{' ' * indent}** {task_or_group.name} :: {iteration_status} :: Status={'✔' if task_or_group.completed else '✖'} **"
                inner_flow = "\n".join(
                    _generate_flow(t, indent + 2) for t in task_or_group.tasks.values() if t.enabled
                )
                return f"{header}\n{inner_flow}" if inner_flow.strip() else ""

        return "\n".join(
            _generate_flow(step) for step in self.steps.values() if step.enabled
        ).strip() + "\n"

    def get_pipeline_description(self) -> str:
        """
        Generate the complete pipeline description with base context and pipeline flow.
        :return: String representing the pipeline description.
        """
        return f"{self.base_context}\nflow:\n{self.get_pipeline_flow()}"