"""Checks every task must pass before it joins the suite (`robobench validate-task NAME`).

Contributors run this locally; the same checks gate merging new tasks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydrake.geometry import Meshcat

    from robobench.tasks.task import Task


@dataclass(frozen=True)
class TaskCheck:
    name: str
    passed: bool
    detail: str = ""
    blocking: bool = True
    """False for warnings that don't fail validation."""


@dataclass(frozen=True)
class TaskValidationReport:
    task: str
    checks: list[TaskCheck]

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks if c.blocking)

    def summary(self) -> str:
        raise NotImplementedError


def validate_task(task: "Task", seeds: tuple[int, ...] = (0, 1, 2), meshcat: "Meshcat | None" = None) -> TaskValidationReport:
    """Run every check below and collect the results."""
    raise NotImplementedError


def check_definition(task: "Task") -> TaskCheck:
    """`name` and `robot` are set, the description is non-empty, the command interface exists on the robot."""
    raise NotImplementedError


def check_scene_builds(task: "Task") -> TaskCheck:
    """The diagram builds on a continuous-time plant and CENIC can advance it briefly."""
    raise NotImplementedError


def check_reset_deterministic(task: "Task", seeds: tuple[int, ...]) -> TaskCheck:
    """Resetting twice with the same seed gives the same context state and the same EpisodeSetup."""
    raise NotImplementedError


def check_reset_varies(task: "Task", seeds: tuple[int, ...]) -> TaskCheck:
    """Different seeds give different initial conditions. Warning only."""
    raise NotImplementedError


def check_not_trivially_solved(task: "Task", seeds: tuple[int, ...]) -> TaskCheck:
    """`is_success` is false right after reset, and stays false if the robot is simply held still."""
    raise NotImplementedError


def check_initial_state_valid(task: "Task", seeds: tuple[int, ...]) -> TaskCheck:
    """No significant penetration between bodies right after reset."""
    raise NotImplementedError


def check_demonstrations(task: "Task") -> list[TaskCheck]:
    """Both demos exist and match the task's command interface; the success demo succeeds on replay;
    the failure demo doesn't; replay stays close to the recorded states (warning only)."""
    raise NotImplementedError


def check_asset_licenses(task: "Task") -> TaskCheck:
    """Every asset the task loads is in the asset manifest with a known license."""
    raise NotImplementedError
