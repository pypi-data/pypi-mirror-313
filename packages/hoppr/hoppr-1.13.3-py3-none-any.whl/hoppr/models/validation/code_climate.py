"""Models to describe a Code Climate issue report."""

from __future__ import annotations

import hashlib

from enum import Enum
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, Annotated, Any, Literal

from pydantic import Field, validator

from hoppr.models.base import HopprBaseModel

if TYPE_CHECKING:
    from collections.abc import Iterable

    from rich.repr import RichReprResult


def _normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


class IssueCategory(str, Enum):
    """Category indicating the nature of the issue being reported."""

    BUG_RISK = "Bug Risk"
    CLARITY = "Clarity"
    COMPATIBILITY = "Compatibility"
    COMPLEXITY = "Complexity"
    DUPLICATION = "Duplication"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    STYLE = "Style"


class IssueSeverity(str, Enum):
    """Severity of the issue."""

    INFO = "info"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"
    BLOCKER = "blocker"


class IssueContent(HopprBaseModel):
    """A markdown snippet describing the issue, including deeper explanations and links to other resources."""

    body: Annotated[str | None, Field(description="Body of the snippet, formatted as markdown.")]


class LineRange(HopprBaseModel):
    """Beginning and end line number to define a range of lines."""

    begin: int
    end: int


class PositionReference(HopprBaseModel):
    """Reference to the a specific character position in a file."""

    line: int
    column: int


class PositionRange(HopprBaseModel):
    """Beginning and end position to define a range of characters."""

    begin: PositionReference
    end: PositionReference


class IssueLocationLineRange(HopprBaseModel):
    """Line-based locations.

    Specify a beginning and end line number for the issue location, which form a range.
    Line numbers are 1-based, so the first line of a file would be represented by 1.
    """

    path: Annotated[Path, Field(description="File path relative to working directory.")]
    lines: LineRange

    _validate_path = validator("path", always=True, allow_reuse=True)(_normalize_path)


class IssueLocationPositionRange(HopprBaseModel):
    """Position-based location.

    Allows more precision by including references to the specific characters
    that form the source code range representing the issue.
    """

    path: Annotated[Path, Field(description="File path relative to working directory.")]
    positions: PositionRange

    _validate_path = validator("path", always=True, allow_reuse=True)(_normalize_path)


IssueLocation = IssueLocationLineRange | IssueLocationPositionRange


class IssueTrace(HopprBaseModel):
    """Represents ordered or unordered lists of source code locations."""

    locations: list[IssueLocation]
    trace: bool = False


class Issue(HopprBaseModel):
    """Represents a single instance of a validation check finding."""

    type: Annotated[Literal["issue"], Field(description='Must always be "issue".')] = "issue"
    check_name: Annotated[
        str | None,
        Field(description="A unique name representing the static analysis check that emitted this issue."),
    ] = None
    description: Annotated[str, Field(description="A string explaining the issue that was detected.")]
    content: Annotated[
        str | None,
        Field(
            description=(
                "A markdown snippet describing the issue, including deeper explanations and links to other resources."
            ),
        ),
    ] = None
    categories: Annotated[
        list[IssueCategory] | None,
        Field(description="At least one category indicating the nature of the issue being reported."),
    ] = None
    location: Annotated[
        IssueLocation,
        Field(
            description="A `Location` object representing the place in the source code where the issue was discovered."
        ),
    ]
    other_locations: list[IssueLocation] | None = None
    trace: Annotated[
        IssueTrace | None,
        Field(
            description="A `Trace` object representing other interesting source code locations related to this issue."
        ),
    ] = None
    remediation_points: Annotated[
        int | None,
        Field(
            description=(
                "An integer indicating a rough estimate of how long it would take to resolve the reported issue."
            )
        ),
    ] = None
    severity: Annotated[
        IssueSeverity,
        Field(
            description=(
                "A `Severity` string (`info`, `minor`, `major`, `critical`, or `blocker`) "
                "describing the potential impact of the issue found."
            ),
        ),
    ]
    fingerprint: Annotated[
        str,
        Field(
            description=(
                "A unique, deterministic identifier for the specific issue being "
                "reported to allow a user to exclude it from future analyses."
            ),
            regex="[a-z0-9]{13,64}",
        ),
    ] = None  # type: ignore[assignment]

    @validator("fingerprint", allow_reuse=True, pre=True, always=True)
    @classmethod
    def _validate_fingerprint(cls, fingerprint: str | None, values: dict[str, Any]) -> str:
        if fingerprint:
            return fingerprint

        hash_ = hashlib.shake_256(str(values).encode(encoding="utf-8"))
        return hash_.hexdigest(8)

    def __hash__(self) -> int:
        return int.from_bytes(self.fingerprint.encode(encoding="utf-8"), byteorder="big")


class IssueList(HopprBaseModel):
    """List of Issue objects."""

    __root__: list[Issue]

    def __getitem__(self, idx: int) -> Issue:
        return self.__root__[idx]

    def __init__(self, issues: Iterable[Issue] | None = None, **data):
        data["__root__"] = data.get("__root__", list(issues or []))
        super().__init__(**data)

    def __iter__(self):
        yield from self.__root__

    def __len__(self) -> int:
        return len(self.__root__)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__root__})"

    def __rich_repr__(self) -> RichReprResult:
        yield self.__root__

    def append(self, item: Issue) -> None:
        """Append object to the end of the list."""
        self.__root__.append(item)  # pragma: no cover

    def extend(self, iterable: Iterable[Issue]) -> None:
        """Extend list by appending elements from the iterable."""
        self.__root__.extend(iterable)  # pragma: no cover


IssueLocationPositionRange.update_forward_refs()
