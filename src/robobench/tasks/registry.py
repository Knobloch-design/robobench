"""Name -> task factory registry, so suites and the CLI can refer to tasks by name,
and filter them by robot or tag without building them."""

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from robobench.tasks.task import Task

TaskFactory = Callable[..., "Task"]


@dataclass(frozen=True)
class TaskEntry:
    name: str
    robot: str
    """Robot name (RobotDefinition.name), for filtering, e.g. "leap_hand"."""
    tags: tuple[str, ...]
    factory: TaskFactory


_REGISTRY: dict[str, TaskEntry] = {}


def register_task(name: str, robot: str, tags: tuple[str, ...] = ()) -> Callable[[TaskFactory], TaskFactory]:
    """Decorator for a function (or Task subclass) that builds the task.

        @register_task("leap/cube_reorientation", robot="leap_hand", tags=("manipulation",))
        def make(angle_tolerance: float = 0.2) -> Task: ...

    Keyword arguments become options that suites can override.
    """

    def decorator(factory: TaskFactory) -> TaskFactory:
        if name in _REGISTRY:
            raise ValueError(f"Task {name!r} is already registered")
        _REGISTRY[name] = TaskEntry(name=name, robot=robot, tags=tags, factory=factory)
        return factory

    return decorator


def _load_builtin_library() -> None:
    importlib.import_module("robobench.tasks.library")


def get_task(name: str, **overrides: Any) -> "Task":
    """Build a registered task. Loads the built-in library on first use."""
    _load_builtin_library()
    try:
        entry = _REGISTRY[name]
    except KeyError:
        raise KeyError(f"Unknown task {name!r}. Known: {sorted(_REGISTRY)}") from None
    return entry.factory(**overrides)


def list_tasks(robot: str | None = None, tags: tuple[str, ...] = ()) -> list[TaskEntry]:
    """Registered tasks, optionally only those for `robot` and with all of `tags`."""
    _load_builtin_library()
    return [
        entry
        for name, entry in sorted(_REGISTRY.items())
        if (robot is None or entry.robot == robot) and set(tags) <= set(entry.tags)
    ]


def source_file_for(name: str) -> Path | None:
    """The file that registered task `name`, or None if it isn't registered."""
    entry = _REGISTRY.get(name)
    return Path(inspect.getfile(entry.factory)) if entry else None
