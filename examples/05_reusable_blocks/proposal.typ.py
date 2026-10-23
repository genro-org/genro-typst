# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""A three-page proposal assembled from an imported Python component library."""

from decimal import Decimal

from company_blocks import Theme, branded_document, contact_card, item_table, notice, signature
from company_blocks.sections import money
from proposal_data import CUSTOMER, SECTIONS

from genro_typst import TypstBuilder


class Document(TypstBuilder):
    def main(self, root):
        theme = Theme(company="Northwind Engineering", accent="#245b63")
        doc = branded_document(root, title="Technical proposal", reference="QT-2026-042", theme=theme)
        doc.heading("Technical proposal", level=1)
        contact_card(doc, label="Prepared for", theme=theme, **CUSTOMER)
        doc.par("Upgrade of the control cabinet and commissioning of packaging line B.")
        total = Decimal(0)
        for index, section in enumerate(SECTIONS, 1):
            if index > 1:
                doc.pagebreak()
            doc.heading(f"{index}. {section['title']}", level=2)
            total += item_table(doc, section["items"], theme=theme)
            notice(doc, "Scope and assumptions", section["note"], theme=theme)
        doc.pagebreak()
        doc.heading("Summary and approval", level=1)
        doc.par(f"Total excluding tax: {money(total)}")
        notice(doc, "Delivery", "Six weeks from approval of the final specification.", theme=theme)
        notice(doc, "Payment", "40% on order, 60% after the acceptance test.", theme=theme)
        signature(doc, role="Customer approval", theme=theme)


if __name__ == "__main__":
    Document.run()
