from abc import ABC, abstractmethod
from typing import Any

from glowbuzzer.gbp import GbcWebsocketInterface, GlowbuzzerInboundMessage


class RegisteredGbcMessageEffect(ABC):
    """
    Interface for effects that are triggered by GBC messages
    """

    @abstractmethod
    def select(self, status: GlowbuzzerInboundMessage) -> Any:
        """
        Select the value from the GBC message that this effect is interested in.

        :param status: The full GBC status object
        :return: The value to be tracked. This should be deeply comparable with the previous state, for example a Tuple or nested Dict.
        """
        pass

    @abstractmethod
    async def on_change(self, state, send: GbcWebsocketInterface) -> None:
        """
        Called when the selected value changes.

        :param state: The state that was selected
        :param send: Object containing methods used to send messages to GBC, if required
        """
        pass
