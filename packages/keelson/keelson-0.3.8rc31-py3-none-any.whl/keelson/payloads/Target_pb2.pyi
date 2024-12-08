from google.protobuf import timestamp_pb2 as _timestamp_pb2
import LocationFix_pb2 as _LocationFix_pb2
import Vessel_pb2 as _Vessel_pb2
import Navigation_pb2 as _Navigation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Targets(_message.Message):
    __slots__ = ("timestamp_source", "targets")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    targets: _containers.RepeatedCompositeFieldContainer[Target]
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., targets: _Optional[_Iterable[_Union[Target, _Mapping]]] = ...) -> None: ...

class Target(_message.Message):
    __slots__ = ("timestamp_source", "identification", "position", "location", "speed_through_water", "speed_over_ground", "rate_of_turn", "heading", "collision_monitoring", "navigation_status", "data_source", "json_str")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    IDENTIFICATION_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    SPEED_THROUGH_WATER_FIELD_NUMBER: _ClassVar[int]
    SPEED_OVER_GROUND_FIELD_NUMBER: _ClassVar[int]
    RATE_OF_TURN_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    COLLISION_MONITORING_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    JSON_STR_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    identification: TargetIdentification
    position: _LocationFix_pb2.PositionFix
    location: _LocationFix_pb2.LocationFix
    speed_through_water: _Navigation_pb2.SpeedThroughWater
    speed_over_ground: _Navigation_pb2.SpeedOverGround
    rate_of_turn: _Navigation_pb2.RateOfTurn
    heading: _Navigation_pb2.Heading
    collision_monitoring: _Navigation_pb2.CollisionMonitoring
    navigation_status: _Navigation_pb2.NavigationStatus
    data_source: TargetDataSource
    json_str: str
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., identification: _Optional[_Union[TargetIdentification, _Mapping]] = ..., position: _Optional[_Union[_LocationFix_pb2.PositionFix, _Mapping]] = ..., location: _Optional[_Union[_LocationFix_pb2.LocationFix, _Mapping]] = ..., speed_through_water: _Optional[_Union[_Navigation_pb2.SpeedThroughWater, _Mapping]] = ..., speed_over_ground: _Optional[_Union[_Navigation_pb2.SpeedOverGround, _Mapping]] = ..., rate_of_turn: _Optional[_Union[_Navigation_pb2.RateOfTurn, _Mapping]] = ..., heading: _Optional[_Union[_Navigation_pb2.Heading, _Mapping]] = ..., collision_monitoring: _Optional[_Union[_Navigation_pb2.CollisionMonitoring, _Mapping]] = ..., navigation_status: _Optional[_Union[_Navigation_pb2.NavigationStatus, _Mapping]] = ..., data_source: _Optional[_Union[TargetDataSource, _Mapping]] = ..., json_str: _Optional[str] = ...) -> None: ...

class TargetIdentification(_message.Message):
    __slots__ = ("timestamp", "vessel_type", "vessel")
    class TargetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[TargetIdentification.TargetType]
        VESSEL: _ClassVar[TargetIdentification.TargetType]
        SEAMARK: _ClassVar[TargetIdentification.TargetType]
    UNKNOWN: TargetIdentification.TargetType
    VESSEL: TargetIdentification.TargetType
    SEAMARK: TargetIdentification.TargetType
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VESSEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    VESSEL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    vessel_type: TargetIdentification.TargetType
    vessel: _Vessel_pb2.Vessel
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., vessel_type: _Optional[_Union[TargetIdentification.TargetType, str]] = ..., vessel: _Optional[_Union[_Vessel_pb2.Vessel, _Mapping]] = ...) -> None: ...

class TargetDataSource(_message.Message):
    __slots__ = ("source",)
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AIS_RADIO: _ClassVar[TargetDataSource.Source]
        AIS_PROVIDER: _ClassVar[TargetDataSource.Source]
        RADAR_MARINE: _ClassVar[TargetDataSource.Source]
        RADAR_ROAD: _ClassVar[TargetDataSource.Source]
        LIDAR: _ClassVar[TargetDataSource.Source]
        CAMERA_RBG: _ClassVar[TargetDataSource.Source]
        CAMERA_MONO: _ClassVar[TargetDataSource.Source]
        CAMERA_IR: _ClassVar[TargetDataSource.Source]
        SIMULATION: _ClassVar[TargetDataSource.Source]
    AIS_RADIO: TargetDataSource.Source
    AIS_PROVIDER: TargetDataSource.Source
    RADAR_MARINE: TargetDataSource.Source
    RADAR_ROAD: TargetDataSource.Source
    LIDAR: TargetDataSource.Source
    CAMERA_RBG: TargetDataSource.Source
    CAMERA_MONO: TargetDataSource.Source
    CAMERA_IR: TargetDataSource.Source
    SIMULATION: TargetDataSource.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: _containers.RepeatedScalarFieldContainer[TargetDataSource.Source]
    def __init__(self, source: _Optional[_Iterable[_Union[TargetDataSource.Source, str]]] = ...) -> None: ...
