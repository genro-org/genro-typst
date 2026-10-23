# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Page furniture composed with the same Python builder as the document body."""

from genro_typst import TypstBuilder, color, expr, length

from .theme import DEFAULT_THEME


def content(draw, *args, **kwargs):
    """Capture a component as a Typst content value for header/footer options.

    Only builder-generated source becomes an expression. User data still goes
    through text() and its literal escaping. This helper belongs to the example
    library; it is not a new Genro Typst API.
    """
    class Fragment(TypstBuilder):
        def main(self, root):
            draw(root.scope(), *args, **kwargs)

    fragment = Fragment()
    fragment.create()
    return expr(fragment.render())


def letterhead(parent, *, theme, reference):
    parent.set_rule(target="text", font=theme.font, size=length("9pt"), fill=color(theme.accent))
    row = parent.grid(columns=[length("1fr"), length("auto")])
    row.strong(theme.company)
    row.text(reference)
    parent.line(length=length("100%"), stroke={"thickness": length("0.5pt"), "paint": color(theme.accent)})


def page_footer(parent, *, theme):
    parent.set_rule(target="text", font=theme.font, size=length("8pt"), fill=color("gray"))
    row = parent.grid(columns=[length("1fr"), length("auto")])
    row.text(f"{theme.company} · Technical services")
    row.context().text(content=expr('counter(page).display("1 / 1", both: true)'))


def branded_document(root, *, title, reference, theme=DEFAULT_THEME):
    doc = root.document(
        paper="a4", margin="22mm",
        metadata={"title": title, "author": [theme.company]},
        page_options={
            "header": content(letterhead, theme=theme, reference=reference),
            "footer": content(page_footer, theme=theme),
        },
    )
    doc.set_rule(target="text", font=theme.font, size=length("10pt"), lang="en")
    doc.set_rule(target="par", leading=length("0.7em"))
    doc.show_rule(selector="heading", target="text", fill=color(theme.accent))
    return doc
