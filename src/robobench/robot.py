"""A robot: its model, what it senses, and what commands it accepts."""

from abc import ABC, abstractmethod

from pydrake.multibody.parsing import Parser
from pydrake.multibody.plant import MultibodyPlant
from pydrake.systems.framework import Context, DiagramBuilder

from robobench.controller import Action, Observation


class Robot(ABC):
    """Base class for each robot (LEAP hand, Unitree G1, Trossen Stationary AI)."""

    name: str

    @abstractmethod
    def add_to_diagram(self, builder: DiagramBuilder, plant: MultibodyPlant, parser: Parser) -> None:
        """Load the robot's model, and add its actuators and any sensor systems (e.g. cameras)."""

    @abstractmethod
    def observe(self, plant: MultibodyPlant, context: Context) -> Observation:
        """Read the robot's sensors: only what the real robot could measure."""

    @abstractmethod
    def apply_action(self, action: Action, plant: MultibodyPlant, context: Context) -> None:
        """Send a command to the actuators, the way the real robot's driver would."""
