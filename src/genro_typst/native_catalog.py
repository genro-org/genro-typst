# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Native content functions, versioned and tested against Typst 0.15.0.

Each entry is (Typst function, argument strategy, documentation section).
The catalog drives grammar registration, rendering and reference generation.
"""

from __future__ import annotations

NATIVE: dict[str, tuple[str, str, str]] = {}


def _add(section: str, mode: str, names: str, prefix: str = "") -> None:
    for name in names.split():
        function = prefix + name
        NATIVE[function.replace(".", "_").replace("-", "_")] = (function, mode, section)


_add("text", "body", "text underline overline strike highlight smallcaps sub super lower upper")
_add("text", "value", "raw lorem")
_add("text", "leaf", "linebreak smartquote")
_add("model", "body", "heading strong emph par quote figure footnote title")
_add("model", "items", "list enum terms")
_add("model", "body", "list.item enum.item")
_add("model", "args", "terms.item")
_add("model", "value", "link ref cite bibliography numbering")
_add("model", "leaf", "outline parbreak divider")
_add("model", "items", "table.header table.footer")
_add("model", "body", "table.cell")
_add("model", "leaf", "table.hline table.vline")
NATIVE["native_table"] = ("table", "items", "model")
_add("layout", "body", "align block box columns hide move pad page place repeat rotate scale skew")
_add("layout", "items", "grid stack grid.header grid.footer")
_add("layout", "body", "grid.cell")
_add("layout", "leaf", "pagebreak colbreak grid.hline grid.vline")
_add("layout", "value", "h v measure")
NATIVE["native_layout"] = ("layout", "value", "layout")
_add("visualize", "body", "circle ellipse rect square")
_add("visualize", "value", "image")
_add(
    "visualize",
    "args",
    "line polygon curve curve.move curve.line curve.quad curve.cubic curve.close",
)
_add(
    "math",
    "body",
    "equation upright italic bold serif sans cal frak mono bb display inline script sscript",
    "math.",
)
_add(
    "math",
    "args",
    "frac root sqrt binom vec mat cases lr attach accent cancel class op limits scripts",
    "math.",
)
_add(
    "math",
    "args",
    "abs norm floor ceil round stretch underbrace overbrace underbracket overbracket underline overline",
    "math.",
)
_add("math", "args", "underparen overparen undershell overshell primes", "math.")
_add("introspection", "value", "metadata")
_add("pdf", "body", "artifact", "pdf.")

SPECIAL = (
    "call",
    "set_rule",
    "show_rule",
    "scope",
    "context",
    "equation",
    "label",
    "let",
    "import_module",
    "include",
    "typst_code",
    "typst_markup",
)
LEGACY_CONTENT = ("layout", "table", "paragraph", "pageNumber")
CONTENT_TAGS = ",".join((*LEGACY_CONTENT, *NATIVE, *SPECIAL))

# Use the same authoring names in Python and JavaScript, including collisions
# present in only one runtime. All other elements use their bare grammar name.
AUTHORING_ALIASES = {
    "columns": "typst_columns",
    "move": "typst_move",
    "label": "typst_label",
}
