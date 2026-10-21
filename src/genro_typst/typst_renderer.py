# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""TypstRenderer — walks the source and produces Typst source code.

Every node renders to a Typst CODE expression (``grid(...)``,
``par("...")``, ``context [...]``); the ``document`` node turns them into
the file: ``#set page(...)`` followed by one ``#<expression>`` per child.
Text always travels as a Typst string literal, so markup characters in the
data never need escaping.

Layout/Row/Cell:

- ``layout`` → ``grid`` with one column, one row per ``row``, wrapped in a
  ``block`` with the outer stroke when ``border_width`` is set;
- ``row`` → ``grid`` with one column per ``cell`` (``width`` → column
  width, ``0`` = ``1fr``) and the layout ``inset``;
- line below a row and after a cell: ``grid.hline`` / ``grid.vline``,
  inherited cell → row → layout as in GenroPy.

TypstPdfRenderer compiles the same code with the ``typst`` binding.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from genro_bag import Bag

from genro_typst.compiler import TypstEngine
from genro_typst.native_catalog import NATIVE
from genro_typst.native_renderer import content_block, render_native
from genro_typst.renderer import DocumentRenderer
from genro_typst.typst_values import (
    typst_align,
    typst_bool,
    typst_color,
    typst_length,
    typst_string,
    typst_stroke,
    typst_width,
)
from genro_typst.values import named_arguments

LABEL_STYLE = "size: 0.7em, fill: luma(90)"


class TypstRenderer(DocumentRenderer):
    """Renderer producing Typst source code."""

    mode = "typst"

    def rendered_item(
        self,
        node: Any,
        item: Any,
        runtime_attrs: dict[str, Any],
        *,
        tag: str,
        **opts: Any,
    ) -> str:
        """Dispatch to ``render_<tag>``; ``item`` holds the children fragments."""
        children = item if isinstance(item, list) else []
        attrs = self.with_defaults(node, runtime_attrs)
        if (tag in NATIVE or tag == "call") and item is not None and not isinstance(item, list):
            if attrs.get("content") is not None:
                raise ValueError("Use either positional content or content=, not both")
            attrs["content"] = item
        method = getattr(self, f"render_{tag}", None)
        if method is None:
            return render_native(tag, children, attrs)
        return str(method(node, children, attrs))

    # ------------------------------------------------------------------
    # Elements
    # ------------------------------------------------------------------

    def render_document(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        page = (
            f"#set page(paper: {typst_string(attrs['paper'])}, "
            f"flipped: {typst_bool(attrs['flipped'])}, "
            f"margin: {typst_length(attrs['margin'])})"
        )
        settings = [page]
        if attrs.get("page_options"):
            settings.append("#set page(" + ", ".join(named_arguments(attrs["page_options"])) + ")")
        if attrs.get("metadata"):
            settings.append("#set document(" + ", ".join(named_arguments(attrs["metadata"])) + ")")
        return "\n".join([*settings, *(f"#{child}" for child in children)]) + "\n"

    def render_layout(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        stroke = self.layout_stroke(attrs)
        rows = self.child_attrs(node)
        parts = []
        for index, (fragment, row_attrs) in enumerate(zip(children, rows)):
            parts.append(fragment)
            last = index == len(children) - 1
            if stroke and not last and self.inherited(row_attrs, attrs, key="row_border"):
                parts.append(f"grid.hline(stroke: {stroke})")
        body = f"grid(columns: (1fr,), {', '.join(parts)})"
        if stroke is None:
            return body
        return f"block(width: 100%, stroke: {stroke}, {body})"

    def render_row(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        if not children:
            return "[]"
        layout_attrs = self.parent_attrs(node)
        stroke = self.layout_stroke(layout_attrs)
        cells = self.child_attrs(node)
        columns = ", ".join(typst_width(cell["width"]) for cell in cells)
        parts = []
        for index, (fragment, cell_attrs) in enumerate(zip(children, cells)):
            parts.append(fragment)
            last = index == len(children) - 1
            if (
                stroke
                and not last
                and self.inherited(cell_attrs, attrs, layout_attrs, key="cell_border")
            ):
                parts.append(f"grid.vline(x: {index + 1}, stroke: {stroke})")
        height = typst_length(attrs["height"]) if attrs.get("height") is not None else "auto"
        return (
            f"grid(columns: ({columns},), rows: ({height},), "
            f"inset: {typst_length(layout_attrs['inset'])}, {', '.join(parts)})"
        )

    def render_cell(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        body_parts = []
        if attrs.get("content") is not None:
            body_parts.append(f"#{typst_string(attrs['content'])}")
        body_parts.extend(f"#{child}" for child in children)
        body = "[" + "\n".join(body_parts) + "]"
        if attrs.get("lbl") is not None:
            label = f"text({LABEL_STYLE}, {typst_string(attrs['lbl'])})"
            body = f"stack(spacing: 0.8mm, {label}, {body})"
        params = []
        if attrs.get("background") is not None:
            params.append(f"fill: {typst_color(attrs['background'])}")
        align = typst_align(attrs.get("align"), attrs.get("valign"))
        if align is not None:
            params.append(f"align: {align}")
        return f"grid.cell({', '.join([*params, body])})"

    def render_table(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        columns = self.child_attrs(node)
        if not columns:
            raise ValueError("A table needs at least one column")
        rows = attrs["data"]
        if not isinstance(rows, Bag):
            raise TypeError(f"table data must resolve to a Bag, got {type(rows).__name__}")
        widths = ", ".join(typst_width(column["width"]) for column in columns)
        aligns = ", ".join(typst_align(column["align"], None) or "auto" for column in columns)
        header = ", ".join(f"strong({typst_string(column['name'])})" for column in columns)
        body = []
        for row in rows.values():
            for column in columns:
                value = row[column["field"]]
                body.append(typst_string("" if value is None else value))
        parts = [
            f"columns: ({widths},)",
            f"align: ({aligns},)",
            f"stroke: {typst_stroke(attrs['border_width'], attrs['border_color'])}",
            f"inset: {typst_length(attrs['inset'])}",
            "fill: (x, y) => if y == 0 { luma(230) }",
            f"table.header(repeat: {typst_bool(attrs['headerRepeat'])}, {header})",
            *body,
        ]
        if attrs["totalize_footer"] is not False:
            parts.append(self.total_footer(columns, rows, attrs["totalize_footer"]))
        return f"table({', '.join(parts)})"

    def render_column(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        """Columns are read by their ``table``; they emit nothing themselves."""
        return ""

    def total_footer(self, columns: list[dict[str, Any]], rows: Bag, caption: bool | str) -> str:
        """``table.footer`` with the column totals.

        Each run of columns without ``totalize`` becomes one cell spanning
        the run; the first run carries the caption (GenroPy
        ``runningTotalsDefaults``).
        """
        cells = []
        run = 0
        captioned = False
        for column in [*columns, None]:
            if column is not None and not column["totalize"]:
                run += 1
                continue
            if run:
                text = caption if isinstance(caption, str) and not captioned else ""
                captioned = True
                cells.append(f"table.cell(colspan: {run}, strong({typst_string(text)}))")
                run = 0
            if column is not None:
                values = [row[column["field"]] for row in rows.values()]
                total = sum(value for value in values if value is not None)
                cells.append(f"strong({typst_string(total)})")
        return f"table.footer(repeat: false, {', '.join(cells)})"

    def render_paragraph(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        if children:
            return f"par({content_block(children, attrs['content'])})"
        return f"par({typst_string(attrs['content'])})"

    def render_pageNumber(
        self,
        node: Any,
        children: list[str],
        attrs: dict[str, Any],
    ) -> str:
        template = attrs["template"]
        markers = {
            "{page}": "#counter(page).display()",
            "{total}": "#counter(page).final().first()",
        }
        parts = []
        rest = template
        while rest:
            positions = [(rest.find(m), m) for m in markers if rest.find(m) >= 0]
            if not positions:
                parts.append(f"#{typst_string(rest)}")
                break
            position, marker = min(positions)
            if position:
                parts.append(f"#{typst_string(rest[:position])}")
            parts.append(markers[marker])
            rest = rest[position + len(marker) :]
        return f"context [{''.join(parts)}]"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def layout_stroke(self, layout_attrs: dict[str, Any]) -> str | None:
        """Stroke of the layout lines, ``None`` when ``border_width`` is unset."""
        if layout_attrs.get("border_width") is None:
            return None
        return typst_stroke(layout_attrs["border_width"], layout_attrs["border_color"])


class TypstPdfRenderer(TypstRenderer):
    """Same walk as TypstRenderer; finalize compiles the code to PDF bytes."""

    mode = "pdf"
    render_type = "object"

    def finalize(self, result: Any, target: Any, **opts: Any) -> Any:
        """Compile the Typst code and deliver the PDF bytes to ``target``.

        ``None`` returns the bytes; a ``str``/``Path`` writes the file;
        an object with ``.write`` receives the bytes.
        """
        code = "".join(result) if isinstance(result, list) else result
        if opts.get("engine", "typst") != "typst":
            raise ValueError("TypstBuilder requires the typst engine.")
        root = Path(opts["root"]) if opts.get("root") else None
        pdf = TypstEngine().compile(code, root=root).pdf
        if target is None:
            return pdf
        if isinstance(target, (str, Path)):
            path = Path(target)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(pdf)
            return None
        write = getattr(target, "write", None)
        if callable(write):
            write(pdf)
            return None
        raise TypeError(f"render target {target!r} is neither a path nor writable")
