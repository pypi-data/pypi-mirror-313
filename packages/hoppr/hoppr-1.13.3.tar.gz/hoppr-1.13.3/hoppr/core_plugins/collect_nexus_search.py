"""Collector plugin to copy artifacts using the Nexus API."""

from __future__ import annotations

import re
import time

from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import jmespath
import requests

from pydantic import SecretStr
from requests.auth import HTTPBasicAuth

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models.types import PurlType, RepositoryUrl
from hoppr.net import download_file
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL

    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


class CollectNexusSearch(
    SerialCollectorPlugin,
    # Unless specified by the user, all types except `git`, `github`, and `gitlab` are supported
    supported_purl_types=[value for value in PurlType.values() if value not in {"git", "github", "gitlab"}],
):
    """Class to copy artifacts using the Nexus API."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.supported_purl_types = (self.config or {}).get("purl_types", type(self).supported_purl_types)

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Collect artifact from Nexus."""
        auth: HTTPBasicAuth | None = None
        if creds is not None and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())

        nexus_url = self._parse_nexus_url(repo_url)[0]

        if not CollectNexusSearch.is_nexus_instance(nexus_url, auth):
            return Result.fail(f"{nexus_url} is not a Nexus instance")

        purl = hoppr.utils.get_package_url(comp.purl)

        try:
            source_urls = self.get_download_urls(purl, repo_url, auth)
        except ValueError as ex:
            self.get_logger().error(msg=str(ex))
            return Result.fail(message=str(ex))

        if not source_urls:
            msg = f"No artifacts found in Nexus instance {repo_url} for purl {comp.purl}"
            self.get_logger().error(msg, indent_level=2)
            return Result.fail(msg)

        target_dir = self._directory_for_nexus(purl, source_urls[0])

        for source_url in source_urls:
            self.get_logger().info(
                msg=f"Collecting from {source_url}",
                indent_level=2,
            )

            file_name = Path(urlparse(source_url).path).parts[-1]

            response = download_file(source_url, str(target_dir / file_name))
            nexus_result = Result.from_http_response(response)

            self.get_logger().info("Download Result: %s", nexus_result, indent_level=3)

            if not nexus_result.is_success():
                return nexus_result

        self.set_collection_params(comp, repo_url, target_dir / file_name)
        return Result.success(return_obj=comp)

    @staticmethod
    def _parse_nexus_url(repo_url: str) -> tuple[str, str | None]:
        nexus_url = repo_url
        nexus_repo = None
        if repo_specified := re.search(r"(https?://.*?)/repository/([^/]*)/?.*$", nexus_url):
            nexus_url = repo_specified[1]
            nexus_repo = repo_specified[2]

        return nexus_url, nexus_repo

    def _directory_for_nexus(self, purl: PackageURL, url: str) -> Path:
        nexus_repo = ""
        path = ""
        if repo_match := re.search(r"(.*?/repository/.*?)(/.*)?/(.*)", url):
            nexus_repo = repo_match[1]
            path = repo_match[2]
            if path is not None:
                path = path[1:]

        subdir = None
        match purl.type:
            case "docker" | "generic" | "maven" | "raw" | "rpm":
                subdir = path
            case "helm" | "pypi":
                subdir = f"{purl.name}_{purl.version}"

        return self.directory_for(purl.type, nexus_repo, subdir=subdir)

    @staticmethod
    def is_nexus_instance(repo_url: str, auth: HTTPBasicAuth | None = None) -> bool:
        """Checks whether or not the repo_url refers to a Nexus instance."""
        test_url = RepositoryUrl(url=repo_url) / "service" / "rest" / "v1" / "status"

        for attempt in range(3):
            if attempt > 0:
                time.sleep(5)

            response = requests.get(
                f"{test_url}",
                auth=auth,
                allow_redirects=True,
                stream=True,
                verify=True,
                timeout=60,
            )

            if response.status_code < 300:
                return True
            if response.status_code < 500:
                return False

        return False

    @staticmethod
    def _get_search_params(purl: PackageURL, nexus_repo: str | None) -> tuple[dict[str, str], list[dict[str, str]]]:
        """Returns search parameters for `get_download_urls`.

        Args:
            purl: Package URL object.
            nexus_repo: Nexus repository URL.

        Returns:
            Base parameters and additional search parameters for `get_download_urls`.
        """
        additional_search_params: list[dict[str, str]] = [{}]

        match purl.type:
            case "deb":
                nexus_format = "apt"
            case "gem":
                nexus_format = "rubygems"
            case "golang":
                nexus_format = "go"
            case "generic" | "raw":
                nexus_format = "raw"
            case "maven":
                nexus_format = "maven2"
                additional_search_params = [
                    {"maven.extension": "jar", "maven.classifier": ""},
                    {"maven.extension": "jar", "maven.classifier": "sources"},
                    {"maven.extension": "pom"},
                ]
            case "rpm" | "yum":
                nexus_format = "yum"
                arch = purl.qualifiers.get("arch")
                additional_search_params = [{"yum.architecture": arch}] if arch is not None else [{}]
            case _:
                nexus_format = purl.type

        base_params = {"sort": "version", "name": purl.name, "format": nexus_format}

        if purl.version is not None:
            base_params["version"] = purl.version

        if nexus_repo is not None:
            base_params["repository"] = nexus_repo

        return base_params, additional_search_params

    def get_download_urls(self, purl: PackageURL, repo_url: str, auth: HTTPBasicAuth | None = None) -> list[str]:
        """Retrieves all urls to be retrieved from Nexus for this component."""
        nexus_url, nexus_repo = CollectNexusSearch._parse_nexus_url(repo_url)
        search_url = RepositoryUrl(url=nexus_url) / "service" / "rest" / "v1" / "search" / "assets"

        base_params, additional_search_params = self._get_search_params(purl, nexus_repo)

        url_list: list[str] = []

        for extra_search_params in additional_search_params:
            response = requests.get(
                f"{search_url}",
                auth=auth,
                allow_redirects=True,
                stream=True,
                verify=True,
                timeout=60,
                params=base_params | extra_search_params,
            )

            try:
                response.raise_for_status()
            except requests.HTTPError:
                continue

            download_urls: list[str] = jmespath.search(
                expression=f"items[].downloadUrl | [? starts_with(@, '{repo_url}')]",
                data=response.json(),
            )

            match download_urls:
                case [url]:
                    url_list.append(url)
                case [url, *extra] if extra:
                    disambiguated_download_urls = _disambiguate_urls(repo_url, download_urls)
                    download_urls_bullets = "\n".join(f"  \u2022\u00a0{url}" for url in disambiguated_download_urls)

                    raise ValueError(
                        f'More than one result found for "{purl.name}" when searching "{repo_url}". '
                        "Please include a more specific repository URL in your manifest file. "
                        f"Either one of these should work:\n{download_urls_bullets}\n"
                    )
                case []:
                    self.get_logger().warning(
                        'No results found for "%s" when searching "%s".', purl.name, repo_url, indent_level=2
                    )

                    self.get_logger().debug("response:", indent_level=2)
                    self.get_logger().debug("url: %s", response.url, indent_level=3)
                    self.get_logger().debug("status code: %s", response.status_code, indent_level=3)
                    self.get_logger().debug("content: %s", response.content, indent_level=3)

        return url_list

    @classmethod
    def get_attestation_products(cls, config: dict | None = None) -> list[str]:  # noqa: D102
        products: list[str] = []

        if config is not None and "purl_types" in config:
            products.extend(f"{purl_type}/*" for purl_type in config["purl_types"])
        else:
            products.extend(
                f"{purl_type}/*" for purl_type in PurlType if str(purl_type) not in ["git", "github", "gitlab"]
            )

        return products


def _disambiguate_urls(base_url: str, urls: list[str]) -> list[str]:
    """Trims the URLs in the provided list after their first unambiguous subdirectory.

    Args:
        base_url: Known commonly-shared starting substring between the provided URLs.
        urls: URLs to disambiguate. Each URL is assumed to start with `base_url`, have one or
            more subdirectories and end with a filename.

    Raises:
        ValueError: If the URLs cannot be disambiguated.

    Returns:
        The provided URLs until their first unambiguous subdirectory.
    """
    ambiguous_paths: list[list[str]] = []
    max_length = 0
    disambiguated_urls: list[str] = []
    base_url = base_url.rstrip("/")

    for url in urls:
        _, *subdirectories, _ = url.removeprefix(base_url).split("/")
        max_length = max(max_length, len(subdirectories))
        ambiguous_paths.append(subdirectories)

    for level in range(max_length):
        not_repeated: dict[str, list[str]] = {}
        for path in ambiguous_paths:
            if len(path) <= level:
                raise ValueError("Repository URLs could not be disambiguated.")

            not_repeated[path[level]] = path if path[level] not in not_repeated else []

        for path in filter(None, not_repeated.values()):
            disambiguated_urls.append("/".join([base_url, *path[: level + 1]]))
            ambiguous_paths.remove(path)

    if ambiguous_paths:
        raise ValueError("Repository URLs could not be disambiguated.")

    return disambiguated_urls
