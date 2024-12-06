import os
import subprocess
import sys
from typing import Dict, List

import aiohttp

from ambient_client_common.utils import logger
from ambient_edge_server import config


class UpgradeService:
    async def get_software_versions(self) -> List[Dict[str, str]]:
        resp_text = ""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{config.settings.backend_api_url}/upgrade_software/versions"
                ) as response:
                    resp_text = await response.text()
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            err_msg = "Error getting software versions. Error"
            if resp_text:
                err_msg += f" response: {resp_text}"
            else:
                err_msg += f": {e}"
            logger.error(err_msg)
            raise Exception(err_msg) from e

    def upgrade_software(self, version: str) -> str:
        result = None
        for package in config.settings.required_packages:
            server_env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", f"{package}=={version}"],
                env=server_env,
                capture_output=True,
            )
            if result.returncode != 0:
                err_msg = f"Failed to install package {package}. Error: {result.stderr}"
                logger.error(err_msg)
            logger.info(f"Successfully installed package {package}")

    async def upgrade_to_latest(self) -> str:
        logger.info("Upgrading to latest version ...")
        versions = await self.get_software_versions()
        logger.debug(f"Versions: {versions}")
        target = "prod"
        if config.settings.ambient_dev_mode:
            target = "dev"
        logger.debug(f"Target: {target}")
        latest_version = next(
            data.get("version", None)
            for data in versions
            if data.get("target", None) == target
        )
        logger.debug(f"Latest version: {latest_version}")
        if not latest_version:
            logger.error("No version found for target")
            raise Exception("No version found for target")
        logger.info(f"Upgrading to version {latest_version}")
        self.upgrade_software(latest_version)
        logger.info(f"Successfully upgraded to version {latest_version}")
        return latest_version
