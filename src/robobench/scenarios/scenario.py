"""The test definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Mapping

from robobench.config import SimParams
from robobench.metrics.standard import default_metrics
from robobench_sdk.specs import TaskInfo

if TYPE_CHECKING:
    from robobench.metrics.base import Metric
    from robobench.robots.base import RobotDefinition
    from robobench.scenarios.disturbances import Disturbance
    from robobench.scenarios.goals import Goal
    from robobench.scenarios.randomizers import Randomizer
    from robobench.scenarios.termination import TerminationCondition
    from robobench.scenes.base import Scene
    from robobench.sensors.definitions import SensorDefinition
    from robobench.sensors.pipeline import ObservationPipeline


@dataclass
class Scenario:
    name: str
    """Registry name, e.g. "g1/walk_rocky_terrain"."""
    robot: "RobotDefinition"
    scene: "Scene"
    goal: "Goal"
    randomizers: list["Randomizer"] = field(default_factory=list)
    """Applied in order. Each sees the samples of the ones before it."""
    terminations: list["TerminationCondition"] = field(default_factory=list)
    """A timeout at `max_duration` is always added."""
    metrics: list["Metric"] = field(default_factory=default_metrics)
    disturbances: list["Disturbance"] = field(default_factory=list)
    sim_params: SimParams = field(default_factory=SimParams)
    sensors: list["SensorDefinition"] | None = None
    """None uses the robot's default sensors."""
    observation_pipeline: "ObservationPipeline | None" = None
    """None passes raw sensor output through."""
    command_interface: str | None = None
    """None uses the robot's default command interface."""
    max_duration: float = 30.0
    description: str = ""
    tags: tuple[str, ...] = ()
    """For filtering suites, e.g. ("locomotion", "g1")."""

    def sample(self, seed: int) -> "ScenarioInstance":
        """Run the randomizers with an RNG seeded from `seed`. Pure: same seed, same instance."""
        raise NotImplementedError


@dataclass(frozen=True)
class ScenarioInstance:
    """One concrete, reproducible episode setup."""

    scenario: Scenario
    seed: int
    samples: Mapping[str, Any]
    """Everything the randomizers drew (start pose, goal pose, target face, friction...).
    Recorded in results so any episode can be replayed."""

    def task_info(self, episode_id: str) -> TaskInfo:
        """What the controller is told at reset: the goal's description plus episode info."""
        raise NotImplementedError
