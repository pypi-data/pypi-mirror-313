import asyncio

from ..logger import log

"""
Tracks stream state and will push new activities to a stream when capacity is available.
Maintains futures that can be awaited when submitted activities are complete.
"""

from glowbuzzer.gbp.client import GbcWebsocketInterface
from .types import RegisteredGbcMessageEffect
from glowbuzzer.gbp.gbc import ActivityStreamItem, STREAMSTATE
from glowbuzzer.gbp.gbc_extra import StreamStatus, GlowbuzzerInboundMessage, GlowbuzzerStreamRequest


class Stream(RegisteredGbcMessageEffect):
    def __init__(self, index: int):
        self.tag = 0
        self.queue = []
        self.sent = []
        self.streamIndex = index

    def select(self, msg: GlowbuzzerInboundMessage):
        if msg.stream and len(msg.stream) > self.streamIndex:
            # remove time as it thrashes the on_change handler when there are no other changes
            copy = StreamStatus(**msg.stream[self.streamIndex].model_dump(exclude={"time"}))
            return copy, self.tag

    async def on_change(self, info: (StreamStatus, int), send: GbcWebsocketInterface):
        queue, tag = info
        log.debug("Stream.on_change: %s", info)
        match queue.state:
            case STREAMSTATE.STREAMSTATE_IDLE:
                self.resolve_futures()
                await self.send_up_to_capacity(queue, send)
            case STREAMSTATE.STREAMSTATE_STOPPED:
                self.resolve_futures(include_queue=True)
            case STREAMSTATE.STREAMSTATE_ACTIVE:
                await self.send_up_to_capacity(queue, send)
            case STREAMSTATE.STREAMSTATE_PAUSED:
                await self.send_up_to_capacity(queue, send)
            case STREAMSTATE.STREAMSTATE_PAUSED_BY_ACTIVITY:
                # TODO: H: we need to send pause command
                pass

    def exec(self, *activities: ActivityStreamItem):
        def create_future(activity: ActivityStreamItem):
            self.tag += 1
            copy = activity.model_copy(update={"tag": self.tag})
            return copy, asyncio.get_event_loop().create_future()

        with_futures = [create_future(activity) for activity in activities]
        log.debug("Adding to internal queue: %d", len(with_futures))
        self.queue.extend(with_futures)

        return asyncio.gather(*[activity[1] for activity in with_futures])

    def resolve_futures(self, include_queue=False):
        for activity, future in self.sent:
            future.set_result(None)

        if include_queue:
            for activity, future in self.queue:
                future.set_result(None)

    async def send_up_to_capacity(self, queue: StreamStatus, send: GbcWebsocketInterface):
        if queue.capacity == 0 or len(self.queue) == 0:
            # no capacity or nothing to send
            return

        # take items from the queue
        items_to_send, self.queue = self.queue[: queue.capacity], self.queue[queue.capacity :]
        # add them to sent items for later resolution
        self.sent.extend(items_to_send)

        # extract the activity
        items = [item[0] for item in items_to_send]

        # do the send
        request = GlowbuzzerStreamRequest(streamIndex=self.streamIndex, items=items)
        log.debug("Sending stream items: %d", len(items))
        await send.stream(request)
