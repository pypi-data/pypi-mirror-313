from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VoyagePlan(_message.Message):
    __slots__ = ("timestamp_source", "timestamp_updated", "id", "name", "created_by", "to", "time_of_arrival_departure", "routes")
    TIMESTAMP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_UPDATED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_ARRIVAL_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    timestamp_source: _timestamp_pb2.Timestamp
    timestamp_updated: _timestamp_pb2.Timestamp
    id: str
    name: str
    created_by: str
    to: str
    time_of_arrival_departure: TimeOfDepartureArrival
    routes: _containers.RepeatedCompositeFieldContainer[VoyageRoute]
    def __init__(self, timestamp_source: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., timestamp_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., created_by: _Optional[str] = ..., to: _Optional[str] = ..., time_of_arrival_departure: _Optional[_Union[TimeOfDepartureArrival, _Mapping]] = ..., routes: _Optional[_Iterable[_Union[VoyageRoute, _Mapping]]] = ..., **kwargs) -> None: ...

class VoyageRoute(_message.Message):
    __slots__ = ("id", "name", "description", "distance", "duration", "duration_seconds", "speed_avg_knots", "time_of_arrival_departure", "waypoints")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SPEED_AVG_KNOTS_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_ARRIVAL_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    distance: float
    duration: _timestamp_pb2.Timestamp
    duration_seconds: int
    speed_avg_knots: float
    time_of_arrival_departure: TimeOfDepartureArrival
    waypoints: _containers.RepeatedCompositeFieldContainer[VoyageWaypoint]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., distance: _Optional[float] = ..., duration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., duration_seconds: _Optional[int] = ..., speed_avg_knots: _Optional[float] = ..., time_of_arrival_departure: _Optional[_Union[TimeOfDepartureArrival, _Mapping]] = ..., waypoints: _Optional[_Iterable[_Union[VoyageWaypoint, _Mapping]]] = ...) -> None: ...

class VoyageWaypoint(_message.Message):
    __slots__ = ("id", "name", "latitude", "longitude", "altitude", "speed", "heading", "time_of_arrival_departure")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_ARRIVAL_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    latitude: float
    longitude: float
    altitude: float
    speed: float
    heading: float
    time_of_arrival_departure: TimeOfDepartureArrival
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., speed: _Optional[float] = ..., heading: _Optional[float] = ..., time_of_arrival_departure: _Optional[_Union[TimeOfDepartureArrival, _Mapping]] = ...) -> None: ...

class TimeOfDepartureArrival(_message.Message):
    __slots__ = ("arrival_time_actual", "arrival_time_planed", "departure_time_actual", "departure_time_planed")
    ARRIVAL_TIME_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    ARRIVAL_TIME_PLANED_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_TIME_ACTUAL_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_TIME_PLANED_FIELD_NUMBER: _ClassVar[int]
    arrival_time_actual: _timestamp_pb2.Timestamp
    arrival_time_planed: _timestamp_pb2.Timestamp
    departure_time_actual: _timestamp_pb2.Timestamp
    departure_time_planed: _timestamp_pb2.Timestamp
    def __init__(self, arrival_time_actual: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., arrival_time_planed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., departure_time_actual: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., departure_time_planed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
