"""Collector plugin for npm packages."""

from __future__ import annotations

import base64
import time

from typing import TYPE_CHECKING, Final
from urllib.parse import quote_plus

import jmespath
import requests as requests

from pydantic import SecretStr
from requests import HTTPError, Response
from requests.auth import HTTPBasicAuth

import hoppr.net
import hoppr.utils

from hoppr import Hash, __version__, cdx
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprPluginError
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService, Credentials
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from pathlib import Path

    from packageurl import PackageURL


class CollectNpmPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["npm"],
    products=["npm/*"],
    system_repositories=["https://registry.npmjs.org"],
):
    """Collector plugin for npm packages."""

    REQUEST_RETRIES: Final[int] = 3
    REQUEST_RETRY_INTERVAL: Final[float] = 5
    REQUEST_TIMEOUT: Final[float] = 60

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def _download_package(
        self,
        purl: str | None,
        download_url: RepositoryUrl,
        dest_file: Path,
        creds: CredentialRequiredService | None,
    ):
        response = hoppr.net.download_file(
            url=str(download_url),
            dest=str(dest_file),
            creds=creds,
            proxies=self._get_proxies_for(str(download_url)),
            timeout=self.process_timeout,
        )
        try:
            response.raise_for_status()
        except HTTPError as ex:
            msg = f"Failed to download NPM package for {purl}, status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            raise HopprPluginError(msg) from ex

    def _get_package_checksum(self, metadata_url: RepositoryUrl, pkg_version: str, auth: HTTPBasicAuth | None) -> Hash:
        try:
            npm_metadata_response = self._stream_url_data(url=metadata_url, auth=auth)
        except HTTPError as ex:
            raise HopprPluginError(f"Failed to download NPM package metadata from {metadata_url}.") from ex

        raw_checksum = jmespath.search(
            expression=f'versions."{pkg_version}".dist.integrity',
            data=npm_metadata_response.json(),
        ).lstrip("sha512-")

        if not raw_checksum:
            raise ValueError("Package metadata is missing package checksum.")

        checksum = base64.b64decode(raw_checksum).hex()

        return Hash(alg=cdx.HashAlg.SHA_512, content=checksum)

    def _get_download_urls(self, purl: PackageURL, repo_url: str) -> tuple[str, RepositoryUrl, RepositoryUrl]:
        tar_name = f"{purl.name}{f'-{purl.version}' if purl.version else ''}.tgz"
        npm_metadata_url = RepositoryUrl(url=repo_url) / quote_plus(purl.namespace or "") / purl.name
        npm_download_url = npm_metadata_url / "-" / tar_name

        return tar_name, npm_metadata_url, npm_download_url

    def _update_hashes(self, comp: Component, package_path: Path) -> Result:
        generated_hashes = self._get_artifact_hashes(package_path)
        try:
            comp.update_hashes(generated_hashes)
        except ValueError as ex:
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.") from ex

        return Result.success()

    def _validate_hashes(
        self,
        comp: Component,
        metadata_url: RepositoryUrl,
        pkg_version: str,
        auth: HTTPBasicAuth | None,
    ) -> Result:
        try:
            validation_hash = self._get_package_checksum(metadata_url, pkg_version, auth=auth)
        except (HopprPluginError, ValueError) as ex:
            self.get_logger().error(msg=str(ex), indent_level=2)
            raise HopprPluginError(f"Failed to download NPM package metadata from {metadata_url}.") from ex

        if not comp.contains_hashes([validation_hash]):
            raise HopprPluginError(f"Hash validation failed for {comp.name}.")

        return Result.success()

    def _stream_url_data(self, url: RepositoryUrl | str, auth: HTTPBasicAuth | None = None) -> Response:
        """Stream download data from specified URL.

        Args:
            url: URL of remote resource to stream.
            auth: Basic authentication if required by URL. Defaults to None.

        Raises:
            HTTPError: Failed to download resource after 3 attempts.

        Returns:
            The web request response.
        """
        url = str(url)
        response = Response()

        for _ in range(self.REQUEST_RETRIES):
            response = requests.get(
                url=url,
                auth=auth,
                stream=True,
                timeout=self.REQUEST_TIMEOUT,
                proxies=self._get_proxies_for(url),
            )

            try:
                response.raise_for_status()
                return response
            except HTTPError:
                time.sleep(self.REQUEST_RETRY_INTERVAL)

        raise HTTPError(f"Failed to retrieve data from {url}", response=response)

    @hoppr_rerunner
    def collect(
        self,
        comp: Component,
        repo_url: str,
        creds: CredentialRequiredService | None = None,
    ) -> Result:
        """Download npm package via get request."""
        purl = hoppr.utils.get_package_url(comp.purl)

        tar_name, npm_metadata_url, npm_download_url = self._get_download_urls(purl, repo_url)
        self.get_logger().info(msg=f"Copying NPM package from {comp.purl}", indent_level=2)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        package_out_path = target_dir / tar_name

        auth: HTTPBasicAuth | None = None
        if (creds := Credentials.find(f"{repo_url}")) and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())

        try:
            self._download_package(comp.purl, npm_download_url, package_out_path, creds)
            self._update_hashes(comp, package_out_path)
            self._validate_hashes(comp, npm_metadata_url, str(purl.version), auth)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo_url, package_out_path)
        return Result.success(return_obj=comp)
