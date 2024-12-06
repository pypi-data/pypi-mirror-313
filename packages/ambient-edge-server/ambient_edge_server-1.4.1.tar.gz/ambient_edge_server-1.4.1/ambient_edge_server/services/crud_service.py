from typing import Optional

from ambient_backend_api_client import ApiClient, Configuration
from ambient_backend_api_client import NodeOutput as Node
from ambient_backend_api_client import NodesApi

from ambient_client_common.repositories.node_repo import NodeRepo
from ambient_client_common.utils import logger


class CRUDService:
    """A service for interacting with stateful data on the node"""

    def __init__(self, node_repo: NodeRepo) -> None:
        self.node_repo = node_repo
        self.api_config: Optional[Configuration] = None

    async def init(self, api_config: Configuration) -> None:
        """Initialize the service with API configuration

        Args:
            api_config (Configuration): API configuration
        """
        self.api_config = api_config

    async def get_node_data(self) -> Node:
        """Get the node data from the repository.

        Returns:
            Node: Node data
        """
        logger.info("Fetching Node data from repository ...")
        return self.node_repo.get_node_data()

    async def clear_node_data(self) -> None:
        """Clear the node data in the repository.

        Returns:
            None
        """
        logger.info("Clearing Node data from repository ...")
        self.node_repo.clear_node_data()
        logger.info("Node data cleared")

    async def update_node_data(self) -> Node:
        """Fetch Node data from API and save to repo

        Returns:
            Node: Node data
        """

        logger.info("Updating Node data ...")
        # get node ID from repo
        node_id = self.node_repo.get_node_id()
        logger.debug("CRUDService.update_node_data() - Node ID: {}", node_id)

        # make API call
        if not self.api_config:
            logger.error("API Configuration not found")
            raise Exception("Has the CRUDService been initiated?")
        node: Optional[Node] = None
        async with ApiClient(self.api_config) as api_client:
            nodes_api = NodesApi(api_client)
            logger.debug(
                "CRUDService.update_node_data() - Fetching Node data from API ..."
            )
            node = await nodes_api.get_node_nodes_node_id_get(node_id=node_id)
            logger.debug("CRUDService.update_node_data() - Node data fetched: {}", node)
        logger.info("Node data fetched")

        # save data using node repo
        logger.info("Saving Node data to repository ...")
        self.node_repo.save_node_data(node)
        logger.info("Node data saved")

        # return node data
        return node
