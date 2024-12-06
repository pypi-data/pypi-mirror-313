import pathlib
from typing import Any, Dict, List, Union

import yaml
from ambient_base_plugin import PluginDefinition
from pydantic import ValidationError

from ambient_client_common.utils import logger
from ambient_edge_server.config import settings


class PluginRepo:
    def load_plugins(
        self, extra_plugin_paths: List[pathlib.Path] = []
    ) -> List[PluginDefinition]:
        """Load plugins

        Args:
            extra_plugin_paths (List[pathlib.Path], optional):
                Extra plugin paths. Defaults to [].

        Returns:
            List[PluginDefinition]: List of plugins
        """
        logger.info("Loading plugins ...")
        builtin_plugins = self.get_builtin_plugins()
        logger.debug("Builtin plugins: {}", builtin_plugins)
        extra_plugins = []
        for path in extra_plugin_paths:
            extra_plugins.extend(self.get_plugins_from_path(path))
        logger.debug("Extra plugins: {}", extra_plugins)
        all_plugins = builtin_plugins + extra_plugins
        logger.info("Loaded {} plugins", len(all_plugins))
        return all_plugins

    def get_builtin_plugins(self) -> List[PluginDefinition]:
        """Get builtin plugins

        Returns:
            List[PluginDefinition]: List of builtin plugins
        """
        logger.info("Loading builtin plugins ...")
        logger.debug("Settings package location: {}", settings.package_location)
        builtin_plugins_path = settings.package_location / "builtin_plugins.yml"
        logger.debug("Builtin plugins path: {}", builtin_plugins_path)

        builtin_plugins = self.get_plugins_from_path(builtin_plugins_path)
        logger.info("Loaded {} builtin plugins", len(builtin_plugins))
        return builtin_plugins

    def load_yaml(self, path: pathlib.Path) -> Union[List[Dict[str, Any]], None]:
        """Load a yaml file

        Args:
            path (pathlib.Path): Path to yaml file

        Returns:
            Union[List[Dict[str, Any]], None]: List of dictionaries or None
        """

        try:
            with open(path, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warning("Error loading yaml file: {}", e)
            return None

    def get_plugins_from_path(self, path: pathlib.Path) -> List[PluginDefinition]:
        """Get plugins from a path

        Args:
            path (pathlib.Path): Path to load plugins from

        Returns:
            List[PluginDefinition]: List of plugins
        """

        logger.info("Loading plugins from path: {}", path)
        if not path.exists():
            logger.warning("Path does not exist: {}", path)
            return []
        plugins = self.load_yaml(path)
        if plugins is None:
            logger.warning("No plugins loaded from path: {}")
            return []
        parsed_plugins = []
        for plugin in plugins:
            try:
                parsed_plugins.append(PluginDefinition.model_validate(plugin))
            except ValidationError as e:
                logger.error("Error parsing plugin: {}", e)
        logger.info("Loaded {} plugins from path: {}", len(parsed_plugins), path)
        return parsed_plugins
