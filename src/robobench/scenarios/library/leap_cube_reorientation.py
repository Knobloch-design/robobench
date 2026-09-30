"""LEAP hand rotates a cube in-hand so a target face ends up on top."""

from __future__ import annotations

from robobench.scenarios.registry import register_scenario
from robobench.scenarios.scenario import Scenario


@register_scenario("leap/cube_reorientation", tags=("leap_hand", "manipulation", "dexterous"))
def make(
    cube_size: float = 0.06,
    angle_tolerance: float = 0.2,
    hold_time: float = 1.0,
    max_duration: float = 20.0,
    randomize_friction: bool = True,
) -> Scenario:
    """
    Robot: LeapHand (palm up). Scene: hand_workspace("cube").
    Randomizers: cube pose above the palm, target face from the 5 faces not already on top,
        optional friction/mass variation.
    Goal: target face normal within `angle_tolerance` of +z.
    Terminations: goal held for `hold_time`; cube below the palm ("dropped").
    Sim params: smaller time step for contact-rich manipulation.
    """
    raise NotImplementedError
