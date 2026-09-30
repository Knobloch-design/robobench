"""Handling for commands that can't be simulated at all."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from robobench.config import InvalidCommandMode
from robobench_sdk.specs import Action, ActionSpec


class InvalidKind(str, Enum):
    MISSING_FIELD = "missing_field"
    WRONG_SHAPE = "wrong_shape"
    NOT_NUMERIC = "not_numeric"
    NAN = "nan"
    INF = "inf"
    UNKNOWN_FIELD = "unknown_field"
    """Extra field the spec doesn't have. Logged and ignored; never ends an episode."""


@dataclass(frozen=True)
class InvalidCommandEvent:
    step: int
    time: float
    kind: InvalidKind
    field: str
    detail: str
    handled_by: str
    """"fail", "hold_last", "hold_default" (hold_last with no previous valid command), or "ignored"."""


class InvalidCommandFailure(Exception):
    """Raised in FAIL mode. The episode loop ends the episode with failure kind INVALID_COMMAND."""

    def __init__(self, event: InvalidCommandEvent) -> None:
        super().__init__(f"{event.kind.value} in field {event.field!r}: {event.detail}")
        self.event = event


class InvalidCommandHandler:
    def __init__(self, spec: ActionSpec, mode: InvalidCommandMode, hold_default: Callable[[], Action]) -> None:
        """
        Args:
            spec: The action spec actions are checked against.
            mode: FAIL (default) or HOLD_LAST.
            hold_default: Produces a safe "hold still" action, used by HOLD_LAST before any
                valid action has been seen (see `CommandInterface.hold_default`).
        """
        raise NotImplementedError

    def reset(self) -> None:
        """Forget the last valid action and events at episode start."""
        raise NotImplementedError

    def find_problems(self, action: Action) -> list[tuple[InvalidKind, str, str]]:
        """All (kind, field, detail) problems with `action`, without handling them."""
        raise NotImplementedError

    def handle(self, action: Action, step: int, time: float) -> Action:
        """Return the action to use this step.

        Valid actions are returned unchanged and remembered as the last valid action.

        Raises:
            InvalidCommandFailure: in FAIL mode, for any problem other than UNKNOWN_FIELD.
        """
        raise NotImplementedError

    @property
    def events(self) -> list[InvalidCommandEvent]:
        raise NotImplementedError
