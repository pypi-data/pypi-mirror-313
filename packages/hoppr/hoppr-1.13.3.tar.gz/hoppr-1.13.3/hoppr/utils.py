"""Hoppr utility functions."""

from __future__ import annotations

import functools
import importlib
import inspect
import os
import sys

from collections.abc import Hashable, Iterable
from importlib.metadata import entry_points
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import psutil

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from packageurl import PackageURL
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError as YAMLParserError
from ruamel.yaml.scanner import ScannerError as YAMLScannerError
from securesystemslib.storage import FilesystemBackend

from hoppr.exceptions import HopprError, HopprLoadDataError, HopprPluginError

if TYPE_CHECKING:
    from types import ModuleType

    from hoppr.base_plugins.hoppr import HopprPlugin
    from hoppr.models import HopprContext

# Highest known Fermat prime (https://en.wikipedia.org/wiki/65,537)
RSA_PUBLIC_EXPONENT = 65537

# Recommended RSA key sizes:
# https://en.wikipedia.org/wiki/Key_size#Asymmetric_algorithm_key_lengths
# Based on the above, RSA keys of size 3072 bits are expected to provide
# security through 2031 and beyond.
RSA_KEY_BITS = 3072


def _class_in_module(plugin_module: ModuleType) -> type[HopprPlugin]:
    """Find the appropriate class in given module.

    Args:
        plugin_module (ModuleType): Previously loaded module to search for specified plugin class

    Raises:
        HopprPluginError: No class definition or more than one class definition found in module

    Returns:
        Type[HopprPlugin]: Class type of plugin
    """
    # Prevent circular import
    base_cls = importlib.import_module(name="hoppr.base_plugins.hoppr").HopprPlugin

    def is_hoppr_plugin(obj: ModuleType) -> bool:
        return (
            inspect.isclass(obj)
            and issubclass(obj, base_cls)
            and obj.__module__ == plugin_module.__name__
        )  # fmt: skip

    # Get classes defined in plugin_module
    module_classes = dict(inspect.getmembers(object=plugin_module, predicate=is_hoppr_plugin))

    match list(module_classes.keys()):
        case []:
            raise HopprPluginError(f"No class definition found in '{plugin_module.__name__}'.")
        case [multiple_cls, *extra] if extra:
            cls_names = ", ".join(f"'{cls_name}'" for cls_name in [multiple_cls, *extra])
            raise HopprPluginError(f"Multiple candidate classes defined in '{plugin_module.__name__}': {cls_names}")

    return next(iter(module_classes.values()))


def plugin_class(plugin_name: str) -> type[HopprPlugin]:
    """Get plugin class type from module path or class name.

    If the plugin name references a module, it is assumed the module defines
    exactly one subclass of `HopprPlugin`, which will be instantiated using
    a default constructor (i.e., one with no parameters).

    Args:
        plugin_name (str): Name of the plugin module or class defined in transfer file

    Raises:
        ModuleNotFoundError: Import of specified module failed
        HopprPluginError: No class definition or more than one class definition found in module

    Returns:
        Type[HopprPlugin]: Class type of plugin
    """
    discovered_plugins = entry_points(group="hoppr.plugin")

    try:
        if found_plugin := [
            *discovered_plugins.select(name=plugin_name),
            *discovered_plugins.select(module=plugin_name),
            *discovered_plugins.select(attr=plugin_name),
        ]:
            match found_plugin:
                case [found_one]:
                    loaded = found_one.load()

                    # Return directly if provided plugin name was loaded as a plugin class
                    # Otherwise, search the loaded plugin module for appropriate class
                    return loaded if inspect.isclass(loaded) else _class_in_module(loaded)
                case [found_multiple, *extra]:
                    matches = ", ".join(f"'{found.name}'" for found in [found_multiple, *extra])
                    raise HopprPluginError(f"Multiple entry points matched '{plugin_name}': {matches}")

        # Provided plugin name not found in entry points
        # Attempt to load using fully qualified module path
        loaded = importlib.import_module(name=plugin_name)
        return _class_in_module(loaded)
    except ModuleNotFoundError as mnfe:
        raise ModuleNotFoundError(f"Unable to locate plug-in '{plugin_name}': {mnfe}") from mnfe
    except HopprPluginError as ex:
        raise ex


def plugin_instance(plugin_name: str, context: HopprContext, config: dict | None = None) -> HopprPlugin:
    """Create an instance of an object defined by a plugin name.

    Assumes the specified plugin will define exactly one concrete class, which
    will be instaniated using a default constructor (i.e., one with no parameters).
    """
    plugin_cls = plugin_class(plugin_name)

    instance = plugin_cls(context=context, config=dict(config or {}))

    # If `instance.supported_purl_types` is empty, all PURL types are supported
    if not instance.supported_purl_types:
        purl_types = importlib.import_module("hoppr.models.types").PurlType
        instance.supported_purl_types = [str(purl_type) for purl_type in purl_types]

    return instance


def load_string(contents: str) -> dict | list | None:
    """Return a YAML or JSON formatted string as a dict."""
    if not contents.strip():
        raise HopprLoadDataError("Empty string cannot be parsed.")

    # Replace tab characters with spaces to prevent parsing errors
    contents = contents.replace("\t", "  ")
    loaded_contents: dict | list | None = None

    try:
        # Applicable to both YAML and JSON formats since valid JSON data is also valid YAML
        yaml = YAML(typ="safe", pure=True)
        loaded_contents = yaml.load(contents)

        # yaml.safe_load will sometimes return a single string rather than the required structure
        if isinstance(loaded_contents, str):
            raise HopprLoadDataError("Expected dictionary or list, but contents were loaded and returned as string")
    except (YAMLParserError, YAMLScannerError) as ex:
        raise HopprLoadDataError("Unable to recognize data as either json or yaml") from ex
    except HopprLoadDataError as ex:
        raise ex

    return loaded_contents


def load_file(input_file_path: Path) -> dict | list | None:
    """Load file content (either JSON or YAML) into a dict."""
    if not input_file_path.is_file():
        raise HopprLoadDataError(f"{input_file_path} is not a file, cannot be opened.")

    with input_file_path.open(mode="r", encoding="utf-8") as input_file:
        content: str = input_file.read()
        if not content.strip():
            raise HopprLoadDataError(f"File {input_file_path} is empty.")

    return load_string(content)


DedupT = TypeVar("DedupT", bound=Hashable)


def dedup_list(list_in: Iterable[DedupT]) -> list[DedupT]:
    """De-duplicate a list."""
    return list(dict.fromkeys(list_in or []))


def obscure_passwords(command_list: list[str], sensitive_args: list[str] | None = None) -> str:
    """Returns an input string with any specified passwords hidden."""
    password_list: list[str] = sensitive_args if sensitive_args is not None else []
    obscured_command_list: list[str] = []

    for arg in command_list:
        # Quote arguments that contain spaces
        if " " in arg:
            arg = f'"{arg}"'

        # Replace password string(s) in argument
        for password in password_list:
            if password is not None and len(password) > 0:
                arg = arg.replace(password, "[masked]")

        obscured_command_list.append(arg)

    return " ".join(obscured_command_list)


def remove_empty(directory: Path) -> set[Path]:
    """Removes empty folders given the directory including parent folders."""
    deleted: set[Path] = set()

    if not directory.exists():
        raise FileNotFoundError()

    for subdir in directory.iterdir():
        if subdir.is_dir():
            deleted.update(remove_empty(subdir))

    if directory.is_dir() and not any(directory.iterdir()):
        directory.rmdir()
        deleted.add(directory)

    return deleted


@functools.cache
def get_package_url(purl_string: str) -> PackageURL:
    """Get the PackageURL for a given purl_string and store it in a cache for improved performance.

    Args:
        purl_string (str): The string representation of a Package URL

    Returns:
        PackageURL: The object representation of a PackageURL

    """
    return PackageURL.from_string(purl_string)


def get_partition(directory: os.PathLike) -> psutil._common.sdiskpart:
    """Returns partition information for a file location."""
    mount = Path(directory).expanduser().resolve()
    while not mount.is_mount():
        mount = mount.parent

    try:
        return next(part for part in psutil.disk_partitions(all=True) if part.mountpoint == str(mount))
    except StopIteration as ex:
        raise HopprError(f"Unable to identify partition for path '{directory}'") from ex


def is_cicd() -> bool:
    """Check if running in CI/CD context."""
    return any(
        os.getenv(env_var, None)
        for env_var in [
            "bamboo.buildKey",
            "BUILD_ID",
            "BUILD_NUMBER",
            "BUILDKITE",
            "CI",
            "CIRCLECI",
            "CIRRUS_CI",
            "CODEBUILD_BUILD_ID",
            "CONTINUOUS_INTEGRATION",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "HEROKU_TEST_RUN_ID",
            "HUDSON_URL",
            "JENKINS_URL",
            "TEAMCITY_VERSION",
            "TF_BUILD",
            "TRAVIS",
        ]
    )


@functools.cache
def is_basic_terminal() -> bool:
    """Check if current terminal supports ANSI multi-byte characters.

    This function is decorated with `functools.cache` so that it always returns the same value after the initial
    invocation. This is to prevent negating the return value once the Rich live display is started, i.e.
    `sys.stdout.isatty()` will then return False instead of True
    """
    return any([
        is_cicd(),
        not sys.stdout.isatty(),
        os.getenv("HOPPR_BASIC_TERM"),
        os.getenv("TERM_PROGRAM") == "Apple_Terminal",
    ])


def rsa_keygen(output_key_prefix: str | os.PathLike[str], password: str | None = None):
    """Generates an RSA key pair.

    Args:
        output_key_prefix: Target path for the private key file. Public key will be the same path,
            but with the ".pub" extension.
        password: Password to use for encryption.
    """
    rsa_private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT, key_size=RSA_KEY_BITS, backend=FilesystemBackend()
    )

    encryption_algorithm = (
        serialization.NoEncryption()
        if password is None
        else serialization.BestAvailableEncryption(password.encode("utf-8"))
    )

    pem = rsa_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption_algorithm,
    )
    pub = rsa_private_key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.PKCS1)

    output_key_prefix = Path(output_key_prefix)
    output_key_prefix.write_bytes(pem)
    output_key_prefix.with_suffix(".pub").write_bytes(pub)
