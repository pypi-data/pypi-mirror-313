"""Hoppr signer class."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa

from hoppr.exceptions import HopprPrivateKeyError

if TYPE_CHECKING:
    import abc

    from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
    from cryptography.hazmat.primitives.serialization.ssh import SSHPrivateKeyTypes


class HopprSigner:
    """Class for managing hoppr digital signatures.

    The intent is to generate digitally signed sboms and bundles
    """

    SUPPORTED_PRIVATE_KEY_TYPES: ClassVar[list[abc.ABCMeta]] = [
        ed25519.Ed25519PrivateKey,
        rsa.RSAPrivateKey,
        ec.EllipticCurvePrivateKey,
    ]

    private_key: SSHPrivateKeyTypes | PrivateKeyTypes | None

    def __init__(
        self,
        sign: bool,
        functionary_key_path: Path | None = None,
        functionary_key_password: str | None = None,
    ) -> None:
        self.sign = sign

        if self.sign and functionary_key_path:
            password_bytes = functionary_key_password.encode(encoding="utf-8") if functionary_key_password else None

            key_text = functionary_key_path.read_text()
            if "BEGIN OPENSSH PRIVATE KEY" in key_text:
                self.private_key = serialization.load_ssh_private_key(
                    key_text.encode(),
                    password=password_bytes,
                    backend=default_backend(),
                )
            else:
                self.private_key = serialization.load_pem_private_key(
                    key_text.encode(),
                    password=password_bytes,
                    backend=default_backend(),
                )

            if not isinstance(self.private_key, tuple(self.SUPPORTED_PRIVATE_KEY_TYPES)):
                raise HopprPrivateKeyError(
                    "Unsupported Private Key type for signing, supported types are rsa, ed25519, ecdsa."
                )

    def sign_blobs(self, blob_files: list[Path]):
        """Wrapper method used for handling multiple blobs that leverages sign_blob."""
        if self.sign:
            for blob_file in blob_files:
                self.sign_blob(blob_file)

    def sign_blob(self, blob_file: Path):
        """Signer method used by hoppr processing."""
        if self.sign:
            # Load the contents of the file to be signed.
            payload = blob_file.read_bytes()

            signature = None

            match self.private_key:
                case rsa.RSAPrivateKey():
                    signature = self.private_key.sign(
                        payload,
                        padding.PKCS1v15(),
                        hashes.SHA256(),
                    )
                case ed25519.Ed25519PrivateKey():
                    signature = self.private_key.sign(payload)
                case ec.EllipticCurvePrivateKey():
                    signature = self.private_key.sign(payload, ec.ECDSA(hashes.SHA256()))

            if signature:
                signature_file = Path(f"{blob_file!s}.sig")
                signature_file.write_bytes(signature)
