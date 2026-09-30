"""Randomizers: draw per-episode values from the seed, then write them into the context.

Used by `ComposedTask.reset`, which runs every randomizer's `sample` in order with one
shared rng, then every `apply`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping, Sequence

import numpy as np

if TYPE_CHECKING:
    from robobench.sim.state import SimState
    from robobench.tasks.task import Task


class Randomizer(ABC):
    goal_keys: tuple[str, ...] = ()
    """Sample keys that go into EpisodeSetup.goal (told to the controller). Everything else goes into info."""

    @abstractmethod
    def sample(self, rng: np.random.Generator, task: "Task", previous: Mapping[str, Any]) -> Mapping[str, Any]:
        """Draw values. `previous` holds earlier randomizers' samples. Values must be plain data."""

    def apply(self, samples: Mapping[str, Any], state: "SimState") -> None:
        """Write the values into the context. Default: nothing (e.g. goal samples)."""


class RegionPoseRandomizer(Randomizer):
    """Place a body (or a floating robot base) at a random pose in one of the scene's regions."""

    def __init__(
        self,
        key: str,
        region: str,
        body_name: str | None = None,
        min_distance_from: str | None = None,
        min_distance: float = 0.0,
        is_goal: bool = False,
    ) -> None:
        """
        Args:
            key: Sample name, e.g. "start_pose".
            region: Scene region to sample from.
            body_name: Body to move in `apply`. None only records the pose (e.g. a goal pose).
            min_distance_from / min_distance: Resample until this far from an earlier sample.
            is_goal: Send this sample to the controller as part of the goal.
        """
        raise NotImplementedError

    def sample(self, rng, task, previous):
        raise NotImplementedError

    def apply(self, samples, state) -> None:
        raise NotImplementedError


class JointPositionRandomizer(Randomizer):
    """Perturb the robot's nominal joint positions by uniform noise."""

    def __init__(self, amplitude: float, key: str = "initial_joint_positions") -> None:
        raise NotImplementedError

    def sample(self, rng, task, previous):
        raise NotImplementedError

    def apply(self, samples, state) -> None:
        raise NotImplementedError


class ChoiceRandomizer(Randomizer):
    """Pick one of a set of discrete options, e.g. which cube face should end up on top."""

    def __init__(self, key: str, options: Sequence[Any], is_goal: bool = False) -> None:
        raise NotImplementedError

    def sample(self, rng, task, previous):
        raise NotImplementedError


class PhysicalParameterRandomizer(Randomizer):
    """Scale friction and/or mass of bodies within ranges."""

    def __init__(
        self,
        body_names: Sequence[str],
        friction_range: tuple[float, float] | None = None,
        mass_scale_range: tuple[float, float] | None = None,
        key: str = "physical_params",
    ) -> None:
        raise NotImplementedError

    def sample(self, rng, task, previous):
        raise NotImplementedError

    def apply(self, samples, state) -> None:
        raise NotImplementedError
