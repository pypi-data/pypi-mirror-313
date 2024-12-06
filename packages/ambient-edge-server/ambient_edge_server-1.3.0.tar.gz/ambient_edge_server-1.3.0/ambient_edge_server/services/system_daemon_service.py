import asyncio
import getpass
import grp
import os
import pwd
import subprocess
from abc import ABC, abstractmethod
from typing import Optional, Set, Union

from result import Err, Ok, Result

from ambient_client_common.utils import logger
from ambient_edge_server import config
from ambient_edge_server.models.system_service import (
    ServiceConfigBase,
    ServiceConfigLinux,
)
from ambient_edge_server.repos.system_daemon_repo import SystemDaemonRepo


class SystemDaemonService(ABC):
    @abstractmethod
    async def install(self) -> Union[None, Err[str]]:
        """Initialize the service."""

    @abstractmethod
    async def save_config(self) -> Result[str, str]:
        """Save the service to the system."""

    @abstractmethod
    async def start(self) -> Result[str, str]:
        """Start the service."""

    @abstractmethod
    async def stop(self) -> Result[str, str]:
        """Stop the service."""

    @abstractmethod
    async def restart(self) -> Result[str, str]:
        """Restart the service."""

    @property
    @abstractmethod
    def status(self) -> Result[str, str]:
        """Get the status of the service.

        Returns:
            Result[str, str]: The status of the service.
                Ok if the service is running.
                Err if the service is not running.
        """

    @property
    @abstractmethod
    def service_config(self) -> ServiceConfigBase:
        """Return the service configuration."""


class LinuxDaemonService(SystemDaemonService):
    def __init__(self, system_daemon_repo: SystemDaemonRepo):
        self.system_daemon_repo = system_daemon_repo
        self._service_config: ServiceConfigLinux = self.build_service_config()
        self.tasks: Set[asyncio.Task] = set()

    async def install(self, env_vars: Optional[dict] = None) -> Optional[Err[str]]:
        """
        This should only be called once when the service is first installed
        on the system. It will render the service configuration and save it to
        the system. It exits upon completion.
        """

        logger.info("starting the installation process ...")
        if env_vars:
            logger.info("Env vars requested, adding to _service_config ...")
            _temp_service_config = self.service_config
            _temp_service_config.environment = env_vars
            self.service_config = _temp_service_config
            logger.debug(
                "LinuxDaemonService.install() - _temp_service_config: {}",
                _temp_service_config,
            )
        save_config_result = await self.save_config()
        if save_config_result.is_err():
            logger.error(
                "Failed to save the configuration: {}", save_config_result.err()
            )
            return Err(save_config_result.err())
        else:
            logger.info("Configuration saved successfully.")

        start_result = await self.start()
        if start_result.is_err():
            logger.error("Failed to start the service: {}", start_result.err())
            return start_result
        else:
            logger.info("Service started successfully.")

        logger.info("Installation complete. Exiting ...")
        return await self.restart()

    @property
    def service_config(self) -> ServiceConfigLinux:
        return self._service_config

    @service_config.setter
    def service_config(self, value: ServiceConfigLinux):
        self._service_config = value

    async def save_config(self) -> Result[str, str]:
        logger.info("Saving configuration ...")
        logger.debug("service config: {}", self.service_config)

        result: Result = await self.system_daemon_repo.render_template_and_save(
            self.service_config
        )
        if result.is_err():
            logger.error("Failed to save the configuration: {}", result.err())
            return result
        elif result.is_ok():
            logger.info("Configuration saved successfully.")
            return result

    async def start(self) -> Result[str, str]:
        logger.info("Starting the service ...")

        refresh_result = await self._refresh_services()
        if refresh_result.is_err():
            return refresh_result

        return await self._start_service()

    async def stop(self) -> Result[str, str]:
        logger.info("Stopping the service ...")
        try:
            stop_task = asyncio.create_task(
                self._run_systemctl_cmd("stop", delay=config.settings.default_delay)
            )
            logger.debug("LinuxDaemonService.stop() - stop_task: {}", stop_task)
            self.tasks.add(stop_task)
            stop_task.add_done_callback(lambda _: self.tasks.remove(stop_task))
            ok_msg = f"Service will stop in {config.settings.default_delay} seconds ..."
            logger.info(ok_msg)
            return Ok(ok_msg)
        except Exception as e:
            err_msg = f"Failed to stop the service: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    async def restart(self) -> Result[str, str]:
        logger.info("Restarting the service ...")
        try:
            restart_task = asyncio.create_task(
                self._run_systemctl_cmd("restart", delay=config.settings.default_delay)
            )
            logger.debug(
                "LinuxDaemonService.restart() - restart_task: {}", restart_task
            )
            self.tasks.add(restart_task)
            restart_task.add_done_callback(lambda _: self.tasks.remove(restart_task))
            ok_msg = (
                f"Service will restart in {config.settings.default_delay} seconds ..."
            )
            logger.info(ok_msg)
            return Ok(ok_msg)
        except Exception as e:
            err_msg = f"Failed to restart the service: {e}"
            logger.error(err_msg)
            return Err(err_msg)

    @property
    def status(self) -> Result[str, str]:
        cmd = ["systemctl", "status", "ambient_edge_server.service"]

        logger.debug("command: {}", cmd)

        try:
            output = subprocess.run(cmd, capture_output=True, text=True)
            logger.debug("output: {}", output)
            output.check_returncode()
            logger.info("service is running.")
            return Ok("service is running.")
        except subprocess.CalledProcessError as e:
            logger.error("service is not running: {}", e)
            return Err("service is not running.")

    async def _refresh_services(self) -> Result[str, str]:
        refresh_cmd = ["systemctl", "daemon-reload"]

        logger.debug("refreshing services ...")
        logger.debug("cmd: {}", refresh_cmd)

        try:
            output = subprocess.run(refresh_cmd, capture_output=True, text=True)
            logger.debug("output: {}", output)
            output.check_returncode()
            logger.info("services refreshed successfully.")
            return Ok("services refreshed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to refresh services: {}", e)
            return Err("Failed to refresh services.")

    async def _start_service(self) -> Result[str, str]:
        return await self._run_systemctl_cmd("start")

    async def _run_systemctl_cmd(
        self, action: str, delay: Optional[int] = None
    ) -> Result[str, str]:

        cmd = ["systemctl", action, "ambient_edge_server.service"]

        logger.debug("command: {}", cmd)

        if delay:
            logger.info("Waiting {} seconds before running command ...", delay)
            await asyncio.sleep(delay)

        try:
            logger.info("running action: {} ...", action)
            output = subprocess.run(cmd, capture_output=True, text=True)
            logger.debug("output: {}", output)
            output.check_returncode()
            logger.info("action {} completed successfully.", action)
            return Ok(f"action {action} completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error("Failed to complete action: {}", e)
            return Err("Failed to complete action.")

    def build_service_config(
        self, env_vars: Optional[dict] = None
    ) -> ServiceConfigLinux:
        logger.debug("building the service configuration ...")
        user = self.get_user()
        group = self.get_group()

        if env_vars:
            logger.debug(
                "LinuxDaemonService.build_service_config - environment variables: {}",
                env_vars,
            )
        return ServiceConfigLinux(
            user=user,
            group=group,
            environment=env_vars,
        )

    def get_user(self) -> str:
        logger.debug("getting the current user ...")
        username = getpass.getuser()
        logger.info("current user: {}", username)
        return username

    def get_group(self) -> str:
        logger.debug("getting the current group ...")

        uid = os.getuid()
        user_info = pwd.getpwuid(uid)
        primary_gid = user_info.pw_gid

        logger.debug(
            "-> uid: {}\n-> primary_gid: {}\n-> user_info: {}",
            uid,
            primary_gid,
            user_info,
        )

        group_info = grp.getgrgid(primary_gid)
        group_name = group_info.gr_name

        logger.info("current group: {}", group_name)
        logger.debug("-> group_info: {}", group_info)

        return group_name
