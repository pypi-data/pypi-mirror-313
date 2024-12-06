"""Collector plugin for Gem packages."""

from __future__ import annotations

from typing import TYPE_CHECKING

import jmespath
import requests as requests

from requests import HTTPError
from typing_extensions import override

import hoppr.net
import hoppr.utils

from hoppr import Hash, __version__, cdx
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprPluginError
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from pathlib import Path

    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


class CollectGemPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["gem"],
    products=["gem/*"],
    system_repositories=["https://rubygems.org/api/v2/rubygems"],
):
    """Collector plugin for Gem packages."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def _update_hashes(self, comp: Component, package_path: Path) -> Result:
        generated_hashes = self._get_artifact_hashes(package_path)
        try:
            comp.update_hashes(generated_hashes)
        except ValueError as ex:
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.") from ex

        return Result.success()

    def _validate_hashes(self, comp: Component, checksum: Hash) -> Result:
        if not comp.contains_hashes([checksum]):
            raise HopprPluginError(f"Hash validation failed for {comp.name}.")

        return Result.success()

    def _get_package_metadata(self, api_url: RepositoryUrl) -> requests.Response:
        response = requests.get(str(api_url), timeout=60)

        try:
            response.raise_for_status()
        except HTTPError as ex:
            msg = f"RubyGems API web request error, request URL='{api_url}', status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            raise HopprPluginError(msg) from ex

        return response

    def _download_gem_file(self, download_url: str, package_out_path: Path, comp: Component):
        response = hoppr.net.download_file(url=download_url, dest=str(package_out_path), timeout=self.process_timeout)

        if not Result.from_http_response(response=response, return_obj=comp).is_success():
            msg = f"Failed to download Gem package {comp.purl}, status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            raise HopprPluginError(msg)

    @override
    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)

        api_url = RepositoryUrl(url=repo_url) / purl.name / "versions" / f"{purl.version}.json"

        if platform := purl.qualifiers.get("platform"):
            api_url = RepositoryUrl(url=f"{api_url}?platform={platform}")

        try:
            gem_package_metadata = self._get_package_metadata(api_url)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        checksum = Hash(
            alg=cdx.HashAlg.SHA_256, content=jmespath.search(expression="sha", data=gem_package_metadata.json())
        )

        download_url: str | None = jmespath.search(expression="gem_uri", data=gem_package_metadata.json())

        if not download_url:
            msg = f"Unable to retrieve download URL for Gem '{comp.purl}'"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.fail(message=msg)

        self.get_logger().info(msg=f"Copying Gem package from {api_url}", indent_level=2)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        self.get_logger().info(msg=target_dir.as_posix())

        package_out_path = target_dir / f"{purl.name}-{purl.version}.gem"

        self.get_logger().info(msg="Downloading Gem:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {package_out_path}", indent_level=3)

        try:
            self._download_gem_file(download_url, package_out_path, comp)
            self._update_hashes(comp, package_out_path)
            self._validate_hashes(comp, checksum)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo_url, package_out_path)
        return Result.success(return_obj=comp)
