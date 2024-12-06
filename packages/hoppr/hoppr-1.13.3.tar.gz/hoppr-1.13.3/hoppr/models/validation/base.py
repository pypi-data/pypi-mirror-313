"""Base model for `hopctl validate sbom` configuration models."""

from __future__ import annotations

import importlib
import inspect
import logging

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias, TypeGuard

import hoppr_cyclonedx_models.base as cdx_base

from pydantic import ConstrainedStr, Field, create_model, root_validator
from typing_extensions import Self

from hoppr.models.base import CycloneDXBaseModel, HopprBaseModel

if TYPE_CHECKING:
    from collections.abc import ValuesView

    from pydantic.fields import ModelField

    DictStrAny: TypeAlias = dict[str, Any]


def _is_list_model_field(field: ModelField) -> bool:
    return any(
        getattr(sub_field, "type_", None)
        and inspect.isclass(object=sub_field.type_)
        and issubclass(sub_field.type_, cdx_base.CycloneDXBaseModel)
        for sub_field in field.sub_fields or []
    )


def _is_model(obj: object) -> TypeGuard[type[cdx_base.CycloneDXBaseModel]]:
    return (
        inspect.isclass(obj)
        and obj.__module__.startswith(("hoppr.models", "hoppr_cyclonedx_models"))
        and issubclass(obj, cdx_base.CycloneDXBaseModel)
    )


class BaseCheckConfig(HopprBaseModel, alias_generator=lambda field_name: field_name.replace("_", "-"), frozen=True):
    """Base class for validation config definitions (singleton, immutable)."""

    __instance__: ClassVar[Self]

    def __new__(cls, *args, **kwargs) -> Self:  # noqa: D102
        if not getattr(cls, "__instance__", None):
            cls.__instance__ = super().__new__(cls)

        return cls.__instance__


BaseCheckConfig.update_forward_refs()


class BaseExcludeConfig(BaseCheckConfig):
    """Generates field definitions for items to exclude from validation.

    This class defines its fields dynamically based on the CycloneDX spec,
    so the final schema for the `exclude:` field is not generated until
    subclassed (i.e. until `__init_subclass__` is executed).
    """

    def __init_subclass__(cls) -> None:
        # Get all base `hoppr_cyclonedx_models.cyclonedx_1_5` model classes, excluding enum types and annotated types.
        # Classes in `hoppr_cyclonedx_models` are overridden by the redefined models in `hoppr` having the same name
        models: ValuesView[type[cdx_base.CycloneDXBaseModel]] = {
            model_name: model_cls
            for module_name in [
                "hoppr_cyclonedx_models.cyclonedx_1_5",
                "hoppr.models.affect",
                "hoppr.models.licenses",
                "hoppr.models.sbom",
            ]
            for model_name, model_cls in inspect.getmembers(
                object=importlib.import_module(name=module_name),
                predicate=_is_model,
            )
        }.values()

        field_definitions: dict[str, tuple[Any, Any]] = {
            field.name: (
                list[dict | ExcludePattern] | None,
                Field(
                    default=None,
                    title=field.field_info.title or field.name,
                    description=field.field_info.description or field.name,
                ),
            )
            for model in models
            for field in filter(_is_list_model_field, model.__fields__.values())
        }  # fmt: skip

        subclass_model = create_model(
            cls.__name__,
            __base__=BaseCheckConfig,
            __module__=__name__,
            **field_definitions,
        )  # type: ignore[call-overload]

        cls.__fields__ = subclass_model.__fields__

        return super().__init_subclass__()


BaseExcludeConfig.update_forward_refs()


class BaseValidator(CycloneDXBaseModel):
    """Base CycloneDX validator class."""

    # Mapping of check IDs to list of callback functions to report result
    observers: ClassVar[dict[object, Callable]] = {}

    @root_validator(pre=True, allow_reuse=True)
    @classmethod
    def remove_if_empty(cls, values: DictStrAny) -> DictStrAny:
        """Remove keys with falsy values to ensure they are counted as missing during validation."""
        for key, value in dict(values).items():
            if not value:
                values.pop(key, None)

        return values

    @classmethod
    def notify(cls, msg: str, log_level: int = logging.INFO, indent_level: int = 0) -> None:
        """Call the callback function for all registered subscribers."""
        for callback in cls.observers.values():
            callback(log_level, msg, indent_level=indent_level)

    @classmethod
    def subscribe(cls, observer: object, callback: Callable) -> None:
        """Register an observer."""
        cls.observers[observer] = callback

    @classmethod
    def unsubscribe(cls, observer: object) -> None:
        """Unregister an observer."""
        cls.observers.pop(observer, None)


BaseValidator.update_forward_refs()


class ExcludePattern(ConstrainedStr):
    """String with regular expression match constraint."""

    min_length = 1
    regex = r"^regexp:\/.+\/[gmi]*|jmespath:.+|.+"
    strip_whitespace = True
