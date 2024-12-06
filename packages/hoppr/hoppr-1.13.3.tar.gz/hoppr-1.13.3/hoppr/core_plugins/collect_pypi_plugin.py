"""Collector plugin for PyPI packages."""

from __future__ import annotations

import importlib.util
import re
import sys

from enum import Enum
from typing import TYPE_CHECKING, Literal, TypeAlias

import jmespath
import requests
import xmltodict

from pydantic import Field, SecretStr, validator
from requests.auth import HTTPBasicAuth

import hoppr.utils

from hoppr import __version__, cdx
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.constants import BomProps
from hoppr.exceptions import HopprPluginError, HopprPluginRetriableError
from hoppr.models.base import HopprBaseModel
from hoppr.models.sbom import Hash, Property
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from packageurl import PackageURL

    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


class CollectionType(str, Enum):
    """Represents a collection type for the PyPI collector."""

    BINARY = "binary"
    BINARY_ONLY = "binary-only"
    BINARY_PREFERRED = "binary-preferred"
    BOTH_PREFERRED = "both-preferred"
    BOTH_REQUIRED = "both-required"
    SOURCE = "source"
    SOURCE_ONLY = "source-only"
    SOURCE_PREFERRED = "source-preferred"

    def __str__(self) -> str:
        return self.value.lower()

    @classmethod
    def _missing_(cls, value: object):  # noqa: ANN206
        return next((member for member in cls if member.name in {str(value), str(value).upper()}), None)


ConcreteCollectionType: TypeAlias = Literal["binary", "source"]


class CollectPypiConfig(HopprBaseModel, underscore_attrs_are_private=True):
    """Configuration options for CollectPypiPlugin."""

    _type_order: tuple[ConcreteCollectionType] | tuple[ConcreteCollectionType, ConcreteCollectionType]

    pip_command: list[str] = Field(default=[sys.executable, "-m", "pip"])
    type: CollectionType = Field(default=CollectionType.BINARY_PREFERRED)

    @validator("pip_command", allow_reuse=True, pre=True)
    @classmethod
    def pip_cmd_to_list(cls, pip_cmd: list[str] | str) -> list[str]:
        """Convert the pip command to a list[str] before pydantic validation."""
        return pip_cmd.split() if isinstance(pip_cmd, str) else pip_cmd

    @validator("type", allow_reuse=True, pre=True)
    @classmethod
    def type_to_lower(cls, type_: str) -> str:
        """Convert the type to lowercase before pydantic validation."""
        return type_.lower()

    def __init__(self, **data):
        super().__init__(**data)

        match self.type.lower():
            case "binary-only":
                self._type_order = ("binary",)
            case "source-only":
                self._type_order = ("source",)
            case "binary" | "binary-preferred" | "both-preferred" | "both-required":
                self._type_order = ("binary", "source")
            case "source" | "source-preferred":
                self._type_order = ("source", "binary")
            case invalid_type:  # pragma: no cover
                raise ValueError(f"Invalid PyPI collection type specified: {invalid_type}")


class CollectPypiPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["pypi"],
    required_commands=[sys.executable],
    products=["pypi/*"],
    system_repositories=["https://pypi.org/simple"],
):
    """Collector plugin for PyPI packages."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.collector_config = CollectPypiConfig(**(config or {}))

        self.manifest_repos: list[str] = []
        self.password_list: list[str] = []

    def _download_package(
        self, purl: PackageURL, download_url: str, target_dir: Path, creds: CredentialRequiredService | None
    ) -> str:
        """Downloads a Python package from a specific repository URL.

        Args:
            purl: Used to identify the package in the logs.
            download_url: Where the package will be downloaded from.
            target_dir: Where the package will be downloaded to.
            creds: Credentials used for the HTTP request.

        Returns:
            A success message.

        Raises:
            HopprPluginRetryException: If package download fails and should be retried.
        """
        password_list = []

        if creds is not None and isinstance(creds.password, SecretStr):
            download_url = str(
                RepositoryUrl(
                    url=download_url,
                    username=creds.username,
                    password=creds.password.get_secret_value(),
                )
            )
            password_list = [creds.password.get_secret_value()]

        command = [
            *self.collector_config.pip_command,
            "download",
            "--no-deps",
            "--no-cache",
            "--timeout",
            str(self.process_timeout),
            "--index-url",
            download_url,
            "--dest",
            str(target_dir),
            f"{purl.name}=={purl.version}",
            *(["--verbose"] if self.get_logger().is_verbose() else []),
        ]

        collection_type = self.collector_config.type

        success_count = 0
        successes_needed = 2 if collection_type == "both-required" else 1

        self.get_logger().info("Pypi collection type: %s", collection_type, indent_level=2)

        result_codes = []

        for attempt_type in self.collector_config._type_order:
            self.get_logger().info("Attempting %s collection", attempt_type, indent_level=2)

            run_result = self.run_command([*command, self._pypi_param_for_type(attempt_type)], password_list)

            result_codes.append(run_result.returncode)

            if run_result.returncode == 0:
                success_count += 1
                self.get_logger().debug("Collection of %s successful", attempt_type, indent_level=2)
            elif not collection_type.endswith("preferred"):
                self.get_logger().debug("Collection of %s failed", attempt_type, indent_level=2)
                raise HopprPluginRetriableError(self._get_retry_exception_message(success_count))

            if success_count >= successes_needed and self.collector_config.type != CollectionType.BOTH_PREFERRED:
                break

        if success_count >= successes_needed:
            return self._get_success_message(success_count, result_codes)

        raise HopprPluginRetriableError(self._get_retry_exception_message(success_count))

    def _get_download_urls(
        self,
        component: Component,
        repo_url: str,
        creds: CredentialRequiredService | None = None,
    ) -> list[dict[str, str]]:
        auth = None
        if creds is not None and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(creds.username, creds.password.get_secret_value())

        response = requests.get(url=f"{repo_url}/simple/{component.name}", auth=auth, timeout=60)

        xml_input = response.text.removeprefix("<!DOCTYPE html>")
        xml_input = re.sub(pattern=r"\s*<head>[.\S\s\n]*</head>", repl="", string=xml_input)
        response_dict = xmltodict.parse(xml_input=xml_input, process_comments=False)

        links: list[dict[str, str]] = jmespath.search(expression="html.body.a", data=response_dict) or []

        # Normalize filenames
        for link in links:
            link["#text"] = str(link.get("#text", "")).lower()

        # Filter links if hash found in component
        for hash_ in component.hashes:
            if str(hash_.alg) == "SHA-256":
                links = jmespath.search(
                    expression=f"""[? ends_with("@href", '#sha256={hash_.content}')]""",
                    data=links,
                )

                break

        return links

    def _map_download_urls(self, component: Component, links: list[dict[str, str]]) -> dict[str, str]:
        pkg_version = component.version or hoppr.utils.get_package_url(component.purl).version

        # Get source links
        source_links = [
            link for link in links
            if (text := link.get("#text", "")).endswith(".tar.gz")
            and f"-{pkg_version}." in text
        ]  # fmt: skip

        # Get binary_links
        binary_links = [
            link for link in links
            if (text := link.get("#text", "")).endswith(".whl")
            and f"-{pkg_version}-" in text
        ]  # fmt: skip

        return {link["#text"].lower(): link["@href"] for link in [*binary_links, *source_links]}

    def _get_file_paths(self, target_dir: Path) -> Iterator[Path]:
        yield from (file_path for file_path in target_dir.iterdir() if file_path.is_file())

    def _update_hashes(self, comp: Component, package_path: Path):
        """Update the hashes of a component with hashes generated from its package file.

        Args:
            comp: Component object whose hashes will be updated.
            package_path: Path of the downloaded package file for the provided component.

        Raises:
            HopprPluginError: If an existing hash doesn't match.
        """
        generated_hashes = list(self._get_artifact_hashes(package_path))

        try:
            comp.update_hashes(generated_hashes)
        except ValueError as ex:
            self.get_logger().debug(
                "Computed hashes: [%s], SBOM hashes: [%s]",
                ", ".join(hash.json() for hash in generated_hashes),
                ", ".join(hash.json() for hash in comp.hashes),
                indent_level=2,
            )
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.") from ex

    def _validate_hashes(self, comp: Component, hash_content: str):
        """Validates the component hashes against the hashes in the package metadata provided by the PyPI server.

        Args:
            comp: Component object whose hashes will be validated.
            filename: Name of the package file. Used for querying the metadata.
            hash_content: Content of hash to validate.
            creds: Credentials used for HTTP requests.

        Raises:
            HopprPluginError: If hash validation fails.
        """
        if not comp.contains_hashes([Hash(alg=cdx.HashAlg.SHA_256, content=hash_content)]):
            self.get_logger().debug(
                "Computed hashes: [%s], expected hashes: [%s]",
                ", ".join(hash.json() for hash in comp.hashes),
                hash_content,
                indent_level=2,
            )

            raise HopprPluginError(f"Hash validation failed for {comp.name}.")

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Copy a component to the local collection directory structure."""
        # sourcery skip: low-code-quality
        if importlib.util.find_spec(name="pip") is None:
            return Result.fail(message="The pip package was not found. Please install and try again.")

        purl = hoppr.utils.get_package_url(comp.purl)

        links = self._get_download_urls(comp, repo_url, creds)
        file_link_map = self._map_download_urls(comp, links)

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.name}_{purl.version}")
        self.get_logger().info(msg=f"Target directory: {target_dir}", indent_level=2)

        simple_index_url = RepositoryUrl(url=repo_url)
        if not re.match(pattern="^.*simple/?$", string=str(simple_index_url)):
            simple_index_url /= "simple"

        try:
            success_message = self._download_package(purl, str(simple_index_url), target_dir, creds)
            downloaded_files = self._get_file_paths(target_dir)

            for file in downloaded_files:
                download_url = file_link_map[file.name.lower()]
                *_, hash_value = download_url.split("#sha256=")
                self._update_hashes(comp, file)
                self._validate_hashes(comp, hash_value)
        except KeyError as ex:
            return Result.fail(f"Download URL not found for filename: {ex}", return_obj=comp)
        except HopprPluginRetriableError as ex:
            return Result.retry(f"Failed to download {purl.name} version {purl.version}. {ex}", return_obj=comp)
        except HopprPluginError as ex:
            return Result.fail(f"Failed to download {purl.name} version {purl.version}. {ex}", return_obj=comp)

        artifact_file, *extra = (file for file in target_dir.iterdir() if file.suffix in [".gz", ".whl"])
        self.set_collection_params(comp, repo_url, artifact_file)

        comp.properties.extend(Property(name=BomProps.COLLECTION_ARTIFACT_FILE, value=file.name) for file in extra)

        return Result.success(success_message, return_obj=comp)

    def _get_success_message(self, success_count: int, result_codes: list[int]) -> str:
        message = ""
        match self.collector_config.type, self.collector_config._type_order, result_codes:
            case ("binary-preferred" | "source-preferred", (first_type, second_type), _):
                message = f"Successfully downloaded {first_type}, {second_type} skipped"
            case ("both-preferred", (first_type, second_type), [1, 0]) if success_count == 1:
                message = f"Only able to download {second_type}"
            case ("both-preferred", (first_type, second_type), [0, 1]) if success_count == 1:
                message = f"Only able to download {first_type}"

        return message

    def _get_retry_exception_message(self, success_count: int) -> str:
        message = ""
        match self.collector_config.type, *self.collector_config._type_order:
            case "both-required", first_type, second_type if success_count == 1:
                message = f"Only able to download {first_type}"
            case "binary-preferred" | "source-preferred" | "both-required" | "both-preferred", first_type, second_type:
                message = f"Unable to download {first_type} or {second_type}."
            case "binary-only" | "source-only", first_type:
                message = f"Unable to collect {first_type}"

        return message

    @staticmethod
    def _pypi_param_for_type(collection_type: str) -> str:
        if collection_type == "source":
            return "--no-binary=:all:"

        return "--only-binary=:all:"
