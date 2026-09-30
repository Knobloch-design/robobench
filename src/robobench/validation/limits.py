"""Checking commands against the robot's limits (the action spec's low/high bounds)."""

from __future__ import annotations

from dataclasses import dataclass

from robobench.config import ValidationMode
from robobench_sdk.specs import Action, ActionSpec


@dataclass(frozen=True)
class Violation:
    step: int
    time: float
    field: str
    """Action field, e.g. "q" or "kp"."""
    index: int
    element_name: str | None
    """e.g. the joint name."""
    commanded: float
    lower: float
    upper: float
    corrected_to: float | None
    """The clipped value in CORRECT mode, None otherwise."""


@dataclass(frozen=True)
class ValidationResult:
    action: Action
    """The action to apply: unchanged in OFF/MONITOR, clipped in CORRECT."""
    violations: list[Violation]


class CommandValidator:
    """Violations are detected and returned in every mode, including OFF, so violation-rate
    metrics always exist. The mode only decides whether the action is changed."""

    def __init__(self, spec: ActionSpec, mode: ValidationMode = ValidationMode.MONITOR) -> None:
        raise NotImplementedError

    def validate(self, action: Action, step: int, time: float) -> ValidationResult:
        """Check an action that has already passed the invalid-command check."""
        raise NotImplementedError
