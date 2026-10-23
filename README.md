# genro-typst

[![Documentation](https://readthedocs.org/projects/genro-typst/badge/?version=latest)](https://genro-typst.readthedocs.io/en/latest/)
[![Documentation build](https://github.com/genro-org/genro-typst/actions/workflows/docs.yml/badge.svg)](https://github.com/genro-org/genro-typst/actions/workflows/docs.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Write Typst documents in Python.** Genro Typst is a Python authoring layer
built on [genro-builders](https://github.com/genro-org/genro-builders) and
[genro-bag](https://github.com/genro-org/genro-bag). Python calls, loops and
functions produce ordinary **Typst source**, which you can read, save, edit
and compile with Typst.

## Built on Typst — with thanks to its authors

The document language, typesetting engine and PDF/SVG compilation are the work
of **[Typst](https://typst.app/)**. We gratefully acknowledge **Laurenz Mädje,
Martin Haug, the Typst team and all Typst contributors** for creating and
maintaining the technology that makes these documents possible.

Genro Typst's contribution is the Python way of writing that source: builder
methods, data binding and serialization. When you request a PDF or SVG preview,
the library delegates compilation to Typst through its Python binding.
**The typesetting quality and rendered output come from Typst.**

Explore the [Typst documentation](https://typst.app/docs/),
[compiler source](https://github.com/typst/typst),
[team](https://typst.app/about/) and [official Typst web app](https://typst.app/).
See [acknowledgements](https://genro-typst.readthedocs.io/en/latest/acknowledgements.html)
for the roles of the upstream projects. Genro Typst is an independent Softwell
project, not an official Typst product or an endorsement by its authors.

## Installation

From a repository checkout, with Python 3.10+:

```bash
git clone https://github.com/genro-org/genro-typst.git
cd genro-typst
python -m pip install -e ".[pdf]"
```

The base package generates Typst source. The `pdf` extra installs the Typst
Python binding, pinned to **0.15.0**, for compilation and previews. To generate
source without installing the compiler, use `python -m pip install -e .`.

## Quick start

Subclass `TypstBuilder`, describe the document in `main`, and call `create()`:

```python
from genro_typst import TypstBuilder


class Report(TypstBuilder):
    def main(self, root):
        doc = root.document(paper="a4", margin="15mm")
        doc.heading("Quarterly report", level=1)
        for name in ("Research", "Development", "Support"):
            doc.par(f"Department: {name}")


report = Report()
report.create()
print(report.render())                         # Readable Typst source
report.render(target="report.typ")             # Save the source
report.render(mode="pdf", target="report.pdf") # Compile with Typst
```

The resulting source contains ordinary Typst calls such as
`#heading(level: 1, [#"Quarterly report"])`. Python supplies the repetition
and application data; Typst supplies the document semantics and typesetting.

`render(mode="pdf")` returns bytes when no target is supplied. `target` can
also be a writable binary stream. For images or imports, pass a compilation
`root`; see the [guide](https://genro-typst.readthedocs.io/en/latest/typst-guide.html).

For Python recipes, we recommend the filename **`mydoc.typ.py`**, with
`mydoc.typ` for generated Typst source and `mydoc.pdf` for the compiled document.
End the recipe with a guarded call to its builder class:

```python
if __name__ == "__main__":
    Report.run()
```

`python mydoc.typ.py` then generates `mydoc.typ` beside the recipe.
`python mydoc.typ.py output/document.typ` uses the given destination instead
(relative to the working directory). This generates Typst source without
requiring the compiler. Use this entry point in place of the manual
instantiation and rendering calls above; importing the guarded recipe does
not write files. The naming convention is optional; see
[naming Python recipes](https://genro-typst.readthedocs.io/en/latest/typst-guide.html#naming-python-recipes).

## Command-line interface

Installing the package also installs `genro-typst`. Run a Python recipe with
one format per invocation:

```bash
genro-typst mydoc.typ.py                          # mydoc.typ beside the recipe
genro-typst mydoc.typ.py --pdf                    # mydoc.pdf
genro-typst mydoc.typ.py --svg -o output/page.svg  # one SVG per page
genro-typst mydoc.typ.py -o output/document.typ   # explicit source destination
```

The CLI selects the recipe's sole locally defined `TypstBuilder` subclass,
or an explicit `BUILDER = MyDocument` / `--builder MyDocument`. It does not run
the main guard. Existing `python mydoc.typ.py [output.typ]` execution remains
supported. `python -m genro_typst` is an alternative to the installed command.

Direct execution accepts the same options, using the same rendering code
without reloading the recipe:

```bash
python mydoc.typ.py --pdf
python mydoc.typ.py --svg -o output/page.svg
python mydoc.typ.py --pdf --root assets -o output/document.pdf
```

The class calling `run()` is the default; `--builder MyDocument` can select
another class in the running script. The legacy positional destination and
`-o` are alternatives and cannot be supplied together.

PDF/SVG require the `pdf` extra and use Typst through its Python binding;
the official Typst CLI is not required. Multipage SVG files are named
`page-1.svg`, `page-2.svg`, etc. See the
[CLI guide](https://genro-typst.readthedocs.io/en/latest/cli.html)
for paths, assets and recipe conventions.

## What the Python layer provides

| Capability | Genro Typst's role |
|---|---|
| Structured authoring | Python methods for 129 native Typst calls, 12 language constructs and eight legacy document elements |
| Python composition | Use your own loops, conditions and functions to generate source |
| Application data | Bind attributes to a `Bag` with `^path` pointers |
| Explicit values | `length`, `color`, `label`, `expr` and `markup` distinguish Typst values from literal strings |
| Persistence | Save and reload the document tree through TYTX |
| Compilation access | Pass generated source to Typst for PDF and SVG output |

Native parameters are forwarded to Typst, which validates their names, types
and context. The catalog targets Typst 0.15.0; it does not claim coverage of
every parameter combination or every future Typst feature.

## Documentation and examples

**[Read the documentation](https://genro-typst.readthedocs.io/en/latest/)**

- [Getting started and guide](https://genro-typst.readthedocs.io/en/latest/typst-guide.html)
- [Python API](https://genro-typst.readthedocs.io/en/latest/api.html)
- [Command-line interface](https://genro-typst.readthedocs.io/en/latest/cli.html)
- [JavaScript builder](https://genro-typst.readthedocs.io/en/latest/javascript.html)
- [Native call reference](https://genro-typst.readthedocs.io/en/latest/native-reference.html)
- [Executable Python and Typst examples](https://genro-typst.readthedocs.io/en/latest/catalog-examples.html)
- [Verification and limits](https://genro-typst.readthedocs.io/en/latest/verification.html)
- [Machine-readable catalog](docs/native-catalog.json)

Complete examples include an [invoice header](examples/01_invoice_header/invoice_header.py),
a [multipage invoice](examples/02_invoice_lines/invoice_lines.py) and a
[native report](examples/03_native_report/report.py) with styles, table spans,
SVG graphics, mathematics and references. Each includes Python, generated
Typst and PDF files.

## JavaScript builder

The [`js/`](js/README.md) package provides a JavaScript authoring layer built on
`@genrojs/builders`. Its grammar is exported directly from `TypstBuilder`;
the JavaScript renderer produces ordinary Typst source. Tests compare it with
Python for every native element, language construct and legacy element.

From a checkout with Node.js 22 or later:

```bash
npm ci --prefix js
npm test --prefix js
node js/examples/report.typ.mjs /tmp/report.typ
```

To try the Python/JavaScript playground with editable recipes, Typst source and
SVG preview, run `npm run demo --prefix js` and open
[localhost:8172](http://127.0.0.1:8172/). Compilation runs in the browser with
Typst WebAssembly. Python recipes execute through the local server using an
interpreter with Genro Typst installed (`venv/bin/python` by default). See the
[browser example guide](https://genro-typst.readthedocs.io/en/latest/browser.html).
The playground includes 149 element recipes, searchable by category, with
editable Python/JavaScript tabs in CodeMirror and live SVG preview driven by
the active tab. In Python, **Python file** also opens imported modules and data
files in CodeMirror; every run uses the main recipe with all edited modules.
Reset and download apply to the selected file. Both languages keep independent
drafts per example until the page reloads. Browser compiler limitations are
marked explicitly in the collection.

Typst remains responsible for compilation. See the
[JavaScript guide](https://genro-typst.readthedocs.io/en/latest/javascript.html)
for usage, regeneration and differences between Python and JavaScript values.

The **Real-world documents** collection adds a technical proposal and service
report built from the same imported Python component library: shared letterheads,
page footers, themes, priced tables and reusable sections. See
[Reusable Python blocks](https://genro-typst.readthedocs.io/en/latest/reusable-blocks.html)
to organize these components as ordinary Python packages.
Follow the [module editor walkthrough](https://genro-typst.readthedocs.io/en/latest/browser.html#walkthrough-change-the-shared-footer)
to change the footer and pricing data directly in the playground.

## Architecture

```text
Your Python recipe and data
          |
          v
Genro Typst builder -> readable .typ source
                              |
                              v
                       Typst compiler
                              |
                              v
                         PDF / SVG
```

`genro-builders` provides the builder infrastructure and `genro-bag` the data
tree. Genro Typst translates that tree into Typst source. `TypstEngine` is a
small adapter around the optional Typst Python binding:

```python
from genro_typst.compiler import TypstEngine

result = TypstEngine().compile(source, preview=True)
# result.pdf: PDF bytes; result.svg_pages: SVG page bytes
```

PDF and SVG use the same source and timestamp. Without `preview=True`, no SVG
pages are generated and `result.pages` is `None`.

The separate **Genro PDF Builder** application provides the visual/Python
editor and MCP services. It depends on this library. See
[repository boundaries](docs/repository-separation.md) and the
[historical design proposal](xmldocs/proposal/typst-backend.md), which is partly
superseded by the current guide.

## Development

```bash
python -m pip install -e ".[dev,docs]"
python -m pytest -q
python -m ruff check src tests tools
python -m mypy
python tools/generate_reference.py --check
python -m sphinx -n -W --keep-going -b html docs docs/_build/html
```

Tests execute every documented native recipe, compile with Typst, compare
SVG pages with independently written Typst references, and check TYTX round
trips and expected errors. See [documentation development](docs/documentation.md)
for generated references, the application gallery and Read the Docs builds.

## License

Genro Typst is licensed under **Apache-2.0**. Copyright 2026 Softwell S.r.l.
See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Typst is a separate project with its own authors and
[Apache-2.0 license](https://github.com/typst/typst/blob/main/LICENSE).
Please credit and support the upstream Typst project when sharing work built
with this library.
