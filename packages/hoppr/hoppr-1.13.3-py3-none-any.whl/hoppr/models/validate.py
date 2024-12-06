"""Result models for `hopctl validate sbom`."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeAlias

from pydantic import Field
from typing_extensions import Self, override

import hoppr.utils

from hoppr.models.base import HopprBaseModel
from hoppr.models.sbom import Component, Sbom
from hoppr.result import Result, ResultStatus

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping


DictStrAny: TypeAlias = dict[str, Any]


def _encode_result(result: ValidateCheckResult) -> Mapping[str, str]:
    return {"status": result.status.name, "message": result.message}


class ValidateCheckResult(Result):
    """`Result` that can be deserialized from JSON."""

    def __init__(self, status: ResultStatus | str, message: str = "", return_obj: Component | Sbom | None = None):
        super().__init__(status=ResultStatus[str(status)], message=message, return_obj=return_obj)

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls, result: Self | DictStrAny) -> Self:
        """Validator to deserialize a result status JSON string into a `Result` object."""
        if isinstance(result, dict):
            message: str = result.get("message", "")
            status: str = str(result.get("status"))

            result = cls(status=ResultStatus[status], message=message)

        return result

    @override
    def merge(self, other: Result):
        super().merge(other)

        # Remove duplicate messages from this result
        messages = self.message.split("\n")
        messages = hoppr.utils.dedup_list(messages)

        self.message = "\n".join(messages)


class ValidateBaseModel(HopprBaseModel, json_encoders={ValidateCheckResult: _encode_result}):
    """Base model for `hopctl validate sbom` results."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and all(
            getattr(self, name) == getattr(other, name) for name in self.__fields__
        )


class ValidateLicenseResult(ValidateBaseModel):
    """Results of `hopctl validate sbom` for an individual license."""

    license_id: str
    expiration: ValidateCheckResult = Field(default=ValidateCheckResult.success(message="License Expiration"))
    required_fields: ValidateCheckResult = Field(default=ValidateCheckResult.success(message="Required License Fields"))


class ValidateComponentResult(ValidateBaseModel):
    """Results of `hopctl validate sbom` for an individual component."""

    component_id: str
    license_results: list[ValidateLicenseResult] = Field(default=[])
    ntia_fields_result: ValidateCheckResult = Field(default=ValidateCheckResult.success(message="Minimum NTIA Fields"))
    result: ValidateCheckResult = Field(default=ValidateCheckResult.success())


class ValidateSbomResult(ValidateBaseModel):
    """Results of `hopctl validate sbom` for an SBOM file."""

    name: str
    component_results: list[ValidateComponentResult] = Field(default=[])
    license_results: list[ValidateLicenseResult] = Field(default=[])
    ntia_fields_result: ValidateCheckResult = Field(default=ValidateCheckResult.success(message="Minimum NTIA Fields"))
    result: ValidateCheckResult = Field(default=ValidateCheckResult.success())
    spec_version_result: ValidateCheckResult = Field(
        default=ValidateCheckResult.success(message="CycloneDX Specification Version")
    )
