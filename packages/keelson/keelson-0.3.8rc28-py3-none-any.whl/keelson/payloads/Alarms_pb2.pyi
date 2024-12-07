from google.protobuf import timestamp_pb2 as _timestamp_pb2
import Image_pb2 as _Image_pb2
import Audio_pb2 as _Audio_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Alarms(_message.Message):
    __slots__ = ("timestamp", "alarms")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ALARMS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    alarms: _containers.RepeatedCompositeFieldContainer[Alarm]
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., alarms: _Optional[_Iterable[_Union[Alarm, _Mapping]]] = ...) -> None: ...

class Alarm(_message.Message):
    __slots__ = ("timestamp", "source_entity", "source_id", "identifier", "description", "category", "priority", "acknowledgers", "audio", "visual", "activation_time_utc", "expiration_time_utc", "duration_seconds", "ack_scheme", "severity", "acknowledged")
    class Category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CATEGORY_UNSPECIFIED: _ClassVar[Alarm.Category]
        CATEGORY_SAFETY: _ClassVar[Alarm.Category]
        CATEGORY_NAVIGATION: _ClassVar[Alarm.Category]
        CATEGORY_TECHNICAL: _ClassVar[Alarm.Category]
        CATEGORY_FIRE_ALARM: _ClassVar[Alarm.Category]
    CATEGORY_UNSPECIFIED: Alarm.Category
    CATEGORY_SAFETY: Alarm.Category
    CATEGORY_NAVIGATION: Alarm.Category
    CATEGORY_TECHNICAL: Alarm.Category
    CATEGORY_FIRE_ALARM: Alarm.Category
    class Priority(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRIORITY_UNSPECIFIED: _ClassVar[Alarm.Priority]
        PRIORITY_NORMAL: _ClassVar[Alarm.Priority]
        PRIORITY_CAUTION: _ClassVar[Alarm.Priority]
        PRIORITY_WARNING: _ClassVar[Alarm.Priority]
        PRIORITY_EMERGENCY: _ClassVar[Alarm.Priority]
    PRIORITY_UNSPECIFIED: Alarm.Priority
    PRIORITY_NORMAL: Alarm.Priority
    PRIORITY_CAUTION: Alarm.Priority
    PRIORITY_WARNING: Alarm.Priority
    PRIORITY_EMERGENCY: Alarm.Priority
    class AckScheme(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_UNSPECIFIED: _ClassVar[Alarm.AckScheme]
        ACK_IMMEDIATELY: _ClassVar[Alarm.AckScheme]
        ACK_AUTO: _ClassVar[Alarm.AckScheme]
        ACK_NONE: _ClassVar[Alarm.AckScheme]
    ACK_UNSPECIFIED: Alarm.AckScheme
    ACK_IMMEDIATELY: Alarm.AckScheme
    ACK_AUTO: Alarm.AckScheme
    ACK_NONE: Alarm.AckScheme
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SEVERITY_UNSPECIFIED: _ClassVar[Alarm.Severity]
        SEVERITY_LOW: _ClassVar[Alarm.Severity]
        SEVERITY_MEDIUM: _ClassVar[Alarm.Severity]
        SEVERITY_HIGH: _ClassVar[Alarm.Severity]
        SEVERITY_CRITICAL: _ClassVar[Alarm.Severity]
    SEVERITY_UNSPECIFIED: Alarm.Severity
    SEVERITY_LOW: Alarm.Severity
    SEVERITY_MEDIUM: Alarm.Severity
    SEVERITY_HIGH: Alarm.Severity
    SEVERITY_CRITICAL: Alarm.Severity
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGERS_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    VISUAL_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_TIME_UTC_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    ACK_SCHEME_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGED_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    source_entity: str
    source_id: str
    identifier: str
    description: str
    category: Alarm.Category
    priority: Alarm.Priority
    acknowledgers: _containers.RepeatedCompositeFieldContainer[AlarmAcknowledgment]
    audio: _Audio_pb2.Audio
    visual: Visual
    activation_time_utc: _timestamp_pb2.Timestamp
    expiration_time_utc: _timestamp_pb2.Timestamp
    duration_seconds: int
    ack_scheme: Alarm.AckScheme
    severity: Alarm.Severity
    acknowledged: bool
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., source_entity: _Optional[str] = ..., source_id: _Optional[str] = ..., identifier: _Optional[str] = ..., description: _Optional[str] = ..., category: _Optional[_Union[Alarm.Category, str]] = ..., priority: _Optional[_Union[Alarm.Priority, str]] = ..., acknowledgers: _Optional[_Iterable[_Union[AlarmAcknowledgment, _Mapping]]] = ..., audio: _Optional[_Union[_Audio_pb2.Audio, _Mapping]] = ..., visual: _Optional[_Union[Visual, _Mapping]] = ..., activation_time_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expiration_time_utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., duration_seconds: _Optional[int] = ..., ack_scheme: _Optional[_Union[Alarm.AckScheme, str]] = ..., severity: _Optional[_Union[Alarm.Severity, str]] = ..., acknowledged: bool = ...) -> None: ...

class AlarmAcknowledgment(_message.Message):
    __slots__ = ("timestamp_acknowledged", "acknowledged_by")
    TIMESTAMP_ACKNOWLEDGED_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGED_BY_FIELD_NUMBER: _ClassVar[int]
    timestamp_acknowledged: _timestamp_pb2.Timestamp
    acknowledged_by: str
    def __init__(self, timestamp_acknowledged: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., acknowledged_by: _Optional[str] = ...) -> None: ...

class Visual(_message.Message):
    __slots__ = ("timestamp", "description", "image", "compressed_image", "compressed_video")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_IMAGE_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_VIDEO_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    description: str
    image: _Image_pb2.ImageRaw
    compressed_image: _Image_pb2.ImageCompressed
    compressed_video: _Image_pb2.VideoCompressed
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., image: _Optional[_Union[_Image_pb2.ImageRaw, _Mapping]] = ..., compressed_image: _Optional[_Union[_Image_pb2.ImageCompressed, _Mapping]] = ..., compressed_video: _Optional[_Union[_Image_pb2.VideoCompressed, _Mapping]] = ...) -> None: ...
