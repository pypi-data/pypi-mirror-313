from typing import List, Optional, Any

from pydantic import BaseModel

from .gbc import (
    STREAMSTATE,
    MachineStatus,
    ActivityStatus,
    JointStatus,
    Vector3,
    Quat,
    ModbusUiinStatus,
    DinStatus,
    SafetyDinStatus,
    ModbusDinStatus,
    TaskStatus,
    SerialStatus,
    AoutStatus,
    AoutCommand,
    IoutStatus,
    IoutCommand,
    DoutStatus,
    DoutCommand,
    SafetyDoutStatus,
    SafetyDoutCommand,
    DinCommand,
    SafetyDinCommand,
    ActivityStreamItem,
)


class StreamStatus(BaseModel):
    capacity: int = 0
    queued: int = 0
    state: STREAMSTATE = STREAMSTATE.STREAMSTATE_IDLE
    tag: int = 0
    time: int = 0
    readCount: int = -1
    writeCount: int = -1


class AnalogOutputStatus(AoutStatus, AoutCommand):
    pass


class IntegerOutputStatus(IoutStatus, IoutCommand):
    pass


class DigitalOutputStatus(DoutStatus, DoutCommand):
    pass


class SafetyDigitalOutputStatus(SafetyDoutStatus, SafetyDoutCommand):
    pass


class DigitalInputStatus(DinStatus, DinCommand):
    pass


class SafetyDigitalInputStatus(SafetyDinStatus, SafetyDinCommand):
    pass


class GlowbuzzerKinematicsConfigurationStatus(BaseModel):
    isNearSingularity: bool
    limitsDisabled: bool
    froActual: float
    froTarget: float
    configuration: int
    toolIndex: int
    position: Vector3
    offset: Quat


class ExternalIOStatus(BaseModel):
    iin: List[int]
    uiin: List[int]
    din: List[bool]
    iout: List["IntegerOutputStatus"]  # Defined elsewhere
    uiout: List["IntegerOutputStatus"]  # Defined elsewhere
    dout: List["DigitalOutputStatus"]  # Defined elsewhere


class GlowbuzzerMachineStatus(MachineStatus):
    controlWord: Optional[int] = None


class GlowbuzzerCombinedStatus(BaseModel):
    machine: Optional[GlowbuzzerMachineStatus] = None
    activity: Optional[List[ActivityStatus]] = None
    joint: Optional[List[JointStatus]] = None
    kc: Optional[List[GlowbuzzerKinematicsConfigurationStatus]] = None
    ain: Optional[List[int]] = None
    iin: Optional[List[int]] = None
    uiin: Optional[List[int]] = None
    modbusUiin: Optional[List[ModbusUiinStatus]] = None
    din: Optional[List[DinStatus]] = None
    safetyDin: Optional[List[SafetyDinStatus]] = None
    modbusDin: Optional[List[ModbusDinStatus]] = None
    aout: Optional[List[AnalogOutputStatus]] = None
    iout: Optional[List[IntegerOutputStatus]] = None
    uiout: Optional[List[IntegerOutputStatus]] = None
    dout: Optional[List[DigitalOutputStatus]] = None
    safetyDout: Optional[List[SafetyDigitalOutputStatus]] = None
    tasks: Optional[List[TaskStatus]] = None
    external: Optional[ExternalIOStatus] = None
    serial: Optional[SerialStatus] = None


class Telemetry(BaseModel):
    t: int
    di: int
    do: int
    sdi: int
    sdo: int
    set: List[dict]  # Could define a specific class if the structure is complex
    act: List[dict]  # Could define a specific class if the structure is complex
    p: List[List[float]]  # Array of arrays for TCP position


class GlowbuzzerInboundMessage(BaseModel):
    stream: Optional[list[StreamStatus]] = None
    status: Optional[GlowbuzzerCombinedStatus] = None
    telemetry: Optional[List[Telemetry]] = None
    response: Optional[Any] = None
    emstat: Optional[dict] = None


class GlowbuzzerStreamRequest(BaseModel):
    streamIndex: int
    items: List[ActivityStreamItem]
