# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Execute Python builder recipes and deliver Typst, PDF or SVG files."""

from __future__ import annotations

import argparse
import runpy
import sys
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any, TypeGuard

from genro_typst.compiler import TypstEngine
from genro_typst.typst_builder import TypstBuilder

RECIPE_MODULE = "__genro_typst_recipe__"


@contextmanager
def recipe_environment(recipe: Path) -> Iterator[None]:
    """Allow sibling Python imports without changing the caller's working directory."""
    previous_path, previous_argv = sys.path[:], sys.argv
    try:
        sys.path.insert(0, str(recipe.parent))
        sys.argv = [str(recipe)]
        yield
    finally:
        sys.path[:] = previous_path
        sys.argv = previous_argv


def load_builder(recipe: Path, name: str | None = None) -> type[TypstBuilder]:
    """Load without running the main guard; choose an explicit or unique local class."""
    with recipe_environment(recipe):
        namespace = runpy.run_path(str(recipe), run_name=RECIPE_MODULE)

    def is_builder(value: Any) -> TypeGuard[type[TypstBuilder]]:
        return isinstance(value, type) and value is not TypstBuilder and issubclass(value, TypstBuilder)

    selected = name or ("BUILDER" if "BUILDER" in namespace else None)
    if selected:
        candidate = namespace.get(selected)
        if not is_builder(candidate):
            raise ValueError(f"{selected} must name a TypstBuilder subclass in the recipe")
        return candidate
    candidates = {
        value for value in namespace.values()
        if is_builder(value) and value.__module__ == RECIPE_MODULE
    }
    if len(candidates) != 1:
        raise ValueError(
            "Recipe must define one TypstBuilder subclass; "
            "set BUILDER = MyDocument or use --builder MyDocument to select one"
        )
    return candidates.pop()


def default_output(recipe: Path, output_format: str) -> Path:
    """Remove .py and an optional .typ, then add the requested format."""
    stem = recipe.name.removesuffix(".py").removesuffix(".typ")
    return recipe.with_name(f"{stem}.{output_format}")


def check_destination(target: Path, recipe: Path) -> None:
    if target.resolve() == recipe.resolve() or (
        target.exists() and target.samefile(recipe)
    ):
        raise ValueError("The output path must not overwrite the Python recipe")
    if target.is_dir():
        raise ValueError(f"Output path is a directory: {target}")


def generate(
    recipe: Path, *, output_format: str = "typ", output: Path | None = None,
    builder_name: str | None = None, root: Path | None = None,
) -> list[Path]:
    """Build once, render completely, then write output files; return their paths."""
    recipe = recipe.absolute()
    if not recipe.is_file() or recipe.suffix != ".py":
        raise ValueError(f"Expected an existing Python recipe (.py): {recipe}")
    if output_format not in {"typ", "pdf", "svg"}:
        raise ValueError(f"Unknown output format: {output_format}")
    target = output if output is not None else default_output(recipe, output_format)
    check_destination(target, recipe)
    compiler_root = root.absolute() if root is not None else recipe.parent
    if output_format != "typ" and not compiler_root.is_dir():
        raise ValueError(f"Compilation root is not a directory: {compiler_root}")
    with recipe_environment(recipe):
        builder_class = load_builder(recipe, builder_name)
        builder = builder_class()
        builder.create()
        source = builder.render()
    if output_format == "typ":
        files = [(target, source.encode("utf-8"))]
    else:
        compiled = TypstEngine().compile(source, root=compiler_root, preview=output_format == "svg")
        if output_format == "pdf":
            files = [(target, compiled.pdf)]
        elif len(compiled.svg_pages) == 1:
            files = [(target, compiled.svg_pages[0])]
        else:
            if not compiled.svg_pages:
                raise ValueError("Typst returned no SVG pages")
            files = [
                (target.with_name(f"{target.stem}-{index}{target.suffix}"), page)
                for index, page in enumerate(compiled.svg_pages, start=1)
            ]
    # Check every page before writing any output, including recipe aliases.
    for path, _ in files:
        check_destination(path, recipe)
    for path, content in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return [path for path, _ in files]


def main(argv: Sequence[str] | None = None) -> int:
    """Console entry point. Usage errors exit 2; recipe/render errors return 1."""
    parser = argparse.ArgumentParser(
        prog="genro-typst", description="Generate Typst, PDF or SVG from a Python builder recipe."
    )
    parser.add_argument("recipe", type=Path, help="Python recipe, e.g. mydoc.typ.py")
    parser.add_argument("-o", "--output", type=Path, help="output path (default: beside the recipe)")
    formats = parser.add_mutually_exclusive_group()
    for name, help_text in (
        ("typ", "generate Typst source (default)"),
        ("pdf", "compile a PDF using the optional typst Python package"),
        ("svg", "compile SVG pages; multipage output uses name-1.svg, name-2.svg, ..."),
    ):
        formats.add_argument(f"--{name}", dest="output_format", action="store_const",
                             const=name, help=help_text)
    parser.set_defaults(output_format="typ")
    parser.add_argument("--builder", help="name of a TypstBuilder subclass defined or imported by the recipe")
    parser.add_argument("--root", type=Path, help="Typst asset root (default: recipe directory)")
    args = parser.parse_args(argv)
    try:
        paths = generate(args.recipe, output_format=args.output_format, output=args.output,
                         builder_name=args.builder, root=args.root)
    except Exception as error:  # noqa: BLE001 -- CLI boundary for recipe/compiler exceptions.
        print(f"genro-typst: {error}", file=sys.stderr)
        return 1
    for path in paths:
        print(path)
    return 0
