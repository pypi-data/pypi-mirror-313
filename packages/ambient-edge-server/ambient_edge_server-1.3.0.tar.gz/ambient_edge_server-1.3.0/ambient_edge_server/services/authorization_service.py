from typing import Optional, Union

import aiohttp
from ambient_backend_api_client import ApiClient, Configuration
from ambient_backend_api_client import NodeOutput as Node
from ambient_backend_api_client import NodesApi, PingApi, TokenResponse
from async_lru import alru_cache
from result import Err, Ok, Result

from ambient_client_common.repositories.node_repo import NodeRepo
from ambient_client_common.utils import logger
from ambient_edge_server.config import settings
from ambient_edge_server.repos.token_repo import TokenRepository


class AuthorizationService:
    def __init__(self, token_repo: TokenRepository, node_repo: NodeRepo) -> None:
        self.token_repo = token_repo
        self.node_repo = node_repo
        self._node_id = None

    @alru_cache(maxsize=1, ttl=3600)
    async def get_token(self) -> Union[str, None]:
        logger.debug("node_id: {}", self.node_id)
        if not self.node_id:
            result = await self.fetch_node()
            logger.debug("result: {}", result)
            if result.is_err():
                logger.error("Error fetching node: {}", result.unwrap_err())
                return None
            self.node_id = result.unwrap().id
        refresh_result = await self.refresh_token()
        if refresh_result.is_err():
            logger.error("Error refreshing token: {}", refresh_result.unwrap_err())
            return None
        return self.token_repo.get_access_token().strip("\n")

    async def verify_authorization_status(self) -> Result[str, str]:
        logger.info("verifying authorization status ...")
        if not self.token_repo.get_access_token():
            logger.error("No access token found in token repo")
            return Err("No access token found in token repo")
        return await self.test_authorization()

    async def fetch_node(self, refresh: bool = False) -> Result[Node, str]:
        if not refresh:
            node = self.node_repo.get_node_data()
            if node:
                logger.debug("node: {}", node.model_dump_json(indent=4))
                return Ok(node)
        node_id = self.node_repo.get_node_id()
        if not node_id:
            return Err("Node not found")
        logger.info("fetching node {} ...", node_id)
        try:
            async with ApiClient(self.api_config) as api_client:
                nodes_api = NodesApi(api_client)
                logger.debug("node_id: {}", node_id)
                if not node_id:
                    return Err("Node ID not found")
                node = await nodes_api.get_node_nodes_node_id_get(node_id=int(node_id))
                logger.debug("node: {}", node.model_dump_json(indent=4))
                self.node_repo.save_node_data(node=node)
                self.node_id = node.id
                return Ok(node)
        except Exception as e:
            err_msg = f"Error fetching node: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    async def authorize_node(self, node_id: str, refresh_token: str) -> None:
        self.node_id = node_id
        async with aiohttp.ClientSession() as session:
            url = settings.backend_api_url
            async with session.post(
                f"{url}/nodes/{node_id}/authorize?refresh_token={refresh_token}"
            ) as response:
                response.raise_for_status()
                token_response = TokenResponse.model_validate(await response.json())
                logger.debug(
                    "token_response: {}", token_response.model_dump_json(indent=4)
                )
                self.token_repo.save_access_token(token_response.access_token)
                self.token_repo.save_refresh_token(token_response.refresh_token)

        await self.get_and_save_node_data(
            node_id=int(node_id), token=token_response.access_token
        )

    async def get_and_save_node_data(
        self, node_id: int, token: str = ""
    ) -> Result[Node, str]:
        logger.info("fetching node {} ...", node_id)
        try:
            async with aiohttp.ClientSession() as session:
                url = settings.backend_api_url
                if not token:
                    token = await self.get_token()
                headers = {"Authorization": f"Bearer {token}"}
                async with session.get(
                    f"{url}/nodes/{node_id}", headers=headers
                ) as response:
                    response.raise_for_status()
                    node = Node.model_validate(await response.json())
                    logger.debug("node: {}", node.model_dump_json(indent=4))
                    self.node_repo.save_node_data(node=node)
                    self.node_id = node.id
                    return Ok(node)
        except Exception as e:
            err_msg = f"Error fetching node: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    async def refresh_token(self) -> Result[None, str]:
        logger.info("refreshing token ...")
        refresh_token = self.token_repo.get_refresh_token()
        if not refresh_token:
            return Err("Refresh token not found")
        logger.debug("refresh_token: {}", refresh_token)
        logger.debug("node_id: {}", self.node_id)
        resp_text: Optional[str] = None
        request_url = f"{settings.backend_api_url}/auth/token?refresh_token\
={refresh_token}"
        logger.debug("request_url: {}", request_url)
        async with aiohttp.ClientSession() as session:
            async with session.post(request_url) as response:
                try:
                    resp_text = await response.text()
                    response.raise_for_status()
                    token_response = TokenResponse.model_validate(await response.json())
                    logger.debug(
                        "token_response: {}", token_response.model_dump_json(indent=4)
                    )
                    self.token_repo.save_access_token(token_response.access_token)
                    self.token_repo.save_refresh_token(token_response.refresh_token)
                    return Ok(None)
                except aiohttp.ClientResponseError as e:
                    logger.error(f"Failed to refresh token: {e}")
                    logger.error(f"response: {resp_text}")
                    return Err(f"Failed to refresh token: {e}")
                except Exception as e:
                    logger.error(f"Failed to refresh token: {e}")
                    logger.error(f"response: {resp_text}")
                    return Err(f"Failed to refresh token: {e}")

    async def create_new_refresh_token(self) -> Result[str, str]:
        logger.info("creating refresh token ...")
        node_data = self.node_repo.get_node_data()
        resp_text: Optional[str] = None
        try:
            headers = {"Authorization": f"Bearer {await self.get_token()}"}
            logger.debug("headers: {}", headers)
            url = settings.backend_api_url
            data = {
                "token_type": "refresh",
                "duration": 3600,
                "user_id": node_data.user_id,
                "org_id": node_data.org_id,
                "node_id": node_data.id,
                "request_type": "node_refresh_token",
            }
            logger.debug("data: {}", data)
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{url}/auth/token-mgmt/", headers=headers, data=data
                ) as response:
                    resp_text = await response.text()
                    logger.debug("response: {}", resp_text)
                    response.raise_for_status()
                    token_response = TokenResponse.model_validate(await response.json())
                    logger.debug(
                        "token_response: {}", token_response.model_dump_json(indent=4)
                    )
                    self.token_repo.save_access_token(token_response.access_token)
                    self.token_repo.save_refresh_token(token_response.refresh_token)
                    return Ok("Refresh token created")
        except Exception as e:
            err_msg = f"Failed to create refresh token: {e}"
            if resp_text:
                err_msg += f"\nresponse: {resp_text}"
            logger.error(err_msg)
            return Err(err_msg)

    async def test_authorization(self) -> Result[str, str]:
        logger.info("testing authorization ...")
        try:
            logger.info("pinging backend ...")
            async with ApiClient(self.api_config) as api_client:
                ping_api = PingApi(api_client)
                pong = await ping_api.auth_ping_auth_ping_get()
                logger.debug("pong: {}", pong)
                logger.info("Authorized")
                return Ok("Authorized")
        except Exception as e:
            logger.error("Error: {}", e)
            return Err("Unauthorized")

    @property
    def node_id(self) -> str:
        return self._node_id

    @node_id.setter
    def node_id(self, value: str) -> None:
        self._node_id = value

    @property
    def api_config(self) -> Configuration:
        return Configuration(
            host=settings.backend_api_url,
            access_token=self.token_repo.get_access_token(),
        )
