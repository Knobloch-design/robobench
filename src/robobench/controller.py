"""What a user writes to control a robot.

A controller only sees observations (sensor readings) and returns actions (motor
commands), the same as on a real robot. It never sees the simulator.

The controller runs in its own process, separate from the simulation. The user writes
a plain Controller subclass; controller_server.py wraps it in a gRPC server, and the
simulation talks to it through a RemoteController (remote_controller.py).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

Observation = dict[str, np.ndarray]
"""Sensor readings by name, e.g. {"joint_position": ..., "camera_rgb": ...}."""

Action = dict[str, np.ndarray]
"""Motor commands by name, e.g. {"joint_position_target": ...}."""


@dataclass
class TaskInfo:
    """What the controller is told at the start of an episode."""

    description: str
    """The objective in plain language, e.g. "Rotate the cube so the red face is on top"."""
    goal: dict
    """The same objective as data, e.g. {"target_face": "+x"}."""


class Controller(ABC):
    """Base class for every controller: a neural net, an LLM, a script, anything."""

    def reset(self, task: TaskInfo) -> None:
        """Called at the start of every episode with the new objective. Optional."""

    @abstractmethod
    def act(self, observation: Observation) -> Action:
        """Called every control step with the latest sensor readings; returns the next command."""
