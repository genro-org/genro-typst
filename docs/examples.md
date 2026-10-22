# Complete document examples

Run these scripts from a checkout with the `pdf` extra installed. They save
Typst source and PDF beside the Python recipe. Generated files are also
available in the source repository.

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
