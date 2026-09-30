"""G1 walks from a random start to a random goal across rocky terrain."""

from __future__ import annotations

from robobench.tasks.registry import register_task
from robobench.tasks.task import Task


@register_task("g1/walk_rocky_terrain", robot="unitree_g1", tags=("locomotion",))
def make(
    terrain_variant: int = 0,
    goal_tolerance: float = 0.3,
    min_start_goal_distance: float = 5.0,
    max_duration: float = 60.0,
    pushes: bool = False,
) -> Task:
    """A ComposedTask:

    Robot: UnitreeG1. Scene: rocky_terrain(terrain_variant).
    Reset: start pose in "start_area"; goal pose in "goal_area" at least
        `min_start_goal_distance` away (sent to the controller); small joint perturbation.
    Success: pelvis within `goal_tolerance` (horizontal) of the goal.
    Failure: pelvis below 0.4 m ("fell").
    Disturbances: optional random pushes to the torso.
    Demos: success = reaches the goal; failure = falls on the rocks.
    """
    raise NotImplementedError
