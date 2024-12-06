"""Define constants used by Hoppr."""

from __future__ import annotations

from enum import Enum


class BomProps(str, Enum):
    """SBOM Property Field Names."""

    COLLECTION_DIRECTORY = "hoppr:collection:directory"
    COLLECTION_PLUGIN = "hoppr:collection:plugin"
    COLLECTION_REPOSITORY = "hoppr:collection:repository"
    COLLECTION_TIMETAG = "hoppr:collection:timetag"
    COLLECTION_ARTIFACT_FILE = "hoppr:collection:artifact_file"

    COMPONENT_SEARCH_SEQUENCE = "hoppr:repository:component_search_sequence"


class ConfigKeys(str, Enum):
    """Keys used in configuration files."""

    CONFIG = "config"
    PLUGINS = "plugins"
