"""Models to express `Affect.versions` fields."""

from __future__ import annotations

from typing import Annotated, ClassVar

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import Field

from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap


class AffectVersion(CycloneDXBaseModel):
    """AffectVersion data model representing properties of `versions` items."""

    version: cdx.Version | None = Field(default=None)
    range: cdx.Range | None = Field(default=None)
    status: cdx.AffectedStatus | None = Field(
        default=cdx.AffectedStatus.affected,
        description="The vulnerability status for the version or range of versions.",
    )


class AffectVersionVersionRequired(AffectVersion):
    """Affect.versions item model with required `version` field."""

    version: cdx.Version

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class AffectVersionRangeRequired(AffectVersion):
    """Affect.versions item model with required `range` field."""

    range: cdx.Range

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


AffectVersions = list[AffectVersionVersionRequired | AffectVersionRangeRequired] | None


class Affect(CycloneDXBaseModel, cdx.Affect):
    """Affect data model derived from CycloneDXBaseModel with overridden `versions` field."""

    versions: Annotated[
        AffectVersions,
        Field(
            description="Zero or more individual versions or range of versions.",
            title="Versions",
        ),
    ] = None

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}
