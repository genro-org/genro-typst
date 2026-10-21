# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Typst compilation and SVG previews, independent of any application."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Any


@dataclass(frozen=True)
class CompiledDocument:
    pdf: bytes
    pages: int | None
    svg_pages: tuple[bytes, ...] = ()


class TypstEngine:
    name = "typst"
    source_mode = "typst"
    source_filename = "main.typ"

    def compile(
        self, source: str, *, root: Path | None = None, preview: bool = False
    ) -> CompiledDocument:
        try:
            import typst
        except ImportError as error:
            raise RuntimeError("Install genro-typst[pdf] to use Typst.") from error
        options: dict[str, Any] = {"timestamp": int(time())}
        if root:
            options["root"] = str(root)
        pdf = typst.compile(source.encode("utf-8"), format="pdf", **options)
        pages: Any = (
            typst.compile(source.encode("utf-8"), format="svg", **options) if preview else []
        )
        if isinstance(pages, bytes):
            pages = [pages]
        return CompiledDocument(pdf, len(pages) if preview else None, tuple(pages))
