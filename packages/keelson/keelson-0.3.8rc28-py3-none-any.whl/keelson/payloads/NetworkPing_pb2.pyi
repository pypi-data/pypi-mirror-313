from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NetworkPing(_message.Message):
    __slots__ = ("timestamp_sender", "timestamp_receiver", "id_sender", "id_receiver", "ping_count", "payload_description", "start_mb", "end_mb", "step_mb", "payload_size_mb", "payload_size_bytes", "dummy_payload", "json_string")
    TIMESTAMP_SENDER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_RECEIVER_FIELD_NUMBER: _ClassVar[int]
    ID_SENDER_FIELD_NUMBER: _ClassVar[int]
    ID_RECEIVER_FIELD_NUMBER: _ClassVar[int]
    PING_COUNT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    START_MB_FIELD_NUMBER: _ClassVar[int]
    END_MB_FIELD_NUMBER: _ClassVar[int]
    STEP_MB_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_SIZE_MB_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    DUMMY_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    timestamp_sender: _timestamp_pb2.Timestamp
    timestamp_receiver: _timestamp_pb2.Timestamp
    id_sender: str
    id_receiver: str
    ping_count: int
    payload_description: str
    start_mb: float
    end_mb: float
    step_mb: float
    payload_size_mb: float
    payload_size_bytes: float
    dummy_payload: bytes
    json_string: str
    def __init__(self, timestamp_sender: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp_receiver: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id_sender: _Optional[str] = ..., id_receiver: _Optional[str] = ..., ping_count: _Optional[int] = ..., payload_description: _Optional[str] = ..., start_mb: _Optional[float] = ..., end_mb: _Optional[float] = ..., step_mb: _Optional[float] = ..., payload_size_mb: _Optional[float] = ..., payload_size_bytes: _Optional[float] = ..., dummy_payload: _Optional[bytes] = ..., json_string: _Optional[str] = ...) -> None: ...

class NetworkResult(_message.Message):
    __slots__ = ("timestamp", "id_sender", "id_target", "payload_description", "latency_ms", "payload_size_mb", "timestamp_sender_init", "timestamp_sender_response", "timestamp_target", "clock_offset", "clock_offset_ping_adjusted", "json_string")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ID_SENDER_FIELD_NUMBER: _ClassVar[int]
    ID_TARGET_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_SIZE_MB_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_SENDER_INIT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_SENDER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_TARGET_FIELD_NUMBER: _ClassVar[int]
    CLOCK_OFFSET_FIELD_NUMBER: _ClassVar[int]
    CLOCK_OFFSET_PING_ADJUSTED_FIELD_NUMBER: _ClassVar[int]
    JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    id_sender: str
    id_target: str
    payload_description: str
    latency_ms: float
    payload_size_mb: float
    timestamp_sender_init: _timestamp_pb2.Timestamp
    timestamp_sender_response: _timestamp_pb2.Timestamp
    timestamp_target: _timestamp_pb2.Timestamp
    clock_offset: float
    clock_offset_ping_adjusted: float
    json_string: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id_sender: _Optional[str] = ..., id_target: _Optional[str] = ..., payload_description: _Optional[str] = ..., latency_ms: _Optional[float] = ..., payload_size_mb: _Optional[float] = ..., timestamp_sender_init: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp_sender_response: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp_target: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., clock_offset: _Optional[float] = ..., clock_offset_ping_adjusted: _Optional[float] = ..., json_string: _Optional[str] = ...) -> None: ...
