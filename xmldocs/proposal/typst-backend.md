<!-- generated from typst-backend.xml by xmldocs: do not edit, edit the XML -->

## Printing with genro-builders and Typst
*Proposal · proposal/typst-backend · 2026-10-20 · draft*

### Problem

Business documents (invoices, delivery notes, quotes, labels) and diagrams currently go through HTML-to-PDF conversion or ReportLab in genro-print.

Typst is a typesetting engine written in Rust and licensed under Apache-2.0. It compiles text source to PDF, SVG and PNG.

This project describes documents with a genro-builders grammar and delegates typesetting to Typst.

The eventual goal is a Gramlot letterhead editor similar to GenroPy's, and a print editor for business applications: lists, pages and forms. Editors are outside this project. genro-typst supplies the grammar, persistence format and renderer.

### Current state

- `READ` `genro-print/src/genro_print/builders/print_lrc_builder.py` · 2026-10-20 — genro-print separates the grammar (builders with document, platypus, canvas, lrc, styled and charts mixins) from ReportLab renderers. Each builder exposes its renderer through the property `renderer_reportlab` and `_default_render_mode = "reportlab"`.
- `RUN` `genro-print (git status)` · 2026-10-20 — In genro-print the move from `compilers/` to `renderers/` is in the working tree, uncommitted. The latest commit is dated 2026-04-07.
- `READ` `genro-builders/src/genro_builders/contrib/svg/svg_builder.py` · 2026-10-20 — The genro-builders SVG dialect has three parts: `SvgBuilder` (grammar, `_name = "svg"`), `SvgElements` (elements declared with `@element`), `SvgRenderer` (subclass of `RendererBase`, `mode = "svg"`, method `rendered_item`) exposed by the property `renderer_svg`.

### Proposed solution

#### Principle

- **must** — The grammar describes business documents, not the Typst language. It does not wrap the entire Typst language.
- **must** — The renderer emits fixed Typst constructs. Builder users never write Typst code.

The model follows GenroPy's Layout/Row/Cell: a feature inventory with one abstract object per feature. For example, "page X of Y" is a dedicated element whose renderer emits a snippet of `context`.

#### Provisional inventory

*Features and emitted Typst constructs*

| Feature | Typst construct | Status |
|---|---|---|
| document, page (format, orientation, margins) | `set page(...)` | verified |
| repeated headers/footers, different first page | `page(header:, footer:)` + `context` | verified |
| page number X of Y | `counter(page).display()`, `counter(page).final()` in `context` | verified |
| elastic layout/row/cell | `grid` with columns `auto`, `1fr`, fixed | verified |
| paragraph, style | `text`, `par`, `set` | to be verified |
| formatted data field | Python formatting, `text` in Typst | to be verified |
| data table with repeated header | `table` + `table.header(repeat: true)` | verified |
| totals, subtotals | `table.footer` | repeated footer verified; page carryover unverified |
| keep together, page break | `block(breakable: false)`, `pagebreak()` | compiles; effect unverified |
| image | `image` | to be verified |
| barcode, QR | external package `@preview/tiaoma` | import 0.3.0 compiles |
| borders, boxes, lines | `box`, `rect`, `line`, `stroke` | to be verified |
| diagrams | SVG from the genro-builders svg dialect, included with `image` | to be verified |

#### Prototype grammar

Based on GenroPy's Layout/Row/Cell (`gnr/core/gnrhtml.py`). In the legacy system each element has an absolute position in `um` (millimeters), and `width=0`/`height=0` divides free space equally. Here layout follows the flow and can continue on the next page.

- A row without `height` takes the height of its content (`auto`). `'1fr'` is allowed only if the layout has a height.
- A width is a length, percentage or fraction: `'25mm'`, `'30%'`, `'2fr'`, `'auto'`. A number is a fraction; `width=0` means `1fr`, as in the legacy system.
- Removed: `um` and `lbl_height`. `top/left/bottom/right` become `inset`.

*Elements*

| Element | Attributes | Typst construct |
|---|---|---|
| `document` | `paper`, `flipped`, `margin` | `set page` |
| `header`, `footer` | `pages='all'|'first'|'others'` | `page(header:, footer:)` + `context` |
| `pageNumber` | `template='Page {page} of {total}'` | `counter(page)` in `context` |
| `style` | `name`, `font`, `size`, `weight`, `color`, `align` | parameters of `text`/`par` |
| `layout` | `border_width`, `border_color`, `border_style`, `row_border`, `cell_border`, `lbl_class`, `content_class`, `inset` | `grid` |
| `row` | `height`, `row_border`, `cell_border`, `lbl_class`, `content_class`, `breakable` | row of `grid` |
| `cell` | `content`, `width`, `lbl`, `lbl_class`, `content_class`, `cell_border`, `align`, `valign`, `background`, `colspan` | `grid.cell` |
| `paragraph` | `content`, `style` | `text` + `par` |
| `field` | `value`, `dtype`, `format`, `style` | Python formatting, escaped text |
| `image` | `src` (including an `SvgBuilder`), `width`, `height`, `fit` | `image` |
| `barcode` | `value`, `kind='qr'|'ean13'|'code128'` | `tiaoma` |
| `spacer`, `hline`, `pageBreak` | `height` for `spacer` | `v`, `line`, `pagebreak` |
| `table` | `data`, `headerRepeat` | `table` + `table.header(repeat: true)` |
| `column` | `field`, `name`, `width`, `dtype`, `format`, `align`, `totalize`, `subtotal`, `background`, `color` | column of `table`; `totalize` produces `table.footer` |

A `cell` can contain a nested `layout`. `colspan` does not exist in the legacy system. Attributes of `column` come from the legacy grid structure (`gnr/web/gnrbaseclasses.py`); `mm_width` becomes `width`.

Legacy names are retained: `lbl`, `lbl_class`, `content_class`, `border_width`, `row_border`, `cell_border`, `totalize`. New names use camelCase.

#### Editor constraints

1. Everything is data. Letterheads and print documents are Bags serialized with TYTX. Every grammar attribute is a value an editor can set. No element requires Python code (the legacy system required `calcRowHeight` and `prepareRow`).
2. Formatted text. The legacy system stored HTML from `ckEditor` for each region. The prototype grammar does not yet have inline elements for bold, italic or a field within a sentence.
3. Data fields. The legacy system used `$campo` in HTML, filled by `templateReplace`. Here the pointers are `^` from genro-builders; the editor offers fields from the table model.
4. Preprinted forms. Lists and pages use elastic layout. A preprinted form has fields at fixed positions in millimeters, requiring an absolute-position element (`place` with `dx`/`dy` in Typst).
5. Browser preview. The Bag-to-Typst renderer is in Python. The browser compiles Typst code with typst.ts.

*Print document types*

| Print document | Structure | Legacy |
|---|---|---|
| List | `table` + `column` | `TableScriptToHtml` with `gridStruct` |
| Page (record) | Elastic LRC | `TableScriptToHtml` with `prepareRow` |
| Form | absolute positions in mm | LRC in mm over a preprinted form |

#### Letterhead

#### How GenroPy works

- `READ` `gnrcore/packages/adm/model/htmltemplate.py` · 2026-10-20 — A letterhead is a record in `adm.htmltemplate`. The column `data` is a Bag: `main.page.{height,width,top,left,right,bottom}` in mm, `main.design` (`headline` or `sidebar`), with a size and HTML containing variables for each region: `$campo`. Document content goes into the region `center_center`.
- `READ` `gnrcore/packages/adm/model/htmltemplate.py` · 2026-10-20 — `based_on` links a letterhead to its parent; `letterheadChain` builds the chain, with each letterhead becoming an overlay. `next_letterhead` identifies the letterhead for pages after the first (`gnr/core/gnrhtml.py`, `newPage`).
- `READ` `gnrcore/packages/adm/resources/tables/htmltemplate/th_htmltemplate.py` · 2026-10-20 — The legacy editor has a form with page dimensions, a tab for `design`, a preview with resizable regions, and `ckEditor` for the selected region's HTML.

#### Proposal

```python
letterhead(name='invoice', paper='a4', flipped=False,
           margin_top='30mm', margin_bottom='20mm',
           margin_left='35mm', margin_right='15mm',
           basedOn='base')
    region(name='top', pages='first', size='30mm')    # LRC content with ^ pointers
    region(name='top', pages='others', size='15mm')
    region(name='left', size='25mm')
    region(name='background')
document(letterhead='invoice')
```

- `top` → `header`; `bottom` → `footer`; `left`, `right`, `background` → `background` with `place`; watermark → `foreground`.
- `pages='first'|'others'` replaces `next_letterhead`: `context` on `counter(page)`.
- `basedOn` replaces `based_on`: regions with the same `name` and `pages` replace those in the base; regions named `background` accumulate.
- `main.design` is removed: `headline` and `sidebar` are choices of regions.
- The letterhead is a Bag serialized with TYTX (`Bag.to_tytx`, `Bag.from_tytx`). The document loads it and grafts it into its source.

- `RUN` `scratch lh.py` · 2026-10-20 — Typst 0.15.0: different first and subsequent page headers using `context`, sidebar using `background` + `place`. Both appear in a two-page PDF.
- `RUN` `scratch lh.py` · 2026-10-20 — Typst does not enlarge the top margin for a taller header: a 40 mm header with a 10 mm margin overlaps the body. Each region's margin must be declared as a length.

A builder Bag must reload from TYTX with its tags and pass grammar validation. This is unverified.

#### Existing Typst editors

- `RUN` `github.com/Myriad-Dreamin/typst.ts` · 2026-10-20 — typst.ts compiles Typst in the browser through WASM. Apache-2.0 license, release v0.7.0 dated 2026-06-01.
- `RUN` `github.com/tyx-editor/TyX` · 2026-10-20 — Open-source visual Typst editors are young: TyX (MIT), typster (MIT), ortic/typst-wysiwyg (MIT, prototype). TyX works on TipTap JSON and compiles it into Typst code, following the same pattern as this project.

The renderer produces actual Typst code. The path is one-way: edits to Typst code do not flow back into the Bag.

#### Renderer responsibilities

- Text escaping: `#` `*` `_` `$` `@` `<` and other markup characters.
- Converting Python types to Typst types: lengths (`2cm`, `1fr`, `50%`), colors, `none`/`auto`, alignment, identifiers distinct from strings.

#### Verified Python binding

- `RUN` `venv: pip install typst` · 2026-10-20 — The PyPI package `typst` 0.15.0 bundles Typst 0.15.0 (`sys.version` in the document prints 0.15.0).
- `READ` `typst/__init__.pyi` · 2026-10-20 — Public API: `compile`, `compile_with_warnings`, `query`, `eval`, `Compiler`, `Fonts`, `FontInfo`, `TypstError`, `TypstWarning`. `compile` accepts source as bytes, a path or a string; formats `pdf`, `svg`, `png`, `html`; parameters `sys_inputs`, `pdf_standards` (including PDF/A), `timestamp`, `root`. `Compiler` accepts `font_paths`, `ignore_system_fonts`, `package_path`, `package_cache_path`.
- `RUN` `scratch probe.py` · 2026-10-20 — A three-page document with a 120-row table compiles without files: `typst.compile(bytes, format="pdf")`. First call: 0.62 s; with an existing `Compiler`: 0.014 s.
- `RUN` `scratch probe.py` · 2026-10-20 — `TypstError` exposes `message`, `hints`, `trace`.
- **must** — The binding version is pinned with `==` in `pyproject.toml`. *(Typst is pre-1.0; syntax changes between minor versions.)*

#### Browser preview

typst.ts (WASM) compiles the same source in the browser. This is unverified.

### Decisions

- **d-carryover** `open` — Should page totals (carried forward / brought forward) use `context` code generated by the renderer, or Python calculations before typesetting?
- **d-grammar** `open` — Should the grammar reuse genro-print names (`layout`, `row`, `cell`, `paragraph`, `table`) or define its own?
- **d-packages** `open` — Should external Typst packages (e.g. `tiaoma`) download on first compilation or ship with the project through `package_path`?
- **d-fonts** `open` — Should we use system fonts or ship a font directory with the project (`ignore_system_fonts=True`) for identical PDFs on every server?
- **d-inline** `open` — Should formatted text in regions and cells use inline grammar elements, or should the renderer convert the format of the text editor chosen for Gramlot?
- **d-preview** `open` — Should the Gramlot preview request Typst code from the server, or should the renderer be ported to genro-builders-js to run entirely in the browser?

### Consequences

Printing no longer depends on ReportLab or a headless browser. It depends on a pinned pre-1.0 Rust library.
