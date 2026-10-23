# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Small composable blocks; inputs are data, output is added to a parent node."""

from decimal import Decimal

from genro_typst import color, expr, length

from .theme import DEFAULT_THEME


def money(value):
    return f"EUR {value:,.2f}"


def contact_card(parent, *, label, name, details, theme=DEFAULT_THEME):
    card = parent.block(width=length("100%"), inset=length("4mm"), fill=color(theme.pale))
    card.text(label.upper(), size=length("8pt"), fill=color(theme.accent))
    card.par(name)
    card.par(details)
    return card


def notice(parent, title, body, *, theme=DEFAULT_THEME):
    # All styling stays inside this block; later siblings keep their own style.
    block = parent.block(width=length("100%"), inset=length("4mm"), fill=color(theme.pale))
    block.set_rule(target="text", size=length("9pt"))
    block.strong(title)
    block.par(body)
    return block


def item_table(parent, items, *, theme=DEFAULT_THEME):
    """Repeat column headings across pages; calculate exact totals with Decimal."""
    table = parent.native_table(
        columns=[length("1fr"), length("auto"), length("auto"), length("auto"), length("auto")],
        inset=length("2.5mm"), stroke=expr("0.3pt + luma(210)"),
    )
    header = table.table_header(repeat=True)
    for title in ["Description", "Qty", "Unit", "Unit price", "Amount"]:
        header.table_cell(fill=color(theme.pale)).strong(title)
    total = Decimal(0)
    for item in items:
        amount = Decimal(str(item["quantity"])) * Decimal(item["price"])
        total += amount
        for value in [item["description"], str(item["quantity"]), item["unit"],
                      money(Decimal(item["price"])), money(amount)]:
            table.table_cell(value)
    parent.par(f"Section total: {money(total)}")
    return total


def signature(parent, *, role="Approved by", theme=DEFAULT_THEME):
    parent.v(content=length("8mm"))
    row = parent.grid(columns=[length("1fr"), length("1fr")], gutter=length("12mm"))
    for title in [role, "Date"]:
        cell = row.stack(dir=expr("ttb"), spacing=length("3mm"))
        cell.line(length=length("100%"), stroke=color(theme.accent))
        cell.text(title, size=length("8pt"))
