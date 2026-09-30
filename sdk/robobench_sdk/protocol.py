"""Messages exchanged between the benchmark (runner) and the controller process.

Exchange sequence (runner on the left, controller on the right):

    HELLO(SessionInfo)          ->
                                <-  HELLO_ACK  |  ERROR (incompatible specs / version)
    per episode:
      RESET(TaskInfo)           ->
                                <-  RESET_ACK
      OBSERVATION(Observation)  ->
                                <-  ACTION(Action)  |  ERROR (act() raised)
      ... repeated ...
      EPISODE_END(EpisodeSummary) ->
                                <-  EPISODE_END_ACK
    SHUTDOWN                    ->

Every message carries a sequence number. An ACTION echoes the sequence number of
the OBSERVATION it answers, which is how real-time mode matches late replies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

PROTOCOL_VERSION = 1


class MessageType(str, Enum):
    HELLO = "hello"
    HELLO_ACK = "hello_ack"
    RESET = "reset"
    RESET_ACK = "reset_ack"
    OBSERVATION = "observation"
    ACTION = "action"
    EPISODE_END = "episode_end"
    EPISODE_END_ACK = "episode_end_ack"
    SHUTDOWN = "shutdown"
    ERROR = "error"


@dataclass(frozen=True)
class Message:
    type: MessageType
    seq: int
    payload: Any = None
    """A spec dataclass, an Observation/Action dict, an error string, or None."""


class ProtocolError(Exception):
    """A malformed or unexpected message."""


class ProtocolVersionMismatch(ProtocolError):
    """The two sides speak different protocol versions."""


def encode(message: Message) -> bytes:
    """Serialize a message (including numpy arrays and spec dataclasses) to bytes.

    Planned implementation: msgpack, with numpy arrays packed as (dtype, shape, raw bytes).
    """
    raise NotImplementedError


def decode(data: bytes) -> Message:
    """Inverse of `encode`. Raises `ProtocolError` on malformed input."""
    raise NotImplementedError
