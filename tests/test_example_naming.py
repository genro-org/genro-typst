"""Python and JavaScript gallery recipes share one authoring vocabulary."""

import ast
import json
import re
import runpy
from pathlib import Path

from genro_typst.native_catalog import AUTHORING_ALIASES, NATIVE, SPECIAL

ROOT = Path(__file__).resolve().parents[1]


def test_python_and_javascript_examples_use_identical_method_names():
    python = runpy.run_path(str(ROOT / "tools/export_app_examples.py"))["catalog"]()
    javascript = json.loads((ROOT / "js/examples/browser/catalog.json").read_text())
    js_entries = {entry["id"]: entry for entry in javascript["examples"]}
    assert set(js_entries) == {entry["id"] for entry in python["examples"]}
    tags = set(NATIVE) | set(SPECIAL) | {
        "document", "layout", "row", "cell", "paragraph", "pageNumber", "table", "column",
    }
    canonical = {AUTHORING_ALIASES.get(tag, tag) for tag in tags}

    def elements(methods):
        return {name for name in methods if name in tags or name.startswith("typst_")}

    for entry in python["examples"]:
        py_names = elements(node.func.attr for node in ast.walk(ast.parse(entry["code"]))
                            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute))
        js_names = elements(re.findall(r"\.(\w+)\(", js_entries[entry["id"]]["code"]))
        assert py_names == js_names, entry["id"]
        assert py_names <= canonical, (entry["id"], py_names - canonical)
