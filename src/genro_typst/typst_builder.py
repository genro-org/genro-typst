# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""The standalone Typst document builder."""

from typing import Any

from genro_builders import BuilderBase
from genro_builders.renderer import RendererBase

from genro_typst.native_catalog import NATIVE
from genro_typst.native_elements import NativeElements
from genro_typst.typst_elements import TypstElements
from genro_typst.typst_renderer import TypstPdfRenderer, TypstRenderer


class TypstBuilder(BuilderBase, TypstElements, NativeElements):
    _name = "typst"
    _default_render_mode = "typst"
    pdf_engine = "typst"

    def __getattr__(self, name: str) -> Any:
        handler = super().__getattr__(name)
        if name not in NATIVE and name != "call":
            return handler

        def native(destination: Any, *args: Any, **kwargs: Any) -> Any:
            # Bag leaf values become child Bags when nesting. Keep native content
            # as an attribute so adding children cannot erase text or link URLs.
            if len(args) > 1:
                raise ValueError("Use args=[...] for multiple Typst positional arguments")
            if args:
                if "content" in kwargs:
                    raise ValueError("Use either positional content or content=, not both")
                kwargs["content"] = args[0]
            return handler(destination, **kwargs)

        return native

    @property
    def renderer_typst(self) -> TypstRenderer:
        return TypstRenderer(builder=self)

    @property
    def renderer_pdf(self) -> RendererBase:
        return TypstPdfRenderer(builder=self)
