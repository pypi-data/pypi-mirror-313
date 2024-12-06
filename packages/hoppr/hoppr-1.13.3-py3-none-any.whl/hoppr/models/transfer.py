"""Transfer file data model."""

from __future__ import annotations

import math
import os

from enum import Enum
from importlib.metadata import entry_points
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Literal

from pydantic import Field, root_validator, validator
from typing_extensions import Self

import hoppr.utils

from hoppr.models.base import HopprBaseModel, HopprBaseSchemaModel

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny
else:
    DictStrAny = dict[str, Any]

_DELTA_SBOM_REFS = {"DeltaSbom", "delta_sbom", "hoppr.core_plugins.delta_sbom"}

# Constrained string type for stage key name
StageName = Annotated[str, Field(regex=r"^\S+", min_length=1)]


class Plugin(HopprBaseModel):
    """Plugin data model."""

    name: str = Field(..., description="Name of plugin")
    config: DictStrAny | None = Field(None, description="Mapping of additional plugin configuration settings to values")

    @root_validator(pre=True)
    @classmethod
    def validate_plugin(cls, values: DictStrAny) -> DictStrAny:
        """Validate Plugin model."""
        name = values.get("name")
        plugin_eps = entry_points(group="hoppr.plugin")

        for plugin in plugin_eps:
            # Check project entry points for plugin name, module, or class
            if str(name) in {plugin.name, plugin.module, plugin.attr}:
                values["name"] = plugin.module
                break

        return values


Plugin.update_forward_refs()


class ComponentCoverage(Enum):
    """Enumeration to indicate how often each component should be processed."""

    OPTIONAL = (0, math.inf)
    EXACTLY_ONCE = (1, 1)
    AT_LEAST_ONCE = (1, math.inf)
    NO_MORE_THAN_ONCE = (0, 1)

    def __init__(self, min_allowed: int, max_allowed: int):
        self.min_value = min_allowed
        self.max_value = max_allowed

    def __str__(self) -> str:
        return str(self.name)

    def accepts_count(self, count: int) -> bool:
        """Identifies whether a specified count is acceptable for this coverage value."""
        return self.min_value <= count <= self.max_value


class Stage(HopprBaseModel):
    """Stage data model."""

    component_coverage: Literal["AT_LEAST_ONCE", "EXACTLY_ONCE", "NO_MORE_THAN_ONCE", "OPTIONAL"] | None = Field(
        default=None, exclude=True, description="Defines how often components should be processed"
    )
    plugins: list[Plugin] = Field(..., description="List of Hoppr plugins to load")


class StageRef(Stage):
    """StageRef data model."""

    name: StageName


Stages = Annotated[dict[StageName, Stage], ...]


class TransferFile(HopprBaseSchemaModel):
    """Transfer file data model."""

    kind: Literal["Transfer"]
    max_processes: int | None = Field(
        default_factory=os.cpu_count, description="Max processes to create when running Hoppr application"
    )
    stages: Stages = Field(..., description="Mapping of stage names to property definitions")

    @classmethod
    def parse_file(cls, path: str | Path, *args, **kwargs) -> Self:
        """Override to resolve local file paths relative to transfer file."""
        path = Path(path)

        data = hoppr.utils.load_file(path)
        if not isinstance(data, dict):
            raise TypeError("Local file content was not loaded as dictionary")

        stages = data.get("stages", {})
        plugins = [plugin for stage in stages.values() for plugin in stage.get("plugins", [])]

        # Resolve DeltaSbom previous delivery path relative to transfer file
        for plugin in plugins:
            if plugin.get("name") in _DELTA_SBOM_REFS and plugin.get("config", {}).get("previous"):
                previous = (path.parent / plugin["config"]["previous"]).resolve()
                plugin["config"]["previous"] = str(previous)

        return cls(**data)


class Transfer(TransferFile):
    """Transfer data model."""

    stages: list[StageRef]  # type: ignore[assignment]

    @validator("stages", allow_reuse=True, pre=True)
    @classmethod
    def validate_stages(cls, stages: DictStrAny) -> list[StageRef]:
        """Transform Stages into list of StageRef objects."""
        stage_refs: list[StageRef] = []
        plugin_names = set()

        for stage_name, stage in stages.items():
            stage["name"] = stage_name
            stage_refs.append(StageRef.parse_obj(stage))

            plugin_names.update({plugin["name"] for plugin in stage["plugins"]})

        if not plugin_names.intersection(_DELTA_SBOM_REFS):
            stage_refs = [
                StageRef(name=StageName("_delta_sbom_"), plugins=[Plugin(name="delta_sbom", config=None)]),
                *stage_refs,
            ]

        return stage_refs

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Self:
        """Load transfer file from local path or dict."""
        match source:
            case dict():
                return cls.parse_obj(source)
            case str() | Path():
                return cls.parse_file(source)
            case _:
                raise TypeError("'source' argument must be one of: 'str', 'Path', 'dict[str, Any]'")

    def yaml(self, *args, **kwargs) -> str:  # noqa: D102
        transfer_dict = self.dict(by_alias=True)
        transfer_dict["stages"] = {str(stage.name): {"plugins": stage.plugins} for stage in self.stages}

        return TransferFile.parse_obj(transfer_dict).yaml(*args, **kwargs)
