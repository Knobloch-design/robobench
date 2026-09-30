"""Randomizers: draw per-episode values from a seed, then apply them to the simulation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Mapping, Sequence

import numpy as np

if TYPE_CHECKING:
    from pydrake.multibody.plant import MultibodyPlant
    from pydrake.systems.framework import Context

    from robobench.scenarios.scenario import Scenario


class Randomizer(ABC):
    """Two phases, so sampling is reproducible and recorded separately from simulation:

    `sample` is pure (only the rng and earlier samples), and its output is stored in the results.
    `apply` writes those values into the simulation at episode reset.
    """

    @abstractmethod
    def sample(
        self, rng: np.random.Generator, scenario: "Scenario", previous: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        """Draw values. `previous` holds samples from earlier randomizers (e.g. keep the goal far from the start).

        Values must be plain data (numbers, lists, strings) so they can be saved as JSON.
        """

    def apply(self, samples: Mapping[str, Any], plant: "MultibodyPlant", plant_context: "Context") -> None:
        """Write the values into the simulation. Default: nothing (e.g. goal samples only affect the goal)."""


class RegionPoseRandomizer(Randomizer):
    """Place a body (or a floating robot base) at a random pose in one of the scene's regions."""

    def __init__(self, key: str, region: str, body_name: str | None = None, min_distance_from: str | None = None, min_distance: float = 0.0) -> None:
        """
        Args:
            key: Sample name, e.g. "start_pose".
            region: Scene region to sample from.
            body_name: Body to move in `apply`. None only records the pose (e.g. a goal pose).
            min_distance_from / min_distance: Resample until this far from an earlier sample.
        """
        raise NotImplementedError

    def sample(self, rng, scenario, previous):
        raise NotImplementedError

    def apply(self, samples, plant, plant_context) -> None:
        raise NotImplementedError


class JointPositionRandomizer(Randomizer):
    """Perturb the robot's nominal joint positions by uniform noise."""

    def __init__(self, amplitude: float, key: str = "initial_joint_positions") -> None:
        raise NotImplementedError

    def sample(self, rng, scenario, previous):
        raise NotImplementedError

    def apply(self, samples, plant, plant_context) -> None:
        raise NotImplementedError


class ChoiceRandomizer(Randomizer):
    """Pick one of a set of discrete options, e.g. which cube face should end up on top."""

    def __init__(self, key: str, options: Sequence[Any]) -> None:
        raise NotImplementedError

    def sample(self, rng, scenario, previous):
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

    def sample(self, rng, scenario, previous):
        raise NotImplementedError

    def apply(self, samples, plant, plant_context) -> None:
        raise NotImplementedError
