from google.protobuf import timestamp_pb2 as _timestamp_pb2
import LocationFix_pb2 as _LocationFix_pb2
import VoyagePlan_pb2 as _VoyagePlan_pb2
import Navigation_pb2 as _Navigation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vessels(_message.Message):
    __slots__ = ("timestamp_source", "vessels")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    VESSELS_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    vessels: _containers.RepeatedCompositeFieldContainer[Vessel]
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., vessels: _Optional[_Iterable[_Union[Vessel, _Mapping]]] = ...) -> None: ...

class Vessel(_message.Message):
    __slots__ = ("timestamp_source", "information", "position", "location", "speed_through_water", "speed_over_ground", "rate_of_turn", "heading", "navigation_status", "common_reference_point", "data_source", "voyage", "statics")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    INFORMATION_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    SPEED_THROUGH_WATER_FIELD_NUMBER: _ClassVar[int]
    SPEED_OVER_GROUND_FIELD_NUMBER: _ClassVar[int]
    RATE_OF_TURN_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_STATUS_FIELD_NUMBER: _ClassVar[int]
    COMMON_REFERENCE_POINT_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    VOYAGE_FIELD_NUMBER: _ClassVar[int]
    STATICS_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    information: VesselInformation
    position: _LocationFix_pb2.PositionFix
    location: _LocationFix_pb2.LocationFix
    speed_through_water: _Navigation_pb2.SpeedThroughWater
    speed_over_ground: _Navigation_pb2.SpeedOverGround
    rate_of_turn: _Navigation_pb2.RateOfTurn
    heading: _Navigation_pb2.Heading
    navigation_status: _Navigation_pb2.NavigationStatus
    common_reference_point: _Navigation_pb2.CommonReferencePoint
    data_source: _containers.RepeatedCompositeFieldContainer[VesselDataSource]
    voyage: VesselVoyage
    statics: VesselStatics
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., information: _Optional[_Union[VesselInformation, _Mapping]] = ..., position: _Optional[_Union[_LocationFix_pb2.PositionFix, _Mapping]] = ..., location: _Optional[_Union[_LocationFix_pb2.LocationFix, _Mapping]] = ..., speed_through_water: _Optional[_Union[_Navigation_pb2.SpeedThroughWater, _Mapping]] = ..., speed_over_ground: _Optional[_Union[_Navigation_pb2.SpeedOverGround, _Mapping]] = ..., rate_of_turn: _Optional[_Union[_Navigation_pb2.RateOfTurn, _Mapping]] = ..., heading: _Optional[_Union[_Navigation_pb2.Heading, _Mapping]] = ..., navigation_status: _Optional[_Union[_Navigation_pb2.NavigationStatus, _Mapping]] = ..., common_reference_point: _Optional[_Union[_Navigation_pb2.CommonReferencePoint, _Mapping]] = ..., data_source: _Optional[_Iterable[_Union[VesselDataSource, _Mapping]]] = ..., voyage: _Optional[_Union[VesselVoyage, _Mapping]] = ..., statics: _Optional[_Union[VesselStatics, _Mapping]] = ...) -> None: ...

class VesselInformation(_message.Message):
    __slots__ = ("timestamp_source", "mmsi", "imo", "name", "call_sign", "length_over_all_meters", "width_over_all_meters", "draft_meters", "type", "json_str")
    class VesselType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[VesselInformation.VesselType]
        WIG: _ClassVar[VesselInformation.VesselType]
        FISHING: _ClassVar[VesselInformation.VesselType]
        TOWING: _ClassVar[VesselInformation.VesselType]
        TOWING_LONG: _ClassVar[VesselInformation.VesselType]
        DREDGING: _ClassVar[VesselInformation.VesselType]
        DIVING: _ClassVar[VesselInformation.VesselType]
        MILITARY: _ClassVar[VesselInformation.VesselType]
        SAILING: _ClassVar[VesselInformation.VesselType]
        PLEASURE: _ClassVar[VesselInformation.VesselType]
        HSC: _ClassVar[VesselInformation.VesselType]
        PILOT: _ClassVar[VesselInformation.VesselType]
        SAR: _ClassVar[VesselInformation.VesselType]
        TUG: _ClassVar[VesselInformation.VesselType]
        PORT: _ClassVar[VesselInformation.VesselType]
        ANTI_POLLUTION: _ClassVar[VesselInformation.VesselType]
        LAW_ENFORCEMENT: _ClassVar[VesselInformation.VesselType]
        MEDICAL: _ClassVar[VesselInformation.VesselType]
        PASSENGER: _ClassVar[VesselInformation.VesselType]
        CARGO: _ClassVar[VesselInformation.VesselType]
        TANKER: _ClassVar[VesselInformation.VesselType]
        OTHER: _ClassVar[VesselInformation.VesselType]
    UNKNOWN: VesselInformation.VesselType
    WIG: VesselInformation.VesselType
    FISHING: VesselInformation.VesselType
    TOWING: VesselInformation.VesselType
    TOWING_LONG: VesselInformation.VesselType
    DREDGING: VesselInformation.VesselType
    DIVING: VesselInformation.VesselType
    MILITARY: VesselInformation.VesselType
    SAILING: VesselInformation.VesselType
    PLEASURE: VesselInformation.VesselType
    HSC: VesselInformation.VesselType
    PILOT: VesselInformation.VesselType
    SAR: VesselInformation.VesselType
    TUG: VesselInformation.VesselType
    PORT: VesselInformation.VesselType
    ANTI_POLLUTION: VesselInformation.VesselType
    LAW_ENFORCEMENT: VesselInformation.VesselType
    MEDICAL: VesselInformation.VesselType
    PASSENGER: VesselInformation.VesselType
    CARGO: VesselInformation.VesselType
    TANKER: VesselInformation.VesselType
    OTHER: VesselInformation.VesselType
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    MMSI_FIELD_NUMBER: _ClassVar[int]
    IMO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CALL_SIGN_FIELD_NUMBER: _ClassVar[int]
    LENGTH_OVER_ALL_METERS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_OVER_ALL_METERS_FIELD_NUMBER: _ClassVar[int]
    DRAFT_METERS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    JSON_STR_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    mmsi: int
    imo: int
    name: str
    call_sign: str
    length_over_all_meters: float
    width_over_all_meters: float
    draft_meters: float
    type: VesselInformation.VesselType
    json_str: str
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mmsi: _Optional[int] = ..., imo: _Optional[int] = ..., name: _Optional[str] = ..., call_sign: _Optional[str] = ..., length_over_all_meters: _Optional[float] = ..., width_over_all_meters: _Optional[float] = ..., draft_meters: _Optional[float] = ..., type: _Optional[_Union[VesselInformation.VesselType, str]] = ..., json_str: _Optional[str] = ...) -> None: ...

class VesselVoyage(_message.Message):
    __slots__ = ("timestamp_source", "departed_country_name", "departed_country_code", "departure_port_name", "departure_port_code", "destination_country_name", "destination_country_code", "destination_port_name", "destination_port_code", "time_to_go_seconds", "time_of_departure_arrival", "voyage_plan", "json_str")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DEPARTED_COUNTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPARTED_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_PORT_NAME_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_PORT_CODE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_COUNTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_PORT_NAME_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_PORT_CODE_FIELD_NUMBER: _ClassVar[int]
    TIME_TO_GO_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_DEPARTURE_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    VOYAGE_PLAN_FIELD_NUMBER: _ClassVar[int]
    JSON_STR_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    departed_country_name: str
    departed_country_code: str
    departure_port_name: str
    departure_port_code: str
    destination_country_name: str
    destination_country_code: str
    destination_port_name: str
    destination_port_code: str
    time_to_go_seconds: int
    time_of_departure_arrival: _VoyagePlan_pb2.TimeOfDepartureArrival
    voyage_plan: _VoyagePlan_pb2.VoyagePlan
    json_str: str
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., departed_country_name: _Optional[str] = ..., departed_country_code: _Optional[str] = ..., departure_port_name: _Optional[str] = ..., departure_port_code: _Optional[str] = ..., destination_country_name: _Optional[str] = ..., destination_country_code: _Optional[str] = ..., destination_port_name: _Optional[str] = ..., destination_port_code: _Optional[str] = ..., time_to_go_seconds: _Optional[int] = ..., time_of_departure_arrival: _Optional[_Union[_VoyagePlan_pb2.TimeOfDepartureArrival, _Mapping]] = ..., voyage_plan: _Optional[_Union[_VoyagePlan_pb2.VoyagePlan, _Mapping]] = ..., json_str: _Optional[str] = ...) -> None: ...

class VesselDataSource(_message.Message):
    __slots__ = ("source", "description", "name", "json_str")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AIS_RADIO_RECEIVER: _ClassVar[VesselDataSource.Source]
        AIS_PROVIDER: _ClassVar[VesselDataSource.Source]
        RADAR: _ClassVar[VesselDataSource.Source]
        LIDAR: _ClassVar[VesselDataSource.Source]
        CAMERA: _ClassVar[VesselDataSource.Source]
        SIMULATION: _ClassVar[VesselDataSource.Source]
        PLATFORM: _ClassVar[VesselDataSource.Source]
    AIS_RADIO_RECEIVER: VesselDataSource.Source
    AIS_PROVIDER: VesselDataSource.Source
    RADAR: VesselDataSource.Source
    LIDAR: VesselDataSource.Source
    CAMERA: VesselDataSource.Source
    SIMULATION: VesselDataSource.Source
    PLATFORM: VesselDataSource.Source
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    JSON_STR_FIELD_NUMBER: _ClassVar[int]
    source: VesselDataSource.Source
    description: str
    name: str
    json_str: str
    def __init__(self, source: _Optional[_Union[VesselDataSource.Source, str]] = ..., description: _Optional[str] = ..., name: _Optional[str] = ..., json_str: _Optional[str] = ...) -> None: ...

class VesselStatics(_message.Message):
    __slots__ = ("model", "rudder_count", "rudder_single_mode", "propulsion_count", "propulsion_type", "bow_thruster_count", "stern_thruster_count", "gps_count", "gyrocompass_count", "magnetic_compass_count")
    class PropulsionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED: _ClassVar[VesselStatics.PropulsionType]
        SINGLE: _ClassVar[VesselStatics.PropulsionType]
        DUAL: _ClassVar[VesselStatics.PropulsionType]
        DIESEL: _ClassVar[VesselStatics.PropulsionType]
        ELECTRIC: _ClassVar[VesselStatics.PropulsionType]
        HYBRID: _ClassVar[VesselStatics.PropulsionType]
    UNSPECIFIED: VesselStatics.PropulsionType
    SINGLE: VesselStatics.PropulsionType
    DUAL: VesselStatics.PropulsionType
    DIESEL: VesselStatics.PropulsionType
    ELECTRIC: VesselStatics.PropulsionType
    HYBRID: VesselStatics.PropulsionType
    MODEL_FIELD_NUMBER: _ClassVar[int]
    RUDDER_COUNT_FIELD_NUMBER: _ClassVar[int]
    RUDDER_SINGLE_MODE_FIELD_NUMBER: _ClassVar[int]
    PROPULSION_COUNT_FIELD_NUMBER: _ClassVar[int]
    PROPULSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    BOW_THRUSTER_COUNT_FIELD_NUMBER: _ClassVar[int]
    STERN_THRUSTER_COUNT_FIELD_NUMBER: _ClassVar[int]
    GPS_COUNT_FIELD_NUMBER: _ClassVar[int]
    GYROCOMPASS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAGNETIC_COMPASS_COUNT_FIELD_NUMBER: _ClassVar[int]
    model: str
    rudder_count: int
    rudder_single_mode: bool
    propulsion_count: int
    propulsion_type: VesselStatics.PropulsionType
    bow_thruster_count: int
    stern_thruster_count: int
    gps_count: int
    gyrocompass_count: int
    magnetic_compass_count: int
    def __init__(self, model: _Optional[str] = ..., rudder_count: _Optional[int] = ..., rudder_single_mode: bool = ..., propulsion_count: _Optional[int] = ..., propulsion_type: _Optional[_Union[VesselStatics.PropulsionType, str]] = ..., bow_thruster_count: _Optional[int] = ..., stern_thruster_count: _Optional[int] = ..., gps_count: _Optional[int] = ..., gyrocompass_count: _Optional[int] = ..., magnetic_compass_count: _Optional[int] = ...) -> None: ...

class Autopilot(_message.Message):
    __slots__ = ("autopilot_on", "control_mode", "course", "radius", "rot", "rudder_limit", "rudder_performance", "rudder_timing", "steering_mode")
    AUTOPILOT_ON_FIELD_NUMBER: _ClassVar[int]
    CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    ROT_FIELD_NUMBER: _ClassVar[int]
    RUDDER_LIMIT_FIELD_NUMBER: _ClassVar[int]
    RUDDER_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    RUDDER_TIMING_FIELD_NUMBER: _ClassVar[int]
    STEERING_MODE_FIELD_NUMBER: _ClassVar[int]
    autopilot_on: bool
    control_mode: str
    course: float
    radius: float
    rot: float
    rudder_limit: float
    rudder_performance: str
    rudder_timing: str
    steering_mode: str
    def __init__(self, autopilot_on: bool = ..., control_mode: _Optional[str] = ..., course: _Optional[float] = ..., radius: _Optional[float] = ..., rot: _Optional[float] = ..., rudder_limit: _Optional[float] = ..., rudder_performance: _Optional[str] = ..., rudder_timing: _Optional[str] = ..., steering_mode: _Optional[str] = ...) -> None: ...

class Orientation(_message.Message):
    __slots__ = ("roll", "pitch", "yaw", "reference_frame")
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    roll: float
    pitch: float
    yaw: float
    reference_frame: str
    def __init__(self, roll: _Optional[float] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., reference_frame: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("id", "name", "type", "location", "orientation", "description")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    location: Location
    orientation: Orientation
    description: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ..., orientation: _Optional[_Union[Orientation, _Mapping]] = ..., description: _Optional[str] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("x", "y", "z", "reference_frame")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    reference_frame: str
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., reference_frame: _Optional[str] = ...) -> None: ...

class LimitMinMax(_message.Message):
    __slots__ = ("min_value", "max_value", "min_safety_value", "max_safety_value")
    MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
    MIN_SAFETY_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAX_SAFETY_VALUE_FIELD_NUMBER: _ClassVar[int]
    min_value: float
    max_value: float
    min_safety_value: float
    max_safety_value: float
    def __init__(self, min_value: _Optional[float] = ..., max_value: _Optional[float] = ..., min_safety_value: _Optional[float] = ..., max_safety_value: _Optional[float] = ...) -> None: ...
