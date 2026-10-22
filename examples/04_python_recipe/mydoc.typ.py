# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Run with python mydoc.typ.py [output.typ] to generate Typst source."""

from genro_typst import TypstBuilder


class MyDocument(TypstBuilder):
    def main(self, root):
        doc = root.document(paper="a4", margin="15mm")
        doc.heading("A document written in Python", level=1)
        for name in ("Research", "Development", "Support"):
            doc.par(f"Department: {name}")


if __name__ == "__main__":
    MyDocument.run()
