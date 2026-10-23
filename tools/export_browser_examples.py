#!/usr/bin/env python3
# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Export editable JavaScript recipes from the shared, executable app catalog."""
import argparse
import json
from pathlib import Path

from export_app_examples import catalog
from genro_bag import Bag
from genro_builders import SourceBag

from genro_typst.native_catalog import AUTHORING_ALIASES

ROOT = Path(__file__).resolve().parents[1]


def javascript(builder):
    lines = ["const builder = new TypstBuilder();"]
    sequence = 0

    def literal(value):
        nonlocal sequence
        if isinstance(value, Bag):
            name = f"data{sequence}"
            sequence += 1
            lines.append(f"const {name} = new Bag();")
            for node in value:
                content = literal(node.value)
                lines.append(f"{name}.setItem({json.dumps(node.label)}, {content});")
            return name
        if isinstance(value, dict):
            if set(value) == {"$typst"}:
                return f"expr({json.dumps(value['$typst'])})"
            return "{ " + ", ".join(f"{json.dumps(k)}: {literal(v)}" for k, v in value.items()) + " }"
        if isinstance(value, (tuple, list)):
            return "[" + ", ".join(map(literal, value)) + "]"
        return json.dumps(value, ensure_ascii=False)

    for node in builder.data:
        value = literal(node.value)
        lines.append(f"builder.data.setItem({json.dumps(node.label)}, {value});")

    def walk(source, parent):
        nonlocal sequence
        for node in source:
            name = "doc" if node.node_tag == "document" else f"node{sequence}"
            sequence += 1
            attrs = literal(dict(node.attr))
            method = AUTHORING_ALIASES.get(node.node_tag, node.node_tag)
            call = f"{parent}.{method}({attrs})"
            if isinstance(node.value, SourceBag) and len(node.value):
                lines.append(f"const {name} = {call};")
                walk(node.value, name)
            else:
                lines.append(f"{call};")

    walk(builder.source, "builder.root")
    return "\n".join(lines) + "\n"


def export():
    data = catalog()
    for entry in data["examples"]:
        python = entry.pop("code").replace(
            "        # Edit the recipe: the preview updates automatically.\n", ""
        )
        entry["python"] = python + '\n\nif __name__ == "__main__":\n    Document.run()\n'
        namespace = {"__name__": "browser_recipe"}
        # Only execute the repository's own recipes, never external input.
        exec(entry["python"], namespace)  # noqa: S102 - trusted repository recipes
        builder = namespace["Document"]()
        builder.create()
        entry["description"] = entry["description"].replace("Python recipe", "JavaScript recipe")
        entry["code"] = "// " + entry["description"] + "\n" + javascript(builder)
        entry["source"] = builder.render()
    welcome = (ROOT / "js/examples/browser/welcome.typ.py").read_text()
    namespace = {"__name__": "browser_recipe"}
    exec(welcome, namespace)  # noqa: S102 - trusted repository recipe
    builder = namespace["Document"]()
    builder.create()
    data["welcome"] = {"python": welcome, "source": builder.render()}
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "js/examples/browser/catalog.json"
    content = json.dumps(export(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not target.exists() or target.read_text() != content:
            parser.exit(1, "Run python tools/export_browser_examples.py to update browser recipes.\n")
    else:
        target.write_text(content)
