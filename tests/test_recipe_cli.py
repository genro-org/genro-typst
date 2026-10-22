# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Executable recipes: destination paths, imports and failure behavior."""

import os
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

from genro_typst import TypstBuilder

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/04_python_recipe/mydoc.typ.py"


class Recipe(TypstBuilder):
    def setup(self, data):
        data["title"] = "Café — 日本語"

    def main(self, root):
        root.document().heading("^title", level=1)


@pytest.mark.parametrize("filename", ["mydoc.typ.py", "mydoc.py", "mydoc.v2.typ.py"])
def test_default_output_beside_recipe(monkeypatch, tmp_path, filename):
    recipe = tmp_path / "recipes" / filename
    recipe.parent.mkdir()
    recipe.write_text("# recipe", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [str(recipe)])
    monkeypatch.chdir(tmp_path)

    target = Recipe.run()

    expected_name = filename[:-3]
    if not expected_name.endswith(".typ"):
        expected_name += ".typ"
    assert target == recipe.parent / expected_name
    assert "Café — 日本語" in target.read_text(encoding="utf-8")
    assert recipe.read_text() == "# recipe"
    assert not (tmp_path / expected_name).exists()


@pytest.mark.parametrize("absolute", [False, True])
def test_explicit_output_and_repeated_run(monkeypatch, tmp_path, absolute):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [str(tmp_path / "mydoc.typ.py")])
    output = Path("output folder/custom.typ")
    if absolute:
        output = tmp_path / output
    target = Recipe.run([str(output)])
    assert target == output
    original = output.read_text(encoding="utf-8")
    output.write_text("old output", encoding="utf-8")
    Recipe.run([str(output)])
    assert output.read_text(encoding="utf-8") == original
    assert not (tmp_path / "mydoc.typ").exists()


@pytest.mark.parametrize("alias", ["same", "symlink", "hardlink"])
def test_cannot_overwrite_recipe(monkeypatch, tmp_path, alias):
    recipe = tmp_path / "mydoc.typ.py"
    recipe.write_text("# keep me", encoding="utf-8")
    output = recipe
    if alias != "same":
        output = tmp_path / "alias.typ"
        if alias == "symlink":
            output.symlink_to(recipe)
        else:
            os.link(recipe, output)
    monkeypatch.setattr(sys, "argv", [str(recipe)])
    with pytest.raises(SystemExit) as error:
        Recipe.run([str(output)])
    assert error.value.code == 2
    assert recipe.read_text() == "# keep me"


@pytest.mark.parametrize("args, code", [(["--help"], 0), (["a.typ", "b.typ"], 2)])
def test_cli_usage_does_not_write(monkeypatch, tmp_path, args, code):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [str(tmp_path / "mydoc.typ.py")])
    with pytest.raises(SystemExit) as error:
        Recipe.run(args)
    assert error.value.code == code
    assert list(tmp_path.iterdir()) == []


def test_example_runs_as_script_and_import_is_passive(tmp_path):
    recipe = tmp_path / "mydoc.typ.py"
    recipe.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
    runpy.run_path(str(recipe))
    assert not recipe.with_suffix("").exists()

    # A missing compiler must not prevent source generation, including imports.
    (tmp_path / "typst.py").write_text("raise ImportError('compiler not installed')\n")
    for args, output in (([], recipe.with_suffix("")), (["custom.typ"], tmp_path / "custom.typ")):
        result = subprocess.run(
            [sys.executable, str(recipe), *args], cwd=tmp_path,
            capture_output=True, text=True, check=False,
        )
        assert result.returncode == 0, result.stderr
        source = output.read_text(encoding="utf-8")
        assert source.startswith("#set page(")
        assert "Department: Research" in source
        assert "Department: Support" in source
    assert not list(tmp_path.glob("*.pdf"))


def test_no_default_for_non_python_entrypoint(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["-c"])
    with pytest.raises(SystemExit) as error:
        Recipe.run([])
    assert error.value.code == 2
    assert Recipe.run([str(tmp_path / "custom.typ")]).is_file()


@pytest.mark.parametrize("mode", ["typ", "pdf", "svg"])
def test_direct_format_options_match_cli_without_reloading(tmp_path, mode):
    recipe = tmp_path / "document.typ.py"
    recipe.write_text('''from pathlib import Path
from genro_typst import TypstBuilder
marker = Path(__file__).with_name("loads.txt")
marker.write_text(marker.read_text() + "loaded\\n" if marker.exists() else "loaded\\n")
class Document(TypstBuilder):
    def main(self, root):
        doc = root.document()
        doc.heading("One")
        doc.pagebreak()
        doc.text("Two")
if __name__ == "__main__":
    Document.run()
''')
    output = tmp_path / "direct" / f"result.{mode}"
    reference = tmp_path / "cli" / f"result.{mode}"
    for command, destination in (([sys.executable, str(recipe)], output),
                                 ([sys.executable, "-m", "genro_typst", str(recipe)], reference)):
        result = subprocess.run([*command, f"--{mode}", "-o", str(destination)],
                                capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
    assert (tmp_path / "loads.txt").read_text() == "loaded\nloaded\n"
    if mode == "svg":
        for index in (1, 2):
            name = f"result-{index}.svg"
            assert (output.parent / name).read_bytes() == (reference.parent / name).read_bytes()
        assert not output.exists()
    elif mode == "typ":
        assert output.read_bytes() == reference.read_bytes()
    else:
        assert output.read_bytes().startswith(b"%PDF-")
        assert reference.read_bytes().startswith(b"%PDF-")


@pytest.mark.parametrize("mode", ["pdf", "svg"])
def test_direct_default_output_assets_and_custom_root(tmp_path, mode):
    recipe = tmp_path / "recipe" / "document.typ.py"
    recipe.parent.mkdir()
    recipe.write_text('''from genro_typst import TypstBuilder
class Document(TypstBuilder):
    def main(self, root):
        root.document().include(path="extra.typ")
if __name__ == "__main__":
    Document.run()
''')
    (recipe.parent / "extra.typ").write_text("Default asset root")
    for args in ([], ["--root", str(tmp_path)]):
        (tmp_path / "extra.typ").write_text("Explicit asset root")
        result = subprocess.run([sys.executable, str(recipe), f"--{mode}", *args],
                                cwd=tmp_path, capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
        assert (recipe.parent / f"document.{mode}").is_file()
        assert not (tmp_path / f"document.{mode}").exists()


def test_direct_explicit_builder_selection(tmp_path):
    recipe = tmp_path / "choice.typ.py"
    recipe.write_text('''from genro_typst import TypstBuilder
class First(TypstBuilder):
    def main(self, root):
        root.document().text("First")
class Second(TypstBuilder):
    def main(self, root):
        root.document().text("Second")
if __name__ == "__main__":
    First.run()
''')
    result = subprocess.run([sys.executable, str(recipe), "--builder", "Second"],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert '"Second"' in recipe.with_suffix("").read_text()
    result = subprocess.run([sys.executable, str(recipe), "--builder", "Missing"],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "must name a TypstBuilder" in result.stderr


@pytest.mark.parametrize("args", [["a.typ", "-o", "b.typ"], ["--pdf", "--svg"]])
def test_direct_conflicting_options_fail_without_output(monkeypatch, tmp_path, args):
    monkeypatch.setattr(sys, "argv", [str(tmp_path / "doc.typ.py")])
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as error:
        Recipe.run(args)
    assert error.value.code == 2
    assert list(tmp_path.iterdir()) == []


def test_direct_optional_compiler_error_and_legacy_pdf_destination(tmp_path):
    recipe = tmp_path / "mydoc.typ.py"
    recipe.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
    output = tmp_path / "positional.pdf"
    result = subprocess.run([sys.executable, str(recipe), str(output), "--pdf"],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert output.read_bytes().startswith(b"%PDF-")
    (tmp_path / "typst.py").write_text("raise ImportError('compiler not installed')\n")
    result = subprocess.run([sys.executable, str(recipe), "--pdf", "-o", str(output)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "genro-typst[pdf]" in result.stderr
    assert "Traceback" not in result.stderr
    assert output.read_bytes().startswith(b"%PDF-")
