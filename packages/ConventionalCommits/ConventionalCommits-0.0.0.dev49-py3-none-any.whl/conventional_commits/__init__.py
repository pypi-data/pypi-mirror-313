from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import re as _re

import pyserials as _ps

from conventional_commits.message import ConventionalCommitMessage
from conventional_commits.parser import ConventionalCommitParser

if _TYPE_CHECKING:
    from typing import Sequence, Callable, Any
    from re import Pattern


def create(
    description: str,
    type: str | None = None,
    scope: Sequence[str] | None = None,
    body: str | None = None,
    footer: Any = None,
    scope_start: str = "(",
    scope_separator: str = ", ",
    scope_end: str = ")",
    description_separator: str = ": ",
    body_separator: str = "\n\n",
    footer_separator: str = f"\n\n{'-' * 50}\n",
    footer_writer: Callable[[Any], str] = _ps.write.to_yaml_string,
    type_regex: Pattern | str = r"^[^:\s(),]*$",
    scope_regex: Pattern | str = r"^[^:\s(),]+$",
    description_regex: Pattern | str = r"^[^\n]+$",
) -> ConventionalCommitMessage:
    """Create a Conventional Commit message."""
    return ConventionalCommitMessage(
        type=type or "",
        scope=scope or [],
        description=description,
        body=body or "",
        footer=footer or {},
        scope_start=scope_start,
        scope_separator=scope_separator,
        scope_end=scope_end,
        description_separator=description_separator,
        body_separator=body_separator,
        footer_separator=footer_separator,
        footer_writer=footer_writer,
        type_regex=_re.compile(type_regex) if isinstance(type_regex, str) else type_regex,
        scope_regex=_re.compile(scope_regex) if isinstance(scope_regex, str) else scope_regex,
        description_regex=_re.compile(description_regex) if isinstance(description_regex, str) else description_regex,
    )


def parse(
    message: str,
    type_regex: Pattern | str = r"^[^:\s(),]*$",
    scope_regex: Pattern | str = r"^[^:\s(),]+$",
    description_regex: Pattern | str = r"^[^\n]+$",
    scope_start_separator_regex: Pattern | str = r"\s*\(\s*",
    scope_end_separator_regex: Pattern | str = r"\s*\)\s*",
    scope_items_separator_regex: Pattern | str = r"\s*,\s*",
    description_separator_regex: Pattern | str = r"\s*:\s+",
    body_separator_regex: Pattern | str = r"\n",
    footer_separator_regex: Pattern | str = r"\n-{3,}\n",
    footer_reader: Callable[[str], Any] = _ps.read.yaml_from_string,
    footer_special_lines: Sequence[tuple[str, Callable[[_re.Match, Any], None]]] = (
        (r"^-{3,}$", lambda match, footer: None),
        (
            r"^Co-authored-by:\s+(.+?)\s+<(.+?)>\s*$",
            lambda match, footer: footer.setdefault("co_authored_by", []).append(
                {"name": match.group(1), "email": match.group(2)}
            ),
        ),
    ),
) -> ConventionalCommitMessage:
    return create_parser(
        type_regex=type_regex,
        scope_regex=scope_regex,
        description_regex=description_regex,
        scope_start_separator_regex=scope_start_separator_regex,
        scope_end_separator_regex=scope_end_separator_regex,
        scope_items_separator_regex=scope_items_separator_regex,
        description_separator_regex=description_separator_regex,
        body_separator_regex=body_separator_regex,
        footer_separator_regex=footer_separator_regex,
        footer_reader=footer_reader,
        footer_special_lines=footer_special_lines,
    ).parse(message)


def create_parser(
    type_regex: Pattern | str = r"^[^:\s(),]*$",
    scope_regex: Pattern | str = r"^[^:\s(),]+$",
    description_regex: Pattern | str = r"^[^\n]+$",
    scope_start_separator_regex: Pattern | str = r"\s*\(\s*",
    scope_end_separator_regex: Pattern | str = r"\s*\)\s*",
    scope_items_separator_regex: Pattern | str = r"\s*,\s*",
    description_separator_regex: Pattern | str = r"\s*:\s+",
    body_separator_regex: Pattern | str = r"\n",
    footer_separator_regex: Pattern | str = r"\n-{3,}\n",
    footer_reader: Callable[[str], Any] = _ps.read.yaml_from_string,
    footer_special_lines: Sequence[tuple[str, Callable[[_re.Match, Any], None]]] = (
        (r"^-{3,}$", lambda match, footer: None),
        (
            r"^Co-authored-by:\s+(.+?)\s+<(.+?)>\s*$",
            lambda match, footer: footer.setdefault("co_authored_by", []).append(
                {"name": match.group(1), "email": match.group(2)}
            ),
        ),
    ),
) -> ConventionalCommitParser:
    return ConventionalCommitParser(
        type_regex=_re.compile(type_regex) if isinstance(type_regex, str) else type_regex,
        scope_regex=_re.compile(scope_regex) if isinstance(scope_regex, str) else scope_regex,
        description_regex=_re.compile(
            description_regex
        ) if isinstance(description_regex, str) else description_regex,
        scope_start_separator_regex=_re.compile(
            scope_start_separator_regex
        ) if isinstance(scope_start_separator_regex, str) else scope_start_separator_regex,
        scope_end_separator_regex=_re.compile(
            scope_end_separator_regex
        ) if isinstance(scope_end_separator_regex, str) else scope_end_separator_regex,
        scope_items_separator_regex=_re.compile(
            scope_items_separator_regex
        ) if isinstance(scope_items_separator_regex, str) else scope_items_separator_regex,
        description_separator_regex=_re.compile(
            description_separator_regex
        ) if isinstance(description_separator_regex, str) else description_separator_regex,
        body_separator_regex=_re.compile(
            body_separator_regex
        ) if isinstance(body_separator_regex, str) else body_separator_regex,
        footer_separator_regex=_re.compile(
            footer_separator_regex
        ) if isinstance(footer_separator_regex, str) else footer_separator_regex,
        footer_reader=footer_reader,
        footer_special_lines=footer_special_lines,
    )
