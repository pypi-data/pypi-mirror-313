"""Base class for all collector plugins."""

from __future__ import annotations

import os
import socket

from abc import abstractmethod
from datetime import datetime, timezone
from fnmatch import fnmatch
from os import PathLike
from pathlib import Path as Path
from typing import TYPE_CHECKING, final
from urllib.parse import urlparse
from urllib.request import getproxies

import hoppr.net
import hoppr.plugin_utils
import hoppr.utils

from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_ignore_excluded, hoppr_process, hoppr_rerunner
from hoppr.constants import BomProps
from hoppr.models.credentials import CredentialRequiredService, Credentials
from hoppr.models.manifest import SearchSequence
from hoppr.models.sbom import Component, Hash, Property
from hoppr.models.transfer import ComponentCoverage
from hoppr.models.types import BomAccess, PurlType, RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from collections.abc import Iterator

    from packageurl import PackageURL


class BaseCollectorPlugin(
    HopprPlugin,
    default_component_coverage=ComponentCoverage.EXACTLY_ONCE,
    bom_access=BomAccess.COMPONENT_ACCESS,
):
    """Base class for collector plugins."""

    system_repositories: list[str]

    def __init_subclass__(
        cls,
        products: list[str] | None = None,
        required_commands: list[str] | None = None,
        supported_purl_types: list[str] | None = None,
        bom_access: BomAccess | str | None = None,
        process_timeout: int | None = None,
        default_component_coverage: ComponentCoverage | str | None = None,
        system_repositories: list[str] | None = None,
    ) -> None:
        super().__init_subclass__(
            products,
            required_commands,
            supported_purl_types,
            bom_access,
            process_timeout,
            default_component_coverage,
        )

        cls.system_repositories = system_repositories or getattr(cls, "system_repositories", [])

    @staticmethod
    def _get_artifact_hashes(path: Path) -> Iterator[Hash]:
        yield from (
            Hash(alg=cdx_alg, content=hoppr.net.get_file_hash(path, hashlib_alg))
            for cdx_alg, hashlib_alg in hoppr.net.HASH_ALG_MAP.items()
        )

    @staticmethod
    def _get_proxies_for(url: str) -> dict[str, str] | None:
        no_proxy_domains = filter(None, set(f"{os.getenv('no_proxy', '')},{os.getenv('NO_PROXY', '')}".split(",")))

        hostname = RepositoryUrl(url=url).hostname or ""

        try:
            next(pattern for pattern in no_proxy_domains if pattern in hostname or fnmatch(name=hostname, pat=pattern))
            return None
        except StopIteration:
            return getproxies()

    @staticmethod
    def _get_repo_search_list(comp: Component) -> list[str]:
        repo_list: list[str] = []

        for prop in [prop for prop in comp.properties if prop.name == BomProps.COMPONENT_SEARCH_SEQUENCE]:
            search_sequence = SearchSequence.parse_raw(prop.value or "{}")
            repo_list.extend(map(str, search_sequence.repositories))

        return hoppr.utils.dedup_list(repo_list)

    def _get_repos(self, comp: Component) -> list[str]:
        """Returns all repos listed in all BOM_PROPS_COMPONENT_SEARCH_SEQUENCE properties for this component."""
        purl = hoppr.utils.get_package_url(comp.purl)
        purl_url = purl.qualifiers.get("repository_url")

        if purl_url is not None and not self.context.strict_repos:
            return [purl_url] if "https://" in purl_url else [f"https://{purl_url}"]

        repo_list = self._get_repo_search_list(comp)

        if purl_url is not None:
            parsed_purl_url = self._parse_url_for_comparison(purl_url)
            for repo in repo_list:
                parsed_repo_url = self._parse_url_for_comparison(repo)
                if (
                    parsed_repo_url[0] == parsed_purl_url[0]
                    and (not parsed_purl_url[1] or parsed_repo_url[1] == parsed_purl_url[1])
                    and parsed_repo_url[2].startswith(parsed_purl_url[2])
                ):
                    return [purl_url]

            return []

        if not self.context.strict_repos:
            repo_list.extend(self.system_repositories)

        return hoppr.utils.dedup_list(repo_list)

    def empty_repo_list_reason(self, comp: Component) -> str:
        """Returns a reasonable explanation as to why _get_repos returned an empty list."""
        purl = hoppr.utils.get_package_url(comp.purl)

        if not self.context.strict_repos:
            return f"No repositories specified for purl type {purl.type}, and no repository_url specified in purl"

        if len(self._get_repo_search_list(comp)) == 0:
            return (
                f"No repositories specified in manifest for purl type {purl.type}. "
                "Add repositories or use --no-strict command line option"
            )

        if purl.qualifiers.get("repository_url") is not None:
            return (
                f"Specified repository_url ({purl.qualifiers.get('repository_url')}) is not in "
                "manifest repository list.  Add it to the manifest, or use --no-strict command "
                "line option"
            )

        return "Reason for empty repo list undetermined"

    def directory_for(
        self,
        purl_type: str | PurlType,
        repo_url: str,
        subdir: str | PathLike[str] | None = None,
    ) -> Path:
        """Create directory for collected component and return the path."""
        repo_dir = hoppr.plugin_utils.dir_name_from_repo_url(repo_url)
        directory = self.context.collect_root_dir / str(purl_type) / repo_dir / (subdir or "")

        directory.mkdir(parents=True, exist_ok=True)

        return directory

    @staticmethod
    def _parse_url_for_comparison(url: str) -> tuple[str, str, str]:
        """Resulting tuple is (host, port, path)."""
        initial_parse = urlparse(url) if url.startswith("file:") or "//" in url else urlparse(f"//{url}")

        host_data = initial_parse.netloc.split(":")

        host = host_data[0]

        if len(host_data) > 1:
            port = host_data[1]
        elif initial_parse.scheme == "":
            port = ""
        else:
            port = str(socket.getservbyname(initial_parse.scheme))

        path = initial_parse.path.rstrip("/")

        return (host, port, path)

    @staticmethod
    def check_purl_specified_url(purl: PackageURL, repo_url: str) -> Result:
        """Test if a repository_url specified as a purl qualifier is a mis-match with a given repo_url.

        If no repository_url is specified, repo_url is fine, no-mismatch, return False

        Otherwise, considered a match if repo_url starts with the purl url (after trimming trailing
        "/"s and URL scheme, if present)
        """
        purl_url = purl.qualifiers.get("repository_url")
        if purl_url is None:
            return Result.success()

        parsed_purl_url = BaseCollectorPlugin._parse_url_for_comparison(purl_url)
        parsed_repo_url = BaseCollectorPlugin._parse_url_for_comparison(repo_url)

        if (
            parsed_repo_url[0] == parsed_purl_url[0]  # Compare host
            and (not parsed_purl_url[1] or parsed_repo_url[1] == parsed_purl_url[1])  # Compare port if present
            and parsed_repo_url[2].startswith(parsed_purl_url[2])  # Compare initial path
        ):
            return Result.success()

        return Result.fail(f"Purl-specified repository url ({purl_url}) does not match current repo ({repo_url}).")

    def set_collection_params(self, comp: Component, repository: str, artifact_file: Path | str) -> None:
        """Set collection parameters on sbom component."""
        rel_dir = str(Path(artifact_file).parent.relative_to(self.context.collect_root_dir))

        collect_props: dict[str, str] = {
            BomProps.COLLECTION_REPOSITORY: repository,
            BomProps.COLLECTION_DIRECTORY: rel_dir,
            BomProps.COLLECTION_PLUGIN: f"{type(self).__name__}:{self.get_version()}",
            BomProps.COLLECTION_TIMETAG: str(datetime.now(timezone.utc)),
            BomProps.COLLECTION_ARTIFACT_FILE: Path(artifact_file).name,
        }

        for prop in comp.properties:
            if prop.name in collect_props:
                prop.value = collect_props.pop(prop.name)

        for key, value in collect_props.items():
            if value is not None:
                comp.properties.append(Property(name=key, value=value))

    def _check_collection_params(self, result: Result) -> Result:
        """Ensures that all successful collections set the collection parameters."""
        if not result.is_success():
            return result

        if not isinstance(result.return_obj, Component):
            return result.fail(
                f"Collector class {type(self).__name__} process_component method returned a successful result "
                "without updating the BOM component."
            )

        if missing_props := [
            req_prop.value
            for req_prop in [
                BomProps.COLLECTION_REPOSITORY,
                BomProps.COLLECTION_DIRECTORY,
                BomProps.COLLECTION_PLUGIN,
                BomProps.COLLECTION_TIMETAG,
                BomProps.COLLECTION_ARTIFACT_FILE,
            ]
            if req_prop.value not in [prop.name for prop in result.return_obj.properties or []]
        ]:
            return result.fail(
                f"Collector class {type(self).__name__} process_component method returned a successful result "
                f"without updating the following component properties: {', '.join(missing_props)}"
            )

        return result


class SerialCollectorPlugin(BaseCollectorPlugin):
    """Base class for multi-process collector plugins."""

    @abstractmethod
    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """This method should attempt to collect a single component from the specified URL."""

    @final
    @hoppr_ignore_excluded
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """Copy a component to the local collection directory structure.

        A CollectorPlugin will never return a RETRY result, but handles the retry logic internally.
        """
        logger = self.get_logger()

        repo_list = self._get_repos(comp)
        if len(repo_list) == 0:
            return Result.fail(self.empty_repo_list_reason(comp))

        result = Result.skip()
        for repo_url in repo_list:
            logger.info("Repository: %s", repo_url)

            repo_creds = Credentials.find(repo_url)
            result = self.collect(comp, repo_url, repo_creds)

            if result.is_success():
                break  ### We found it, no need to try any more repositories

        return self._check_collection_params(result)

    @hoppr_process
    def post_stage_process(self) -> Result:  # noqa: D102
        self.get_logger().info("Removing empty subdirectories from collection root directory")

        for purl_type in self.supported_purl_types:
            if (directory := self.context.collect_root_dir / purl_type).is_dir():
                hoppr.utils.remove_empty(directory)

        return Result.success()


class BatchCollectorPlugin(BaseCollectorPlugin):
    """Base class for single-process collector plugins."""

    config_file: Path

    @abstractmethod
    @hoppr_rerunner
    def collect(self, comp: Component):
        """This method should attempt to collect all components from any of the specified URLs.

        Manifest repositories or registries should be configured in the pre stage process.
        Use of a single batch operation (i.e. dynamically constructed shell command) is encouraged
        if supported by the underlying collection tool(s).
        """

    @final
    @hoppr_ignore_excluded
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """Copy a component to the local collection directory structure.

        A CollectorPlugin will never return a RETRY result, but handles the retry logic internally.
        """
        logger = self.get_logger()
        logger.info("Processing component %s", comp.purl)

        return self._check_collection_params(self.collect(comp))
