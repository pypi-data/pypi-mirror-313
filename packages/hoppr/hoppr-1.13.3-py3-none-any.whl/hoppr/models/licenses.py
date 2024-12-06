"""Models to express `licenses` fields."""

from __future__ import annotations

from typing import Annotated, ClassVar, TypeAlias

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from hoppr_cyclonedx_models import spdx
from pydantic import Extra, Field

from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap


class LicensingOrganizationRequired(CycloneDXBaseModel):
    """Licensing data model derived from CycloneDXBaseModel with required `organization` field."""

    organization: cdx.OrganizationalEntity


class LicensingIndividualRequired(CycloneDXBaseModel):
    """Licensing data model derived from CycloneDXBaseModel with required `organization` field."""

    individual: cdx.OrganizationalContact


OrganizationOrIndividualData: TypeAlias = LicensingOrganizationRequired | LicensingIndividualRequired | None


class Licensing(CycloneDXBaseModel, cdx.Licensing, extra=Extra.allow):
    """Licensing data model derived from CycloneDXBaseModel."""

    licensor: Annotated[
        OrganizationOrIndividualData,
        Field(
            description="The individual or organization that grants a license to another individual or organization",
            title="Licensor",
        ),
    ] = None

    licensee: Annotated[
        OrganizationOrIndividualData,
        Field(description="The individual or organization for which a license was granted to", title="Licensee"),
    ] = None

    purchaser: Annotated[
        OrganizationOrIndividualData,
        Field(description="The individual or organization that purchased the license", title="Purchaser"),
    ] = None

    unique_id_map: ClassVar[UniqueIDMap] = {}


class License(CycloneDXBaseModel, cdx.License):
    """License data model derived from CycloneDXBaseModel."""

    licensing: Annotated[
        Licensing | None,
        Field(
            description=(
                "Licensing details describing the licensor/licensee, license type, "
                "renewal and expiration dates, and other important metadata"
            ),
            title="Licensing information",
        ),
    ] = None

    def __hash__(self) -> int:  # pragma: no cover
        return hash(self.bom_ref or self.id or self.name or repr(self))

    unique_id_map: ClassVar[UniqueIDMap] = {}


class SPDXLicense(License):
    """License data model derived from CycloneDXBaseModel with required `id` field."""

    # Override to make `id` field required by removing default value
    id: Annotated[
        spdx.LicenseID,
        Field(
            description="A valid SPDX license ID",
            examples=["Apache-2.0"],
            title="License ID (SPDX)",
        ),
    ]

    def __hash__(self) -> int:  # pragma: no cover
        return hash(self.id)

    unique_id_map: ClassVar[UniqueIDMap] = {}


class NamedLicense(License):
    """License data model derived from CycloneDXBaseModel with required `name` field."""

    # Override to make `name` field required by removing default value
    name: Annotated[
        str,
        Field(
            description="If SPDX does not define the license used, this field may be used to provide the license name",
            examples=["Acme Software License"],
            title="License Name",
        ),
    ]

    def __hash__(self) -> int:  # pragma: no cover
        return hash(self.name)

    unique_id_map: ClassVar[UniqueIDMap] = {}


class LicenseMultipleItem(CycloneDXBaseModel):
    """Multiple named or SPDX licenses data model."""

    license: SPDXLicense | NamedLicense

    def __hash__(self) -> int:
        return hash(self.license)

    unique_id_map: ClassVar[UniqueIDMap] = {}


MultipleLicenses: TypeAlias = Annotated[
    list[LicenseMultipleItem],
    Field(
        description="A list of SPDX licenses and/or named licenses.",
        title="Multiple licenses",
    ),
]


class LicenseExpressionItem(CycloneDXBaseModel):
    """SPDX license expression data model."""

    expression: Annotated[
        str,
        Field(
            title="SPDX License Expression",
            examples=["Apache-2.0 AND (MIT OR GPL-2.0-only)", "GPL-3.0-only WITH Classpath-exception-2.0"],
        ),
    ]
    bom_ref: Annotated[
        str | None,
        Field(
            title="BOM Reference",
            description=(
                "An optional identifier which can be used to reference the license elsewhere in the BOM. "
                "Every bom-ref MUST be unique within the BOM."
            ),
            alias="bom-ref",
            min_length=1,
        ),
    ] = None

    unique_id_map: ClassVar[UniqueIDMap] = {}


LicenseExpression: TypeAlias = Annotated[
    list[LicenseExpressionItem],
    Field(
        title="SPDX License Expression",
        description="A tuple of exactly one SPDX License Expression.",
        min_items=1,
        max_items=1,
    ),
]


LicenseChoice: TypeAlias = Annotated[
    MultipleLicenses | LicenseExpression | None,
    Field(
        description="EITHER (list of SPDX licenses and/or named licenses) OR (tuple of one SPDX License Expression)",
        title="License Choice",
    ),
]
