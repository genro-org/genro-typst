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

import typst
from genro_builders.renderer import RendererBase

from genro_typst.typst_values import (
    typst_align,
    typst_bool,
    typst_color,
    typst_length,
    typst_string,
    typst_stroke,
    typst_width,
)

LABEL_STYLE = "size: 0.7em, fill: luma(90)"


class TypstRenderer(RendererBase):
    """Renderer producing Typst source code."""

    mode = "typst"

    def rendered_item(
        self,
        node: Any,
        item: Any,
        runtime_attrs: dict[str, Any],
        *,
        tag: str,
        **_opts: Any,
    ) -> str:
        """Dispatch to ``render_<tag>``; ``item`` holds the children fragments."""
        children = item if isinstance(item, list) else []
        method = getattr(self, f"render_{tag}")
        return str(method(node, children, self.with_defaults(node, runtime_attrs)))

    # ------------------------------------------------------------------
    # Elements
    # ------------------------------------------------------------------

    def render_document(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        page = (
            f"#set page(paper: {typst_string(attrs['paper'])}, "
            f"flipped: {typst_bool(attrs['flipped'])}, "
            f"margin: {typst_length(attrs['margin'])})"
        )
        return "\n".join([page, *(f"#{child}" for child in children)]) + "\n"

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

    def render_paragraph(self, node: Any, children: list[str], attrs: dict[str, Any]) -> str:
        return f"par({typst_string(attrs['content'])})"

    def render_pageNumber(
        self, node: Any, children: list[str], attrs: dict[str, Any],
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
            rest = rest[position + len(marker):]
        return f"context [{''.join(parts)}]"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def layout_stroke(self, layout_attrs: dict[str, Any]) -> str | None:
        """Stroke of the layout lines, ``None`` when ``border_width`` is unset."""
        if layout_attrs.get("border_width") is None:
            return None
        return typst_stroke(layout_attrs["border_width"], layout_attrs["border_color"])

    def with_defaults(self, node: Any, attrs: dict[str, Any]) -> dict[str, Any]:
        """Runtime attributes completed with the defaults of the signature.

        The source keeps only the attributes the author wrote; the defaults
        declared by the element signature are read from the grammar.
        """
        validations = node.builder._get_schema_info(node.node_tag)["call_args_validations"]
        defaults = {name: spec[2] for name, spec in validations.items()}
        return {**defaults, **attrs}

    def child_attrs(self, node: Any) -> list[dict[str, Any]]:
        """Runtime attributes, with defaults, of the children of ``node``."""
        return [
            self.with_defaults(child, child.builder.runtime_values(child)[1])
            for child in node.value
        ]

    def parent_attrs(self, node: Any) -> dict[str, Any]:
        """Runtime attributes, with defaults, of the parent node of ``node``."""
        parent = node.parent_node
        return self.with_defaults(parent, parent.builder.runtime_values(parent)[1])

    def inherited(self, *levels: dict[str, Any], key: str) -> bool:
        """First non-``None`` value of ``key`` from the innermost level out."""
        for level in levels:
            value = level.get(key)
            if value is not None:
                return bool(value)
        raise ValueError(f"no level defines {key!r}")


class TypstPdfRenderer(TypstRenderer):
    """Same walk as TypstRenderer; finalize compiles the code to PDF bytes."""

    mode = "pdf"
    render_type = "object"

    def finalize(self, result: Any, target: Any, **_opts: Any) -> Any:
        """Compile the Typst code and deliver the PDF bytes to ``target``.

        ``None`` returns the bytes; a ``str``/``Path`` writes the file;
        an object with ``.write`` receives the bytes.
        """
        code = "".join(result) if isinstance(result, list) else result
        pdf = typst.compile(code.encode("utf-8"), format="pdf")
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
