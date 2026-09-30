"""Controller-side SDK for robobench.

Users subclass `Controller`, then either let the benchmark launch it
(`ControllerLaunchConfig(target="my_pkg.my_module:MyController")`) or start it
themselves with `serve(...)`. Nothing in this package imports Drake.
"""

from robobench_sdk.controller import Controller, IncompatibleSpecError
from robobench_sdk.protocol import PROTOCOL_VERSION
from robobench_sdk.server import serve
from robobench_sdk.specs import (
    Action,
    ActionSpec,
    ArraySpec,
    EpisodeSummary,
    Observation,
    ObservationSpec,
    SessionInfo,
    TaskInfo,
    TextSpec,
)

__all__ = [
    "PROTOCOL_VERSION",
    "Action",
    "ActionSpec",
    "ArraySpec",
    "Controller",
    "EpisodeSummary",
    "IncompatibleSpecError",
    "Observation",
    "ObservationSpec",
    "SessionInfo",
    "TaskInfo",
    "TextSpec",
    "serve",
]
