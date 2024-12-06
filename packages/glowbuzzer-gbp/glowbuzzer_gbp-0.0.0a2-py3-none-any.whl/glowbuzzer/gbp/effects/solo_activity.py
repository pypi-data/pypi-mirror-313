import asyncio
from typing import Any

from glowbuzzer.gbp import log
from glowbuzzer.gbp.client import GbcWebsocketInterface
from glowbuzzer.gbp.effects import RegisteredGbcMessageEffect
from glowbuzzer.gbp.gbc import ActivityStatus, ActivityStreamItem, ACTIVITYSTATE, ACTIVITYTYPE
from glowbuzzer.gbp.gbc_extra import GlowbuzzerInboundMessage


class SoloActivity(RegisteredGbcMessageEffect):
    def __init__(self, index: int = 0):
        self.index = index
        self.tag = 0
        self.sent = []

    def select(self, message: GlowbuzzerInboundMessage) -> Any:
        if message.status and message.status.activity:
            return message.status.activity[self.index]

    async def on_change(self, status: ActivityStatus, send: GbcWebsocketInterface) -> None:
        state = status.state
        tag = status.tag

        while self.sent[0][0].tag < tag:
            # resolve any old activities that have been superseded by a later tag
            activity, future = self.sent.pop(0)
            future.set_result((tag, False))

        if state == ACTIVITYSTATE.ACTIVITY_COMPLETED:
            activity, future = self.sent.pop(0)
            future.set_result((tag, True))
        elif state == ACTIVITYSTATE.ACTIVITY_CANCELLED:
            activity, future = self.sent.pop(0)
            future.set_result((tag, False))

    async def exec(self, send: GbcWebsocketInterface, activity: ActivityStreamItem):
        self.tag += 1
        copy = activity.model_copy(update={"tag": self.tag})
        future = asyncio.get_event_loop().create_future()
        self.sent.append((copy, future))
        await send.command(copy, self.index)
        return await future

    async def cancel(self, send: GbcWebsocketInterface):
        return await self.exec(send, ActivityStreamItem(activityType=ACTIVITYTYPE.ACTIVITYTYPE_NONE))