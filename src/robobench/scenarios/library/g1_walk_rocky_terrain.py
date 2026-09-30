"""G1 walks from a random start to a random goal across rocky terrain."""

from __future__ import annotations

from robobench.scenarios.registry import register_scenario
from robobench.scenarios.scenario import Scenario


@register_scenario("g1/walk_rocky_terrain", tags=("g1", "locomotion"))
def make(
    terrain_variant: int = 0,
    goal_tolerance: float = 0.3,
    min_start_goal_distance: float = 5.0,
    max_duration: float = 60.0,
    pushes: bool = False,
) -> Scenario:
    """
    Robot: UnitreeG1. Scene: rocky_terrain(terrain_variant).
    Randomizers: start pose in "start_area", goal pose in "goal_area" at least
        `min_start_goal_distance` away, small joint perturbation.
    Goal: pelvis within `goal_tolerance` (horizontal) of the goal.
    Terminations: goal reached; pelvis below 0.4 m ("fell").
    Disturbances: optional random pushes to the torso.
    """
    raise NotImplementedError
