"""JSON file parser to generate mappings of object locations for use in Code Climate issue report."""

from __future__ import annotations

import json
import re

from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from typing_extensions import Self, overload

from hoppr.exceptions import HopprLoadDataError
from hoppr.models.base import CycloneDXBaseModel
from hoppr.models.validation.code_climate import (
    IssueLocationPositionRange,
    PositionRange,
    PositionReference,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from os import PathLike


__all__ = ["JSONLocationMapper"]


class JSONElementName(str, Enum):
    """Names for elements in a JSON document."""

    # Structural characters
    BEGIN_ARRAY = "["
    BEGIN_OBJECT = "{"
    END_ARRAY = "]"
    END_OBJECT = "}"
    NAME_SEPARATOR = ":"
    VALUE_SEPARATOR = ","

    # Literal names
    TRUE = "true"
    FALSE = "false"
    NULL = "null"

    # Types
    NUMBER = "NUMBER"
    STRING = "STRING"
    ARRAY = "ARRAY"
    OBJECT = "OBJECT"

    # Higher-Level
    MEMBER = "MEMBER"
    VALUE = "VALUE"

    # Whitespace
    HORIZONTAL_WHITESPACE = "H_WS"
    VERTICAL_WHITESPACE = "V_WS"

    # Special
    END_OF_FILE = "EOF"
    ERROR = "ERROR"


@dataclass
class JSONElement:
    """Represents a JSON element."""

    name: JSONElementName
    start_position: int
    end_position: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    children: list[JSONElement] = field(default_factory=list)


class JSONLexer:
    """Performs lexical tokenization on JSON strings."""

    TOKEN_REGEX_NAME_PAIRS: Final[list[tuple[re.Pattern, JSONElementName | None]]] = [
        (re.compile(r"([\[\]{},:])"), None),  # Structural tokens
        (re.compile(r"\b(true|false|null)\b"), None),  # Literal name tokens
        (
            re.compile(r'(?:"(?:\\(?:["\\\/bfnrt]|u[a-fA-F0-9]{4})|[^"\\\0-\x1F\x7F]+)*")'),
            JSONElementName.STRING,
        ),
        (
            re.compile(r"((?:-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?))"),
            JSONElementName.NUMBER,
        ),
        (
            re.compile(r"([^\S\r\n]+)", flags=re.M),
            JSONElementName.HORIZONTAL_WHITESPACE,
        ),
        (re.compile(r"(\r\n|\r|\n)", flags=re.M), JSONElementName.VERTICAL_WHITESPACE),
    ]

    def __init__(self):
        self.position = 0
        self.line_position = 0
        self.line_number = 1

    def _get_next_token(self, reader: StringIO, line: str) -> JSONElement:
        for regex, token_name in self.TOKEN_REGEX_NAME_PAIRS:
            if matched := regex.match(line):
                end_position = self.position + len(matched[0])

                return JSONElement(
                    token_name or JSONElementName(str(matched[1])),
                    self.position,
                    end_position,
                    start_line=self.line_number,
                    start_column=1 + self.position - self.line_position,
                    end_line=self.line_number,
                    end_column=end_position - self.line_position,
                )

        remaining_text = reader.read()
        eof_position = self.position + len(remaining_text)

        return JSONElement(
            JSONElementName.ERROR,
            self.position + len(remaining_text),
            eof_position,
            start_line=self.line_number,
            start_column=1 + self.position - self.line_position,
            end_line=self.line_number + remaining_text.count("\n") + 1,
            end_column=eof_position - self.position + remaining_text.rfind("\n"),
        )

    def _get_line_tokens(self, reader: StringIO, line: str) -> Iterator[JSONElement]:
        new_token = self._get_next_token(reader, line)

        self.position = new_token.end_position
        reader.seek(self.position)

        if new_token.name == JSONElementName.HORIZONTAL_WHITESPACE:
            return

        if new_token.name == JSONElementName.VERTICAL_WHITESPACE:
            self.line_position = self.position
            self.line_number += 1
            return

        yield new_token

    def get_tokens(self, reader: StringIO) -> Iterator[JSONElement]:
        """Performs lexical tokenization of a JSON document.

        Args:
            reader: Text stream to the JSON document you want to tokenize.

        Yields:
            JSON tokens.
        """
        for line in reader:
            yield from self._get_line_tokens(reader, line)

        yield JSONElement(
            JSONElementName.END_OF_FILE,
            self.position,
            self.position,
            start_line=self.line_number,
            start_column=self.position - self.line_position,
            end_line=self.line_number,
            end_column=self.position - self.line_position,
        )


class JSONParser:
    """Parser for JSON documents."""

    VALUE_ELEMENT_NAMES: Final[list[JSONElementName]] = [
        JSONElementName.OBJECT,
        JSONElementName.ARRAY,
        JSONElementName.NUMBER,
        JSONElementName.STRING,
        JSONElementName.TRUE,
        JSONElementName.FALSE,
        JSONElementName.NULL,
    ]

    ALLOWED_AT_ROOT: Final[list[JSONElementName]] = [
        JSONElementName.BEGIN_ARRAY,
        JSONElementName.BEGIN_OBJECT,
        *VALUE_ELEMENT_NAMES,
    ]

    ERROR_MESSAGE: Final[str] = "Invalid JSON document provided."

    def __init__(self):
        self._parse_stack = deque[JSONElement]()

    def _shift(self, token: JSONElement):
        self._parse_stack.append(token)

    def _reduce(
        self,
        production_name: JSONElementName,
        handle_start_name: JSONElementName | None = None,
    ):
        handle: list[JSONElement] = []
        while element := self._parse_stack.pop():
            if not handle_start_name:
                handle_start_name = element.name

            handle = [element, *handle]

            if element.name == handle_start_name:
                self._parse_stack.append(
                    JSONElement(
                        production_name,
                        handle[0].start_position,
                        handle[-1].end_position,
                        handle[0].start_line,
                        handle[0].start_column,
                        handle[-1].end_line,
                        handle[-1].end_column,
                        children=handle,
                    )
                )

                return

    def _reduce_if_member(self):
        if len(self._parse_stack) > 1 and self._parse_stack[-2].name == JSONElementName.NAME_SEPARATOR:
            self._reduce(JSONElementName.MEMBER, JSONElementName.STRING)

    def _handle_token(self, token: JSONElement) -> JSONElement | None:
        parsed: JSONElement | None = None

        match (self._parse_stack, token):
            # ----- Root Values -----
            case [[], token] if token.name in self.ALLOWED_AT_ROOT:
                self._shift(token)

                if token.name in self.VALUE_ELEMENT_NAMES:
                    self._reduce(JSONElementName.VALUE)

            # ----- Property Values, Array Values, and Members -----
            case [
                [
                    *_,
                    JSONElement(name=JSONElementName.MEMBER),
                    JSONElement(name=JSONElementName.VALUE_SEPARATOR),
                ],
                JSONElement(name=JSONElementName.STRING),
            ]:
                self._shift(token)

            case [
                [
                    *_,
                    JSONElement(name=JSONElementName.NAME_SEPARATOR | JSONElementName.BEGIN_ARRAY),
                ]
                | [
                    *_,
                    JSONElement(name=JSONElementName.VALUE),
                    JSONElement(name=JSONElementName.VALUE_SEPARATOR),
                ],
                token,
            ] if token.name in self.ALLOWED_AT_ROOT:
                self._shift(token)

                if token.name in self.VALUE_ELEMENT_NAMES:
                    self._reduce(JSONElementName.VALUE)
                    self._reduce_if_member()

            # ----- Property Names -----
            case [
                [*_, JSONElement(name=JSONElementName.BEGIN_OBJECT)]
                | [
                    *_,
                    JSONElement(name=JSONElementName.VALUE),
                    JSONElement(name=JSONElementName.VALUE_SEPARATOR),
                ],
                JSONElement(name=JSONElementName.STRING),
            ]:
                self._shift(token)

            # ----- Value Separators -----
            case [
                [
                    *_,
                    JSONElement(),
                    JSONElement(name=JSONElementName.VALUE | JSONElementName.MEMBER),
                ],
                JSONElement(name=JSONElementName.VALUE_SEPARATOR),
            ]:
                self._shift(token)

            # ----- Name Separators -----
            case [
                [*_, JSONElement(name=JSONElementName.STRING)],
                JSONElement(name=JSONElementName.NAME_SEPARATOR),
            ]:
                self._shift(token)

            # ----- Object End -----
            case [
                [
                    *_,
                    JSONElement(name=JSONElementName.BEGIN_OBJECT | JSONElementName.MEMBER),
                ],
                JSONElement(name=JSONElementName.END_OBJECT),
            ]:
                self._shift(token)
                self._reduce(JSONElementName.OBJECT, JSONElementName.BEGIN_OBJECT)
                self._reduce(JSONElementName.VALUE, JSONElementName.OBJECT)
                self._reduce_if_member()

            # ----- Array End -----
            case [
                [*_, JSONElement(name=JSONElementName.BEGIN_ARRAY)]
                | [
                    *_,
                    JSONElement(name=JSONElementName.BEGIN_ARRAY) | JSONElement(name=JSONElementName.VALUE_SEPARATOR),
                    JSONElement(name=JSONElementName.VALUE),
                ],
                JSONElement(name=JSONElementName.END_ARRAY),
            ]:
                self._shift(token)
                self._reduce(JSONElementName.ARRAY, JSONElementName.BEGIN_ARRAY)
                self._reduce(JSONElementName.VALUE, JSONElementName.ARRAY)
                self._reduce_if_member()

            # ----- Accept -----
            case [
                [JSONElement(name=JSONElementName.VALUE)],
                JSONElement(name=JSONElementName.END_OF_FILE),
            ]:
                parsed = self._parse_stack.pop()

            # ----- Error -----
            case _:
                raise ValueError(self.ERROR_MESSAGE) from None

        return parsed

    def parse(self, reader: StringIO) -> JSONElement:
        """Generates an abstract syntax tree of a JSON document.

        Args:
            reader: Text stream to the JSON document you want to parse.

        Raises:
            ValueError: If an invalid JSON document is provided.

        Returns:
            An abstract syntax tree with the positions of each element.
        """
        for token in JSONLexer().get_tokens(reader):
            if parsed := self._handle_token(token):
                return parsed

        # Unreachable
        raise ValueError(self.ERROR_MESSAGE)  # pragma: no cover


class JSONLocationMapper:
    """Represents mappings of objects to their locations in a JSON document."""

    def __init__(
        self,
        location_map: defaultdict[str, list[IssueLocationPositionRange]] | None = None,
    ):
        self._location_map = location_map or defaultdict[str, list[IssueLocationPositionRange]](list)

    def __delitem__(self, key: str) -> None:
        del self._location_map[json.dumps(json.loads(key), ensure_ascii=False)]  # pragma: no cover

    def __getitem__(self, key: str) -> list[IssueLocationPositionRange]:
        return self._location_map[json.dumps(json.loads(key), ensure_ascii=False)]

    def _populate_location_map(self, syntax_tree_node: JSONElement, source_path: Path, reader: StringIO):
        if syntax_tree_node.name in {JSONElementName.VALUE, JSONElementName.MEMBER}:
            reader.seek(syntax_tree_node.start_position)
            token_length = syntax_tree_node.end_position - syntax_tree_node.start_position
            location_map_key = reader.read(token_length)

            if syntax_tree_node.name == JSONElementName.MEMBER:
                location_map_key = f"{{{location_map_key}}}"

            location_map_key = json.dumps(json.loads(location_map_key), ensure_ascii=False)

            self._location_map[location_map_key].append(
                IssueLocationPositionRange(
                    path=source_path,
                    positions=PositionRange(
                        begin=PositionReference(
                            line=syntax_tree_node.start_line,
                            column=syntax_tree_node.start_column,
                        ),
                        end=PositionReference(
                            line=syntax_tree_node.end_line,
                            column=syntax_tree_node.end_column,
                        ),
                    ),
                )
            )

        for node in syntax_tree_node.children:
            self._populate_location_map(node, source_path, reader)

    @overload
    def find(self, obj: str) -> list[IssueLocationPositionRange]: ...

    @overload
    def find(self, obj: dict[str, Any]) -> list[IssueLocationPositionRange]: ...

    @overload
    def find(self, obj: list[Any]) -> list[IssueLocationPositionRange]: ...

    @overload
    def find(self, obj: CycloneDXBaseModel) -> list[IssueLocationPositionRange]: ...

    def find(self, obj: str | dict | list | CycloneDXBaseModel | object) -> list[IssueLocationPositionRange]:
        """Get file position information for an object in the parser's file.

        Args:
            obj: Object to search for.

        Raises:
            HopprLoadDataError: Attempted to load invalid JSON string

        Returns:
            A list of `IssueLocationPositionRange` containing start and end locations of the referenced object.
        """
        try:
            match obj:
                case dict() | list():
                    key = json.dumps(obj, ensure_ascii=False)

                case str():
                    key = json.dumps(json.loads(obj), ensure_ascii=False)

                case CycloneDXBaseModel():
                    key = obj.json()

                case _:
                    key = str(obj).replace("'", '"')

            return self._location_map[key]

        except json.JSONDecodeError:
            raise HopprLoadDataError(f"Failed to parse as valid JSON: {obj}") from None

    @classmethod
    def load_file(cls, source_path: PathLike[str] | str) -> Self:
        """Maps JSON values and members to their line and column numbers.

        Args:
            source_path: Path to the source file containing JSON document to be mapped.

        Returns:
            Mapping of parsed JSON objects to their location in the file
        """
        source_path = Path(source_path)
        location_mapper = cls()

        reader = StringIO(initial_value=source_path.read_bytes().decode(encoding="utf-8"))

        try:
            syntax_tree = JSONParser().parse(reader)
            location_mapper._populate_location_map(syntax_tree, source_path, reader)
        finally:
            reader.close()

        return location_mapper
