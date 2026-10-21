# genro-typst

A standalone Python builder for print documents, using `genro-builders` and
`genro-bag` to generate Typst source and PDF. Licensed under Apache 2.0.

The library owns the Typst grammar, renderer and compilation API. It has no
dependency on Genro PDF Builder, HTML/WeasyPrint, Kajenn, Gramlot or an editor.
The separate **Genro PDF Builder** application depends on this library and
provides the visual/Python editor, previews and MCP tools.

## Install

Python 3.10+ is supported. Source generation only needs the base dependencies;
PDF compilation and SVG previews require the `pdf` extra.

```bash
python -m pip install -e ".[pdf]"
```

## A document from Python

```python
from genro_typst import TypstBuilder

class Invoice(TypstBuilder):
    def setup(self, data):
        data["customer.name"] = "Rossi & Figli"

    def main(self, root):
        doc = root.document(paper="a4", margin="15mm")
        doc.paragraph(content="Invoice")
        row = doc.layout(border_width="0.5pt").row()
        row.cell(content="Softwell S.r.l.", lbl="From")
        row.cell(content="^customer.name", lbl="Customer")
        doc.pageNumber(template="Page {page} of {total}")

invoice = Invoice()
invoice.create()
source = invoice.render()                     # Typst source string
invoice.render(target="invoice.typ")
invoice.render(mode="pdf", target="invoice.pdf")
```

`render(mode="pdf")` returns bytes when no target is supplied. It also accepts
a writable binary stream. The PDF engine is Typst; HTML uses a separate builder
in the application, with its own grammar.

## Grammar and data

The grammar now includes **129 native Typst calls**, covering text and styles,
document structure, layout, native tables, graphics, mathematics and references.
It also includes explicit set/show rules, scopes, contextual evaluation,
imports, includes, bindings and access to custom functions and trusted code.
The original `document`, `layout`, `row`, `cell`, `table`, `column`, `paragraph`
and `pageNumber` elements remain compatible.

Start with the [Italian guide](docs/typst-guide.md), the generated
[native API reference](docs/native-reference.md) and the
[machine-readable catalog](docs/native-catalog.json). The catalog targets Typst
0.15.0. Native keyword parameters are forwarded to Typst for validation; this
is not a Python reimplementation of the entire Typst type system.

Every registered native call has an [executable Python example](docs/catalog-examples.md)
and a handwritten Typst reference. Tests compile both, compare every SVG page,
check PDF output, TYTX round trips and expected errors. See the
[verification contract and limits](docs/verification.md).

Legacy signatures in [`typst_elements.py`](src/genro_typst/typst_elements.py)
define their attributes and defaults. Native registration and call conventions
are defined in `native_elements.py` and `native_catalog.py`.

Data lives in a `Bag`; `^path` attributes refer to that data. Python loops and
helper methods can generate any number of elements. Tables support columns,
headers and totals. Text is emitted as Typst string literals, preserving markup
characters in business data. SourceBag TYTX serialization is covered by tests.

Examples with Python, generated Typst and PDF:

- [Invoice header](examples/01_invoice_header/invoice_header.py): layout, cells,
  bound data and page numbering.
- [Invoice lines](examples/02_invoice_lines/invoice_lines.py): table columns and
  totals.

The original design proposal is retained in
[`xmldocs/proposal/typst-backend.md`](xmldocs/proposal/typst-backend.md).

The [native report](examples/03_native_report/report.py) demonstrates styles,
inline content, tables with spans, SVG figures, equations, links and references.
Run `python examples/03_native_report/report.py` to regenerate its Typst, PDF
and SVG preview. Use `length("12pt")`, `color("navy")`, `label("intro")`,
`expr("center + horizon")` and `markup("*Caption*")` for explicit Typst values;
ordinary strings always remain literal text.

## Compilation and previews

Applications can compile raw Typst through the same independent API:

```python
from genro_typst.compiler import TypstEngine

result = TypstEngine().compile(source, preview=True)
pdf_bytes = result.pdf
svg_pages = result.svg_pages
page_count = result.pages
```

`root=Path(...)` sets Typst's file-access root. PDF and SVG are compiled from
the same source with a shared timestamp. Without `preview=True`, no SVG pages
are generated and `pages` is `None`. Importing the library or generating source
does not import the optional Typst compiler.

## Development and repository boundary

```bash
uv venv venv --python 3.12
uv pip install --python venv/bin/python -e ".[dev]"
venv/bin/pytest -q
venv/bin/ruff check src tests
venv/bin/mypy
venv/bin/python tools/generate_reference.py --check
```

This repository contains only the library, documentation, examples and library
tests. The sibling `genro-pdf-builder` repository owns the CLI, frontend, server,
application tests and local document workspace. Its package declares
`genro-typst[pdf]>=0.0.1` as a dependency. See
[repository separation](docs/repository-separation.md) for migration details.

The Typst binding is pinned to `0.15.0`; `genro-bag>=0.28.0` and
`genro-builders>=0.29.0` provide the data and builder infrastructure.

Genro Typst is an independent Softwell project and is not affiliated with or
endorsed by Typst's authors. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
