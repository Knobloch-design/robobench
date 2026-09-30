"""The configurable pipeline between raw sensor output and the controller's observation.

    raw sensor fields  ->  stage 1  ->  stage 2  ->  ...  ->  observation sent to controller

An empty pipeline passes raw sensor output through unchanged, which is the default.
Stages run on the observation dict at each control step, outside the Drake diagram.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np

from robobench_sdk.specs import Observation, ObservationSpec


class ObservationStage(ABC):
    """One transformation of the observation (noise, delay, dropout, resizing...)."""

    def reset(self, rng: np.random.Generator) -> None:
        """Called at episode start. Stages with randomness or history must use this `rng` for reproducibility."""

    def output_spec(self, input_spec: ObservationSpec) -> ObservationSpec:
        """How this stage changes the spec. Default: unchanged."""
        return input_spec

    @abstractmethod
    def apply(self, observation: Observation) -> Observation:
        """Transform one observation. Must not modify its input in place."""


class ObservationPipeline:
    def __init__(self, stages: Sequence[ObservationStage] = ()) -> None:
        raise NotImplementedError

    @classmethod
    def passthrough(cls) -> "ObservationPipeline":
        return cls(())

    @classmethod
    def from_config(cls, config: list[dict]) -> "ObservationPipeline":
        """Build from YAML-style config, e.g. [{"type": "gaussian_noise", "field": "joint_position", "std": 0.01}]."""
        raise NotImplementedError

    def output_spec(self, raw_spec: ObservationSpec) -> ObservationSpec:
        """The spec the controller receives in the handshake."""
        raise NotImplementedError

    def reset(self, rng: np.random.Generator) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError
