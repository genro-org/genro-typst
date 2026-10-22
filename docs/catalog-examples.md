# Verified catalog examples

Generated from `tests/native_cases.py` by `tools/generate_reference.py`.
Every recipe is executed in tests; its source compiles to PDF and SVG
with Typst 0.15.0. SVGs match the handwritten Typst reference
in the same context. See [verification](verification.md).

Recipes are self-contained except for the local files below. To compile:

```python
from pathlib import Path
from genro_typst.compiler import TypstEngine
result = TypstEngine().compile(source, root=Path("assets"), preview=True)
Path("example.pdf").write_bytes(result.pdf)
```

Create the `assets` directory. `image` requires `assets/logo.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">
  <circle cx="10" cy="10" r="8" fill="blue"/>
</svg>
```

`cite` and `bibliography` require `assets/refs.yml`:

```yaml
manual:
  type: Book
  title: Test manual
  author: Example, Alice
  date: 2026
```

Python and JavaScript examples use the same short method names. Only
`typst_columns`, `typst_move` and `typst_label` need qualification to avoid
SourceBag collisions. `typst_code` and `typst_markup` are actual element names.
`expr` marks explicit Typst values; dictionaries and lists remain Python data.

## text

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.text(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#text("Example")
#text("After")
```

## underline

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.underline(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#underline("Example")
#text("After")
```

## overline

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.overline(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#overline("Example")
#text("After")
```

## strike

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.strike(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#strike("Example")
#text("After")
```

## highlight

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.highlight(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#highlight("Example")
#text("After")
```

## smallcaps

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.smallcaps(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#smallcaps("Example")
#text("After")
```

## sub

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.sub(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#sub("Example")
#text("After")
```

## super

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.super(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#super("Example")
#text("After")
```

## lower

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.lower(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#lower([Example])
#text("After")
```

## upper

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.upper(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#upper([Example])
#text("After")
```

## raw

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.raw(content='#literal <x>', lang='typst')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#raw("#literal <x>", lang: "typst")
#text("After")
```

## lorem

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.lorem(content=12)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#lorem(12)
#text("After")
```

## linebreak

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.linebreak(justify=True)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#linebreak(justify: true)
#text("After")
```

## smartquote

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.smartquote(double=False)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#smartquote(double: false)
#text("After")
```

## heading

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.heading(content='Heading', level=2)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#heading(level: 2, "Heading")
#text("After")
```

## strong

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.strong(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#strong("Example")
#text("After")
```

## emph

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.emph(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#emph("Example")
#text("After")
```

## par

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.par(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#par("Example")
#text("After")
```

## quote

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.quote(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#quote("Example")
#text("After")
```

## figure

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.figure(caption=expr('[Caption\n]'))
node2.rect(width=expr('10mm'), height=expr('5mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#figure(rect(width: 10mm, height: 5mm), caption: [Caption])
#text("After")
```

## footnote

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.footnote(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#footnote("Example")
#text("After")
```

## title

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.title(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#title("Example")
#text("After")
```

## list

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.list(args=['One', 'Two'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#list("One", "Two")
#text("After")
```

## enum

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.enum(args=['One', 'Two'], start=3)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#enum(start: 3, "One", "Two")
#text("After")
```

## terms

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.terms()
node2.terms_item(args=['API', 'Interface'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#terms(terms.item("API", "Interface"))
#text("After")
```

## list_item

Case context: `list`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.list()
node2.list_item(content='Item')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#list(list.item("Item"))
#text("After")
```

## enum_item

Case context: `enum`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.enum()
node2.enum_item(content='Item')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#enum(enum.item("Item"))
#text("After")
```

## terms_item

Case context: `terms`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.terms()
node2.terms_item(args=['API', 'Interface'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#terms(terms.item("API", "Interface"))
#text("After")
```

## link

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.link(content='https://typst.app')
node2.text(content='Website')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#link("https://typst.app", [#text("Website")])
#text("After")
```

## ref

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.set_rule(target='heading', numbering='1.')
doc.heading(content='Target')
doc.typst_label(name='target')
doc.ref(content=expr('label("target")'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#set heading(numbering: "1.")
#heading("Target")
#label("target")
#ref(label("target"))
#text("After")
```

## cite

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.cite(content=expr('label("manual")'))
doc.bibliography(content='refs.yml')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#cite(label("manual"))
#bibliography("refs.yml")
#text("After")
```

## bibliography

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.bibliography(content='refs.yml', full=True)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#bibliography("refs.yml", full: true)
#text("After")
```

## numbering

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.numbering(args=['1.a', 2, 3])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#numbering("1.a", 2, 3)
#text("After")
```

## outline

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.set_rule(target='heading', numbering='1.')
doc.heading(content='Target')
doc.typst_label(name='target')
doc.outline(title=expr('[Contents\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#set heading(numbering: "1.")
#heading("Target")
#label("target")
#outline(title: [Contents])
#text("After")
```

## parbreak

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.parbreak()
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#parbreak()
#text("After")
```

## divider

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.divider()
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#divider()
#text("After")
```

## table_header

Case context: `table`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.native_table(columns=2)
node3 = node2.table_header()
node3.table_cell(content='Span', colspan=2)
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#table(columns: 2, table.header(table.cell("Span", colspan: 2)), text("A"), text("B"))
#text("After")
```

## table_footer

Case context: `table`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.native_table(columns=2)
node2.text(content='A')
node2.text(content='B')
node5 = node2.table_footer()
node5.table_cell(content='Span', colspan=2)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#table(columns: 2, text("A"), text("B"), table.footer(table.cell("Span", colspan: 2)))
#text("After")
```

## table_cell

Case context: `table`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.native_table(columns=2)
node2.table_cell(content='Span', colspan=2)
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#table(columns: 2, table.cell("Span", colspan: 2), text("A"), text("B"))
#text("After")
```

## table_hline

Case context: `table`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.native_table(columns=2)
node2.table_hline(stroke=expr('2pt + blue'))
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#table(columns: 2, table.hline(stroke: 2pt + blue), text("A"), text("B"))
#text("After")
```

## table_vline

Case context: `table`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.native_table(columns=2)
node2.table_vline(x=1, stroke=expr('2pt + blue'))
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#table(columns: 2, table.vline(x: 1, stroke: 2pt + blue), text("A"), text("B"))
#text("After")
```

## native_table

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.native_table(columns=2, args=['A', 'B'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#table(columns: 2, "A", "B")
#text("After")
```

## align

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.align(args=[expr('center')], content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#align(center, "Example")
#text("After")
```

## block

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.block(content='Example', inset=expr('2mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#block(inset: 2mm, "Example")
#text("After")
```

## box

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.box(content='Example', width=expr('30mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#box(width: 30mm, "Example")
#text("After")
```

## columns

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.typst_columns(args=[2], content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#columns(2, "Example")
#text("After")
```

## hide

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.hide(content='Invisible')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#hide("Invisible")
#text("After")
```

## move

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.typst_move(content='Example', dx=expr('2mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#move(dx: 2mm, "Example")
#text("After")
```

## pad

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.pad(args=[expr('2mm')], content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#pad(2mm, "Example")
#text("After")
```

## page

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.page(content='Example', paper='a5')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#page(paper: "a5", "Example")
#text("After")
```

## place

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.place(args=[expr('top + right')], content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#place(top + right, "Example")
#text("After")
```

## repeat

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.repeat(content='.')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#repeat(".")
#text("After")
```

## rotate

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.rotate(args=[expr('10deg')], content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#rotate(10deg, "Example")
#text("After")
```

## scale

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.scale(x=expr('120%'), content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#scale(x: 120%, "Example")
#text("After")
```

## skew

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.skew(ax=expr('10deg'), content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#skew(ax: 10deg, "Example")
#text("After")
```

## grid

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.grid(columns=2, args=['A', 'B'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#grid(columns: 2, "A", "B")
#text("After")
```

## stack

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.stack(dir=expr('ltr'), spacing=expr('2mm'), args=['A', 'B'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#stack(dir: ltr, spacing: 2mm, "A", "B")
#text("After")
```

## grid_header

Case context: `grid`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.grid(columns=2)
node3 = node2.grid_header()
node3.grid_cell(content='Span', colspan=2)
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#grid(columns: 2, grid.header(grid.cell("Span", colspan: 2)), text("A"), text("B"))
#text("After")
```

## grid_footer

Case context: `grid`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.grid(columns=2)
node2.text(content='A')
node2.text(content='B')
node5 = node2.grid_footer()
node5.grid_cell(content='Span', colspan=2)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#grid(columns: 2, text("A"), text("B"), grid.footer(grid.cell("Span", colspan: 2)))
#text("After")
```

## grid_cell

Case context: `grid`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.grid(columns=2)
node2.grid_cell(content='Span', colspan=2)
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#grid(columns: 2, grid.cell("Span", colspan: 2), text("A"), text("B"))
#text("After")
```

## pagebreak

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.pagebreak()
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#pagebreak()
#text("After")
```

## colbreak

Case context: `columns`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.typst_columns(args=[2])
node2.text(content='Left')
node2.colbreak()
node2.text(content='Right')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#columns(2, [#text("Left")#colbreak()#text("Right")])
#text("After")
```

## grid_hline

Case context: `grid`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.grid(columns=2)
node2.grid_hline(stroke=expr('2pt + blue'))
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#grid(columns: 2, grid.hline(stroke: 2pt + blue), text("A"), text("B"))
#text("After")
```

## grid_vline

Case context: `grid`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.grid(columns=2)
node2.grid_vline(x=1, stroke=expr('2pt + blue'))
node2.text(content='A')
node2.text(content='B')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#grid(columns: 2, grid.vline(x: 1, stroke: 2pt + blue), text("A"), text("B"))
#text("After")
```

## h

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.h(content=expr('5mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#h(5mm)
#text("After")
```

## v

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.v(content=expr('5mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#v(5mm)
#text("After")
```

## measure

Case context: `measure`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.context()
node3 = node2.call(function='repr', mode='args')
node3.measure(content='Example')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#context [#repr(measure("Example"))]
#text("After")
```

## native_layout

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.native_layout(content=expr('size => [Width: #size.width]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#layout(size => [Width: #size.width])
#text("After")
```

## circle

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.circle(content='G', fill=expr('rgb("#eeeeee")'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#circle(fill: rgb("#eeeeee"), "G")
#text("After")
```

## ellipse

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.ellipse(content='G', fill=expr('rgb("#eeeeee")'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#ellipse(fill: rgb("#eeeeee"), "G")
#text("After")
```

## rect

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.rect(content='G', fill=expr('rgb("#eeeeee")'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#rect(fill: rgb("#eeeeee"), "G")
#text("After")
```

## square

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.square(content='G', fill=expr('rgb("#eeeeee")'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#square(fill: rgb("#eeeeee"), "G")
#text("After")
```

## image

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.image(content='logo.svg', width=expr('10mm'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#image("logo.svg", width: 10mm)
#text("After")
```

## line

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.line(start=[expr('0pt'), expr('0pt')], end=[expr('10mm'), expr('10mm')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#line(start: (0pt, 0pt), end: (10mm, 10mm))
#text("After")
```

## polygon

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.polygon(args=[[expr('0pt'), expr('0pt')], [expr('10mm'), expr('0pt')], [expr('10mm'), expr('10mm')]], fill=expr('blue'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#polygon((0pt, 0pt), (10mm, 0pt), (10mm, 10mm), fill: blue)
#text("After")
```

## curve

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.curve()
node2.curve_move(args=[[expr('0pt'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('10mm')]])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#curve(curve.move((0pt, 0pt)), curve.line((10mm, 10mm)))
#text("After")
```

## curve_move

Case context: `curve`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.curve()
node2.curve_move(args=[[expr('0pt'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('0pt')]])
node2.curve_move(args=[[expr('10mm'), expr('0pt')]])
node2.curve_line(args=[[expr('0pt'), expr('10mm')]])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#curve(curve.move((0pt, 0pt)), curve.line((10mm, 0pt)), curve.move((10mm, 0pt)), curve.line((0pt, 10mm)))
#text("After")
```

## curve_line

Case context: `curve`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.curve()
node2.curve_move(args=[[expr('0pt'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('10mm')]])
node2.curve_line(args=[[expr('0pt'), expr('10mm')]])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#curve(curve.move((0pt, 0pt)), curve.line((10mm, 0pt)), curve.line((10mm, 10mm)), curve.line((0pt, 10mm)))
#text("After")
```

## curve_quad

Case context: `curve`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.curve()
node2.curve_move(args=[[expr('0pt'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('0pt')]])
node2.curve_quad(args=[[expr('10mm'), expr('10mm')], [expr('10mm'), expr('0pt')]])
node2.curve_line(args=[[expr('0pt'), expr('10mm')]])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#curve(curve.move((0pt, 0pt)), curve.line((10mm, 0pt)), curve.quad((10mm, 10mm), (10mm, 0pt)), curve.line((0pt, 10mm)))
#text("After")
```

## curve_cubic

Case context: `curve`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.curve()
node2.curve_move(args=[[expr('0pt'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('0pt')]])
node2.curve_cubic(args=[[expr('10mm'), expr('10mm')], [expr('10mm'), expr('0pt')], [expr('0pt'), expr('10mm')]])
node2.curve_line(args=[[expr('0pt'), expr('10mm')]])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#curve(curve.move((0pt, 0pt)), curve.line((10mm, 0pt)), curve.cubic((10mm, 10mm), (10mm, 0pt), (0pt, 10mm)), curve.line((0pt, 10mm)))
#text("After")
```

## curve_close

Case context: `curve`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.curve()
node2.curve_move(args=[[expr('0pt'), expr('0pt')]])
node2.curve_line(args=[[expr('10mm'), expr('0pt')]])
node2.curve_close()
node2.curve_line(args=[[expr('0pt'), expr('10mm')]])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#curve(curve.move((0pt, 0pt)), curve.line((10mm, 0pt)), curve.close(), curve.line((0pt, 10mm)))
#text("After")
```

## math_equation

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.math_equation(content=expr('[$x + y$\n]'), block=True)
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [$x + y$])
#text("After")
```

## math_upright

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_upright(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.upright([$x$])])
#text("After")
```

## math_italic

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_italic(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.italic([$x$])])
#text("After")
```

## math_bold

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_bold(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.bold([$x$])])
#text("After")
```

## math_serif

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_serif(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.serif([$x$])])
#text("After")
```

## math_sans

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_sans(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.sans([$x$])])
#text("After")
```

## math_cal

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_cal(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.cal([$x$])])
#text("After")
```

## math_frak

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_frak(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.frak([$x$])])
#text("After")
```

## math_mono

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_mono(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.mono([$x$])])
#text("After")
```

## math_bb

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_bb(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.bb([$x$])])
#text("After")
```

## math_display

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_display(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.display([$x$])])
#text("After")
```

## math_inline

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_inline(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.inline([$x$])])
#text("After")
```

## math_script

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_script(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.script([$x$])])
#text("After")
```

## math_sscript

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_sscript(content=expr('[$x$\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.sscript([$x$])])
#text("After")
```

## math_frac

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_frac(args=[expr('[$x$\n]'), expr('[$y$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.frac([$x$], [$y$])])
#text("After")
```

## math_root

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_root(args=['3', expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.root("3", [$x$])])
#text("After")
```

## math_sqrt

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_sqrt(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.sqrt([$x$])])
#text("After")
```

## math_binom

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_binom(args=['n', 'k'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.binom("n", "k")])
#text("After")
```

## math_vec

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_vec(args=['1', '2'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.vec("1", "2")])
#text("After")
```

## math_mat

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_mat(args=[['1', '2'], ['3', '4']])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.mat(("1", "2"), ("3", "4"))])
#text("After")
```

## math_cases

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_cases(args=[expr('[$x & x >= 0$\n]'), expr('[$-x & x < 0$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.cases([$x & x >= 0$], [$-x & x < 0$])])
#text("After")
```

## math_lr

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_lr(args=[expr('[$(x)$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.lr([$(x)$])])
#text("After")
```

## math_attach

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_attach(args=[expr('[$x$\n]')], t=expr('[2\n]'), b=expr('[i\n]'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.attach([$x$], t: [2], b: [i])])
#text("After")
```

## math_accent

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_accent(args=[expr('[$x$\n]'), '^'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.accent([$x$], "^")])
#text("After")
```

## math_cancel

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_cancel(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.cancel([$x$])])
#text("After")
```

## math_class

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_class(args=['relation', expr('[$=$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.class("relation", [$=$])])
#text("After")
```

## math_op

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_op(args=['custom'])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.op("custom")])
#text("After")
```

## math_limits

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_limits(args=[expr('sym.sum')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.limits(sym.sum)])
#text("After")
```

## math_scripts

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_scripts(args=[expr('sym.sum')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.scripts(sym.sum)])
#text("After")
```

## math_abs

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_abs(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.abs([$x$])])
#text("After")
```

## math_norm

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_norm(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.norm([$x$])])
#text("After")
```

## math_floor

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_floor(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.floor([$x$])])
#text("After")
```

## math_ceil

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_ceil(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.ceil([$x$])])
#text("After")
```

## math_round

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_round(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.round([$x$])])
#text("After")
```

## math_stretch

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_stretch(args=[expr('sym.arrow.r')], size=expr('200%'))
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.stretch(sym.arrow.r, size: 200%)])
#text("After")
```

## math_underbrace

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_underbrace(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.underbrace([$x$])])
#text("After")
```

## math_overbrace

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_overbrace(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.overbrace([$x$])])
#text("After")
```

## math_underbracket

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_underbracket(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.underbracket([$x$])])
#text("After")
```

## math_overbracket

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_overbracket(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.overbracket([$x$])])
#text("After")
```

## math_underline

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_underline(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.underline([$x$])])
#text("After")
```

## math_overline

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_overline(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.overline([$x$])])
#text("After")
```

## math_underparen

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_underparen(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.underparen([$x$])])
#text("After")
```

## math_overparen

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_overparen(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.overparen([$x$])])
#text("After")
```

## math_undershell

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_undershell(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.undershell([$x$])])
#text("After")
```

## math_overshell

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_overshell(args=[expr('[$x$\n]')])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.overshell([$x$])])
#text("After")
```

## math_primes

Case context: `math`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
node2 = doc.math_equation(block=True)
node2.math_primes(args=[3])
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#math.equation(block: true, [#math.primes(3)])
#text("After")
```

## metadata

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.metadata(content={'answer': 42})
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#metadata(("answer": 42,))
#text("After")
```

## pdf_artifact

Case context: `document`.

```python
from genro_typst import TypstBuilder, expr

builder = TypstBuilder()
doc = builder.source.document()
doc.text(content='Before')
doc.pdf_artifact(content='Decoration')
doc.text(content='After')

source = builder.render()
```

Independent Typst reference:

```typst
#set page(paper: "a4", flipped: false, margin: 15mm)
#text("Before")
#pdf.artifact("Decoration")
#text("After")
```
