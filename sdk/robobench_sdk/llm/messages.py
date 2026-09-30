"""Chat message type shared by the harness and memory."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class ChatMessage:
    role: str
    """"system", "user", or "assistant"."""
    content: str
    images: list[np.ndarray] = field(default_factory=list)
