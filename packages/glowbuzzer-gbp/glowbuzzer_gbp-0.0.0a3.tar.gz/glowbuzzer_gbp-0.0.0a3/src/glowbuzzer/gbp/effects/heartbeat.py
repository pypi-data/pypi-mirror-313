from glowbuzzer.gbp import RegisteredGbcMessageEffect, GlowbuzzerInboundMessage, GbcWebsocketInterface, MachineCommand


class HeartbeatEcho(RegisteredGbcMessageEffect):
    def __init__(self):
        self.previous_heartbeat = 0

    def __repr__(self):
        return f"HeatbeatEffect({self.previous_heartbeat})"

    def select(self, msg: GlowbuzzerInboundMessage):
        if msg.status and msg.status.machine:
            return msg.status.machine.heartbeat

    async def on_change(self, new_heartbeat: int, send: GbcWebsocketInterface):
        if new_heartbeat - self.previous_heartbeat > 100:
            command: MachineCommand = MachineCommand(heartbeat=new_heartbeat)
            self.previous_heartbeat = new_heartbeat
            await send.command(command)
