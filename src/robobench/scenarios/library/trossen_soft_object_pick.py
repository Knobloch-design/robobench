"""Trossen bimanual cell picks up a soft (deformable) object from the table."""

from __future__ import annotations

from robobench.scenarios.registry import register_scenario
from robobench.scenarios.scenario import Scenario


@register_scenario("trossen/soft_object_pick", tags=("trossen", "manipulation", "deformable"))
def make(
    object_name: str = "soft_ball",
    lift_height: float = 0.1,
    hold_time: float = 2.0,
    max_duration: float = 30.0,
) -> Scenario:
    """
    Robot: TrossenStationaryAI. Scene: tabletop(deformable=(object_name,)).
    Randomizers: object pose on the table.
    Goal: object lifted `lift_height` above its start.
    Terminations: goal held for `hold_time`; object off the table.
    Sim params: SAP contact (required for deformable bodies).
    """
    raise NotImplementedError
