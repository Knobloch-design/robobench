"""The gRPC protocol between the benchmark (client) and the controller (server).

The wire format is defined in `proto/controller.proto`; see it for the call order
and error codes. This module holds the protocol version and converts between the
plain dataclasses in `specs` (what user code sees) and the generated protobuf
messages (what goes over the wire). Numpy arrays travel as `Tensor` messages:
dtype, shape, and raw bytes, so there is no per-element conversion cost.
"""

from __future__ import annotations

import numpy as np

from robobench_sdk.proto import controller_pb2 as pb
from robobench_sdk.specs import Action, EpisodeSummary, Observation, SessionInfo, TaskInfo

PROTOCOL_VERSION = 1

DEFAULT_MAX_MESSAGE_BYTES = 64 * 1024 * 1024
"""gRPC's 4 MB default is too small for camera images; both sides raise it to this."""


class ProtocolError(Exception):
    """A malformed or unexpected message."""


class ProtocolVersionMismatch(ProtocolError):
    """The two sides speak different protocol versions."""


def tensor_to_proto(array: np.ndarray) -> pb.Tensor:
    raise NotImplementedError


def tensor_from_proto(message: pb.Tensor) -> np.ndarray:
    """Zero-copy where possible (numpy view over the message bytes, marked read-only)."""
    raise NotImplementedError


def session_to_proto(session: SessionInfo) -> pb.SessionInfo:
    raise NotImplementedError


def session_from_proto(message: pb.SessionInfo) -> SessionInfo:
    raise NotImplementedError


def task_to_proto(task: TaskInfo) -> pb.TaskInfo:
    raise NotImplementedError


def task_from_proto(message: pb.TaskInfo) -> TaskInfo:
    raise NotImplementedError


def observation_to_proto(observation: Observation, seq: int) -> pb.Observation:
    """Arrays go in `arrays`, strings in `texts`, and observation["time"] in `time`."""
    raise NotImplementedError


def observation_from_proto(message: pb.Observation) -> Observation:
    raise NotImplementedError


def action_to_proto(action: Action, seq: int) -> pb.Action:
    """Raises ProtocolError if a value can't be converted to an array.

    Values that convert but are wrong (NaN, wrong shape) are sent as-is: judging them is the
    benchmark's job, so that invalid commands are handled and logged the same way for everyone.
    """
    raise NotImplementedError


def action_from_proto(message: pb.Action) -> Action:
    raise NotImplementedError


def summary_to_proto(summary: EpisodeSummary) -> pb.EpisodeSummary:
    raise NotImplementedError


def summary_from_proto(message: pb.EpisodeSummary) -> EpisodeSummary:
    raise NotImplementedError
