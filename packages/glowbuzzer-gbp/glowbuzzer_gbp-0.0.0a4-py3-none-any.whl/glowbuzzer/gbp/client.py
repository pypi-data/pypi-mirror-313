import json
from abc import ABC, abstractmethod

from pydantic import BaseModel

from glowbuzzer.gbp import (
    MachineCommand,
    ActivityStreamItem,
    DoutCommand,
    StreamCommand,
    JointCommand,
    KinematicsConfigurationCommand,
    SafetyDoutCommand,
    ExternalDoutCommand,
    DinCommand,
    SafetyDinCommand,
    ExternalDinCommand,
    ModbusDinCommand,
    AoutCommand,
    AinCommand,
    IoutCommand,
    UioutCommand,
    ExternalIoutCommand,
    ExternalUioutCommand,
    IinCommand,
    UiinCommand,
    ExternalIinCommand,
    ExternalUiinCommand,
    ModbusUiinCommand,
    GlowbuzzerStreamRequest,
)


def create_command_message(command: BaseModel, index: int, code: str) -> str:
    return json.dumps(
        {"command": {code: {str(index): {"command": command.model_dump(exclude_none=True, mode="json")}}}}
    )


def command_code(command: BaseModel) -> str:
    """
    Determine the correct command code for the given command, used to construct the message to send to GBC.
    :param command: The command to determine the code for
    :return: The command code
    """
    if isinstance(command, MachineCommand):
        return "machine"
    elif isinstance(command, StreamCommand):
        return "stream"
    elif isinstance(command, ActivityStreamItem):
        return "soloActivity"
    elif isinstance(command, JointCommand):
        return "joint"
    elif isinstance(command, KinematicsConfigurationCommand):
        return "kinematicsConfiguration"

    elif isinstance(command, DoutCommand):
        return "dout"
    elif isinstance(command, SafetyDoutCommand):
        return "safetyDout"
    elif isinstance(command, ExternalDoutCommand):
        return "externalDout"

    elif isinstance(command, DinCommand):
        return "din"
    elif isinstance(command, SafetyDinCommand):
        return "safetyDin"
    elif isinstance(command, ExternalDinCommand):
        return "externalDin"
    elif isinstance(command, ModbusDinCommand):
        return "modbusDin"

    elif isinstance(command, AoutCommand):
        return "aout"
    elif isinstance(command, AinCommand):
        return "ain"

    elif isinstance(command, IoutCommand):
        return "iout"
    elif isinstance(command, UioutCommand):
        return "uiout"
    elif isinstance(command, ExternalIoutCommand):
        return "externalIout"
    elif isinstance(command, ExternalUioutCommand):
        return "externalUiout"

    elif isinstance(command, IinCommand):
        return "iin"
    elif isinstance(command, UiinCommand):
        return "uiin"
    elif isinstance(command, ExternalIinCommand):
        return "externalIin"
    elif isinstance(command, ExternalUiinCommand):
        return "externalUiin"
    elif isinstance(command, ModbusUiinCommand):
        return "modbusUiin"

    else:
        raise ValueError(f"Unknown command type: {command.__class__.__name__}")


class GbcWebsocketInterface(ABC):
    @abstractmethod
    async def send(self, message: str):
        """
        Send raw message to GBC.
        :param message: The message to send
        """
        pass

    async def command(self, command: BaseModel, index: int = 0):
        """
        Send a command to GBC.
        :param command: The command to send. This must be a recognised command type or an error will occur.
        :param index: The index of the item in the GBC configuration to send the command to, default 0.
        :raises ValueError: If the command type is not recognised
        """
        return await self.send(create_command_message(command, index, command_code(command)))

    async def stream(self, request: GlowbuzzerStreamRequest):
        """
        Send activities to GBC.
        :param request: The stream index and activities to send.
        """
        msg = {"stream": request.model_dump(exclude_none=True, mode="json")}
        return await self.send(json.dumps(msg))
