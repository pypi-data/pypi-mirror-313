import datetime
import pathlib
from typing import Optional, Union

import aiohttp
from ambient_backend_api_client import ApiClient, Configuration
from ambient_backend_api_client import NodeOutput as Node
from ambient_backend_api_client import NodesApi, PingApi, TokenResponse
from async_lru import alru_cache
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import NameOID
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

    async def cycle_certificate(self) -> Result[str, str]:
        logger.info("cycling certificate ...")

        # prep directories
        private_key_path = pathlib.Path(settings.private_key_file)
        private_key_path.parent.mkdir(parents=True, exist_ok=True)
        certificate_path = pathlib.Path(settings.certificate_file)
        certificate_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info("directories created")

        # generate private key and certificate
        private_key = generate_private_key()
        save_private_key_to_pem(private_key, private_key_path.as_posix())
        logger.info("private key generated")

        # generate csr and self sign certificate
        csr = generate_certificate_signing_request(private_key, self.node_id)
        logger.info("csr generated")
        certificate = self_sign_certificate(csr, private_key)
        logger.info("certificate signed")
        save_certificate_to_pem(certificate, certificate_path.as_posix())
        logger.info("certificate saved")

        # publish certificate to backend
        result = await publish_certificate_to_backend(
            certificate, self.node_id, await self.get_token()
        )
        if result.is_err():
            return result
        logger.info("certificate published")

        return Ok("Certificate cycled successfully")


def generate_private_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def save_private_key_to_pem(private_key: rsa.RSAPrivateKey, file_path: str) -> None:
    with open(file_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def generate_certificate_signing_request(
    private_key: rsa.RSAPrivateKey, node_id: int
) -> x509.CertificateSigningRequest:
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Colorado"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, "Denver"),
                    x509.NameAttribute(
                        NameOID.ORGANIZATION_NAME, "Ambient Labs Computing"
                    ),
                    x509.NameAttribute(NameOID.COMMON_NAME, f"node-{node_id}"),
                ]
            )
        )
        .sign(private_key, hashes.SHA256())
    )
    return csr


def self_sign_certificate(
    csr: x509.CertificateSigningRequest, private_key: rsa.RSAPrivateKey
) -> x509.Certificate:
    certificate = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(csr.subject)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .sign(private_key, hashes.SHA256())
    )
    return certificate


def save_certificate_to_pem(certificate: x509.Certificate, file_path: str) -> None:
    with open(file_path, "wb") as f:
        f.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))


async def publish_certificate_to_backend(
    certificate: x509.Certificate, node_id: int, token: str
) -> Result[str, str]:
    logger.info("publishing certificate to backend ...")
    # use patch to update the node's certificate field with text of certificate
    resp_text: Optional[str] = None
    logger.debug("token: {}", token)
    try:
        async with aiohttp.ClientSession() as session:
            url = settings.backend_api_url
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
            data = {
                "certificate": certificate.public_bytes(
                    encoding=serialization.Encoding.PEM
                ).decode(),
            }
            async with session.patch(
                f"{url}/nodes/{node_id}", headers=headers, json=data
            ) as response:
                resp_text = await response.text()
                response.raise_for_status()
                return Ok("Certificate published to backend")
    except Exception as e:
        err_msg = "Failed to publish certificate to backend"
        if resp_text:
            err_msg += f": {resp_text}"
        else:
            err_msg += f": {e}"
        logger.error(err_msg)
        return Err(err_msg)
