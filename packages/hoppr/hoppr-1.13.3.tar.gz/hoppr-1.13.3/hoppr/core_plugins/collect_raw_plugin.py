"""Collector plugin for raw files."""

from __future__ import annotations

import shutil

from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import unquote

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprPluginError
from hoppr.models.types import RepositoryUrl
from hoppr.net import download_file
from hoppr.result import Result

if TYPE_CHECKING:
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


class CollectRawPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["binary", "generic", "raw"],
    products=["binary/*", "generic/*", "raw/*"],
):
    """Collector plugin for raw files."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def _validate_hashes(self, comp: Component, file_location: Path):
        """Validates the component hashes against hashes generated for each component.

        If no conflicting hashes are found, update the component with the generated hashes.

        Args:
            comp: Component object whose hashes will be validated.
            file_location: Path to the file to generate hashes from.

        Raises:
            HopprPluginError: If hash validation fails.
        """
        generated_hashes = self._get_artifact_hashes(file_location)

        try:
            comp.update_hashes(generated_hashes)
        except ValueError as ex:
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.") from ex

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Copy a component to the local collection directory structure."""
        source_url = RepositoryUrl(url=repo_url)

        purl = hoppr.utils.get_package_url(comp.purl)

        subdir = None
        if purl.namespace is not None:
            source_url /= f"{purl.namespace}"
            subdir = unquote(purl.namespace)

        target_dir = self.directory_for(purl.type, repo_url, subdir=subdir)

        file_name = unquote(purl.name)

        if source_url.scheme == "file":
            repo_path = Path(repo_url.removeprefix("file:").removeprefix("//"))
            source_file = (repo_path / (purl.namespace or "") / file_name).expanduser()

            self.get_logger().info(msg="Copying component:", indent_level=2)
            self.get_logger().info(msg=f"source: {source_file}", indent_level=3)
            self.get_logger().info(msg=f"destination: {target_dir.joinpath(file_name)}", indent_level=3)

            if not source_file.is_file():
                msg = f"Unable to locate file {source_file}, skipping remaining attempts"
                self.get_logger().error(msg=msg, indent_level=2)
                return Result.fail(message=msg)

            shutil.copy(source_file, target_dir)

            self._validate_hashes(comp, target_dir.joinpath(file_name))
            self.set_collection_params(comp, repo_url, target_dir / file_name)

            return Result.success(return_obj=comp)

        download_url = source_url / file_name

        self.get_logger().info(msg="Downloading file:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {target_dir.joinpath(file_name)}", indent_level=3)

        response = download_file(f"{download_url}", str(target_dir / file_name), creds, timeout=self.process_timeout)
        result = Result.from_http_response(response)

        if result.is_fail():
            msg = f"Unable to download from {download_url}, skipping remaining attempts"
            self.get_logger().error(msg=msg, indent_level=2)

        if not result.is_success():
            return result

        self.set_collection_params(comp, repo_url, target_dir / file_name)

        return Result.success(return_obj=comp)
