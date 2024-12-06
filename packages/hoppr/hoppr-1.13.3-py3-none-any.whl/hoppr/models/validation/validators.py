"""Models to perform SBOM validation checks."""

from __future__ import annotations

import json
import logging
import os
import re

from datetime import date, timedelta
from typing import TYPE_CHECKING, Any, TypeAlias

import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx
import jmespath

from pydantic import ValidationError, root_validator, validator

from hoppr.exceptions import HopprValidationError
from hoppr.models.licenses import LicenseExpressionItem, LicenseMultipleItem
from hoppr.models.validation.base import BaseValidator
from hoppr.models.validation.checks import ValidateConfig
from hoppr.models.validation.code_climate import Issue, IssueList, IssueSeverity
from hoppr.models.validation.exclude import JMESPathOptions
from hoppr.models.validation.json_mapper import JSONLocationMapper

if TYPE_CHECKING:
    from pathlib import Path

    from pydantic.fields import ModelField

    DictStrAny: TypeAlias = dict[str, Any]

_CONFIG: ValidateConfig


def _field_validator(*field_names: str, check_name: str) -> classmethod[Any, Any, Any]:
    """Wrap a callable with the pydantic `validator` or `root_validator` decorator."""

    def _validator(obj: object | None, field: ModelField, values: DictStrAny) -> object:
        # Remove current field from `field_names`
        fields = list(field_names)
        fields.remove(field.name)

        # The `values` variable is a dictionary of all fields previously validated by pydantic.
        # This check will be `False` if this is the last unvalidated field in `field_names`.
        if any(name not in values for name in fields):
            return obj

        # Current field plus previously validated fields
        field_values = [obj, *[values.get(name) for name in fields]]

        if not any(field_values):
            missing_fields = ", ".join(f"'{name}'" for name in field_names)
            msg = f"Missing field{'s: one of' if len(field_names) > 1 else ':'} {missing_fields}"

            BaseValidator.notify(msg=msg, log_level=_get_log_level(check_name), indent_level=2)

            raise HopprValidationError(msg, check_name=check_name)

        return obj

    # Assign validator method a unique name
    _validator.__name__ = f"_validate_{'_'.join(field_names)}"

    return validator(*field_names, allow_reuse=True, always=True, pre=True)(_validator)


def _get_check_config(check_name: str) -> str:
    match check_name:
        case _ if matched := re.match(pattern=r"components\.licenses\.(.*)", string=check_name):
            check_config = _CONFIG.component_checks.licenses.dict(by_alias=True)[matched[1]]

        case _ if matched := re.match(pattern=r"components\.(.*)", string=check_name):
            check_config = _CONFIG.component_checks.dict(by_alias=True)[matched[1]]

        case _ if matched := re.match(pattern=r"metadata\.licenses\.(.*)", string=check_name):
            check_config = _CONFIG.metadata_checks.licenses.dict(by_alias=True)[matched[1]]

        case _ if matched := re.match(pattern=r"metadata\.(.*)", string=check_name):
            check_config = _CONFIG.metadata_checks.dict(by_alias=True)[matched[1]]

        case _ if matched := re.match(pattern=r"sbom\.(.*)", string=check_name):
            check_config = _CONFIG.sbom_checks.dict(by_alias=True)[matched[1]]

        case _:
            check_config = "ignore"

    return check_config


def _get_file_issue_list(exc: ValidationError, sbom_file: Path) -> IssueList:
    issue_list = IssueList()
    location_mapper = _get_location_map(sbom_file)

    for error in exc.errors():
        ctx = error.get("ctx", {})
        check_name = ctx.get("check_name", "")

        # Prepend `components` or `metadata` to the check name to
        # identify which type of license check it pertains to
        if check_name.startswith("licenses."):
            loc_idx = error["loc"].index("licenses")
            loc = tuple(reversed(error["loc"][:loc_idx]))
            prefix = next((name for name in loc if name in {"components", "metadata"}), None)
            check_name = f"{f'{prefix}.' if prefix else ''}{check_name}"

        if not (locations := location_mapper.find(_get_file_location_from_error(error["loc"], sbom_file))):
            continue

        location, *_ = locations

        if (severity := _get_severity(check_name)) == IssueSeverity.INFO:
            continue

        issue_list.append(
            Issue(
                check_name=check_name,
                description=error.get("msg", ""),
                location=location,
                severity=severity,
            )
        )

    return issue_list


def _get_file_location_from_error(error_loc: tuple[int | str, ...], sbom_file: Path) -> DictStrAny:
    """Get the location of the failing object in the specified SBOM file.

    For example:
        error_loc = ("components", 2, "licenses", 1, "__root__")

        corresponds to

        file_loc["components"][2]["licenses"][1]

    Args:
        error_loc: A pydantic ErrorDict["loc"] describing the JSON path to the failing object.
        sbom_file: Path to SBOM file with a validation issue.

    Returns:
        Dict representing the the object in which a validation issue was found.
    """
    file_loc = json.loads(sbom_file.read_bytes().decode(encoding="utf-8"))

    for sub_loc in error_loc:
        match sub_loc:
            case str():
                file_loc = file_loc.get(sub_loc, file_loc)

                if isinstance(file_loc, str):
                    return {sub_loc: file_loc}

            case int():
                file_loc = file_loc[sub_loc]

    return file_loc


def _get_location_map(sbom_file: Path) -> JSONLocationMapper:
    location_mapper = JSONLocationMapper.load_file(sbom_file)
    data = json.loads(sbom_file.read_bytes().decode(encoding="utf-8"))
    searches = _CONFIG.exclude.dict(by_alias=True, exclude_none=True, exclude_unset=True) if _CONFIG.exclude else {}

    # Remove excluded objects from location map
    for exclude_type, search_list in searches.items():
        search = "||".join(expr.removeprefix("jmespath:") for expr in search_list)
        search = f"{exclude_type}[*]|{search.replace(']||[?', '||')}"

        for result in jmespath.search(
            expression=search.removeprefix("jmespath:"),
            data=data,
            options=JMESPathOptions(),
        ) or []:  # fmt: skip
            del location_mapper[json.dumps(result, ensure_ascii=False)]

    return location_mapper


def _get_log_level(check_name: str) -> int:
    log_mapping = {
        "ignore": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
    }

    return log_mapping.get(_get_check_config(check_name), logging.INFO)


def _get_severity(check_name: str) -> IssueSeverity:
    severity_mapping = {
        "ignore": IssueSeverity.INFO,
        "warn": IssueSeverity.MINOR,
        "error": IssueSeverity.MAJOR,
    }

    return severity_mapping.get(_get_check_config(check_name), IssueSeverity.INFO)


class LicenseValidator(BaseValidator):
    """Model to perform validation checks on licenses."""

    __root__: LicenseMultipleItem | LicenseExpressionItem

    @root_validator
    @classmethod
    def _validate_license_expiration(cls, values: DictStrAny) -> DictStrAny:
        license_ = values["__root__"]

        expiration_days = float(os.getenv("HOPPR_EXPIRATION_DAYS", "30"))

        if (
            isinstance(license_, LicenseMultipleItem)
            and license_.license.licensing
            and license_.license.licensing.expiration
            and license_.license.licensing.expiration.date() < date.today() + timedelta(days=expiration_days)
        ):
            raise HopprValidationError(
                f"License expired or expiring within {int(expiration_days)} days",
                check_name="licenses.expiration",
            )

        return values

    @root_validator
    @classmethod
    def _validate_last_renewal(cls, values: DictStrAny) -> DictStrAny:
        license_ = values["__root__"]

        if (
            isinstance(license_, LicenseMultipleItem)
            and license_.license.licensing
            and license_.license.licensing.lastRenewal
        ):
            return values

        raise HopprValidationError("Missing or invalid lastRenewal", check_name="licenses.last-renewal")

    @root_validator
    @classmethod
    def _validate_license_types(cls, values: DictStrAny) -> DictStrAny:
        license_ = values["__root__"]

        if (
            isinstance(license_, LicenseMultipleItem)
            and license_.license.licensing
            and license_.license.licensing.licenseTypes
        ):
            return values

        raise HopprValidationError("Missing or invalid licenseTypes", check_name="licenses.license-types")

    @root_validator
    @classmethod
    def _validate_purchase_order(cls, values: DictStrAny) -> DictStrAny:
        license_ = values["__root__"]

        if (
            isinstance(license_, LicenseMultipleItem)
            and license_.license.licensing
            and license_.license.licensing.purchaseOrder
        ):
            return values

        raise HopprValidationError("Missing or invalid purchaseOrder", check_name="licenses.purchase-order")

    @root_validator
    @classmethod
    def _validate_license_name_or_id(cls, values: DictStrAny) -> DictStrAny:
        license_ = values["__root__"]

        if isinstance(license_, LicenseMultipleItem) and (license_.license.name or license_.license.id):
            return values

        raise HopprValidationError("Missing license name or id", check_name="licenses.name-or-id")


LicenseValidator.update_forward_refs()


class ComponentValidator(BaseValidator, cdx.Component):
    """Model to perform validation checks on components."""

    licenses: list[LicenseValidator] | None = None
    components: list[ComponentValidator] | None = None  # type: ignore[assignment]

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def _validate(cls, values: DictStrAny) -> DictStrAny:
        component_id = "@".join(filter(None, [values.get("name"), values.get("version")]))

        BaseValidator.notify(
            f"Validating component: {component_id}",
            log_level=logging.INFO,
            indent_level=1,
        )

        for license_ in values.get("licenses") or []:
            try:
                LicenseValidator.validate(license_)
            except ValidationError as ex:
                license_id = (
                    license_.get("expression")
                    if "expression" in license_
                    else str(license_.get("license").get("id") or license_.get("license").get("name"))
                )

                BaseValidator.notify(
                    f"Issues found for license {license_id}:",
                    log_level=logging.INFO,
                    indent_level=2,
                )

                for error in ex.errors():
                    ctx = error.get("ctx", {})
                    check_name = ctx.get("check_name", "")

                    BaseValidator.notify(
                        msg=str(error.get("msg")),
                        log_level=_get_log_level(f"components.{check_name}"),
                        indent_level=3,
                    )

        return values

    _validate_licenses_field = _field_validator("licenses", check_name="components.licenses.licenses-field")
    _validate_supplier = _field_validator("supplier", check_name="components.supplier-field")
    _validate_name = _field_validator("name", check_name="components.name-field")
    _validate_version = _field_validator("version", check_name="components.version-field")
    _validate_unique_id = _field_validator("cpe", "purl", "swid", check_name="components.unique-id")


ComponentValidator.update_forward_refs()


class MetadataValidator(BaseValidator, cdx.Metadata):
    """Model to perform validation checks on SBOM metadata."""

    timestamp: str | None = None  # type: ignore[assignment]
    tools: list | dict | None = None  # type: ignore[assignment]
    component: ComponentValidator | None = None
    licenses: list[LicenseValidator] | None = None

    @root_validator(allow_reuse=True, pre=True)
    @classmethod
    def _validate(cls, values: DictStrAny) -> DictStrAny:
        BaseValidator.notify("Validating Metadata", indent_level=1)
        for license_ in values.get("licenses") or []:
            try:
                LicenseValidator.validate(license_)
            except ValidationError as ex:
                license_id = (
                    license_.get("expression")
                    if "expression" in license_
                    else str(license_.get("license").get("id") or license_.get("license").get("name"))
                )

                BaseValidator.notify(
                    f"Issues found for license {license_id}:",
                    log_level=logging.INFO,
                    indent_level=2,
                )

                for error in ex.errors():
                    ctx = error.get("ctx", {})
                    check_name = ctx.get("check_name", "")

                    BaseValidator.notify(
                        msg=str(error.get("msg")),
                        log_level=_get_log_level(f"components.{check_name}"),
                        indent_level=3,
                    )

        return values

    _validate_timestamp = _field_validator("timestamp", check_name="metadata.timestamp")
    _validate_authors = _field_validator("authors", "tools", check_name="metadata.authors")
    _validate_licenses_field = _field_validator("licenses", check_name="metadata.licenses.licenses-field")
    _validate_supplier = _field_validator("supplier", check_name="metadata.supplier-field")


MetadataValidator.update_forward_refs()


class SbomValidator(BaseValidator, cdx.CyclonedxSoftwareBillOfMaterialsStandard):
    """Model to perform validation checks on overall SBOM document."""

    metadata: MetadataValidator | None = None
    components: list[ComponentValidator] | None = None  # type: ignore[assignment]

    _validate_components_field = _field_validator("components", check_name="sbom.components-field")
    _validate_vulnerabilities_field = _field_validator("vulnerabilities", check_name="sbom.vulnerabilities-field")
    _validate_unique_id = _field_validator("serialNumber", check_name="sbom.unique-id")

    @root_validator(pre=True)
    @classmethod
    def _remove_schema_field(cls, values: DictStrAny) -> DictStrAny:
        values.pop("$schema", None)

        return values

    @validator("specVersion", always=True, pre=True)
    @classmethod
    def _validate_spec_version(cls, spec_version: str) -> str:
        match spec_version:
            case "1.2":
                raise HopprValidationError(
                    f"Got specVersion {spec_version}; cannot be validated",
                    check_name="sbom.spec-version",
                )
            case "1.3" | "1.4":
                raise HopprValidationError(
                    f"Got specVersion {spec_version}; should be 1.5",
                    check_name="sbom.spec-version",
                )
            case "1.5":
                return spec_version
            case _:
                raise HopprValidationError(
                    f"Got an invalid specVersion of {spec_version}; should be 1.5",
                    check_name="sbom.spec-version",
                )


SbomValidator.update_forward_refs()


def validate(sbom_file: Path) -> IssueList:
    """Run validation against SBOM(s) with specified configuration.

    Args:
        sbom_file: Path to a file to run validation against.
    """
    # Get previously parsed ValidateConfig. Each call returns
    # the existing config without instantiating a new one.
    global _CONFIG
    _CONFIG = ValidateConfig()

    issue_list = IssueList()

    try:
        SbomValidator.parse_file(sbom_file)
    except ValidationError as exc:
        # Capture errors and create Code Climate issue for each
        issue_list.extend(_get_file_issue_list(exc, sbom_file))

    return issue_list
