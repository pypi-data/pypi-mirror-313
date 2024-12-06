"""Plugin to cascade through various collectors to try to capture an artifact."""

from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from hoppr import __version__, constants
from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_ignore_excluded, hoppr_process
from hoppr.exceptions import HopprPluginError
from hoppr.models.transfer import ComponentCoverage
from hoppr.result import Result
from hoppr.utils import plugin_class, plugin_instance

if TYPE_CHECKING:
    from hoppr.models import HopprContext
    from hoppr.models.sbom import Component


class CompositeCollector(HopprPlugin, default_component_coverage=ComponentCoverage.EXACTLY_ONCE):
    """Plugin to cascade through various collectors to try to capture an artifact."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        if self.config is None:
            raise HopprPluginError("CompositeCollector requires configuration be defined in the transfer config file")

        if (
            constants.ConfigKeys.PLUGINS not in self.config
            or not isinstance(self.config[constants.ConfigKeys.PLUGINS], list)
            or len(self.config[constants.ConfigKeys.PLUGINS]) == 0
        ):
            raise HopprPluginError("CompositeCollector requires at least one plugin be configured")

        self.child_plugins: list[HopprPlugin] = []

        for plugin_spec in self.config[constants.ConfigKeys.PLUGINS]:
            plugin = plugin_instance(plugin_spec["name"], context, plugin_spec.get(constants.ConfigKeys.CONFIG))
            self.child_plugins.append(plugin)

    @hoppr_process
    def pre_stage_process(self) -> Result:
        """Run all child plugin pre-stage processes."""
        for plugin in self.child_plugins:
            result = plugin.pre_stage_process()
            if result.is_fail() or result.is_retry():
                return Result.fail(f"Failure running {type(plugin).__name__}")

        return Result.success()

    @hoppr_ignore_excluded
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """Run component through each child plugin component processes."""
        for plugin in self.child_plugins:
            self._log_and_flush("Attempting to process %s using %s", comp.purl, type(plugin).__name__)

            result = plugin.process_component(comp)
            if result.is_success():
                return Result.success(f"Used {type(plugin).__name__}")

        return Result.fail(f"Failed to run component {comp.purl} through all child plugins.")

    @hoppr_process
    def post_stage_process(self) -> Result:
        """Run all child plugin post-stage processes."""
        for plugin in self.child_plugins:
            msg = f"Running post stage process for {type(plugin).__name__}"
            self.get_logger().info(msg)
            self.notify(msg, type(self).__name__)

            result = plugin.post_stage_process()

            if result.is_fail() or result.is_retry():
                return Result.fail(f"Failure running {type(plugin).__name__}")

        return Result.success()

    def _log_and_flush(self, msg: str, *args, level: int = logging.INFO, indent_level: int = 0):
        self.get_logger().log(level, msg, *args, indent_level=indent_level)
        self.get_logger().flush()

    def supports_purl_type(self, purl_type: str) -> bool:
        """Composite collector purl type support is based on first child collector."""
        return self.child_plugins[0].supports_purl_type(purl_type)

    @classmethod
    def get_attestation_products(cls, config: dict | None = None) -> list[str]:
        """Return a list of attestation products for this class."""
        if (
            config is None
            or constants.ConfigKeys.PLUGINS not in config
            or not isinstance(config[constants.ConfigKeys.PLUGINS], list)
            or len(config[constants.ConfigKeys.PLUGINS]) == 0
        ):
            raise HopprPluginError("CompositeCollector requires at least one plugin be configured")

        plugin_cls = plugin_class(config[constants.ConfigKeys.PLUGINS][0]["name"])
        plugin_config = config[constants.ConfigKeys.PLUGINS][0].get(constants.ConfigKeys.CONFIG)

        return plugin_cls.get_attestation_products(plugin_config)
