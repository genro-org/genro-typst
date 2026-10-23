# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Build a trusted local playground recipe in a disposable worker process."""

from __future__ import annotations

import json
import os
import sys
import traceback
from contextlib import redirect_stdout
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

from genro_typst.cli import load_builder, recipe_environment


def build_source(code: str, assets: dict[str, str]) -> str:
    """Use the CLI's class selection and lifecycle, without executing the main guard."""
    previous = Path.cwd()
    with TemporaryDirectory(prefix="genro-typst-playground-") as directory:
        root = Path(directory)
        for name, content in assets.items():
            path = PurePosixPath(name)
            if not name or path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
                raise ValueError(f"Invalid asset path: {name}")
            if name == "recipe.typ.py":
                raise ValueError("Asset path is reserved: recipe.typ.py")
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        recipe = root / "recipe.typ.py"
        recipe.write_text(code, encoding="utf-8")
        try:
            os.chdir(root)
            with recipe_environment(recipe):
                builder = load_builder(recipe)()
                builder.create()
                source = builder.render()
                if not isinstance(source, str):
                    raise TypeError("The recipe must render Typst source as text")
                return source
        finally:
            os.chdir(previous)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        # Recipe prints go to stderr; stdout remains the worker protocol.
        with redirect_stdout(sys.stderr):
            source = build_source(payload["code"], payload.get("assets", {}))
        result = {"source": source}
    except (Exception, SystemExit):  # noqa: BLE001 - return recipe failures over the worker protocol
        result = {"error": traceback.format_exc()}
    json.dump(result, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
