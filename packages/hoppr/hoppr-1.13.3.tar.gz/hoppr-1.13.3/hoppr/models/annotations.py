"""Models to express `Annotations.annotator` fields."""

from __future__ import annotations

from typing import Annotated, ClassVar

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import Field

from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap


class AnnotatorBase(CycloneDXBaseModel):
    """Annotations data model derived from CycloneDXBaseModel."""

    organization: Annotated[
        cdx.OrganizationalEntity | None,
        Field(
            description="The organization that created the annotation",
        ),
    ] = None
    individual: Annotated[
        cdx.OrganizationalContact | None,
        Field(
            description="The person that created the annotation",
        ),
    ] = None
    component: Annotated[
        cdx.Component | None,
        Field(
            description="The tool or component that created the annotation",
        ),
    ] = None
    service: Annotated[
        cdx.Service | None,
        Field(
            description="The service that created the annotation",
        ),
    ] = None


class AnnotatorOrganizationRequired(AnnotatorBase):
    """Annotations.annotator item model with required `organization` field."""

    organization: cdx.OrganizationalEntity

    unique_id_map: ClassVar[UniqueIDMap] = {}


class AnnotatorIndividualRequired(AnnotatorBase):
    """Annotations.annotator item model with required `individual` field."""

    individual: cdx.OrganizationalContact

    unique_id_map: ClassVar[UniqueIDMap] = {}


class AnnotatorComponentRequired(AnnotatorBase):
    """Annotations.annotator item model with required `component` field."""

    component: cdx.Component

    unique_id_map: ClassVar[UniqueIDMap] = {}


class AnnotatorServiceRequired(AnnotatorBase):
    """Annotations.annotator item model with required `service` field."""

    service: cdx.Service

    unique_id_map: ClassVar[UniqueIDMap] = {}


Annotator = Annotated[
    AnnotatorOrganizationRequired
    | AnnotatorIndividualRequired
    | AnnotatorComponentRequired
    | AnnotatorServiceRequired,
    Field(
        description="The organization, person, component, or service which "
        "created the textual content of the annotation.",
        title="Annotator",
    ),
]  # fmt: skip


class Annotations(CycloneDXBaseModel, cdx.Annotations):
    """Annotations data model derived from CycloneDXBaseModel."""

    def __hash__(self) -> int:
        return hash(self.bom_ref)

    annotator: Annotator

    unique_id_map: ClassVar[UniqueIDMap] = {}
