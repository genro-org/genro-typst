"""Language constructs, parameter boundaries and legacy integration."""

import pytest
import typst
from genro_bag import Bag

from genro_typst import TypstBuilder, color, expr, length, markup
from genro_typst.compiler import TypstEngine
from genro_typst.native_catalog import NATIVE, SPECIAL
from genro_typst.values import value_code
from test_catalog_compilation import restore

LANGUAGE_CASES = {
    "call": ({"function": "strong", "content": "Value"}, 'strong("Value")'),
    "set_rule": ({"target": "text", "fill": color("blue")}, "set text(fill: blue)"),
    "show_rule": (
        {"selector": "text", "target": "text", "fill": color("blue")},
        "show text: set text(fill: blue)",
    ),
    "scope": ({}, '[#text("Nested")]'),
    "context": ({}, 'context [#text("Nested")]'),
    "equation": (
        {"formula": "x^2 + y^2", "block": True},
        "math.equation(block: true, $x^2 + y^2$)",
    ),
    "label": ({"name": "target"}, 'label("target")'),
    "let": ({"name": "message", "value": "Bound"}, 'let message = "Bound"'),
    "import_module": ({"path": "helper.typ", "alias": "helper"}, 'import "helper.typ" as helper'),
    "include": ({"path": "extra.typ"}, 'include "extra.typ"'),
    "typst_code": (
        {"code": 'let name = "Code"; strong(name)'},
        '{let name = "Code"; strong(name)\n}',
    ),
    "typst_markup": ({"source": "*Markup* // final comment"}, "[*Markup* // final comment\n]"),
}


def test_language_cases_cover_all_constructs():
    assert set(LANGUAGE_CASES) == set(SPECIAL)


@pytest.mark.parametrize("tag", LANGUAGE_CASES)
def test_language_pdf_svg_and_roundtrip(tag, tmp_path):
    (tmp_path / "helper.typ").write_text("#let greeting(name) = [Hello #name]")
    (tmp_path / "extra.typ").write_text("Included")
    builder = TypstBuilder()
    doc = builder.source.document()
    doc.heading("Target")
    attrs, expected = LANGUAGE_CASES[tag]
    node = getattr(doc, "typst_" + tag)(**attrs)
    if tag in ("scope", "context"):
        node.text("Nested")
    tail = 'text("Following")'
    if tag == "let":
        doc.text(content=expr("message"))
        tail = "text(message)"
    elif tag == "import_module":
        doc.call(function="helper.greeting", mode="value", args=["Reader"])
        tail = 'helper.greeting("Reader")'
    else:
        doc.text("Following")
    source = builder.render()
    assert builder.validate_source() == []
    assert restore(builder).render() == source
    compiled = TypstEngine().compile(source, root=tmp_path, preview=True)
    reference = '#set page(paper: "a4", flipped: false, margin: 15mm)\n#heading("Target")\n'
    reference += f"#{expected}\n#{tail}\n"
    expected_svg = typst.compile(reference.encode(), root=str(tmp_path), format="svg")
    if isinstance(expected_svg, bytes):
        expected_svg = [expected_svg]
    assert compiled.pdf.startswith(b"%PDF")
    assert compiled.svg_pages == tuple(expected_svg)


@pytest.mark.parametrize(
    "names,alias", [(["greeting"], None), (["*"], None), (None, "helper"), (["greeting"], "helper")]
)
def test_import_variants(names, alias, tmp_path):
    (tmp_path / "helper.typ").write_text("#let greeting() = [Hello]")
    b = TypstBuilder()
    doc = b.source.document()
    doc.import_module(path="helper.typ", names=names, alias=alias)
    doc.call(function="greeting" if names else "helper.greeting", mode="args")
    assert TypstEngine().compile(b.render(), root=tmp_path).pdf.startswith(b"%PDF")


@pytest.mark.parametrize("mode", ["body", "items", "args", "value", "leaf"])
def test_generic_call_modes(mode):
    b = TypstBuilder()
    doc = b.source.document()
    if mode == "leaf":
        doc.call(function="linebreak", mode=mode)
    elif mode in ("items", "args"):
        doc.call(function="stack", mode=mode).text("Item")
    elif mode == "value":
        doc.call(function="link", mode=mode, content="https://typst.app").text("Website")
    else:
        doc.call(function="strong", mode=mode, content="Text").emph(" nested")
    assert TypstEngine().compile(b.render(), preview=True).pages == 1


@pytest.mark.parametrize(
    "attrs,message",
    [
        ({"options": []}, "options must"),
        ({"options": False}, "options must"),
        ({"options": ""}, "options must"),
        ({"args": {}}, "args must"),
        ({"args": False}, "args must"),
        ({"args": ""}, "args must"),
        ({"options": {"size": length("12pt")}, "size": length("10pt")}, "Duplicate"),
        ({"options": {"font-size": 12}, "font_size": 10}, "Duplicate"),
    ],
)
def test_malformed_call_containers_fail_without_silent_loss(attrs, message):
    b = TypstBuilder()
    node = b.source.document().text("Text")
    # Simulate malformed persisted or programmatically updated attributes.
    node.attr.update(attrs)
    with pytest.raises((TypeError, ValueError), match=message):
        b.render()


@pytest.mark.parametrize("tag", [tag for tag, (_, mode, _) in NATIVE.items() if mode == "leaf"])
def test_leaf_calls_reject_content(tag):
    b = TypstBuilder()
    getattr(b.source.document(), "typst_" + tag)(content="Unexpected body")
    with pytest.raises(ValueError, match="does not accept child content"):
        b.render()


@pytest.mark.parametrize("family", ["native_table", "grid"])
def test_footer_must_be_last_in_native_table_or_grid(family):
    b = TypstBuilder()
    table = getattr(b.source.document(), family)(columns=1)
    tag = "table_footer" if family == "native_table" else "grid_footer"
    getattr(table, tag)().text("Footer")
    table.text("Too late")
    with pytest.raises(typst.TypstError, match="footer must end at the last row"):
        TypstEngine().compile(b.render())


@pytest.mark.parametrize(
    "tag,attrs,message",
    [
        ("call", {"function": 'text); panic("oops")', "content": "x"}, "identifier"),
        (
            "show_rule",
            {"selector": "heading", "target": "text", "transform": expr("it => it")},
            "either",
        ),
        ("show_rule", {"selector": "heading"}, "requires transform"),
        (
            "show_rule",
            {"selector": "heading", "transform": expr("it => it"), "fill": color("red")},
            "requires transform",
        ),
        ("let", {"name": "a.b", "value": 1}, "simple name"),
        ("import_module", {"path": "helper.typ", "alias": "a.b"}, "simple name"),
        ("import_module", {"path": "helper.typ", "names": ["a.b"]}, "simple name"),
    ],
)
def test_invalid_language_constructs_are_rejected(tag, attrs, message):
    b = TypstBuilder()
    getattr(b.source.document(), "typst_" + tag)(**attrs)
    with pytest.raises(ValueError, match=message):
        b.render()


def test_markup_ending_in_line_comment_keeps_closing_delimiter():
    b = TypstBuilder()
    b.source.document().text(content=markup("Visible // final comment"))
    assert TypstEngine().compile(b.render(), preview=True).pages == 1


@pytest.mark.parametrize(
    "value",
    [0, False, "", [], {}, None, 1e-7, -1e20, "\x00\x1b\u2028\u2029", '"\\\n\t', "caffè 漢字 €"],
)
def test_literal_values_retain_type_and_value(value):
    # Typst's JSON parser is an independent value oracle (including Unicode/controls).
    import json

    encoded = value_code(value)
    json_literal = value_code(json.dumps(value, ensure_ascii=True))
    source = f"#assert.eq({encoded}, json(bytes({json_literal})))"
    assert typst.compile(source.encode()).startswith(b"%PDF")


def test_all_legacy_elements_with_native_children_and_bound_data():
    b = TypstBuilder()
    b.data["title"] = "Bound title"
    rows = Bag()
    row = Bag()
    row["name"], row["qty"] = "Example", 2
    rows["r1"] = row
    b.data["rows"] = rows
    doc = b.source.document()
    doc.paragraph(content="^title")
    layout = doc.layout(border_width="0.5pt")
    layout.row().cell(lbl="Native child").strong("Inside cell")
    layout.row().cell().pageNumber()
    table = doc.table(data="^rows", totalize_footer="Total")
    table.column(field="name", name="Name")
    table.column(field="qty", name="Quantity", totalize=True)
    source = b.render()
    assert "Bound title" in source and "Inside cell" in source
    restored = restore(b)
    restored.data = b.data
    assert restored.render() == source
    assert b.validate_source() == []
    result = TypstEngine().compile(source, preview=True)
    assert result.pdf.startswith(b"%PDF") and result.pages == 1


@pytest.mark.parametrize("tag", LANGUAGE_CASES)
def test_language_constructs_reject_unknown_parameters(tag):
    b = TypstBuilder()
    attrs, _reference = LANGUAGE_CASES[tag]
    with pytest.raises((ValueError, typst.TypstError), match="does not accept|unexpected argument"):
        getattr(b.source.document(), "typst_" + tag)(**attrs, nonexistent_native_parameter=True)
        TypstEngine().compile(b.render())
