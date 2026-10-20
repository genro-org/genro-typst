# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""A print document saved as TYTX and reloaded renders the same Typst code.

This is the storage format of the editors: the source Bag serialized with
TYTX, reloaded into a builder that has no ``main``.
"""

from __future__ import annotations

from genro_builders import SourceBag

from genro_typst import TypstBuilder


class Header(TypstBuilder):
    def setup(self, data):
        data["customer.name"] = "Rossi & Figli"

    def main(self, root):
        doc = root.document(paper="a5", flipped=True)
        layout = doc.layout(border_width="0.5pt", border_color="#555555")
        row = layout.row(height="12mm")
        row.cell(content="^customer.name", lbl="Cliente", width=2)
        row.cell(lbl="Pagina", width="25mm", background="#eeeeee").pageNumber()


def reloaded(wire: str) -> TypstBuilder:
    """A bare TypstBuilder carrying the decoded source.

    genro-builders 0.29 has no public call to attach a decoded source.
    Its own test suite sets ``_builder`` on the root only
    (tests/test_custom_types.py), which covers a flat source. A node finds
    its builder in its own slot or in the Bag that contains it, never
    further up, so here every decoded branch gets the builder.
    """
    builder = TypstBuilder()
    source = SourceBag.from_tytx(wire)
    source._builder = builder
    for node in source.traverse():
        if isinstance(node.value, SourceBag):
            node.value._builder = builder
    source.set_backref()
    builder.source = source
    builder.data["customer.name"] = "Rossi & Figli"
    return builder


def test_wire_roundtrip_is_stable():
    page = Header()
    page.create()
    wire = page.source.to_tytx()
    assert SourceBag.from_tytx(wire).to_tytx() == wire


def test_reloaded_source_renders_the_same_code():
    page = Header()
    page.create()
    builder = reloaded(page.source.to_tytx())
    assert builder.render() == page.render()


def test_reloaded_source_validates():
    page = Header()
    page.create()
    builder = reloaded(page.source.to_tytx())
    assert builder.validate_source() == []


def test_pointer_survives_as_pointer():
    page = Header()
    page.create()
    builder = reloaded(page.source.to_tytx())
    builder.data["customer.name"] = "Bianchi S.p.A."
    assert '"Bianchi S.p.A."' in builder.render()
