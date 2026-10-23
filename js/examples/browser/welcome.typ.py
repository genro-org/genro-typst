# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
from genro_typst import TypstBuilder, color, expr, length


class Document(TypstBuilder):
    def main(self, root):
        doc = root.document(paper="a5", margin="14mm")
        doc.set_rule(target="text", font="Libertinus Serif", size=length("10pt"))
        doc.text("GENRO / FIELD NOTES", size=length("8pt"), fill=color("#526b60"))
        doc.heading("Small ideas,\nbeautiful documents.", level=1)
        doc.par("Written with Genro. Typeset by Typst.")
        doc.v(content=length("5mm"))

        table = doc.native_table(
            columns=[length("1fr"), length("auto")],
            inset=length("3mm"), stroke=expr("0.4pt + gray"),
        )
        header = table.table_header()
        header.table_cell("Work item").strong("")
        header.table_cell("Hours")
        for name, hours in [("Research", 4), ("Design", 6), ("Development", 12)]:
            table.table_cell(name)
            table.table_cell(str(hours))
        doc.v(content=length("5mm"))
        doc.par("Change this recipe and run it again.")


if __name__ == "__main__":
    Document.run()
