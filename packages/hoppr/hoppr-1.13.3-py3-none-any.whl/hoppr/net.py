"""Hoppr Network utility functions."""

from __future__ import annotations

import hashlib

from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, TypeAlias

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx
import requests as requests

from pydantic import SecretStr
from requests.auth import HTTPBasicAuth

from hoppr.exceptions import HopprLoadDataError
from hoppr.models.credentials import (
    CredentialRequiredService,
    Credentials as Credentials,
)
from hoppr.utils import load_string

if TYPE_CHECKING:
    from collections.abc import Mapping
    from os import PathLike

_BLOCK_SIZE: Final[int] = 65536


HashlibAlgs: TypeAlias = Literal[
    "blake2b",
    "blake2s",
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "shake_128",
    "shake_256",
    "blake2b_256",
]
# Mapping CDX hash algorithms to those supported by builtin `hashlib` library.
HASH_ALG_MAP: Final[Mapping[cdx.HashAlg, HashlibAlgs]] = {
    cdx.HashAlg.MD5: "md5",
    cdx.HashAlg.SHA_1: "sha1",
    cdx.HashAlg.SHA_256: "sha256",
    cdx.HashAlg.SHA_384: "sha384",
    cdx.HashAlg.SHA_512: "sha512",
    cdx.HashAlg.SHA3_256: "sha3_256",
    cdx.HashAlg.SHA3_384: "sha3_384",
    cdx.HashAlg.SHA3_512: "sha3_512",
    cdx.HashAlg.BLAKE2B_256: "blake2b_256",
    cdx.HashAlg.BLAKE2B_512: "blake2b",
}


def get_file_hash(artifact: str | PathLike[str], algorithm: cdx.HashAlg | HashlibAlgs = "sha1") -> str:
    """Compute hash of downloaded component.

    Args:
        artifact: Path to downloaded file
        algorithm: Hashing algorithm to use. Defaults to SHA1.
            The only supported `cdx.HashAlg` values are those with a matching `HashlibAlgs` in `HASH_ALG_MAP`.

    Returns:
        The computed hexidecimal hash digest.

    Raises:
        ValueError: If `algorithm` is an unsupported value of `cdx.HashAlg`.
    """
    if isinstance(algorithm, cdx.HashAlg):
        try:
            algorithm = HASH_ALG_MAP[algorithm]
        except KeyError as ex:
            raise ValueError(
                f"Hash generation using the specified algorithm ({algorithm}) is not supported by Hoppr."
            ) from ex

    artifact = Path(artifact)
    hash_obj: hashlib._Hash
    match algorithm:
        case "blake2b_256":
            hash_obj = hashlib.blake2b(artifact.read_bytes(), digest_size=32)
        case _:
            hash_obj = hashlib.new(name=algorithm)

            with artifact.open(mode="rb") as hash_bytes:
                while file_bytes := hash_bytes.read(_BLOCK_SIZE):
                    hash_obj.update(file_bytes)

    return hash_obj.hexdigest().lower()


def load_url(url: str) -> dict | list | None:
    """Load config content (either json or yml) from a url into a dict."""
    creds = Credentials.find(url)

    response = None
    if creds is not None and isinstance(creds.password, SecretStr):
        authorization_headers = {
            "PRIVATE-TOKEN": creds.password.get_secret_value(),
            "Authorization": f"Bearer {creds.password.get_secret_value()}",
        }

        basic_auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())
        response = requests.get(url, auth=basic_auth, headers=authorization_headers, timeout=60)
    else:
        response = requests.get(url, timeout=60)

    response.raise_for_status()
    valid_data = True
    try:
        if isinstance(response.content, bytes):
            return load_string(response.content.decode("utf-8"))
        if isinstance(response.content, str):
            return load_string(response.content)
        valid_data = False
    except HopprLoadDataError as parse_error:
        message = f"Unable to parse result from {url}."
        if response.url != url:
            message += f" Request was redirected to {response.url}. An auth issue might have occurred."
        raise HopprLoadDataError(message) from parse_error

    if not valid_data:
        raise HopprLoadDataError("Response type is not bytes or str")

    return None  # pragma: no cover


def download_file(
    url: str,
    dest: str,
    creds: CredentialRequiredService | None = None,
    proxies: dict[str, str] | None = None,
    timeout: int | None = 60,
    cert: tuple[str, str] | None = None,
) -> requests.Response:
    """Download content from a url into a file."""
    if creds is None:
        creds = Credentials.find(url)

    basic_auth = None
    if creds is not None and isinstance(creds.password, SecretStr):
        basic_auth = HTTPBasicAuth(username=creds.username, password=creds.password.get_secret_value())

    response = requests.get(
        url=url,
        auth=basic_auth,
        allow_redirects=True,
        proxies=proxies,
        stream=True,
        verify=True,
        timeout=timeout,
        cert=cert,
    )

    if 200 <= response.status_code < 300:
        with Path(dest).open(mode="wb") as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    out_file.write(chunk)

    return response
