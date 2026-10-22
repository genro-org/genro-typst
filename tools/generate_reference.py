#!/usr/bin/env python3
"""Regenerate the native API reference and machine-readable catalog."""

from __future__ import annotations

import argparse
import ast
import json
import sys
import textwrap
from pathlib import Path

from genro_typst.native_catalog import NATIVE, SPECIAL

ROOT = Path(__file__).resolve().parents[1]


def reference() -> tuple[str, str]:
    lines = [
        "# Native element reference",
        "",
        "Generated from `native_catalog.py` by `tools/generate_reference.py`. Do not edit by hand.",
        "",
        f"**{len(NATIVE)} native calls**, verified with Typst **0.15.0**, alongside the language",
        "constructs below and the eight legacy business-document elements.",
        "",
        "For parameter types and defaults, follow the links",
        "to the official documentation. Online pages may describe newer",
        "versions: this project's executable reference remains Typst 0.15.0.",
        "",
        "## Common signature",
        "",
        "```python",
        "node.heading(content=None, args=None, options=None, **typst_parameters)",
        "```",
        "",
        "`content` also accepts the first positional argument (`node.heading('Title')`).",
        "`args` is a list of Typst positional arguments; `options` supports names that",
        "collide with builder parameters. Additional parameters are forwarded to Typst:",
        "the compiler validates names and types beyond the checks in the Python schema.",
        "",
        "| Mode | Meaning |",
        "|---|---|",
        "| `body` | Initial text and children form one content value; no implicit spaces between children. |",
        "| `items` | Each child becomes a separate argument, such as a cell. |",
        "| `args` | Arguments and children are passed separately, following the function's types. |",
        "| `value` | Initial content is a positional value, such as a URL or path; children form an optional body. |",
        "| `leaf` | No content or children; `args` and named parameters remain available. |",
        "",
        "Strings remain strings. Use `length`, `color`, `label`, `expr` and `markup`",
        "for non-text Typst values. Underscored methods map to dotted",
        "Typst paths (`table_cell` → `table.cell`); parameter underscores",
        "become hyphens (`column_gutter` → `column-gutter`).",
        "",
    ]
    entries = []
    for section in dict.fromkeys(section for _, _, section in NATIVE.values()):
        url = f"https://typst.app/docs/reference/{'pdf' if section == 'pdf' else section}/"
        lines += [
            f"## {section}",
            "",
            f"[Official reference]({url})",
            "",
            "| Builder method (verified example) | Typst function | Mode |",
            "|---|---|---|",
        ]
        for tag, (function, mode, group) in NATIVE.items():
            if group != section:
                continue
            lines.append(f"| [`{tag}`](catalog-examples.md#{tag}) | `{function}` | `{mode}` |")
            entries.append({"tag": tag, "function": function, "mode": mode, "section": group})
        lines += [""]
    lines += [
        "## Language constructs",
        "",
        ", ".join(f"`{s}`" for s in SPECIAL),
        "",
        "Signatures, examples and limits are described in the [guide](typst-guide.md).",
        "",
    ]
    catalog = {
        "typst_version": "0.15.0",
        "native_elements": entries,
        "language_elements": list(SPECIAL),
    }
    return "\n".join(lines), json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def examples() -> str:
    # Development-only fixtures: no test dependency is imported by the package.
    sys.path.insert(0, str(ROOT / "tests"))
    from native_cases import CASES, build_case, example_python

    if set(CASES) != set(NATIVE):
        raise ValueError("Every catalog entry needs an explicit executable example")
    lines = [
        "# Verified catalog examples",
        "",
        "Generated from `tests/native_cases.py` by `tools/generate_reference.py`.",
        "Every recipe is executed in tests; its source compiles to PDF and SVG",
        "with Typst 0.15.0. SVGs match the handwritten Typst reference",
        "in the same context. See [verification](verification.md).",
        "",
        "Recipes are self-contained except for the local files below. To compile:",
        "",
        "```python",
        "from pathlib import Path",
        "from genro_typst.compiler import TypstEngine",
        'result = TypstEngine().compile(source, root=Path("assets"), preview=True)',
        'Path("example.pdf").write_bytes(result.pdf)',
        "```",
        "",
        "Create the `assets` directory. `image` requires `assets/logo.svg`:",
        "",
        "```xml",
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">',
        '  <circle cx="10" cy="10" r="8" fill="blue"/>',
        "</svg>",
        "```",
        "",
        "`cite` and `bibliography` require `assets/refs.yml`:",
        "",
        "```yaml",
        "manual:",
        "  type: Book",
        "  title: Test manual",
        "  author: Example, Alice",
        "  date: 2026",
        "```",
        "",
        "Python and JavaScript examples use the same short method names. Only",
        "`typst_columns`, `typst_move` and `typst_label` need qualification to avoid",
        "SourceBag collisions. `typst_code` and `typst_markup` are actual element names.",
        "`expr` marks explicit Typst values; dictionaries and lists remain Python data.",
        "",
    ]
    for tag in NATIVE:
        case = CASES[tag]
        builder, _, reference = build_case(case)
        lines += [
            f"## {tag}",
            "",
            f"Case context: `{case.context}`.",
            "",
            "```python",
            example_python(builder),
            "```",
            "",
            "Independent Typst reference:",
            "",
            "```typst",
            reference.rstrip(),
            "```",
            "",
        ]
    return "\n".join(lines)


def grammar_api() -> str:
    """Read declaration signatures before @element replaces them with markers."""
    lines = [
        "Declared grammar signatures",
        "===========================",
        "",
        "Generated from the Python grammar declarations. Do not edit by hand.",
        "Call these methods on source nodes; they are not module-level functions.",
        "Language constructs use keyword arguments. For ``label``, use the",
        "``typst_label`` alias to avoid the SourceBag property with that name.",
        "See :doc:`typst-guide` for usage and :doc:`native-reference` for native calls.",
        "",
    ]
    for filename, title in [
        ("typst_elements.py", "Legacy document elements"),
        ("native_elements.py", "Language constructs"),
    ]:
        lines += [title, "-" * len(title), ""]
        tree = ast.parse((ROOT / "src" / "genro_typst" / filename).read_text())
        for cls in tree.body:
            if not isinstance(cls, ast.ClassDef):
                continue
            for method in cls.body:
                if not isinstance(method, ast.FunctionDef):
                    continue
                method.args.args = [a for a in method.args.args if a.arg != "self"]
                for node in ast.walk(method.args):
                    if isinstance(node, ast.arg):
                        node.annotation = None
                lines += [f".. py:function:: {method.name}({ast.unparse(method.args)})", ""]
                doc = ast.get_docstring(method) or ""
                if "\n\nArgs:\n" in doc:
                    summary, arguments = doc.split("\n\nArgs:\n", 1)
                    fields = []
                    for line in arguments.splitlines():
                        if line.startswith("    ") and not line.startswith("        "):
                            name, description = line.strip().split(":", 1)
                            fields.append(f":param {name}:{description}")
                        elif line.strip():
                            fields[-1] += " " + line.strip()
                    doc = summary + "\n\n" + "\n".join(fields)
                lines += [textwrap.indent(doc, "   "), ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    check = parser.parse_args().check
    markdown, catalog = reference()
    for name, content in [
        ("native-reference.md", markdown),
        ("native-catalog.json", catalog),
        ("catalog-examples.md", examples()),
        ("grammar-api.rst", grammar_api()),
    ]:
        path = ROOT / "docs" / name
        if check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"Regenerate {path} with tools/generate_reference.py")
        else:
            path.write_text(content)


if __name__ == "__main__":
    main()
