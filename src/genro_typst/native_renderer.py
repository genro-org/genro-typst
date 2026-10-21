# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Rendering shared by native elements and explicit language constructs."""

from __future__ import annotations

from typing import Any

from genro_typst.native_catalog import NATIVE
from genro_typst.typst_values import typst_string
from genro_typst.values import identifier, named_arguments, value_code


def content_block(children: list[str], content: Any = None) -> str:
    """Adjacent inline elements stay adjacent; statements end with a newline."""
    parts = [f"#{value_code(content)}"] if content is not None else []
    for child in children:
        if not child:
            continue
        statement = child.startswith(("set ", "show ", "let ", "import "))
        parts.append(f"#{child}" + (";\n" if statement else ""))
    return "[" + "".join(parts) + "]"


def _options(attrs: dict[str, Any], reserved: set[str]) -> dict[str, Any]:
    options = attrs.get("options")
    if options is None:
        options = {}
    if not isinstance(options, dict):
        raise TypeError("options must be a dictionary")
    extra = {k: v for k, v in attrs.items() if k not in reserved and k != "_meta"}
    duplicate = set(options) & set(extra)
    if duplicate:
        raise ValueError(f"Duplicate options: {sorted(duplicate)}")
    return {**options, **extra}


def render_call(function: str, mode: str, children: list[str], attrs: dict[str, Any]) -> str:
    identifier(function)
    if mode not in ("body", "items", "args", "value", "leaf"):
        raise ValueError(f"Unknown call mode: {mode}")
    args = attrs.get("args")
    if args is None:
        args = []
    if not isinstance(args, (list, tuple)):
        raise TypeError("args must be a list or tuple")
    parts = [value_code(a) for a in args]
    options = _options(attrs, {"content", "args", "options"})
    parts.extend(named_arguments(options))
    content = attrs.get("content")
    if mode == "body":
        if content is not None or children:
            parts.append(content_block(children, content))
    elif mode in ("items", "args"):
        if content is not None:
            parts.append(value_code(content))
        for child in children:
            if child.startswith(("set ", "show ", "let ", "import ")):
                raise ValueError("Put rules inside a scope, not directly among call arguments")
            parts.append(child)
    elif mode == "value":
        if content is not None:
            parts.append(value_code(content))
        if children:
            parts.append(content_block(children))
    elif children or content is not None:
        raise ValueError(f"{function} does not accept child content")
    return f"{function}({', '.join(parts)})"


def render_native(tag: str, children: list[str], attrs: dict[str, Any]) -> str:
    if tag in NATIVE:
        function, mode, _section = NATIVE[tag]
        return render_call(function, mode, children, attrs)
    if tag == "call":
        params = {k: v for k, v in attrs.items() if k not in ("function", "mode")}
        return render_call(attrs["function"], attrs["mode"], children, params)
    if tag in ("scope", "context"):
        return ("context " if tag == "context" else "") + content_block(children)
    if tag == "set_rule":
        options = _options(attrs, {"target", "options"})
        return f"set {identifier(attrs['target'])}({', '.join(named_arguments(options))})"
    if tag == "show_rule":
        selector = attrs["selector"]
        selector = identifier(selector) if isinstance(selector, str) else value_code(selector)
        options = _options(attrs, {"selector", "transform", "target", "options"})
        if attrs["target"] is not None:
            if attrs["transform"] is not None:
                raise ValueError("A show rule takes either transform or target, not both")
            transform = f"set {identifier(attrs['target'])}({', '.join(named_arguments(options))})"
        else:
            if attrs["transform"] is None or options:
                raise ValueError(
                    "A transformational show rule requires transform and no set options"
                )
            transform = value_code(attrs["transform"])
        return f"show {selector}: {transform}"
    if tag == "equation":
        options = {k: v for k, v in attrs.items() if k not in ("formula", "_meta")}
        return f"math.equation({', '.join(named_arguments(options))}, ${attrs['formula']}$)"
    if tag == "label":
        return f"label({typst_string(attrs['name'])})"
    if tag == "let":
        name = identifier(attrs["name"])
        if "." in name:
            raise ValueError("A let binding needs a simple name")
        return f"let {name} = {value_code(attrs['value'])}"
    if tag == "import_module":
        statement = f"import {typst_string(attrs['path'])}"
        alias = attrs["alias"]
        if alias is not None:
            if "." in identifier(alias):
                raise ValueError("An import alias needs a simple name")
            statement += f" as {alias}"
        names = attrs["names"]
        if names:
            if names != ["*"] and any("." in identifier(n) for n in names):
                raise ValueError("An imported binding needs a simple name")
            statement += ": " + ("*" if names == ["*"] else ", ".join(identifier(n) for n in names))
        return statement
    if tag == "include":
        return f"include {typst_string(attrs['path'])}"
    if tag == "typst_code":
        return "{" + str(attrs["code"]) + "\n}"
    if tag == "typst_markup":
        return "[" + str(attrs["source"]) + "\n]"
    raise ValueError(f"Unknown Typst element: {tag}")
