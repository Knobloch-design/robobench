from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tensor(_message.Message):
    __slots__ = ("dtype", "shape", "data")
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    dtype: str
    shape: _containers.RepeatedScalarFieldContainer[int]
    data: bytes
    def __init__(self, dtype: _Optional[str] = ..., shape: _Optional[_Iterable[int]] = ..., data: _Optional[bytes] = ...) -> None: ...

class ArraySpec(_message.Message):
    __slots__ = ("name", "shape", "dtype", "low", "high", "units", "element_names", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_NAMES_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    shape: _containers.RepeatedScalarFieldContainer[int]
    dtype: str
    low: Tensor
    high: Tensor
    units: str
    element_names: _containers.RepeatedScalarFieldContainer[str]
    description: str
    def __init__(self, name: _Optional[str] = ..., shape: _Optional[_Iterable[int]] = ..., dtype: _Optional[str] = ..., low: _Optional[_Union[Tensor, _Mapping]] = ..., high: _Optional[_Union[Tensor, _Mapping]] = ..., units: _Optional[str] = ..., element_names: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ...) -> None: ...

class TextSpec(_message.Message):
    __slots__ = ("name", "description")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ObservationSpec(_message.Message):
    __slots__ = ("arrays", "texts")
    class ArraysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArraySpec
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ArraySpec, _Mapping]] = ...) -> None: ...
    class TextsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: TextSpec
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[TextSpec, _Mapping]] = ...) -> None: ...
    ARRAYS_FIELD_NUMBER: _ClassVar[int]
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    arrays: _containers.MessageMap[str, ArraySpec]
    texts: _containers.MessageMap[str, TextSpec]
    def __init__(self, arrays: _Optional[_Mapping[str, ArraySpec]] = ..., texts: _Optional[_Mapping[str, TextSpec]] = ...) -> None: ...

class ActionSpec(_message.Message):
    __slots__ = ("interface", "arrays")
    class ArraysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ArraySpec
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ArraySpec, _Mapping]] = ...) -> None: ...
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    ARRAYS_FIELD_NUMBER: _ClassVar[int]
    interface: str
    arrays: _containers.MessageMap[str, ArraySpec]
    def __init__(self, interface: _Optional[str] = ..., arrays: _Optional[_Mapping[str, ArraySpec]] = ...) -> None: ...

class SessionInfo(_message.Message):
    __slots__ = ("protocol_version", "robot", "observation_spec", "action_spec", "control_period", "timing_mode", "robot_constants")
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_SPEC_FIELD_NUMBER: _ClassVar[int]
    ACTION_SPEC_FIELD_NUMBER: _ClassVar[int]
    CONTROL_PERIOD_FIELD_NUMBER: _ClassVar[int]
    TIMING_MODE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_CONSTANTS_FIELD_NUMBER: _ClassVar[int]
    protocol_version: int
    robot: str
    observation_spec: ObservationSpec
    action_spec: ActionSpec
    control_period: float
    timing_mode: str
    robot_constants: _struct_pb2.Struct
    def __init__(self, protocol_version: _Optional[int] = ..., robot: _Optional[str] = ..., observation_spec: _Optional[_Union[ObservationSpec, _Mapping]] = ..., action_spec: _Optional[_Union[ActionSpec, _Mapping]] = ..., control_period: _Optional[float] = ..., timing_mode: _Optional[str] = ..., robot_constants: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ConnectReply(_message.Message):
    __slots__ = ("protocol_version", "controller_name")
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_NAME_FIELD_NUMBER: _ClassVar[int]
    protocol_version: int
    controller_name: str
    def __init__(self, protocol_version: _Optional[int] = ..., controller_name: _Optional[str] = ...) -> None: ...

class TaskInfo(_message.Message):
    __slots__ = ("task", "episode_id", "description", "goal", "max_duration", "controller_seed", "metadata")
    TASK_FIELD_NUMBER: _ClassVar[int]
    EPISODE_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    MAX_DURATION_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_SEED_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    task: str
    episode_id: str
    description: str
    goal: _struct_pb2.Struct
    max_duration: float
    controller_seed: int
    metadata: _struct_pb2.Struct
    def __init__(self, task: _Optional[str] = ..., episode_id: _Optional[str] = ..., description: _Optional[str] = ..., goal: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., max_duration: _Optional[float] = ..., controller_seed: _Optional[int] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Observation(_message.Message):
    __slots__ = ("seq", "time", "arrays", "texts")
    class ArraysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Tensor
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Tensor, _Mapping]] = ...) -> None: ...
    class TextsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SEQ_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ARRAYS_FIELD_NUMBER: _ClassVar[int]
    TEXTS_FIELD_NUMBER: _ClassVar[int]
    seq: int
    time: float
    arrays: _containers.MessageMap[str, Tensor]
    texts: _containers.ScalarMap[str, str]
    def __init__(self, seq: _Optional[int] = ..., time: _Optional[float] = ..., arrays: _Optional[_Mapping[str, Tensor]] = ..., texts: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Action(_message.Message):
    __slots__ = ("seq", "arrays")
    class ArraysEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Tensor
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Tensor, _Mapping]] = ...) -> None: ...
    SEQ_FIELD_NUMBER: _ClassVar[int]
    ARRAYS_FIELD_NUMBER: _ClassVar[int]
    seq: int
    arrays: _containers.MessageMap[str, Tensor]
    def __init__(self, seq: _Optional[int] = ..., arrays: _Optional[_Mapping[str, Tensor]] = ...) -> None: ...

class EpisodeSummary(_message.Message):
    __slots__ = ("episode_id", "success", "termination_reason", "metrics")
    class MetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    EPISODE_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TERMINATION_REASON_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    episode_id: str
    success: bool
    termination_reason: str
    metrics: _containers.ScalarMap[str, float]
    def __init__(self, episode_id: _Optional[str] = ..., success: _Optional[bool] = ..., termination_reason: _Optional[str] = ..., metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
