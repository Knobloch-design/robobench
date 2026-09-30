"""Tasks: what the benchmark asks robots to do.

A task subclasses `Task` and defines the scene, a reset map (seed -> initial context),
a success condition, and a natural-language description, and ships a success and a
failure demonstration. `ComposedTask` builds one from the reusable pieces in `helpers`.
"""

from robobench.tasks.composed import ComposedTask
from robobench.tasks.registry import TaskEntry, get_task, list_tasks, register_task
from robobench.tasks.task import EpisodeSetup, Task

__all__ = ["ComposedTask", "EpisodeSetup", "Task", "TaskEntry", "get_task", "list_tasks", "register_task"]
