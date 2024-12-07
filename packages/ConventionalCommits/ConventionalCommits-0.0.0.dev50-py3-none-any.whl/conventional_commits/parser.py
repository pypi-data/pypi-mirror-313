from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import re as _re
import pyserials as _ps

import conventional_commits as _convcom

if _TYPE_CHECKING:
    from typing import Sequence, Callable
    from re import Pattern


class ConventionalCommitParser:
    def __init__(
        self,
        type_regex: Pattern,
        scope_regex: Pattern,
        description_regex: Pattern,
        scope_start_separator_regex: Pattern,
        scope_end_separator_regex: Pattern,
        scope_items_separator_regex: Pattern,
        description_separator_regex: Pattern,
        body_separator_regex: Pattern,
        footer_separator_regex: Pattern,
        footer_reader: Callable[[str], dict],
        footer_special_lines: Sequence[tuple[str, Callable[[_re.Match, dict], None]]],
    ):
        self._type_regex = type_regex
        self._scope_regex = scope_regex
        self._description_regex = description_regex
        self._scope_start_separator_regex = scope_start_separator_regex
        self._scope_end_separator_regex = scope_end_separator_regex
        self._scope_items_separator_regex = scope_items_separator_regex
        self._description_separator_regex = description_separator_regex
        self._body_separator_regex = body_separator_regex
        self._footer_separator_regex = footer_separator_regex
        self._footer_reader = footer_reader
        self._footer_special_lines = footer_special_lines
        return

    def parse(self, message: str) -> _convcom.ConventionalCommitMessage | None:
        if not isinstance(message, str):
            raise TypeError(f"Invalid commit message type: {type(message)}")
        rest, footer = self._parse_footer(message)
        if not rest:
            raise ValueError("Empty commit message")
        summary, body = self._parse_body(rest)
        if not summary:
            raise ValueError("Empty commit summary")
        typ, scope, description = self._parse_summary(summary)
        return _convcom.create(
            type=typ,
            scope=scope,
            description=description,
            body=body,
            footer=footer,
            type_regex=self._type_regex,
            scope_regex=self._scope_regex,
            description_regex=self._description_regex,
        )

    def _parse_summary(self, summary: str) -> tuple[str | None, list[str], str]:
        parts = self._description_separator_regex.split(summary, maxsplit=1)
        if len(parts) == 1:
            typ = ""
            scope = []
            description = parts[0]
        else:
            description = parts[1]
            parts = self._scope_start_separator_regex.split(parts[0], maxsplit=1)
            if len(parts) == 1:
                typ = parts[0]
                scope = []
            else:
                typ = parts[0]
                scope_clean = self._scope_end_separator_regex.split(parts[1], maxsplit=1)
                if len(scope_clean) == 1:
                    raise ValueError(f"Invalid scope: {parts[1]}")
                if scope_clean[1].strip():
                    raise ValueError(f"Invalid scope end: {scope_clean[1]}")
                scope_clean = scope_clean[0]
                scope = self._scope_items_separator_regex.split(scope_clean)
        return typ, scope, description

    def _parse_body(self, footerless_message: str) -> tuple[str, str]:
        parts = self._body_separator_regex.split(footerless_message, maxsplit=1)
        if len(parts) == 1:
            return footerless_message, ""
        return parts[0].strip(), parts[1].strip()


    def _parse_footer(self, message: str) -> tuple[str, dict]:
        parts = self._footer_separator_regex.split(message, maxsplit=1)
        if len(parts) == 1:
            return message, {}
        rest, footer_str = parts

        footer_lines_special = []
        if self._footer_special_lines:
            footer_lines = footer_str.splitlines()
            footer_lines_main = []
            for footer_line in footer_lines:
                for pattern, handler in self._footer_special_lines:
                    match = _re.match(pattern, footer_line)
                    if match:
                        footer_lines_special.append((match, handler))
                        break
                else:
                    footer_lines_main.append(footer_line)
            footer_str = "\n".join(footer_lines_main)
        try:
            footer = self._footer_reader(footer_str)
        except Exception as e:
            raise ValueError(f"Invalid footer: {footer_str}") from e
        if footer_lines_special:
            for match, handler in footer_lines_special:
                handler(match, footer)
        if not isinstance(footer, dict):
            raise ValueError(f"Invalid footer type {type(footer)}: {footer}")
        return rest.strip(), footer
