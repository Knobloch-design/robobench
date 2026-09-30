"""LEAP hand rotates a cube in-hand so a target face ends up on top."""

from __future__ import annotations

from robobench.tasks.registry import register_task
from robobench.tasks.task import Task


@register_task("leap/cube_reorientation", robot="leap_hand", tags=("manipulation", "dexterous"))
def make(
    cube_size: float = 0.06,
    angle_tolerance: float = 0.2,
    hold_time: float = 1.0,
    max_duration: float = 20.0,
    randomize_friction: bool = True,
) -> Task:
    """A ComposedTask:

    Robot: LeapHand (palm up). Scene: hand_workspace("cube").
    Reset: cube pose above the palm; target face from the 5 faces not already on top
        (sent to the controller); optional friction/mass variation.
    Success: target face normal within `angle_tolerance` of +z, held for `hold_time`.
    Failure: cube below the palm ("dropped").
    Sim params: tighter CENIC accuracy for contact-rich manipulation.
    Demos: success = rotates to the target face; failure = drops the cube.
    """
    raise NotImplementedError
