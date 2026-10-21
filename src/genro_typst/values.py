# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Explicit Typst values that survive JSON/TYTX without custom Python objects."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from typing import Any

from genro_typst.typst_values import typst_color, typst_length, typst_string

EXPRESSION_KEY = "$typst"
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*$")


def expr(code: str) -> dict[str, str]:
    """An explicit trusted Typst expression, not ordinary document text."""
    if not isinstance(code, str) or not code.strip():
        raise ValueError("A Typst expression must be a nonempty string")
    return {EXPRESSION_KEY: code}


def length(value: str) -> dict[str, str]:
    """A validated length/ratio/fraction, e.g. length('12pt')."""
    return expr(typst_length(value))


def color(value: str) -> dict[str, str]:
    """A validated named or hexadecimal color."""
    return expr(typst_color(value))


def label(name: str) -> dict[str, str]:
    """A Typst label value for ref, cite and link."""
    return expr(f"label({typst_string(name)})")


def markup(source: str) -> dict[str, str]:
    """Trusted Typst markup as a content value (caption, header, footer, ...)."""
    # A final // comment must not consume the closing content delimiter.
    return expr(f"[{source}\n]")


def identifier(name: str) -> str:
    if not isinstance(name, str) or not _IDENTIFIER.fullmatch(name):
        raise ValueError(f"Invalid Typst identifier: {name!r}")
    return name


def value_code(value: Any) -> str:
    """Serialize data as literals; code requires the explicit expr/markup marker."""
    if value is None:
        return "none"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return typst_string(value)
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("Typst numbers must be finite")
        return str(value)
    if isinstance(value, Mapping):
        if EXPRESSION_KEY in value:
            if set(value) != {EXPRESSION_KEY}:
                raise ValueError("A Typst expression marker cannot contain other keys")
            return expr(value[EXPRESSION_KEY])[EXPRESSION_KEY]
        if not value:
            return "(:)"
        if any(not isinstance(key, str) for key in value):
            raise TypeError("Typst dictionary keys must be strings")
        return (
            "(" + ", ".join(f"{typst_string(k)}: {value_code(v)}" for k, v in value.items()) + ",)"
        )
    if isinstance(value, (list, tuple)):
        return "(" + ", ".join(value_code(v) for v in value) + (",)" if value else ")")
    raise TypeError(f"Cannot encode {type(value).__name__} as a Typst value")


def named_arguments(options: Mapping[str, Any]) -> list[str]:
    result = []
    seen = set()
    for key, value in options.items():
        name = identifier(key.removesuffix("_").replace("_", "-"))
        if "." in name:
            raise ValueError(f"Argument name cannot be a dotted path: {key!r}")
        if name in seen:
            raise ValueError(f"Duplicate Typst argument: {name}")
        seen.add(name)
        result.append(f"{name}: {value_code(value)}")
    return result
