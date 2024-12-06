from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from glowbuzzer.gbp import GbcWebsocketInterface, RegisteredGbcMessageEffect, GlowbuzzerInboundMessage


class Ros2Spinner(RegisteredGbcMessageEffect):
    """
    Simple GBC message effect to spin ROS2 node when a message is received
    """

    def __init__(self, node: Node):
        self.executor = MultiThreadedExecutor()
        self.executor.add_node(node)

    def select(self, msg: GlowbuzzerInboundMessage) -> int:
        if msg.status and msg.status.machine:
            return msg.status.machine.heartbeat

    async def on_change(self, state: int, controller: GbcWebsocketInterface):
        self.executor.spin_once(0)
