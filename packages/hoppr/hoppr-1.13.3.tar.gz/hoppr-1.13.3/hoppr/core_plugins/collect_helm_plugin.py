"""Collector plugin for helm charts."""

from __future__ import annotations

import re

from pathlib import Path
from typing import TYPE_CHECKING

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import SecretStr

import hoppr.net
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.exceptions import HopprLoadDataError, HopprPluginError
from hoppr.models.sbom import Component, Hash
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService


class CollectHelmPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["helm"],
    required_commands=["helm"],
    products=["helm/*"],
    system_repositories=[],
):
    """Class to copy helm charts."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.required_commands = (self.config or {}).get("helm_command", self.required_commands)
        self.base_command = [self.required_commands[0], "pull"]

        system_repos_file = Path.home() / ".config" / "helm" / "repositories.yaml"
        if not self.context.strict_repos and system_repos_file.exists():
            system_repos: list[dict[str, str]] = []

            try:
                system_repos_dict = hoppr.utils.load_file(input_file_path=system_repos_file)
                if not isinstance(system_repos_dict, dict):
                    raise HopprLoadDataError("Incorrect format.")

                system_repos = system_repos_dict["repositories"]
            except HopprLoadDataError as ex:
                self.get_logger().warning(msg=f"Unable to parse Helm repositories file ({system_repos_file}): '{ex}'")

            self.system_repositories.extend(repo["url"] for repo in system_repos)

    def _get_provenance_sha(self, prov_file: Path) -> str | Result | None:
        """Open an optional provenance file of a helm package and extract the sha signature.

        Args:
            prov_file: Path reference to the provenance file

        Returns:
            str: signature hash given by the provenance file
        """
        if provenance_sha := re.search(r"sha256:([a-fA-F0-9]{64})", prov_file.read_text(encoding="utf-8")):
            return provenance_sha[1]

        raise HopprPluginError("Hash cannot be found in provenance file")

    def _verify_provenance_sha(self, comp: Component, prov_sha: str) -> None:
        """Given a provenance signature, see if it is in the component's hashes.

        Args:
            comp: artifact that will be compared against the provenance signature
            prov_sha: provenance signature given as a str

        Raises:
            HopprPluginError: if component hash doesn't match provenance hash
        """
        if Hash(alg=cdx.HashAlg.SHA_256, content=prov_sha) not in comp.hashes:
            raise HopprPluginError(f"Hash for {comp.name} does not match hash from provenance.")

    def _update_hashes(self, comp: Component, package_path: Path) -> None:
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

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Collect helm chart."""
        purl = hoppr.utils.get_package_url(comp.purl)

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.name}_{purl.version}")
        package_out_path = target_dir / f"{purl.name}-{purl.version}.tgz"

        run_result = None
        for subdir in ["", purl.name]:
            source_url = RepositoryUrl(url=repo_url) / subdir

            self.get_logger().info(msg="Fetching helm chart:", indent_level=2)
            self.get_logger().info(msg=f"source: {source_url}", indent_level=3)
            self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

            command = [
                *self.base_command,
                "--repo",
                f"{source_url}",
                "--destination",
                f"{target_dir}",
                purl.name,
                "--version",
                purl.version,
                *(["--debug"] if self.get_logger().is_verbose() else []),
            ]

            password_list = []

            if creds is not None and isinstance(creds.password, SecretStr):
                command = [
                    *command,
                    "--username",
                    creds.username,
                    "--password",
                    creds.password.get_secret_value(),
                ]

                password_list = [creds.password.get_secret_value()]

            run_result = self.run_command(command, password_list)

            if run_result.returncode == 0:
                self.get_logger().info("Complete helm chart artifact copy for %s version %s", purl.name, purl.version)

                # Check for provenance
                command = [*command, "--prov"]
                self.run_command(command, password_list)
                file_path = target_dir / f"{purl.name}-{purl.version}.tgz"

                try:
                    self._update_hashes(comp, file_path)
                    self._verify_provenance_sha(
                        comp,
                        self._get_provenance_sha(file_path.with_suffix(".tgz.prov")),  # type: ignore[arg-type]
                    )
                except FileNotFoundError:
                    self.get_logger().info("Target artifact has no provenance file")
                except HopprPluginError as ex:
                    return Result.fail(str(ex))

                self.get_logger().info(msg="Fetching helm chart:", indent_level=2)
                self.set_collection_params(comp, repo_url, package_out_path)

                return Result.success(return_obj=comp)

        msg = f"Failed to download {purl.name} version {purl.version} helm chart from {repo_url}."

        if run_result is not None and "404 Not Found" in str(run_result.stderr):
            self.get_logger().debug(msg=msg, indent_level=2)
            return Result.fail(f"{msg} Chart not found.")

        self.get_logger().debug(msg=msg, indent_level=2)
        return Result.retry(msg)
