"""Compile native language features with the pinned Typst compiler."""

from __future__ import annotations

import json

import pytest
import typst
from genro_builders import SourceBag

from genro_typst import TypstBuilder, color, expr, label, length, markup
from genro_typst.native_catalog import NATIVE
from genro_typst.values import named_arguments, value_code


def document():
    builder = TypstBuilder()
    return builder, builder.source.document()


def assert_compiles(builder, root=None):
    assert builder.validate_source() == []
    source = builder.render()
    assert typst.compile(source.encode(), root=str(root) if root else None).startswith(b"%PDF")
    return source


def test_every_catalog_entry_resolves_in_pinned_typst():
    # floor/ceil are callable symbols rather than function-typed values.
    source = "\n".join(
        f"#assert(type({fn}) == {'symbol' if fn in ('math.floor', 'math.ceil') else 'function'})"
        for fn, _, _ in NATIVE.values()
    )
    assert typst.compile(source.encode()).startswith(b"%PDF")


def test_native_style_metadata_and_inline_adjacency():
    b = TypstBuilder()
    doc = b.source.document(
        metadata={"title": "A report", "author": ["Softwell"]},
        page_options={"header": markup("Report"), "numbering": "1"},
    )
    doc.set_rule(target="text", size=length("11pt"))
    doc.show_rule(selector="heading", target="text", fill=color("navy"))
    doc.heading("Introduction", level=1)
    p = doc.par(justify=True)
    p.text("alpha")
    p.strong("beta")
    p.emph(" gamma")
    source = assert_compiles(b)
    assert '#text([#"alpha"])#strong([#"beta"])' in source
    assert '#set document(title: "A report"' in source


@pytest.mark.parametrize(
    "tag,options",
    [
        ("underline", {}),
        ("overline", {}),
        ("strike", {}),
        ("highlight", {}),
        ("smallcaps", {}),
        ("sub", {}),
        ("super", {}),
        ("lower", {}),
        ("upper", {}),
        ("quote", {"block": True}),
        ("footnote", {}),
        ("title", {}),
        ("align", {"args": [expr("center")]}),
        ("block", {"inset": length("2mm")}),
        ("box", {"width": length("30mm")}),
        ("columns", {"args": [2]}),
        ("hide", {}),
        ("move", {"dx": length("2mm")}),
        ("pad", {"args": [length("2mm")]}),
        ("page", {"paper": "a5"}),
        ("place", {"args": [expr("top + right")]}),
        ("repeat", {}),
        ("rotate", {"args": [expr("10deg")]}),
        ("scale", {"x": length("120%")}),
        ("skew", {"ax": expr("10deg")}),
        ("circle", {"radius": length("10mm")}),
        ("ellipse", {"width": length("40mm")}),
        ("rect", {"fill": color("#eeeeee")}),
        ("square", {"size": length("20mm")}),
        ("pdf_artifact", {}),
    ],
)
def test_native_content_functions(tag, options):
    b, doc = document()
    getattr(doc, "typst_" + tag)(content="Native content", **options)
    assert_compiles(b)


def test_lists_grid_and_explicit_table_cells():
    b, doc = document()
    items = doc.list(tight=False)
    items.list_item("First")
    items.list_item().strong("Second")
    numbered = doc.enum(start=3)
    numbered.enum_item("Third")
    terms = doc.terms()
    terms.terms_item(args=["API", "Application programming interface"])
    grid = doc.grid(columns=[length("1fr"), length("2fr")], gutter=length("2mm"))
    grid.grid_cell("Left")
    grid.grid_cell("Right")
    table = doc.native_table(columns=[length("1fr"), length("2fr")], inset=length("2mm"))
    header = table.table_header(repeat=True)
    header.table_cell("Code").strong(" / unit")
    header.table_cell("Value")
    table.table_cell("Combined", colspan=2, fill=color("#eeeeee"))
    table.table_hline(stroke=expr("1pt + blue"))
    table.table_cell("A")
    table.table_cell("42")
    footer = table.table_footer(repeat=False)
    footer.table_cell("End", colspan=2)
    assert_compiles(b)


def test_equations_and_structured_math():
    b, doc = document()
    doc.equation(formula=r"sum_(i=1)^n i = (n (n+1))/2", numbering="(1)")
    eq = doc.math_equation(block=True)
    eq.math_frac(args=[markup("$a^2$"), markup("$b$")])
    eq.math_sqrt(args=[markup("$x$")])
    eq.math_mat(args=[["1", "2"], ["3", "4"]])
    eq.math_vec(args=["1", "2", "3"])
    eq.math_cases(args=[markup("$x & x >= 0$"), markup("$-x & x < 0$")])
    eq.math_attach(args=[markup("$x$")], t=markup("$2$"), b=markup("$i$"))
    eq.math_floor(args=[markup("$x$")])
    eq.math_ceil(args=[markup("$x$")])
    assert_compiles(b)


def test_references_bibliography_image_and_files(tmp_path):
    (tmp_path / "logo.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><circle cx="10" cy="10" r="8" fill="blue"/></svg>'
    )
    (tmp_path / "refs.yml").write_text(
        "manual:\n  type: Book\n  title: Test manual\n  author: Example, Alice\n  date: 2026\n"
    )
    (tmp_path / "extra.typ").write_text("Included content")
    (tmp_path / "helper.typ").write_text("#let greeting(name) = [Hello #name]")
    b, doc = document()
    doc.set_rule(target="heading", numbering="1.")
    doc.heading("Files", level=1)
    doc.typst_label(name="files")
    doc.ref(label("files"))
    doc.link("https://typst.app").text("Typst")
    fig = doc.figure(caption=markup("A vector image"), alt="A blue circle")
    fig.image("logo.svg", width=length("15mm"))
    doc.import_module(path="helper.typ", names=["greeting"])
    doc.call(function="greeting", mode="value", args=["Reader"])
    doc.include(path="extra.typ")
    doc.cite(label("manual"))
    doc.bibliography("refs.yml", title=markup("References"))
    assert_compiles(b, tmp_path)


def test_shapes_and_curve_segments():
    b, doc = document()
    doc.line(start=[length("0pt"), length("0pt")], end=[length("20mm"), length("5mm")])
    doc.polygon(
        args=[
            [length("0pt"), length("0pt")],
            [length("10mm"), length("0pt")],
            [length("5mm"), length("10mm")],
        ],
        fill=color("blue"),
    )
    curve = doc.curve(stroke=expr("1pt + red"))
    curve.curve_move(args=[[length("0pt"), length("0pt")]])
    curve.curve_line(args=[[length("20mm"), length("5mm")]])
    curve.curve_close()
    assert_compiles(b)


def test_scope_context_rules_and_trusted_escape_hatches():
    b, doc = document()
    scope = doc.scope()
    scope.set_rule(target="text", fill=color("blue"))
    scope.let(name="message", value="Scoped")
    scope.text(content=expr("message"))
    scope.show_rule(selector=expr('"Scoped"'), transform=expr("it => strong(it)"))
    scope.text("Scoped")
    doc.context().text(content=expr("counter(page).display()"))
    doc.typst_markup(source="*Markup* and $x^2$")
    doc.typst_code(code='let greet(name) = [Hello #name]; greet("world")')
    doc.text("Outside")
    assert_compiles(b)


def test_native_values_round_trip_and_grammar_export(tmp_path):
    b, doc = document()
    doc.heading("Round trip", level=2)
    doc.text(content="Color", fill=color("#167665"), size=length("14pt"))
    doc.set_rule(target="page", margin={"left": length("10mm"), "right": length("15mm")})
    source = SourceBag.from_tytx(b.source.to_tytx())
    restored = TypstBuilder()
    source._builder = restored
    for node in source.traverse():
        if isinstance(node.value, SourceBag):
            node.value._builder = restored
    source.set_backref()
    restored.source = source
    assert restored.render() == b.render()
    assert_compiles(restored)
    TypstBuilder.to_grammar(tmp_path / "grammar.json")
    exported = json.loads((tmp_path / "grammar.json").read_text())
    assert "heading" in json.dumps(exported)


@pytest.mark.parametrize(
    "value", [float("nan"), float("inf"), object(), {1: "bad"}, {"$typst": "x", "extra": 1}]
)
def test_invalid_values_fail_before_compiling(value):
    with pytest.raises((ValueError, TypeError)):
        value_code(value)


def test_literal_strings_are_never_guessed_as_code_and_collisions_fail():
    assert value_code("12pt") == '"12pt"'
    assert value_code('#panic("not code")') == '"#panic(\\"not code\\")"'
    assert value_code({}) == "(:)"
    assert value_code([]) == "()"
    with pytest.raises(ValueError, match="Duplicate"):
        named_arguments({"font_size": 1, "font-size": 2})
    _b, doc = document()
    with pytest.raises(ValueError, match="either positional"):
        doc.text("first", content="second")


def test_documented_catalog_matches_registered_grammar():
    from genro_typst.native_catalog import SPECIAL

    b = TypstBuilder()
    for tag in (*NATIVE, *SPECIAL):
        assert b._get_schema_info(tag) is not None
    for tag in NATIVE:
        assert b._get_schema_info(tag)["accepts_var_keyword"]


def test_positional_content_survives_nesting_and_multiple_args_are_explicit():
    b, doc = document()
    doc.heading("Before").strong(" after")
    doc.link("https://typst.app").text("Link")
    source = assert_compiles(b)
    assert 'heading([#"Before"#strong([#" after"])])' in source
    assert 'link("https://typst.app", [#text([#"Link"])])' in source
    with pytest.raises(ValueError, match="args="):
        doc.heading("one", "two")


def test_rules_in_argument_lists_and_unknown_call_mode_are_rejected():
    b, doc = document()
    doc.stack().set_rule(target="text", size=length("12pt"))
    with pytest.raises(ValueError, match="scope"):
        b.render()
    b, doc = document()
    doc.call(function="text", mode="unknown", content="X")
    with pytest.raises(ValueError, match="Unknown call mode"):
        b.render()


def test_data_bindings_and_literals_remain_distinct():
    b, doc = document()
    b.data["title"] = "A #title with *characters*"
    doc.heading(content="^title")
    source = assert_compiles(b)
    assert "A #title with *characters*" in source
    assert "^title" not in source


def test_compiler_reports_invalid_native_options_and_text_stays_literal():
    b, doc = document()
    doc.text('#panic("This is text")', size=length("12pt"))
    doc.raw('print("hello")', lang="python", block=True)
    assert_compiles(b)
    doc.text("Bad options", definitely_not_a_typst_parameter=True)
    with pytest.raises(typst.TypstError, match="unexpected argument"):
        b.render(mode="pdf")
