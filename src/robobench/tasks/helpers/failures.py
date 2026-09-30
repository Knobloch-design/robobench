"""Failure conditions that end an episode early (a fallen robot, a dropped object).

Success comes from `Task.is_success` and timeouts from `Task.max_duration`; the episode
loop handles both, and controller-side failures (crash, hang, invalid command) too.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from robobench.sim.state import SimState
    from robobench.tasks.task import EpisodeSetup


class FailureCondition(ABC):
    @abstractmethod
    def check(self, state: "SimState", setup: "EpisodeSetup") -> str | None:
        """Return a short reason ("fell", "dropped") to end the episode now, or None."""


class BodyBelowHeight(FailureCondition):
    """A body drops below a height: a fallen humanoid or a dropped object."""

    def __init__(self, body_name: str, min_height: float, reason: str = "fell") -> None:
        raise NotImplementedError

    def check(self, state, setup) -> str | None:
        raise NotImplementedError


class LeftRegion(FailureCondition):
    """A body leaves a scene region (object knocked off the table, robot out of bounds)."""

    def __init__(self, body_name: str, region: str, reason: str = "out_of_bounds") -> None:
        raise NotImplementedError

    def check(self, state, setup) -> str | None:
        raise NotImplementedError


class CustomFailure(FailureCondition):
    """Wrap a function for one-off conditions."""

    def __init__(self, fn: Callable[["SimState", "EpisodeSetup"], str | None]) -> None:
        raise NotImplementedError

    def check(self, state, setup) -> str | None:
        raise NotImplementedError
