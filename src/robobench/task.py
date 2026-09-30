"""A task: one thing the benchmark asks a robot to do.

Defining a task means writing four methods:
    build_scene   what's in the world
    reset         seed -> starting conditions
    is_success    has the robot done it?
    description   the objective in plain language
and recording two demonstrations: one that succeeds and one that fails.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydrake.multibody.parsing import Parser
from pydrake.multibody.plant import MultibodyPlant
from pydrake.systems.framework import Context, DiagramBuilder

from robobench.controller import Action
from robobench.robot import Robot


@dataclass
class Demonstration:
    """A recorded run of a task: the commands sent at each control step, from one seed.

    Replaying the success demo must succeed and replaying the failure demo must not.
    That checks the task is well defined, and shows what the goal looks like.
    """

    seed: int
    actions: list[Action]


class Task(ABC):
    """Base class for every task."""

    name: str
    robot: Robot
    max_duration: float = 20.0
    """Seconds of simulated time before the episode ends as a timeout."""

    @abstractmethod
    def build_scene(self, builder: DiagramBuilder, plant: MultibodyPlant, parser: Parser) -> None:
        """Add everything except the robot: the floor, table, objects, terrain..."""

    @abstractmethod
    def reset(self, seed: int, plant: MultibodyPlant, context: Context) -> dict:
        """Set the starting conditions for this seed, and return the goal.

        The same seed must always give the same start and goal.
        """

    @abstractmethod
    def is_success(self, plant: MultibodyPlant, context: Context, goal: dict) -> bool:
        """Whether the goal has been reached, judged from the true simulation state."""

    @abstractmethod
    def description(self, goal: dict) -> str:
        """The objective in plain language, as the controller will read it."""

    def is_failure(self, plant: MultibodyPlant, context: Context, goal: dict) -> bool:
        """Whether to end early as a failure (robot fell, object dropped). Optional."""
        return False

    def demonstrations(self) -> dict[str, Demonstration]:
        """{"success": ..., "failure": ...}, loaded from files stored beside the task."""
        raise NotImplementedError
