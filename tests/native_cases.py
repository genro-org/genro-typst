"""Explicit executable examples: adding a catalog tag requires a new case here.

The reference expressions are handwritten Typst, independent of the renderer.
Shared contexts put nested elements where Typst permits them (cells, math, etc.).
"""

from dataclasses import dataclass, field
from typing import Any

from genro_typst import TypstBuilder, color, expr, label, length, markup
from genro_typst.native_catalog import AUTHORING_ALIASES


@dataclass
class Case:
    tag: str
    reference: str
    attrs: dict[str, Any] = field(default_factory=dict)
    context: str = "document"
    children: tuple[tuple[str, dict[str, Any]], ...] = ()


CASES: dict[str, Case] = {}


def case(tag, reference, *, context="document", children=(), **attrs):
    assert tag not in CASES
    CASES[tag] = Case(tag, reference, attrs, context, children)


# Text and semantic document elements.
for tag in [
    "text",
    "underline",
    "overline",
    "strike",
    "highlight",
    "smallcaps",
    "sub",
    "super",
    "lower",
    "upper",
]:
    case(tag, f'{tag}("Example")', content="Example")
for tag in ("lower", "upper"):
    CASES[tag].reference = f"{tag}([Example])"
case("raw", 'raw("#literal <x>", lang: "typst")', content="#literal <x>", lang="typst")
case("lorem", "lorem(12)", content=12)
case("linebreak", "linebreak(justify: true)", justify=True)
case("smartquote", "smartquote(double: false)", double=False)
case("heading", 'heading(level: 2, "Heading")', content="Heading", level=2)
for tag in ["strong", "emph", "par", "quote", "footnote", "title"]:
    case(tag, f'{tag}("Example")', content="Example")
case(
    "figure",
    "figure(rect(width: 10mm, height: 5mm), caption: [Caption])",
    children=(("rect", {"width": length("10mm"), "height": length("5mm")}),),
    caption=markup("Caption"),
)
case("list", 'list("One", "Two")', args=["One", "Two"])
case("enum", 'enum(start: 3, "One", "Two")', args=["One", "Two"], start=3)
case(
    "terms",
    'terms(terms.item("API", "Interface"))',
    children=(("terms_item", {"args": ["API", "Interface"]}),),
)
case("list_item", 'list.item("Item")', content="Item", context="list")
case("enum_item", 'enum.item("Item")', content="Item", context="enum")
case("terms_item", 'terms.item("API", "Interface")', args=["API", "Interface"], context="terms")
case(
    "link",
    'link("https://typst.app", [#text("Website")])',
    content="https://typst.app",
    children=(("text", {"content": "Website"}),),
)
case("ref", 'ref(label("target"))', content=label("target"))
case("cite", 'cite(label("manual"))', content=label("manual"))
case("bibliography", 'bibliography("refs.yml", full: true)', content="refs.yml", full=True)
case("numbering", 'numbering("1.a", 2, 3)', args=["1.a", 2, 3])
case("outline", "outline(title: [Contents])", title=markup("Contents"))
case("parbreak", "parbreak()")
case("divider", "divider()")
for family in ("table", "grid"):
    for part in ("header", "footer"):
        case(
            f"{family}_{part}",
            f'{family}.{part}({family}.cell("Span", colspan: 2))',
            context=family,
            children=((f"{family}_cell", {"content": "Span", "colspan": 2}),),
        )
    case(
        f"{family}_cell",
        f'{family}.cell("Span", colspan: 2)',
        content="Span",
        colspan=2,
        context=family,
    )
    case(
        f"{family}_hline",
        f"{family}.hline(stroke: 2pt + blue)",
        stroke=expr("2pt + blue"),
        context=family,
    )
    case(
        f"{family}_vline",
        f"{family}.vline(x: 1, stroke: 2pt + blue)",
        x=1,
        stroke=expr("2pt + blue"),
        context=family,
    )
case("native_table", 'table(columns: 2, "A", "B")', columns=2, args=["A", "B"])

# Layout: spatial transforms, flow, contextual measurements.
case("align", 'align(center, "Example")', args=[expr("center")], content="Example")
case("block", 'block(inset: 2mm, "Example")', content="Example", inset=length("2mm"))
case("box", 'box(width: 30mm, "Example")', content="Example", width=length("30mm"))
case("columns", 'columns(2, "Example")', args=[2], content="Example")
case("hide", 'hide("Invisible")', content="Invisible")
case("move", 'move(dx: 2mm, "Example")', content="Example", dx=length("2mm"))
case("pad", 'pad(2mm, "Example")', args=[length("2mm")], content="Example")
case("page", 'page(paper: "a5", "Example")', content="Example", paper="a5")
case("place", 'place(top + right, "Example")', args=[expr("top + right")], content="Example")
case("repeat", 'repeat(".")', content=".")
case("rotate", 'rotate(10deg, "Example")', args=[expr("10deg")], content="Example")
case("scale", 'scale(x: 120%, "Example")', x=length("120%"), content="Example")
case("skew", 'skew(ax: 10deg, "Example")', ax=expr("10deg"), content="Example")
case("grid", 'grid(columns: 2, "A", "B")', columns=2, args=["A", "B"])
case(
    "stack",
    'stack(dir: ltr, spacing: 2mm, "A", "B")',
    dir=expr("ltr"),
    spacing=length("2mm"),
    args=["A", "B"],
)
case("pagebreak", "pagebreak()")
case("colbreak", "colbreak()", context="columns")
case("h", "h(5mm)", content=length("5mm"))
case("v", "v(5mm)", content=length("5mm"))
case("measure", 'measure("Example")', content="Example", context="measure")
case(
    "native_layout",
    "layout(size => [Width: #size.width])",
    content=expr("size => [Width: #size.width]"),
)

# Graphics and every type of curve segment.
for tag in ("circle", "ellipse", "rect", "square"):
    case(tag, f'{tag}(fill: rgb("#eeeeee"), "G")', content="G", fill=color("#eeeeee"))
case("image", 'image("logo.svg", width: 10mm)', content="logo.svg", width=length("10mm"))
p0, p1, p2, p3 = (
    [length(x), length(y)]
    for x, y in (("0pt", "0pt"), ("10mm", "0pt"), ("10mm", "10mm"), ("0pt", "10mm"))
)
case("line", "line(start: (0pt, 0pt), end: (10mm, 10mm))", start=p0, end=p2)
case(
    "polygon",
    "polygon((0pt, 0pt), (10mm, 0pt), (10mm, 10mm), fill: blue)",
    args=[p0, p1, p2],
    fill=color("blue"),
)
case(
    "curve",
    "curve(curve.move((0pt, 0pt)), curve.line((10mm, 10mm)))",
    children=(("curve_move", {"args": [p0]}), ("curve_line", {"args": [p2]})),
)
case("curve_move", "curve.move((10mm, 0pt))", args=[p1], context="curve")
case("curve_line", "curve.line((10mm, 10mm))", args=[p2], context="curve")
case("curve_quad", "curve.quad((10mm, 10mm), (10mm, 0pt))", args=[p2, p1], context="curve")
case(
    "curve_cubic",
    "curve.cubic((10mm, 10mm), (10mm, 0pt), (0pt, 10mm))",
    args=[p2, p1, p3],
    context="curve",
)
case("curve_close", "curve.close()", context="curve")

# Structured math is called in code mode, inside an equation.
case(
    "math_equation", "math.equation(block: true, [$x + y$])", content=markup("$x + y$"), block=True
)
for name in [
    "upright",
    "italic",
    "bold",
    "serif",
    "sans",
    "cal",
    "frak",
    "mono",
    "bb",
    "display",
    "inline",
    "script",
    "sscript",
]:
    case("math_" + name, f"math.{name}([$x$])", content=markup("$x$"), context="math")
for name in [
    "sqrt",
    "abs",
    "norm",
    "floor",
    "ceil",
    "round",
    "cancel",
    "underbrace",
    "overbrace",
    "underbracket",
    "overbracket",
    "underline",
    "overline",
    "underparen",
    "overparen",
    "undershell",
    "overshell",
]:
    case("math_" + name, f"math.{name}([$x$])", args=[markup("$x$")], context="math")
case("math_frac", "math.frac([$x$], [$y$])", args=[markup("$x$"), markup("$y$")], context="math")
case("math_root", 'math.root("3", [$x$])', args=["3", markup("$x$")], context="math")
case("math_binom", 'math.binom("n", "k")', args=["n", "k"], context="math")
case("math_vec", 'math.vec("1", "2")', args=["1", "2"], context="math")
case("math_mat", 'math.mat(("1", "2"), ("3", "4"))', args=[["1", "2"], ["3", "4"]], context="math")
case(
    "math_cases",
    "math.cases([$x & x >= 0$], [$-x & x < 0$])",
    args=[markup("$x & x >= 0$"), markup("$-x & x < 0$")],
    context="math",
)
case("math_lr", "math.lr([$(x)$])", args=[markup("$(x)$")], context="math")
case(
    "math_attach",
    "math.attach([$x$], t: [2], b: [i])",
    args=[markup("$x$")],
    t=markup("2"),
    b=markup("i"),
    context="math",
)
case("math_accent", 'math.accent([$x$], "^")', args=[markup("$x$"), "^"], context="math")
case(
    "math_class", 'math.class("relation", [$=$])', args=["relation", markup("$=$")], context="math"
)
case("math_op", 'math.op("custom")', args=["custom"], context="math")
for name in ("limits", "scripts"):
    case("math_" + name, f"math.{name}(sym.sum)", args=[expr("sym.sum")], context="math")
case(
    "math_stretch",
    "math.stretch(sym.arrow.r, size: 200%)",
    args=[expr("sym.arrow.r")],
    size=length("200%"),
    context="math",
)
case("math_primes", "math.primes(3)", args=[3], context="math")
case("metadata", 'metadata(("answer": 42,))', content={"answer": 42})
case("pdf_artifact", 'pdf.artifact("Decoration")', content="Decoration")


def build_case(case):
    b = TypstBuilder()
    doc = b.source.document()
    doc.text("Before")
    before = ['text("Before")']
    after = ['text("After")']
    if case.tag in ("ref", "outline"):
        doc.set_rule(target="heading", numbering="1.")
        doc.heading("Target")
        doc.typst_label(name="target")
        before += ['set heading(numbering: "1.")', 'heading("Target")', 'label("target")']
    target = doc
    ctx = case.context
    wrap = lambda s: s
    if ctx in ("list", "enum", "terms"):
        target = getattr(doc, "typst_" + ctx)()
        wrap = lambda s: f"{ctx}({s})"
    elif ctx in ("table", "grid"):
        target = getattr(doc, "native_table" if ctx == "table" else "grid")(columns=2)
        wrap = lambda s: f'{ctx}(columns: 2, {s}, text("A"), text("B"))'
    elif ctx == "columns":
        target = doc.typst_columns(args=[2])
        target.text("Left")
        wrap = lambda s: f'columns(2, [#text("Left")#{s}#text("Right")])'
    elif ctx == "curve":
        target = doc.curve()
        target.curve_move(args=[p0])
        target.curve_line(args=[p1])
        wrap = lambda s: (
            f"curve(curve.move((0pt, 0pt)), curve.line((10mm, 0pt)), {s}, curve.line((0pt, 10mm)))"
        )
    elif ctx == "math":
        target = doc.math_equation(block=True)
        wrap = lambda s: f"math.equation(block: true, [#{s}])"
    elif ctx == "measure":
        target = doc.context().call(function="repr", mode="args")
        wrap = lambda s: f"context [#repr({s})]"
    if case.tag in ("table_footer", "grid_footer"):
        target.text("A")
        target.text("B")
        wrap = lambda s: f'{ctx}(columns: 2, text("A"), text("B"), {s})'
    node = getattr(target, "typst_" + case.tag)(**case.attrs)
    for tag, attrs in case.children:
        getattr(node, "typst_" + tag)(**attrs)
    if ctx in ("table", "grid") and case.tag not in ("table_footer", "grid_footer"):
        target.text("A")
        target.text("B")
    elif ctx == "columns":
        target.text("Right")
    elif ctx == "curve":
        target.curve_line(args=[p3])
    if case.tag == "cite":
        doc.bibliography("refs.yml")
        after.insert(0, 'bibliography("refs.yml")')
    doc.text("After")
    reference = '#set page(paper: "a4", flipped: false, margin: 15mm)\n'
    reference += "\n".join("#" + s for s in [*before, wrap(case.reference), *after]) + "\n"
    return b, node, reference


def write_assets(root):
    (root / "logo.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><circle cx="10" cy="10" r="8" fill="blue"/></svg>'
    )
    (root / "refs.yml").write_text(
        "manual:\n  type: Book\n  title: Test manual\n  author: Example, Alice\n  date: 2026\n"
    )


def example_python(builder):
    """Complete recipe for the generated documentation; exercised by catalog tests."""
    from genro_builders import SourceBag

    def literal(value):
        if isinstance(value, dict):
            if set(value) == {"$typst"}:
                return f"expr({value['$typst']!r})"
            return "{" + ", ".join(f"{k!r}: {literal(v)}" for k, v in value.items()) + "}"
        if isinstance(value, list):
            return "[" + ", ".join(literal(v) for v in value) + "]"
        return repr(value)

    lines = ["from genro_typst import TypstBuilder, expr", "", "builder = TypstBuilder()"]
    sequence = 0

    def walk(bag, parent):
        nonlocal sequence
        for node in bag:
            name = "doc" if node.node_tag == "document" else f"node{sequence}"
            sequence += 1
            args = ", ".join(f"{k}={literal(v)}" for k, v in node.attr.items())
            method = AUTHORING_ALIASES.get(node.node_tag, node.node_tag)
            call = f"{parent}.{method}({args})"
            if isinstance(node.value, SourceBag):
                lines.append(f"{name} = {call}")
                walk(node.value, name)
            else:
                lines.append(call)

    walk(builder.source, "builder.source")
    lines += ["", "source = builder.render()"]
    return "\n".join(lines)
