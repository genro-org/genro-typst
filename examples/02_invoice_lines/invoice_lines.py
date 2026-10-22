# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""02 — Invoice lines: a data table over several pages.

What you learn:
    - ``table`` reads its rows from a Bag in the data (``data='^lines'``).
    - ``column`` follows the GenroPy grid struct: ``field``, ``name``,
      ``width``, ``align``, ``totalize``.
    - The header repeats on every page (``headerRepeat``).
    - ``totalize_footer`` adds the total row after the last row, with its
      caption across the columns before the first total.
    - ``pageNumber`` in the document body.

Usage:
    python invoice_lines.py
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from genro_bag import Bag

from genro_typst import TypstBuilder

HERE = Path(__file__).parent

ARTICLES = [
    ("Stainless steel screws M6x20", Decimal("0.18")),
    ("Self-locking nuts M6", Decimal("0.09")),
    ("Flat washers 6 mm", Decimal("0.04")),
    ("Angle bracket 40x40", Decimal("1.75")),
    ("Nylon wall plug 8 mm", Decimal("0.12")),
]


class InvoiceLines(TypstBuilder):
    """Invoice with 120 lines: three pages, header repeated, total at the end."""

    def setup(self, data):
        lines = Bag()
        for index in range(120):
            description, price = ARTICLES[index % len(ARTICLES)]
            quantity = 10 * (index % 7 + 1)
            line = Bag()
            line["code"] = f"ART{index + 1:04d}"
            line["description"] = description
            line["quantity"] = quantity
            line["price"] = price
            line["amount"] = price * quantity
            lines[f"r{index:03d}"] = line
        data["lines"] = lines

    def main(self, root):
        doc = root.document(paper="a4", margin="15mm")
        doc.paragraph(content="Invoice 2026/0142 — lines")
        table = doc.table(data="^lines", totalize_footer="Invoice total")
        table.column(field="code", name="Code", width="25mm")
        table.column(field="description", name="Description")
        table.column(field="quantity", name="Qty.", width="18mm", align="right", totalize=True)
        table.column(field="price", name="Price", width="22mm", align="right")
        table.column(field="amount", name="Amount", width="25mm", align="right", totalize=True)
        doc.pageNumber(template="Page {page} of {total}")


if __name__ == "__main__":
    page = InvoiceLines()
    page.create()
    page.render(target=HERE / "invoice_lines.typ")
    page.render(mode="pdf", target=HERE / "invoice_lines.pdf")
    print(f"Saved {HERE / 'invoice_lines.pdf'}")
