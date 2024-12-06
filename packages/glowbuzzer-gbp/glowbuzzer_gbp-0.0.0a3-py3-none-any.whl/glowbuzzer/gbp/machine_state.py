from enum import Enum

"""
Provides low-level machine status word and control word handling. Understands how to
interpret the status word and how to generate the control word to transition GBC through
the CIA402 state machine.
"""


class MachineState(Enum):
    UNKNOWN = "UNKNOWN"
    FAULT_REACTION_ACTIVE = "FAULT_REACTION_ACTIVE"
    FAULT = "FAULT"
    NOT_READY_TO_SWITCH_ON = "NOT_READY_TO_SWITCH_ON"
    SWITCH_ON_DISABLED = "SWITCH_ON_DISABLED"  # this actually means it can be switched on!!!
    READY_TO_SWITCH_ON = "READY_TO_SWITCH_ON"
    SWITCHED_ON = "SWITCHED_ON"
    OPERATION_ENABLED = "OPERATION_ENABLED"
    QUICK_STOP = "QUICK_STOP"


class DesiredState(Enum):
    NONE = "NONE"
    OPERATIONAL = "OPERATIONAL"
    STANDBY = "STANDBY"
    QUICKSTOP = "QUICKSTOP"


def determine_machine_state(status: int) -> MachineState:
    if status & 0b1000:
        return MachineState.FAULT_REACTION_ACTIVE if (status & 0b1111) == 0b1111 else MachineState.FAULT

    if (status & 0b01001111) == 0b01000000:
        return MachineState.SWITCH_ON_DISABLED

    match status & 0b100111:
        case 0b100001:
            return MachineState.READY_TO_SWITCH_ON
        case 0b100011:
            return MachineState.SWITCHED_ON
        case 0b100111:
            return MachineState.OPERATION_ENABLED
        case 0b000111:
            return MachineState.QUICK_STOP

    return MachineState.UNKNOWN


class PossibleTransitions:
    @staticmethod
    def FaultSet():
        return 0b10000000000000000

    @staticmethod
    def FaultClear(c):
        return c & 0b10111111

    @staticmethod
    def FaultReset():
        return 0b10000000

    @staticmethod
    def Shutdown():
        return 0b00000110

    @staticmethod
    def DisableVoltage():
        return 0b00000000

    @staticmethod
    def SwitchOn():
        return 0b00000111

    @staticmethod
    def EnableOperation():
        return 0b00001111

    @staticmethod
    def QuickStop():
        return 0b00000010


def handle_machine_state(current_state: MachineState, control_word: int, desired_state: DesiredState) -> int | None:
    match desired_state:
        case DesiredState.OPERATIONAL:
            match current_state:
                case MachineState.FAULT:
                    return PossibleTransitions.FaultReset()
                case MachineState.SWITCH_ON_DISABLED:
                    return PossibleTransitions.Shutdown()
                case MachineState.READY_TO_SWITCH_ON:
                    return PossibleTransitions.SwitchOn()
                case MachineState.QUICK_STOP | MachineState.SWITCHED_ON:
                    return PossibleTransitions.EnableOperation()
        case DesiredState.STANDBY:
            match current_state:
                case MachineState.SWITCH_ON_DISABLED:
                    if control_word == PossibleTransitions.FaultReset():
                        # clear the fault reset command
                        return PossibleTransitions.DisableVoltage()
                case MachineState.OPERATION_ENABLED | MachineState.QUICK_STOP | MachineState.READY_TO_SWITCH_ON:
                    return PossibleTransitions.DisableVoltage()
        case DesiredState.QUICKSTOP:
            match current_state:
                case MachineState.OPERATION_ENABLED:
                    return PossibleTransitions.QuickStop()
        case DesiredState.NONE:
            if current_state == MachineState.SWITCH_ON_DISABLED and control_word == PossibleTransitions.FaultReset():
                # clear the fault reset command
                return PossibleTransitions.DisableVoltage()
    return None
