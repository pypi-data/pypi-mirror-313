from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimestampedBytes(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: bytes
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[bytes] = ...) -> None: ...

class TimestampedDouble(_message.Message):
    __slots__ = ("timestamp", "value", "unit")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: float
    unit: MeasurementUnit
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ..., unit: _Optional[_Union[MeasurementUnit, _Mapping]] = ...) -> None: ...

class TimestampedFloat(_message.Message):
    __slots__ = ("timestamp", "value", "unit")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: float
    unit: MeasurementUnit
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[float] = ..., unit: _Optional[_Union[MeasurementUnit, _Mapping]] = ...) -> None: ...

class TimestampedString(_message.Message):
    __slots__ = ("timestamp", "value", "unit")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: str
    unit: MeasurementUnit
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[str] = ..., unit: _Optional[_Union[MeasurementUnit, _Mapping]] = ...) -> None: ...

class MeasurementUnit(_message.Message):
    __slots__ = ("unit",)
    class Unit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[MeasurementUnit.Unit]
        METERS: _ClassVar[MeasurementUnit.Unit]
        DEGREES: _ClassVar[MeasurementUnit.Unit]
        KNOTS: _ClassVar[MeasurementUnit.Unit]
        CELSIUS: _ClassVar[MeasurementUnit.Unit]
    UNKNOWN: MeasurementUnit.Unit
    METERS: MeasurementUnit.Unit
    DEGREES: MeasurementUnit.Unit
    KNOTS: MeasurementUnit.Unit
    CELSIUS: MeasurementUnit.Unit
    UNIT_FIELD_NUMBER: _ClassVar[int]
    unit: MeasurementUnit.Unit
    def __init__(self, unit: _Optional[_Union[MeasurementUnit.Unit, str]] = ...) -> None: ...
