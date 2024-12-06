"""Hoppr exceptions and warnings."""

from __future__ import annotations


class HopprError(RuntimeError):
    """Base exception raised within the hoppr app."""


class HopprPluginError(HopprError):
    """Exception raised for errors working with plug-ins."""


class HopprPluginRetriableError(HopprPluginError):
    """Exception raised when a plugin fails to perform an action that can be retried."""


class HopprLoadDataError(HopprError):
    """Exception raised for errors loading json/yml data."""


class HopprCredentialsError(HopprError):
    """Exception raised for errors loading credential data."""


class HopprPrivateKeyError(HopprError):
    """Exception raised for unsupported private key usage."""


class HopprValidationError(ValueError):  # pragma: no cover
    """Exception raised for failures during SBOM validation."""

    def __init__(self, *args: object, check_name: str) -> None:
        super().__init__(*args)
        self.check_name = check_name

    def __str__(self) -> str:
        return "".join(str(arg) for arg in self.args)


class HopprExperimentalWarning(UserWarning):
    """Warning raised when experimental features are accessed."""
