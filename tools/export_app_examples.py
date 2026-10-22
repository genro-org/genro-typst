#!/usr/bin/env python3
"""Export the verified Typst examples as a self-contained app resource.

The application ships the resulting JSON and has no runtime dependency on
this checkout, its tests, or pytest. Re-run when the catalog changes.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

from genro_typst.native_catalog import NATIVE, SPECIAL

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from native_cases import CASES, build_case, example_python

SECTIONS = {
    "text": "Text and styles",
    "model": "Document structure",
    "layout": "Page layout",
    "visualize": "Graphics and images",
    "math": "Mathematics",
    "introspection": "Metadata",
    "pdf": "PDF",
    "language": "Typst language",
    "legacy": "Genro documents and data",
}
DESCRIPTIONS = {
    "text": "Text and typography settings.",
    "underline": "Underlined text.",
    "overline": "A line above text.",
    "strike": "Struck-through text.",
    "highlight": "Highlighted text.",
    "smallcaps": "Small capitals.",
    "sub": "Subscript text.",
    "super": "Superscript text.",
    "lower": "Convert to lowercase.",
    "upper": "Convert to uppercase.",
    "raw": "Literal code and text, without interpreting markup.",
    "lorem": "Placeholder text with an editable word count.",
    "linebreak": "Line break.",
    "smartquote": "Typographic quotation marks.",
    "heading": "Headings and section levels.",
    "strong": "Bold text.",
    "emph": "Typographic emphasis.",
    "par": "Paragraph and text layout.",
    "quote": "A quotation in the document.",
    "figure": "A figure with caption and numbering.",
    "footnote": "Footnote.",
    "title": "Document title.",
    "list": "Bulleted list.",
    "enum": "Numbered list.",
    "terms": "Glossary of terms and definitions.",
    "list_item": "An item in a bulleted list.",
    "enum_item": "An item in a numbered list.",
    "terms_item": "A term and its definition.",
    "link": "A link with editable text.",
    "ref": "Reference to a labeled section.",
    "cite": "Citation from the included local bibliography.",
    "bibliography": "Bibliography with an included YAML file.",
    "numbering": "Numbering format.",
    "outline": "Section outline.",
    "parbreak": "Paragraph break.",
    "divider": "Document divider.",
    "native_table": "Native Typst table with explicit cells.",
    "align": "Content alignment.",
    "block": "Block with padding.",
    "box": "Inline box with a fixed width.",
    "columns": "Text in multiple columns.",
    "hide": "Invisible content that preserves its space.",
    "move": "Move content.",
    "pad": "Padding.",
    "page": "A page with a different format.",
    "place": "Position content relative to the page.",
    "repeat": "Repeated content.",
    "rotate": "Rotation.",
    "scale": "Scaling.",
    "skew": "Skewing.",
    "grid": "Content grid.",
    "stack": "A sequence of blocks with direction and spacing.",
    "pagebreak": "Page break: inspect both pages in the preview.",
    "colbreak": "Column break inside a columns container.",
    "h": "Horizontal space.",
    "v": "Vertical space.",
    "measure": "Contextual content measurement; the result is a dictionary.",
    "native_layout": "A callback receiving the available dimensions.",
    "circle": "Circle with content.",
    "ellipse": "Ellipse with content.",
    "rect": "Filled rectangle.",
    "square": "Square with content.",
    "image": "An included local SVG image.",
    "line": "Line between two points.",
    "polygon": "Polygon with vertices and fill.",
    "curve": "A curve built from segments.",
    "metadata": "Invisible data embedded in the document.",
    "pdf_artifact": "Decorative content marked as a PDF artifact.",
}
for family in ("table", "grid"):
    for part, meaning in {
        "header": "Header",
        "footer": "Footer, after body cells",
        "cell": "Cell spanning multiple columns",
        "hline": "Horizontal line",
        "vline": "Vertical line",
    }.items():
        DESCRIPTIONS[f"{family}_{part}"] = (
            f"{meaning} in the native {family}."
        )
for name, meaning in {
    "move": "Move the starting point",
    "line": "Straight segment",
    "quad": "Quadratic curve",
    "cubic": "Cubic curve",
    "close": "Close the path",
}.items():
    DESCRIPTIONS[f"curve_{name}"] = meaning + " inside curve."

LANGUAGE = {
    "call": (
        "Call a Typst or imported function.",
        'doc.call(function="strong", content="Customizable function")',
    ),
    "set_rule": (
        "Style rule for subsequent elements.",
        'doc.set_rule(target="text", fill=color("blue"))\ndoc.text("This text is blue")',
    ),
    "show_rule": (
        "Transform or style selected elements.",
        'doc.show_rule(selector="heading", target="text", fill=color("blue"))\ndoc.heading("Transformed heading")',
    ),
    "scope": (
        "Styles local to a container.",
        'scope = doc.scope()\nscope.set_rule(target="text", fill=color("blue"))\nscope.text("Local style")\ndoc.text("Outer style")',
    ),
    "context": (
        "Values requiring page context.",
        'doc.context().text(content=expr("counter(page).display()"))',
    ),
    "equation": (
        "Formula written in Typst math syntax.",
        'doc.equation(formula="sum_(i=1)^n i = (n (n+1))/2", numbering="(1)")',
    ),
    "label": (
        "Label and reference to a section.",
        'doc.set_rule(target="heading", numbering="1.")\ndoc.heading("Example section")\ndoc.typst_label(name="example")\ndoc.ref(label("example"))',
    ),
    "let": (
        "Typst variable used by subsequent elements.",
        'doc.let(name="message", value="Hello from a Typst variable")\ndoc.text(content=expr("message"))',
    ),
    "import_module": (
        "Import a function from helper.typ, included in this example.",
        'doc.import_module(path="helper.typ", names=["greeting"])\ndoc.call(function="greeting", args=["Reader"], mode="value")',
    ),
    "include": (
        "Include extra.typ, provided with this example.",
        'doc.include(path="extra.typ")',
    ),
    "typst_code": (
        "Typst code block with local variables.",
        "doc.typst_code(code='let name = \"Reader\"; [Hello #name]')",
    ),
    "typst_markup": (
        "Typst markup inside a Python recipe.",
        'doc.typst_markup(source="*Bold*, _emphasis_ and $x^2$. // final comment")',
    ),
}
LEGACY = {
    "document": (
        "Page settings and document metadata.",
        'doc = root.document(paper="a5", margin="12mm", metadata={"title": "Example document"})\ndoc.paragraph(content="Edit the page format and margins.")',
    ),
    "layout": (
        "Genro container with rows and cells.",
        'doc = root.document()\nlayout = doc.layout(border_width="0.5pt")\nfor name in ("First row", "Second row"):\n    row = layout.row()\n    row.cell(content=name)\n    row.cell(content="Value", width="40mm")',
    ),
    "row": (
        "Rows with configurable height and borders.",
        'doc = root.document()\nlayout = doc.layout(border_width="0.5pt")\nlayout.row(height="18mm").cell(content="An 18 mm tall row")\nlayout.row().cell(content="Automatic height")',
    ),
    "cell": (
        "Cells with labels, widths and native content.",
        'doc = root.document()\nrow = doc.layout(border_width="0.5pt").row()\nrow.cell(content="Customer", lbl="Customer details", width=2)\nrow.cell(lbl="Native content", background="#eeeeee").strong("Bold")',
    ),
    "paragraph": (
        "Genro paragraph with data binding.",
        'doc = root.document()\ndoc.paragraph(content="^customer.name")\ndoc.paragraph().strong("Native content in a paragraph")',
    ),
    "pageNumber": (
        "Automatically updated current and total page numbers.",
        'doc = root.document()\nfor index in range(2):\n    if index:\n        doc.pagebreak()\n    doc.paragraph(content=f"Test page {index + 1}")\n    doc.pageNumber(template="Page {page} of {total}")',
    ),
    "table": (
        "Table from Bag data, with headers and totals.",
        'doc = root.document()\ntable = doc.table(data="^lines", totalize_footer="Total")\ntable.column(field="description", name="Description", width=3)\ntable.column(field="quantity", name="Quantity", totalize=True)\ntable.column(field="amount", name="Amount", totalize=True)',
    ),
    "column": (
        "Data table columns: width, alignment and totals.",
        'doc = root.document()\ntable = doc.table(data="^lines", totalize_footer="Total")\ntable.column(field="description", name="Description", width="80mm")\ntable.column(field="quantity", name="Quantity", align="right")\ntable.column(field="amount", name="Amount", align="right", totalize=True)',
    ),
}
ASSETS = {
    "logo.svg": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><circle cx="10" cy="10" r="8" fill="blue"/></svg>',
    "refs.yml": "manual:\n  type: Book\n  title: Test manual\n  author: Example, Alice\n  date: 2026\n",
    "helper.typ": "#let greeting(name) = [Hello #name]",
    "extra.typ": "= Included content\nThis text comes from extra.typ.\n",
}


def recipe(body: str, description: str, setup: str = "") -> str:
    imports = "from genro_typst import TypstBuilder, expr, length, color, label, markup\nfrom genro_bag import Bag\n"
    code = imports + "\n\nclass Document(TypstBuilder):\n"
    if setup:
        code += "    def setup(self, data):\n" + textwrap.indent(setup, "        ") + "\n\n"
    code += "    def main(self, root):\n"
    code += (
        textwrap.indent(
            "# "
            + description
            + "\n# Edit the recipe: the preview updates automatically.\n"
            + body,
            "        ",
        )
        + "\n"
    )
    return code


def catalog() -> dict:
    entries = []
    for tag, (function, _mode, section) in NATIVE.items():
        case = CASES[tag]
        builder, _, reference = build_case(case)
        body = (
            example_python(builder)
            .split("builder = TypstBuilder()\n", 1)[1]
            .rsplit("\n\nsource = builder.render()", 1)[0]
            .replace("builder.source", "root")
        )
        description = DESCRIPTIONS.get(tag, f"Math function {function}, inside an equation.")
        files = {"image": ["logo.svg"], "cite": ["refs.yml"], "bibliography": ["refs.yml"]}.get(
            tag, []
        )
        entries.append(
            {
                "id": tag,
                "title": function,
                "section": section,
                "description": description,
                "code": recipe(body, description),
                "reference": reference,
                "assets": {name: ASSETS[name] for name in files},
            }
        )
    assert set(LANGUAGE) == set(SPECIAL)
    for tag, (description, body) in LANGUAGE.items():
        files = {"import_module": ["helper.typ"], "include": ["extra.typ"]}.get(tag, [])
        entries.append(
            {
                "id": tag,
                "title": tag,
                "section": "language",
                "description": description,
                "code": recipe("doc = root.document()\n" + body, description),
                "reference": "",
                "assets": {name: ASSETS[name] for name in files},
            }
        )
    setup = """data["customer.name"] = "Rossi & Figli"
lines = Bag()
for index, (description, quantity, amount) in enumerate([
    ("Analysis", 2, 240), ("Template", 3, 150),
]):
    row = Bag()
    row["description"] = description
    row["quantity"] = quantity
    row["amount"] = amount
    lines[f"r{index}"] = row
data["lines"] = lines"""
    for tag, (description, body) in LEGACY.items():
        entries.append(
            {
                "id": tag,
                "title": tag,
                "section": "legacy",
                "description": description,
                "code": recipe(
                    body, description, setup if tag in ("table", "column", "paragraph") else ""
                ),
                "reference": "",
                "assets": {},
            }
        )
    return {"typst_version": "0.15.0", "sections": SECTIONS, "examples": entries}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    exported = catalog()
    content = json.dumps(exported, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != content:
            raise SystemExit("The app catalog is out of date: regenerate it with this tool.")
        print(f"Verified {len(exported['examples'])} packaged examples.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
        print(f"Exported {len(exported['examples'])} examples to {args.output}")
