"""Base model for Hoppr config files."""

from __future__ import annotations

import functools
import io
import json
import sys

from collections.abc import Callable, MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, ClassVar, Literal, TypeGuard, TypeVar

import hoppr_cyclonedx_models.base as cdx_base
import hoppr_cyclonedx_models.cyclonedx_1_5 as cdx

from pydantic import BaseConfig, BaseModel, Extra, Field, Protocol, create_model, validator
from rich.markdown import Markdown
from ruamel.yaml import YAML
from typing_extensions import Self

import hoppr.utils

if TYPE_CHECKING:
    from pydantic.types import StrBytes
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny
    from rich.console import Console, ConsoleOptions, RenderResult
    from rich.repr import RichReprResult

    YamlStyle = Literal["", '"', "'", "|", ">"] | None

AnyCycloneDXModel = TypeVar("AnyCycloneDXModel", bound="CycloneDXBaseModel")
ExtendedProto = Protocol | Literal["yaml", "yml"]
UniqueIDMap = Annotated[MutableMapping[str, AnyCycloneDXModel], Field(default=...)]

__all__: list[str] = []


class HopprBaseModel(BaseModel):
    """Base Hoppr data model."""

    class Config(BaseConfig):
        """Config options for HopprBaseModel."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        extra = Extra.forbid
        use_enum_values = True

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """Define to test equality or uniqueness between objects."""
        return hash(repr(self))

    def __repr__(self) -> str:
        attributes = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items() if value)
        return f"{type(self).__name__}({attributes})"

    def __rich_repr__(self) -> RichReprResult:
        yield from [(key, value) for key, value in self.__dict__.items() if value]

    @classmethod
    def parse_file(
        cls,
        path: str | Path,
        *,
        content_type: str | None = None,
        encoding: str = "utf-8",
        proto: ExtendedProto | None = None,
        allow_pickle: bool = False,
    ) -> Self:
        path = Path(path)

        return cls.parse_raw(
            path.read_text(),
            allow_pickle=allow_pickle,
            content_type=content_type,
            encoding=encoding,
            proto=proto,
        )

    @classmethod
    def parse_raw(
        cls,
        b: StrBytes,
        *,
        content_type: str | None = None,
        encoding: str = "utf-8",
        proto: ExtendedProto | None = None,
        allow_pickle: bool = False,
    ) -> Self:
        return cls.parse_obj(hoppr.utils.load_string(b if isinstance(b, str) else b.decode()))

    def yaml(
        self,
        *,
        include: AbstractSetIntStr | MappingIntStrAny | None = None,
        exclude: AbstractSetIntStr | MappingIntStrAny | None = None,
        by_alias: bool = True,
        skip_defaults: bool | None = None,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        sort_keys: bool = False,
        default_flow_style: bool | None = False,
        default_style: YamlStyle = None,
        indent: bool | None = True,
        encoding: str | None = None,
        **kwargs,
    ) -> str:
        """Generate a YAML representation of the model instance.

        Args:
            include: Fields to include. See `BaseModel.dict()`.
            exclude: Fields to exclude. See `BaseModel.dict()`.
            by_alias: Whether to use aliases instead of declared names. Defaults to False.
            skip_defaults: See `BaseModel.dict()`.
            exclude_unset: See `BaseModel.dict()`.
            exclude_defaults: See `BaseModel.dict()`.
            exclude_none: See `BaseModel.dict()`.
            sort_keys: If True, will sort the keys in alphanumeric order for dictionaries.
                Defaults to False, which will dump in the field definition order.
            default_flow_style: Whether to use the "flow" style in the dumper. Defaults to False,
                which uses the "block" style (probably the most familiar to users).
            default_style: This is the default style for quoting strings, used by `ruamel.yaml` dumper.
                One of: {None, "", "'", '"', "|", ">"}.
                Defaults to None, which varies the style based on line length.
            indent: Additional arguments for the dumper.
            encoding: Additional arguments for the dumper.
            kwargs: Additional arguments for the dumper.

        Returns:
            The encoded YAML string.
        """
        # Serialize to JSON first rather than calling self.dict()
        model_json = self.json(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

        data = json.loads(model_json)

        stream = io.StringIO()
        stream.write("---\n")

        yaml_writer = YAML(typ="safe", pure=True)
        yaml_writer.default_flow_style = default_flow_style
        yaml_writer.default_style = default_style  # type: ignore[assignment]
        yaml_writer.encoding = encoding or "utf-8"
        yaml_writer.line_break = "\n"  # type: ignore[assignment]
        yaml_writer.map_indent = 2 if indent else None
        yaml_writer.sequence_dash_offset = 2 if indent else 0
        yaml_writer.sequence_indent = 4 if indent else None
        yaml_writer.sort_base_mapping_type_on_output = sort_keys  # type: ignore[assignment]
        yaml_writer.width = 120

        for key, value in data.items():
            yaml_writer.dump(data={key: value}, stream=stream)
            stream.write("\n")

        # Remove final extra newline character
        stream.seek(stream.tell() - 1)
        stream.truncate()

        return stream.getvalue().replace("'", '"')


class HopprMetadata(BaseModel):
    """Metadata data model."""

    name: str
    version: str | int
    description: str


class HopprBaseSchemaModel(HopprBaseModel):
    """Base Hoppr config file schema model."""

    kind: Literal["Credentials", "Manifest", "Transfer"] = Field(description="Data model/schema kind")
    metadata: HopprMetadata | None = Field(default=None, description="Metadata for the file")
    schema_version: str = Field(default="v1", alias="schemaVersion", title="Schema Version")

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:  # pragma: no cover
        yield Markdown(
            markup="\n".join([
                "```yaml",
                self.yaml(),
                "```",
            ]).strip("\n"),
            code_theme="github-dark",
        )

    @validator("kind", allow_reuse=True, pre=True)
    @classmethod
    def validate_kind(cls, kind: str) -> str:
        """Return supplied `kind` value with only first letter capitalized."""
        return kind.capitalize()


class CycloneDXBaseModel(
    cdx_base.CycloneDXBaseModel,
    allow_population_by_field_name=True,
    arbitrary_types_allowed=True,
    extra=Extra.allow,
    use_enum_values=True,
):
    """Base CycloneDX data model."""

    # Defining as ClassVar to allow dynamic model creation using custom root types
    deep_merge: ClassVar[bool] = False
    flatten: ClassVar[bool] = False
    observers: ClassVar[dict[object, Callable]] = {}
    unique_id_map: ClassVar[UniqueIDMap] = {}

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other) if isinstance(other, type(self)) else False

    def __hash__(self) -> int:
        return hash(self.unique_id_callback())

    def __init__(self, **data):
        super().__init__(**data)

        unique_id = self.unique_id_callback()
        type(self).unique_id_map[unique_id] = self

    def _has_field(self, field_name: str) -> bool:
        return hasattr(self, field_name) and (getattr(self, field_name) or field_name in list(self.__fields_set__))

    @staticmethod
    def _is_model_list_field(field: object) -> TypeGuard[list[CycloneDXBaseModel]]:
        """Checks if the provided field is a list of the specified type."""
        return isinstance(field, list) and bool(field) and all(isinstance(item, CycloneDXBaseModel) for item in field)

    def _merge_field(self, target_field_name: str, source_field: object) -> None:
        """Merges `source_field` into the field referenced by `target_field_name`."""
        merged_field = getattr(self, target_field_name)
        field_type = type(merged_field)

        if not self._has_field(target_field_name):
            setattr(self, target_field_name, source_field)
            return

        if isinstance(field_type, type(BaseModel)) and isinstance(source_field, field_type):
            merged_field = CycloneDXBaseModel.create(model=merged_field)
            source_field = type(merged_field).create(model=source_field)
            merged_field.merge(source_field)
        elif self._is_model_list_field(merged_field) or self._is_model_list_field(source_field):
            merged_field = hoppr.utils.dedup_list([CycloneDXBaseModel.create(model=_field) for _field in merged_field])
            source_field = [CycloneDXBaseModel.create(model=_field) for _field in source_field or []]  # type: ignore[attr-defined]
            self._merge_field_items(merged_field, source_field)

        setattr(self, target_field_name, merged_field)

    @staticmethod
    def _merge_field_items(target_field: list[CycloneDXBaseModel], source_field: list[CycloneDXBaseModel]) -> None:
        """Merges the items from `source_field` into `target_field`."""
        for source_item in source_field:
            if source_item in target_field:
                merged_item = target_field[target_field.index(source_item)]
                merged_item.merge(source_item)
            else:
                target_field.append(source_item)

    def unique_id_callback(self) -> str:
        """Default callback method to get a model object's unique ID."""
        try:
            callback = {
                "Advisory": lambda obj: obj.url,
                "Annotations": lambda obj: obj.bom_ref or obj.text,
                "Command": lambda obj: obj.executed or repr(self),
                "Commit": lambda obj: obj.uid,
                "Component": lambda obj: obj.bom_ref,
                "ComponentData": lambda obj: obj.bom_ref or repr(self),
                "Copyright": lambda obj: obj.text,
                "Dependency": lambda obj: obj.ref,
                "ExternalReference": lambda obj: f"{obj.type}-{obj.url}",
                "Formula": lambda obj: obj.bom_ref or repr(self),
                "License": lambda obj: obj.id or obj.name or repr(self),
                "LicenseChoice": lambda obj: obj.license or obj.expression or repr(self),
                "Note": lambda obj: obj.text,
                "Occurrence": lambda obj: obj.bom_ref or repr(self),
                "Reference": lambda obj: obj.id,
                "Sbom": lambda obj: obj.serialNumber,
                "Service": lambda obj: obj.bom_ref or f"{obj.name}-{obj.version}",
                "Signer": lambda obj: obj.value,
                "Task": lambda obj: obj.bom_ref or obj.uid,
                "Vulnerability": lambda obj: obj.id or repr(self),
                "Workflow": lambda obj: obj.bom_ref or obj.uid,
                "Workspace": lambda obj: obj.bom_ref or obj.uid,
            }[type(self).__name__]

            return callback(self)
        except KeyError:
            return repr(self)

    @classmethod
    def create(cls, model: cdx_base.CycloneDXBaseModel) -> Self:
        """Update a BaseModel object with CycloneDXBaseModel attributes and methods.

        Args:
            model (cdx_base.CycloneDXBaseModel): The `hoppr-cyclonedx-models` object to update

        Returns:
            AnyCycloneDXModel: The updated BaseModel object
        """
        model_cls = cls.make_model(name=type(model).__name__)
        return model_cls(**model.dict(by_alias=True, exclude_none=True, exclude_unset=True))

    @classmethod
    @functools.cache
    def make_model(cls, name: str) -> type[Self]:
        """Dynamically create a model class suitable for merging.

        Args:
            name (str): Name of the existing model

        Returns:
            type[AnyCycloneDXModel]: The generated model class
        """
        # Return explicitly defined models directly
        members = {
            **sys.modules[f"{__package__}.affect"].__dict__,
            **sys.modules[f"{__package__}.annotations"].__dict__,
            **sys.modules[f"{__package__}.licenses"].__dict__,
            **sys.modules[f"{__package__}.sbom"].__dict__,
        }

        if model_cls := members.get(name):
            return model_cls

        model_cls = cdx.__dict__[name]

        merge_model = create_model(model_cls.__name__, __base__=(cls, model_cls), __module__=__name__)

        # Set model's pydantic `Config` class and `__hash__` method
        merge_model.__config__ = cls.__config__

        # Add `unique_id_map` class attribute for caching model objects
        merge_model.__class_vars__.add("unique_id_map")
        merge_model.__annotations__["unique_id_map"] = "ClassVar[UniqueIDMap]"
        merge_model.unique_id_map = {}

        # Add updated model to current module and make importable from other modules
        setattr(sys.modules[__name__], merge_model.__name__, merge_model)
        global __all__
        __all__ += [merge_model.__name__]

        merge_model.update_forward_refs()

        return merge_model

    @classmethod
    def find(cls, unique_id: str) -> Self | None:
        """Look up model object by its unique ID string.

        Args:
            unique_id (str): Unique ID string to look up

        Returns:
            AnyCycloneDXModel | None: Model object if found, otherwise None
        """
        return cls.unique_id_map.get(unique_id)

    def merge(self, other: CycloneDXBaseModel) -> None:
        """Merge model instance of same type into self.

        Args:
            other (CycloneDXBaseModel): Model object to merge
        """
        if (self_type := type(self).__name__) != (other_type := type(other).__name__):
            raise TypeError(f"Type '{other_type}' cannot be merged into '{self_type}'")

        self.notify(data=f"  Merging '{type(self).__qualname__}' attributes...")

        for field_name in self.__fields__:
            self.notify(data=f"    Merging field '{type(self).__qualname__}.{field_name}'...")

            if (source_field := getattr(other, field_name, None)) is None:
                continue

            self._merge_field(field_name, source_field)

    def notify(self, data: str) -> None:
        """Call the callback function for all registered subscribers."""
        for callback in self.observers.values():
            callback(data)

    def subscribe(self, observer: object, callback: Callable) -> None:
        """Register an observer."""
        self.observers[observer] = callback

    def unsubscribe(self, observer: object) -> None:
        """Unregister an observer."""
        self.observers.pop(observer, None)
