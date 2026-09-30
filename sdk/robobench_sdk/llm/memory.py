"""Memory for LLM controllers.

Memory is split into two scopes:
  - "episode": cleared on every reset.
  - "persistent": kept across episodes. This lets a model learn between test runs,
    which changes what a benchmark measures, so it's opt-in.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal

from robobench_sdk.llm.messages import ChatMessage

Scope = Literal["episode", "persistent"]


@dataclass
class MemoryEntry:
    time: float
    """Simulation time the entry was recorded."""
    kind: str
    """e.g. "observation", "response", "note", "episode_summary"."""
    content: str
    scope: Scope = "episode"
    metadata: dict[str, Any] = field(default_factory=dict)


class Memory(ABC):
    @abstractmethod
    def add(self, entry: MemoryEntry) -> None: ...

    @abstractmethod
    def recent(self, n: int, scope: Scope | None = None) -> list[MemoryEntry]:
        """The last `n` entries, oldest first. `scope=None` returns both scopes."""

    @abstractmethod
    def search(self, query: str, k: int = 5) -> list[MemoryEntry]:
        """The `k` entries most relevant to `query`."""

    @abstractmethod
    def clear(self, scope: Scope = "episode") -> None: ...

    @abstractmethod
    def as_messages(self, max_entries: int | None = None) -> list[ChatMessage]:
        """Render memory as chat messages to include in the prompt."""


class RollingMemory(Memory):
    """Keeps the last `max_episode_entries` episode entries, and optionally persistent notes."""

    def __init__(self, max_episode_entries: int = 50, keep_persistent: bool = False) -> None:
        raise NotImplementedError

    def add(self, entry: MemoryEntry) -> None:
        raise NotImplementedError

    def recent(self, n: int, scope: Scope | None = None) -> list[MemoryEntry]:
        raise NotImplementedError

    def search(self, query: str, k: int = 5) -> list[MemoryEntry]:
        """Simple keyword match. Swap in an embedding-based Memory for anything smarter."""
        raise NotImplementedError

    def clear(self, scope: Scope = "episode") -> None:
        raise NotImplementedError

    def as_messages(self, max_entries: int | None = None) -> list[ChatMessage]:
        raise NotImplementedError
