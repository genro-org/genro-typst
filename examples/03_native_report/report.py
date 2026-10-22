# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""A standalone report mixing native Typst features and Python data generation."""

from pathlib import Path

from genro_typst import TypstBuilder, color, expr, label, length, markup
from genro_typst.compiler import TypstEngine


class Report(TypstBuilder):
    def main(self, root):
        doc = root.document(
            margin="18mm",
            metadata={"title": "Genro Typst — native document", "author": ["Softwell"]},
            page_options={"numbering": "1 / 1", "header": markup("Genro Typst · example")},
        )
        doc.set_rule(target="text", size=length("11pt"), lang="en")
        doc.set_rule(target="heading", numbering="1.")
        doc.show_rule(selector="heading", target="text", fill=color("#167665"))
        doc.heading("A complete document", level=1)
        doc.typst_label(name="intro")
        paragraph = doc.par(justify=True)
        paragraph.text("This report is built with ")
        paragraph.strong("Python")
        paragraph.text(" and uses native Typst elements with ")
        paragraph.emph("nested styles and content")
        paragraph.text(".")
        paragraph.footnote("The recipe remains readable and editable.")

        doc.heading("Data and merged cells", level=2)
        table = doc.native_table(
            columns=[length("3fr"), length("1fr"), length("1fr")],
            inset=length("2mm"),
            stroke=expr('0.5pt + rgb("#b8ccc5")'),
        )
        header = table.table_header(repeat=True)
        for caption in ("Description", "Quantity", "Amount"):
            header.table_cell(caption, fill=color("#e5f2ed")).strong(" ")
        for description, quantity, amount in (("Analysis", 2, 240), ("Template", 3, 150)):
            for value in (description, quantity, amount):
                table.table_cell(str(value))
        footer = table.table_footer(repeat=False)
        footer.table_cell("Total", colspan=2).strong(" for the document")
        footer.table_cell("390")

        doc.heading("Graphics and formulas", level=2)
        figure = doc.figure(caption=markup("A local SVG"), alt="Green circle with the letter G")
        figure.image("mark.svg", width=length("18mm"))
        doc.equation(formula="sum_(i=1)^n i = (n (n+1))/2", numbering="(1)")
        doc.rect(
            content="Native box",
            width=length("100%"),
            inset=length("3mm"),
            fill=color("#e5f2ed"),
            stroke=None,
        )
        items = doc.list()
        items.list_item("Text and styles")
        items.list_item("Tables, mathematics and graphics")
        doc.par().link(content="https://typst.app/docs/").text("Typst documentation")
        reference = doc.par()
        reference.text("Back to section ")
        reference.ref(label("intro"))


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    report = Report()
    report.create()
    source = report.render()
    (directory / "report.typ").write_text(source)
    result = TypstEngine().compile(source, root=directory, preview=True)
    (directory / "report.pdf").write_bytes(result.pdf)
    for index, svg in enumerate(result.svg_pages, start=1):
        (directory / f"page-{index}.svg").write_bytes(svg)
    print(f"Generated {result.pages} page(s) in {directory}")
