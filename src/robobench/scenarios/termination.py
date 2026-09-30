"""Conditions that end an episode (success or failure) based on simulation state.

Controller-side failures (crash, hang, invalid command) are handled by the episode loop, not here.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from robobench.scenarios.goals import Goal
    from robobench.scenarios.scenario import ScenarioInstance
    from robobench.sim.state import SimState


@dataclass(frozen=True)
class TerminationResult:
    success: bool
    reason: str
    """Short identifier recorded in results, e.g. "goal_reached", "fell", "timeout"."""


class TerminationCondition(ABC):
    def reset(self, instance: "ScenarioInstance") -> None:
        """Clear any internal timers at episode start."""

    @abstractmethod
    def check(self, state: "SimState", instance: "ScenarioInstance") -> TerminationResult | None:
        """Return a result to end the episode now, or None to keep going."""


class Timeout(TerminationCondition):
    """Failure when sim time reaches `max_duration`. Added to every scenario automatically."""

    def __init__(self, max_duration: float) -> None:
        raise NotImplementedError

    def check(self, state, instance):
        raise NotImplementedError


class GoalAchieved(TerminationCondition):
    """Success once the goal has held for `hold_time` seconds (e.g. cube stays face-up)."""

    def __init__(self, goal: "Goal", hold_time: float = 0.0) -> None:
        raise NotImplementedError

    def check(self, state, instance):
        raise NotImplementedError


class BodyBelowHeight(TerminationCondition):
    """Failure when a body drops below a height: a fallen humanoid or a dropped object."""

    def __init__(self, body_name: str, min_height: float, reason: str = "fell") -> None:
        raise NotImplementedError

    def check(self, state, instance):
        raise NotImplementedError


class LeftRegion(TerminationCondition):
    """Failure when a body leaves a region (object knocked off the table, robot out of bounds)."""

    def __init__(self, body_name: str, region: str, reason: str = "out_of_bounds") -> None:
        raise NotImplementedError

    def check(self, state, instance):
        raise NotImplementedError


class CustomTermination(TerminationCondition):
    """Wrap a function for one-off conditions."""

    def __init__(self, fn: Callable[["SimState", "ScenarioInstance"], TerminationResult | None]) -> None:
        raise NotImplementedError

    def check(self, state, instance):
        raise NotImplementedError
