"""Goals: what the task is (told to the controller) and how far from it we are (measured on ground truth)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from robobench.sim.state import SimState
    from robobench.tasks.task import EpisodeSetup


class Goal(ABC):
    tolerance: float
    """`error <= tolerance` counts as achieved."""

    @abstractmethod
    def describe(self, setup: "EpisodeSetup") -> str:
        """Natural-language objective for this episode."""

    @abstractmethod
    def error(self, state: "SimState", setup: "EpisodeSetup") -> float:
        """Distance from the goal (units depend on the goal). 0 means exactly achieved."""

    def is_achieved(self, state: "SimState", setup: "EpisodeSetup") -> bool:
        return self.error(state, setup) <= self.tolerance


class ReachPositionGoal(Goal):
    """Get a body (e.g. the G1 pelvis) to a sampled position. Error: horizontal distance (m)."""

    def __init__(self, body_name: str, target_key: str = "goal_pose", tolerance: float = 0.3, horizontal_only: bool = True) -> None:
        raise NotImplementedError

    def describe(self, setup) -> str:
        raise NotImplementedError

    def error(self, state, setup) -> float:
        raise NotImplementedError


class ObjectOrientationGoal(Goal):
    """Rotate an object so a sampled face points up. Error: angle between that face's normal and +z (rad)."""

    def __init__(self, object_body: str, face_key: str = "target_face", tolerance: float = 0.2) -> None:
        raise NotImplementedError

    def describe(self, setup) -> str:
        raise NotImplementedError

    def error(self, state, setup) -> float:
        raise NotImplementedError


class ObjectLiftGoal(Goal):
    """Lift an object to a height above its start. Error: remaining height (m), 0 once reached."""

    def __init__(self, object_body: str, height: float = 0.1, tolerance: float = 0.02) -> None:
        raise NotImplementedError

    def describe(self, setup) -> str:
        raise NotImplementedError

    def error(self, state, setup) -> float:
        raise NotImplementedError
