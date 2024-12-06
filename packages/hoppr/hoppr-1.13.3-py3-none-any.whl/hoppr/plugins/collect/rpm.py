"""Collector plugin for RPM packages."""

from __future__ import annotations

import gzip
import os
import re
import time
import warnings

from collections import OrderedDict
from configparser import ConfigParser
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Final

import jmespath
import requests
import xmltodict

from pydantic import AnyUrl, Extra, Field, FileUrl, HttpUrl, SecretStr, root_validator, validator
from requests import HTTPError, Response
from requests.auth import HTTPBasicAuth
from typing_extensions import Self, override

import hoppr.net
import hoppr.utils

from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_process, hoppr_rerunner
from hoppr.constants import BomProps
from hoppr.exceptions import HopprExperimentalWarning, HopprPluginError
from hoppr.models import HopprContext
from hoppr.models.base import ExtendedProto, HopprBaseModel
from hoppr.models.credentials import CredentialRequiredService, Credentials
from hoppr.models.manifest import SearchSequence
from hoppr.models.sbom import Component, Hash
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable, MutableMapping

    from packageurl import PackageURL
    from pydantic.typing import DictStrAny
    from rich.repr import RichReprResult


warnings.filterwarnings(action="once", category=HopprExperimentalWarning)
warnings.warn(
    message="The RPM collector plugin is experimental; use at your own risk.",
    category=HopprExperimentalWarning,
    stacklevel=2,
)


def _file_exists(path: Path) -> Path:
    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")

    return path


class RepoConfig(HopprBaseModel, extra=Extra.allow):
    """Configuration options for CollectRpmPlugin."""

    base_url: list[str] = Field(alias="baseurl")
    mirror_list: HttpUrl | FileUrl | AnyUrl | str | None = Field(default=None, alias="mirrorlist")
    enabled: bool = True
    gpg_check: bool = Field(default=True, alias="gpgcheck")
    gpg_key: str | None = Field(default=None, alias="gpgkey")
    name: str | None = None
    priority: int = 1
    proxy: str = "_none_"
    username: str | None = None
    password: str | None = None
    ssl_ca_cert: Path | None = Field(default=None, alias="sslcacert")
    ssl_client_cert: Path | None = Field(default=None, alias="sslclientcert")
    ssl_client_key: Path | None = Field(default=None, alias="sslclientkey")

    vars_dir: ClassVar[Path | None] = None
    base_arch: ClassVar[str | None] = None
    release_ver: ClassVar[str | None] = None

    _validate_ssl_ca_cert = validator("ssl_ca_cert", allow_reuse=True)(_file_exists)
    _validate_ssl_client_cert = validator("ssl_client_cert", allow_reuse=True)(_file_exists)
    _validate_ssl_client_key = validator("ssl_client_key", allow_reuse=True)(_file_exists)

    @validator("base_url", pre=True)
    def _assemble_base_url(cls, base_url: str | list[str]) -> list[str]:
        return [base_url] if isinstance(base_url, str) and not isinstance(base_url, list) else base_url

    @validator("enabled", pre=True)
    def _assemble_enabled(cls, enabled: str | bool | int) -> bool:
        return False if str(enabled).lower() == "false" else bool(enabled)

    @root_validator(allow_reuse=True)
    def _resolve_dnf_vars(cls, values: DictStrAny) -> DictStrAny:
        if cls.vars_dir is not None and not cls.vars_dir.exists():
            return values

        for key, value in values.items():
            if isinstance(value, str):
                value = cls._match_dnf_var(value)
                values[key] = value
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    value[index] = cls._match_dnf_var(item)
                values[key] = value

        return values

    @classmethod
    def _match_dnf_var(cls, content: str) -> str:
        matches = re.findall(r"\$\w+", content)

        for var in matches:
            if var == "$basearch" and cls.base_arch:
                content = content.replace(var, cls.base_arch)
            elif var == "$releasever" and cls.release_ver:
                content = content.replace(var, cls.release_ver)
            elif cls.vars_dir:
                content = content.replace(var, (cls.vars_dir / var.removeprefix("$")).read_text())

        return content


class RepoConfigList(HopprBaseModel):
    """List of RepoConfig objects."""

    __root__: list[RepoConfig]

    def __getitem__(self, idx: int) -> RepoConfig:
        return self.__root__[idx]  # pragma: no cover

    def __init__(self, issues: Iterable[RepoConfig] | None = None, **data):
        data["__root__"] = data.get("__root__", list(issues or []))
        super().__init__(**data)

    def __iter__(self):
        yield from self.__root__

    def __len__(self) -> int:
        return len(self.__root__)  # pragma: no cover

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__root__})"  # pragma: no cover

    def __rich_repr__(self) -> RichReprResult:
        yield self.__root__  # pragma: no cover

    def append(self, item: RepoConfig) -> None:
        """Append object to the end of the list."""
        self.__root__.append(item)  # pragma: no cover

    def extend(self, iterable: Iterable[RepoConfig]) -> None:
        """Extend list by appending elements from the iterable."""
        self.__root__.extend(iterable)  # pragma: no cover

    @classmethod
    def parse_file(
        cls,
        path: str | Path,
        *,
        content_type: str | None = None,
        encoding: str = "utf-8",
        proto: ExtendedProto | None = None,
        allow_pickle: bool = False,
    ) -> Self:
        """Parse a .repo file."""
        parser = ConfigParser()
        parser.read(path)

        repo_config_list = cls()

        # Use ConfigParser to parse values in file into new object
        for section in parser.sections():
            if bool(parser[section].get("enabled", None)):
                repo_config_list.append(RepoConfig.parse_obj(dict(parser[section])))

        return repo_config_list


class CollectRpmConfig(HopprBaseModel):
    """Configuration options for CollectRpmPlugin."""

    base_arch: str | None = Field(default=None, description="Value for $basearch in repository configs")
    release_ver: str | None = Field(default=None, description="Value for $releasever in repository configs")
    vars_dir: Path | None = Field(
        default=next((Path("/", "etc", name, "vars") for name in ["dnf", "yum"]), None),
        description="DNF variable definitions directory.",
    )


class CollectRpmPlugin(
    SerialCollectorPlugin,
    products=["rpm/*"],
    supported_purl_types=["rpm"],
    system_repositories=[],
):
    """Collector plugin for RPM packages."""

    REQUEST_RETRIES: Final[int] = 3
    REQUEST_RETRY_INTERVAL: Final[float] = 5
    REQUEST_TIMEOUT: Final[float] = 60

    rpm_data: ClassVar[MutableMapping[str, OrderedDict[str, Any]]] = {}

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.collector_config = CollectRpmConfig(**(config or {}))
        self.repo_configs = RepoConfigList()

    def get_version(self) -> str:
        """Get plugin version."""
        return hoppr.__version__

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

    def _download_component(
        self,
        download_url: str,
        dest_file: Path,
        creds: CredentialRequiredService | None = None,
        cert: tuple[str, str] | None = None,
    ):
        self.get_logger().info(msg="Downloading RPM package:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {dest_file}", indent_level=3)

        # Download the RPM file to the target directory
        response = hoppr.net.download_file(
            url=download_url,
            dest=str(dest_file),
            creds=creds,
            proxies=self._get_proxies_for(download_url),
            cert=cert,
        )

        if not (download_result := Result.from_http_response(response=response)).is_success():
            raise HopprPluginError(download_result.message)

    def _determine_sha_hash_alg(self, hash_alg: str, hash_string: str) -> hoppr.net.HashlibAlgs:
        """Determine type of sha hash if not specified."""
        match len(hash_string):
            case 32:
                return "md5"
            case 40:
                return "sha1"
            case 56:
                return "sha224"
            case 64:
                return "sha256"
            case 96:
                return "sha384"
            case 128:
                return "sha512"
            case _:
                raise HopprPluginError(f'Could not determine hash algorithm for hash type "{hash_alg}"')

    def _get_download_url(self, purl: PackageURL, repo_url: str) -> tuple[str, hoppr.net.HashlibAlgs, str]:
        """Get information required to download and verify an RPM package.

        Args:
            purl: PackageURL of component attributes
            repo_url: The RPM repository URL

        Returns:
            Tuple containing download URL, hash algorithm, and checksum string.

        Raises:
            HopprPluginError: malformed/missing `purl.version`, or component not found in repodata
        """
        try:
            rpm_version, rpm_release = purl.version.split("-")
        except (AttributeError, ValueError) as ex:
            raise HopprPluginError(f"Failed to parse version string from PURL: '{purl}'") from ex

        arch = purl.qualifiers.get("arch") or "noarch"

        if (check_result := self.check_purl_specified_url(purl, repo_url)).is_fail():
            if self.context.strict_repos:
                raise HopprPluginError(check_result.message)

            repo_url = purl.qualifiers.get("repository_url", repo_url)
            self._populate_rpm_data(RepositoryUrl(url=repo_url))

        self.get_logger().debug("Searching RPM data for package with attributes:", indent_level=2)
        self.get_logger().debug("name:    %s", purl.name, indent_level=3)
        self.get_logger().debug("version: %s", rpm_version, indent_level=3)
        self.get_logger().debug("release: %s", rpm_release, indent_level=3)
        self.get_logger().debug("arch:    %s", arch, indent_level=3)

        component_data = jmespath.search(
            expression=f"""
                metadata.package[? name=='{purl.name}' &&
                version."@ver"=='{rpm_version}' &&
                version."@rel"=='{rpm_release}' &&
                (arch=='{arch}' || arch=='noarch')] | [0]
            """,
            data=self.rpm_data[repo_url],
        )

        if not component_data:
            raise HopprPluginError(f"RPM package not found in repository: '{purl}'")

        download_url, hash_alg, hash_string = jmespath.search(
            expression='[location."@href", checksum."@type", checksum."#text"]',
            data=component_data,
        )

        download_url = f"{repo_url}/{download_url}"

        if hash_alg not in hoppr.net.HASH_ALG_MAP.values():
            self._logger.info('Unknown hash algorithm "%s". Attempting to resolve', hash_alg, indent_level=1)
            try:
                hash_alg = self._determine_sha_hash_alg(hash_alg, hash_string)
                self._logger.info('Resolved hash algorithm to "%s"', hash_alg, indent_level=1)
            except HopprPluginError as e:
                raise HopprPluginError(e) from e

        return download_url, hash_alg, hash_string

    def _get_primary_xml_data(
        self,
        repo_url: RepositoryUrl,
        repomd_dict: OrderedDict[str, Any],
        auth: HTTPBasicAuth | None = None,
        cert: tuple[str, str] | None = None,
    ) -> OrderedDict[str, Any]:
        primary_xml_url = jmespath.search(
            expression="""repomd.data[? "@type"=='primary'].location."@href" | [0]""",
            data=repomd_dict,
        )

        primary_xml_url = repo_url / primary_xml_url

        try:
            response = self._stream_url_data(url=primary_xml_url, auth=auth, cert=cert)
        except HTTPError as ex:
            raise HopprPluginError(f"Failed to get primary XML data from {primary_xml_url}") from ex

        data: OrderedDict[str, Any] = OrderedDict()

        # Parse primary XML data to dict
        for chunk in response.iter_content(chunk_size=None):
            data = xmltodict.parse(xml_input=gzip.decompress(chunk), force_list=["package"])

        return data

    def _get_repodata(
        self, repo_url: RepositoryUrl, auth: HTTPBasicAuth | None = None, cert: tuple[str, str] | None = None
    ) -> OrderedDict[str, Any]:
        repomd_url = repo_url / "repodata" / "repomd.xml"

        try:
            response = self._stream_url_data(url=repomd_url, auth=auth, cert=cert)
        except HTTPError as ex:
            raise HopprPluginError(f"Failed to get repository metadata from {repo_url}") from ex

        repomd_dict: OrderedDict[str, Any] = xmltodict.parse(xml_input=response.text, force_list=["data"])

        # Download all metadata files listed in repomd.xml to bundle directory for this repo
        metadata_files = jmespath.search(expression='repomd.data[].location."@href"', data=repomd_dict)
        repodata_dir = self.directory_for(purl_type="rpm", repo_url=str(repo_url), subdir="repodata")

        for metadata_file in metadata_files:
            self.get_logger().debug("Downloading %s", metadata_file, indent_level=2)
            hoppr.net.download_file(url=str(repo_url / metadata_file), dest=str(repodata_dir.parent / metadata_file))

        return repomd_dict

    def _populate_rpm_data(self, repo_url: RepositoryUrl) -> None:
        """Populate `rpm_data` dict for a repository.

        Args:
            repo_url (str): The RPM repository URL
        """
        if type(self).rpm_data.get(f"{repo_url}"):
            return

        self.get_logger().debug("Populating RPM data for repository: %s", repo_url, indent_level=1)

        auth: HTTPBasicAuth | None = None

        if (creds := Credentials.find(f"{repo_url}")) and isinstance(creds.password, SecretStr):
            auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())
            self.repo_configs.append(
                RepoConfig(
                    base_url=[str(repo_url)], username=creds.username, password=creds.password.get_secret_value()
                )
            )
        else:
            self.repo_configs.append(
                RepoConfig(
                    base_url=[str(repo_url)],
                )
            )

        cert = None
        for repo in self.repo_configs:
            for url in repo.base_url:
                if url in f"{repo_url}":
                    if repo.ssl_client_cert and repo.ssl_client_key:
                        cert = (str(repo.ssl_client_cert), str(repo.ssl_client_key))
                    elif repo.username and repo.password:
                        auth = HTTPBasicAuth(username=repo.username, password=repo.password)

        try:
            repomd_dict: OrderedDict[str, Any] = self._get_repodata(repo_url, auth=auth, cert=cert)
            primary_xml_data: OrderedDict[str, Any] = self._get_primary_xml_data(repo_url, repomd_dict, auth, cert)
        except HopprPluginError as ex:
            raise ex

        type(self).rpm_data[f"{repo_url}"] = primary_xml_data

    def _stream_url_data(
        self,
        url: RepositoryUrl,
        auth: HTTPBasicAuth | None = None,
        cert: tuple[str, str] | None = None,
    ) -> Response:
        """Stream download data from specified URL.

        Args:
            url: URL of remote resource to stream.
            auth: Basic authentication if required by URL. Defaults to None.
            cert: Certificate and key to use for request. Defaults to None.

        Raises:
            HTTPError: Failed to download resource after 3 attempts.

        Returns:
            The web request response.
        """
        response = Response()

        for _ in range(self.REQUEST_RETRIES):
            response = requests.get(
                url=f"{url}",
                auth=auth,
                stream=True,
                timeout=self.REQUEST_TIMEOUT,
                proxies=self._get_proxies_for(f"{url}"),
                cert=cert,
            )

            try:
                response.raise_for_status()
                return response
            except HTTPError:
                time.sleep(self.REQUEST_RETRY_INTERVAL)

        raise HTTPError(f"Failed to retrieve data from {url}", response=response)

    @hoppr_process
    @hoppr_rerunner
    def pre_stage_process(self) -> Result:  # sourcery skip: use-named-expression
        """Populate RPM data mapping for repositories."""
        # Get all repository search sequences from all components
        results: list[str] = jmespath.search(
            expression=f"""
                components[*] | [?
                    type != 'operating-system' &&
                    not_null(purl) &&
                    starts_with(purl, 'pkg:rpm')
                ].properties[] | [?
                    name=='{BomProps.COMPONENT_SEARCH_SEQUENCE.value}'
                ].value
            """,
            data=self.context.consolidated_sbom.dict(),
        )

        # Parse and flatten repositories from component search sequence JSON strings, then remove duplicates
        search_repos = hoppr.utils.dedup_list([
            str(repo) for result in results for repo in SearchSequence.parse_raw(result).repositories
        ])

        for repo_url in [RepositoryUrl(url=url) for url in search_repos]:
            self._populate_rpm_data(repo_url)

        # Get all system-managed .repo files and append urls to system repositories
        if self._get_repo_files():
            base_urls = [url for repo in self.repo_configs for url in repo.base_url]
            for url in base_urls:
                type(self).system_repositories.append(url)
                self._populate_rpm_data(RepositoryUrl(url=url))

        return Result.success()

    def _get_repo_files(self) -> Generator[Path, None, None] | None:
        """Return a list of the system repo files and update the plugin repo config."""
        repo_files = None

        if not self.context.strict_repos and os.name != "nt":
            # Set RepoConfig class variables
            RepoConfig.base_arch = self.collector_config.base_arch
            RepoConfig.release_ver = self.collector_config.release_ver
            RepoConfig.vars_dir = self.collector_config.vars_dir

            # Get all system-managed .repo files
            repo_files = Path("/", "etc", "yum.repos.d").glob("*.repo")

            for file in repo_files:
                self.repo_configs.extend(RepoConfigList.parse_file(file))

        return repo_files

    def _validate_hashes(self, package_hash: Hash, comp: Component):
        """Validate generated hash to the RPM package hash.

        Args:
            package_hash: hash pulled from the package file
            comp: Component object whose name will be referenced in case of an error
        Raises:
            HopprPluginError: raise HopprPluginError in case of hash mismatch.
        """
        if all(package_hash != comp_hash for comp_hash in comp.hashes):
            raise HopprPluginError(f"Hash for {comp.name} does not match expected hash.")

    @override
    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        purl = hoppr.utils.get_package_url(comp.purl)

        try:
            download_url, hash_alg, hash_string = self._get_download_url(purl=purl, repo_url=repo_url)
        except HopprPluginError as ex:
            return Result.retry(message=str(ex))

        target_dir = self.directory_for(
            purl_type="rpm",
            repo_url=repo_url,
            subdir=Path(download_url).parent.relative_to(repo_url),
        )

        dest_file = target_dir / Path(download_url).name

        cert = None

        # Obtain cert from local repositories
        repo_files = self._get_repo_files()
        if repo_files is not None:
            for repo in self.repo_configs:
                for url in repo.base_url:
                    if url in f"{repo_url}" and repo.ssl_client_cert and repo.ssl_client_key:
                        cert = (str(repo.ssl_client_cert), str(repo.ssl_client_key))

        try:
            self._download_component(download_url, dest_file, creds, cert)
            self._update_hashes(comp, dest_file)
            self._validate_hashes(
                Hash(
                    alg=next(key for key, value in hoppr.net.HASH_ALG_MAP.items() if value == hash_alg),
                    content=hash_string,
                ),
                comp,
            )
        except (HopprPluginError, ValueError) as ex:
            return Result.fail(message=str(ex))

        self.set_collection_params(comp, repo_url, target_dir)

        return Result.success(return_obj=comp)
