#!/usr/bin/env python3
# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Export the portable builder grammar and renderer metadata; --check detects drift."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from genro_typst import TypstBuilder
from genro_typst.native_catalog import AUTHORING_ALIASES, NATIVE
from genro_typst.typst_values import NAMED_COLORS

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    with TemporaryDirectory() as directory:
        path = Path(directory) / "typst.json"
        TypstBuilder.to_grammar(path)
        grammar = path.read_text(encoding="utf-8")
    metadata = json.dumps(
        {"native": NATIVE, "namedColors": sorted(NAMED_COLORS), "authoringAliases": AUTHORING_ALIASES},
        indent=2, ensure_ascii=False,
    ) + "\n"
    files = {
        "src/typst.json": grammar,
        "src/catalog.json": metadata,
        "LICENSE": (ROOT / "LICENSE").read_text(encoding="utf-8"),
        "NOTICE": (ROOT / "NOTICE").read_text(encoding="utf-8"),
    }
    stale = []
    for name, content in files.items():
        target = ROOT / "js" / name
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(str(target.relative_to(ROOT)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    if stale:
        parser.exit(1, "Run python tools/export_js.py; stale files: " + ", ".join(stale) + "\n")


if __name__ == "__main__":
    main()
