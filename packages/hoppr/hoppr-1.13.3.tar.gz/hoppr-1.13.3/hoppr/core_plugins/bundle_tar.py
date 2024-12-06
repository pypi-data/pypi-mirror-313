"""Plugin to create tar file bundle."""

from __future__ import annotations

import re
import tarfile
import time

from pathlib import Path

from hoppr import __version__
from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_process
from hoppr.result import Result


class TarBundlePlugin(HopprPlugin):
    """Plugin to create tar file bundle.

    This plug-in supports the following config values:

    - compression: Specifies the compression to be applied to the output tar file. Defaults
        to "gz". Recognized values are "none", "gzip", "gz", "bzip2", "bz", "lmza", "xz"
    - tarfile_name: Name of the tar file to be created. Defaults to "bundle.tar.<comp>", where <comp>
        is the short form of the compression used. For "none" compression, default is "bundle.tar"
    """

    def get_version(self) -> str:  # noqa: D102
        return __version__

    @hoppr_process
    def post_stage_process(self) -> Result:
        """Tar-up the context.collect_root_dir directory."""
        compression: str = (self.config or {}).get("compression", "gz").lower()

        match compression:
            case "none":
                compression = ""
            case "gzip" | "gz":
                compression = "gz"
            case "bzip2" | "bz2" | "bz":
                compression = "bz2"
            case "lzma" | "xz":
                compression = "xz"
            case _:
                return Result.fail(f"Unrecognized compression in config: {compression}")

        default_filename = Path.cwd() / f"bundle.tar{f'.{compression}' if compression else ''}"
        tarfile_name = Path((self.config or {}).get("tarfile_name", default_filename)).expanduser()

        if tarfile_name.exists():
            timestr = time.strftime("%Y%m%d-%H%M%S")
            base_name, suffix = filter(None, re.split(pattern=r"^(.*)(\.tar\.?.*)$", string=tarfile_name.name))
            tarfile_name = tarfile_name.with_name(f"{base_name}-{timestr}{suffix}")

        msg = f"Bundling collected artifacts into {tarfile_name}"
        self.get_logger().info(msg)
        self.notify(msg, type(self).__name__)

        try:
            with tarfile.open(tarfile_name, f"x:{compression}") as tar:
                tar.add(self.context.collect_root_dir, ".")
        except tarfile.ReadError as err:
            return Result.fail(f"Unable to create tarfile {tarfile_name}, {err}")
        except FileNotFoundError:
            return Result.fail(f"File {tarfile_name}: Directory not found.")
        except PermissionError:
            return Result.fail(f"File {tarfile_name}: Permission denied.")

        self.context.signable_file_paths.append(tarfile_name)

        return Result.success()
