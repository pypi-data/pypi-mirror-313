from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LocationFix(_message.Message):
    __slots__ = ("timestamp_source", "timestamp", "frame_id", "latitude", "longitude", "altitude", "position_covariance", "position_covariance_type")
    class PositionCovarianceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[LocationFix.PositionCovarianceType]
        APPROXIMATED: _ClassVar[LocationFix.PositionCovarianceType]
        DIAGONAL_KNOWN: _ClassVar[LocationFix.PositionCovarianceType]
        KNOWN: _ClassVar[LocationFix.PositionCovarianceType]
    UNKNOWN: LocationFix.PositionCovarianceType
    APPROXIMATED: LocationFix.PositionCovarianceType
    DIAGONAL_KNOWN: LocationFix.PositionCovarianceType
    KNOWN: LocationFix.PositionCovarianceType
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    timestamp: _timestamp_pb2.Timestamp
    frame_id: str
    latitude: float
    longitude: float
    altitude: float
    position_covariance: _containers.RepeatedScalarFieldContainer[float]
    position_covariance_type: LocationFix.PositionCovarianceType
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., frame_id: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., position_covariance: _Optional[_Iterable[float]] = ..., position_covariance_type: _Optional[_Union[LocationFix.PositionCovarianceType, str]] = ...) -> None: ...

class PositionFix(_message.Message):
    __slots__ = ("timestamp_source", "latitude_degree", "longitude_degree", "altitude_meters", "horizontal_accuracy_meters", "vertical_accuracy_meters", "geodetic_datum", "source")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_DEGREE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_DEGREE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_METERS_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_ACCURACY_METERS_FIELD_NUMBER: _ClassVar[int]
    VERTICAL_ACCURACY_METERS_FIELD_NUMBER: _ClassVar[int]
    GEODETIC_DATUM_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    latitude_degree: float
    longitude_degree: float
    altitude_meters: float
    horizontal_accuracy_meters: float
    vertical_accuracy_meters: float
    geodetic_datum: str
    source: PositionSource
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., latitude_degree: _Optional[float] = ..., longitude_degree: _Optional[float] = ..., altitude_meters: _Optional[float] = ..., horizontal_accuracy_meters: _Optional[float] = ..., vertical_accuracy_meters: _Optional[float] = ..., geodetic_datum: _Optional[str] = ..., source: _Optional[_Union[PositionSource, _Mapping]] = ...) -> None: ...

class PositionSource(_message.Message):
    __slots__ = ("source", "quality")
    class Source(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[PositionSource.Source]
        GPS: _ClassVar[PositionSource.Source]
        GLONASS: _ClassVar[PositionSource.Source]
        GALILEO: _ClassVar[PositionSource.Source]
        BEIDOU: _ClassVar[PositionSource.Source]
        SBAS: _ClassVar[PositionSource.Source]
        QZSS: _ClassVar[PositionSource.Source]
        IRNSS: _ClassVar[PositionSource.Source]
        NAVIC: _ClassVar[PositionSource.Source]
        OTHER: _ClassVar[PositionSource.Source]
    UNKNOWN: PositionSource.Source
    GPS: PositionSource.Source
    GLONASS: PositionSource.Source
    GALILEO: PositionSource.Source
    BEIDOU: PositionSource.Source
    SBAS: PositionSource.Source
    QZSS: PositionSource.Source
    IRNSS: PositionSource.Source
    NAVIC: PositionSource.Source
    OTHER: PositionSource.Source
    class Quality(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NO_FIX: _ClassVar[PositionSource.Quality]
        GPS_FIX: _ClassVar[PositionSource.Quality]
        DIFFERENTIAL_GPS_FIX: _ClassVar[PositionSource.Quality]
        PPS_FIX: _ClassVar[PositionSource.Quality]
        RTK: _ClassVar[PositionSource.Quality]
        FLOAT_RTK: _ClassVar[PositionSource.Quality]
        ESTIMATED: _ClassVar[PositionSource.Quality]
        MANUAL: _ClassVar[PositionSource.Quality]
        SIMULATION: _ClassVar[PositionSource.Quality]
        NOT_AVAILABLE: _ClassVar[PositionSource.Quality]
    NO_FIX: PositionSource.Quality
    GPS_FIX: PositionSource.Quality
    DIFFERENTIAL_GPS_FIX: PositionSource.Quality
    PPS_FIX: PositionSource.Quality
    RTK: PositionSource.Quality
    FLOAT_RTK: PositionSource.Quality
    ESTIMATED: PositionSource.Quality
    MANUAL: PositionSource.Quality
    SIMULATION: PositionSource.Quality
    NOT_AVAILABLE: PositionSource.Quality
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    source: PositionSource.Source
    quality: PositionSource.Quality
    def __init__(self, source: _Optional[_Union[PositionSource.Source, str]] = ..., quality: _Optional[_Union[PositionSource.Quality, str]] = ...) -> None: ...
