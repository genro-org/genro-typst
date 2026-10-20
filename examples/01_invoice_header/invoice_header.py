# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""01 — Invoice header with an elastic Layout/Row/Cell.

What you learn:
    - Subclass ``TypstBuilder`` and write the document in ``main``.
    - Cells with ``width=0`` share the free width; a length fixes it.
    - Rows without ``height`` take the height of their content.
    - Cell content read from the data with ``^`` pointers.
    - Two render modes: ``typst`` (source code) and ``pdf``.

Usage:
    python invoice_header.py
"""

from __future__ import annotations

from pathlib import Path

from genro_typst import TypstBuilder

HERE = Path(__file__).parent


class InvoiceHeader(TypstBuilder):
    """Header of an invoice: seller, customer, document data."""

    def setup(self, data):
        data["invoice.number"] = "2026/0142"
        data["invoice.date"] = "20/10/2026"
        data["customer.name"] = "Rossi & Figli S.r.l. #1"
        data["customer.address"] = "Via Roma 12, 20100 Milano"
        data["customer.vat"] = "IT01234567890"

    def main(self, root):
        doc = root.document(paper="a4", margin="15mm")
        doc.paragraph(content="Fattura")
        layout = doc.layout(border_width="0.5pt", border_color="#555555")
        top = layout.row()
        top.cell(content="Softwell S.r.l.", lbl="Fornitore")
        top.cell(content="^customer.name", lbl="Cliente")
        middle = layout.row()
        middle.cell(content="^customer.address", lbl="Indirizzo")
        middle.cell(content="^customer.vat", lbl="Partita IVA", width="45mm")
        bottom = layout.row(height="12mm")
        bottom.cell(content="^invoice.number", lbl="Numero", width="40mm")
        bottom.cell(content="^invoice.date", lbl="Data", width="30mm")
        bottom.cell(content="Bonifico a 30 giorni", lbl="Pagamento")
        notes = bottom.cell(lbl="Pagina", width="25mm", align="right", background="#eeeeee")
        notes.pageNumber(template="{page} di {total}")


if __name__ == "__main__":
    page = InvoiceHeader()
    page.create()
    page.render(target=HERE / "invoice_header.typ")
    page.render(mode="pdf", target=HERE / "invoice_header.pdf")
    print((HERE / "invoice_header.typ").read_text())
