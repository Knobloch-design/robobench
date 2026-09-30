"""A reference sheet of constants an LLM can consult.

Populated automatically from the session's robot constants (joint limits, link
lengths, etc.) and extendable by the user with task rules or anything else.
It can be pasted into the prompt as text, or exposed as a lookup tool for
models that support tool calling.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from robobench_sdk.specs import SessionInfo


class ReferenceSheet:
    def __init__(self, entries: Mapping[str, Any] | None = None) -> None:
        raise NotImplementedError

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ReferenceSheet":
        raise NotImplementedError

    def set(self, key: str, value: Any, description: str = "") -> None:
        raise NotImplementedError

    def get(self, key: str) -> Any:
        """Raises KeyError if missing."""
        raise NotImplementedError

    def keys(self) -> Iterable[str]:
        raise NotImplementedError

    def update_from_session(self, session: SessionInfo) -> None:
        """Add robot constants and action/observation limits from the handshake."""
        raise NotImplementedError

    def as_text(self, keys: Iterable[str] | None = None) -> str:
        """Human/LLM-readable rendering, optionally limited to some keys."""
        raise NotImplementedError

    def lookup_tool_schema(self) -> dict[str, Any]:
        """JSON-schema description of a `lookup(key)` tool, for tool-calling models."""
        raise NotImplementedError
