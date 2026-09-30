"""The task base class.

Defining a task means specifying the four things the design calls for:

    build_scene   the scene to simulate (models and systems added to a Drake diagram)
    reset         a reset map: random seed -> valid initial conditions (a Drake context)
    is_success    a success condition that reads the system state
    description   a natural-language description of the objective

plus a robot, and two demonstration trajectories (one success, one failure) stored
beside the task and checked by `robobench validate-task`.

Everything else has a default. Subclass `Task` directly for full control, or use
`ComposedTask` to assemble one from the helpers in `robobench.tasks.helpers`.
"""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from robobench.config import SimParams
from robobench_sdk.specs import TaskInfo

if TYPE_CHECKING:
    from pydrake.multibody.parsing import Parser
    from pydrake.multibody.plant import MultibodyPlant
    from pydrake.systems.framework import DiagramBuilder

    from robobench.metrics.base import Metric
    from robobench.robots.base import RobotDefinition
    from robobench.sensors.definitions import SensorDefinition
    from robobench.sensors.pipeline import ObservationPipeline
    from robobench.sim.state import SceneHandles, SimState
    from robobench.tasks.demonstrations import Demonstration, DemoKind
    from robobench.tasks.helpers.disturbances import Disturbance


@dataclass(frozen=True)
class EpisodeSetup:
    """What `reset` produced for one seed. Recorded in results so any episode can be replayed."""

    task: str
    seed: int
    goal: Mapping[str, Any] = field(default_factory=dict)
    """Structured goal told to the controller, e.g. {"target_face": "+x"}. Plain data only."""
    info: Mapping[str, Any] = field(default_factory=dict)
    """Everything else that was randomized (start pose, friction...). Recorded, never sent to the controller."""


class Task(ABC):
    """Base class for every task in the benchmark."""

    name: str
    """Registry name, e.g. "leap/cube_reorientation". Set as a class or instance attribute."""
    robot: "RobotDefinition"
    """The robot this task uses. Set as a class or instance attribute."""

    max_duration: float = 30.0
    """Sim seconds before the episode ends as a timeout."""
    success_hold_time: float = 0.0
    """`is_success` must stay true this long (sim seconds) for the episode to count as a success."""
    tags: tuple[str, ...] = ()

    # ---- Required ---------------------------------------------------------------------------

    @abstractmethod
    def build_scene(
        self, builder: "DiagramBuilder", plant: "MultibodyPlant", parser: "Parser"
    ) -> Mapping[str, Any] | None:
        """Add the scene: terrain, furniture, manipulands, and any extra systems.

        Called after the robot has been added and before the plant is finalized.
        The plant is continuous-time (CENIC); don't change its time step.

        Returns:
            Optional named handles (model instances, body names...) for use in the other
            methods, available later as `state.scene.extras`.
        """

    @abstractmethod
    def reset(self, seed: int, state: "SimState") -> EpisodeSetup:
        """The reset map: write valid initial conditions for `seed` into the context.

        `state` wraps a freshly defaulted context; write to `state.plant_context`
        (robot pose, object poses, parameters). Must be deterministic: the same seed
        must always produce the same context and the same `EpisodeSetup`. Use
        `numpy.random.default_rng(seed)` for all randomness.
        """

    @abstractmethod
    def is_success(self, state: "SimState", setup: EpisodeSetup) -> bool:
        """The success condition, evaluated on ground-truth state after every control step."""

    @abstractmethod
    def description(self, setup: EpisodeSetup) -> str:
        """Natural-language objective sent to the controller, e.g. "Rotate the cube so the red face is up"."""

    # ---- Demonstrations ---------------------------------------------------------------------

    @property
    def demo_dir(self) -> Path:
        """Where this task's demonstrations live: `demos/<name>/` beside the file that registers
        the task (or that defines its class, if it isn't registered)."""
        from robobench.tasks.registry import source_file_for

        source = source_file_for(self.name) or Path(inspect.getfile(type(self)))
        return source.parent / "demos" / self.name.replace("/", "__")

    def demonstrations(self) -> Mapping["DemoKind", "Demonstration"]:
        """The task's success and failure demonstrations. Default: load from `demo_dir`.

        Raises:
            FileNotFoundError: a demonstration is missing (validate-task reports this).
        """
        raise NotImplementedError

    # ---- Optional hooks ---------------------------------------------------------------------

    def finalize_scene(self, builder: "DiagramBuilder", plant: "MultibodyPlant", scene: "SceneHandles") -> None:
        """Called after the plant is finalized, for systems that need a finalized plant."""

    def check_failure(self, state: "SimState", setup: EpisodeSetup) -> str | None:
        """Return a reason ("fell", "dropped") to end the episode early as a failure, else None."""
        return None

    def goal_error(self, state: "SimState", setup: EpisodeSetup) -> float | None:
        """Distance from the goal, for the goal-error metrics. None if the task has no natural measure."""
        return None

    def sim_params(self) -> SimParams:
        """CENIC accuracy and contact settings for this task."""
        return SimParams()

    def sensors(self) -> list["SensorDefinition"] | None:
        """None uses the robot's default sensors."""
        return None

    def command_interface(self) -> str | None:
        """None uses the robot's default command interface."""
        return None

    def observation_pipeline(self) -> "ObservationPipeline | None":
        """None passes raw sensor output through."""
        return None

    def metrics(self) -> list["Metric"]:
        from robobench.metrics.standard import default_metrics

        return default_metrics()

    def disturbances(self) -> list["Disturbance"]:
        return []

    # ---- Provided ---------------------------------------------------------------------------

    def task_info(self, setup: EpisodeSetup, episode_id: str, controller_seed: int) -> TaskInfo:
        """What the controller is told at the start of an episode."""
        raise NotImplementedError
