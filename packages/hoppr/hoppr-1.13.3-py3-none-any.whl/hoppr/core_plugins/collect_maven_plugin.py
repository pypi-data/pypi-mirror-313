"""Collector plugin for maven artifacts."""

from __future__ import annotations

import importlib
import os

from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING, Any

import jmespath
import xmltodict

from pydantic import SecretStr

import hoppr.net
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.result import Result

if TYPE_CHECKING:
    from collections import OrderedDict

    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


_MAVEN_DEP_PLUGIN = "org.apache.maven.plugins:maven-dependency-plugin:3.5.0"


class CollectMavenPlugin(
    SerialCollectorPlugin,
    required_commands=["mvn"],
    supported_purl_types=["maven"],
    products=["maven/*"],
    system_repositories=["https://repo.maven.apache.org/maven2"],
):
    """Collector plugin for maven artifacts."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.extra_opts: list[str] = []

        if self.config is not None:
            self.required_commands = self.config.get("maven_command", self.required_commands)
            self.extra_opts = self.config.get("maven_opts", self.extra_opts)

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

                    for repo in repo_urls or []:
                        if repo not in self.system_repositories:
                            self.system_repositories.append(repo)

    def _get_maven_component(self, command: list[str], password_list: list[str], **kwargs) -> CompletedProcess[bytes]:
        full_command = command.copy()
        full_command.extend(f"-D{key}={value}" for key, value in kwargs.items())
        result = self.run_command(full_command, password_list)

        # The maven plugin does not recognize the 'destFileName' argument, so rename the file
        if result.returncode == 0:
            _, name, version, extension = kwargs.get("artifact", "::::").split(":")
            directory: Path = kwargs.get("outputDirectory", ".")
            old_name = f"{name}-{version}.{extension}"
            new_name = kwargs.get("destFileName", f"{name}_{version}.{extension}")

            (directory / old_name).rename(directory / new_name)

        return result

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Copy a component to the local collection directory structure."""
        purl = hoppr.utils.get_package_url(comp.purl)
        artifact = f"{purl.namespace}:{purl.name}:{purl.version}"

        extension = purl.qualifiers.get("type", "tar.gz")
        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        package_out_path = target_dir / f"{purl.name}_{purl.version}.{extension}"

        self.get_logger().info(msg="Copying maven artifact:", indent_level=2)
        self.get_logger().info(msg=f"source: {repo_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

        settings_dict = {
            "settings": {
                "servers": {
                    "server": {
                        "id": "repoId",
                        "username": "${repo.login}",
                        "password": "${repo.pwd}",
                    }
                }
            }
        }

        with NamedTemporaryFile(mode="w+", encoding="utf-8") as settings_file:
            settings_file.write(xmltodict.unparse(input_dict=settings_dict, pretty=True))
            settings_file.flush()

            password_list = []

            defines = {
                "artifact": f"{artifact}:{extension}",
                "outputDirectory": target_dir,
                "destFileName": f"{purl.name}_{purl.version}.{extension}",
                "remoteRepositories": f"repoId::::{repo_url}",
            }

            if creds is not None and isinstance(creds.password, SecretStr):
                defines["repo.login"] = creds.username
                defines["repo.pwd"] = creds.password.get_secret_value()
                password_list = [creds.password.get_secret_value()]

            command = [
                self.required_commands[0],
                f"{_MAVEN_DEP_PLUGIN}:copy",
                f"--settings={settings_file.name}",
                *self.extra_opts,
                *(["--debug"] if self.get_logger().is_verbose() else []),
            ]

            run_result = self._get_maven_component(command, password_list, **defines)
            error_msg = f"Failed to download maven artifact {artifact} type={extension}"

            try:
                run_result.check_returncode()

                if extension != "pom":
                    defines["artifact"] = str(defines["artifact"]).replace(f":{extension}", ":pom")
                    defines["destFileName"] = str(defines["destFileName"]).replace(f".{extension}", ".pom")

                    error_msg = f"Failed to download pom for maven artifact {artifact}"
                    run_result = self._get_maven_component(command, password_list, **defines)
                    run_result.check_returncode()
            except CalledProcessError:
                self.get_logger().debug(msg=error_msg, indent_level=2)
                return Result.retry(message=error_msg)

        self.set_collection_params(comp, repo_url, package_out_path)

        return Result.success(return_obj=comp)


if os.getenv("HOPPR_EXPERIMENTAL"):
    module = importlib.import_module(name="hoppr.plugins.collect.maven")
    CollectMavenPlugin = module.CollectMavenPlugin  # type: ignore[misc]
