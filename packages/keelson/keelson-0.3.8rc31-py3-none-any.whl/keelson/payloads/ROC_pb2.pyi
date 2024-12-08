from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Assignment(_message.Message):
    __slots__ = ("station_id", "vessel_id", "state")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Assignment.State]
        UNASSIGNED: _ClassVar[Assignment.State]
        WATCHING: _ClassVar[Assignment.State]
        CONTROLLING: _ClassVar[Assignment.State]
    UNKNOWN: Assignment.State
    UNASSIGNED: Assignment.State
    WATCHING: Assignment.State
    CONTROLLING: Assignment.State
    STATION_ID_FIELD_NUMBER: _ClassVar[int]
    VESSEL_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    station_id: str
    vessel_id: str
    state: Assignment.State
    def __init__(self, station_id: _Optional[str] = ..., vessel_id: _Optional[str] = ..., state: _Optional[_Union[Assignment.State, str]] = ...) -> None: ...

class Assignments(_message.Message):
    __slots__ = ("assignments", "source_timestamp")
    ASSIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    assignments: _containers.RepeatedCompositeFieldContainer[Assignment]
    source_timestamp: _timestamp_pb2.Timestamp
    def __init__(self, assignments: _Optional[_Iterable[_Union[Assignment, _Mapping]]] = ..., source_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
