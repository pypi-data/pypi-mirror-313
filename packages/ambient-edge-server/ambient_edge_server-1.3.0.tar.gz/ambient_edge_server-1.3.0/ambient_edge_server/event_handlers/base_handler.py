from abc import ABC, abstractmethod

from ambient_backend_api_client import EventLabel
from ambient_event_bus_client import Message

from ambient_edge_server.services.event_service import EventService


class BaseHandler(ABC):
    def __init__(self, event_service: EventService):
        self.event_svc = event_service

    @abstractmethod
    async def handle(self, msg: Message) -> None:
        """Handle a msg.

        Args:
            msg (Message): Message to handle
        """

    @property
    @abstractmethod
    def label(self) -> EventLabel:
        """Get the label of the handler.

        Returns:
            str: Handler label
        """

    async def subscribe(self):
        await self.event_svc.add_event_handler(self.label, self.handle)
