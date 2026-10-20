# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Grammar of the print document: document and Layout/Row/Cell.

The model is GenroPy's Layout/Row/Cell (``gnr/core/gnrhtml.py``) without
absolute positioning: a row without ``height`` takes the height of its
content, a cell with ``width=0`` takes an equal share of the free width.
Lengths are strings with their unit (``'25mm'``, ``'30%'``, ``'2fr'``);
a numeric width is a fraction.
"""

from __future__ import annotations

from genro_builders.builder import element


class TypstElements:
    """Mixin defining the print elements for TypstBuilder."""

    @element(sub_tags="layout,paragraph,pageNumber")
    def document(
        self,
        paper: str = "a4",
        flipped: bool = False,
        margin: str = "15mm",
    ) -> None:
        """Document root: page format, orientation and margins.

        Args:
            paper: Typst paper name (``a4``, ``a5``, ``us-letter``...).
            flipped: Landscape orientation.
            margin: Page margin on every side.
        """
        ...

    @element(sub_tags="row")
    def layout(
        self,
        border_width: str | None = None,
        border_color: str = "black",
        row_border: bool = True,
        cell_border: bool = True,
        inset: str = "1mm",
    ) -> None:
        """Layout container: a vertical sequence of rows.

        Args:
            border_width: Width of the outer border and of the lines
                between rows and cells. ``None`` draws no line.
            border_color: Color of every line of the layout.
            row_border: Default for the line below each row.
            cell_border: Default for the line after each cell.
            inset: Padding inside every cell.
        """
        ...

    @element(sub_tags="cell")
    def row(
        self,
        height: str | None = None,
        row_border: bool | None = None,
        cell_border: bool | None = None,
    ) -> None:
        """Row: a horizontal sequence of cells.

        Args:
            height: Row height. ``None`` takes the height of the content.
            row_border: Line below this row (``None`` inherits from layout).
            cell_border: Default for the cells of this row (``None``
                inherits from layout).
        """
        ...

    @element(sub_tags="layout,paragraph,pageNumber")
    def cell(
        self,
        content: str | None = None,
        width: float | str = 0,
        lbl: str | None = None,
        cell_border: bool | None = None,
        align: str | None = None,
        valign: str | None = None,
        background: str | None = None,
    ) -> None:
        """Cell: text content, nested layout or content elements.

        Args:
            content: Text of the cell, shown after the label.
            width: Number (fraction, ``0`` = ``1fr``) or length string.
            lbl: Label shown above the content.
            cell_border: Line after this cell (``None`` inherits from row).
            align: ``left``, ``center``, ``right``.
            valign: ``top``, ``middle``, ``bottom``.
            background: Fill color (``'#rrggbb'`` or a Typst color name).
        """
        ...

    @element(sub_tags="")
    def paragraph(self, content: str = "") -> None:
        """Paragraph of plain text."""
        ...

    @element(sub_tags="")
    def pageNumber(self, template: str = "{page} / {total}") -> None:
        """Page number. ``{page}`` is the current page, ``{total}`` the last."""
        ...
