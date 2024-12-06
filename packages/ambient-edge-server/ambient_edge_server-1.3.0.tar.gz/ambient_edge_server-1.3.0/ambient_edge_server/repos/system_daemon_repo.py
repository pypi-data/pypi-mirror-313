from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from result import Err, Ok, Result

from ambient_client_common.utils import logger
from ambient_edge_server.config import settings
from ambient_edge_server.models.system_service import (
    ServiceConfigBase,
    ServiceConfigLinux,
)


class SystemDaemonRepo(ABC):
    @abstractmethod
    async def render_template_and_save(
        self, service_config: ServiceConfigBase, output_path: Path
    ) -> Result[str, str]:
        """Render the service template and save it to the output path."""

    @abstractmethod
    async def render_template_dry_run(
        self, service_config: ServiceConfigBase
    ) -> Result[str, str]:
        """Render the service template without saving it to disk."""

    @abstractmethod
    async def _render_service_template(
        self, service_config: ServiceConfigBase
    ) -> Result[str, str]:
        """Render the service template."""


class LinuxSystemDaemonRepo(SystemDaemonRepo):
    def __init__(self):
        package_location = Path(__file__).parent.parent
        logger.debug("app.startup() - __file__: {}", __file__)
        logger.debug("app.startup() - package location: {}", package_location)
        self.template_path = package_location / settings.service_template_location
        if not self.template_path.exists():
            logger.warning("Template path does not exist: {}", self.template_path)
        logger.debug("template: {}", self.template_path.absolute())

    async def _render_service_template(
        self, service_config: ServiceConfigLinux
    ) -> Result[str, str]:
        logger.debug("Rendering service template")
        try:
            loader_path = self.template_path.absolute().parent
            logger.debug("Template path: {}", loader_path)
            loader = FileSystemLoader(loader_path)
            logger.debug("Loader: {}", loader.list_templates())
            env = Environment(loader=loader, autoescape=True)
            logger.debug("Environment: {}", env)
            try:
                template = env.get_template("ambient_edge_server.service.jinja2")
            except TemplateNotFound as e:
                logger.error("Template not found: {}", e)
                return Err(str(e))
            logger.debug("Template: {}", template)

            logger.debug(
                "LinuxSystemDaemonRepo._render_service_template - service: {}",
                service_config.model_dump_json(indent=4),
            )
            rendered_content = template.render(service=service_config.model_dump())
            logger.debug(
                "LinuxSystemDaemonRepo._render_service_template - Rendered content: {}",
                rendered_content,
            )
            return Ok(rendered_content)
        except Exception as e:
            logger.error(
                "Failed to render service template: {}", e.with_traceback(None)
            )
            return Err(str(e))

    async def render_template_and_save(
        self,
        service_config: ServiceConfigLinux,
        output_path: Path = Path("/etc/systemd/system/ambient_edge_server.service"),
    ) -> Result[str, str]:
        logger.info(
            "Rendering service template and saving to {}", output_path.absolute()
        )
        try:
            rendered_content = await self._render_service_template(service_config)
            if rendered_content.is_err():
                return rendered_content
            logger.debug("Rendered content: {}", rendered_content)
            output_path.write_text(rendered_content.unwrap())
        except Exception as e:
            logger.error("Failed to render service template: {}", e)
            return Err(str(e))
        finally:
            logger.info("Template saved to {}", output_path.absolute())
            return Ok(f"Template saved to {output_path.absolute()}")

    async def render_template_dry_run(
        self, service_config: ServiceConfigLinux
    ) -> Result[str, str]:
        logger.debug("Rendering service template in dry run mode")
        return await self._render_service_template(service_config)
