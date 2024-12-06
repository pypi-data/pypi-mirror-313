"""Collector plugin for docker images."""

from __future__ import annotations

import json
import re
import urllib.parse

from base64 import b64encode
from pathlib import Path
from subprocess import CalledProcessError
from types import NoneType
from typing import TYPE_CHECKING, Final

import jmespath

from oras.container import Container
from pydantic import SecretStr
from requests import HTTPError

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.constants import BomProps
from hoppr.core_plugins.oras_registry import Registry
from hoppr.exceptions import HopprPluginError
from hoppr.models.sbom import Property
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL

    from hoppr.models import HopprContext
    from hoppr.models.credentials import CredentialRequiredService
    from hoppr.models.sbom import Component


ALLOWED_MEDIA_TYPES: Final[str] = (
    "application/vnd.oci.image.index.v1+json,"
    "application/vnd.docker.distribution.manifest.v2+json,"
    "application/vnd.oci.image.manifest.v1+json"
)

_ANNOTATION_BUNDLE = "dev.sigstore.cosign/bundle"
_ANNOTATION_CERTIFICATE = "dev.sigstore.cosign/certificate"
_ANNOTATION_CHAIN = "dev.sigstore.cosign/chain"
_ANNOTATION_SIGNATURE = "dev.cosignproject.cosign/signature"

_ANNOTATION_EXT_MAP: Final[dict] = {
    _ANNOTATION_BUNDLE: ".bundle",
    _ANNOTATION_CHAIN: ".chain",
}

_ANNOTATION_JSON_EXT_MAP: Final[dict] = {
    _ANNOTATION_SIGNATURE: ".sig",
    _ANNOTATION_CERTIFICATE: ".pem",
}


class CollectDockerPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["docker", "oci"],
    required_commands=["skopeo"],
    products=["docker/*", "oci/*"],
    process_timeout=300,
    system_repositories=["https://docker.io/"],
):
    """Collector plugin for docker images."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)
        self.required_commands = (self.config or {}).get("skopeo_command", self.required_commands)

    def _download_package(
        self,
        purl: PackageURL,
        repo_url: str,
        package_str: str,
        dest_file: Path,
        creds: CredentialRequiredService | None,
    ):
        """Downloads a Docker package from a specific repo via Skopeo.

        Args:
            purl: Used to identify the package in the logs and check against purl version
            repo_url: Designates registry to pull package from
            package_str: Docker container to be downloaded.
            dest_file: Where the package will be downloaded to.
            creds: Credentials used for the HTTP request.

        Raises:
            HopprPluginError: If package download fails.
        """
        command = [
            self.required_commands[0],
            "copy",
            "--additional-tag",
            f"{purl.name}:{purl.version.replace(':', '')}",
        ]
        password_list = []

        if creds is not None and isinstance(creds.password, SecretStr):
            password_list = [creds.password.get_secret_value()]
            command = [*command, "--src-creds", f"{creds.username}:{creds.password.get_secret_value()}"]

        if re.match("^http://", repo_url):
            command = [*command, "--src-tls-verify=false"]

        if self.get_logger().is_verbose():
            command = [*command, "--debug"]

        command = [
            *command,
            urllib.parse.unquote(package_str),
            f"{purl.type}-archive:{dest_file}",
        ]
        copy_result = self.run_command(command, password_list)

        try:
            copy_result.check_returncode()
        except CalledProcessError as ex:
            msg = f"Skopeo failed to copy {purl.type} image to {dest_file}, return_code={copy_result.returncode}"
            self.get_logger().error(msg=msg, indent_level=2)
            raise HopprPluginError(msg) from ex

    def _prep_headers(self, client: Registry, creds: CredentialRequiredService | None) -> dict:
        client.set_header("Authorization", None)
        auth_header = {"Authorization": None}
        accept_header = {"Accept": ALLOWED_MEDIA_TYPES}

        if creds is not None and isinstance(creds.password, SecretStr):
            client.auth.set_basic_auth(creds.username, creds.password.get_secret_value())
            basic_auth = b64encode(f"{(creds.username)}:{creds.password.get_secret_value()}".encode()).decode("utf-8")
            client.set_header("Authorization", f"Basic {basic_auth}")

            auth_header = client.auth.get_auth_header()

        return accept_header | auth_header

    def _get_digest(self, client: Registry, container: Container, creds: CredentialRequiredService | None) -> str:
        """Retrieves Digest for Docker package from a specific registry.

        Args:
            client: Oras Registry Object used to call do_request
            container: Oras Container Object of Docker Package
            creds: User Configured Credentials for making requests

        Raises:
            HopprPluginError: If digest retrieval fails.
        """
        headers = self._prep_headers(client=client, creds=creds)

        get_digest = (
            f"{client.prefix}://{container.registry}/v2/{container.api_prefix}"
            f"/manifests/{container.digest or container.tag}"
        )

        try:
            response = client.do_request(get_digest, "GET", headers=headers)
            response.raise_for_status()
            return response.headers.get("Docker-Content-Digest") or ""
        except (ValueError, HTTPError) as ex:
            msg = f"Failed to retrieve Digest for {container.repository}"
            self.get_logger().warning(msg=msg, indent_level=2)
            raise HopprPluginError(msg) from ex

    def _get_signature_manifest(
        self, client: Registry, container: Container, digest: str, creds: CredentialRequiredService | None
    ) -> str:
        """Retrieves signature Manifest for Docker package from a specific registry.

        Returns empty string if no signature manifest found.

        Args:
            client: Oras Registry Object used to call do_request
            container: Oras Container Object of Docker Package
            digest: Digest string for Docker package
            creds: User Configured Credentials for making requests
        """
        headers = self._prep_headers(client=client, creds=creds)
        digest = digest.replace(":", "-")
        get_signature_manifest = (
            f"{client.prefix}://{container.registry}/v2/{container.api_prefix}/manifests/{digest}.sig"
        )
        response = client.do_request(get_signature_manifest, "GET", headers=headers)
        return response.content if response.status_code == 200 else ""

    def _get_oras_container(self, purl: PackageURL, repo_url: str) -> Container:
        """Parses Purl/Repo information to create Oras container Object.

        Args:
            purl: PackageURL for Docker Component
            repo_url: Repo for Docker Package
        """
        version = re.sub(
            pattern=r"^(sha256:)?([a-f0-9]{64})$", repl=r"sha256:\2", string=urllib.parse.unquote(purl.version)
        )

        if (repo := re.sub(r"^https?://", "", repo_url)) == "docker.io":
            return Container(name=f"index.{repo}/{purl.namespace or 'library'}/{purl.name}@{version}")

        return Container(name=f"{repo}/{f'{purl.namespace}/' if purl.namespace else ''}{purl.name}@{version}")

    def _parse_manifest(self, manifest: str, dest_file: Path, digest: str):
        """Parses signature manifest file for Docker package to check for signature entries.

        Args:
            manifest: manifest file containing signature blob shas
            dest_file: path to download files to
            digest: digest to write to json file
        """
        manifest_json = json.loads(manifest)
        # Get all signature layers
        layers = jmespath.search(
            expression="layers[? mediaType == 'application/vnd.dev.cosign.simplesigning.v1+json']",
            data=manifest_json,
        )

        for layer in layers:
            # Get the signature layer's index in the manifest's full `layers` list
            idx = manifest_json.get("layers", []).index(layer)
            self._create_signature_files(layer.get("annotations", {}), dest_file, idx, digest)

    def _create_signature_files(self, annotations_field: dict[str, str], dest_file: Path, index: int, digest: str):
        """Creates signature related files from annotation fields if appropriate.

        Args:
            annotations_field: json encoded string of signature manifest layer annotation field
            index: differentiates multiple of the same file types if more than on signature is present
            dest_file: path to download files to
            digest: digest to write to json file
        """
        qualifier = f"-{index}" if index else ""
        file = f"{dest_file}{qualifier}"

        for field, ext in _ANNOTATION_EXT_MAP.items():
            if found_value := annotations_field.get(field):
                Path(f"{file}{ext}").write_text(found_value, encoding="utf-8")

        for field, ext in _ANNOTATION_JSON_EXT_MAP.items():
            if found_value := annotations_field.get(field):
                Path(f"{file}.json{ext}").write_text(found_value, encoding="utf-8")

        Path(f"{file}.json").write_text(digest, encoding="utf-8")

    def _get_package_signatures(
        self,
        repo_url: str,
        purl: PackageURL,
        dest_file: Path,
        creds: CredentialRequiredService | None,
    ):
        """Attempts to collect signature files for a given component.

        Args:
            repo_url: Repo for Docker Package
            purl: PackageURL for Docker Component
            dest_file: Path of file to write signature to
            creds: Credentials to use with registry.

        Raises:
            HopprPluginError: If collection fails, but a lack of signatures is not a failure
        """
        client = Registry(hostname=re.sub(r"^https?://", "", repo_url), auth_backend="basic", logger=self.get_logger())
        container = self._get_oras_container(purl, repo_url)

        try:
            if digest := self._get_digest(client, container, creds):
                if signature_manifest := self._get_signature_manifest(client, container, digest, creds):
                    for layer in jmespath.search(expression="layers", data=json.loads(signature_manifest)):
                        blob = (
                            client.get_blob(
                                container=container,
                                digest=layer.get("digest"),
                            )
                        ).text
                        self._parse_manifest(signature_manifest, dest_file, blob)
                else:
                    self.get_logger().info(f"No signatures to collect for {purl}.")
        except HopprPluginError:
            self.get_logger().warning(f"Failed to collect signatures for {purl}.")

    def _get_image(self, url: str, purl: PackageURL) -> RepositoryUrl:
        """Return the image details for skopeo to process.

        Args:
            url (str): Repository URL
            purl (PackageURL): Purl of component to operate on

        Returns:
            RepositoryUrl: Image information
        """
        # Determine if purl version contains SHA string, determine proper formatting for skopeo command
        match purl.version:
            case NoneType():
                raise HopprPluginError(f"Missing `version` from purl string: {purl}. Must be a valid tag or digest")
            case no_sha if re.search(r"^(sha256:)?[a-fA-F0-9]{12,64}$", no_sha) is None:
                image_name = f"{purl.name}:{purl.version}"
            case sha if sha.startswith("sha256:"):
                image_name = f"{purl.name}@{purl.version}"
            case _:
                image_name = f"{purl.name}@sha256:{purl.version}"

        if purl.type == "oci" and "repository_url" in purl.qualifiers:
            url = purl.qualifiers.get("repository_url", "")

        source_image = RepositoryUrl(url=url) / (purl.namespace or "") / urllib.parse.quote_plus(image_name)

        if source_image.scheme != "docker":
            source_image = RepositoryUrl(url="docker://" + re.sub(r"^(.*://)", "", str(source_image)))

        return source_image

    def _get_target_path(self, repo_url: str, purl: PackageURL) -> Path:
        """Get target path for image download.

        Args:
            repo_url (str): Repository URL
            purl (PackageURL): Purl of component to operate on

        Returns:
            Path: Filesystem location for downloaded image
        """
        version = re.sub(pattern=r"^(sha256:)?([a-f0-9]{64})$", repl=r"sha256:\2", string=purl.version)

        version = urllib.parse.quote_plus(re.sub(r"^https?://", "", version))
        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

        return target_dir / f"{purl.name}@{version}"

    def _inspect_image(self, source_image: RepositoryUrl, purl: PackageURL) -> Result:
        """Verify provided image tag digest matches PURL version.

        Args:
            source_image (RepositoryUrl): Full image name
            purl (PackageURL): Purl of component to operate on

        Returns:
            Result: The result of the verification
        """
        image_prefix, _ = source_image.url.rsplit("/", maxsplit=1)
        image_id = f"{purl.name}:{purl.qualifiers.get('tag')}"

        command = [self.required_commands[0], "inspect", "--format", "{{.Digest}}", f"{image_prefix}/{image_id}"]
        inspect_command = self.run_command(command)

        try:
            inspect_command.check_returncode()
            sha_tag = inspect_command.stdout.decode().strip()
        except CalledProcessError:
            return Result.retry(message=f"Failed to get image digest for '{source_image}'")

        if sha_tag != purl.version:
            return Result.fail(
                message=f"Provided tag '{purl.qualifiers.get('tag')}' image digest does not match '{purl.version}'"
            )

        return Result.success()

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredentialRequiredService | None = None) -> Result:
        """Copy a component to the local collection directory structure."""
        purl = hoppr.utils.get_package_url(comp.purl)

        try:
            source_image = self._get_image(url=repo_url, purl=purl)
        except HopprPluginError as ex:
            self._logger.error("%s", ex)
            self._logger.debug("purl.type:       %s", purl.type, indent_level=2)
            self._logger.debug("purl.name:       %s", purl.name, indent_level=2)
            self._logger.debug("purl.namespace:  %s", purl.namespace, indent_level=2)
            self._logger.debug("purl.version:    %s", purl.version, indent_level=2)
            self._logger.debug("purl.qualifiers: %s", purl.qualifiers, indent_level=2)

            return Result.fail(return_obj=comp, message=f"{ex}")

        target_path = self._get_target_path(repo_url, purl)
        package_out_path = target_path.parent / f"{purl.name}@{purl.version}"

        if (
            purl.type == "oci"
            and "tag" in purl.qualifiers
            and not (inspect_result := self._inspect_image(source_image, purl)).is_success()
        ):
            return inspect_result

        self._logger.info(msg=f"Copying {purl.type} image:", indent_level=2)
        self._logger.info(msg=f"source: {source_image}", indent_level=3)
        self._logger.info(msg=f"destination: {target_path}", indent_level=3)

        try:
            self._download_package(purl, repo_url, source_image.url, target_path, creds)
            self._get_package_signatures(repo_url, purl, package_out_path, creds)

        except HopprPluginError as ex:
            self._logger.info(msg="Artifact collection failed, deleting file and retrying", indent_level=2)
            target_path.unlink(missing_ok=True)
            return Result.retry(message=str(ex))

        self.set_collection_params(comp, repo_url, package_out_path)

        if Path(f"{package_out_path}.json").is_file():
            comp.properties.remove(Property(name=BomProps.COLLECTION_ARTIFACT_FILE, value=Path(package_out_path).name))
            comp.properties.append(
                Property(name=BomProps.COLLECTION_ARTIFACT_FILE, value=str(f"{Path(package_out_path).name}.json"))
            )

        return Result.success(return_obj=comp)
