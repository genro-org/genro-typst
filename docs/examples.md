# Complete document examples

Run these scripts from a repository checkout. The invoice and native report
examples require the `pdf` extra and save Typst source and PDF beside the
Python recipe; their generated files are also available in the repository.
The executable Python recipe below only generates source and needs no compiler.

## Executable Python recipe

A recipe following the `mydoc.typ.py` naming convention, with Python loops
and a guarded `run()` entry point. Importing it does not write any files.

```bash
python examples/04_python_recipe/mydoc.typ.py
python examples/04_python_recipe/mydoc.typ.py output/document.typ
```

The first command writes `mydoc.typ` beside the recipe. The second uses the
destination path relative to your working directory. See
[naming Python recipes](typst-guide.md#naming-python-recipes) for details.

```{literalinclude} ../examples/04_python_recipe/mydoc.typ.py
:language: python
```

[Download Python recipe](../examples/04_python_recipe/mydoc.typ.py)

## Invoice header

An elastic layout with labeled cells, fixed and shared widths, data binding
and page numbering.

```{literalinclude} ../examples/01_invoice_header/invoice_header.py
:language: python
```

[Download Python](../examples/01_invoice_header/invoice_header.py) ·
[Typst source](../examples/01_invoice_header/invoice_header.typ) ·
[PDF](../examples/01_invoice_header/invoice_header.pdf)

## Invoice lines

A multipage data table with 120 rows, repeated headers and a total footer.

```{literalinclude} ../examples/02_invoice_lines/invoice_lines.py
:language: python
```

[Download Python](../examples/02_invoice_lines/invoice_lines.py) ·
[Typst source](../examples/02_invoice_lines/invoice_lines.typ) ·
[PDF](../examples/02_invoice_lines/invoice_lines.pdf)

## Native report

Styles, inline content, table spans, an SVG figure, an equation and references.
The script also exports an SVG preview. Keep `mark.svg` alongside the recipe.

```{literalinclude} ../examples/03_native_report/report.py
:language: python
```

[Download Python](../examples/03_native_report/report.py) ·
[SVG asset](../examples/03_native_report/mark.svg) ·
[Typst source](../examples/03_native_report/report.typ) ·
[PDF](../examples/03_native_report/report.pdf)
