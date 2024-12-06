"""Collector plugin for git repositories."""

from __future__ import annotations

import re

from pathlib import Path
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

from pydantic import SecretStr

import hoppr
import hoppr.utils

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.models import HopprContext
from hoppr.models.credentials import CredentialRequiredService
from hoppr.models.sbom import Component
from hoppr.models.types import RepositoryUrl
from hoppr.result import Result

if TYPE_CHECKING:
    from pathlib import Path


class CollectGitPlugin(
    SerialCollectorPlugin,
    supported_purl_types=["git", "gitlab", "github"],
    required_commands=["git"],
    products=["git/*", "gitlab/*", "github/*"],
):
    """Class to copy git repositories.

    configuration options:
    config:
      depth: all, 1, or any int > 1
    """

    def get_version(self) -> str:  # noqa: D102
        return __version__

    def __init__(self, context: HopprContext, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)
        self.required_commands = (self.config or {}).get("git_command", self.required_commands)

    @hoppr_rerunner
    def collect(
        self,
        comp: Component,
        repo_url: str,
        creds: CredentialRequiredService | None = None,
    ) -> Result:
        """Collect git repository."""
        purl = hoppr.utils.get_package_url(comp.purl)
        source_url = RepositoryUrl(url=repo_url) / (purl.namespace or "") / purl.name

        self.get_logger().info(msg=f"Cloning {source_url}", indent_level=2)

        # Only reference the namespace.  The actual clone creates the named directory
        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)

        git_result = self.git_clone(
            tmp_dir=target_dir,
            source_url=f"{source_url}",
            source_creds=creds,
            comp=comp,
        )
        if not git_result.is_success():
            return git_result

        git_result = self.git_update(target_dir, purl.name)
        self.cleanup_git_config(target_dir, purl.name)
        if not git_result.is_success():
            return git_result

        self.set_collection_params(comp, repo_url, target_dir / purl.name)

        return Result.success(return_obj=comp)

    def git_clone(
        self,
        tmp_dir: Path,
        source_url: str,
        source_creds: CredentialRequiredService | None,
        comp: Component,
    ) -> Result:
        """Git clone."""
        git_src = source_url
        password_list: list[str] = []

        if re.match("^https?://", git_src) and source_creds is not None:
            git_src = git_src.replace("://", f"://{source_creds.username}@", 1)

            if source_creds.password and isinstance(source_creds.password, SecretStr):
                git_src = git_src.replace("@", f":{source_creds.password.get_secret_value()}@")
                password_list = [source_creds.password.get_secret_value()]

        if git_src.startswith("ssh://") and source_creds is not None:
            git_src = git_src.replace("ssh://", f"ssh://{source_creds.username}@")

        if not git_src.endswith(".git"):
            git_src += ".git"

        opts: list[str] = []

        # Allow for further depth (default: 1)
        depth = hoppr.utils.get_package_url(comp.purl).qualifiers.get("depth") or (self.config or {}).get("depth", "1")

        if comp.version is not None:
            opts = [*opts, f"--branch={comp.version}", "--single-branch"]

        # Recognize the 'all' keyword as requesting all history
        elif str(depth).lower() != "all":
            opts = [*opts, f"--depth={depth}"]

        if self.get_logger().is_verbose():
            opts = [*opts, "--verbose"]

        # Clone with a requested depth and reference the version if specified
        try:
            result = self.run_command([self.required_commands[0], "clone", *opts, git_src], password_list, cwd=tmp_dir)
            result.check_returncode()
        except CalledProcessError:
            return self.log_git_error(f"Failed to clone {source_url}")

        if comp.version:
            # If the component is versioned do a hard reset to that version
            self._logger.info(msg=f"Resetting repo to version {comp.version}")
            try:
                result = self.run_command(
                    [self.required_commands[0], "reset", "--hard", comp.version], password_list, cwd=tmp_dir / comp.name
                )

                result.check_returncode()
            except CalledProcessError:
                return self.log_git_error(f"Failed to reset {source_url} to {comp.version}")

            # Fetch desired depth if depth is not all
            if str(depth) != "all":
                self._logger.info(msg=f"Fetching repo at depth {depth}")
                try:
                    result = self.run_command(
                        [self.required_commands[0], "fetch", "--depth", str(depth)],
                        password_list,
                        cwd=tmp_dir / comp.name,
                    )

                    result.check_returncode()
                except CalledProcessError:
                    return self.log_git_error(f"Failed to set {source_url} to desired depth")

        return Result.success()

    def log_git_error(self, error: str) -> Result:
        """Log an error and return a retry."""
        self.get_logger().debug(msg=error, indent_level=2)
        return Result.retry(message=error)

    def git_update(self, tmp_dir: Path, name_git: str) -> Result:
        """Git update-server-info."""
        repo_dir = tmp_dir / name_git.removesuffix(".git")

        # Make the clone usable as a remote
        result = self.run_command(
            [self.required_commands[0], "update-server-info"],
            cwd=repo_dir,
        )

        if result.returncode != 0:
            msg = "Failed to make the clone usable as a remote"
            self.get_logger().debug(msg=msg, indent_level=2)
            return Result.retry(message=msg)

        return Result.success()

    def cleanup_git_config(self, tmp_dir: Path, name_git: str):
        """Remove credentials from git config url."""
        if not (config_file_path := tmp_dir / name_git.removesuffix(".git") / ".git" / "config").is_file():
            return

        config_data = config_file_path.read_text("utf-8")
        scrubbed_data = re.sub(
            pattern=r"(https?://)([^:/@]+:[^/@]+@)?(.*)",
            repl=r"\1\3",
            string=config_data,
        )
        config_file_path.write_text(scrubbed_data, "utf-8")
