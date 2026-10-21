# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Shared document traversal and grammar defaults."""

from typing import Any

from genro_builders.renderer import RendererBase


class DocumentRenderer(RendererBase):
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
            for child in (node.value or [])
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
