import asyncio
from typing import Any, Optional

from glowbuzzer.gbp import (
    GlowbuzzerInboundMessage,
    DigitalOutputStatus,
    GbcWebsocketInterface,
    RegisteredGbcMessageEffect,
    TRIGGERTYPE,
)


class DigitalInputTriggerEffect(RegisteredGbcMessageEffect):
    """
    Effect to wait for a trigger on a digital input. This effect can be used to wait for a rising or falling edge,
    or for the input to be high or low. Once created and registed with the GBC client, the `wait` method can be used to
    wait for the trigger to occur, with an optional timeout.

    Normally this is used with the `run_once` method of the GBC client to ensure the effect is used with a clean state
    and is unregistered after use.

    Example usage:
        ```python
        gbc = GbcClient()
        await gbc.connect("ws://localhost:8080")
        await gbc.run_once(DigitalInputTriggerEffect(0, TRIGGERTYPE.TRIGGERTYPE_RISING), lambda effect: effect.wait(10))
        ```
    """

    def __init__(self, input: int, trigger: TRIGGERTYPE):
        self.input = input
        self.state: Optional[bool] = None

        future = asyncio.get_event_loop().create_future()
        self.require = (trigger, future)

    def select(self, status: GlowbuzzerInboundMessage) -> Any:
        if status.status and status.status.din:
            return status.status.din[self.input].actValue

    async def on_change(self, state: bool, send: GbcWebsocketInterface) -> None:
        if self.require is not None:
            if self.state is not None:
                trigger, future = self.require
                match trigger:
                    case TRIGGERTYPE.TRIGGERTYPE_RISING:
                        if not self.state and state:
                            future.set_result(True)
                    case TRIGGERTYPE.TRIGGERTYPE_FALLING:
                        if self.state and not state:
                            future.set_result(True)
                    case TRIGGERTYPE.TRIGGERTYPE_HIGH:
                        if state:
                            future.set_result(True)
                    case TRIGGERTYPE.TRIGGERTYPE_LOW:
                        if not state:
                            future.set_result(True)

            self.state = state

    async def wait(self, timeout: int = 0) -> bool:
        trigger, future = self.require
        if timeout:
            return await asyncio.wait_for(future, timeout)

        return await future


class DigitalOutputStatusEffect(RegisteredGbcMessageEffect):
    """
    Effect to track the status of the specified digital output. Users of this effect can get the current state
    at any time but be aware there can be a short delay between setting a digital output and the status being updated.
    """

    def __init__(self, output: int):
        self.output = output
        self.state: Optional[DigitalOutputStatus] = None

    def select(self, status: GlowbuzzerInboundMessage) -> Any:
        if status.status and status.status.dout:
            return status.status.dout[self.output]

    async def on_change(self, state: DigitalOutputStatus, send: GbcWebsocketInterface) -> None:
        self.state = state
