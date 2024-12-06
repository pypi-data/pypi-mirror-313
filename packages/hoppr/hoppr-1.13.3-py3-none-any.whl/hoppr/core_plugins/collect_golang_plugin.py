"""Collector plugin for Golang images."""

from __future__ import annotations

import base64
import hashlib
import itertools
import zipfile

from typing import TYPE_CHECKING

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx
import requests

from pydantic import SecretStr
from requests import HTTPError
from requests.auth import HTTPBasicAuth

import hoppr.net
import hoppr.utils

from hoppr import Hash, __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprPluginError
from hoppr.models.credentials import CredentialRequiredService, Credentials
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path

    from packageurl import PackageURL

    from hoppr.models.sbom import Component


class CollectGolangPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["golang"],
    products=["golang/*"],
    system_repositories=["https://proxy.golang.org"],
):
    """Collector plugin for Golang images."""

    go_sum_url: str = "https://sum.golang.org/lookup"

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def _download_package(
        self, purl: str | None, download_url: RepositoryUrl, dest_file: Path, creds: CredentialRequiredService | None
    ):
        """Downloads a golang package from a specific URL.

        Args:
            purl: Used to identify the package in the logs.
            download_url: Where the package will be downloaded from.
            dest_file: Where the package will be downloaded to.
            creds: Credentials used for the HTTP request.

        Raises:
            HopprPluginError: If package download fails.
        """
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
            msg = f"Failed to download golang package for {purl}, status_code={response.status_code}"
            self.get_logger().error(msg=msg, indent_level=2)
            raise HopprPluginError(msg) from ex

    def _get_package_checksum(self, metadata_url: str, purl: PackageURL, auth: HTTPBasicAuth | None) -> Hash:
        """Gets the package checksum from the metadata at the specified URL.

        Args:
            metadata_url: URL to the JSON document containing the package metadata.
            purl: PackageURL to get checksum for
            auth: Basic HTTP authentication

        Returns:
            The SHA256 hash contained in the metadata.

        Raises:
            HopprPluginError: If download fails.
            ValueError: If the downloaded file does not contain the checksum.
        """
        package_metadata_response = requests.get(
            url=metadata_url,
            auth=auth,
            timeout=300,
            proxies=self._get_proxies_for(metadata_url),
        )

        try:
            package_metadata_response.raise_for_status()
        except HTTPError as ex:
            msg = (
                f"Failed to download Golang package metadata from {metadata_url}, "
                f"status_code={package_metadata_response.status_code}"
            )
            raise HopprPluginError(msg) from ex

        response_text = package_metadata_response.text.split("\n")[1]

        if purl.name not in response_text and purl.version not in response_text:
            raise ValueError("Package metadata missing package information.")

        checksum = response_text.split("h1:")[1]

        decoded_checksum = base64.b64decode(checksum).hex()

        return Hash(alg=cdx.HashAlg.SHA_256, content=decoded_checksum)

    def _get_download_urls(self, purl: PackageURL, repo_url: str) -> tuple[str, RepositoryUrl, RepositoryUrl]:
        package_name = f"{'_'.join(filter(None, [purl.name, purl.version]))}.zip"
        golang_metadata_url = (
            RepositoryUrl(url=self.go_sum_url) / (purl.namespace or "") / f"{purl.name}@{purl.version}"
        )
        golang_download_url = (
            RepositoryUrl(url=repo_url) / (purl.namespace or "") / purl.name / "@v" / f"{purl.version}.zip"
        )

        return package_name, golang_metadata_url, golang_download_url

    def _get_golang_file_hash(self, artifact: str | PathLike[str]) -> Hash:
        """Compute hash of downloaded golang component using algorithm used for golang package checksum database.

        Golang documentation explaining algorithm:
            - https://pkg.go.dev/golang.org/x/mod/sumdb/dirhash#Hash1

        Golang algorithm in code:
            - https://cs.opensource.google/go/x/mod/+/v0.16.0:sumdb/dirhash/hash.go;l=44.

        Args:
            artifact: Path to downloaded file

        Returns:
            A Hash Object with computed hexidecimal hash digest.

        Raises:
            HopprPluginError: If artifact is not a Zip file.
        """
        if not zipfile.is_zipfile(artifact):
            raise HopprPluginError("Incorrect File Type for golang hash generation")

        with zipfile.ZipFile(artifact) as pkg_zip:
            file_list = pkg_zip.namelist()
            file_list.sort()
            hash_obj = hashlib.sha256()

            for file in file_list:
                if "\n" in file:
                    raise HopprPluginError("Filenames with newlines are not supported")

                file_content = pkg_zip.read(file)
                file_hash = hashlib.sha256()
                file_hash.update(file_content)

                file_entry = f"{file_hash.hexdigest()}  {file}\n"
                hash_obj.update(str.encode(file_entry))

        return Hash(alg=cdx.HashAlg.SHA_256, content=hash_obj.hexdigest())

    def _update_hashes(self, comp: Component, package_path: Path) -> Result:
        """Update the hashes of a component with hashes generated from its package file.

        Args:
            comp: Component object whose hashes will be updated.
            package_path: Path of the downloaded package file for the provided component.

        Raises:
            HopprPluginError: If an existing hash doesn't match.
        """
        generated_hashes = self._get_artifact_hashes(package_path)
        golang_hash = self._get_golang_file_hash(package_path)
        generated_hashes = itertools.chain(generated_hashes, [golang_hash])

        try:
            comp.update_hashes(generated_hashes)
        except ValueError as ex:
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.") from ex

        return Result.success()

    def _validate_hashes(
        self, comp: Component, metadata_url: RepositoryUrl, purl: PackageURL, auth: HTTPBasicAuth | None
    ) -> Result:
        """Validates the component hashes against the hashes in the package metadata provided by the golang server.

        Args:
            comp: Component object whose hashes will be validated.
            metadata_url: URL to the JSON document containing the package metadata.
            purl: PackageURL to validate hashes for
            auth: Basic HTTP authentication

        Raises:
            HopprPluginError: If hash validation fails.
        """
        try:
            validation_hash = self._get_package_checksum(metadata_url.url, purl, auth=auth)
        except (HopprPluginError, ValueError) as ex:
            self.get_logger().error(msg=str(ex), indent_level=2)
            raise HopprPluginError(f"Failed to download Golang package metadata from {metadata_url}.") from ex

        if not comp.contains_hashes([validation_hash]):
            raise HopprPluginError(f"Hash validation failed for {comp.name}.")

        return Result.success()

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Download golang package via get request."""
        purl = hoppr.utils.get_package_url(comp.purl)

        package_name, golang_metadata_url, golang_download_url = self._get_download_urls(purl, repo_url)
        self.get_logger().info(msg=f"Copying Golang package from {comp.purl}", indent_level=2)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        package_out_path = target_dir / package_name

        auth: HTTPBasicAuth | None = None
        if (creds := Credentials.find(f"{repo_url}")) and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())

        try:
            self._download_package(comp.purl, golang_download_url, package_out_path, creds)
            self._update_hashes(comp, package_out_path)
            self._validate_hashes(comp, golang_metadata_url, purl, auth)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo_url, package_out_path)
        return Result.success(return_obj=comp)
