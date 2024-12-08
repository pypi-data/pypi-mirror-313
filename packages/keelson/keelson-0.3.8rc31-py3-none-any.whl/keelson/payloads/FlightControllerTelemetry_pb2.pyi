from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PowerStatus(_message.Message):
    __slots__ = ("Vcc", "Vservo", "flags")
    VCC_FIELD_NUMBER: _ClassVar[int]
    VSERVO_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    Vcc: int
    Vservo: int
    flags: int
    def __init__(self, Vcc: _Optional[int] = ..., Vservo: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...

class MemInfo(_message.Message):
    __slots__ = ("brkval", "freemem", "freemem32")
    BRKVAL_FIELD_NUMBER: _ClassVar[int]
    FREEMEM_FIELD_NUMBER: _ClassVar[int]
    FREEMEM32_FIELD_NUMBER: _ClassVar[int]
    brkval: int
    freemem: int
    freemem32: int
    def __init__(self, brkval: _Optional[int] = ..., freemem: _Optional[int] = ..., freemem32: _Optional[int] = ...) -> None: ...

class MissionCurrent(_message.Message):
    __slots__ = ("seq", "total", "mission_state", "mission_mode")
    SEQ_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    MISSION_STATE_FIELD_NUMBER: _ClassVar[int]
    MISSION_MODE_FIELD_NUMBER: _ClassVar[int]
    seq: int
    total: int
    mission_state: int
    mission_mode: int
    def __init__(self, seq: _Optional[int] = ..., total: _Optional[int] = ..., mission_state: _Optional[int] = ..., mission_mode: _Optional[int] = ...) -> None: ...

class ServoOutputRaw(_message.Message):
    __slots__ = ("time_usec", "port", "servo_raw")
    TIME_USEC_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SERVO_RAW_FIELD_NUMBER: _ClassVar[int]
    time_usec: int
    port: int
    servo_raw: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, time_usec: _Optional[int] = ..., port: _Optional[int] = ..., servo_raw: _Optional[_Iterable[int]] = ...) -> None: ...

class RCChannels(_message.Message):
    __slots__ = ("time_boot_ms", "chancount", "chan_raw", "rssi")
    TIME_BOOT_MS_FIELD_NUMBER: _ClassVar[int]
    CHANCOUNT_FIELD_NUMBER: _ClassVar[int]
    CHAN_RAW_FIELD_NUMBER: _ClassVar[int]
    RSSI_FIELD_NUMBER: _ClassVar[int]
    time_boot_ms: int
    chancount: int
    chan_raw: _containers.RepeatedScalarFieldContainer[int]
    rssi: int
    def __init__(self, time_boot_ms: _Optional[int] = ..., chancount: _Optional[int] = ..., chan_raw: _Optional[_Iterable[int]] = ..., rssi: _Optional[int] = ...) -> None: ...

class RawIMU(_message.Message):
    __slots__ = ("time_usec", "xacc", "yacc", "zacc", "xgyro", "ygyro", "zgyro", "xmag", "ymag", "zmag", "id", "temperature")
    TIME_USEC_FIELD_NUMBER: _ClassVar[int]
    XACC_FIELD_NUMBER: _ClassVar[int]
    YACC_FIELD_NUMBER: _ClassVar[int]
    ZACC_FIELD_NUMBER: _ClassVar[int]
    XGYRO_FIELD_NUMBER: _ClassVar[int]
    YGYRO_FIELD_NUMBER: _ClassVar[int]
    ZGYRO_FIELD_NUMBER: _ClassVar[int]
    XMAG_FIELD_NUMBER: _ClassVar[int]
    YMAG_FIELD_NUMBER: _ClassVar[int]
    ZMAG_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    time_usec: int
    xacc: int
    yacc: int
    zacc: int
    xgyro: int
    ygyro: int
    zgyro: int
    xmag: int
    ymag: int
    zmag: int
    id: int
    temperature: int
    def __init__(self, time_usec: _Optional[int] = ..., xacc: _Optional[int] = ..., yacc: _Optional[int] = ..., zacc: _Optional[int] = ..., xgyro: _Optional[int] = ..., ygyro: _Optional[int] = ..., zgyro: _Optional[int] = ..., xmag: _Optional[int] = ..., ymag: _Optional[int] = ..., zmag: _Optional[int] = ..., id: _Optional[int] = ..., temperature: _Optional[int] = ...) -> None: ...

class ScaledPressure(_message.Message):
    __slots__ = ("time_boot_ms", "press_abs", "press_diff", "temperature", "temperature_press_diff")
    TIME_BOOT_MS_FIELD_NUMBER: _ClassVar[int]
    PRESS_ABS_FIELD_NUMBER: _ClassVar[int]
    PRESS_DIFF_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_PRESS_DIFF_FIELD_NUMBER: _ClassVar[int]
    time_boot_ms: int
    press_abs: float
    press_diff: float
    temperature: int
    temperature_press_diff: float
    def __init__(self, time_boot_ms: _Optional[int] = ..., press_abs: _Optional[float] = ..., press_diff: _Optional[float] = ..., temperature: _Optional[int] = ..., temperature_press_diff: _Optional[float] = ...) -> None: ...

class GPSRawInt(_message.Message):
    __slots__ = ("time_usec", "fix_type", "lat", "lon", "alt", "eph", "epv", "vel", "cog", "satellites_visible", "alt_ellipsoid", "h_acc", "v_acc", "vel_acc", "hdg_acc", "yaw")
    TIME_USEC_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    EPH_FIELD_NUMBER: _ClassVar[int]
    EPV_FIELD_NUMBER: _ClassVar[int]
    VEL_FIELD_NUMBER: _ClassVar[int]
    COG_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    ALT_ELLIPSOID_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    VEL_ACC_FIELD_NUMBER: _ClassVar[int]
    HDG_ACC_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    time_usec: int
    fix_type: int
    lat: int
    lon: int
    alt: int
    eph: int
    epv: int
    vel: int
    cog: int
    satellites_visible: int
    alt_ellipsoid: int
    h_acc: int
    v_acc: int
    vel_acc: int
    hdg_acc: int
    yaw: int
    def __init__(self, time_usec: _Optional[int] = ..., fix_type: _Optional[int] = ..., lat: _Optional[int] = ..., lon: _Optional[int] = ..., alt: _Optional[int] = ..., eph: _Optional[int] = ..., epv: _Optional[int] = ..., vel: _Optional[int] = ..., cog: _Optional[int] = ..., satellites_visible: _Optional[int] = ..., alt_ellipsoid: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ..., vel_acc: _Optional[int] = ..., hdg_acc: _Optional[int] = ..., yaw: _Optional[int] = ...) -> None: ...

class SystemTime(_message.Message):
    __slots__ = ("time_unix_usec", "time_boot_ms")
    TIME_UNIX_USEC_FIELD_NUMBER: _ClassVar[int]
    TIME_BOOT_MS_FIELD_NUMBER: _ClassVar[int]
    time_unix_usec: int
    time_boot_ms: int
    def __init__(self, time_unix_usec: _Optional[int] = ..., time_boot_ms: _Optional[int] = ...) -> None: ...

class AHRS(_message.Message):
    __slots__ = ("omegaIx", "omegaIy", "omegaIz", "accel_weight", "renorm_val", "error_rp", "error_yaw")
    OMEGAIX_FIELD_NUMBER: _ClassVar[int]
    OMEGAIY_FIELD_NUMBER: _ClassVar[int]
    OMEGAIZ_FIELD_NUMBER: _ClassVar[int]
    ACCEL_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    RENORM_VAL_FIELD_NUMBER: _ClassVar[int]
    ERROR_RP_FIELD_NUMBER: _ClassVar[int]
    ERROR_YAW_FIELD_NUMBER: _ClassVar[int]
    omegaIx: float
    omegaIy: float
    omegaIz: float
    accel_weight: float
    renorm_val: float
    error_rp: float
    error_yaw: float
    def __init__(self, omegaIx: _Optional[float] = ..., omegaIy: _Optional[float] = ..., omegaIz: _Optional[float] = ..., accel_weight: _Optional[float] = ..., renorm_val: _Optional[float] = ..., error_rp: _Optional[float] = ..., error_yaw: _Optional[float] = ...) -> None: ...

class EKFStatusReport(_message.Message):
    __slots__ = ("flags", "velocity_variance", "pos_horiz_variance", "pos_vert_variance", "compass_variance", "terrain_alt_variance", "airspeed_variance")
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    POS_HORIZ_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    POS_VERT_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    COMPASS_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    TERRAIN_ALT_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    AIRSPEED_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    flags: int
    velocity_variance: float
    pos_horiz_variance: float
    pos_vert_variance: float
    compass_variance: float
    terrain_alt_variance: float
    airspeed_variance: float
    def __init__(self, flags: _Optional[int] = ..., velocity_variance: _Optional[float] = ..., pos_horiz_variance: _Optional[float] = ..., pos_vert_variance: _Optional[float] = ..., compass_variance: _Optional[float] = ..., terrain_alt_variance: _Optional[float] = ..., airspeed_variance: _Optional[float] = ...) -> None: ...

class Vibration(_message.Message):
    __slots__ = ("time_usec", "vibration_x", "vibration_y", "vibration_z", "clipping_0", "clipping_1", "clipping_2")
    TIME_USEC_FIELD_NUMBER: _ClassVar[int]
    VIBRATION_X_FIELD_NUMBER: _ClassVar[int]
    VIBRATION_Y_FIELD_NUMBER: _ClassVar[int]
    VIBRATION_Z_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_0_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_1_FIELD_NUMBER: _ClassVar[int]
    CLIPPING_2_FIELD_NUMBER: _ClassVar[int]
    time_usec: int
    vibration_x: float
    vibration_y: float
    vibration_z: float
    clipping_0: int
    clipping_1: int
    clipping_2: int
    def __init__(self, time_usec: _Optional[int] = ..., vibration_x: _Optional[float] = ..., vibration_y: _Optional[float] = ..., vibration_z: _Optional[float] = ..., clipping_0: _Optional[int] = ..., clipping_1: _Optional[int] = ..., clipping_2: _Optional[int] = ...) -> None: ...

class BatteryStatus(_message.Message):
    __slots__ = ("id", "battery_function", "type", "temperature", "voltages", "current_battery", "current_consumed", "energy_consumed", "battery_remaining", "time_remaining", "charge_state", "voltages_ext", "mode", "fault_bitmask")
    ID_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    VOLTAGES_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BATTERY_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    ENERGY_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    BATTERY_REMAINING_FIELD_NUMBER: _ClassVar[int]
    TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    CHARGE_STATE_FIELD_NUMBER: _ClassVar[int]
    VOLTAGES_EXT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FAULT_BITMASK_FIELD_NUMBER: _ClassVar[int]
    id: int
    battery_function: int
    type: int
    temperature: int
    voltages: _containers.RepeatedScalarFieldContainer[int]
    current_battery: int
    current_consumed: int
    energy_consumed: int
    battery_remaining: int
    time_remaining: int
    charge_state: int
    voltages_ext: _containers.RepeatedScalarFieldContainer[int]
    mode: int
    fault_bitmask: int
    def __init__(self, id: _Optional[int] = ..., battery_function: _Optional[int] = ..., type: _Optional[int] = ..., temperature: _Optional[int] = ..., voltages: _Optional[_Iterable[int]] = ..., current_battery: _Optional[int] = ..., current_consumed: _Optional[int] = ..., energy_consumed: _Optional[int] = ..., battery_remaining: _Optional[int] = ..., time_remaining: _Optional[int] = ..., charge_state: _Optional[int] = ..., voltages_ext: _Optional[_Iterable[int]] = ..., mode: _Optional[int] = ..., fault_bitmask: _Optional[int] = ...) -> None: ...

class RCChannelsScaled(_message.Message):
    __slots__ = ("time_boot_ms", "port", "chan_scaled", "rssi")
    TIME_BOOT_MS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    CHAN_SCALED_FIELD_NUMBER: _ClassVar[int]
    RSSI_FIELD_NUMBER: _ClassVar[int]
    time_boot_ms: int
    port: int
    chan_scaled: _containers.RepeatedScalarFieldContainer[int]
    rssi: int
    def __init__(self, time_boot_ms: _Optional[int] = ..., port: _Optional[int] = ..., chan_scaled: _Optional[_Iterable[int]] = ..., rssi: _Optional[int] = ...) -> None: ...

class Attitude(_message.Message):
    __slots__ = ("time_boot_ms", "roll", "pitch", "yaw", "rollspeed", "pitchspeed", "yawspeed")
    TIME_BOOT_MS_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    ROLLSPEED_FIELD_NUMBER: _ClassVar[int]
    PITCHSPEED_FIELD_NUMBER: _ClassVar[int]
    YAWSPEED_FIELD_NUMBER: _ClassVar[int]
    time_boot_ms: int
    roll: float
    pitch: float
    yaw: float
    rollspeed: float
    pitchspeed: float
    yawspeed: float
    def __init__(self, time_boot_ms: _Optional[int] = ..., roll: _Optional[float] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., rollspeed: _Optional[float] = ..., pitchspeed: _Optional[float] = ..., yawspeed: _Optional[float] = ...) -> None: ...

class VFRHUD(_message.Message):
    __slots__ = ("airspeed", "groundspeed", "heading", "throttle", "alt", "climb")
    AIRSPEED_FIELD_NUMBER: _ClassVar[int]
    GROUNDSPEED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    CLIMB_FIELD_NUMBER: _ClassVar[int]
    airspeed: float
    groundspeed: float
    heading: int
    throttle: int
    alt: float
    climb: float
    def __init__(self, airspeed: _Optional[float] = ..., groundspeed: _Optional[float] = ..., heading: _Optional[int] = ..., throttle: _Optional[int] = ..., alt: _Optional[float] = ..., climb: _Optional[float] = ...) -> None: ...

class AHRS2(_message.Message):
    __slots__ = ("roll", "pitch", "yaw", "altitude", "lat", "lng")
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LNG_FIELD_NUMBER: _ClassVar[int]
    roll: float
    pitch: float
    yaw: float
    altitude: float
    lat: int
    lng: int
    def __init__(self, roll: _Optional[float] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., altitude: _Optional[float] = ..., lat: _Optional[int] = ..., lng: _Optional[int] = ...) -> None: ...

class GlobalPositionInt(_message.Message):
    __slots__ = ("time_boot_ms", "lat", "lon", "alt", "relative_alt", "vx", "vy", "vz", "hdg")
    TIME_BOOT_MS_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_ALT_FIELD_NUMBER: _ClassVar[int]
    VX_FIELD_NUMBER: _ClassVar[int]
    VY_FIELD_NUMBER: _ClassVar[int]
    VZ_FIELD_NUMBER: _ClassVar[int]
    HDG_FIELD_NUMBER: _ClassVar[int]
    time_boot_ms: int
    lat: int
    lon: int
    alt: int
    relative_alt: int
    vx: int
    vy: int
    vz: int
    hdg: int
    def __init__(self, time_boot_ms: _Optional[int] = ..., lat: _Optional[int] = ..., lon: _Optional[int] = ..., alt: _Optional[int] = ..., relative_alt: _Optional[int] = ..., vx: _Optional[int] = ..., vy: _Optional[int] = ..., vz: _Optional[int] = ..., hdg: _Optional[int] = ...) -> None: ...

class SysStatus(_message.Message):
    __slots__ = ("onboard_control_sensors_present", "onboard_control_sensors_enabled", "onboard_control_sensors_health", "load", "voltage_battery", "current_battery", "battery_remaining", "drop_rate_comm", "errors_comm", "errors_count1", "errors_count2", "errors_count3", "errors_count4")
    ONBOARD_CONTROL_SENSORS_PRESENT_FIELD_NUMBER: _ClassVar[int]
    ONBOARD_CONTROL_SENSORS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ONBOARD_CONTROL_SENSORS_HEALTH_FIELD_NUMBER: _ClassVar[int]
    LOAD_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_BATTERY_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BATTERY_FIELD_NUMBER: _ClassVar[int]
    BATTERY_REMAINING_FIELD_NUMBER: _ClassVar[int]
    DROP_RATE_COMM_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COMM_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT1_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT2_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT3_FIELD_NUMBER: _ClassVar[int]
    ERRORS_COUNT4_FIELD_NUMBER: _ClassVar[int]
    onboard_control_sensors_present: int
    onboard_control_sensors_enabled: int
    onboard_control_sensors_health: int
    load: int
    voltage_battery: int
    current_battery: int
    battery_remaining: int
    drop_rate_comm: int
    errors_comm: int
    errors_count1: int
    errors_count2: int
    errors_count3: int
    errors_count4: int
    def __init__(self, onboard_control_sensors_present: _Optional[int] = ..., onboard_control_sensors_enabled: _Optional[int] = ..., onboard_control_sensors_health: _Optional[int] = ..., load: _Optional[int] = ..., voltage_battery: _Optional[int] = ..., current_battery: _Optional[int] = ..., battery_remaining: _Optional[int] = ..., drop_rate_comm: _Optional[int] = ..., errors_comm: _Optional[int] = ..., errors_count1: _Optional[int] = ..., errors_count2: _Optional[int] = ..., errors_count3: _Optional[int] = ..., errors_count4: _Optional[int] = ...) -> None: ...
