"""Module including functions and classes for working with the in-toto spec.

This module includes a function for creating in-toto layout files, and
wrapping other processing with "start" and "stop" functions.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from in_toto.models.layout import Layout, Step
from in_toto.models.metadata import Metablock
from in_toto.runlib import in_toto_record_start, in_toto_record_stop
from securesystemslib.signer import CryptoSigner
from securesystemslib.storage import FilesystemBackend

from hoppr.utils import plugin_class

if TYPE_CHECKING:
    from hoppr.models.transfer import Transfer


def _get_products(transfer: Transfer) -> tuple[dict[str, list[str]], list[str]]:
    """Function to determine what products are produced for each "hoppr stage"/"in-toto step".

    This is done by looking at all plugins in a stage, and create a list of "products". There
    are two additional "products" included in each step/stage which are a consolidated bom
    and a delivered bom.
    """
    stages = ["_collect_metadata"]

    products = {"_collect_metadata": ["generic/_metadata_/*"]}
    for stage_ref in transfer.stages:
        stages.append(stage_ref.name)

        products[stage_ref.name] = []
        for plugin_ref in stage_ref.plugins:
            plugin_cls = plugin_class(plugin_ref.name)
            products[stage_ref.name] += plugin_cls.get_attestation_products(plugin_ref.config)

        products[stage_ref.name] += [
            "generic/_metadata_/_delivered_bom.json",
            "generic/_metadata_/_delivered_bom.json.sig",
            f"generic/_metadata_/_intermediate_{stage_ref.name}_delivered_bom.json",
            f"generic/_metadata_/_intermediate_{stage_ref.name}_delivered_bom.json.sig",
            "generic/_metadata_/_run_data_",
        ]

    stages.append("_finalize")
    products["_finalize"] = ["generic/_metadata_/_delivered_bom.json", "generic/_metadata_/_delivered_bom.json.sig"]

    return (products, stages)


def generate_in_toto_layout(
    transfer: Transfer,
    project_owner_key_path: Path,
    functionary_key_path: Path,
    project_owner_key_password: str | None = None,
    relative_expiration: int = 6,
) -> None:
    """Function to create an in-toto layout file based on a transfer object.

    The layout file will have "steps" where each "step" is equal to a hoppr stage. All files changed in a stage
    must be referenced in the "step" to have a verifiable layout. All plugins have a `products` property which
    lists the expected files it will change. The "step" products is a list of all of these hoppr plugin `products`
    of the stage.

    Additionally there are two additional "steps":
    1. _collect_metadata - wraps the `_collect_metadata()` called before hoppr processes stages
    1. _finalize - wraps the `_collect_bom()`  called after hoppr processes stages
    """
    layout = Layout()
    layout.set_relative_expiration(months=relative_expiration)

    project_owner_private_key = _load_private_key_from_file(project_owner_key_path, project_owner_key_password)

    functionary_pubkey = layout.add_functionary_key_from_path(str(functionary_key_path.with_suffix(".pub")))

    (products, stages) = _get_products(transfer)

    for i, stage in enumerate(stages):
        step = Step(name=stage, pubkeys=[functionary_pubkey["keyid"]])

        for j in range(i):
            step.add_material_rule_from_string(f"MATCH * WITH PRODUCTS FROM {stages[j]}")

        for product in products[stage]:
            step.add_product_rule_from_string(f"ALLOW {product}")

        step.add_material_rule_from_string("DISALLOW *")
        step.add_product_rule_from_string("DISALLOW *")

        layout.steps.append(step)

    metablock = Metablock(signed=layout)
    metablock.create_signature(CryptoSigner(project_owner_private_key))
    metablock.dump("in-toto.layout")


def _load_private_key_from_file(path: Path, password: str | None) -> rsa.RSAPrivateKey:
    """Internal helper to load key from PEM file."""
    data = path.read_bytes()
    password_bytes = password.encode("utf-8") if password else None

    return cast(rsa.RSAPrivateKey, serialization.load_pem_private_key(data, password_bytes, FilesystemBackend()))


class HopprInTotoLinks:
    """Class for managing state of in-toto "start" and "stop" function calls.

    The intent is to simplify the creation of in-toto link (aka attestation) files.
    These methods are used to "wrap" hoppr processing capabilities to track changes
    to the temporary hoppr storage location.

    This wrapping of hoppr processing capabilities should be on stages (not plugins)
    to allow parallel processing of plugins.
    """

    def __init__(
        self,
        create_attestations: bool,
        transfer: Transfer,
        functionary_key_path: Path | None = None,
        functionary_key_password: str | None = None,
        metadata_directory: str | None = None,
    ) -> None:
        self.create_attestations = create_attestations

        if self.create_attestations:
            self.products, _ = _get_products(transfer)
            self.functionary_key_signer = (
                CryptoSigner(_load_private_key_from_file(functionary_key_path, functionary_key_password))
                if functionary_key_path
                else None
            )
            self._collection_root = ""
            self.metadata_directory = metadata_directory

    @property
    def collection_root(self) -> str:
        """Collection root location."""
        return self._collection_root

    @collection_root.setter
    def collection_root(self, collection_root: str):
        """Setter method for the collection root location.

        Since the collection root is a temporary directory, its created after
        the hoppr_in_toto_links object is created.
        """
        self._collection_root = collection_root

    def record_stage_start(self, stage_name: str):
        """Method called just before a stage is processed.

        This will call the in-toto framework and record all files within the hoppr temporary
        processing folder.
        """
        if self.create_attestations:
            in_toto_record_start(
                step_name=stage_name,
                material_list=["./"],
                base_path=self.collection_root,
                record_environment=True,
                signer=self.functionary_key_signer,
            )

    def record_stage_stop(self, stage_name: str):
        """Method called just after a stage is processed.

        This will call the in-toto framework and record all products files produced based on the
        expected products of the plugins running in the stage.
        """
        if self.create_attestations:
            # Use pathlib to find files using wildcard in names
            posix_path_list: list[Path] = []
            for product in self.products[stage_name]:
                posix_path_list += Path(self.collection_root).glob(product)

            # After finding paths, convert them to strings that are a relative path from
            # the collect root directory.
            product_list = [str(posix_path.relative_to(self.collection_root)) for posix_path in posix_path_list]

            in_toto_record_stop(
                step_name=stage_name,
                product_list=product_list,
                base_path=self.collection_root,
                metadata_directory=self.metadata_directory,
                signer=self.functionary_key_signer,
            )
