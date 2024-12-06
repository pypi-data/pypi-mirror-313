"""Collector plugin for Cargo packages."""

from __future__ import annotations

from typing import TYPE_CHECKING

import jmespath
import requests as requests

from pydantic import SecretStr
from requests import HTTPError
from requests.auth import HTTPBasicAuth
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

    from packageurl import PackageURL

    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


class CollectCargoPlugin(
    SerialCollectorPlugin,
    products=["cargo/*"],
    supported_purl_types=["cargo"],
    system_repositories=["https://crates.io/api/v1/crates"],
):
    """Collector plugin for Cargo packages."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def _download_package(
        self, purl: str | None, download_url: str, dest_file: Path, creds: CredentialRequiredService | None
    ):
        """Downloads a cargo package from a specific URL.

        Args:
            purl: Used to identify the package in the logs.
            download_url: Where the package will be downloaded from.
            dest_file: Where the package will be downloaded to.
            creds: Credentials used for the HTTP request.

        Raises:
            HopprPluginError: If package download fails.
        """
        response = hoppr.net.download_file(
            url=download_url,
            dest=str(dest_file),
            creds=creds,
            proxies=self._get_proxies_for(download_url),
            timeout=self.process_timeout,
        )

        try:
            response.raise_for_status()
        except HTTPError as ex:
            msg = f"Failed to download Cargo package {purl}, status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            raise HopprPluginError(msg) from ex

    def _get_package_checksum(self, metadata_url: str, creds: CredentialRequiredService | None) -> Hash:
        """Gets the package checksum from the metadata at the specified URL.

        Args:
            metadata_url: URL to the JSON document containing the package metadata.
            creds: Credentials used for the HTTP request.

        Returns:
            The SHA256 hash contained in the metadata.

        Raises:
            HopprPluginError: If download fails.
            ValueError: If the downloaded file does not contain the checksum.
        """
        authentication = None
        if creds is not None and isinstance(creds.password, SecretStr):
            authentication = HTTPBasicAuth(creds.username, creds.password.get_secret_value())

        package_metadata_response = requests.get(
            url=metadata_url,
            auth=authentication,
            timeout=300,
            proxies=self._get_proxies_for(metadata_url),
        )

        try:
            package_metadata_response.raise_for_status()
        except HTTPError as ex:
            msg = (
                f"Failed to download Cargo package metadata from {metadata_url}, "
                f"status_code={package_metadata_response.status_code}"
            )
            raise HopprPluginError(msg) from ex

        checksum = jmespath.search(expression="version.checksum", data=package_metadata_response.json())

        if checksum is None:
            raise ValueError("Package metadata is missing package checksum.")

        return Hash(alg=cdx.HashAlg.SHA_256, content=checksum)

    def _get_download_urls(self, purl: PackageURL, repo_url: str) -> tuple[str, str]:
        package_metadata_url = RepositoryUrl(url=repo_url) / purl.name / (purl.version or "")
        package_download_url = package_metadata_url / "download"
        return str(package_metadata_url), str(package_download_url)

    def _update_hashes(self, comp: Component, package_path: Path):
        """Update the hashes of a component with hashes generated from its package file.

        Args:
            comp: Component object whose hashes will be updated.
            package_path: Path of the downloaded package file for the provided component.

        Raises:
            HopprPluginError: If an existing hash doesn't match.
        """
        generated_hashes = self._get_artifact_hashes(package_path)
        try:
            comp.update_hashes(generated_hashes)
        except ValueError as ex:
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.") from ex

    def _validate_hashes(self, comp: Component, metadata_url: str, creds: CredentialRequiredService | None):
        """Validates the component hashes against the hashes in the package metadata provided by the Cargo server.

        Args:
            comp: Component object whose hashes will be validated.
            metadata_url: URL to the JSON document containing the package metadata.
            creds: Credentials used for HTTP requests.

        Raises:
            HopprPluginError: If hash validation fails.
        """
        try:
            validation_hash = self._get_package_checksum(metadata_url, creds)
        except (HopprPluginError, ValueError) as ex:
            self.get_logger().error(msg=str(ex), indent_level=2)
            raise HopprPluginError() from ex

        if not comp.contains_hashes([validation_hash]):
            raise HopprPluginError(f"Hash validation failed for {comp.name}.")

    @override
    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)

        package_metadata_url, package_download_url = self._get_download_urls(purl, repo_url)

        self.get_logger().info(msg=f"Copying Cargo package from {package_download_url}", indent_level=2)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        package_out_path = target_dir / f"{purl.name}-{purl.version}.crate"

        try:
            self._download_package(comp.purl, package_download_url, package_out_path, creds)
            self._update_hashes(comp, package_out_path)
            self._validate_hashes(comp, package_metadata_url, creds)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo_url, package_out_path)
        return Result.success(return_obj=comp)
