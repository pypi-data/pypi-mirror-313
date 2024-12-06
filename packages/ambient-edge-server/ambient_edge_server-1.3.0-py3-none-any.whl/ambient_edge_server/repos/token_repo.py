from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from cryptography.fernet import Fernet

from ambient_client_common.utils import hash_string, logger


class TokenRepository(ABC):
    @abstractmethod
    def save_access_token(self, token: str) -> None:
        """Save the access token to the repository.

        Args:
            token (str): JWT access token
        """

    @abstractmethod
    def get_access_token(self) -> str:
        """Get the access token from the repository.

        Returns:
            str: JWT access token
        """

    @abstractmethod
    def save_refresh_token(self, token: str) -> None:
        """Save the refresh token to the repository.

        Args:
            token (str): JWT refresh token
        """

    @abstractmethod
    def get_refresh_token(self) -> str:
        """Get the refresh token from the repository.

        Returns:
            str: JWT refresh token
        """


class EncryptedTokenRepository(TokenRepository):
    def __init__(self, key: Optional[str] = None):
        self.key = key or Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.home_path = Path.home() / ".ambient"
        self.access_token_path = self.home_path / ".access_token.enc"
        self.refresh_token_path = self.home_path / ".refresh_token.enc"
        self.fernet_key_path = self.home_path / f".{hash_string('fernet_key')}"

        self._init_files()

    def _init_files(self):
        self.home_path.mkdir(parents=True, exist_ok=True, mode=0o700)

        if not self.access_token_path.exists():
            logger.debug("creating access token file ...")
            self._write_to_file(self.access_token_path, b"")

        if not self.refresh_token_path.exists():
            logger.debug("creating refresh token file ...")
            self._write_to_file(self.refresh_token_path, b"")

        if not self.fernet_key_path.exists():
            logger.debug("creating fernet key file ...")
            self._write_to_file(self.fernet_key_path, self.key)
        else:
            logger.debug("reading fernet key file ...")
            self.key = self._read_from_file(self.fernet_key_path)
            self.cipher_suite = Fernet(self.key)

    def _write_to_file(self, path: Path, data: bytes):
        with path.open("wb") as file:
            path.chmod(0o600)
            file.write(data)

    def _read_from_file(self, path: Path) -> bytes:
        if not path.exists():
            logger.warning(f"File not found: {path}")
            return b""
        with path.open("rb") as file:
            return file.read()

    def save_access_token(self, token: str):
        encrypted_token = self.cipher_suite.encrypt(token.encode())
        self._write_to_file(self.access_token_path, encrypted_token)

    def get_access_token(self) -> Union[str, None]:
        encrypted_token = self._read_from_file(self.access_token_path)
        if not encrypted_token:
            return None
        return self.cipher_suite.decrypt(encrypted_token).decode()

    def save_refresh_token(self, token: str):
        encrypted_token = self.cipher_suite.encrypt(token.encode())
        self._write_to_file(self.refresh_token_path, encrypted_token)

    def get_refresh_token(self) -> str:
        logger.debug("reading refresh token ...")
        encrypted_token = self._read_from_file(self.refresh_token_path)
        if not encrypted_token:
            return ""
        return self.cipher_suite.decrypt(encrypted_token).decode()
