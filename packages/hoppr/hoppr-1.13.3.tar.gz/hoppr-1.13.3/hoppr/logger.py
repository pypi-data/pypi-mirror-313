"""A logger that gets dumped to stdout when closed."""

from __future__ import annotations

import functools
import inspect
import itertools
import logging

from collections.abc import Callable, MutableMapping
from logging import FileHandler, Formatter, Logger, LoggerAdapter
from logging.handlers import MemoryHandler
from typing import TYPE_CHECKING, cast

from typing_extensions import override

if TYPE_CHECKING:
    from threading import _RLock as RLock


def locked(func: Callable) -> Callable:
    """Acquire logfile lock, run the wrapped function, then release the lock."""

    @functools.wraps(func)
    def wrapper(self: HopprLogger, *args, **kwargs):
        if self.lock:
            self.lock.acquire()

        func(self, *args, **kwargs)

        if self.lock:
            self.lock.release()

    return wrapper


class HopprLogger(LoggerAdapter):
    """Logger that buffers log records in memory until flushed."""

    id_iter = itertools.count()

    def __init__(
        self,
        name: str | None = None,
        filename: str = "hoppr.log",
        level: int = logging.INFO,
        lock: RLock | None = None,
        flush_immed: bool = False,
    ) -> None:
        """Initialize the logger, formatter, and handlers.

        Args:
            name (str | None, optional): Name to assign the logger. Defaults to None.
            filename (str, optional): Log file to create. Defaults to "hoppr.log".
            level (int, optional): Logging level. Defaults to logging.INFO.
            lock (RLock | None, optional): Lock object to acquire/release when writing to log file. Defaults to None.
            flush_immed (bool, optional): Flush immediately when logging. Defaults to False.
        """
        self.extra: MutableMapping[str, object]
        self.logger: Logger

        self.filename = filename
        self.flush_immed: bool = flush_immed
        self.instance_id: int = next(self.id_iter)
        self.lock: RLock | None = lock

        _, frame_info, *_ = inspect.stack(context=2)
        caller = frame_info.function

        if (caller_cls := frame_info.frame.f_locals.get("self")) is not None:
            caller = type(caller_cls).__name__

        extra = cast(MutableMapping, {})
        extra["caller"] = name or caller

        logger = logging.getLogger(f"{name}-{self.instance_id}" if name else f"{caller}-{self.instance_id}")
        logger.setLevel(level)

        formatter = Formatter(
            fmt="[$asctime] - [${caller}] - [$levelname] - $message",
            style="$",
            defaults={"caller": caller},
        )

        file_handler = FileHandler(filename)
        file_handler.setFormatter(formatter)

        log_handler = MemoryHandler(10000, flushLevel=logging.CRITICAL, target=file_handler)
        logger.addHandler(log_handler)

        super().__init__(logger, extra)

    def clear_targets(self) -> None:
        """Set target for all MemoryHandlers in this logger to None.

        Thus when these handlers are flushed, nothing will go to standard output
        """
        for handler in self.logger.handlers:
            if isinstance(handler, MemoryHandler):
                handler.setTarget(None)

    @locked
    def close(self) -> None:
        """Close (and flush) all handlers for this logger."""
        for handler in self.logger.handlers:
            handler.close()

    @locked
    def flush(self) -> None:
        """Flush all handlers for this logger."""
        for handler in self.logger.handlers:
            handler.flush()

    def is_verbose(self) -> bool:
        """Check whether running with `--debug`/`--verbose` flag."""
        return self.logger.level == logging.DEBUG

    def log(self, level: int, msg: object, *args, **kwargs) -> None:
        """Wrapper function for logging messages."""
        super().log(level, msg, *args, **kwargs)

        if self.flush_immed:
            self.flush()

    @override
    def process(self, msg: str, kwargs: MutableMapping[str, object]) -> tuple[str, MutableMapping[str, object]]:
        indent_level = cast(int, kwargs.pop("indent_level", 0))
        indent_string = " " * 4 * indent_level
        msg = f"{indent_string}{msg}"

        return super().process(msg, kwargs)
