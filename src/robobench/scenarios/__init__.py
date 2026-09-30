"""Building blocks for defining tests, a registry, and a library of ready-made tests.

A `Scenario` is a test definition. Users compose one from:
    robot + scene + goal + randomizers + terminations + metrics + disturbances + sim params
Calling `scenario.sample(seed)` gives a concrete `ScenarioInstance` for one episode.
"""

from robobench.scenarios.registry import get_scenario, list_scenarios, register_scenario
from robobench.scenarios.scenario import Scenario, ScenarioInstance

__all__ = ["Scenario", "ScenarioInstance", "get_scenario", "list_scenarios", "register_scenario"]
