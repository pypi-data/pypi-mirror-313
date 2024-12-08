from google.protobuf import timestamp_pb2 as _timestamp_pb2
import LocationFix_pb2 as _LocationFix_pb2
import Pose_pb2 as _Pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigurationSensorPlatform(_message.Message):
    __slots__ = ("timestamp", "name", "type", "description", "devices", "communication", "fallback_strategy", "power")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    COMMUNICATION_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    name: str
    type: str
    description: str
    devices: _containers.RepeatedCompositeFieldContainer[Device]
    communication: Communication
    fallback_strategy: FallbackStrategy
    power: Power
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., description: _Optional[str] = ..., devices: _Optional[_Iterable[_Union[Device, _Mapping]]] = ..., communication: _Optional[_Union[Communication, _Mapping]] = ..., fallback_strategy: _Optional[_Union[FallbackStrategy, _Mapping]] = ..., power: _Optional[_Union[Power, _Mapping]] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("id", "name", "type", "location", "orientation", "description", "device_type")
    class DeviceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[Device.DeviceType]
        CAMERA: _ClassVar[Device.DeviceType]
        LIDAR: _ClassVar[Device.DeviceType]
        RADAR_MARINE: _ClassVar[Device.DeviceType]
        RADAR_VEHICLE: _ClassVar[Device.DeviceType]
        GNSS: _ClassVar[Device.DeviceType]
        IMU: _ClassVar[Device.DeviceType]
        SONAR: _ClassVar[Device.DeviceType]
        ACOUSTIC: _ClassVar[Device.DeviceType]
        THERMAL: _ClassVar[Device.DeviceType]
        OPTICAL: _ClassVar[Device.DeviceType]
        HYDROPHONE: _ClassVar[Device.DeviceType]
        MICROPHONE: _ClassVar[Device.DeviceType]
        PRESSURE: _ClassVar[Device.DeviceType]
        TEMPERATURE: _ClassVar[Device.DeviceType]
        HUMIDITY: _ClassVar[Device.DeviceType]
        WIND: _ClassVar[Device.DeviceType]
        CURRENT: _ClassVar[Device.DeviceType]
        VOLTAGE: _ClassVar[Device.DeviceType]
    UNKNOWN: Device.DeviceType
    CAMERA: Device.DeviceType
    LIDAR: Device.DeviceType
    RADAR_MARINE: Device.DeviceType
    RADAR_VEHICLE: Device.DeviceType
    GNSS: Device.DeviceType
    IMU: Device.DeviceType
    SONAR: Device.DeviceType
    ACOUSTIC: Device.DeviceType
    THERMAL: Device.DeviceType
    OPTICAL: Device.DeviceType
    HYDROPHONE: Device.DeviceType
    MICROPHONE: Device.DeviceType
    PRESSURE: Device.DeviceType
    TEMPERATURE: Device.DeviceType
    HUMIDITY: Device.DeviceType
    WIND: Device.DeviceType
    CURRENT: Device.DeviceType
    VOLTAGE: Device.DeviceType
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    location: Location
    orientation: Orientation
    description: str
    device_type: Device.DeviceType
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., location: _Optional[_Union[Location, _Mapping]] = ..., orientation: _Optional[_Union[Orientation, _Mapping]] = ..., description: _Optional[str] = ..., device_type: _Optional[_Union[Device.DeviceType, str]] = ...) -> None: ...

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

class Communication(_message.Message):
    __slots__ = ("primary_network", "backup_network", "description")
    PRIMARY_NETWORK_FIELD_NUMBER: _ClassVar[int]
    BACKUP_NETWORK_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    primary_network: str
    backup_network: str
    description: str
    def __init__(self, primary_network: _Optional[str] = ..., backup_network: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class FallbackStrategy(_message.Message):
    __slots__ = ("description", "strategies")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STRATEGIES_FIELD_NUMBER: _ClassVar[int]
    description: str
    strategies: _containers.RepeatedCompositeFieldContainer[FallbackScenario]
    def __init__(self, description: _Optional[str] = ..., strategies: _Optional[_Iterable[_Union[FallbackScenario, _Mapping]]] = ...) -> None: ...

class FallbackScenario(_message.Message):
    __slots__ = ("scenario", "response")
    SCENARIO_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    scenario: str
    response: str
    def __init__(self, scenario: _Optional[str] = ..., response: _Optional[str] = ...) -> None: ...

class Power(_message.Message):
    __slots__ = ("primary_source", "backup_source", "description")
    PRIMARY_SOURCE_FIELD_NUMBER: _ClassVar[int]
    BACKUP_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    primary_source: str
    backup_source: str
    description: str
    def __init__(self, primary_source: _Optional[str] = ..., backup_source: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class ConfigurationSensorPerception(_message.Message):
    __slots__ = ("timestamp", "location", "pose", "view_horizontal_angel_deg", "view_horizontal_start_angel_deg", "view_horizontal_end_angel_deg", "view_vertical_angel_deg", "mode", "mode_timestamp", "other_json")
    class SensorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[ConfigurationSensorPerception.SensorType]
        CAMERA: _ClassVar[ConfigurationSensorPerception.SensorType]
        LIDAR: _ClassVar[ConfigurationSensorPerception.SensorType]
        RADAR_MARINE: _ClassVar[ConfigurationSensorPerception.SensorType]
        RADAR_VEHICLE: _ClassVar[ConfigurationSensorPerception.SensorType]
    UNKNOWN: ConfigurationSensorPerception.SensorType
    CAMERA: ConfigurationSensorPerception.SensorType
    LIDAR: ConfigurationSensorPerception.SensorType
    RADAR_MARINE: ConfigurationSensorPerception.SensorType
    RADAR_VEHICLE: ConfigurationSensorPerception.SensorType
    class mode_operating(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RUNNING: _ClassVar[ConfigurationSensorPerception.mode_operating]
        STANDBY: _ClassVar[ConfigurationSensorPerception.mode_operating]
        DISABLED: _ClassVar[ConfigurationSensorPerception.mode_operating]
        OFF: _ClassVar[ConfigurationSensorPerception.mode_operating]
        ERROR: _ClassVar[ConfigurationSensorPerception.mode_operating]
    RUNNING: ConfigurationSensorPerception.mode_operating
    STANDBY: ConfigurationSensorPerception.mode_operating
    DISABLED: ConfigurationSensorPerception.mode_operating
    OFF: ConfigurationSensorPerception.mode_operating
    ERROR: ConfigurationSensorPerception.mode_operating
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    VIEW_HORIZONTAL_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    VIEW_HORIZONTAL_START_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    VIEW_HORIZONTAL_END_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    VIEW_VERTICAL_ANGEL_DEG_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OTHER_JSON_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    location: _LocationFix_pb2.LocationFix
    pose: _Pose_pb2.Pose
    view_horizontal_angel_deg: float
    view_horizontal_start_angel_deg: float
    view_horizontal_end_angel_deg: float
    view_vertical_angel_deg: float
    mode: str
    mode_timestamp: str
    other_json: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., location: _Optional[_Union[_LocationFix_pb2.LocationFix, _Mapping]] = ..., pose: _Optional[_Union[_Pose_pb2.Pose, _Mapping]] = ..., view_horizontal_angel_deg: _Optional[float] = ..., view_horizontal_start_angel_deg: _Optional[float] = ..., view_horizontal_end_angel_deg: _Optional[float] = ..., view_vertical_angel_deg: _Optional[float] = ..., mode: _Optional[str] = ..., mode_timestamp: _Optional[str] = ..., other_json: _Optional[str] = ...) -> None: ...
