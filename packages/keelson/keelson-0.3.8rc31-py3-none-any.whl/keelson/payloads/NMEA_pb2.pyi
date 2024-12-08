from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GNGNS(_message.Message):
    __slots__ = ("timestamp", "utc", "latitude", "longitude", "mode_indicator", "satellites_used", "hdop", "altitude", "geoid_height")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UTC_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    MODE_INDICATOR_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    GEOID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    utc: _timestamp_pb2.Timestamp
    latitude: float
    longitude: float
    mode_indicator: str
    satellites_used: int
    hdop: float
    altitude: float
    geoid_height: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., mode_indicator: _Optional[str] = ..., satellites_used: _Optional[int] = ..., hdop: _Optional[float] = ..., altitude: _Optional[float] = ..., geoid_height: _Optional[float] = ...) -> None: ...

class GNGGA(_message.Message):
    __slots__ = ("timestamp", "utc", "latitude", "longitude", "gps_quality", "satellites_used", "hdop", "altitude", "height_of_geoid", "geoid_height", "time_since_last_dgps_update", "dgps_station_id", "reference_station_id")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UTC_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    GPS_QUALITY_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_USED_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_OF_GEOID_FIELD_NUMBER: _ClassVar[int]
    GEOID_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_SINCE_LAST_DGPS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    DGPS_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    utc: _timestamp_pb2.Timestamp
    latitude: float
    longitude: float
    gps_quality: int
    satellites_used: int
    hdop: float
    altitude: float
    height_of_geoid: float
    geoid_height: float
    time_since_last_dgps_update: float
    dgps_station_id: int
    reference_station_id: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., utc: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., gps_quality: _Optional[int] = ..., satellites_used: _Optional[int] = ..., hdop: _Optional[float] = ..., altitude: _Optional[float] = ..., height_of_geoid: _Optional[float] = ..., geoid_height: _Optional[float] = ..., time_since_last_dgps_update: _Optional[float] = ..., dgps_station_id: _Optional[int] = ..., reference_station_id: _Optional[int] = ...) -> None: ...
