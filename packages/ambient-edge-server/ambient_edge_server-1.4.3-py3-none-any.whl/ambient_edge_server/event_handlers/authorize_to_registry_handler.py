import json
from typing import Optional

from ambient_backend_api_client import ContainerRegistryType, EventLabel
from ambient_event_bus_client import Message

from ambient_client_common.utils import logger
from ambient_edge_server.event_handlers.base_handler import BaseHandler
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.services.registry_service import RegistryServiceFactory


class AuthorizeRegistryHandler(BaseHandler):
    def __init__(
        self, event_svc: EventService, registry_svc_factory: RegistryServiceFactory
    ) -> None:
        super().__init__(event_svc)
        self.registry_svc_factory = registry_svc_factory
        logger.debug("AuthorizeRegistryHandler initialized.")

    @property
    def label(self) -> EventLabel:
        return EventLabel.CONTAINER_AUTH_REQUESTED

    async def handle(self, msg: Message) -> None:
        logger.info("Handling message for topic: {}", msg.topic)
        msg_data: dict = json.loads(msg.message)
        logger.info("Message data: {}", json.dumps(msg_data, indent=4))
        ws_session: Optional[str] = msg_data.get("ws_session", None)
        logger.debug("AuthorizeRegistryHandler.handle() - ws_session: {}", ws_session)

        if ws_session is None:
            logger.error("No websocket session found in message data.")
            return

        registry_type: ContainerRegistryType = msg_data.get(
            "registry_type", ContainerRegistryType.DOCKER_HUB
        )
        registry_svc = self.registry_svc_factory.get_registry_service(registry_type)
        logger.debug(
            "AuthorizeRegistryHandler.handle() - registry_svc: {} - {}",
            registry_svc,
            type(registry_svc),
        )

        logger.info("Authorizing ...")
        logger.debug(
            "AuthorizeRegistryHandler.handle() - authorize method: {}",
            registry_svc.authorize,
        )
        result = await registry_svc.authorize(ws_session=ws_session)
        if result.is_err():
            logger.error("Failed to authorize registry: {}", result.unwrap_err())
            return
        logger.info("Registry authorized successfully.")
