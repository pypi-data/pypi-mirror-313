"""Generate JSON schema files from pydantic models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from hoppr.models import (
    CredentialsFile,
    HopprBaseModel,
    HopprSchemaModel,
    ManifestFile,
    TransferFile,
    ValidateConfig,
)

_yaml_writer = YAML(typ="safe", pure=True)
_yaml_writer.default_flow_style = False
_yaml_writer.map_indent = 2
_yaml_writer.sequence_indent = 4
_yaml_writer.sequence_dash_offset = 2
_yaml_writer.sort_base_mapping_type_on_output = False  # type: ignore[assignment]


def write_json_schema(schema_name: str, model_type: type[HopprBaseModel]) -> None:  # pragma: no cover
    """Write JSON schema to file."""
    schema_file = Path(f"hoppr-{schema_name}-schema-v1.json")
    schema_file.write_text(data=model_type.schema_json(indent=2), encoding="utf-8")


def write_yaml_schema(schema_name: str, model_type: type[HopprBaseModel]) -> None:  # pragma: no cover
    """Write YAML schema to file."""
    schema_file = Path(f"hoppr-{schema_name}-schema-v1.yml")

    _yaml_writer.dump(data=model_type.schema(by_alias=True), stream=schema_file)

    # Replace generated single quotes with double
    content = schema_file.read_text(encoding="utf-8")
    content = content.replace("'", '"')
    content = f"---\n{content}"
    schema_file.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    schema_args: list[dict[str, Any]] = [
        {"schema_name": "credentials", "model_type": CredentialsFile},
        {"schema_name": "manifest", "model_type": ManifestFile},
        {"schema_name": "transfer", "model_type": TransferFile},
        {"schema_name": "combined", "model_type": HopprSchemaModel},
        {"schema_name": "validate-config", "model_type": ValidateConfig},
    ]

    for args in schema_args:
        # Write JSON schema files
        write_json_schema(**args)

        # Write YAML schema files
        write_yaml_schema(**args)
