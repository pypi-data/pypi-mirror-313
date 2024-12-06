from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SailControlState(_message.Message):
    __slots__ = ("sheeting_mode", "coupled_steering_mode", "variable_thrust_mode", "variable_thrust_set_pct", "variable_thrust_actual_pct")
    SHEETING_MODE_FIELD_NUMBER: _ClassVar[int]
    COUPLED_STEERING_MODE_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_THRUST_MODE_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_THRUST_SET_PCT_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_THRUST_ACTUAL_PCT_FIELD_NUMBER: _ClassVar[int]
    sheeting_mode: int
    coupled_steering_mode: int
    variable_thrust_mode: int
    variable_thrust_set_pct: float
    variable_thrust_actual_pct: float
    def __init__(self, sheeting_mode: _Optional[int] = ..., coupled_steering_mode: _Optional[int] = ..., variable_thrust_mode: _Optional[int] = ..., variable_thrust_set_pct: _Optional[float] = ..., variable_thrust_actual_pct: _Optional[float] = ...) -> None: ...

class SailState(_message.Message):
    __slots__ = ("is_active_mode", "sheeting_angle_actual_deg", "boom_angle_actual_deg", "sheeting_angle_set_deg", "sheeting_angle_add_deg", "wind_apparent_speed_ms", "wind_apparent_angle_deg", "wind_true_speed_ms", "wind_true_angle_deg")
    IS_ACTIVE_MODE_FIELD_NUMBER: _ClassVar[int]
    SHEETING_ANGLE_ACTUAL_DEG_FIELD_NUMBER: _ClassVar[int]
    BOOM_ANGLE_ACTUAL_DEG_FIELD_NUMBER: _ClassVar[int]
    SHEETING_ANGLE_SET_DEG_FIELD_NUMBER: _ClassVar[int]
    SHEETING_ANGLE_ADD_DEG_FIELD_NUMBER: _ClassVar[int]
    WIND_APPARENT_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    WIND_APPARENT_ANGLE_DEG_FIELD_NUMBER: _ClassVar[int]
    WIND_TRUE_SPEED_MS_FIELD_NUMBER: _ClassVar[int]
    WIND_TRUE_ANGLE_DEG_FIELD_NUMBER: _ClassVar[int]
    is_active_mode: int
    sheeting_angle_actual_deg: float
    boom_angle_actual_deg: float
    sheeting_angle_set_deg: float
    sheeting_angle_add_deg: float
    wind_apparent_speed_ms: float
    wind_apparent_angle_deg: float
    wind_true_speed_ms: float
    wind_true_angle_deg: float
    def __init__(self, is_active_mode: _Optional[int] = ..., sheeting_angle_actual_deg: _Optional[float] = ..., boom_angle_actual_deg: _Optional[float] = ..., sheeting_angle_set_deg: _Optional[float] = ..., sheeting_angle_add_deg: _Optional[float] = ..., wind_apparent_speed_ms: _Optional[float] = ..., wind_apparent_angle_deg: _Optional[float] = ..., wind_true_speed_ms: _Optional[float] = ..., wind_true_angle_deg: _Optional[float] = ...) -> None: ...
