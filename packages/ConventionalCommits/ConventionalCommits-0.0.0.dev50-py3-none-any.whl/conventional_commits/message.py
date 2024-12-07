from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING, Sequence as _Sequence
import copy as _copy

import pyserials as _ps

if _TYPE_CHECKING:
    from typing import Callable, Any
    from re import Pattern


class ConventionalCommitMessage:
    def __init__(
        self,
        type: str,
        scope: _Sequence[str],
        description: str,
        body: str,
        footer: Any,
        scope_start: str,
        scope_separator: str,
        scope_end: str,
        description_separator: str,
        body_separator: str,
        footer_separator: str,
        footer_writer: Callable[[dict], str],
        type_regex: Pattern,
        scope_regex: Pattern,
        description_regex: Pattern,
    ):
        self._type_regex = type_regex
        self._scope_regex = scope_regex
        self._description_regex = description_regex

        self.scope_start = scope_start
        self.scope_separator = scope_separator
        self.scope_end = scope_end
        self.description_separator = description_separator
        self.body_separator = body_separator
        self.footer_separator = footer_separator
        self.footer_writer = footer_writer

        self.type = type
        self.scope = scope
        self.description = description
        self.body = body
        self.footer = footer
        return

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Type must be a string, but got {type(value)}: {value}")
        if not self._type_regex.match(value):
            raise ValueError(f"Type does not match RegEx '{self._type_regex}': {value}")
        self._type = value
        return

    @property
    def scope(self) -> tuple[str, ...]:
        return self._scope

    @scope.setter
    def scope(self, value: _Sequence[str]):
        if isinstance(value, str) or not isinstance(value, _Sequence):
            raise TypeError(f"Scope must be a sequence of strings, but got {type(value)}: {value}")
        for scope_entry in value:
            if not isinstance(scope_entry, str):
                raise TypeError(f"Scope elements must be strings, but got {type(scope_entry)}: {scope_entry}")
            if not self._scope_regex.match(scope_entry):
                raise ValueError(f"Scope element does not match RegEx '{self._scope_regex}': {scope_entry}")
        self._scope = tuple(value)
        return

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Description must be a string, but got {type(value)}: {value}")
        if not self._description_regex.match(value):
            raise ValueError(f"Description does not match RegEx '{self._description_regex}': {value}")
        self._description = value
        return

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f"Body must be a string, but got {type(value)}: {value}")
        self._body = value.strip()
        return

    @property
    def footer(self) -> Any:
        return _copy.deepcopy(self._footer)

    @footer.setter
    def footer(self, value: Any):
        try:
            self.footer_writer(value)
        except Exception as e:
            raise ValueError(f"Invalid footer data: {value}") from e
        self._footer = _copy.deepcopy(value)
        return

    @property
    def parts(self) -> dict:
        return {
            "type": self.type,
            "scope": self.scope,
            "description": self.description,
            "body": self.body,
            "footer": self.footer,
        }

    @property
    def signature(self):
        typ = self.type or ""
        scope = f"{self.scope_start}{self.scope_separator.join(self.scope)}{self.scope_end}" if self.scope else ""
        return f"{typ}{scope}"
    
    @property
    def summary(self) -> str:
        if not self.type:
            return self.description
        return f"{self.signature}{self.description_separator}{self.description}"

    @property
    def footerless(self) -> str:
        commit = self.summary
        if self.body:
            commit += f"{self.body_separator}{self.body}"
        return commit.strip()

    def __str__(self):
        commit = self.footerless
        if self._footer:
            footer_str = self.footer_writer(self._footer)
            if footer_str:
                commit += f"{self.footer_separator}{footer_str}"
        return commit.strip()

    def __repr__(self):
        return (
            f"ConventionalCommitMessage(\n"
            f"  type={repr(self.type)},\n"
            f"  scope={repr(self.scope)},\n"
            f"  description={repr(self.description)},\n"
            f"  body={repr(self._body)},\n"
            f"  footer={repr(self._footer)},\n"
            f"  scope_start={repr(self.scope_start)},\n"
            f"  scope_separator={repr(self.scope_separator)},\n"
            f"  scope_end={repr(self.scope_end)},\n"
            f"  description_separator={repr(self.description_separator)},\n"
            f"  body_separator={repr(self.body_separator)},\n"
            f"  footer_separator={repr(self.footer_separator)},\n"
            f"  footer_writer={repr(self.footer_writer)},\n"
            f"  type_regex={repr(self._type_regex)},\n"
            f"  scope_regex={repr(self._scope_regex)},\n"
            f"  description_regex={repr(self._description_regex)},\n"
            f")"
        )
