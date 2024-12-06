from enum import Enum, auto
from typing import Optional
from typing import List
from pydantic import BaseModel

# CONSTANTS
DEFAULT_HLC_HEARTBEAT_TOLERANCE = 2000
JOINT_CONTROL_WORD_CST_POS_VEL_DISABLE_BIT = 1

# ENUMS
class FAULT_CAUSE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    FAULT_CAUSE_SAFETY_BIT_NUM                           =  (0),
    FAULT_CAUSE_DRIVE_FAULT_BIT_NUM                     =  (1),
    FAULT_CAUSE_GBC_FAULT_REQUEST_BIT_NUM               =  (2),
    FAULT_CAUSE_HEARTBEAT_LOST_BIT_NUM                  =  (3),
    FAULT_CAUSE_LIMIT_REACHED_BIT_NUM                   =  (4),
    FAULT_CAUSE_DRIVE_STATE_CHANGE_TIMEOUT_BIT_NUM      =  (5),
    FAULT_CAUSE_DRIVE_FOLLOW_ERROR_BIT_NUM              =  (6),
    FAULT_CAUSE_DRIVE_NO_REMOTE_BIT_NUM                 =  (7),
    FAULT_CAUSE_ECAT_BIT_NUM                            =  (8),
    FAULT_CAUSE_DRIVE_WARNING_BIT_NUM                   =  (9),
    FAULT_CAUSE_GBC_OPERATION_ERROR_BIT_NUM             =  (10),
    FAULT_CAUSE_DRIVE_MOOERROR_BIT_NUM                  =  (11),
    FAULT_CAUSE_ECAT_SLAVE_ERROR_BIT_NUM                =  (12),
    FAULT_CAUSE_PLC_SIGNALLED_ERROR_BIT_NUM             =  (13),
    FAULT_CAUSE_HOMING_ERROR_BIT_NUM                    =  (14),
    FAULT_CAUSE_GBC_TO_PLC_CON_ERROR_BIT_NUM            =  (15),
    FAULT_CAUSE_MOVE_NOT_OP_EN_BIT_NUM                  =  (16),
    FAULT_CAUSE_DRIVE_STATE_MISMATCH_BIT_NUM            =  (17),
    FAULT_CAUSE_FSOE_ERROR_BIT_NUM                      =  (18),

class STATUS_WORD_GBEM(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    STATUS_WORD_GBEM_ALIVE_BIT_NUM                       =  (16),
    STATUS_WORD_GBEM_BOOT_IN_PROGRESS_BIT_NUM            =  (17),
    STATUS_WORD_GBEM_BOOTED_BIT_NUM                      =  (18),
    STATUS_WORD_GBEM_HOMING_NEEDED_BIT_NUM               =  (19),
    STATUS_WORD_GBEM_WAITING_FOR_START_HOMING_BIT_NUM    =  (20),
    STATUS_WORD_GBEM_HOMING_IN_PROGRESS_BIT_NUM          =  (21),
    STATUS_WORD_GBEM_HOMING_ERROR_BIT_NUM                =  (23),
    STATUS_WORD_GBEM_HOMING_ATTAINED_BIT_NUM             =  (24),

class CONTROL_WORD_GBC_GBEM(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    CONTROL_WORD_GBC_OPERATION_ERROR_BIT_NUM            =  (16),
    CONTROL_WORD_GBEM_START_HOMING_BIT_NUM              =  (17),
    CONTROL_WORD_GBC_REQUEST_FAULT_BIT_NUM              =  (18),
    CONTROL_WORD_GBEM_REBOOT_BIT_NUM                    =  (20),

class FSOE_SLAVE_HIGH_LEVEL_STATE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    FSOE_SLAVE_HIGH_LEVEL_STATE_NONE                    =  (0),
    FSOE_SLAVE_HIGH_LEVEL_STATE_PROCESS_DATA            =  (1),
    FSOE_SLAVE_HIGH_LEVEL_STATE_RESET                   =  (2),
    FSOE_SLAVE_HIGH_LEVEL_STATE_SESSION                 =  (3),
    FSOE_SLAVE_HIGH_LEVEL_STATE_CONNECTION              =  (4),
    FSOE_SLAVE_HIGH_LEVEL_STATE_PARAMETER               =  (5),
    FSOE_SLAVE_HIGH_LEVEL_STATE_FAILSAFEDATA            =  (6),
    FSOE_SLAVE_HIGH_LEVEL_STATE_UNKNOWN                 =  (7),

class FSOE_SLAVE_TYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    FSOE_SLAVE_TYPE_NONE                                =  (0),
    FSOE_SLAVE_TYPE_SYNAPTICON                          =  (1),
    FSOE_SLAVE_TYPE_EL1904                              =  (2),
    FSOE_SLAVE_TYPE_EL2904                              =  (3),
    FSOE_SLAVE_TYPE_SCU_1_EC                            =  (4),
    FSOE_SLAVE_TYPE_EL6900                              =  (5),
    FSOE_SLAVE_TYPE_EL6910                              =  (6),
    FSOE_SLAVE_TYPE_ELM7231                             =  (7),

class FSOE_MASTER_HIGH_LEVEL_STATE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    FSOE_MASTER_HIGH_LEVEL_STATE_NONE                   =  (0),
    FSOE_MASTER_HIGH_LEVEL_STATE_START_UP               =  (1),
    FSOE_MASTER_HIGH_LEVEL_STATE_SENDCONFIG             =  (2),
    FSOE_MASTER_HIGH_LEVEL_STATE_STARTUP_BUS            =  (3),
    FSOE_MASTER_HIGH_LEVEL_STATE_RUN                    =  (4),
    FSOE_MASTER_HIGH_LEVEL_STATE_STOP                   =  (5),
    FSOE_MASTER_HIGH_LEVEL_STATE_ERROR                  =  (6),
    FSOE_MASTER_HIGH_LEVEL_STATE_ALARM                  =  (7),
    FSOE_MASTER_HIGH_LEVEL_STATE_NO_NETWORK             =  (8),

class GBEM_REQUEST(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    GBEM_REQUEST_NONE                                  =  (0),
    GBEM_REQUEST_SDO_READ                              =  (1),
    GBEM_REQUEST_SDO_WRITE                             =  (2),
    GBEM_REQUEST_GET_VERSION                           =  (3),
    GBEM_REQUEST_GET_FILE                              =  (4),

class CONFIG_STATUS(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    CONFIG_STATUS_NONE = auto()
    CONFIG_STATUS_RELOAD = auto()
    CONFIG_STATUS_RELOAD_FULL = auto()
    CONFIG_STATUS_LOADED = auto()

class LIMITPROFILE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    LIMITPROFILE_DEFAULT = auto()
    LIMITPROFILE_JOGGING = auto()
    LIMITPROFILE_RAPIDS = auto()

class MODBUSERRORCODES(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    MODBUS_NO_SLAVE_INIT = auto()
    MODBUS_NO_ERROR = auto()
    MODBUS_COMMS_TIMEOUT = auto()
    MODBUS_BAD_CRC = auto()
    MODBUS_BAD_DATA = auto()
    MODBUS_BAD_FUNCTION = auto()
    MODBUS_BAD_EXCEPTION = auto()
    MODBUS_TOO_MUCH_DATA = auto()
    MODBUS_BAD_SLAVE = auto()
    MODBUS_INTERNAL_TIMEOUT = auto()
    MODBUS_CONNECTION_RESET = auto()
    MODBUS_INVALID_ARGUMENT = auto()
    MODBUS_INTERRUPTED = auto()
    MODBUS_EX_ILLEGAL_FUNCTION = auto()
    MODBUS_EX_ILLEGAL_DATA_ADDRESS = auto()
    MODBUS_EX_ILLEGAL_DATA_VALUE = auto()
    MODBUS_EX_SLAVE_OR_SERVER_FAILURE = auto()
    MODBUS_EX_ACKNOWLEDGE = auto()
    MODBUS_EX_SLAVE_OR_SERVER_BUSY = auto()
    MODBUS_EX_NEGATIVE_ACKNOWLEDGE = auto()
    MODBUS_EX_MEMORY_PARITY = auto()
    MODBUS_EX_GATEWAY_PATH = auto()
    MODBUS_EX_GATEWAY_TARGET = auto()
    MODBUS_EL6021_RX_FIFO_FULL = auto()
    MODBUS_EL6021_PARITY_ERROR = auto()
    MODBUS_EL6021_FRAMING_ERROR = auto()
    MODBUS_EL6021_OVERRUN_ERROR = auto()
    MODBUS_EL6021_NO_SLAVE_INIT = auto()
    MODBUS_GENERAL_ERROR = auto()

class MACHINETARGET(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    MACHINETARGET_NONE = auto()
    MACHINETARGET_FIELDBUS = auto()
    MACHINETARGET_SIMULATION = auto()

class OPERATION_ERROR(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    OPERATION_ERROR_NONE = auto()
    OPERATION_ERROR_HLC_HEARTBEAT_LOST = auto()
    OPERATION_ERROR_OPERATION_NOT_ENABLED = auto()
    OPERATION_ERROR_INVALID_ARC = auto()
    OPERATION_ERROR_TOOL_INDEX_OUT_OF_RANGE = auto()
    OPERATION_ERROR_JOINT_LIMIT_EXCEEDED = auto()
    OPERATION_ERROR_KINEMATICS_FK_INVALID_VALUE = auto()
    OPERATION_ERROR_KINEMATICS_IK_INVALID_VALUE = auto()
    OPERATION_ERROR_KINEMATICS_INVALID_KIN_CHAIN_PARAMS = auto()
    OPERATION_ERROR_JOINT_DISCONTINUITY = auto()
    OPERATION_ERROR_JOINT_OVER_SPEED = auto()
    OPERATION_ERROR_INVALID_ROTATION = auto()
    OPERATION_ERROR_CONFIG_RELOADED = auto()
    OPERATION_ERROR_KINEMATICS_ENVELOPE_VIOLATION = auto()
    OPERATION_ERROR_KINEMATICS_NEAR_SINGULARITY = auto()
    OPERATION_ERROR_MODBUS_WRITE_FAILURE = auto()

class POSITIONREFERENCE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    ABSOLUTE = auto()
    RELATIVE = auto()
    MOVESUPERIMPOSED = auto()

class ROTATIONINTERPOLATION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    ROTATIONINTERPOLATION_SHORT_SLERP = auto()
    ROTATIONINTERPOLATION_LONG_SLERP = auto()

class TASK_STATE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    TASK_NOTSTARTED = auto()
    TASK_RUNNING = auto()
    TASK_FINISHED = auto()
    TASK_PAUSED = auto()
    TASK_STOPPING = auto()
    TASK_CANCELLED = auto()
    TASK_ERROR = auto()

class TASK_COMMAND(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    TASK_IDLE = auto()
    TASK_RUN = auto()
    TASK_CANCEL = auto()
    TASK_PAUSE = auto()
    TASK_RESUME = auto()

class GTLT(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    GREATERTHAN = auto()
    LESSTHAN = auto()

class ACTIVITYTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    ACTIVITYTYPE_NONE = auto()
    ACTIVITYTYPE_PAUSEPROGRAM = auto()
    ACTIVITYTYPE_ENDPROGRAM = auto()
    ACTIVITYTYPE_MOVEJOINTS = auto()
    ACTIVITYTYPE_MOVEJOINTSATVELOCITY = auto()
    ACTIVITYTYPE_MOVELINE = auto()
    ACTIVITYTYPE_MOVEVECTORATVELOCITY = auto()
    ACTIVITYTYPE_MOVEROTATIONATVELOCITY = auto()
    ACTIVITYTYPE_MOVEARC = auto()
    ACTIVITYTYPE_MOVEINSTANT = auto()
    ACTIVITYTYPE_MOVETOPOSITION = auto()
    ACTIVITYTYPE_SETDOUT = auto()
    ACTIVITYTYPE_SETIOUT = auto()
    ACTIVITYTYPE_SETAOUT = auto()
    ACTIVITYTYPE_DWELL = auto()
    ACTIVITYTYPE_SPINDLE = auto()
    ACTIVITYTYPE_MOVEJOINTSINTERPOLATED = auto()
    ACTIVITYTYPE_SET_UIOUT = auto()
    ACTIVITYTYPE_SET_EXTERNAL_IOUT = auto()
    ACTIVITYTYPE_GEARINPOS = auto()
    ACTIVITYTYPE_GEARINVELO = auto()
    ACTIVITYTYPE_SET_EXTERNAL_DOUT = auto()
    ACTIVITYTYPE_TOOLOFFSET = auto()
    ACTIVITYTYPE_SET_EXTERNAL_UIOUT = auto()
    ACTIVITYTYPE_SET_PAYLOAD = auto()
    ACTIVITYTYPE_SETMODBUSDOUT = auto()
    ACTIVITYTYPE_SETMODBUSUIOUT = auto()

class ACTIVITYSTATE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    ACTIVITY_INACTIVE = auto()
    ACTIVITY_ACTIVE = auto()
    ACTIVITY_COMPLETED = auto()
    ACTIVITY_BLEND_ACTIVE = auto()
    ACTIVITY_CANCELLED = auto()

class STRATEGYGEARINPOS(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    PHASESHIFT = auto()
    EARLY = auto()
    LATE = auto()
    SLOW = auto()

class TRIGGERTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    TRIGGERTYPE_RISING = auto()
    TRIGGERTYPE_FALLING = auto()
    TRIGGERTYPE_HIGH = auto()
    TRIGGERTYPE_LOW = auto()

class ARCTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    ARCTYPE_CENTRE = auto()
    ARCTYPE_RADIUS = auto()

class ARCDIRECTION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    ARCDIRECTION_CW = auto()
    ARCDIRECTION_CCW = auto()

class SPINDLEDIRECTION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    SPINDLEDIRECTION_CW = auto()
    SPINDLEDIRECTION_CCW = auto()

class JOINT_TYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    JOINT_PRISMATIC = auto()
    JOINT_REVOLUTE = auto()

class JOINT_MODEOFOPERATION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    JOINT_MODEOFOPERATION_NONE    =  0,
    JOINT_MODEOFOPERATION_CSP     =  1,
    JOINT_MODEOFOPERATION_CSV     =  2,
    JOINT_MODEOFOPERATION_CST     =  4,
    JOINT_MODEOFOPERATION_HOMING  =  8,

class JOINT_FINITECONTINUOUS(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    JOINT_FINITE = auto()
    JOINT_CONTINUOUS = auto()

class JOINT_TORQUE_MODE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    JOINT_TORQUE_MODE_DEFAULT    =  0,
    JOINT_TORQUE_MODE_GRAVITY    =  1,
    JOINT_TORQUE_MODE_DIRECT     =  2,

class KC_KINEMATICSCONFIGURATIONTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_NAKED = auto()
    KC_SIXDOF = auto()
    KC_IGUS = auto()
    KC_SCARA = auto()
    KC_CARTESIAN = auto()
    KC_CARTESIAN_SLAVED = auto()
    KC_TWO_LINK = auto()
    KC_CUSTOM = auto()
    KC_REVOLUTE_DELTA = auto()
    KC_ANGLED_LINEAR_DELTA = auto()
    KC_RRPR_SCARA = auto()
    KC_PRISMATIC_STEWART = auto()
    KC_PUMA = auto()
    KC_FIVE_AXIS = auto()
    KC_WMR = auto()
    KC_MOVEABLE_SIXDOF = auto()

class KC_SHOULDERCONFIGURATION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_LEFTY = auto()
    KC_RIGHTY = auto()

class KC_ELBOWCONFIGURATION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_EPOSITIVE = auto()
    KC_ENEGATIVE = auto()

class KC_WRISTCONFIGURATION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_WPOSITIVE = auto()
    KC_WNEGATIVE = auto()

class KC_AUXILIARYAXISTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_AUXILIARYAXIS_NONE = auto()
    KC_AUXILIARYAXIS_X = auto()
    KC_AUXILIARYAXIS_Y = auto()
    KC_AUXILIARYAXIS_Z = auto()

class KC_ENVELOPE_CONSTRAINT_TYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_ENVELOPE_CONSTRAINT_NONE = auto()
    KC_ENVELOPE_CONSTRAINT_PLANE = auto()
    KC_ENVELOPE_CONSTRAINT_BOX = auto()
    KC_ENVELOPE_CONSTRAINT_CYLINDER = auto()
    KC_ENVELOPE_CONSTRAINT_SPHERE = auto()

class KC_ENVELOPE_CONSTRAINT_AXIS(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    KC_ENVELOPE_CONSTRAINT_AXIS_X = auto()
    KC_ENVELOPE_CONSTRAINT_AXIS_Y = auto()
    KC_ENVELOPE_CONSTRAINT_AXIS_Z = auto()

class BLENDTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    BLENDTYPE_NONE = auto()
    BLENDTYPE_OVERLAPPED = auto()

class SYNCTYPE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    SYNCTYPE_NONE = auto()
    SYNCTYPE_DURATION_MS = auto()
    SYNCTYPE_AT_TICK = auto()

class OPENCLOSED(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    OPEN = auto()
    CLOSED = auto()

class INTERFACE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    IO = auto()
    Modbus = auto()

class STREAMCOMMAND(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    STREAMCOMMAND_RUN = auto()
    STREAMCOMMAND_PAUSE = auto()
    STREAMCOMMAND_STOP = auto()

class STREAMSTATE(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    STREAMSTATE_IDLE = auto()
    STREAMSTATE_ACTIVE = auto()
    STREAMSTATE_PAUSED = auto()
    STREAMSTATE_PAUSED_BY_ACTIVITY = auto()
    STREAMSTATE_STOPPING = auto()
    STREAMSTATE_STOPPED = auto()

class TRIGGERON(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    TRIGGERON_NONE = auto()
    TRIGGERON_ANALOG_INPUT = auto()
    TRIGGERON_DIGITAL_INPUT = auto()
    TRIGGERON_SAFE_DIGITAL_INPUT = auto()
    TRIGGERON_UNSIGNED_INTEGER_INPUT = auto()
    TRIGGERON_INTEGER_INPUT = auto()
    TRIGGERON_EXTERNAL_UNSIGNED_INTEGER_INPUT = auto()
    TRIGGERON_EXTERNAL_INTEGER_INPUT = auto()
    TRIGGERON_TIMER = auto()
    TRIGGERON_TICK = auto()

class TRIGGERACTION(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    TRIGGERACTION_NONE = auto()
    TRIGGERACTION_CANCEL = auto()
    TRIGGERACTION_START = auto()

class SERIAL_CONTROL_WORD(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    SERIAL_TRANSMIT_REQUEST_BIT_NUM                      =  (0),
    SERIAL_RECEIVE_ACCEPTED_BIT_NUM                      =  (1),
    SERIAL_INIT_REQUEST_BIT_NUM                          =  (2),

class SERIAL_STATUS_WORD(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return count  # This changes auto() to generate zero-based indexes

    SERIAL_TRANSMIT_ACCEPTED_BIT_NUM                     =  (0),
    SERIAL_RECEIVE_REQUEST_BIT_NUM                       =  (1),
    SERIAL_INIT_ACCEPTED_BIT_NUM                         =  (2),
    SERIAL_ERROR_BIT_NUM                                 =  (3),


# STRUCTS
class SharedMemHeader(BaseModel):
    status: Optional[CONFIG_STATUS] = None
    pass

class LimitConfiguration(BaseModel):
    vmax: Optional[float] = None
    amax: Optional[float] = None
    jmax: Optional[float] = None
    pass

class MachineConfig(BaseModel):
    busCycleTime: Optional[int] = None
    statusFrequency: Optional[int] = None
    heartbeatTimeout: Optional[int] = None
    pass

class MachineStatus(BaseModel):
    statusWord: Optional[int] = None
    activeFault: Optional[int] = None
    faultHistory: Optional[int] = None
    heartbeat: Optional[int] = None
    target: Optional[MACHINETARGET] = None
    targetConnectRetryCnt: Optional[int] = None
    operationError: Optional[OPERATION_ERROR] = None
    operationErrorMessage: Optional[str] = None
    pass

class MachineCommand(BaseModel):
    controlWord: Optional[int] = None
    hlcControlWord: Optional[int] = None
    heartbeat: Optional[int] = None
    target: Optional[MACHINETARGET] = None
    pass

class StreamConfig(BaseModel):
    enableEndProgram: Optional[bool] = None
    pass

class StreamStatus(BaseModel):
    streamState: Optional[STREAMSTATE] = None
    tag: Optional[int] = None
    time: Optional[int] = None
    pass

class StreamCommand(BaseModel):
    streamCommand: Optional[STREAMCOMMAND] = None
    pass

class MoveParametersConfig(BaseModel):
    vmax: Optional[float] = None
    vmaxPercentage: Optional[int] = None
    amaxPercentage: Optional[int] = None
    jmaxPercentage: Optional[int] = None
    limitConfigurationIndex: Optional[int] = None
    blendType: Optional[BLENDTYPE] = None
    blendTimePercentage: Optional[int] = None
    blendTolerance: Optional[float] = None
    toolIndex: Optional[int] = None
    syncType: Optional[SYNCTYPE] = None
    syncValue: Optional[int] = None
    optimizeJointDistance: Optional[bool] = None
    ignoreFeedrateOverride: Optional[bool] = None
    pass

class Vector3(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    pass

class Quat(BaseModel):
    w: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    pass

class CartesianPosition(BaseModel):
    positionReference: Optional[POSITIONREFERENCE] = None
    translation: Optional[Vector3] = None
    rotation: Optional[Quat] = None
    frameIndex: Optional[int] = None
    pass

class PositionAbsRel(BaseModel):
    positionReference: Optional[POSITIONREFERENCE] = None
    translation: Optional[Vector3] = None
    pass

class CartesianVector(BaseModel):
    vector: Optional[Vector3] = None
    frameIndex: Optional[int] = None
    pass

class DoubleValue(BaseModel):
    value: Optional[float] = None
    pass

class ArcsConfig(BaseModel):
    arcType: Optional[ARCTYPE] = None
    arcDirection: Optional[ARCDIRECTION] = None
    destination: Optional[CartesianPosition] = None
    plane: Optional[Quat] = None
    rotationInterpolation: Optional[ROTATIONINTERPOLATION] = None
    centre: Optional[PositionAbsRel] = None
    radius: Optional[DoubleValue] = None
    pass

class CartesianPositionsConfig(BaseModel):
    position: Optional[CartesianPosition] = None
    configuration: Optional[int] = None
    pass

class TriggerOnAnalogInput(BaseModel):
    input: Optional[int] = None
    when: Optional[GTLT] = None
    value: Optional[float] = None
    pass

class TriggerOnDigitalInput(BaseModel):
    input: Optional[int] = None
    when: Optional[TRIGGERTYPE] = None
    pass

class TriggerOnUnsignedIntegerInput(BaseModel):
    input: Optional[int] = None
    when: Optional[GTLT] = None
    value: Optional[int] = None
    pass

class TriggerOnIntegerInput(BaseModel):
    input: Optional[int] = None
    when: Optional[GTLT] = None
    value: Optional[int] = None
    pass

class TriggerOnTimer(BaseModel):
    delay: Optional[int] = None
    pass

class TriggerOnTick(BaseModel):
    value: Optional[int] = None
    pass

class TriggerParams(BaseModel):
    type: Optional[TRIGGERON] = None
    action: Optional[TRIGGERACTION] = None
    analog: Optional[TriggerOnAnalogInput] = None
    digital: Optional[TriggerOnDigitalInput] = None
    unsignedInteger: Optional[TriggerOnUnsignedIntegerInput] = None
    integer: Optional[TriggerOnIntegerInput] = None
    timer: Optional[TriggerOnTimer] = None
    tick: Optional[TriggerOnTick] = None
    pass

class TaskConfig(BaseModel):
    activityCount: Optional[int] = None
    firstActivityIndex: Optional[int] = None
    triggers: Optional[List[TriggerParams]] = None
    pass

class TaskStatus(BaseModel):
    taskState: Optional[TASK_STATE] = None
    currentActivityIndex: Optional[int] = None
    pass

class TaskCommand(BaseModel):
    taskCommand: Optional[TASK_COMMAND] = None
    pass

class PidConfig(BaseModel):
    kp: Optional[float] = None
    ki: Optional[float] = None
    kd: Optional[float] = None
    maxIntegral: Optional[float] = None
    minIntegral: Optional[float] = None
    sampleTime: Optional[int] = None
    pass

class JointConfig(BaseModel):
    jointType: Optional[JOINT_TYPE] = None
    limits: Optional[List[LimitConfiguration]] = None
    preferredMode: Optional[JOINT_MODEOFOPERATION] = None
    supportedModes: Optional[int] = None
    supportedTorqueModes: Optional[int] = None
    scale: Optional[float] = None
    scalePos: Optional[float] = None
    scaleVel: Optional[float] = None
    scaleTorque: Optional[float] = None
    pow10: Optional[int] = None
    negLimit: Optional[float] = None
    posLimit: Optional[float] = None
    inverted: Optional[bool] = None
    finiteContinuous: Optional[JOINT_FINITECONTINUOUS] = None
    isVirtualInternal: Optional[bool] = None
    isVirtualFromEncoder: Optional[bool] = None
    correspondingJointNumberOnPhysicalFieldbus: Optional[int] = None
    correspondingJointNumberOnVirtualFieldbus: Optional[int] = None
    pidConfig: Optional[List[PidConfig]] = None
    dynamicsVelocityThreshold: Optional[float] = None
    pass

class JointStatus(BaseModel):
    statusWord: Optional[int] = None
    actPos: Optional[float] = None
    actVel: Optional[float] = None
    actTorque: Optional[float] = None
    actControlEffort: Optional[int] = None
    pass

class JointCommand(BaseModel):
    controlWord: Optional[int] = None
    setTorque: Optional[float] = None
    torqueMode: Optional[JOINT_TORQUE_MODE] = None
    pass

class MatrixInstanceDouble(BaseModel):
    numRows: Optional[int] = None
    numCols: Optional[int] = None
    data: Optional[List[float]] = None
    invJointAngles: Optional[List[int]] = None
    pass

class RollPitchYaw(BaseModel):
    r: Optional[float] = None
    p: Optional[float] = None
    y: Optional[float] = None
    pass

class UrdfFrame(BaseModel):
    translation: Optional[Vector3] = None
    rpy: Optional[RollPitchYaw] = None
    pass

class RigidBodyInertia(BaseModel):
    m: Optional[float] = None
    h: Optional[Vector3] = None
    Ixx: Optional[float] = None
    Iyy: Optional[float] = None
    Izz: Optional[float] = None
    Ixy: Optional[float] = None
    Ixz: Optional[float] = None
    Iyz: Optional[float] = None
    pass

class InverseDynamicParameters(BaseModel):
    urdfFrame: Optional[UrdfFrame] = None
    rigidBodyInertia: Optional[RigidBodyInertia] = None
    jointOffset: Optional[float] = None
    jointScale: Optional[float] = None
    jointInertia: Optional[float] = None
    jointAxis: Optional[Vector3] = None
    damping: Optional[float] = None
    friction: Optional[float] = None
    pass

class PlanarEnvelope(BaseModel):
    direction: Optional[KC_ENVELOPE_CONSTRAINT_AXIS] = None
    position: Optional[float] = None
    outside: Optional[bool] = None
    pass

class BoxEnvelope(BaseModel):
    origin: Optional[Vector3] = None
    extents: Optional[Vector3] = None
    outside: Optional[bool] = None
    pass

class CylinderEnvelope(BaseModel):
    center: Optional[Vector3] = None
    radius: Optional[float] = None
    height: Optional[float] = None
    axis: Optional[KC_ENVELOPE_CONSTRAINT_AXIS] = None
    outside: Optional[bool] = None
    pass

class SphericalEnvelope(BaseModel):
    center: Optional[Vector3] = None
    radius: Optional[float] = None
    outside: Optional[bool] = None
    pass

class EnvelopeConstraint(BaseModel):
    constraintType: Optional[KC_ENVELOPE_CONSTRAINT_TYPE] = None
    plane: Optional[PlanarEnvelope] = None
    box: Optional[BoxEnvelope] = None
    cylinder: Optional[CylinderEnvelope] = None
    sphere: Optional[SphericalEnvelope] = None
    pass

class VelocityScaling(BaseModel):
    enabled: Optional[bool] = None
    trigger: Optional[TriggerOnDigitalInput] = None
    safeInput: Optional[bool] = None
    scaleFactor: Optional[float] = None
    pass

class KinematicsConfigurationConfig(BaseModel):
    kinematicsConfigurationType: Optional[KC_KINEMATICSCONFIGURATIONTYPE] = None
    supportedConfigurationBits: Optional[int] = None
    frameIndex: Optional[int] = None
    participatingJoints: Optional[List[int]] = None
    participatingJointsCount: Optional[int] = None
    scaleX: Optional[float] = None
    scaleY: Optional[float] = None
    scaleZ: Optional[float] = None
    linearLimits: Optional[List[LimitConfiguration]] = None
    angularLimits: Optional[List[LimitConfiguration]] = None
    velocityScaling: Optional[List[VelocityScaling]] = None
    kinChainParams: Optional[MatrixInstanceDouble] = None
    inverseDynamicParams: Optional[List[InverseDynamicParameters]] = None
    envelopeConstraints: Optional[List[EnvelopeConstraint]] = None
    auxiliaryAxisType: Optional[KC_AUXILIARYAXISTYPE] = None
    auxiliaryAxisFactor: Optional[float] = None
    defaultToolIndex: Optional[int] = None
    pass

class KinematicsConfigurationStatus(BaseModel):
    froTarget: Optional[float] = None
    froActual: Optional[float] = None
    configuration: Optional[int] = None
    cartesianActPos: Optional[Vector3] = None
    cartesianActOrientation: Optional[Quat] = None
    cartesianActVel: Optional[Vector3] = None
    cartesianActAcc: Optional[Vector3] = None
    limitsDisabled: Optional[bool] = None
    isNearSingularity: Optional[int] = None
    toolIndex: Optional[int] = None
    pass

class KinematicsConfigurationCommand(BaseModel):
    doStop: Optional[bool] = None
    disableLimits: Optional[bool] = None
    fro: Optional[float] = None
    translation: Optional[Vector3] = None
    rotation: Optional[Quat] = None
    payload: Optional[float] = None
    pass

class DinConfig(BaseModel):
    inverted: Optional[bool] = None
    pass

class DinStatus(BaseModel):
    actValue: Optional[bool] = None
    pass

class DinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class SafetyDinConfig(BaseModel):
    inverted: Optional[bool] = None
    pass

class SafetyDinStatus(BaseModel):
    actValue: Optional[bool] = None
    pass

class SafetyDinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class ExternalDinConfig(BaseModel):
    inverted: Optional[bool] = None
    pass

class ExternalDinStatus(BaseModel):
    actValue: Optional[bool] = None
    pass

class ExternalDinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class ModbusDinConfig(BaseModel):
    slaveNum: Optional[int] = None
    address: Optional[int] = None
    function: Optional[int] = None
    littleEndian: Optional[bool] = None
    inverted: Optional[bool] = None
    pass

class ModbusDinStatus(BaseModel):
    actValue: Optional[bool] = None
    errorCode: Optional[int] = None
    isError: Optional[bool] = None
    pass

class ModbusDinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class DoutConfig(BaseModel):
    loopback: Optional[int] = None
    pass

class DoutStatus(BaseModel):
    effectiveValue: Optional[bool] = None
    pass

class DoutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class SafetyDoutConfig(BaseModel):
    loopback: Optional[int] = None
    pass

class SafetyDoutStatus(BaseModel):
    effectiveValue: Optional[bool] = None
    pass

class SafetyDoutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class ExternalDoutConfig(BaseModel):
    loopback: Optional[int] = None
    pass

class ExternalDoutStatus(BaseModel):
    effectiveValue: Optional[bool] = None
    pass

class ExternalDoutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[bool] = None
    pass

class ModbusDoutConfig(BaseModel):
    slaveNum: Optional[int] = None
    startAddress: Optional[int] = None
    endAddress: Optional[int] = None
    pass

class AinConfig(BaseModel):
    useForVirtualAxis: Optional[bool] = None
    jointIndexForVirtualAxis: Optional[int] = None
    pass

class AinStatus(BaseModel):
    actValue: Optional[float] = None
    pass

class AinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[float] = None
    pass

class AoutConfig(BaseModel):
    pass

class AoutStatus(BaseModel):
    effectiveValue: Optional[float] = None
    pass

class AoutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[float] = None
    pass

class UiinConfig(BaseModel):
    pass

class UiinStatus(BaseModel):
    actValue: Optional[int] = None
    pass

class UiinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class IinConfig(BaseModel):
    pass

class IinStatus(BaseModel):
    actValue: Optional[int] = None
    pass

class IinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class ExternalUiinConfig(BaseModel):
    pass

class ExternalUiinStatus(BaseModel):
    actValue: Optional[int] = None
    pass

class ExternalUiinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class ExternalIinConfig(BaseModel):
    pass

class ExternalIinStatus(BaseModel):
    actValue: Optional[int] = None
    pass

class ExternalIinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class ModbusUiinConfig(BaseModel):
    slaveNum: Optional[int] = None
    address: Optional[int] = None
    function: Optional[int] = None
    pass

class ModbusUiinStatus(BaseModel):
    actValue: Optional[int] = None
    errorCode: Optional[int] = None
    isError: Optional[bool] = None
    pass

class ModbusUiinCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class UioutConfig(BaseModel):
    pass

class UioutStatus(BaseModel):
    effectiveValue: Optional[int] = None
    pass

class UioutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class IoutConfig(BaseModel):
    pass

class IoutStatus(BaseModel):
    effectiveValue: Optional[int] = None
    pass

class IoutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class ExternalUioutConfig(BaseModel):
    pass

class ExternalUioutStatus(BaseModel):
    effectiveValue: Optional[int] = None
    pass

class ExternalUioutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class ExternalIoutConfig(BaseModel):
    pass

class ExternalIoutStatus(BaseModel):
    effectiveValue: Optional[int] = None
    pass

class ExternalIoutCommand(BaseModel):
    override: Optional[bool] = None
    setValue: Optional[int] = None
    pass

class ModbusUioutConfig(BaseModel):
    slaveNum: Optional[int] = None
    startAddress: Optional[int] = None
    endAddress: Optional[int] = None
    littleEndian: Optional[bool] = None
    pass

class MoveJointsActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    jointPositionArray: Optional[List[float]] = None
    positionReference: Optional[POSITIONREFERENCE] = None
    moveParamsIndex: Optional[int] = None
    pass

class MoveJointsActivityStatus(BaseModel):
    percentageComplete: Optional[int] = None
    pass

class MoveJointsActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveJointsStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    positionReference: Optional[POSITIONREFERENCE] = None
    jointPositionArray: Optional[List[float]] = None
    moveParams: Optional[MoveParametersConfig] = None
    pass

class MoveJointsInterpolatedActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    jointPositionArray: Optional[List[float]] = None
    jointVelocityArray: Optional[List[float]] = None
    timecode: Optional[float] = None
    moveParamsIndex: Optional[int] = None
    pass

class MoveJointsInterpolatedActivityStatus(BaseModel):
    pass

class MoveJointsInterpolatedActivityCommand(BaseModel):
    pass

class MoveJointsInterpolatedStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    jointPositionArray: Optional[List[float]] = None
    jointVelocityArray: Optional[List[float]] = None
    duration: Optional[float] = None
    moveParams: Optional[MoveParametersConfig] = None
    pass

class MoveJointsAtVelocityActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParamsIndex: Optional[int] = None
    jointVelocityArray: Optional[List[float]] = None
    pass

class MoveJointsAtVelocityActivityStatus(BaseModel):
    pass

class MoveJointsAtVelocityActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveJointsAtVelocityStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    jointVelocityArray: Optional[List[float]] = None
    pass

class MoveLineActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParamsIndex: Optional[int] = None
    line: Optional[CartesianPosition] = None
    superimposedIndex: Optional[int] = None
    pass

class MoveLineActivityStatus(BaseModel):
    pass

class MoveLineActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveLineStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    line: Optional[CartesianPosition] = None
    superimposedIndex: Optional[int] = None
    pass

class MoveVectorAtVelocityActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParamsIndex: Optional[int] = None
    vector: Optional[CartesianVector] = None
    pass

class MoveVectorAtVelocityActivityStatus(BaseModel):
    pass

class MoveVectorAtVelocityActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveVectorAtVelocityStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    vector: Optional[CartesianVector] = None
    pass

class MoveRotationAtVelocityActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParamsIndex: Optional[int] = None
    axis: Optional[CartesianVector] = None
    pass

class MoveRotationAtVelocityActivityStatus(BaseModel):
    pass

class MoveRotationAtVelocityActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveRotationAtVelocityStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    axis: Optional[CartesianVector] = None
    pass

class MoveArcActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    superimposedIndex: Optional[int] = None
    moveParamsIndex: Optional[int] = None
    arc: Optional[ArcsConfig] = None
    pass

class MoveArcActivityStatus(BaseModel):
    pass

class MoveArcActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveArcStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    arc: Optional[ArcsConfig] = None
    superimposedIndex: Optional[int] = None
    pass

class MoveInstantActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    position: Optional[CartesianPosition] = None
    pass

class MoveInstantActivityStatus(BaseModel):
    pass

class MoveInstantActivityCommand(BaseModel):
    pass

class MoveInstantStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    position: Optional[CartesianPosition] = None
    pass

class MoveToPositionActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParamsIndex: Optional[int] = None
    cartesianPosition: Optional[CartesianPositionsConfig] = None
    pass

class MoveToPositionActivityStatus(BaseModel):
    pass

class MoveToPositionActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class MoveToPositionStream(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    moveParams: Optional[MoveParametersConfig] = None
    cartesianPosition: Optional[CartesianPositionsConfig] = None
    pass

class SetDoutActivityParams(BaseModel):
    doutToSet: Optional[int] = None
    valueToSet: Optional[bool] = None
    pass

class SetDoutActivityStatus(BaseModel):
    pass

class SetDoutActivityCommand(BaseModel):
    pass

class SetModbusDoutActivityParams(BaseModel):
    doutToSet: Optional[int] = None
    valueToSetArray: Optional[List[bool]] = None
    pass

class SetModbusDoutActivityStatus(BaseModel):
    errorCode: Optional[int] = None
    isError: Optional[bool] = None
    pass

class SetModbusDoutActivityCommand(BaseModel):
    pass

class SetAoutActivityParams(BaseModel):
    aoutToSet: Optional[int] = None
    valueToSet: Optional[float] = None
    pass

class SetAoutActivityStatus(BaseModel):
    pass

class SetAoutActivityCommand(BaseModel):
    pass

class SetIoutActivityParams(BaseModel):
    ioutToSet: Optional[int] = None
    valueToSet: Optional[int] = None
    pass

class SetIoutActivityStatus(BaseModel):
    pass

class SetIoutActivityCommand(BaseModel):
    pass

class SetUioutActivityParams(BaseModel):
    ioutToSet: Optional[int] = None
    valueToSet: Optional[int] = None
    pass

class SetUioutActivityStatus(BaseModel):
    pass

class SetUioutActivityCommand(BaseModel):
    pass

class SetModbusUioutActivityParams(BaseModel):
    uioutToSet: Optional[int] = None
    valueToSetArray: Optional[List[int]] = None
    pass

class SetModbusUioutActivityStatus(BaseModel):
    errorCode: Optional[int] = None
    isError: Optional[bool] = None
    pass

class SetModbusUioutActivityCommand(BaseModel):
    pass

class DwellActivityParams(BaseModel):
    msToDwell: Optional[int] = None
    pass

class DwellActivityStatus(BaseModel):
    pass

class DwellActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    pass

class SpindleConfig(BaseModel):
    enableDigitalOutIndex: Optional[int] = None
    directionDigitalOutIndex: Optional[int] = None
    directionInvert: Optional[bool] = None
    speedAnalogOutIndex: Optional[int] = None
    pass

class SpindleActivityParams(BaseModel):
    spindleIndex: Optional[int] = None
    enable: Optional[bool] = None
    direction: Optional[SPINDLEDIRECTION] = None
    speed: Optional[float] = None
    pass

class SpindleActivityStatus(BaseModel):
    pass

class SpindleActivityCommand(BaseModel):
    pass

class ToolOffsetActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    toolIndex: Optional[int] = None
    pass

class GearInVeloActivityParams(BaseModel):
    masterKinematicsConfigurationIndex: Optional[int] = None
    slaveKinematicsConfigurationIndex: Optional[int] = None
    gearingFrameIndex: Optional[int] = None
    gearRatio: Optional[float] = None
    syncActivationDelay: Optional[int] = None
    pass

class GearInVeloActivityStatus(BaseModel):
    percentageComplete: Optional[int] = None
    gearInFailed: Optional[bool] = None
    gearedIn: Optional[bool] = None
    pass

class GearInVeloActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    updatedRatio: Optional[float] = None
    updateRation: Optional[bool] = None
    pass

class GearInPosActivityParams(BaseModel):
    masterKinematicsConfigurationIndex: Optional[int] = None
    slaveKinematicsConfigurationIndex: Optional[int] = None
    gearingFrameIndex: Optional[int] = None
    gearRatio: Optional[float] = None
    strategyToUse: Optional[STRATEGYGEARINPOS] = None
    gearRatioMaster: Optional[float] = None
    gearRatioSlave: Optional[float] = None
    masterSyncPosition: Optional[CartesianPosition] = None
    slaveSyncPosition: Optional[CartesianPosition] = None
    syncActivationDelay: Optional[int] = None
    pass

class GearInPosActivityStatus(BaseModel):
    percentageComplete: Optional[int] = None
    gearInFailed: Optional[bool] = None
    gearedIn: Optional[bool] = None
    pass

class GearInPosActivityCommand(BaseModel):
    skipToNext: Optional[bool] = None
    updatedRatioMaster: Optional[float] = None
    updatedRatioSlave: Optional[float] = None
    updatedMasterSyncPosition: Optional[CartesianPosition] = None
    updatedSlaveSyncPosition: Optional[CartesianPosition] = None
    pass

class SetPayloadActivityStatus(BaseModel):
    pass

class SetPayloadActivityCommand(BaseModel):
    pass

class SetPayloadActivityParams(BaseModel):
    kinematicsConfigurationIndex: Optional[int] = None
    mass: Optional[float] = None
    pass

class ActivityConfig(BaseModel):
    activityType: Optional[ACTIVITYTYPE] = None
    triggers: Optional[List[TriggerParams]] = None
    moveJoints: Optional[MoveJointsActivityParams] = None
    moveJointsInterpolated: Optional[MoveJointsInterpolatedActivityParams] = None
    moveJointsAtVelocity: Optional[MoveJointsAtVelocityActivityParams] = None
    moveLine: Optional[MoveLineActivityParams] = None
    moveVectorAtVelocity: Optional[MoveVectorAtVelocityActivityParams] = None
    moveRotationAtVelocity: Optional[MoveRotationAtVelocityActivityParams] = None
    moveArc: Optional[MoveArcActivityParams] = None
    moveInstant: Optional[MoveInstantActivityParams] = None
    moveToPosition: Optional[MoveToPositionActivityParams] = None
    gearInPos: Optional[GearInPosActivityParams] = None
    gearInVelo: Optional[GearInVeloActivityParams] = None
    setDout: Optional[SetDoutActivityParams] = None
    setExternalDout: Optional[SetDoutActivityParams] = None
    setAout: Optional[SetAoutActivityParams] = None
    setIout: Optional[SetIoutActivityParams] = None
    setUiout: Optional[SetUioutActivityParams] = None
    setExternalIout: Optional[SetIoutActivityParams] = None
    setExternalUiout: Optional[SetUioutActivityParams] = None
    dwell: Optional[DwellActivityParams] = None
    spindle: Optional[SpindleActivityParams] = None
    setModbusDout: Optional[SetModbusDoutActivityParams] = None
    setModbusUiout: Optional[SetModbusUioutActivityParams] = None
    pass

class ActivityStatus(BaseModel):
    state: Optional[ACTIVITYSTATE] = None
    tag: Optional[int] = None
    moveJoints: Optional[MoveJointsActivityStatus] = None
    moveJointsInterpolated: Optional[MoveJointsInterpolatedActivityStatus] = None
    moveJointsAtVelocity: Optional[MoveJointsAtVelocityActivityStatus] = None
    moveLine: Optional[MoveLineActivityStatus] = None
    moveVectorAtVelocity: Optional[MoveVectorAtVelocityActivityStatus] = None
    moveRotationAtVelocity: Optional[MoveRotationAtVelocityActivityStatus] = None
    moveArc: Optional[MoveArcActivityStatus] = None
    moveInstant: Optional[MoveInstantActivityStatus] = None
    moveToPosition: Optional[MoveToPositionActivityStatus] = None
    gearInPos: Optional[GearInPosActivityStatus] = None
    gearInVelo: Optional[GearInVeloActivityStatus] = None
    setDout: Optional[SetDoutActivityStatus] = None
    setExternalDout: Optional[SetDoutActivityStatus] = None
    setAout: Optional[SetAoutActivityStatus] = None
    setIout: Optional[SetIoutActivityStatus] = None
    setUiout: Optional[SetUioutActivityStatus] = None
    setExternalIout: Optional[SetIoutActivityStatus] = None
    setExternalUiout: Optional[SetUioutActivityStatus] = None
    dwell: Optional[DwellActivityStatus] = None
    spindle: Optional[SpindleActivityStatus] = None
    setModbusDout: Optional[SetModbusDoutActivityStatus] = None
    setModbusUiout: Optional[SetModbusUioutActivityStatus] = None
    pass

class ActivityCommand(BaseModel):
    moveJoints: Optional[MoveJointsActivityCommand] = None
    moveJointsInterpolated: Optional[MoveJointsInterpolatedActivityCommand] = None
    moveJointsAtVelocity: Optional[MoveJointsAtVelocityActivityCommand] = None
    moveLine: Optional[MoveLineActivityCommand] = None
    moveVectorAtVelocity: Optional[MoveVectorAtVelocityActivityCommand] = None
    moveRotationAtVelocity: Optional[MoveRotationAtVelocityActivityCommand] = None
    moveArc: Optional[MoveArcActivityCommand] = None
    moveInstant: Optional[MoveInstantActivityCommand] = None
    moveToPosition: Optional[MoveToPositionActivityCommand] = None
    gearInPos: Optional[GearInPosActivityCommand] = None
    gearInVelo: Optional[GearInVeloActivityCommand] = None
    setDout: Optional[SetDoutActivityCommand] = None
    setExternalDout: Optional[SetDoutActivityCommand] = None
    setAout: Optional[SetAoutActivityCommand] = None
    setIout: Optional[SetIoutActivityCommand] = None
    setUiout: Optional[SetUioutActivityCommand] = None
    setExternalIout: Optional[SetIoutActivityCommand] = None
    setExternalUiout: Optional[SetUioutActivityCommand] = None
    dwell: Optional[DwellActivityCommand] = None
    spindle: Optional[SpindleActivityCommand] = None
    setToolOffset: Optional[ToolOffsetActivityParams] = None
    setPayload: Optional[SetPayloadActivityParams] = None
    setModbusDout: Optional[SetModbusDoutActivityCommand] = None
    setModbusUiout: Optional[SetModbusUioutActivityCommand] = None
    pass

class ActivityStreamItem(BaseModel):
    activityType: Optional[ACTIVITYTYPE] = None
    tag: Optional[int] = None
    triggers: Optional[List[TriggerParams]] = None
    moveJoints: Optional[MoveJointsStream] = None
    moveJointsInterpolated: Optional[MoveJointsInterpolatedStream] = None
    moveJointsAtVelocity: Optional[MoveJointsAtVelocityStream] = None
    moveLine: Optional[MoveLineStream] = None
    moveVectorAtVelocity: Optional[MoveVectorAtVelocityStream] = None
    moveRotationAtVelocity: Optional[MoveRotationAtVelocityStream] = None
    moveArc: Optional[MoveArcStream] = None
    moveInstant: Optional[MoveInstantStream] = None
    moveToPosition: Optional[MoveToPositionStream] = None
    setDout: Optional[SetDoutActivityParams] = None
    setExternalDout: Optional[SetDoutActivityParams] = None
    setModbusDout: Optional[SetModbusDoutActivityParams] = None
    setAout: Optional[SetAoutActivityParams] = None
    setIout: Optional[SetIoutActivityParams] = None
    setUiout: Optional[SetUioutActivityParams] = None
    setExternalIout: Optional[SetIoutActivityParams] = None
    setExternalUiout: Optional[SetUioutActivityParams] = None
    setModbusUiout: Optional[SetModbusUioutActivityParams] = None
    dwell: Optional[DwellActivityParams] = None
    spindle: Optional[SpindleActivityParams] = None
    setToolOffset: Optional[ToolOffsetActivityParams] = None
    setPayload: Optional[SetPayloadActivityParams] = None
    pass

class SoloActivityConfig(BaseModel):
    pass

soloActivityStatus = ActivityStatus

soloActivityCommand = ActivityStreamItem

class FramesConfig(BaseModel):
    translation: Optional[Vector3] = None
    rotation: Optional[Quat] = None
    parentFrameIndex: Optional[int] = None
    positionReference: Optional[POSITIONREFERENCE] = None
    workspaceOffset: Optional[int] = None
    pass

class FramesCommand(BaseModel):
    pass

class FramesStatus(BaseModel):
    pass

class PointsConfig(BaseModel):
    frameIndex: Optional[int] = None
    translation: Optional[Vector3] = None
    rotation: Optional[Quat] = None
    configuration: Optional[int] = None
    pass

class ToolConfig(BaseModel):
    translation: Optional[Vector3] = None
    rotation: Optional[Quat] = None
    diameter: Optional[float] = None
    rigidBodyInertia: Optional[RigidBodyInertia] = None
    interface: Optional[INTERFACE] = None
    graspIo: Optional[int] = None
    releaseIo: Optional[int] = None
    graspSenseIo: Optional[int] = None
    releaseSenseIo: Optional[int] = None
    pass

class SerialConfig(BaseModel):
    pass

class SerialStatus(BaseModel):
    statusWord: Optional[int] = None
    length: Optional[int] = None
    data: Optional[List[int]] = None
    pass

class SerialCommand(BaseModel):
    controlWord: Optional[int] = None
    length: Optional[int] = None
    data: Optional[List[int]] = None
    pass

