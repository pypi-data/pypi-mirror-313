"""Base class for all Hoppr plug-ins."""

from __future__ import annotations

import functools
import subprocess as subprocess
import time
import traceback

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar

import hoppr.plugin_utils
import hoppr.utils

from hoppr.logger import HopprLogger
from hoppr.models.transfer import ComponentCoverage
from hoppr.models.types import BomAccess
from hoppr.result import Result

if TYPE_CHECKING:
    from collections.abc import Callable
    from os import PathLike

    from hoppr.models import HopprContext
    from hoppr.models.sbom import Component


def _get_component(*args, **kwargs) -> Component | None:
    # TODO: This will only utilize the first Component found in 1) args, 2) kwargs
    # and assumes all plugins operate this way
    all_args = [*args, *kwargs.values()]

    return next((arg for arg in all_args if type(arg).__name__ == "Component"), None)


def hoppr_process(func: Callable) -> Callable:
    """Decorator to handle generic bookkeeping for hoppr plug-ins."""

    @functools.wraps(func)
    def wrapper(self: HopprPlugin, *args, **kwargs) -> Result:
        self._start_time = time.time()

        comp = _get_component(*args, **kwargs)

        arg_string = ""
        if comp is not None:
            arg_string = f"(purl: {comp.purl})"

        self.get_logger().debug(f"Starting {self.__class__.__name__}.{func.__name__} {arg_string}")

        result = None
        if comp is not None:
            if comp.purl is None:
                result = Result.fail("No purl supplied for component")

            else:
                purl_type = hoppr.utils.get_package_url(comp.purl).type

                if not self.supports_purl_type(purl_type):
                    return Result.skip(f"Class {self.__class__.__name__} does not support purl type {purl_type}")

                component_header = f"{comp.name}" + (f"@{comp.version}" if comp.version is not None else "")

                self.get_logger().info(
                    msg=f"{'-' * 4} Component: {component_header} {'-' * 50}",
                )

        if result is None:
            # Only check for missing commands if func has been overridden
            if func.__module__ != HopprPlugin.__module__:
                command_result = hoppr.plugin_utils.check_for_missing_commands(self.required_commands)
                if command_result.is_fail():
                    self.get_logger().error(command_result.message)
                    return command_result

            try:
                result = func(self, *args, **kwargs)
            except Exception as error:
                self.get_logger().error(
                    f"Unexpected exception running {self.__class__.__name__}.{func.__name__}: {error}",
                )
                self.get_logger().error(traceback.format_exc())
                result = Result.fail(f"Unexpected Exception: {error}")

        self.get_logger().debug(f"Completed {self.__class__.__name__}.{func.__name__}")

        duration = time.time() - self._start_time
        self.get_logger().debug(f"Process duration {duration:3f} seconds")
        self.get_logger().info(f"Result: '{result}'")

        if result.is_skip():
            self.get_logger().clear_targets()

        self.close_logger()

        return result

    return wrapper


def hoppr_rerunner(method: Callable) -> Callable:
    """Runs a method (assumed to return a Result object) a number of times, or until the result type is not RETRY."""

    @functools.wraps(method)
    def wrapper(self: HopprPlugin, *args, **kwargs) -> Result:
        log = self.get_logger()

        result = Result.fail(message="Context max_attempts must be a positive integer.")

        for attempt in range(self.context.max_attempts):
            log.info(msg=f"Processing component [attempt {attempt + 1} of {self.context.max_attempts}]", indent_level=1)

            result = method(self, *args, **kwargs)

            if not isinstance(result, Result):
                msg = f"Method {method.__name__} returned {type(result).__name__} in rerunner. Result object required"

                log.error(msg=msg, indent_level=1)
                return Result.fail(message=msg)

            if not result.is_retry():
                return result

            if attempt < self.context.max_attempts - 1:
                log.warning(
                    msg=(f"Method {method.__name__} will be retried in {self.context.retry_wait_seconds} seconds"),
                    indent_level=1,
                )

                log.warning(msg=f"Result message for attempt {attempt + 1}: {result.message}", indent_level=1)

                time.sleep(self.context.retry_wait_seconds)

        log.error(msg=f"Method {method.__name__} failed after {self.context.max_attempts} attempts")
        log.error(msg=f"Result message for final attempt: {result.message}")

        return Result.fail(f"Failure after {self.context.max_attempts} attempts, final message {result.message}")

    return wrapper


def hoppr_ignore_excluded(func: Callable) -> Callable:
    """Decorator to ignore components which have a scope of `excluded`."""

    @functools.wraps(func)
    def wrapper(self: HopprPlugin, *args, **kwargs) -> Result:
        comp = _get_component(*args, **kwargs)
        if comp is not None and str(comp.scope) in {
            "excluded",
            "Scope.excluded",
        }:
            return Result.excluded()
        return func(self, *args, **kwargs)

    return wrapper


class HopprPlugin(ABC):
    """Base class for all Hoppr plug-ins."""

    required_commands: list[str]
    supported_purl_types: list[str]

    """
    Product: the result of carrying out a step. Products are usually persistent (e.g,.
    files), and are often meant to be used as materials on subsequent steps. Products are
    recorded as part of link metadata.

    This is a list of strings where each element is a relative path file or wildcard.

    See in-toto specification:
    - https://github.com/in-toto/docs/blob/master/in-toto-spec.md
    """
    products: list[str]

    default_component_coverage = ComponentCoverage.OPTIONAL
    bom_access = BomAccess.NO_ACCESS
    process_timeout = 60

    observers: ClassVar[dict[object, Callable]] = {}

    def __init__(
        self,
        context: HopprContext,
        config: dict | None = None,
    ) -> None:
        self._start_time: float = 0.0
        self.config = config
        self.context = context

        self._logger = HopprLogger(
            filename=str(self.context.logfile_location),
            level=self.context.log_level,
            lock=self.context.logfile_lock,
        )

        self.process_timeout = (self.config or {}).get("process_timeout", self.process_timeout)

    def __init_subclass__(
        cls,
        products: list[str] | None = None,
        required_commands: list[str] | None = None,
        supported_purl_types: list[str] | None = None,
        bom_access: BomAccess | str | None = None,
        process_timeout: int | None = None,
        default_component_coverage: ComponentCoverage | str | None = None,
    ) -> None:
        super().__init_subclass__()

        cls.products = products or getattr(cls, "products", [])
        cls.required_commands = required_commands or getattr(cls, "required_commands", [])
        cls.supported_purl_types = supported_purl_types or getattr(cls, "supported_purl_types", [])
        cls.bom_access = BomAccess(bom_access) if bom_access else cls.bom_access
        cls.process_timeout = process_timeout or cls.process_timeout
        cls.default_component_coverage = (
            ComponentCoverage[str(default_component_coverage)]
            if default_component_coverage
            else cls.default_component_coverage
        )

    @abstractmethod
    def get_version(self) -> str:
        """Returns the version of this plug-in."""

    def notify(self, *args, **kwargs) -> None:
        """Call the callback function for all registered subscribers."""
        for callback in self.observers.values():
            callback(*args, **kwargs)

    def subscribe(self, observer: object, callback: Callable) -> None:
        """Register an observer."""
        self.observers[observer] = callback

    def unsubscribe(self, observer: object) -> None:
        """Unregister an observer."""
        self.observers.pop(observer, None)

    @hoppr_process
    @hoppr_rerunner
    def pre_stage_process(self) -> Result:
        """Process to be run before other processing within a stage for this plug-in."""
        return Result.skip("pre_stage_process not defined.")

    @hoppr_process
    @hoppr_rerunner
    def process_component(self, comp: Component) -> Result:
        """Process a single component through this plug-in."""
        return Result.skip("process_component not defined.")

    @hoppr_process
    @hoppr_rerunner
    def post_stage_process(self) -> Result:
        """Finalize processing for this plug-in."""
        return Result.skip("post_stage_process not defined.")

    def supports_purl_type(self, purl_type: str) -> bool:
        """Indicates whether or not this particular plug-in supports components of the specified purl type.

        If no supported purl types are defined, the plug-in supports all purl types.
        """
        return purl_type in self.supported_purl_types or not self.supported_purl_types

    @classmethod
    def get_attestation_products(cls, config: dict | None = None) -> list[str]:
        """Return a list of attestation products for this class."""
        return cls.products

    def get_logger(self) -> HopprLogger:
        """Returns the logger to be used for the current process."""
        return self._logger

    def close_logger(self) -> None:
        """Close (and flush) all handlers for this plug-in's logger."""
        self._logger.close()

    def run_command(
        self, command: list[str], password_list: list[str] | None = None, cwd: str | PathLike[str] | None = None
    ) -> subprocess.CompletedProcess[bytes]:
        """Run a command and log any errors."""
        obscured_command = hoppr.utils.obscure_passwords(command, password_list)
        self.get_logger().debug(msg=f"Running command: '{obscured_command}'", indent_level=2)

        try:
            result = subprocess.run(
                command, check=False, shell=False, capture_output=True, cwd=cwd, timeout=self.process_timeout
            )
        except subprocess.TimeoutExpired as timeout_expired:
            self.get_logger().error(
                'Command "%s" timed out after %d seconds', command[0], timeout_expired.timeout, indent_level=2
            )
            result = subprocess.CompletedProcess(
                command, returncode=124, stdout=timeout_expired.stdout or b"", stderr=timeout_expired.stderr or b""
            )

        if result.returncode != 0:
            # Prefix each line of the command's stdout and stderr with 4 spaces
            stdout_indented, stderr_indented = (
                "\n".join([f"    {line}" for line in output.decode("utf-8").split("\n")])
                for output in [result.stdout, result.stderr]
            )

            self.get_logger().debug(msg=f"{command[0]} command stdout content:\n{stdout_indented}", indent_level=2)
            self.get_logger().error(msg=f"{command[0]} command failed with error:\n{stderr_indented}", indent_level=2)

        return result
