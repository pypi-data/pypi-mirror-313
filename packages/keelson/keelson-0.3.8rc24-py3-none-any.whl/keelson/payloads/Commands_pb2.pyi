from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandThruster(_message.Message):
    __slots__ = ("timestamp", "set_percentage", "actual_percentage")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set_percentage: float
    actual_percentage: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set_percentage: _Optional[float] = ..., actual_percentage: _Optional[float] = ...) -> None: ...

class CommandEngine(_message.Message):
    __slots__ = ("timestamp", "set_rpm", "actual_rpm")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_RPM_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_RPM_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set_rpm: float
    actual_rpm: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set_rpm: _Optional[float] = ..., actual_rpm: _Optional[float] = ...) -> None: ...

class CommandEnginePercentage(_message.Message):
    __slots__ = ("timestamp", "set_percentage", "actual_percentage")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set_percentage: float
    actual_percentage: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set_percentage: _Optional[float] = ..., actual_percentage: _Optional[float] = ...) -> None: ...

class CommandEngineMode(_message.Message):
    __slots__ = ("timestamp", "set", "actual")
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[CommandEngineMode.Mode]
        STOP: _ClassVar[CommandEngineMode.Mode]
        STANDBY: _ClassVar[CommandEngineMode.Mode]
        RUNNING: _ClassVar[CommandEngineMode.Mode]
    UNKNOWN: CommandEngineMode.Mode
    STOP: CommandEngineMode.Mode
    STANDBY: CommandEngineMode.Mode
    RUNNING: CommandEngineMode.Mode
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set: CommandEngineMode.Mode
    actual: CommandEngineMode.Mode
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set: _Optional[_Union[CommandEngineMode.Mode, str]] = ..., actual: _Optional[_Union[CommandEngineMode.Mode, str]] = ...) -> None: ...

class CommandRudder(_message.Message):
    __slots__ = ("timestamp", "set_degrees", "actual_degrees")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SET_DEGREES_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_DEGREES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    set_degrees: float
    actual_degrees: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., set_degrees: _Optional[float] = ..., actual_degrees: _Optional[float] = ...) -> None: ...

class CommandPanTiltXY(_message.Message):
    __slots__ = ("set_x_degrees", "set_y_degrees", "move_x_degrees", "move_y_degrees", "actual_x_degrees", "actual_y_degrees")
    SET_X_DEGREES_FIELD_NUMBER: _ClassVar[int]
    SET_Y_DEGREES_FIELD_NUMBER: _ClassVar[int]
    MOVE_X_DEGREES_FIELD_NUMBER: _ClassVar[int]
    MOVE_Y_DEGREES_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_X_DEGREES_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_Y_DEGREES_FIELD_NUMBER: _ClassVar[int]
    set_x_degrees: float
    set_y_degrees: float
    move_x_degrees: float
    move_y_degrees: float
    actual_x_degrees: float
    actual_y_degrees: float
    def __init__(self, set_x_degrees: _Optional[float] = ..., set_y_degrees: _Optional[float] = ..., move_x_degrees: _Optional[float] = ..., move_y_degrees: _Optional[float] = ..., actual_x_degrees: _Optional[float] = ..., actual_y_degrees: _Optional[float] = ...) -> None: ...

class CommandPrimitiveFloat(_message.Message):
    __slots__ = ("timestamp", "value_set", "value_actual")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value_set: float
    value_actual: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value_set: _Optional[float] = ..., value_actual: _Optional[float] = ...) -> None: ...

class CommandPrimitiveInt(_message.Message):
    __slots__ = ("timestamp", "value_set", "value_actual")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value_set: int
    value_actual: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value_set: _Optional[int] = ..., value_actual: _Optional[int] = ...) -> None: ...

class CommandPrimitiveBool(_message.Message):
    __slots__ = ("timestamp", "value_set", "value_actual")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value_set: bool
    value_actual: bool
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value_set: bool = ..., value_actual: bool = ...) -> None: ...

class CommandPrimitiveString(_message.Message):
    __slots__ = ("timestamp", "value_set", "value_actual")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value_set: str
    value_actual: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value_set: _Optional[str] = ..., value_actual: _Optional[str] = ...) -> None: ...
