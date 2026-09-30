"""G1 walks between two random rooms of a building."""

from __future__ import annotations

from robobench.tasks.registry import register_task
from robobench.tasks.task import Task


@register_task("g1/walk_building", robot="unitree_g1", tags=("locomotion", "navigation"))
def make(
    building_variant: int = 0,
    goal_tolerance: float = 0.5,
    max_duration: float = 120.0,
) -> Task:
    """A ComposedTask:

    Robot: UnitreeG1 (head camera on). Scene: building(building_variant).
    Reset: start and goal in two different random rooms, random poses within them.
    Success: pelvis within `goal_tolerance` of the goal. The description names the goal room.
    Failure: fell.
    Demos: success = reaches the goal room; failure = walks into a wall and falls.
    """
    raise NotImplementedError
