#!/usr/bin/env python3
# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Generate Python-oracle cases for the JavaScript renderer; requires the dev extra."""

import argparse
import json
import sys
from pathlib import Path

from genro_bag import Bag
from genro_builders import SourceBag

from genro_typst import TypstBuilder, expr, length, markup
from genro_typst.native_catalog import NATIVE, SPECIAL
from genro_typst.values import value_code

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from native_cases import CASES, build_case
from test_language_compilation import LANGUAGE_CASES


def encode(value):
    if isinstance(value, Bag):
        return {"$bag": [[node.label, encode(node.value)] for node in value]}
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def tree(source):
    return [
        {
            "tag": node.node_tag,
            "attrs": encode(dict(node.attr)),
            "value": None if isinstance(node.value, SourceBag) else encode(node.value),
            "children": tree(node.value) if isinstance(node.value, SourceBag) else [],
        }
        for node in source
    ]


def cases():
    result = []

    def add(name, builder):
        item = {"name": name, "data": encode(builder.data), "tree": tree(builder.source)}
        try:
            item["source"] = builder.render()
        except (TypeError, ValueError) as error:
            item["error"] = str(error)
        result.append(item)

    assert set(CASES) == set(NATIVE)
    for tag, case in CASES.items():
        add("native/" + tag, build_case(case)[0])
    assert set(LANGUAGE_CASES) == set(SPECIAL)
    for tag, (attrs, _) in LANGUAGE_CASES.items():
        b = TypstBuilder()
        doc = b.source.document()
        doc.heading("Target")
        node = getattr(doc, "typst_" + tag)(**attrs)
        if tag in ("scope", "context"):
            node.text("Nested")
        doc.text("Following")
        add("language/" + tag, b)

    for mode in ("body", "items", "args", "value", "leaf"):
        b = TypstBuilder()
        node = b.source.document().call(function="example", mode=mode)
        if mode != "leaf":
            node.text("Child")
        add("call-mode/" + mode, b)

    b = TypstBuilder()
    b.data["title"] = "Bound Café — 日本語"
    rows = Bag()
    for index, (name, quantity) in enumerate((("A", 2), ("B", None), ("C", 5))):
        row = Bag()
        row["name"], row["qty"] = name, quantity
        rows[f"r{index}"] = row
    b.data["rows"] = rows
    doc = b.source.document(metadata={"title": "Report", "author": ["Softwell"]},
                            page_options={"numbering": "1 / 1", "footer": markup("Footer")})
    doc.paragraph(content="^title").strong(" appended")
    layout = doc.layout(border_width="0.5pt", inset="2mm")
    row = layout.row(height="12mm")
    row.cell(content="^title", lbl="Label", background="#eee", align="center", valign="middle")
    row.cell(content="Right", width="40mm", cell_border=False)
    row.cell(content="End", width=2)
    layout.row(row_border=False).cell().pageNumber(template="{page} of {total} {page}")
    layout.row().cell().text("End")
    table = doc.table(data="^rows", totalize_footer="Total")
    table.column(field="name", name="Name")
    table.column(field="qty", name="Quantity", totalize=True, align="right", width=2)
    add("legacy/all-with-binding", b)

    b = TypstBuilder()
    doc = b.source.document()
    doc.layout().row()  # Empty rows and borderless layout.
    doc.paragraph(content="Simple")
    doc.pageNumber(template="")
    local = doc.scope()
    local.set_rule(target="text", size=length("10pt"))
    local.show_rule(selector=expr("heading.where(level: 1)"), transform=expr("it => strong(it)"))
    local.let(name="x", value={"nested": [None, True, 3, 1.25]})
    local.import_module(path="helper.typ", names=["helper"])
    local.text('Quotes " slash \\ newline\n tab\t # $ <tag>')
    local.link("https://typst.app").strong("Typst")
    doc.import_module(path="helper.typ", names=["*"])
    add("language/nested-rules-and-escaping", b)

    invalid = [
        ("call", {"function": 'text); panic("oops")'}),
        ("call", {"function": "text", "mode": "invalid"}),
        ("show_rule", {"selector": "heading"}),
        ("show_rule", {"selector": "heading", "target": "text", "transform": expr("it => it")}),
        ("show_rule", {"selector": "heading", "transform": expr("it => it"), "fill": expr("red")}),
        ("let", {"name": "a.b", "value": 1}),
        ("import_module", {"path": "helper.typ", "alias": "a.b"}),
        ("import_module", {"path": "helper.typ", "names": ["a.b"]}),
        ("text", {"options": {"size": 12}, "size": 10}),
        ("text", {"options": {"font-size": 12}, "font_size": 10}),
        ("text", {"content": {"$typst": "red", "other": 1}}),
        ("text", {"content": {"$typst": ""}}),
        ("text", {"options": {"a.b": 1}}),
    ]
    for tag, (_, mode, _) in NATIVE.items():
        if mode == "leaf":
            invalid.append((tag, {"content": "Unexpected body"}))
    for index, (tag, attrs) in enumerate(invalid):
        b = TypstBuilder()
        getattr(b.source.document(), "typst_" + tag)(**attrs)
        add(f"invalid/{index}-{tag}", b)
        assert "error" in result[-1]
    for mode in ("items", "args"):
        b = TypstBuilder()
        b.source.document().call(function="example", mode=mode).set_rule(target="text", size=12)
        add("invalid/rule-in-" + mode, b)

    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    values = [None, False, True, "", [], {}, 0, 42, 1.25, 1e-7,
              '"\\\n\r\t\x00\x1b\u2028\u2029', "Café 漢字 €", [1, "a", None],
              {"left": length("2mm"), "value": [False, 1.5]}, markup("Text // comment")]
    data = {"cases": cases(), "values": [{"value": v, "source": value_code(v)} for v in values]}
    content = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    target = ROOT / "js/tests/python-fixtures.json"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            parser.exit(1, "Run python tools/export_js_fixtures.py to update Python equivalence fixtures.\n")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
