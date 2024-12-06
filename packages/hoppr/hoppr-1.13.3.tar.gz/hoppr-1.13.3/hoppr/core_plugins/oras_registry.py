"""Supporting class for oras bundle plugin."""

from __future__ import annotations

import copy
import json
import os
import platform

from datetime import datetime
from http import cookiejar
from pathlib import Path
from typing import TYPE_CHECKING

import jsonschema
import oras.auth.utils
import oras.container
import oras.defaults
import oras.oci
import oras.provider
import oras.schemas
import oras.utils

from oras import decorator
from oras.container import Container
from oras.decorator import ensure_container
from requests import Response, Session

import hoppr

from hoppr.logger import HopprLogger

if TYPE_CHECKING:
    from oras.container import Container
    from oras.types import container_type


class Registry(oras.provider.Registry):
    """Override the default Oras Registry Class."""

    def __init__(
        self,
        hostname: str | None = None,
        insecure: bool = False,
        tls_verify: bool = True,
        auth_backend: str = "token",
        logger: HopprLogger | None = None,
    ):
        """Create an ORAS client."""
        self.hostname: str | None = hostname
        self.headers: dict = {}
        self.session: Session = Session()
        self.prefix: str = "http" if insecure else "https"
        self._tls_verify = tls_verify
        self.token: str | None = None

        self.logger = logger or HopprLogger(flush_immed=True)

        # Ignore all cookies: some registries try to set one
        # and take it as a sign they are talking to a browser,
        # trying to set further CSRF cookies (Harbor is such a case)
        self.session.cookies.set_policy(cookiejar.DefaultCookiePolicy(allowed_domains=[]))

        # Get custom backend, pass on session to share
        self.auth = oras.auth.get_auth_backend(auth_backend, self.session)

    @decorator.retry(attempts=5)
    def do_request(
        self,
        url: str,
        method: str = "GET",
        data: dict | bytes | None = None,
        headers: dict | None = None,
        json_param: dict | None = None,
        stream: bool = False,
    ) -> Response:
        """Do a request. This is a wrapper around requests to handle retry auth."""
        headers = headers or {}

        # Make the request and return to calling function, unless requires auth
        response = self.session.request(
            method,
            url,
            data=data,
            json=json_param,
            headers=headers,
            stream=stream,
            verify=self._tls_verify,
        )

        # A 401 response is a request for authentication
        if response.status_code not in [401, 404]:
            return response

        # Otherwise, authenticate the request and retry
        if self.authenticate_request(response):
            headers.update(self.headers)
            response = self.session.request(
                method,
                url,
                data=data,
                json=json_param,
                headers=headers,
                stream=stream,
            )

        return response

    def authenticate_request(self, original_response: Response) -> bool:
        """Authenticate a request with a given response."""
        auth_header_raw = original_response.headers.get("Www-Authenticate")
        if not auth_header_raw:
            self.logger.debug("Www-Authenticate not found in original response, cannot authenticate.")

            return False

        # If we have a token, set auth header (base64 encoded user/pass)
        if self.token:
            self.set_header("Authorization", f"Bearer {self.auth._basic_auth}")

            return True

        headers = copy.deepcopy(self.headers)
        auth_headers = oras.auth.utils.parse_auth_header(auth_header_raw)

        params = {}

        # Prepare request to retry
        if auth_headers.service:
            self.logger.debug(f"Service: {auth_headers.service}")
            params["service"] = auth_headers.service
            headers.update({
                "Service": auth_headers.service,
                "Accept": "application/json",
                "User-Agent": "oras-py",
            })

        # Ensure the realm starts with http
        if auth_headers.realm and not auth_headers.realm.startswith("http"):
            auth_headers.realm = f"{self.prefix}://{auth_headers.realm}"

        # If the www-authenticate included a scope, honor it!
        if auth_headers.scope:
            self.logger.debug(f"Scope: {auth_headers.scope}")
            params["scope"] = auth_headers.scope

        auth_response = self.session.get(auth_headers.realm, headers=headers, params=params)
        if auth_response.status_code != 200:
            self.logger.debug(f"Auth response was not successful: {auth_response.text}")

            return False

        # Request the token
        info = auth_response.json()
        token = info.get("token") or info.get("access_token")

        # Set the token to the original request and retry
        self.headers.update({"Authorization": f"Bearer {token}"})

        return True

    @ensure_container
    def push_container(
        self,
        container: Container,
        archives: list,
        logger: HopprLogger,
    ) -> Response:
        """Given a list of layer metadata (paths and corresponding mediaType) push."""
        # Prepare a new manifest
        manifest = oras.oci.NewManifest()
        self.session.cookies.set_policy(BlockAll())

        self.upload_blobs(container, archives, manifest, logger)

        # Prepare manifest and config (add your custom annotations here)
        manifest["annotations"] = {
            "org.opencontainers.image.created": str(datetime.now()),
            "ArtifactType": "Oras OCI Bundle",
            "Documentation": "https://oras.land/cli/",
        }
        config_file = "/tmp/oras-conf.json"
        config_blob = {
            "os": str(platform.platform()),
            "HopctlVersion": hoppr.__version__,
        }
        self.setup_default_config(config_blob, config_file)
        conf, config_file = oras.oci.ManifestConfig(
            path=config_file, media_type="application/vnd.oci.image.config.v1+json"
        )
        conf["annotations"] = config_blob

        # Config is just another layer blob!
        logger.info(f"Uploading config to {container.uri}")
        logger.info(f"Config {conf}")
        logger.flush()
        response = self.upload_blob(config_file, container, conf)
        self._check_200_response(response)
        Path(config_file).unlink(missing_ok=True)

        # Final upload of the manifest
        manifest["config"] = conf
        # Try updating the manifest
        response = self.upload_manifest(manifest=manifest, container=container)
        self._check_200_response(response=response)

        return response

    def put_upload(
        self,
        blob: str,
        container: oras.container.Container,
        layer: dict,
        refresh_headers: bool = True,
    ) -> Response:
        """Upload to a registry via put."""
        # Start an upload session
        headers = {"Content-Type": "application/octet-stream"}

        if not refresh_headers:
            headers |= self.headers

        upload_url = f"{self.prefix}://{container.upload_blob_url()}"
        request = self.do_request(upload_url, "POST", headers=headers)

        # Location should be in the header
        session_url = self._get_location(request, container)
        if not session_url:
            raise ValueError(f"Issue retrieving session url: {request.json()}")

        # PUT to upload blob url
        headers = {
            "Content-Length": str(layer["size"]),
            "Content-Type": "application/octet-stream",
        } | self.headers

        blob_url = oras.utils.append_url_params(session_url, {"digest": layer["digest"]})
        with Path(blob).open("rb") as fd:
            response = self.do_request(
                blob_url,
                method="PUT",
                data=fd.read(),
                headers=headers,
            )

        return response

    def upload_blobs(
        self,
        container: Container,
        archives: list,
        manifest: dict,
        logger: HopprLogger,
    ) -> dict:
        """Upload individual layers to OCI registry."""
        # Upload files as blobs
        for item in archives:
            blob = item.get("path")
            media_type = item.get("media_type")
            annots = item.get("annotations") or {}

            if not blob or not Path(blob).exists():
                logger.info(f"Path {blob} does not exist or is not defined.")

                continue

            # Artifact title is basename or user defined
            blob_name = item.get("title") or Path(blob).name

            # Create a new layer from the blob
            layer = oras.oci.NewLayer(blob, media_type, is_dir=False)
            logger.info(f"Preparing layer {layer}")

            # Update annotations with title we will need for extraction
            annots.update({oras.defaults.annotation_title: blob_name})
            layer["annotations"] = annots

            # update the manifest with the new layer
            manifest["layers"].append(layer)

            # Upload the blob layer
            logger.info(f"Uploading {blob} to {container.uri}")
            logger.flush()
            response = self.upload_blob(blob, container, layer)
            self._check_200_response(response)

        return manifest

    def upload_blob(
        self,
        blob: str,
        container: container_type,
        layer: dict,
        do_chunked: bool = False,
        refresh_headers: bool = True,
    ) -> Response:
        """Prepare and upload a blob."""
        # Reauthorize for each upload
        self.set_header("Authorization", self.auth.get_auth_header()["Authorization"])

        blob = os.path.abspath(blob)  # noqa: PTH100
        container = self.get_container(container)

        # Chunked for large, otherwise POST and PUT
        # This is currently disabled unless the user asks for it, as
        # it doesn't seem to work for all registries
        if not do_chunked:
            response = self.put_upload(blob, container, layer, refresh_headers=refresh_headers)
        else:
            response = self.chunked_upload(blob, container, layer)

        # If we have an empty layer digest and the registry didn't accept, just return dummy successful response
        if response.status_code not in [200, 201, 202] and layer["digest"] == oras.defaults.blank_hash:
            response = Response()
            response.status_code = 200

        return response

    def upload_manifest(self, manifest: dict, container: Container) -> Response:
        """Read a manifest file and upload it."""
        # Reauthorize manifest upload
        self.set_header("Authorization", self.auth.get_auth_header()["Authorization"])

        jsonschema.validate(manifest, schema=oras.schemas.manifest)

        headers = {
            "Content-Type": oras.defaults.default_manifest_media_type,
            "Content-Length": str(len(manifest)),
        }

        hostname, *_ = container.registry.split(":")
        put_url = f"{self.prefix}://{hostname}/v2/{container.api_prefix}/manifests/{container.tag}"

        return self.do_request(put_url, "PUT", headers=headers, json_param=manifest)

    def setup_default_config(self, config_blob: dict, config_file: str):
        """Setup default oras object config."""
        Path(config_file).write_text(json.dumps(obj=config_blob, indent=4))


class BlockAll(cookiejar.CookiePolicy):
    """Block all cookies."""

    def _block_all(self, *_, **__) -> bool:  # pragma: no cover
        return False

    netscape = True
    return_ok = set_ok = domain_return_ok = path_return_ok = _block_all
    rfc2965 = hide_cookie2 = False
