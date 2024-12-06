"""Configuration file models for `hopctl validate sbom`."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Final, TypeAlias

from jinja2 import Environment, PackageLoader
from pydantic import Field, validator
from typing_extensions import Self

from hoppr.models.base import HopprBaseModel
from hoppr.models.validation.base import BaseCheckConfig
from hoppr.models.validation.exclude import ExcludeConfig

if TYPE_CHECKING:
    DictStrAny: TypeAlias = dict[str, Any]


class OnCheckFail(str, Enum):
    """Values to configure response behavior for individual checks."""

    IGNORE = "ignore"
    WARN = "warn"
    ERROR = "error"

    def __str__(self) -> str:
        return self.value


class LicenseCheckConfig(BaseCheckConfig):
    """Configuration for SBOM license checks."""

    # Override parent class to bypass singleton constraint
    def __new__(cls, *args, **kwargs) -> Self:  # noqa: D102
        return super(HopprBaseModel, cls).__new__(cls)

    name_or_id: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="One of the `license.id`, `license.name` fields must be specified",
    )
    last_renewal: OnCheckFail = Field(
        default=OnCheckFail.IGNORE,
        description="The `license.licensing.lastRenewal` field is not specified",
    )
    purchase_order: OnCheckFail = Field(
        default=OnCheckFail.IGNORE,
        description="The `license.licensing.purchaseOrder` field is not specified",
    )
    license_types: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `license.licensing.licenseType` field is either not specified or empty",
    )
    licenses_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `licenses` field is either not specified or empty",
    )
    expiration: OnCheckFail = Field(
        default=OnCheckFail.IGNORE,
        description="The `license.licensing.expiration` field contains an expired or soon-to-expire date",
    )


class ComponentCheckConfig(BaseCheckConfig):
    """Configuration for SBOM component checks."""

    licenses: LicenseCheckConfig = Field(
        default=LicenseCheckConfig(),
        description="Configurations for the `components[].licenses` checks",
    )
    name_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `components[].name` field is not specified",
    )
    supplier_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `components[].supplier` field is not specified",
    )
    version_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `components[].version` field is not specified",
    )
    unique_id: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="One of the `components[].purl`, `components[].cpe`, `components[].swid` fields must be specified",
    )


class MetadataCheckConfig(BaseCheckConfig):
    """Configuration for SBOM metadata checks."""

    licenses: LicenseCheckConfig = Field(
        default=LicenseCheckConfig(),
        description="Configurations for the `metadata.licenses` checks",
    )
    authors: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="One of the `metadata.authors`, `metadata.tools` fields must be specified and not empty",
    )
    supplier_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `metadata.supplier` field is not specified",
    )
    timestamp: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `metadata.timestamp` field is either not specified or invalid",
    )


class SbomCheckConfig(BaseCheckConfig):
    """Configuration for top-level SBOM field checks."""

    components_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `components` field is either not specified or empty",
    )
    spec_version: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `specVersion` should be 1.5",
    )
    unique_id: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `serialNumber` field is either not specified or invalid",
    )
    vulnerabilities_field: OnCheckFail = Field(
        default=OnCheckFail.WARN,
        description="The `vulnerabilities` field is either not specified or empty",
    )


_CONFIG_FILE_HEADER: Final[str] = """\
# Default values for `hopctl validate sbom` configuration options and checks.
#
# Each check listed will accept a value of either `ignore`, `warn`, or `error` to configure
# desired response behavior on failure.
#
# Items can be excluded from validation altogether by specifying a pattern under the top-level
# `exclude:` key. Any items matching these patterns will not be evaluated during validation.
#
# A pattern can be one of the following forms:
#
# - `jmespath:<JMESPath search expression>`
# - An object representing objects to exclude based on the fields and patterns specified
#
# In the latter form, the name of each first child of the `exclude:` object must be one of the
# types defined as an array by the CycloneDX specification.
#
# ```yaml
# exclude:
#   <CycloneDX array object name>:  # e.g. `components`, `licenses`
#     # multiple fields defined on the same list item represent an AND relationship
#     - <field name 1>: <field value or pattern>
#       <field name 2>: <field value or pattern>
#
#     # separate list items represent an OR relationship when filtering
#     - <field name 3>: <field value or pattern>
#
#     # alternatively, exclusion filter can be specified with a JMESPath expression
#     - jmespath:<JMESPath search expression>
#
#     ...
# ```
#
# The `<field value or pattern>` above can be one of:
#
# - `regexp:/<regular expression identifying elements to exclude>/[gmi]*`
# - literal string representing the desired exclusion value
"""  # fmt: skip


class ValidateConfig(BaseCheckConfig):
    """Model for SBOM validation configuration."""

    exclude: ExcludeConfig | None = None
    sbom_checks: SbomCheckConfig = SbomCheckConfig()
    metadata_checks: MetadataCheckConfig = MetadataCheckConfig()
    component_checks: ComponentCheckConfig = ComponentCheckConfig()

    @validator("exclude", allow_reuse=True, always=True, pre=True)
    @classmethod
    def _default_exclude(cls, exclude: DictStrAny | None) -> DictStrAny:
        return exclude or {"components": [{"type": "operating-system"}]}

    def yaml(self, *args, **kwargs) -> str:
        """YAML representation of current config settings."""
        environment = Environment(
            loader=PackageLoader(
                package_name="hoppr.models.validation",
                package_path="templates",
            )
        )

        template = environment.get_template("config.yml.jinja2")

        return template.render(fields=self.__fields__.values(), obj=self, header=_CONFIG_FILE_HEADER)


ValidateConfig.update_forward_refs()
