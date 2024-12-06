"""CycloneDX data models."""

from __future__ import annotations

import uuid

from collections.abc import Callable, MutableMapping
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Literal, TypeAlias

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import Extra, Field, root_validator, validator
from rapidfuzz import fuzz
from requests import HTTPError

import hoppr.net
import hoppr.utils

from hoppr.exceptions import HopprLoadDataError
from hoppr.models.affect import Affect
from hoppr.models.annotations import Annotations
from hoppr.models.base import CycloneDXBaseModel, UniqueIDMap
from hoppr.models.licenses import LicenseChoice, LicenseExpressionItem, LicenseMultipleItem, NamedLicense
from hoppr.models.types import LocalFile, OciFile, UrlFile

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from packageurl import PackageURL


DictStrAny: TypeAlias = dict[str, Any]
UpdateRefsCallback: TypeAlias = Callable[[str], None]

# Type aliases for CycloneDX enums
ComponentType: TypeAlias = cdx.Type
PatchType: TypeAlias = cdx.Type1
IssueType: TypeAlias = cdx.Type2
ExternalReferenceType: TypeAlias = cdx.Type3
LearningType: TypeAlias = cdx.Type4
SubjectMatterType: TypeAlias = cdx.Type5
EventType: TypeAlias = cdx.Type6
DataOutputType: TypeAlias = cdx.Type7
__all__ = [
    "Component",
    "ComponentType",
    "DataOutputType",
    "EventType",
    "ExternalReference",
    "ExternalReferenceType",
    "Hash",
    "IssueType",
    "LearningType",
    "Metadata",
    "PatchType",
    "Property",
    "Sbom",
    "SubjectMatterType",
    "Tools",
]

SbomRef = Annotated[LocalFile | OciFile | UrlFile, Field(description="Reference to a local or remote SBOM file")]

FUZZY_MATCH_THRESHOLD = 85


def _extract_components(components: list[Component]) -> list[Component]:
    """Explicitly set scope of flattened components to `exclude`."""
    for component in components:
        component.scope = cdx.Scope.EXCLUDED

    return hoppr.utils.dedup_list(components)


def _extract_sbom_components(external_refs: list[ExternalReference]) -> list[Component]:
    """Extracts `external_refs` of type "bom" and returns the set of their components."""
    components: list[Component] = []

    for ref in _get_bom_refs(external_refs):
        sbom = Sbom.load(_resolve_sbom_source(ref.dict()["url"]))
        sbom.components = _extract_components(sbom.components)
        components.extend(sbom.components)
        external_refs.remove(ref)

    return components


def _flatten_component(component: Component) -> list[Component]:
    """Helper function to flatten a component's subcomponents into a set."""
    flattened = []

    for subcomponent in component.components or []:
        # Ensure validator is run to set `bom_ref`
        subcomponent = Component(**subcomponent.dict())
        subcomponent.scope = cdx.Scope.EXCLUDED

        # Flatten nested components into top level components list
        flattened.append(subcomponent)

    component.components.clear()
    return flattened


def _get_bom_refs(external_refs: list[ExternalReference]) -> Iterator[ExternalReference]:
    """Get `externalReferences` of type "bom"."""
    yield from (ref.copy(deep=True) for ref in (external_refs or []) if ref.type == "bom")


def _make_validator(function: Callable, field_name: str, pre: bool = False) -> classmethod[Any, Any, Any]:
    """Wrap a callable with the pydantic validator wrapper."""
    return validator(field_name, allow_reuse=True, always=True, pre=pre)(function)


def _resolve_sbom_source(source: str) -> str | Path | DictStrAny:
    """Resolves an SBOM source as a file path, URL or `dict`."""
    return Path(source.removeprefix("file://")).resolve() if source.startswith("file://") else source


def _set_component_bom_ref(values: DictStrAny) -> DictStrAny:
    """Set `bom-ref` identifier for a component if not set."""
    component = Component.parse_obj(values)

    if not any([component.purl, component.bom_ref, all([component.name, component.version])]):
        raise ValueError(
            "Either 'bom-ref' or 'purl' must be defined, or 'name' and 'version' must be defined on a component"
        )

    if component.purl:
        # Decode any unicode escape sequences, e.g. "\u0026" -> "&"
        component.purl = component.purl.encode("utf-8").decode("utf-8")

        # If component has no `version` set, try to parse version from `purl` field
        purl_version = hoppr.utils.get_package_url(component.purl).version
        component.version = component.version or purl_version

    bom_ref = str(
        component.bom_ref or component.purl or f"{'@'.join(filter(None, [component.name, component.version]))}"
    )

    component.bom_ref = bom_ref.encode("utf-8").decode("utf-8")

    return component.dict(exclude_none=True, exclude_unset=True)


def _validate_components_pre(cls: CycloneDXBaseModel, values: list[DictStrAny]) -> list[DictStrAny]:
    """Validator to set `bom-ref` identifier for each component if not set.

    This validation is only performed on the `components` field for the `Sbom` and `Component` models.
    """
    validated: list[DictStrAny] = [_set_component_bom_ref(component_dict) for component_dict in values]

    return validated


def _validate_components(cls: CycloneDXBaseModel, components: list[Component]) -> list[Component]:
    """Validator to optionally flatten `components` list."""
    if not cls.flatten:
        return components

    flattened = list(components)

    for component in components:
        flattened.extend(_flatten_component(component))

    return hoppr.utils.dedup_list(flattened)


def _validate_external_refs(
    cls: CycloneDXBaseModel, external_refs: list[ExternalReference], values: DictStrAny
) -> list[ExternalReference]:
    """Validator to optionally resolve `externalReferences`."""
    external_refs = [ExternalReference.create(ref) for ref in external_refs or []]

    if cls.deep_merge:
        external_ref_components = _extract_sbom_components(external_refs)
        values["components"] = hoppr.utils.dedup_list([*values.get("components", []), *external_ref_components])

    return external_refs


def _validate_licenses(cls: CycloneDXBaseModel, licenses: LicenseChoice) -> list[LicenseMultipleItem]:
    """Validator to resolve expression field."""
    license_list: list[LicenseMultipleItem] = [
        LicenseMultipleItem(license=NamedLicense(bom_ref=license_.bom_ref, name=license_.expression))
        if isinstance(license_, LicenseExpressionItem)
        else license_
        for license_ in licenses or []
    ]

    return hoppr.utils.dedup_list(license_list)


class ExternalReference(CycloneDXBaseModel, cdx.ExternalReference, extra=Extra.allow):
    """ExternalReference data model derived from CycloneDXBaseModel."""

    type: ExternalReferenceType

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Hash(CycloneDXBaseModel, cdx.Hash, extra=Extra.allow):
    """Hash data model derived from CycloneDXBaseModel."""

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Property(CycloneDXBaseModel, cdx.Property, extra=Extra.allow):
    """Property data model derived from CycloneDXBaseModel."""

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Component(CycloneDXBaseModel, cdx.Component, extra=Extra.allow):
    """Component data model derived from CycloneDXBaseModel."""

    type: ComponentType
    bom_ref: Annotated[str, Field(alias="bom-ref")] = None  # type: ignore[assignment]
    components: list[Component] = []  # type: ignore[assignment]
    externalReferences: list[ExternalReference] = []  # type: ignore[assignment]
    hashes: list[Hash] = []  # type: ignore[assignment]
    licenses: LicenseChoice = []
    properties: list[Property] = []  # type: ignore[assignment]

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}

    validate_components_pre: classmethod = _make_validator(_validate_components_pre, "components", pre=True)
    validate_components: classmethod = _make_validator(_validate_components, "components")
    validate_external_refs: classmethod = _make_validator(_validate_external_refs, "externalReferences")

    reference_updater_map: ClassVar[MutableMapping[Component, UpdateRefsCallback]] = {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Component):
            return False

        # Remove `purl` and `bom_ref` from field comparisons. Field checks are only
        # performed if these fields have already been checked and found to be not equal
        field_names = (self.__fields_set__ | other.__fields_set__).difference({"bom_ref", "purl"})

        return (
            self._purl_check(other)
            or self._bom_ref_check(other)
            or all(getattr(self, name, None) == getattr(other, name, None) for name in field_names)
        )

    def _bom_ref_check(self, other: Component) -> bool:
        if not (self.bom_ref and other.bom_ref):
            return False

        return self.bom_ref == other.bom_ref and self._hash_match(other.hashes)

    def _hash_match(self, other_hashes: list[Hash]) -> bool:
        """Compare this component's hashes against a specified list of hashes.

        Args:
            other_hashes: Hash list to compare against this component's hashes.

        Returns:
            `True` if the content of each component hash matches the content of each hash in
            `other_hashes` with a matching algorithm; otherwise, `False`.
        """
        content_match = True

        # Compare hashes from both components that have matching algorithm
        hash_alg_matches = (
            (self_hash, other_hash)
            for self_hash in self.hashes
            for other_hash in other_hashes
            if self_hash.alg == other_hash.alg
        )

        for self_hash, other_hash in hash_alg_matches:
            content_match = content_match and self_hash.content == other_hash.content

        return content_match

    def _purl_check(self, other: Component) -> bool:
        if not (self.purl and other.purl):
            return False

        self_purl = hoppr.utils.get_package_url(self.purl)
        other_purl = hoppr.utils.get_package_url(other.purl)

        qual_keys = hoppr.utils.dedup_list(self_purl.qualifiers | other_purl.qualifiers)

        return all([
            self_purl.name == other_purl.name,
            self_purl.type == other_purl.type,
            self_purl.namespace == other_purl.namespace,
            str(self_purl.version).removeprefix("v") == str(other_purl.version).removeprefix("v"),
            self_purl.subpath == other_purl.subpath,
            *[self._qualifier_match(key, self_purl, other_purl) for key in qual_keys],
        ]) and self._hash_match(other.hashes)

    def _qualifier_match(self, key: str, self_purl: PackageURL, other_purl: PackageURL) -> bool:
        # Compare only if both purls have a value for specified qualifier
        if key not in (self_qual := self_purl.qualifiers) or key not in (other_qual := other_purl.qualifiers):
            return True

        return fuzz.ratio(self_qual.get(key, ""), other_qual.get(key, "")) > FUZZY_MATCH_THRESHOLD

    def contains_hashes(self, other_hashes: list[Hash]) -> bool:
        """Verify that the provided hashes are in this component's hashes.

        Args:
            other_hashes: Hash list used to validate this component's hashes.

        Returns:
            `True` if the provided hashes match all component hashes; otherwise, `False`.
        """
        return all(other_hash in self.hashes for other_hash in other_hashes)

    def update_hashes(self, hashes: Iterable[Hash]):
        """Updates the hashes for the component.

        Hashes using an algorithm matching an existing hash in this component will be compared against the current hash
        for that algorithm. If they don't match, a `ValueError` will be raised.

        Args:
            hashes: Hashes for updating the component hashes.

        Raises:
            ValueError: If the provided hashes have an existing algorithm that doesn't match the corresponding hash in
            the component.
        """
        current_hash_algs = [hash_.alg for hash_ in self.hashes]
        for hash_ in hashes:
            if hash_.alg not in current_hash_algs:
                self.hashes.append(hash_)
            elif hash_ not in self.hashes:
                raise ValueError("Mismatched hash for existing algorithm.")

    def merge(self, other: CycloneDXBaseModel) -> None:
        """Merge Component instance into self.

        Args:
            other: Component object to merge
        """
        if not isinstance(other, Component):
            return

        if other.bom_ref and self.bom_ref != other.bom_ref and other in self.reference_updater_map:
            self.reference_updater_map[other](self.bom_ref)

        super().merge(other)


Component.update_forward_refs()


class Tools(CycloneDXBaseModel, cdx.ToolModel, extra=Extra.allow):
    """Tools data model derived from CycloneDXBaseModel."""

    components: list[Component] = Field(default=[])  # type: ignore[assignment]

    @classmethod
    def _convert_tool_to_component(cls, tool: cdx.Tool) -> Component:
        return Component(
            type=ComponentType.APPLICATION,
            name=str(tool.name),
            version=tool.version,
            hashes=[Hash.create(hash) for hash in tool.hashes or []],
            externalReferences=[ExternalReference.create(ref) for ref in tool.externalReferences or []],
            scope=cdx.Scope.EXCLUDED,
        )

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def validate_tools(cls, values: list[DictStrAny] | DictStrAny) -> DictStrAny:
        """Validator to convert deprecated list of `Tool` objects to a `Tools` object."""
        if isinstance(values, list):
            tool_model = cdx.ToolModel()
            tool_model.components = []

            tools = [cdx.Tool.parse_obj(tool) for tool in values]
            tool_model.components.extend(cls._convert_tool_to_component(tool) for tool in tools)

            values = tool_model.dict(exclude_none=True, exclude_unset=True)

        return values

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Metadata(CycloneDXBaseModel, cdx.Metadata, extra=Extra.allow):
    """Metadata data model derived from CycloneDXBaseModel."""

    tools: Tools | None = None
    licenses: LicenseChoice = None

    validate_licenses: classmethod = _make_validator(_validate_licenses, "licenses")

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def validate_metadata(cls, values: DictStrAny | None) -> DictStrAny:
        """Validator to populate and normalize `metadata` field."""
        values = values or {}

        if isinstance(tool_list := values.get("tools"), list):
            values["tools"] = Tools.validate_tools(tool_list)

        metadata = cdx.Metadata.parse_obj(values)
        metadata.timestamp = datetime.now(timezone.utc)
        metadata.tools = Tools.parse_obj(values.get("tools") or {})

        # Generate `metadata` field containing Hoppr tool component
        metadata.tools.components = hoppr.utils.dedup_list([
            Component(
                type=cdx.Type("application"),
                name="hoppr",
                version=hoppr.__version__,
                bom_ref=f"pkg:pypi/hoppr@{hoppr.__version__}",
                purl=f"pkg:pypi/hoppr@{hoppr.__version__}",
                scope=cdx.Scope.EXCLUDED,
            ),
            *metadata.tools.components,
        ])

        values = metadata.dict(exclude_none=True, exclude_unset=True)
        return values

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Vulnerability(CycloneDXBaseModel, cdx.Vulnerability, extra=Extra.allow):
    """Vulnerability data model derived from CycloneDXBaseModel."""

    tools: Tools | None = None  # type: ignore[assignment]
    affects: Annotated[
        list[Affect],
        Field(description="The components or services that are affected by the vulnerability.", title="Affects"),
    ] = []  # type: ignore[assignment]

    # Attributes not included in schema
    unique_id_map: ClassVar[UniqueIDMap] = {}


class Sbom(CycloneDXBaseModel, cdx.CyclonedxSoftwareBillOfMaterialsStandard, extra=Extra.allow):
    """Sbom data model derived from CycloneDXBaseModel."""

    specVersion: str = "1.5"
    version: int = 1
    metadata: Metadata | None = None
    components: list[Component] = []  # type: ignore[assignment]
    externalReferences: list[ExternalReference] = []  # type: ignore[assignment]
    vulnerabilities: list[Vulnerability] = []  # type: ignore[assignment]
    annotations: list[Annotations] = []  # type: ignore[assignment]

    # Attributes not included in schema
    loaded_sboms: ClassVar[MutableMapping[SbomRef, "Sbom"]] = {}
    unique_id_map: ClassVar[UniqueIDMap] = {}

    validate_components_pre: classmethod = _make_validator(_validate_components_pre, "components", pre=True)
    validate_components: classmethod = _make_validator(_validate_components, "components")
    validate_external_refs: classmethod = _make_validator(_validate_external_refs, "externalReferences")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sbom):
            return False

        return True if self.serialNumber == other.serialNumber else super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.serialNumber)

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def validate_sbom(cls, values: DictStrAny) -> DictStrAny:
        """Validator to standardize fields."""
        values["$schema"] = "http://cyclonedx.org/schema/bom-1.5.schema.json"
        values["specVersion"] = "1.5"
        values["serialNumber"] = values.get("serialNumber", None) or uuid.uuid4().urn

        return values

    @classmethod
    def find_ref(cls, ref_type: Literal["local", "oci", "url"], location: str | Path) -> Sbom | None:
        """Look up SBOM object by reference.

        Args:
            ref_type (Literal["local", "oci", "url"]): Type of SBOM reference
            location (str | Path): Location of SBOM reference

        Returns:
            Sbom | None: SBOM object if found, otherwise None
        """
        match ref_type:
            case "local":
                return cls.loaded_sboms.get(LocalFile(local=Path(location)), None)
            case "oci":
                return cls.loaded_sboms.get(OciFile(oci=str(location)), None)
            case "url":
                return cls.loaded_sboms.get(UrlFile(url=str(location)), None)
            case _:
                return None

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Sbom:
        """Load SBOM from local file, URL, or dict."""
        match source:
            case dict():
                sbom = cls(**source)
            case Path():
                # Convert source to relative path if in current working directory subpath
                source = source.resolve()
                source = source.relative_to(Path.cwd()) if source.is_relative_to(Path.cwd()) else source

                sbom = cls.parse_file(source)
                cls.loaded_sboms[LocalFile(local=source)] = sbom
            case str():
                try:
                    sbom_dict = hoppr.net.load_url(source)
                    if not isinstance(sbom_dict, dict):
                        raise TypeError("URL SBOM was not loaded as dictionary")

                    sbom = cls.parse_obj(sbom_dict)
                    url_ref = UrlFile(url=source)
                    cls.loaded_sboms[url_ref] = sbom
                except (HopprLoadDataError, HTTPError) as ex:
                    raise HopprLoadDataError from ex

        return sbom

    @staticmethod
    def _append_dependency_update_functions(
        update_functions: list[UpdateRefsCallback], dependency: cdx.Dependency, bom_ref: str
    ):
        if dependency.ref == bom_ref:

            def update_dependency_ref(new_ref: str):
                dependency.ref = new_ref

            update_functions.append(update_dependency_ref)

        bom_ref_link = cdx.RefLinkType(bom_ref)
        subdependencies: list[cdx.RefLinkType] = dependency.dependsOn or []
        if bom_ref_link in subdependencies:

            def update_subdependency(new_ref: str):
                subdependencies.remove(bom_ref_link)
                subdependencies.append(cdx.RefLinkType(new_ref))

            update_functions.append(update_subdependency)

    @staticmethod
    def _append_vulnerability_update_function(
        update_functions: list[UpdateRefsCallback], vulnerability: Vulnerability, bom_ref: str
    ):
        def update_affected_ref(new_ref: str, affected: Affect):
            affected.ref = new_ref

        for affected in filter(lambda af: af.ref == bom_ref, vulnerability.affects):
            update_functions.append(partial(update_affected_ref, affected=affected))

    def _get_update_refs_callback(self, bom_ref: str) -> UpdateRefsCallback:
        update_functions: list[UpdateRefsCallback] = []

        def update_refs(new_ref: str):
            for update in update_functions:
                update(new_ref)

        for dependency in self.dependencies or []:
            self._append_dependency_update_functions(update_functions, dependency, bom_ref)

        for vulnerability in self.vulnerabilities:
            self._append_vulnerability_update_function(update_functions, vulnerability, bom_ref)

        return update_refs

    def _set_component_bom_ref_update_callbacks(self):
        for component in self.components:
            Component.reference_updater_map[component] = self._get_update_refs_callback(component.bom_ref)

    def merge(self, other: CycloneDXBaseModel) -> None:
        """Merge Sbom instance into self.

        Args:
            other: Sbom object to merge
        """
        if type(other) is Sbom:
            other._set_component_bom_ref_update_callbacks()

        super().merge(other)
