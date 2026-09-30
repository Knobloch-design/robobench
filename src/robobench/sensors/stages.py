"""Ready-made observation pipeline stages."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from robobench.sensors.pipeline import ObservationStage
from robobench_sdk.specs import Observation, ObservationSpec


class GaussianNoise(ObservationStage):
    """Add zero-mean Gaussian noise to a numeric field."""

    def __init__(self, field: str, std: float | np.ndarray) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class Bias(ObservationStage):
    """Add a constant offset, optionally re-sampled each episode (e.g. encoder calibration error)."""

    def __init__(self, field: str, offset: float | np.ndarray = 0.0, sample_std: float | None = None) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class Delay(ObservationStage):
    """Deliver a field `steps` control steps late (sensor/communication latency)."""

    def __init__(self, fields: Sequence[str], steps: int) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class Dropout(ObservationStage):
    """With probability `p`, repeat a field's previous value instead of the new one (a missed reading)."""

    def __init__(self, fields: Sequence[str], p: float) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class Downsample(ObservationStage):
    """Update a field only every `every_n` control steps (a slower sensor)."""

    def __init__(self, fields: Sequence[str], every_n: int) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class Quantize(ObservationStage):
    """Round a field to a resolution (encoder ticks)."""

    def __init__(self, field: str, resolution: float) -> None:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class ResizeImage(ObservationStage):
    """Resize an image field."""

    def __init__(self, field: str, width: int, height: int) -> None:
        raise NotImplementedError

    def output_spec(self, input_spec: ObservationSpec) -> ObservationSpec:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError


class DropFields(ObservationStage):
    """Remove fields entirely (e.g. test a controller without cameras)."""

    def __init__(self, fields: Sequence[str]) -> None:
        raise NotImplementedError

    def output_spec(self, input_spec: ObservationSpec) -> ObservationSpec:
        raise NotImplementedError

    def apply(self, observation: Observation) -> Observation:
        raise NotImplementedError
