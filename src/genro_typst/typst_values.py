# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Conversion of Python values into Typst source fragments.

Every function returns a fragment of Typst CODE (not markup): the renderer
emits text as string literals (``"..."``), so markup characters (``#``,
``*``, ``_``, ``$``, ``@``, ``<``) never need escaping. A value outside the
accepted forms raises ``ValueError`` (``TypeError`` for a wrong type):
the grammar has no silent fallback.
"""

from __future__ import annotations

import re

_LENGTH_RE = re.compile(r"^-?\d+(\.\d+)?(mm|cm|pt|in|em|%|fr)$")
_HEX_COLOR_RE = re.compile(r"^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")

#: Typst predefined color names accepted as they are.
NAMED_COLORS = frozenset(
    {
        "black",
        "gray",
        "silver",
        "white",
        "navy",
        "blue",
        "aqua",
        "teal",
        "eastern",
        "purple",
        "fuchsia",
        "maroon",
        "red",
        "orange",
        "yellow",
        "olive",
        "green",
        "lime",
    }
)

#: Grammar alignment words and their Typst alignment.
HORIZONTAL_ALIGN = {"left": "left", "center": "center", "right": "right"}
VERTICAL_ALIGN = {"top": "top", "middle": "horizon", "bottom": "bottom"}


def typst_string(value: object) -> str:
    """Typst string literal for ``value`` (``str()`` of it)."""
    text = str(value)
    text = (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'"{text}"'


def typst_length(value: object) -> str:
    """Typst length, ratio or fraction from a string with its unit.

    ``'25mm'``, ``'2cm'``, ``'10pt'``, ``'30%'``, ``'2fr'`` and ``'auto'``
    pass through after validation.
    """
    if not isinstance(value, str):
        raise TypeError(f"length {value!r} must be a string with a unit")
    if value == "auto" or _LENGTH_RE.match(value):
        return value
    raise ValueError(
        f"length {value!r}: expected a number with mm, cm, pt, in, em, %, fr, or 'auto'",
    )


def typst_width(value: object) -> str:
    """Typst column width: a number is a fraction, ``0`` is ``1fr``.

    A string goes through :func:`typst_length`.
    """
    if isinstance(value, bool):
        raise TypeError(f"width {value!r} is not a number nor a length")
    if isinstance(value, (int, float)):
        if value < 0:
            raise ValueError(f"width {value!r} is negative")
        return "1fr" if value == 0 else f"{value}fr"
    return typst_length(value)


def typst_color(value: object) -> str:
    """Typst color from ``'#rrggbb'``, ``'#rgb'`` or a predefined name."""
    if isinstance(value, str):
        if _HEX_COLOR_RE.match(value):
            return f'rgb("{value}")'
        if value in NAMED_COLORS:
            return value
    raise ValueError(
        f"color {value!r}: expected '#rrggbb', '#rgb' or one of {', '.join(sorted(NAMED_COLORS))}",
    )


def typst_bool(value: object) -> str:
    """Typst boolean."""
    if not isinstance(value, bool):
        raise TypeError(f"{value!r} is not a boolean")
    return "true" if value else "false"


def typst_align(align: str | None, valign: str | None) -> str | None:
    """Typst alignment from the grammar words, ``None`` when both are absent."""
    parts = []
    if align is not None:
        if align not in HORIZONTAL_ALIGN:
            raise ValueError(f"align {align!r}: expected one of {sorted(HORIZONTAL_ALIGN)}")
        parts.append(HORIZONTAL_ALIGN[align])
    if valign is not None:
        if valign not in VERTICAL_ALIGN:
            raise ValueError(f"valign {valign!r}: expected one of {sorted(VERTICAL_ALIGN)}")
        parts.append(VERTICAL_ALIGN[valign])
    return " + ".join(parts) if parts else None


def typst_stroke(width: object, color: object) -> str:
    """Typst stroke ``<length> + <color>``."""
    return f"{typst_length(width)} + {typst_color(color)}"
