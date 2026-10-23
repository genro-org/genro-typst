# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""A different document using exactly the same page furniture and body blocks."""

from company_blocks import Theme, branded_document, contact_card, notice, signature
from proposal_data import CUSTOMER

from genro_typst import TypstBuilder


class Document(TypstBuilder):
    def main(self, root):
        theme = Theme(company="Northwind Engineering", accent="#614a78", pale="#f3eff8")
        doc = branded_document(root, title="Service report", reference="SR-2026-018", theme=theme)
        doc.heading("Service report", level=1)
        contact_card(doc, label="Site", theme=theme, **CUSTOMER)
        doc.heading("Work completed", level=2)
        for task in ["Verified cabinet wiring", "Calibrated the conveyor sensor", "Tested the emergency stop"]:
            doc.par(task)
        notice(doc, "Next visit", "Inspect the sensor alignment after 500 operating hours.", theme=theme)
        signature(doc, role="Service technician", theme=theme)


if __name__ == "__main__":
    Document.run()
