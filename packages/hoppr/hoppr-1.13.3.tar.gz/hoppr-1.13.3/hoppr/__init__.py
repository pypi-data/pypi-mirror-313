"""Tool for manipulating bundles for airgapped transfers."""

from __future__ import annotations

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_process, hoppr_rerunner
from hoppr.exceptions import (
    HopprCredentialsError,
    HopprError,
    HopprExperimentalWarning,
    HopprLoadDataError,
    HopprPluginError,
)
from hoppr.logger import HopprLogger
from hoppr.models import HopprContext
from hoppr.models.affect import Affect
from hoppr.models.credentials import CredentialRequiredService, Credentials
from hoppr.models.licenses import (
    License,
    LicenseChoice,
    LicenseExpression,
    LicenseExpressionItem,
    LicenseMultipleItem,
    MultipleLicenses,
    NamedLicense,
    SPDXLicense,
)
from hoppr.models.manifest import Manifest
from hoppr.models.sbom import (
    Component,
    ComponentType,
    DataOutputType,
    EventType,
    ExternalReference,
    ExternalReferenceType,
    Hash,
    IssueType,
    LearningType,
    Metadata,
    PatchType,
    Property,
    Sbom,
    SubjectMatterType,
    Tools,
    Vulnerability,
)
from hoppr.models.transfer import ComponentCoverage, Transfer
from hoppr.models.types import BomAccess, PurlType
from hoppr.result import Result

__version__ = "1.13.3"

__all__ = [  # noqa: RUF022
    "__version__",
    "BomAccess",
    "ComponentCoverage",
    "CredentialRequiredService",
    "Credentials",
    "hoppr_process",
    "hoppr_rerunner",
    "HopprContext",
    "HopprCredentialsError",
    "HopprError",
    "HopprExperimentalWarning",
    "HopprLoadDataError",
    "HopprLogger",
    "HopprPlugin",
    "HopprPluginError",
    "Manifest",
    "PurlType",
    "Result",
    "Transfer",
    # CycloneDX model classes and type aliases
    "cdx",
    "Affect",
    "Component",
    "ComponentType",
    "DataOutputType",
    "EventType",
    "ExternalReference",
    "ExternalReferenceType",
    "Hash",
    "IssueType",
    "LearningType",
    "License",
    "LicenseChoice",
    "LicenseExpression",
    "LicenseExpressionItem",
    "LicenseMultipleItem",
    "Metadata",
    "MultipleLicenses",
    "NamedLicense",
    "PatchType",
    "Property",
    "Sbom",
    "SPDXLicense",
    "SubjectMatterType",
    "Tools",
    "Vulnerability",
]
