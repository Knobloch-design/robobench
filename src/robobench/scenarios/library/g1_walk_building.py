"""G1 walks between two random rooms of a building."""

from __future__ import annotations

from robobench.scenarios.registry import register_scenario
from robobench.scenarios.scenario import Scenario


@register_scenario("g1/walk_building", tags=("g1", "locomotion", "navigation"))
def make(
    building_variant: int = 0,
    goal_tolerance: float = 0.5,
    max_duration: float = 120.0,
) -> Scenario:
    """
    Robot: UnitreeG1 (head camera on). Scene: building(building_variant).
    Randomizers: start and goal rooms chosen at random (different rooms), poses within them.
    Goal: pelvis within `goal_tolerance` of the goal. The description names the goal room.
    Terminations: goal reached; fell.
    """
    raise NotImplementedError
