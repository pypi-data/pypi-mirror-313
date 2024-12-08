from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpeedThroughWater(_message.Message):
    __slots__ = ("timestamp_source", "speed_through_water_knots")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    SPEED_THROUGH_WATER_KNOTS_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    speed_through_water_knots: float
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., speed_through_water_knots: _Optional[float] = ...) -> None: ...

class SpeedOverGround(_message.Message):
    __slots__ = ("timestamp_source", "course_over_ground_degrees", "speed_over_ground_knots", "bow_speed_over_ground_knots", "stern_speed_over_ground_knots")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    COURSE_OVER_GROUND_DEGREES_FIELD_NUMBER: _ClassVar[int]
    SPEED_OVER_GROUND_KNOTS_FIELD_NUMBER: _ClassVar[int]
    BOW_SPEED_OVER_GROUND_KNOTS_FIELD_NUMBER: _ClassVar[int]
    STERN_SPEED_OVER_GROUND_KNOTS_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    course_over_ground_degrees: float
    speed_over_ground_knots: float
    bow_speed_over_ground_knots: float
    stern_speed_over_ground_knots: float
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., course_over_ground_degrees: _Optional[float] = ..., speed_over_ground_knots: _Optional[float] = ..., bow_speed_over_ground_knots: _Optional[float] = ..., stern_speed_over_ground_knots: _Optional[float] = ...) -> None: ...

class RateOfTurn(_message.Message):
    __slots__ = ("timestamp_source", "rate_of_turn_degrees_per_minute")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    RATE_OF_TURN_DEGREES_PER_MINUTE_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    rate_of_turn_degrees_per_minute: float
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rate_of_turn_degrees_per_minute: _Optional[float] = ...) -> None: ...

class Heading(_message.Message):
    __slots__ = ("timestamp_source", "heading_degrees")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    HEADING_DEGREES_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    heading_degrees: float
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., heading_degrees: _Optional[float] = ...) -> None: ...

class CommonReferencePoint(_message.Message):
    __slots__ = ("distance_to_bow_meters", "distance_to_stern_meters", "distance_to_port_meters", "distance_to_starboard_meters")
    DISTANCE_TO_BOW_METERS_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TO_STERN_METERS_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TO_PORT_METERS_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TO_STARBOARD_METERS_FIELD_NUMBER: _ClassVar[int]
    distance_to_bow_meters: float
    distance_to_stern_meters: float
    distance_to_port_meters: float
    distance_to_starboard_meters: float
    def __init__(self, distance_to_bow_meters: _Optional[float] = ..., distance_to_stern_meters: _Optional[float] = ..., distance_to_port_meters: _Optional[float] = ..., distance_to_starboard_meters: _Optional[float] = ...) -> None: ...

class Sonar(_message.Message):
    __slots__ = ("timestamp_source", "depth_meters", "temperature_celsius", "salinity_ppt", "speed_of_sound_meters_per_second", "speed_through_water", "speed_over_ground")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DEPTH_METERS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_CELSIUS_FIELD_NUMBER: _ClassVar[int]
    SALINITY_PPT_FIELD_NUMBER: _ClassVar[int]
    SPEED_OF_SOUND_METERS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    SPEED_THROUGH_WATER_FIELD_NUMBER: _ClassVar[int]
    SPEED_OVER_GROUND_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    depth_meters: float
    temperature_celsius: float
    salinity_ppt: float
    speed_of_sound_meters_per_second: float
    speed_through_water: SpeedThroughWater
    speed_over_ground: SpeedOverGround
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., depth_meters: _Optional[float] = ..., temperature_celsius: _Optional[float] = ..., salinity_ppt: _Optional[float] = ..., speed_of_sound_meters_per_second: _Optional[float] = ..., speed_through_water: _Optional[_Union[SpeedThroughWater, _Mapping]] = ..., speed_over_ground: _Optional[_Union[SpeedOverGround, _Mapping]] = ...) -> None: ...

class CollisionMonitoring(_message.Message):
    __slots__ = ("timestamp", "cpa_metres", "tcpa_seconds", "bcr_metres", "bct_seconds", "bearing_north_degrees", "distance_metres")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CPA_METRES_FIELD_NUMBER: _ClassVar[int]
    TCPA_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BCR_METRES_FIELD_NUMBER: _ClassVar[int]
    BCT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    BEARING_NORTH_DEGREES_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_METRES_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    cpa_metres: float
    tcpa_seconds: float
    bcr_metres: float
    bct_seconds: float
    bearing_north_degrees: float
    distance_metres: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., cpa_metres: _Optional[float] = ..., tcpa_seconds: _Optional[float] = ..., bcr_metres: _Optional[float] = ..., bct_seconds: _Optional[float] = ..., bearing_north_degrees: _Optional[float] = ..., distance_metres: _Optional[float] = ...) -> None: ...

class SteeringAngle(_message.Message):
    __slots__ = ("timestamp_source", "rudder_angle_degrees")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    RUDDER_ANGLE_DEGREES_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    rudder_angle_degrees: float
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., rudder_angle_degrees: _Optional[float] = ...) -> None: ...

class NavigationStatus(_message.Message):
    __slots__ = ("timestamp_source", "navigation_status")
    class NavigationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNDER_WAY: _ClassVar[NavigationStatus.NavigationStatus]
        AT_ANCHOR: _ClassVar[NavigationStatus.NavigationStatus]
        NOT_UNDER_COMMAND: _ClassVar[NavigationStatus.NavigationStatus]
        RESTRICTED_MANEUVERABILITY: _ClassVar[NavigationStatus.NavigationStatus]
        CONSTRAINED_BY_DRAUGHT: _ClassVar[NavigationStatus.NavigationStatus]
        MOORED: _ClassVar[NavigationStatus.NavigationStatus]
        AGROUND: _ClassVar[NavigationStatus.NavigationStatus]
        ENGAGED_IN_FISHING: _ClassVar[NavigationStatus.NavigationStatus]
        UNDER_WAY_SAILING: _ClassVar[NavigationStatus.NavigationStatus]
        FUTURE_HSC: _ClassVar[NavigationStatus.NavigationStatus]
        FUTURE_WIG: _ClassVar[NavigationStatus.NavigationStatus]
        TOWING_ASTERN: _ClassVar[NavigationStatus.NavigationStatus]
        PUSHING_AHEAD: _ClassVar[NavigationStatus.NavigationStatus]
        RESERVED_FUTURE_USE: _ClassVar[NavigationStatus.NavigationStatus]
        AIS_SART: _ClassVar[NavigationStatus.NavigationStatus]
        UNDEFINED: _ClassVar[NavigationStatus.NavigationStatus]
    UNDER_WAY: NavigationStatus.NavigationStatus
    AT_ANCHOR: NavigationStatus.NavigationStatus
    NOT_UNDER_COMMAND: NavigationStatus.NavigationStatus
    RESTRICTED_MANEUVERABILITY: NavigationStatus.NavigationStatus
    CONSTRAINED_BY_DRAUGHT: NavigationStatus.NavigationStatus
    MOORED: NavigationStatus.NavigationStatus
    AGROUND: NavigationStatus.NavigationStatus
    ENGAGED_IN_FISHING: NavigationStatus.NavigationStatus
    UNDER_WAY_SAILING: NavigationStatus.NavigationStatus
    FUTURE_HSC: NavigationStatus.NavigationStatus
    FUTURE_WIG: NavigationStatus.NavigationStatus
    TOWING_ASTERN: NavigationStatus.NavigationStatus
    PUSHING_AHEAD: NavigationStatus.NavigationStatus
    RESERVED_FUTURE_USE: NavigationStatus.NavigationStatus
    AIS_SART: NavigationStatus.NavigationStatus
    UNDEFINED: NavigationStatus.NavigationStatus
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    navigation_status: NavigationStatus.NavigationStatus
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., navigation_status: _Optional[_Union[NavigationStatus.NavigationStatus, str]] = ...) -> None: ...
