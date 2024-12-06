import asyncio
import datetime
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set

import aiohttp
import apluggy as pluggy
from ambient_backend_api_client import ApiClient, Configuration, DockerSwarmInfo
from ambient_backend_api_client import NodeOutput as Node
from result import Err, Ok, Result

from ambient_client_common.repositories.docker_repo import DockerRepo
from ambient_client_common.repositories.node_repo import NodeRepo
from ambient_client_common.utils import logger
from ambient_edge_server.services.authorization_service import AuthorizationService
from ambient_edge_server.services.event_service import EventService
from ambient_edge_server.services.interface_service import InterfaceService


class HealthService(ABC):
    @abstractmethod
    async def start(self):
        """Start the service."""

    @abstractmethod
    async def stop(self):
        """Stop the service."""

    @abstractmethod
    async def get_health(self) -> str:
        """Get the health of the service."""

    @abstractmethod
    async def run_system_sweep(self) -> str:
        """Run a system sweep and update backend with results."""

    @property
    @abstractmethod
    def interval_min(self) -> int:
        """Get the interval in minutes for the system sweep."""


class LinuxHealthService(HealthService):
    def __init__(
        self,
        node_repo: NodeRepo,
        event_service: EventService,
        auth_service: AuthorizationService,
        interface_service: InterfaceService,
        docker_repo: DockerRepo,
        interval_minutes: int = 5,
    ):
        self.node_repo = node_repo
        self.event_service = event_service
        self.auth_service = auth_service
        self.interface_service = interface_service
        self.docker_repo = docker_repo
        self._interval_min_ = interval_minutes

        self.api_config: Optional[Configuration] = None
        self._running = False
        self._tasks: Set[asyncio.Task] = set()

    async def start(self, api_config: Configuration):
        self.api_config = api_config
        self._running = True
        sys_sweep_task = asyncio.create_task(self._system_sweep_task())
        sys_sweep_task.add_done_callback(self._handleDoneTask)
        self._tasks.add(sys_sweep_task)

    async def stop(self):
        self._running = False
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()

    async def get_health(self) -> Result[str, str]:
        if not self._running:
            return Err("Service not running")
        if len(self._tasks) == 0:
            return Err("No health tasks running")
        return Ok("OK")

    async def run_system_sweep(self) -> Result[str, str]:
        """Run a system sweep

        Workflow:
            - Check health of the system
            - Check if event service is running
            - Check if node is authorized with backend

        Returns:
            Result[str, str]: Ok if system sweep completed successfully.
        """
        logger.info("Running system sweep ...")
        self_health_result = await self.get_health()
        logger.debug("self_health_result: {}", self_health_result)
        if self_health_result.is_err():
            logger.error(
                "Health check failed. Error: {}", self_health_result.unwrap_err()
            )
            return Err("Health check failed")

        if not self.event_service.is_running or self.event_service.error:
            logger.error(
                "Event service not running or in error state.\n\
  is_running: {}\n    error: {}",
                self.event_service.is_running,
                self.event_service.error,
            )
            return Err("Event service not running or in error state")

        if (await self.auth_service.verify_authorization_status()).is_err():
            logger.error("Node is not authorized with backend")
            return Err("Node is not authorized with backend")

        logger.info("Core system sweep completed successfully")

        logger.info("Running plugin system sweep ...")
        try:
            node = self.node_repo.get_node_data()
            await trigger_system_sweep_hook(
                plugin_manager=self.event_service.plugin_manager, node=node
            )
        except Exception as e:
            logger.error("Failed to run plugin system sweep: {}", e)

        return Ok("System sweep completed successfully")

    @property
    def interval_min(self) -> int:
        return self._interval_min_

    def _get_api_session(self) -> ApiClient:
        if not self.api_config:
            raise ValueError("API Configuration not set")
        return ApiClient(configuration=self.api_config)

    async def _system_sweep_task(self):
        while True:
            try:
                logger.debug("waiting for system sweep interval delay ... ")
                await asyncio.sleep(self._interval_min_ * 60)
                logger.debug("running system sweep ...")
                result = await self.run_system_sweep()
            except Exception as e:
                logger.error("error running system sweep: {}", str(e))
                result = Err(str(e))
            finally:
                logger.info("result of system sweep: {}", result)
                logger.debug("handling system sweep result ...")
                await self._handle_system_sweep_result(result)

    async def trigger_check_in(self):
        result = await self.run_system_sweep()
        await self._handle_system_sweep_result(result)

    async def _handle_system_sweep_result(self, result: Result[str, str]):
        """Handle the result of the system sweep

        This is the meat and potatoes of collecting the system information
        and updating the backend with the results.

        Args:
            result (Result[str, str]): Result of the system sweep.
        """
        logger.info("Handling system sweep result ...")
        last_seen = datetime.datetime.now().isoformat()
        logger.debug("last_seen: {}", last_seen)
        current_interfaces = await self.interface_service.get_network_interfaces()
        logger.debug("Found {} interfaces", len(current_interfaces))
        interfaces = [i.model_dump_json(indent=4) for i in current_interfaces]
        docker_info = self.docker_repo.get_docker_info()
        node_docker_info = None
        if docker_info.Swarm.Cluster:
            node_docker_info = DockerSwarmInfo(
                NodeID=docker_info.Swarm.NodeID,
                NodeAddr=docker_info.Swarm.NodeAddr,
                LocalNodeState=docker_info.Swarm.LocalNodeState,
                Error=docker_info.Swarm.Error,
            )
        if result.is_ok():
            logger.debug("updating backend with system sweep results ...")
            await self._patch_node(
                {
                    "last_seen": last_seen,
                    "status": "active",
                    "interfaces": interfaces,
                    "docker_swarm_info": (
                        node_docker_info.model_dump() if node_docker_info else None
                    ),
                }
            )
        else:
            await self._patch_node(
                {
                    "last_seen": last_seen,
                    "status": "error",
                    "error": result.unwrap_err(),
                    "interfaces": interfaces,
                }
            )

    async def _patch_node(self, data: Dict[str, Any]) -> Result[str, str]:
        async def __patch_node():
            logger.debug("in __patch_node ...")
            async with aiohttp.ClientSession() as session:
                async with session.patch(
                    f"{self.api_config.host}/nodes/{node_id}",
                    json=data,
                    headers={
                        "Authorization": f"Bearer {await self.auth_service.get_token()}"
                    },
                ) as response:
                    resp_text = None
                    try:
                        resp_text = await response.text()
                        response.raise_for_status()
                        updated_node_d = json.loads(resp_text)
                        updated_node = Node.model_validate(updated_node_d)
                        logger.debug(
                            "Node patched: {}", updated_node.model_dump_json(indent=4)
                        )
                        self.node_repo.save_node_data(updated_node)
                    except Exception as e:
                        logger.error(
                            "Failed to patch node: {}\nresponse: {}", e, resp_text
                        )
                        raise e

        logger.info("Patching node with data: {}", json.dumps(data, indent=4))
        node_id = self.node_repo.get_node_id()
        logger.debug("Node ID: {}", node_id)

        try:
            await __patch_node()
            return Ok("Node patched successfully")
        except aiohttp.ClientResponseError as e:
            # if unauthorized (401) then refresh token and retry
            if e.status == 401:
                logger.debug("Unauthorized, refreshing token ...")
                refresh_result = await self.auth_service.refresh_token()
                if refresh_result.is_err():
                    logger.error(
                        "Failed to refresh token: {}", refresh_result.unwrap_err()
                    )
                    return Err("Failed to refresh token")
                logger.debug("Token refreshed, retrying patch ...")
                await __patch_node()
                return Ok("Node patched successfully")
        except Exception as e:
            err_msg = f"Failed to patch node: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    def _handleDoneTask(self, task: asyncio.Task):
        logger.debug("Handling task completion ...")
        self._tasks.remove(task)
        sys_sweep_task = asyncio.create_task(self._system_sweep_task())
        sys_sweep_task.add_done_callback(self._handleDoneTask)
        self._tasks.add(sys_sweep_task)


async def trigger_system_sweep_hook(plugin_manager: pluggy.PluginManager, node: Node):
    logger.debug("triggering system sweep hook ...")
    results = await plugin_manager.ahook.run_system_sweep(node=node)
    logger.debug("system sweep hook results: {}", results)
