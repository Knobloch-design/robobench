"""Disturbances: things done to the robot or world during an episode (pushes, scheduled events).

Sensor-side problems (noise, dropout, delay) belong in the observation pipeline instead.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Mapping

import numpy as np

if TYPE_CHECKING:
    from robobench.sim.environment import SimulationEnvironment


class Disturbance(ABC):
    def sample(self, rng: np.random.Generator) -> Mapping[str, Any]:
        """Draw this episode's timing/magnitudes. Recorded in results. Default: nothing."""
        return {}

    @abstractmethod
    def update(self, env: "SimulationEnvironment", samples: Mapping[str, Any]) -> None:
        """Called every control step. Applies the disturbance when its time comes."""


class ExternalPush(Disturbance):
    """Push a body with a random force at a random time."""

    def __init__(
        self,
        body_name: str,
        force_range: tuple[float, float],
        time_range: tuple[float, float],
        duration: float = 0.1,
    ) -> None:
        """Force magnitude in N, horizontal with random direction; start time in seconds."""
        raise NotImplementedError

    def sample(self, rng):
        raise NotImplementedError

    def update(self, env, samples) -> None:
        raise NotImplementedError


class ScheduledEvent(Disturbance):
    """Run a function once at a fixed sim time (e.g. drop an extra object on the table)."""

    def __init__(self, time: float, fn: Callable[["SimulationEnvironment"], None]) -> None:
        raise NotImplementedError

    def update(self, env, samples) -> None:
        raise NotImplementedError
