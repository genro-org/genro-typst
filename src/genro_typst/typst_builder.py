# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""TypstBuilder — print documents typeset with Typst.

The grammar comes from ``TypstElements``. Two render modes:
``typst`` returns the Typst source code, ``pdf`` compiles it.
"""

from __future__ import annotations

from genro_builders.builder import BuilderBase

from genro_typst.typst_elements import TypstElements
from genro_typst.typst_renderer import TypstPdfRenderer, TypstRenderer


class TypstBuilder(BuilderBase, TypstElements):
    """Print document builder. Grammar only — rendering on the renderers."""

    _name = "typst"
    _default_render_mode = "typst"

    @property
    def renderer_typst(self) -> TypstRenderer:
        """Fresh ``TypstRenderer`` bound to this builder (Typst source code)."""
        return TypstRenderer(builder=self)

    @property
    def renderer_pdf(self) -> TypstPdfRenderer:
        """Fresh ``TypstPdfRenderer`` bound to this builder (PDF bytes)."""
        return TypstPdfRenderer(builder=self)
