import Quaternion_pb2 as _Quaternion_pb2
import Vector_pb2 as _Vector_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FrameTransforms(_message.Message):
    __slots__ = ("transforms",)
    TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    transforms: _containers.RepeatedCompositeFieldContainer[FrameTransform]
    def __init__(self, transforms: _Optional[_Iterable[_Union[FrameTransform, _Mapping]]] = ...) -> None: ...

class FrameTransform(_message.Message):
    __slots__ = ("timestamp", "parent_frame_id", "child_frame_id", "translation", "rotation")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PARENT_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    CHILD_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    parent_frame_id: str
    child_frame_id: str
    translation: _Vector_pb2.Vector3
    rotation: _Quaternion_pb2.Quaternion
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., parent_frame_id: _Optional[str] = ..., child_frame_id: _Optional[str] = ..., translation: _Optional[_Union[_Vector_pb2.Vector3, _Mapping]] = ..., rotation: _Optional[_Union[_Quaternion_pb2.Quaternion, _Mapping]] = ...) -> None: ...
