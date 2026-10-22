# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""The standalone Typst document builder."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
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

    @classmethod
    def run(cls, argv: Sequence[str] | None = None) -> Path:
        """Build a recipe and write Typst source to an optional CLI output path.

        Call from a script's ``if __name__ == "__main__"`` guard. With no
        output argument, ``mydoc.typ.py`` and ``mydoc.py`` both produce
        ``mydoc.typ`` beside the script. Explicit relative paths are resolved
        from the working directory. Existing output files are replaced.

        ``argv`` defaults to command-line arguments, excluding the script name.
        The output is always Typst source; no compiler is required.
        Returns the destination path.
        """
        parser = argparse.ArgumentParser(description="Generate Typst source from a Python recipe.")
        parser.add_argument(
            "output", nargs="?", type=Path,
            help="destination path (default: the recipe path with a .typ extension)",
        )
        args = parser.parse_args(argv)
        recipe = Path(sys.argv[0]).absolute()
        if args.output is None:
            if recipe.suffix != ".py":
                parser.error("provide an output path when the recipe filename does not end in .py")
            target = recipe.with_suffix("")
            if target.suffix != ".typ":
                target = target.with_name(target.name + ".typ")
        else:
            target = args.output
        if target.resolve() == recipe.resolve() or (
            target.exists() and recipe.exists() and target.samefile(recipe)
        ):
            parser.error("the output path must not overwrite the Python recipe")
        builder = cls()
        builder.create()
        builder.render(target=target)
        return target

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
