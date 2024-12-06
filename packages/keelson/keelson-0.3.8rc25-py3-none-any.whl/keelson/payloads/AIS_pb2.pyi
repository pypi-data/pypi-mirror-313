from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AISVesselMessage(_message.Message):
    __slots__ = ("timestamp", "ais_vessel")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AIS_VESSEL_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    ais_vessel: AISVessel
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ais_vessel: _Optional[_Union[AISVessel, _Mapping]] = ...) -> None: ...

class AISVessel(_message.Message):
    __slots__ = ("timestamp", "mmsi", "class_a", "statics_valid", "sog_knots", "position_accuracy", "latitude_degree", "longitude_degree", "cog_degree", "true_heading_degree", "statics", "position_class_a", "statics_class_a")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MMSI_FIELD_NUMBER: _ClassVar[int]
    CLASS_A_FIELD_NUMBER: _ClassVar[int]
    STATICS_VALID_FIELD_NUMBER: _ClassVar[int]
    SOG_KNOTS_FIELD_NUMBER: _ClassVar[int]
    POSITION_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_DEGREE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_DEGREE_FIELD_NUMBER: _ClassVar[int]
    COG_DEGREE_FIELD_NUMBER: _ClassVar[int]
    TRUE_HEADING_DEGREE_FIELD_NUMBER: _ClassVar[int]
    STATICS_FIELD_NUMBER: _ClassVar[int]
    POSITION_CLASS_A_FIELD_NUMBER: _ClassVar[int]
    STATICS_CLASS_A_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    mmsi: int
    class_a: bool
    statics_valid: bool
    sog_knots: float
    position_accuracy: int
    latitude_degree: float
    longitude_degree: float
    cog_degree: float
    true_heading_degree: int
    statics: AISVesselStatics
    position_class_a: AISVesselPositionClassA
    statics_class_a: AISVesselStaticsClassA
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., mmsi: _Optional[int] = ..., class_a: bool = ..., statics_valid: bool = ..., sog_knots: _Optional[float] = ..., position_accuracy: _Optional[int] = ..., latitude_degree: _Optional[float] = ..., longitude_degree: _Optional[float] = ..., cog_degree: _Optional[float] = ..., true_heading_degree: _Optional[int] = ..., statics: _Optional[_Union[AISVesselStatics, _Mapping]] = ..., position_class_a: _Optional[_Union[AISVesselPositionClassA, _Mapping]] = ..., statics_class_a: _Optional[_Union[AISVesselStaticsClassA, _Mapping]] = ...) -> None: ...

class AISVesselStatics(_message.Message):
    __slots__ = ("timestamp", "callsign", "name", "type_and_cargo", "dim_a_meters", "dim_b_meters", "dim_c_meters", "dim_d_meters")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_AND_CARGO_FIELD_NUMBER: _ClassVar[int]
    DIM_A_METERS_FIELD_NUMBER: _ClassVar[int]
    DIM_B_METERS_FIELD_NUMBER: _ClassVar[int]
    DIM_C_METERS_FIELD_NUMBER: _ClassVar[int]
    DIM_D_METERS_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    callsign: str
    name: str
    type_and_cargo: int
    dim_a_meters: int
    dim_b_meters: int
    dim_c_meters: int
    dim_d_meters: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., callsign: _Optional[str] = ..., name: _Optional[str] = ..., type_and_cargo: _Optional[int] = ..., dim_a_meters: _Optional[int] = ..., dim_b_meters: _Optional[int] = ..., dim_c_meters: _Optional[int] = ..., dim_d_meters: _Optional[int] = ...) -> None: ...

class AISVesselStaticsClassA(_message.Message):
    __slots__ = ("timestamp", "ais_version", "imo", "fix_type", "eta_month", "eta_day", "eta_hour", "eta_minute", "draught_meter", "destination")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AIS_VERSION_FIELD_NUMBER: _ClassVar[int]
    IMO_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    ETA_MONTH_FIELD_NUMBER: _ClassVar[int]
    ETA_DAY_FIELD_NUMBER: _ClassVar[int]
    ETA_HOUR_FIELD_NUMBER: _ClassVar[int]
    ETA_MINUTE_FIELD_NUMBER: _ClassVar[int]
    DRAUGHT_METER_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    ais_version: int
    imo: int
    fix_type: int
    eta_month: int
    eta_day: int
    eta_hour: int
    eta_minute: int
    draught_meter: float
    destination: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., ais_version: _Optional[int] = ..., imo: _Optional[int] = ..., fix_type: _Optional[int] = ..., eta_month: _Optional[int] = ..., eta_day: _Optional[int] = ..., eta_hour: _Optional[int] = ..., eta_minute: _Optional[int] = ..., draught_meter: _Optional[float] = ..., destination: _Optional[str] = ...) -> None: ...

class AISVesselPositionClassA(_message.Message):
    __slots__ = ("timestamp", "nav_status", "rot_over_range", "rot_raw", "rot", "special_manoeuvre")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NAV_STATUS_FIELD_NUMBER: _ClassVar[int]
    ROT_OVER_RANGE_FIELD_NUMBER: _ClassVar[int]
    ROT_RAW_FIELD_NUMBER: _ClassVar[int]
    ROT_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_MANOEUVRE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    nav_status: int
    rot_over_range: bool
    rot_raw: int
    rot: float
    special_manoeuvre: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., nav_status: _Optional[int] = ..., rot_over_range: bool = ..., rot_raw: _Optional[int] = ..., rot: _Optional[float] = ..., special_manoeuvre: _Optional[int] = ...) -> None: ...
