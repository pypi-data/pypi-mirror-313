"""Collector plugin for maven artifacts."""

from __future__ import annotations

import importlib
import os
import warnings

from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, Any

import jmespath
import xmltodict

from typing_extensions import override

import hoppr.net
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprExperimentalWarning, HopprPluginError
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from collections import OrderedDict

    from packageurl import PackageURL

    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


warnings.warn(
    message="This Maven collector plugin is experimental; use at your own risk.",
    category=HopprExperimentalWarning,
    stacklevel=1,
)


class CollectMavenPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["maven"],
    products=["maven/*"],
    system_repositories=["https://repo.maven.apache.org/maven2"],
):
    """Collector plugin for maven artifacts (EXPERIMENTAL)."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        system_settings_file = Path("/") / "etc" / "maven" / "settings.xml"
        user_settings_file = Path.home() / ".m2" / "settings.xml"

        if not self.context.strict_repos:
            # Identify system repositories
            for settings_file in [system_settings_file, user_settings_file]:
                if settings_file.is_file():
                    settings_dict: OrderedDict[str, Any] = xmltodict.parse(
                        settings_file.read_text(encoding="utf-8"),
                        encoding="utf-8",
                        force_list={"profile", "repository"},
                    )

                    repo_urls: list[str] = jmespath.search(
                        expression="settings.profiles.profile[].repositories.repository[].url", data=settings_dict
                    )

                    self.system_repositories.extend(
                        repo for repo in repo_urls or []
                        if repo not in self.system_repositories
                    )  # fmt: skip

    def update_hashes(self, comp: Component, package_path: Path) -> Result:
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

        return Result.success()

    def _check_artifact_hash(
        self,
        download_url: str,
        dest_file: str,
        creds: CredentialRequiredService | None = None,
    ) -> Result:
        with NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as hash_file:
            # Download SHA1 hash file for artifact
            response = hoppr.net.download_file(
                url=f"{download_url}.sha1",
                dest=hash_file.name,
                creds=creds,
                proxies=self._get_proxies_for(download_url),
            )

            result = Result.from_http_response(response=response)
            hash_string = Path(hash_file.name).read_text(encoding="utf-8").strip().lower()
            hash_file.flush()
            hash_file.close()
            Path(hash_file.name).unlink()

        if (computed_hash := hoppr.net.get_file_hash(artifact=dest_file)) != hash_string:
            result.merge(Result.fail(message=f"SHA1 hash for {Path(dest_file).name} does not match expected hash."))
            self.get_logger().debug("Computed hash: %s, expected: %s", computed_hash, hash_string, indent_level=2)

        return result

    # Helper function to combine a classifier, if present, with the artifact version
    def _set_classifier(self, purl: PackageURL) -> str:
        artifact_type = purl.qualifiers.get("type", "jar")
        artifact_classifier = purl.qualifiers.get("classifier")

        return "-".join(filter(None, [purl.version, "" if artifact_type == "pom" else artifact_classifier]))

    def _get_maven_component(
        self,
        purl: PackageURL,
        repo_url: str,
        target_dir: Path,
        creds: CredentialRequiredService | None = None,
    ) -> Result:
        artifact_path = "/".join((purl.namespace or "").split("."))
        artifact_type = purl.qualifiers.get("type", "jar")

        version_qualifiers = self._set_classifier(purl)
        artifact_file = f"{purl.name}-{version_qualifiers}.{artifact_type}"

        download_url = str(RepositoryUrl(url=repo_url) / artifact_path / purl.name / purl.version / artifact_file)

        # Reconstructs the file name to match what is expected by downstream plugins
        file_name = f"{purl.name}_{version_qualifiers}.{artifact_type}"
        dest_file = f"{target_dir / file_name}"

        self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {dest_file}", indent_level=3)

        response = hoppr.net.download_file(
            url=download_url,
            dest=dest_file,
            creds=creds,
            proxies=self._get_proxies_for(download_url),
        )

        if not (result := Result.from_http_response(response=response)).is_success():
            return result

        result.merge(self._check_artifact_hash(download_url, dest_file, creds))

        return result

    @override
    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)
        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

        artifact_type = purl.qualifiers.get("type", "jar")

        version_qualifiers = self._set_classifier(purl)

        # Reconstructs the file name to match what is expected by downstream plugins
        file_name = f"{purl.name}_{version_qualifiers}.{artifact_type}"
        package_out_path = target_dir / file_name

        self.get_logger().info(msg="Downloading Maven artifact:", indent_level=2)
        result = self._get_maven_component(purl, repo_url, target_dir, creds)

        if not result.is_success():
            msg = f"Failed to download Maven artifact {comp.purl}, {result.message}"
            self.get_logger().error(msg=msg, indent_level=2)
            return Result.fail(message=msg)

        if purl.qualifiers.get("type") != "pom":
            purl_copy = deepcopy(purl)
            purl_copy.qualifiers["type"] = "pom"
            artifact_type_copy = "pom"

            # Don't need to run the _set_classifier function as it has to be a pom here
            file_name = f"{purl.name}_{purl.version}.{artifact_type_copy}"

            self.get_logger().info(msg="Downloading pom for Maven artifact:", indent_level=2)
            result = self._get_maven_component(purl_copy, repo_url, target_dir, creds)

            if not result.is_success():
                msg = f"Failed to download pom for Maven artifact {comp.purl}, {result.message}"
                self.get_logger().error(msg=msg, indent_level=2)
                return Result.fail(message=msg)

        self.update_hashes(comp, Path(package_out_path))

        self.set_collection_params(comp, repo_url, package_out_path)

        return Result.success(return_obj=comp)


if not os.getenv("HOPPR_EXPERIMENTAL"):
    warnings.warn(
        message="Either the --experimental flag or the environment variable "
        "HOPPR_EXPERIMENTAL must be set in order to use this plugin.",
        category=HopprExperimentalWarning,
        stacklevel=1,
    )

    module = importlib.import_module(name="hoppr.core_plugins.collect_maven_plugin")
    CollectMavenPlugin = module.CollectMavenPlugin  # type: ignore[misc]
