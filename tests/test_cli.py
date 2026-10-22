# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Public recipe CLI: real compilation, builder selection and filesystem behavior."""

import builtins
import os
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest

from genro_typst.cli import generate, main

RECIPE = '''from genro_typst import TypstBuilder
class Document(TypstBuilder):
    def main(self, root):
        doc = root.document()
        doc.heading("Café — 日本語", level=1)
        {extra}

if __name__ == "__main__":
    Document.run()
'''


@pytest.fixture
def recipe(tmp_path):
    directory = tmp_path / "recipe folder"
    directory.mkdir()
    path = directory / "mydoc.typ.py"
    path.write_text(RECIPE.format(extra="pass"), encoding="utf-8")
    return path


@pytest.mark.parametrize("mode", ["typ", "pdf", "svg"])
def test_real_output_default_path(recipe, tmp_path, monkeypatch, mode):
    monkeypatch.chdir(tmp_path)
    paths = generate(recipe, output_format=mode)
    assert paths == [recipe.parent / f"mydoc.{mode}"]
    content = paths[0].read_bytes()
    if mode == "typ":
        assert 'Café — 日本語' in content.decode("utf-8")
    elif mode == "pdf":
        assert content.startswith(b"%PDF-")
    else:
        assert ElementTree.fromstring(content).tag.endswith("svg")
    assert sorted(p.name for p in recipe.parent.iterdir()) == [f"mydoc.{mode}", "mydoc.typ.py"]


@pytest.mark.parametrize("mode", ["typ", "pdf", "svg"])
def test_explicit_output_and_direct_execution_compatibility(recipe, tmp_path, mode):
    output = tmp_path / "new folder" / f"chosen.{mode}"
    result = subprocess.run(
        [sys.executable, "-m", "genro_typst", str(recipe), f"--{mode}", "-o", str(output)],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == str(output)
    assert output.is_file()
    assert not (recipe.parent / "mydoc.typ").exists()  # Main guard was not executed.
    if mode == "typ":
        direct = subprocess.run([sys.executable, str(recipe)], capture_output=True, check=False)
        assert direct.returncode == 0, direct.stderr
        assert recipe.with_suffix("").read_bytes() == output.read_bytes()


def test_svg_multipage_names_and_root_for_assets(recipe, tmp_path, monkeypatch):
    (recipe.parent / "image.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">'
        '<circle cx="10" cy="10" r="5"/></svg>'
    )
    (recipe.parent / "extra.typ").write_text("Included text")
    recipe.write_text(RECIPE.format(extra='doc.image("image.svg"); doc.pagebreak(); '
                                   'doc.include(path="extra.typ")'))
    monkeypatch.chdir(tmp_path)
    paths = generate(recipe, output_format="svg", output=Path("out/pages.svg"))
    assert paths == [Path("out/pages-1.svg"), Path("out/pages-2.svg")]
    for path in paths:
        assert ElementTree.fromstring(path.read_bytes()).tag.endswith("svg")
    assert not Path("out/pages.svg").exists()
    assert not list(tmp_path.rglob("*.pdf"))


def test_explicit_root(recipe, tmp_path):
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "extra.typ").write_text("Custom asset root")
    recipe.write_text(RECIPE.format(extra='doc.include(path="extra.typ")'))
    assert generate(recipe, output_format="pdf", root=assets)[0].read_bytes().startswith(b"%PDF")


def test_selection_conventions(recipe):
    recipe.write_text(RECIPE.format(extra="pass") + '''
Alias = Document
class Alternative(TypstBuilder):
    def main(self, root):
        root.document().text("Alternative")
''')
    with pytest.raises(ValueError, match="one TypstBuilder"):
        generate(recipe)
    assert "Alternative" in generate(recipe, builder_name="Alternative")[0].read_text()
    recipe.write_text(recipe.read_text() + "\nBUILDER = Document\n")
    assert "Café" in generate(recipe)[0].read_text()
    assert "Alternative" in generate(recipe, builder_name="Alternative")[0].read_text()
    with pytest.raises(ValueError, match="must name"):
        generate(recipe, builder_name="Missing")


def test_imported_builder_and_sibling_imports(recipe):
    (recipe.parent / "cli_test_helper.py").write_text(
        "from genro_typst import TypstBuilder\n"
        "TITLE = 'Sibling import'\n"
        "class External(TypstBuilder):\n"
        "    def main(self, root):\n"
        "        root.document().text(TITLE)\n"
    )
    recipe.write_text("from cli_test_helper import External\n")
    with pytest.raises(ValueError, match="one TypstBuilder"):
        generate(recipe)
    assert "Sibling import" in generate(recipe, builder_name="External")[0].read_text()
    recipe.write_text(RECIPE.format(extra="from cli_test_helper import TITLE; doc.text(TITLE)"))
    assert "Sibling import" in generate(recipe)[0].read_text()


@pytest.mark.parametrize("body", ["BUILDER = 42", "from genro_typst import TypstBuilder",
                                  "raise RuntimeError('recipe failed')"])
def test_invalid_recipes_return_errors_without_files(recipe, capsys, body):
    recipe.write_text(body)
    old_path, old_argv = sys.path[:], sys.argv
    assert main([str(recipe)]) == 1
    assert "genro-typst:" in capsys.readouterr().err
    assert not recipe.with_suffix("").exists()
    assert sys.path == old_path and sys.argv is old_argv


def test_no_compiler_needed_for_source_and_clear_optional_dependency_error(recipe, monkeypatch):
    original_import = builtins.__import__

    def without_typst(name, *args, **kwargs):
        if name == "typst":
            raise ImportError("not installed")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_typst)
    assert generate(recipe)[0].is_file()
    with pytest.raises(RuntimeError, match=r"genro-typst\[pdf\]"):
        generate(recipe, output_format="pdf")
    with pytest.raises(RuntimeError, match=r"genro-typst\[pdf\]"):
        generate(recipe, output_format="svg")


@pytest.mark.parametrize("alias", ["same", "symlink", "hardlink", "svg-page"])
def test_recipe_cannot_be_overwritten(recipe, tmp_path, alias):
    recipe.write_text(RECIPE.format(extra="doc.pagebreak(); doc.text('Second page')"))
    original = recipe.read_bytes()
    output = recipe
    mode = "typ"
    if alias != "same":
        output = tmp_path / "output.typ"
        if alias == "symlink":
            output.symlink_to(recipe)
        elif alias == "hardlink":
            os.link(recipe, output)
        else:
            mode = "svg"
            output = tmp_path / "output.svg"
            (tmp_path / "output-2.svg").symlink_to(recipe)
    with pytest.raises(ValueError, match="overwrite"):
        generate(recipe, output_format=mode, output=output)
    assert recipe.read_bytes() == original
    assert not (tmp_path / "output-1.svg").exists()


def test_compilation_failure_preserves_existing_output(recipe, tmp_path, capsys):
    recipe.write_text(RECIPE.format(extra='doc.typst_code(code="not valid typst!")'))
    output = tmp_path / "old.pdf"
    output.write_bytes(b"old output")
    assert main([str(recipe), "--pdf", "-o", str(output)]) == 1
    assert capsys.readouterr().err.startswith("genro-typst:")
    assert output.read_bytes() == b"old output"


@pytest.mark.parametrize("argv,code", [([], 2), (["--help"], 0),
                                      (["missing.py", "--pdf", "--svg"], 2)])
def test_argument_errors_and_help(argv, code):
    with pytest.raises(SystemExit) as error:
        main(argv)
    assert error.value.code == code


def test_bad_paths(recipe, tmp_path, capsys):
    assert main([str(tmp_path / "missing.py")]) == 1
    assert main([str(recipe), "-o", str(tmp_path)]) == 1
    assert main([str(recipe), "--pdf", "--root", str(tmp_path / "missing")]) == 1
    assert "genro-typst:" in capsys.readouterr().err


def test_installed_console_command(recipe, tmp_path):
    executable = shutil.which("genro-typst", path=str(Path(sys.executable).parent))
    assert executable is not None, "Install the package to register the console entry point"
    output = tmp_path / "console.typ"
    result = subprocess.run([executable, str(recipe), "-o", str(output)],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert "Café" in output.read_text(encoding="utf-8")
