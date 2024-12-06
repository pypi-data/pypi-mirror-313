"""Exclude models for `hopctl validate sbom` configuration file."""

from __future__ import annotations

import re

from typing import TYPE_CHECKING, TypeGuard

import jmespath.functions

from pydantic import root_validator

from hoppr.models.validation.base import BaseExcludeConfig

if TYPE_CHECKING:
    from rich.repr import RichReprResult


class JMESPathOptions(jmespath.Options):
    """Custom JMESPath options and function to enable evaluation of regular expressions."""

    class JMESPathRegexFunction(jmespath.functions.Functions):
        """Custom JMESPath function to enable evaluation of regular expressions."""

        @jmespath.functions.signature({"types": ["string", "null"]}, {"types": ["string"]})
        def _func_regexp(self, string: str, pattern: str) -> bool:
            """Enables use of a custom `regexp` function inside a JMESPath search expression.

            NOTE: the `_func_` method name prefix is required.

            Args:
                string: The string to search
                pattern: The pattern to match against

            Returns:
                `True` if a match was found, otherwise `False`
            """
            if not string or not (
                pattern_match := re.match(
                    pattern="(?:regexp:)?/(?P<pattern>.*)/(?P<flags>[GMIgmi]+)?",
                    string=pattern,
                )
            ):
                return False

            pattern = pattern_match["pattern"]

            re_func = re.match
            re_flags = re.RegexFlag(0)

            for flag in pattern_match["flags"] or "":
                if flag.upper() == "G":
                    re_func = re.search
                else:
                    re_flags |= re.RegexFlag[flag.upper()]

            return re_func(pattern=pattern, string=string, flags=re_flags) is not None

    def __init__(self):
        super().__init__(custom_functions=self.JMESPathRegexFunction())


class ExcludeConfig(BaseExcludeConfig):
    """Configuration for items to exclude from validation."""

    def __repr__(self) -> str:  # pragma: no cover
        attributes = ", ".join([f"{key}={value}" for key, value in self.__dict__.items() if value])
        return f"ExcludeConfig({attributes})"

    def __rich_repr__(self) -> RichReprResult:  # pragma: no cover
        yield from [(key, value) for key, value in self.__dict__.items() if value]

    @classmethod
    def _build_jmespath(cls, obj: object) -> list[str]:
        expr: list[str] = []

        match obj:
            case dict():
                expr.extend(cls._build_jmespath(list(obj.items())))

            case list():
                expr.extend(token for value in obj for token in cls._build_jmespath(value))

            case (str() as key, dict() as value):
                expr.extend(
                    token
                    for subkey, subvalue in value.items()
                    for token in cls._build_jmespath((f'"{key}"."{subkey}"', subvalue))
                )

            case (str() as key, list() as values):
                expr.extend([f'"{key}"', "[?", *cls._build_jmespath(values), "]"])

            case (str() as key, str() as value) if value.startswith("regexp:"):
                expr.append(f"""regexp("{key}", '{value}')""")

            case (*_, str() as value) if value.startswith("jmespath:"):
                expr.append(value.removeprefix("jmespath:"))

            case (str() as key, str() as value):
                expr.extend([key, "==", f"'{value}'"])

        return expr

    @root_validator
    @classmethod
    def convert_to_jmespath(cls, values: dict[str, list[str | object] | None]) -> dict[str, list[str]]:
        """Convert complex objects to JMESPath expressions."""

        def _has_items(obj: tuple[str, list[object] | None]) -> TypeGuard[tuple[str, list[object]]]:
            return bool(obj[1])

        converted: dict[str, list[str]] = {
            field_name: [
                item if isinstance(item, str) and item.startswith("jmespath:")
                else f"jmespath:[?{''.join(cls._build_jmespath(item))}]"
                for item in items
            ]
            for field_name, items in filter(_has_items, values.items())
        }  # fmt: skip

        return converted
