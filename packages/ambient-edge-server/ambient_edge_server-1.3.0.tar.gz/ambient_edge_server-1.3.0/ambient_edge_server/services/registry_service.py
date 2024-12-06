import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import docker
import websockets
from ambient_backend_api_client import (
    ApiClient,
    Configuration,
    ContainerRegistry,
    ContainerRegistryAuth,
    ContainerRegistryType,
    RegistriesApi,
)
from cryptography.fernet import Fernet
from result import Err, Ok, Result

from ambient_client_common.utils import logger
from ambient_edge_server import config
from ambient_edge_server.services.authorization_service import AuthorizationService


class RegistryService(ABC):
    @abstractmethod
    async def authorize(self, ws_session: str) -> Result[None, str]:
        """
        Authorize the registry.

        Args:
            ws_session (str): Websocket session
            registry_type (ContainerRegistryType): Registry type

        Returns:
            Result[None, str]: Ok if authorized, Err otherwise
        """
        raise NotImplementedError("Method not implemented")


class RegistryServiceBase:
    """A base class for registry service to perform repeated tasks"""

    def __init__(self, auth_svc: AuthorizationService) -> None:
        super().__init__()
        self.auth_svc = auth_svc
        logger.debug("RegistryServiceBase initialized.")
        self.api_config: Optional[Configuration] = None

    async def init(self) -> None:
        self.api_config = Configuration(
            host=config.settings.backend_api_url,
            access_token=await self.auth_svc.get_token(),
        )

    async def _get_registry(self, registry_id: int) -> ContainerRegistry:
        """Get Container Registry from API

        Args:
            registry_id (int): Registry ID

        Returns:
            ContainerRegistry: ContainerRegistry object
        """
        async with ApiClient(self.api_config) as api_client:
            logger.debug("RegistryServiceBase._get_registry() - within async context")
            registries_api = RegistriesApi(api_client)
            logger.info(
                "Making request to backend API with registry ID: {}", registry_id
            )
            return await registries_api.get_registry_registries_registry_id_get_0(
                registry_id=registry_id
            )

    async def _get_registry_creds(self, creds_id: int) -> ContainerRegistryAuth:
        """Get Container Registry Auth from API

        Args:
            creds_id (int): Credentials ID

        Returns:
            ContainerRegistryAuth: ContainerRegistryAuth object
        """
        async with ApiClient(self.api_config) as api_client:
            logger.debug(
                "RegistryServiceBase._get_registry_creds() - within async context"
            )
            registries_api = RegistriesApi(api_client)
            logger.info("Making request to backend API with creds ID: {}", creds_id)
            return await registries_api.get_registry_auth_cred_registries_creds_creds_id_get(  # noqa
                creds_id=creds_id
            )

    async def _decrypt_password(self, creds: ContainerRegistryAuth) -> str:
        """Decrypt the password

        Args:
            creds (ContainerRegistryAuth): ContainerRegistryAuth object

        Returns:
            str: Decrypted password
        """
        logger.info("Decrypting password ...")
        encrypted_password = creds.password.encode("utf-8")
        logger.debug(
            "RegistryServiceBase._decrypt_password() - encrypted password encoded [ {} chars ]",  # noqa
            len(encrypted_password),
        )
        cipher_suite: Fernet = self.auth_svc.get_cipher_suite()
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode("utf-8")
        logger.debug(
            "RegistryServiceBase._decrypt_password() - decrypted password [ {} chars ]",
            len(decrypted_password),
        )
        logger.info("Password decrypted successfully")
        return decrypted_password


class DockerRegistryService(RegistryService, RegistryServiceBase):
    def __init__(self, docker_client: docker.DockerClient, **kwargs) -> None:
        super().__init__(**kwargs)
        self.docker_client = docker_client
        logger.debug("DockerRegistryService initialized.")

    async def authorize(self, ws_session: str) -> Result[None, str]:
        """
        Authorize the registry.

        Args:
            ws_session (str): Websocket session
            registry_type (ContainerRegistryType): Registry type

        Returns:
            Result[None, str]: Ok if authorized, Err otherwise
        """
        logger.info("Authorizing to registry ...")
        logger.debug("DockerRegistryService.authorize() - ws_session: {}", ws_session)
        try:
            # connect to ws session
            async with websockets.connect(ws_session) as ws:
                logger.info("connected to web socket session")
                # send token
                token = await self.auth_svc.get_token()
                await ws.send(token)
                logger.info("authorized web socket session")

                # receive registry auth data
                auth_msg = await ws.recv()
                logger.debug(
                    "DockerRegistryService.authorize() - auth_msg: {}", auth_msg
                )
                auth_data: dict = json.loads(auth_msg)
                logger.debug(
                    "DockerRegistryService.authorize() - auth_data contains [ {} ] keys",  # noqa
                    len(auth_data.keys()),
                )
                creds_id = auth_data.get("creds_id", None)
                logger.info("Authorizing using credentials: {}", creds_id)
                if creds_id is None:
                    logger.error("creds_id not found in auth data")
                    return Err("creds_id not found in auth data")
                creds = await self._get_registry_creds(creds_id)
                logger.info("Got credentials for registry: {}", creds.registry_id)
                logger.debug(
                    "DockerRegistryService.authorize() - creds: {}",
                    creds.model_dump_json(indent=4),
                )
                registry = await self._get_registry(registry_id=creds.registry_id)
                logger.info("Got registry: {}", registry.id)
                logger.debug(
                    "DockerRegistryService.authorize() - registry: {}",
                    registry.model_dump_json(indent=4),
                )

                # send "ack"
                await ws.send("ack")
                logger.info("Acknowledged the auth request")

                # authorize to registry using the docker client
                url = registry.url
                username = creds.username
                logger.info(
                    "Authentication to registry @ [ {} ] using username: {} ...",
                    url,
                    username,
                )
                password = await self._decrypt_password(creds)
                logger.debug("DockerRegistryService.authorize() - password decrypted.")
                result = await self._docker_login(url, username, password)
                del password
                logger.debug("DockerRegistryService.authorize() - password deleted.")
                if result.is_err():
                    return result
                logger.info("Authenticated to registry [ {} ] successfully", url)

                # send "completed" message
                await ws.send("completed")
                logger.info("backend notified about successful authorization")

                # successful authorization
                logger.debug("DockerRegistryService.authorize() - returning Ok object")
                return Ok(None)
        except Exception as e:
            error_msg = f"Failed to authorize to registry: {e}"
            logger.error(error_msg)
            return Err(error_msg)

    async def _docker_login(
        self, url: str, username: str, password: str
    ) -> Result[Dict[Any, Any], str]:
        """Login to the docker registry.

        Args:
            url (str): URL of the registry
            username (str): username
            password (str): password (already decrypted)

        Returns:
            Result[Dict[Any, Any], str]: The authenticatoin response
        """
        try:
            logger.debug(
                "DockerRegistryService._docker_login() - url: {}, username: {}",
                url,
                username,
            )
            login_resp = self.docker_client.login(
                username=username, password=password, registry=url
            )
            logger.debug(
                "DockerRegistryService._docker_login() - login_resp: {}", login_resp
            )
            return Ok(login_resp)
        except docker.errors.APIError as e:
            error_msg = f"Failed to authenticate to registry (Docker API Error): {e}"
            logger.error(error_msg)
            return Err(error_msg)
        except Exception as e:
            error_msg = f"Failed to authenticate to registry: {e}"
            logger.error(error_msg)
            return Err(error_msg)


class RegistryServiceFactory:
    def __init__(
        self,
        docker_client: docker.DockerClient,
        auth_svc: AuthorizationService,
    ) -> None:
        base_kwargs = {
            "auth_svc": auth_svc,
        }
        self.docker_registry_service = DockerRegistryService(
            docker_client=docker_client, **base_kwargs
        )

    async def init(self):
        await self.docker_registry_service.init()

    def get_registry_service(
        self, registry_type: ContainerRegistryType
    ) -> RegistryService:
        if registry_type == ContainerRegistryType.DOCKER_HUB:
            return self.docker_registry_service
        else:
            raise NotImplementedError(f"Registry type {registry_type} not supported")
