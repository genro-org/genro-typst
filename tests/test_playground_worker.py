"""The local browser worker uses the same trusted Python recipe lifecycle as the CLI."""

import json
import subprocess
import sys

import pytest

from genro_typst.playground_worker import build_source

RECIPE = '''from genro_typst import TypstBuilder
class Document(TypstBuilder):
    def main(self, root):
        doc = root.document()
        for word in ["Café", "世界"]:
            doc.text(word)
if __name__ == "__main__":
    raise RuntimeError("Main guard must not execute")
'''


def test_worker_uses_real_python_loops_and_preserves_main_guard():
    assert '#text([#"Café"])' in build_source(RECIPE, {})
    assert '#text([#"世界"])' in build_source(RECIPE, {})


def test_worker_supports_local_assets_and_sibling_imports():
    code = '''from genro_typst import TypstBuilder
from helper import title
class Document(TypstBuilder):
    def main(self, root):
        root.document().text(title + open("data.txt").read())
'''
    assert 'Hello Reader' in build_source(code, {"helper.py": 'title = "Hello "', "data.txt": "Reader"})
    with pytest.raises(ModuleNotFoundError):
        # Each actual worker request runs in a new process, with no imported module cache.
        build_source(code.replace("from helper import title", "from missing_helper import title"), {})


@pytest.mark.parametrize("path", ["../escape", "/absolute", "dir/../../escape", "C:/escape", "a\\b", "recipe.typ.py"])
def test_worker_rejects_asset_paths_outside_its_workspace(path):
    with pytest.raises(ValueError):
        build_source(RECIPE, {path: "x"})


def test_worker_prints_do_not_break_protocol():
    request = {"code": 'print("debug output")\n' + RECIPE, "assets": {}}
    result = subprocess.run([sys.executable, "-m", "genro_typst.playground_worker"],
                            input=json.dumps(request), capture_output=True, text=True, check=True)
    assert 'Café' in json.loads(result.stdout)["source"]
    assert 'debug output' in result.stderr


def test_worker_reports_syntax_errors():
    result = subprocess.run([sys.executable, "-m", "genro_typst.playground_worker"],
                            input=json.dumps({"code": "def invalid(", "assets": {}}),
                            capture_output=True, text=True, check=True)
    assert 'SyntaxError' in json.loads(result.stdout)["error"]
