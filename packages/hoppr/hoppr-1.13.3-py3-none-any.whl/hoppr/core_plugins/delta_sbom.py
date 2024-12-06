"""Plugin to remove SBOM components that are specified by a "previous" SBOM."""

from __future__ import annotations

import io
import tarfile

from pathlib import Path
from typing import TYPE_CHECKING

import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_process
from hoppr.exceptions import HopprError, HopprLoadDataError
from hoppr.models.manifest import Manifest
from hoppr.models.sbom import Component, Sbom
from hoppr.models.types import BomAccess
from hoppr.result import Result

if TYPE_CHECKING:
    from packageurl import PackageURL


class DeltaSbom(HopprPlugin, bom_access=BomAccess.FULL_ACCESS, products=["generic/_metadata_/_previous_bom.json"]):
    """Plugin to remove SBOM components that are specified by a "previous" SBOM."""

    def get_version(self) -> str:  # noqa: D102
        return __version__

    @hoppr_process
    def pre_stage_process(self) -> Result:
        """Tar-up the context.collect_root_dir directory."""
        self.config = self.config or {}

        try:
            previous_source = str(next(filter(None, [self.context.previous_delivery, self.config.get("previous")])))
        except StopIteration:
            return Result.success(
                "No previously delivered bundle specified for delta bundle. All components will be delivered"
            )

        fail_on_empty = bool(self.config.get("fail_on_empty"))

        if not Path(previous_source).exists():
            return Result.fail(f'Previous source file "{previous_source}" not found.')

        self.get_logger().info("Creating delta/update SBOM, previous SBOM being retrieved from %s", previous_source)

        previous_sbom = self._get_previous_bom(previous_source)

        target_dir = self.context.collect_root_dir / "generic" / "_metadata_"
        target_dir.mkdir(parents=True, exist_ok=True)

        with (target_dir / "_previous_bom.json").open(mode="w", encoding="utf-8") as bom_data:
            bom_data.write(previous_sbom.json(exclude_none=True, by_alias=True, indent=2))

        delta_sbom = self.context.delivered_sbom.copy(deep=True)
        delta_sbom.components.clear()

        for new_comp in self.context.delivered_sbom.components or []:
            include_component = not any(
                DeltaSbom._component_match(new_comp, prev_comp) for prev_comp in previous_sbom.components or []
            )
            if include_component:
                self.get_logger().debug("Including purl %s", new_comp.purl, indent_level=1)
                delta_sbom.components.append(new_comp)

        self.get_logger().info("Input sbom has %d components", len(self.context.delivered_sbom.components))
        self.get_logger().info("Prev  sbom has %d components", len(previous_sbom.components))
        self.get_logger().info("Delta sbom has %d components", len(delta_sbom.components))

        if len(delta_sbom.components) == 0:
            msg = f'No components updated since "{previous_source}".'

            return Result.fail(msg) if fail_on_empty else Result.success(msg)

        return Result.success(
            f"Delivering updates for {len(delta_sbom.components)} of "
            f"{len(self.context.delivered_sbom.components)} components.",
            return_obj=delta_sbom,
        )

    def _extract_tarfile_bom(self, source: str) -> Sbom:
        with tarfile.open(source) as tar:
            buffer = tar.extractfile("./generic/_metadata_/_consolidated_bom.json")

            if buffer is None:
                raise HopprError("Unable to extract BOM file from tar")

            with io.TextIOWrapper(buffer) as bom_file:
                content: str = bom_file.read()
                bom_dict = hoppr.utils.load_string(content)

                if not isinstance(bom_dict, dict):
                    raise HopprError("Invalid BOM file retrieved from tar")

                return Sbom(**bom_dict)

    def _get_previous_bom(self, source: str) -> Sbom:
        if tarfile.is_tarfile(name=source):
            return self._extract_tarfile_bom(source)

        Sbom.loaded_sboms.clear()

        data = hoppr.utils.load_file(Path(source))
        if not isinstance(data, dict):
            raise HopprLoadDataError("Previous delivery file not loaded as dictionary")

        # Try parsing previous delivery as SBOM file
        if "bomFormat" in data:
            return Sbom.load(Path(source))

        return Manifest.load(Path(source)).consolidated_sbom

    @staticmethod
    def _purl_match(new_purl: PackageURL, prev_purl: PackageURL) -> bool:
        if any(
            getattr(new_purl, attr) != getattr(prev_purl, attr)
            for attr in ["name", "type", "namespace", "version", "subpath"]
        ):
            return False

        qual_keys = list(new_purl.qualifiers.keys())
        qual_keys.extend(list(prev_purl.qualifiers.keys()))

        return all(
            new_purl.qualifiers.get(key) == prev_purl.qualifiers.get(key) for key in hoppr.utils.dedup_list(qual_keys)
        )

    @staticmethod
    def _component_match(new_comp: Component, prev_comp: Component) -> bool:
        if not (new_comp.purl and prev_comp.purl):
            return False

        new_purl = hoppr.utils.get_package_url(new_comp.purl)
        prev_purl = hoppr.utils.get_package_url(prev_comp.purl)

        if not DeltaSbom._purl_match(new_purl, prev_purl):
            return False

        hash_matches = 0

        for new_hash in new_comp.hashes:
            for prev_hash in prev_comp.hashes:
                if new_hash.alg != prev_hash.alg:
                    continue
                if new_hash.content != prev_hash.content:
                    return False
                hash_matches += 1

        if hash_matches > 0:
            return True

        return new_purl.version is not None and new_purl.version != "latest"
