# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Data table: columns from the grid struct, rows from the data, totals."""

from __future__ import annotations

from decimal import Decimal

import pytest
import typst
from genro_bag import Bag

from genro_typst import TypstBuilder


def lines_bag(count: int) -> Bag:
    lines = Bag()
    for index in range(count):
        line = Bag()
        line["code"] = f"A{index}"
        line["quantity"] = index + 1
        line["price"] = Decimal("1.50")
        line["amount"] = Decimal("1.50") * (index + 1)
        lines[f"r{index}"] = line
    return lines


class Lines(TypstBuilder):
    count = 3
    caption: bool | str = "Totale"

    def setup(self, data):
        data["lines"] = lines_bag(self.count)

    def main(self, root):
        table = root.document().table(data="^lines", totalize_footer=self.caption)
        table.column(field="code", name="Codice", width="20mm")
        table.column(field="quantity", name="Q.tà", align="right", totalize=True)
        table.column(field="price", name="Prezzo", align="right")
        table.column(field="amount", name="Importo", width=2, align="right", totalize=True)


def rendered(cls: type[TypstBuilder]) -> str:
    page = cls()
    page.create()
    return page.render()


def test_columns_and_alignments():
    code = rendered(Lines)
    assert "columns: (20mm, 1fr, 1fr, 2fr,)" in code
    assert "align: (auto, right, right, right,)" in code


def test_header_repeats():
    code = rendered(Lines)
    assert (
        'table.header(repeat: true, strong("Codice"), strong("Q.tà"), '
        'strong("Prezzo"), strong("Importo"))'
    ) in code


def test_one_cell_per_field_per_row():
    code = rendered(Lines)
    assert '"A0", "1", "1.50", "1.50", "A1", "2", "1.50", "3.00"' in code


def test_totals_and_caption_runs():
    code = rendered(Lines)
    assert (
        'table.footer(repeat: false, table.cell(colspan: 1, strong("Totale")), '
        'strong("6"), table.cell(colspan: 1, strong("")), strong("9.00"))'
    ) in code


def test_no_footer_without_totalize_footer():
    class NoTotals(Lines):
        caption = False

    assert "table.footer" not in rendered(NoTotals)


def test_long_table_spans_pages_and_compiles():
    class Long(Lines):
        count = 200

    pdf = typst.compile(rendered(Long).encode(), format="pdf")
    assert pdf.startswith(b"%PDF")


def test_data_must_be_a_bag():
    class Wrong(TypstBuilder):
        def setup(self, data):
            data["lines"] = "not a bag"

        def main(self, root):
            root.document().table(data="^lines").column(field="x")

    page = Wrong()
    page.create()
    with pytest.raises(TypeError, match="must resolve to a Bag"):
        page.render()
