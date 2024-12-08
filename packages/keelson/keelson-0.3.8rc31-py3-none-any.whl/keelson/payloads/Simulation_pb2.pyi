from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SimulationState(_message.Message):
    __slots__ = ("timestamp", "state", "name", "id", "timestampSimulation")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[SimulationState.State]
        STOPPED: _ClassVar[SimulationState.State]
        ASSIGNED: _ClassVar[SimulationState.State]
        PLAYING: _ClassVar[SimulationState.State]
        PAUSED: _ClassVar[SimulationState.State]
    UNKNOWN: SimulationState.State
    STOPPED: SimulationState.State
    ASSIGNED: SimulationState.State
    PLAYING: SimulationState.State
    PAUSED: SimulationState.State
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPSIMULATION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    state: SimulationState.State
    name: str
    id: str
    timestampSimulation: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[SimulationState.State, str]] = ..., name: _Optional[str] = ..., id: _Optional[str] = ..., timestampSimulation: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
