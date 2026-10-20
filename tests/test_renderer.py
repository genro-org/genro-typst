# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""TypstRenderer: Layout/Row/Cell to Typst code, and compilation to PDF."""

from __future__ import annotations

import pytest
import typst

from genro_typst import TypstBuilder


class Invoice(TypstBuilder):
    def setup(self, data):
        data["customer.name"] = 'Rossi "& Figli" #1 *bold* $x$ @ref <lbl>'

    def main(self, root):
        doc = root.document(margin="10mm")
        layout = doc.layout(border_width="0.5pt")
        top = layout.row()
        top.cell(content="Seller", lbl="From")
        top.cell(content="^customer.name", lbl="To", width="40mm")
        bottom = layout.row(height="12mm", row_border=False)
        bottom.cell(content="A", cell_border=False)
        bottom.cell(width=2).pageNumber(template="Pag. {page} di {total}")


@pytest.fixture
def invoice():
    page = Invoice()
    page.create()
    return page


def test_page_settings(invoice):
    code = invoice.render()
    assert code.startswith('#set page(paper: "a4", flipped: false, margin: 10mm)\n')


def test_row_columns_from_cell_widths(invoice):
    code = invoice.render()
    assert "grid(columns: (1fr, 40mm,), rows: (auto,)" in code
    assert "grid(columns: (1fr, 2fr,), rows: (12mm,)" in code


def test_lines_follow_inheritance(invoice):
    code = invoice.render()
    assert code.count("grid.hline(") == 1
    # first row: line after its first cell; second row: cell_border=False
    assert code.count("grid.vline(") == 1


def test_data_text_is_a_string_literal(invoice):
    code = invoice.render()
    assert '[#"Rossi \\"& Figli\\" #1 *bold* $x$ @ref <lbl>"]' in code


def test_page_number_context(invoice):
    code = invoice.render()
    assert (
        'context [#"Pag. "#counter(page).display()#" di "'
        "#counter(page).final().first()]"
    ) in code


def test_pdf_compiles_and_keeps_text(invoice, tmp_path):
    pdf = invoice.render(mode="pdf")
    assert pdf.startswith(b"%PDF")
    target = tmp_path / "invoice.pdf"
    invoice.render(mode="pdf", target=target)
    assert target.read_bytes().startswith(b"%PDF")


def test_unknown_attribute_raises():
    class Wrong(TypstBuilder):
        def main(self, root):
            root.document().layout(um="mm")

    with pytest.raises(ValueError, match="does not accept 'um'"):
        Wrong().create()


def test_invalid_length_raises_at_render():
    class Wrong(TypstBuilder):
        def main(self, root):
            root.document().layout().row(height="12").cell(content="x")

    page = Wrong()
    page.create()
    with pytest.raises(ValueError, match="length '12'"):
        page.render()


def test_generated_code_is_valid_typst(invoice):
    typst.compile(invoice.render().encode(), format="pdf")
