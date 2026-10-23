"""Real imported components work in direct recipes, the CLI and the playground."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from genro_typst.compiler import TypstEngine

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "examples/05_reusable_blocks"
DOCUMENTS = json.loads((ROOT / "js/examples/browser/catalog.json").read_text())["documents"]


def worker(code, assets):
    result = subprocess.run(
        [sys.executable, "-m", "genro_typst.playground_worker"],
        input=json.dumps({"code": code, "assets": assets}), capture_output=True, text=True, check=True,
    )
    payload = json.loads(result.stdout)
    assert "error" not in payload, payload.get("error")
    return payload["source"]


@pytest.mark.parametrize("entry,pages", list(zip(DOCUMENTS, [3, 1])), ids=[e["id"] for e in DOCUMENTS])
def test_imported_recipe_direct_cli_and_browser_match_and_compile(entry, pages, tmp_path):
    recipe = FOLDER / f"{entry['id']}.typ.py"
    for command, name in [([sys.executable, str(recipe)], "direct.typ"),
                          ([sys.executable, "-m", "genro_typst", str(recipe)], "cli.typ")]:
        target = tmp_path / name
        subprocess.run([*command, "-o", str(target)], cwd=tmp_path, check=True, capture_output=True)
        assert target.read_text() == entry["source"]
    source = worker(entry["python"], entry["assets"])
    assert source == entry["source"]
    result = TypstEngine().compile(source, root=tmp_path, preview=True)
    assert result.pdf.startswith(b"%PDF")
    assert result.pages == len(result.svg_pages) == pages


def test_changing_one_shared_module_updates_both_documents():
    for entry in DOCUMENTS:
        assets = dict(entry["assets"])
        assets["company_blocks/chrome.py"] = assets["company_blocks/chrome.py"].replace(
            "Technical services", "Customer aftercare")
        source = worker(entry["python"], assets)
        assert "Customer aftercare" in source
        assert "Technical services" not in source


def test_data_changes_recalculate_totals_and_text_is_literal(tmp_path):
    entry = DOCUMENTS[0]
    assert "EUR 6,562.00" in entry["source"]
    assets = dict(entry["assets"])
    assets["proposal_data.py"] = assets["proposal_data.py"].replace("1850.00", "2850.00").replace(
        "Riverbank Foods", "Riverbank #panic() [Foods]")
    source = worker(entry["python"], assets)
    assert "EUR 7,562.00" in source
    assert '#"Riverbank #panic() [Foods]"' in source
    assert TypstEngine().compile(source, root=tmp_path, preview=True).pages == 3


def test_table_component_flows_across_pages(tmp_path):
    code = '''from genro_typst import TypstBuilder
from company_blocks import branded_document, item_table
class Document(TypstBuilder):
    def main(self, root):
        doc = branded_document(root, title="Long estimate", reference="LONG-001")
        item_table(doc, [dict(description=f"Component {n}", quantity=1, unit="pc", price="10.00")
                         for n in range(90)])
'''
    source = worker(code, DOCUMENTS[0]["assets"])
    assert "EUR 900.00" in source
    assert "table.header(repeat: true" in source
    assert TypstEngine().compile(source, root=tmp_path, preview=True).pages > 1
