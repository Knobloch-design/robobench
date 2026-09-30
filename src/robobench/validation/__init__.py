"""Command checks run on every action before it reaches the robot.

Order each step:
    1. InvalidCommandHandler: missing fields, wrong shape, NaN/inf. (fail | hold_last)
    2. CommandValidator: values outside the action spec's limits. (off | monitor | correct)
"""

from robobench.validation.invalid import InvalidCommandEvent, InvalidCommandFailure, InvalidCommandHandler, InvalidKind
from robobench.validation.limits import CommandValidator, ValidationResult, Violation

__all__ = [
    "CommandValidator",
    "InvalidCommandEvent",
    "InvalidCommandFailure",
    "InvalidCommandHandler",
    "InvalidKind",
    "ValidationResult",
    "Violation",
]
