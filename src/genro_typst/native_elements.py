# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Native Typst elements and explicit language constructs."""

from __future__ import annotations

from typing import Any

from genro_builders.builder import element

from genro_typst.native_catalog import CONTENT_TAGS, NATIVE


class NativeElements:
    @element(sub_tags=CONTENT_TAGS)
    def call(
        self,
        function: str,
        content: Any = None,
        args: list[Any] | None = None,
        options: dict[str, Any] | None = None,
        mode: str = "body",
        **attrs: Any,
    ) -> None:
        """Call a native or imported Typst function; mode is body, items, args or value."""
        ...

    @element(sub_tags="")
    def set_rule(self, target: str, options: dict[str, Any] | None = None, **attrs: Any) -> None:
        """Emit a set rule; applies to following siblings in the enclosing scope."""
        ...

    @element(sub_tags="")
    def show_rule(
        self,
        selector: Any,
        transform: Any = None,
        target: str | None = None,
        options: dict[str, Any] | None = None,
        **attrs: Any,
    ) -> None:
        """Emit a transformational show or show-set rule."""
        ...

    @element(sub_tags=CONTENT_TAGS)
    def scope(self) -> None:
        """Content scope: local set/show/let rules do not escape."""
        ...

    @element(sub_tags=CONTENT_TAGS)
    def context(self) -> None:
        """Evaluate children in Typst's contextual evaluation scope."""
        ...

    @element(sub_tags="")
    def equation(self, formula: str, block: bool = True, **options: Any) -> None:
        """Math-mode Typst source without the surrounding dollar signs."""
        ...

    @element(sub_tags="")
    def label(self, name: str) -> None:
        """Attach a label to the preceding labellable element."""
        ...

    @element(sub_tags="")
    def let(self, name: str, value: Any) -> None:
        """Bind a literal or explicit expression for following siblings."""
        ...

    @element(sub_tags="")
    def import_module(
        self, path: str, names: list[str] | None = None, alias: str | None = None
    ) -> None:
        """Import a local module or versioned Typst package."""
        ...

    @element(sub_tags="")
    def include(self, path: str) -> None:
        """Include a local Typst file relative to the compiler root."""
        ...

    @element(sub_tags="")
    def typst_code(self, code: str) -> None:
        """Insert trusted Typst code as one code block; definitions stay local."""
        ...

    @element(sub_tags="")
    def typst_markup(self, source: str) -> None:
        """Insert trusted Typst markup in its own content scope."""
        ...


def _declare(tag: str, function: str, mode: str) -> Any:
    def declaration(
        self: Any,
        content: Any = None,
        args: list[Any] | None = None,
        options: dict[str, Any] | None = None,
        **attrs: Any,
    ) -> None:
        pass

    declaration.__name__ = tag
    declaration.__doc__ = (
        f"Native {function}: {mode} arguments. See docs/native-reference.md. "
        "content is literal text/value, args supplies positional arguments, "
        "options and keyword attributes supply native named parameters."
    )
    return element(sub_tags="" if mode == "leaf" else CONTENT_TAGS)(declaration)


for _tag, (_function, _mode, _section) in NATIVE.items():
    setattr(NativeElements, _tag, _declare(_tag, _function, _mode))
