from collections.abc import Callable, MutableMapping
from itertools import count
from logging import Logger, LoggerAdapter
from threading import _RLock as RLock

from typing_extensions import override

def locked(func: Callable) -> Callable: ...

class HopprLogger(LoggerAdapter):
    id_iter: count[int]
    extra: MutableMapping[str, object]
    logger: Logger
    filename: str
    flush_immed: bool
    instance_id: int
    lock: RLock | None
    def __init__(
        self,
        name: str | None = ...,
        filename: str = ...,
        level: int = ...,
        lock: RLock | None = ...,
        flush_immed: bool = ...,
    ) -> None: ...
    def clear_targets(self) -> None: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def is_verbose(self) -> bool: ...
    @override
    def log(  # type: ignore[override]
        self,
        level: int,
        msg: object,
        *args: object,
        indent_level: int = 0,
        **kwargs: object,
    ) -> None: ...
    def process(
        self, msg: str, kwargs: MutableMapping[str, object]
    ) -> tuple[str, MutableMapping[str, object]]: ...
    @override
    def debug(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        ...
    @override
    def info(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        ...
    @override
    def warning(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        ...
    @override
    def error(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        ...
    @override
    def critical(self, msg: str, *args, indent_level: int = 0, **kwargs) -> None:  # type: ignore[override]
        ...
