"""A Task assembled from reusable helpers, for the common cases.

    ComposedTask(
        name="leap/cube_reorientation",
        robot=LeapHand(),
        scene=hand_workspace("cube"),
        goal=ObjectOrientationGoal("cube"),
        randomizers=[RegionPoseRandomizer(...), ChoiceRandomizer("target_face", FACES)],
        failures=[BodyBelowHeight("cube", 0.0, reason="dropped")],
    )

maps onto the Task methods as:
    build_scene  -> scene.add_to_plant
    reset        -> each randomizer samples (in order), then each applies to the context
    is_success   -> goal.is_achieved
    description  -> goal.describe (or `objective`, if given)
    check_failure-> the first failure condition that fires
    goal_error   -> goal.error
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Mapping

from robobench.config import SimParams
from robobench.tasks.task import EpisodeSetup, Task

if TYPE_CHECKING:
    from robobench.metrics.base import Metric
    from robobench.robots.base import RobotDefinition
    from robobench.scenes.base import Scene
    from robobench.sensors.definitions import SensorDefinition
    from robobench.sensors.pipeline import ObservationPipeline
    from robobench.sim.state import SimState
    from robobench.tasks.helpers.disturbances import Disturbance
    from robobench.tasks.helpers.failures import FailureCondition
    from robobench.tasks.helpers.goals import Goal
    from robobench.tasks.helpers.randomizers import Randomizer


@dataclass
class ComposedTask(Task):
    name: str
    robot: "RobotDefinition"
    scene: "Scene"
    goal: "Goal"
    randomizers: list["Randomizer"] = field(default_factory=list)
    failures: list["FailureCondition"] = field(default_factory=list)
    objective: str | None = None
    """Fixed description. None uses `goal.describe`."""
    max_duration: float = 30.0
    success_hold_time: float = 0.0
    tags: tuple[str, ...] = ()
    params: SimParams = field(default_factory=SimParams)
    sensor_overrides: list["SensorDefinition"] | None = None
    pipeline: "ObservationPipeline | None" = None
    interface: str | None = None
    metric_list: list["Metric"] | None = None
    disturbance_list: list["Disturbance"] = field(default_factory=list)

    def build_scene(self, builder, plant, parser) -> Mapping[str, Any] | None:
        raise NotImplementedError

    def reset(self, seed: int, state: "SimState") -> EpisodeSetup:
        raise NotImplementedError

    def is_success(self, state: "SimState", setup: EpisodeSetup) -> bool:
        raise NotImplementedError

    def description(self, setup: EpisodeSetup) -> str:
        raise NotImplementedError

    def check_failure(self, state: "SimState", setup: EpisodeSetup) -> str | None:
        raise NotImplementedError

    def goal_error(self, state: "SimState", setup: EpisodeSetup) -> float | None:
        raise NotImplementedError

    def sim_params(self) -> SimParams:
        return self.params

    def sensors(self):
        return self.sensor_overrides

    def command_interface(self) -> str | None:
        return self.interface

    def observation_pipeline(self):
        return self.pipeline

    def metrics(self):
        return self.metric_list if self.metric_list is not None else super().metrics()

    def disturbances(self):
        return self.disturbance_list
