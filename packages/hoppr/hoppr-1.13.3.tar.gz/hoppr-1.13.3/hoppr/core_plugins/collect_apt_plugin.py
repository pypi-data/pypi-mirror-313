"""Collector plugin for apt packages."""

from __future__ import annotations

import fnmatch
import os
import shutil

from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from subprocess import CalledProcessError
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import jc

from pydantic import SecretStr

import hoppr.utils

from hoppr import Hash, __version__, cdx
from hoppr.base_plugins.collector import BatchCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_process, hoppr_rerunner
from hoppr.exceptions import HopprPluginError
from hoppr.models.credentials import Credentials
from hoppr.models.types import PurlType
from hoppr.result import Result

if TYPE_CHECKING:
    from collections.abc import Mapping

    from packageurl import PackageURL

    from hoppr.models import HopprContext
    from hoppr.models.manifest import Repository
    from hoppr.models.sbom import Component


class CollectAptPlugin(
    BatchCollectorPlugin,
    required_commands=["apt", "apt-cache"],
    supported_purl_types=["deb"],
    products=["deb/*"],
):
    """Collector plugin for apt packages."""

    def __init__(
        self,
        context: HopprContext,
        config: dict | None = None,
        config_dir: str | PathLike[str] = Path.cwd() / ".hoppr-apt",
    ) -> None:
        super().__init__(
            context=context,
            config=config,
        )

        self.manifest_repos: list[str] = []

        self.manifest_repos = [f"{repo.url}" for repo in self.context.repositories[PurlType.DEB]]

        proxy_args = self._repo_proxy()
        self.config_dir = Path(config_dir)

        self.apt_paths_dict: Mapping[str, Mapping] = {
            "etc": {
                "apt": {"auth.conf": None, "preferences.d": {}, "sources.list": None, "sources.list.d": {}},
                "cache": {"apt": {"archives": {"lock": None, "partial": {}}}},
            },
            "var": {
                "lib": {
                    "apt": {"lists": {"lock": None, "partial": {}}},
                    "dpkg": {"lock-frontend": None, "status": None},
                }
            },
        }

        self.base_command = [
            self.required_commands[0],
            f"--option=Dir={self.config_dir}",
            f"--option=Dir::State::status={self.config_dir / 'var' / 'lib' / 'dpkg' / 'status'}",
            *proxy_args,
        ]

        self.debug_args = [
            "--option=Debug::pkgProblemResolver=1",
            "--option=Debug::Acquire::http=1",
            "--option=Debug::Acquire::https=1",
            "--option=Debug::Acquire::gpgv=1",
            "--option=Debug::pkgAcquire=1",
            "--option=Debug::pkgAcquire::Auth=1",
            "--option=Debug::pkgAcquire::Worker=1",
            "--option=Debug::pkgPackageManager=1",
            "--option=Debug::sourceList=1",
        ]

    def _artifact_string(self, purl: PackageURL) -> str:
        arch = purl.qualifiers.get("arch")
        return f"{purl.name}{f':{arch}' if arch else ''}{f'={purl.version}' if purl.version else ''}"

    def _download_component(self, purl: PackageURL) -> None:
        artifact = self._artifact_string(purl)

        try:
            # Download the component
            download_result = self.run_command([
                *self.base_command,
                *(self.debug_args if self.get_logger().is_verbose() else []),
                "download",
                artifact,
            ])

            download_result.check_returncode()
        except CalledProcessError as ex:
            raise ex

    def _get_component_download_info(self, purl: PackageURL) -> tuple[str, str, str]:
        artifact = self._artifact_string(purl=purl)

        try:
            # Try getting component download URL
            url_result = self.run_command([
                *self.base_command,
                "--print-uris",
                "download",
                artifact,
            ])

            url_result.check_returncode()

            if len(url_result.stdout.decode("utf-8")) == 0:
                raise HopprPluginError
        except (CalledProcessError, HopprPluginError) as ex:
            msg = f"Failed to get download URL for component: '{purl}'"
            self.get_logger().debug(msg=msg, indent_level=2)
            raise ex

        # Take the first URL and download filename if multiple are returned
        # Apt download output format:
        #   '<download URL>' <URL-encoded download filename> <download size> SHA512:<package hash>
        # Extract the output into a tuple of the form (<download URL>, <URL-encoded download filename>). For example:
        #   ("http://archive.ubuntu.com/ubuntu/pool/main/g/git/git_2.34.1-1ubuntu1.5_amd64.deb",
        #    "git_1%3a2.34.1-1ubuntu1.5_amd64.deb")
        result = url_result.stdout.decode("utf-8").split("\n")[0]
        found_url, download_filename, _, file_checksum = result.split(" ")
        *_, file_checksum = file_checksum.split(":")

        self.get_logger().debug(msg=f"Found URL: {found_url}", indent_level=3)
        self.get_logger().debug(msg=f"Download filename: {download_filename}", indent_level=3)

        return found_url.strip("'"), download_filename, file_checksum

    def _get_download_url_path(self, purl: PackageURL) -> str:
        """Get the path segment of the component download URL using `apt-cache show`."""
        artifact = self._artifact_string(purl)

        command = [*self.base_command, *(self.debug_args if self.get_logger().is_verbose() else []), "show", artifact]
        command[0] = "apt-cache"

        cmd_result = self.run_command(command)

        try:
            cmd_result.check_returncode()
        except CalledProcessError as ex:
            raise ex

        pkg_info = jc.parse(parser_mod_name="ini", data=cmd_result.stdout.decode(encoding="utf-8"))

        if not isinstance(pkg_info, dict) or not isinstance(pkg_info["Filename"], str):
            raise TypeError("Parsed output not in the expected format.")

        return pkg_info["Filename"]

    def _get_found_repo(self, found_url: str) -> str | None:
        """Identify the repository associated with the specified URL."""
        return next((repo for repo in self.manifest_repos if found_url.startswith(repo)), None)

    def _populate_apt_folder_structure(self, apt_path: Path, path_dict: Mapping[str, Mapping | None]) -> None:
        for key, value in path_dict.items():
            # None type indicates file to create
            if value is None:
                apt_file = apt_path / key
                apt_file.touch(exist_ok=True, mode=0o644)
            # dict type indicates directory to create
            elif isinstance(value, dict):
                apt_dir = apt_path / key
                apt_dir.mkdir(exist_ok=True, parents=True)

                if len(value.items()) > 0:
                    self._populate_apt_folder_structure(apt_path=apt_dir, path_dict=value)
            else:
                raise TypeError("Value is not expected type.")

    def _populate_auth_conf(self, repo_list: list[Repository], file: Path) -> None:
        """Populate Apt authentication config file."""
        creds: list[str] = []
        for repo in repo_list:
            repo_credentials = Credentials.find(f"{repo.url}")
            if repo_credentials is not None and isinstance(repo_credentials.password, SecretStr):
                creds.append(
                    f"machine {repo.url} "
                    f"login {repo_credentials.username} "
                    f"password {repo_credentials.password.get_secret_value()}\n"
                )

        # Set restrictive permissions on Apt authentication config file
        file.chmod(mode=0o600)

        with file.open(mode="w+", encoding="utf-8") as auth_conf:
            auth_conf.write("\n".join(creds))

    def _populate_sources_list(self, repo_list: list[str], file: Path) -> None:
        """Populate sources list."""
        # Read data from /etc/os-release file
        parser = ConfigParser()

        with (Path("/") / "etc" / "os-release").open(mode="r", encoding="utf-8") as os_release:
            parser.read_string(string=f"[os-release]\n{os_release.read()}")

        version_codename = parser["os-release"]["VERSION_CODENAME"]

        sources: list[str] = []
        for repo in repo_list:
            for component in ["main restricted", "universe", "multiverse"]:
                sources.extend((
                    f"deb {repo} {version_codename} {component}",
                    f"deb {repo} {version_codename}-updates {component}",
                    f"deb {repo} {version_codename}-security {component}",
                ))

        with file.open(mode="w+", encoding="utf-8") as sources_list:
            sources_list.write("\n".join(sources))

    def _repo_proxy(self) -> set[str]:
        proxy_args: list[str] = []

        for proto in ["http", "https"]:
            if proxy := os.getenv(f"{proto}_proxy"):
                proxy_args = [*proxy_args, f"--option=Acquire::{proto}::Proxy={proxy}"]

        no_proxy_urls = [item for item in os.getenv("no_proxy", "").split(",") if item != ""]

        for url in self.manifest_repos:
            parsed_url = urlparse(url)

            for pattern in no_proxy_urls:
                # Check if pattern is a substring or wildcard match of manifest repo URL
                if pattern in parsed_url.netloc or fnmatch.fnmatch(name=parsed_url.netloc, pat=pattern):
                    proxy_args = [
                        *proxy_args,
                        f"--option=Acquire::http::Proxy::{parsed_url.netloc}=DIRECT",
                        f"--option=Acquire::https::Proxy::{parsed_url.netloc}=DIRECT",
                    ]

        return set(proxy_args)

    def get_version(self) -> str:  # noqa: D102
        return __version__

    @hoppr_process
    def pre_stage_process(self) -> Result:  # noqa: D102
        self._populate_apt_folder_structure(apt_path=self.config_dir, path_dict=self.apt_paths_dict)

        self._populate_sources_list(
            repo_list=self.manifest_repos,
            file=self.config_dir / "etc" / "apt" / "sources.list",
        )

        self._populate_auth_conf(
            repo_list=self.context.repositories[PurlType.DEB],
            file=self.config_dir / "etc" / "apt" / "auth.conf",
        )

        if not self.context.strict_repos:
            system_apt_path = Path("/") / "etc" / "apt"
            plugin_apt_path = self.config_dir / "etc" / "apt"

            # Copy system Apt source lists into temporary directory
            shutil.copyfile(
                src=system_apt_path / "sources.list",
                dst=plugin_apt_path / "sources.list.d" / "system.list",
            )

            shutil.copytree(
                src=system_apt_path / "sources.list.d",
                dst=plugin_apt_path / "sources.list.d",
                dirs_exist_ok=True,
            )

        # Populate user Apt cache
        result = self.run_command([
            *self.base_command,
            *(self.debug_args if self.get_logger().is_verbose() else []),
            "--option=Dir::Etc::trusted=/etc/apt/trusted.gpg",
            "--option=Dir::Etc::trustedparts=/etc/apt/trusted.gpg.d",
            "update",
        ])

        if result.returncode != 0:
            return Result.fail("Failed to populate Apt cache.")

        return Result.success()

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

    def _validate_hashes(self, comp: Component, file_checksum: str):
        validation_hash = Hash(alg=cdx.HashAlg.SHA_512, content=file_checksum)
        if not comp.contains_hashes([validation_hash]):
            raise HopprPluginError(f"Hash validation failed for {comp.name}.")

    @hoppr_rerunner
    def collect(self, comp: Component) -> Result:
        """Copy a component to the local collection directory structure."""
        purl = hoppr.utils.get_package_url(comp.purl)

        try:
            found_url, download_filename, file_checksum = self._get_component_download_info(purl=purl)
        except (CalledProcessError, HopprPluginError) as ex:
            return Result.retry(message=str(ex))

        download_url_path = Path(self._get_download_url_path(purl=purl))
        subdir = download_url_path.parent

        if self.context.strict_repos:
            # Strip surrounding single quotes to compare against manifest repos
            repo = self._get_found_repo(found_url)

            # Return failure if found APT URL is not from a repo defined in the manifest
            if repo is None:
                return Result.fail(
                    f"Apt download URL does not match any repository in manifest. (Found URL: '{found_url}')"
                )

            result = self.check_purl_specified_url(purl, repo)
            if not result.is_success():
                return result
        else:
            # Default to found_url with the path component removed
            repo = found_url.removesuffix(str(download_url_path))

        target_dir = self.directory_for(purl.type, repo, subdir=str(subdir))
        package_out_path = target_dir / download_filename

        try:
            self._download_component(purl=purl)
        except CalledProcessError:
            msg = f"Failed to download Apt artifact {purl.name} version {purl.version}"
            return Result.retry(msg)

        self.get_logger().info(msg="Moving downloaded component:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_filename}", indent_level=3)
        self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

        shutil.move(src=download_filename, dst=target_dir)

        try:
            self._update_hashes(comp, target_dir / download_filename)
            self._validate_hashes(comp, file_checksum)
        except HopprPluginError as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo, package_out_path)

        return Result.success(return_obj=comp)
