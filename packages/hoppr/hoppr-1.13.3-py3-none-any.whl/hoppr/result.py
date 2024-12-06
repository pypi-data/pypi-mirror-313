"""Class to store results of processes."""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from typing_extensions import Self

from hoppr.exceptions import HopprError
from hoppr.models.sbom import Component, Sbom

if TYPE_CHECKING:
    import requests


class ResultStatus(IntEnum):
    """Enumeration of possible result states."""

    EXCLUDED = 0
    SUCCESS = 1
    RETRY = 2
    WARN = 3
    FAIL = 4
    SKIP = 5

    def __str__(self) -> str:
        return self.name


class Result:
    """Class to store results of processes."""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Result) and all([
            self.status == other.status,
            self.message == other.message,
            self.return_obj == other.return_obj,
        ])

    def __init__(self, status: ResultStatus, message: str = "", return_obj: Component | Sbom | None = None):
        self.status = status
        self.message = message
        self.return_obj = return_obj

    def __str__(self) -> str:
        result_msg = f"{self.status.name}"
        if self.message != "":
            result_msg += f", msg: {self.message}"

        return result_msg.rstrip()

    @classmethod
    def success(cls, message: str = "", return_obj: Component | Sbom | None = None) -> Self:
        """Convenience method for generating success messages."""
        return cls(ResultStatus.SUCCESS, message, return_obj)

    @classmethod
    def retry(cls, message: str = "", return_obj: Component | Sbom | None = None) -> Self:
        """Convenience method for generating retry messages."""
        return cls(ResultStatus.RETRY, message, return_obj)

    @classmethod
    def fail(cls, message: str = "", return_obj: Component | Sbom | None = None) -> Self:
        """Convenience method for generating failure messages."""
        return cls(ResultStatus.FAIL, message, return_obj)

    @classmethod
    def warn(cls, message: str = "", return_obj: Component | Sbom | None = None) -> Self:
        """Convenience method for generating warning messages."""
        return cls(ResultStatus.WARN, message, return_obj)

    @classmethod
    def excluded(cls, message: str = "", return_obj: Component | Sbom | None = None) -> Self:
        """Convenience method for generating excluded messages."""
        return cls(ResultStatus.EXCLUDED, message, return_obj)

    @classmethod
    def skip(cls, message: str = "", return_obj: Component | Sbom | None = None) -> Self:
        """Convenience method for generating skip messages."""
        return cls(ResultStatus.SKIP, message, return_obj)

    def is_success(self) -> bool:
        """Convenience method for testing for success messages."""
        return self.status == ResultStatus.SUCCESS

    def is_retry(self) -> bool:
        """Convenience method for testing for retry messages."""
        return self.status == ResultStatus.RETRY

    def is_fail(self) -> bool:
        """Convenience method for testing for failure messages."""
        return self.status == ResultStatus.FAIL

    def is_warn(self) -> bool:
        """Convenience method for testing for warning messages."""
        return self.status == ResultStatus.WARN

    def is_excluded(self) -> bool:
        """Convenience method for testing for excluded messages."""
        return self.status == ResultStatus.EXCLUDED

    def is_skip(self) -> bool:
        """Convenience method for testing for skip messages."""
        return self.status == ResultStatus.SKIP

    def merge(self, other: Result):
        """Logically combine two Result objects."""
        if other.is_skip():
            return

        self.status = max(self.status, other.status)
        self.message = "\n".join(filter(None, [self.message, other.message]))

        if self.return_obj and other.return_obj:
            raise HopprError("Unable to merge two results with return objects")

        self.return_obj = next((obj for obj in [self.return_obj, other.return_obj] if obj), None)

    @staticmethod
    def from_http_response(response: requests.Response, return_obj: Component | Sbom | None = None) -> Result:
        """Build a Result object from an HTTP request response."""
        match response.status_code:
            case response_code if 200 <= response_code <= 299:
                return Result.success(
                    f"HTTP Status Code: {response.status_code}",
                    return_obj=return_obj,
                )
            case response_code if response_code >= 500:
                status = ResultStatus.RETRY
            case _:
                status = ResultStatus.FAIL

        message = f"HTTP Status Code: {response.status_code}; {response.reason or response.text}"
        return Result(status, message, return_obj=return_obj)
