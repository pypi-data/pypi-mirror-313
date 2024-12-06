"""Collector plugin for NuGet packages."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests as requests

from pydantic import SecretStr
from requests.auth import HTTPBasicAuth
from typing_extensions import override

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.result import Result

if TYPE_CHECKING:
    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


class CollectNugetPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["nuget"],
    products=["nuget/*"],
    process_timeout=60,
    system_repositories=["https://www.nuget.org/api/v2/package"],
):
    """Collector plugin for NuGet packages."""

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.manifest_repos: list[str] = []
        self.password_list: list[str] = []

    def get_version(self) -> str:  # noqa: D102
        return __version__

    @override
    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)
        self.get_logger().info(msg=f"Copying Nuget package from {comp.purl}", indent_level=2)

        nuget_url = "/".join([repo_url.rstrip("/"), purl.name, purl.version])

        authentication = None
        if creds is not None and isinstance(creds.password, SecretStr):
            authentication = HTTPBasicAuth(creds.username, creds.password.get_secret_value())
        response = requests.get(nuget_url, auth=authentication, timeout=120, proxies=self._get_proxies_for(repo_url))

        if response.status_code == 404:
            msg = (
                f"NuGet failed to locate package for {comp.purl}, "
                f"return_code={response.status_code}, "
                f"URL should be full domain with path up to package, "
                f"e.g. https://www.nuget.org/api/v2/package"
            )
            self.get_logger().debug(msg=msg, indent_level=2)

            return Result.fail(message=msg)

        if response.status_code not in range(200, 300):
            msg = f"NuGet failed to locate package for {comp.purl}, return_code={response.status_code}"
            self.get_logger().debug(msg=msg, indent_level=2)

            return Result.retry(message=msg)

        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

        package_name = f"{'_'.join(filter(None, [purl.name, purl.version]))}.nupkg"

        package_out_path = target_dir / package_name

        package_out_path.write_bytes(response.content)

        self.set_collection_params(comp, repo_url, package_out_path)
        return Result.success(return_obj=comp)
