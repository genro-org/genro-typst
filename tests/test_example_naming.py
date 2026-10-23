"""Python and JavaScript gallery recipes share one authoring vocabulary."""

import ast
import json
import re
import runpy
from pathlib import Path

import pytest

from genro_typst.native_catalog import AUTHORING_ALIASES, NATIVE, SPECIAL

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "js/examples/browser/catalog.json").read_text())


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


@pytest.mark.parametrize("entry", [*CATALOG["examples"], {"id": "welcome", **CATALOG["welcome"]}],
                         ids=lambda entry: entry["id"])
def test_displayed_python_recipe_produces_the_shared_typst_source(entry):
    namespace = {"__name__": "browser_example_test"}
    exec(entry["python"], namespace)  # noqa: S102 - trusted repository examples
    builder = namespace["Document"]()
    builder.create()
    assert builder.render() == entry["source"]


def test_downloaded_python_recipe_runs_directly(tmp_path):
    import subprocess
    import sys

    recipe = tmp_path / "welcome.typ.py"
    recipe.write_text(CATALOG["welcome"]["python"])
    result = subprocess.run([sys.executable, str(recipe)], capture_output=True, text=True, check=True)
    assert (tmp_path / "welcome.typ").read_text() == CATALOG["welcome"]["source"]
    assert str(tmp_path / "welcome.typ") in result.stdout
