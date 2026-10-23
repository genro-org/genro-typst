# Reusable Python document blocks

A document recipe can import ordinary Python modules. Put shared page furniture,
styles, tables and sections in a package, then compose them in different recipes.
There is no special plugin registry or template language: Python supplies modules,
functions and data processing; **Typst supplies typography, pagination and rendering**.

The repository includes a three-page **technical proposal** and a **service report**
using the same component library. Try both under **Real-world documents** in the
[browser playground](browser.md). Select Python, change the recipe and watch the
shared SVG preview. Use **Python file** to edit the main recipe or any imported
module in CodeMirror, and **Download file** to save the selected file. The JavaScript tab is the expanded equivalent document tree, not a port
of the Python package's component API.

For a step-by-step edit of the footer and pricing data, follow the
[module editor walkthrough](browser.md#walkthrough-change-the-shared-footer).

## Organize a small component library

```text
05_reusable_blocks/
├── company_blocks/
│   ├── __init__.py       # Public imports
│   ├── theme.py          # Immutable brand settings
│   ├── chrome.py         # Letterhead, page footer and document defaults
│   └── sections.py       # Contact card, priced table, notice and signature
├── proposal_data.py     # Demonstration records
├── proposal.typ.py      # A multipage technical proposal
└── service_report.typ.py # Another composition of the same blocks
```

The directory containing a recipe is available for sibling imports both with
direct Python execution and the Genro Typst CLI. From the checkout root:

```bash
python examples/05_reusable_blocks/proposal.typ.py
python examples/05_reusable_blocks/proposal.typ.py --pdf -o output/proposal.pdf
genro-typst examples/05_reusable_blocks/service_report.typ.py --svg -o output/service.svg
```

Install the `pdf` extra for PDF/SVG compilation. Keep the `company_blocks` directory
and `proposal_data.py` alongside a downloaded recipe, preserving the paths.
In the playground, every Python run uses the current recipe and all edited
modules. For example, change `company_blocks/chrome.py` to update the shared
preview without touching the main recipe. Drafts remain separate for each
example and last until the page reloads. To change the library for both
documents permanently, save the module back to the shared local package.

## Compose documents with functions

A body component takes a parent builder node, explicit data and a theme, and adds
its own children. It may return its container for further customization, or a
calculated result such as a table total. It does not own the entire document or
write output files.

```{literalinclude} ../examples/05_reusable_blocks/proposal.typ.py
:language: python
```

Here Python groups the priced sections, calculates totals with `Decimal` and
selects which blocks to include. The records could come from your application,
a database or a Genro Bag adapter. Adapt those records at the application boundary
so the presentation components remain independent of the data source.

The same functions work inside a document, a column or another block. Keep local
styles inside the component's container, so a notice's font size does not leak
into the following section. These are the actual reusable body components:

```{literalinclude} ../examples/05_reusable_blocks/company_blocks/sections.py
:language: python
```

## Repeat headers and footers on every page

Page headers and footers are content values passed to Typst's page settings.
The example's `content()` helper captures a Python component as a content value
using a small builder fragment. Only builder-generated source becomes an explicit
Typst expression; customer and company names still pass through literal text
escaping. This helper is part of the example package, not a new core API.

```{literalinclude} ../examples/05_reusable_blocks/company_blocks/chrome.py
:language: python
```

Typst repeats this page furniture as the document grows. The page counter remains
a contextual Typst expression, evaluated on each page, so it shows the current
page and total. Python must not estimate page numbers or copy the footer after
each section. Similarly, `table_header(repeat=True)` lets Typst repeat column
headings when a long table crosses a page boundary.

## Reuse the library in a different document

The service report imports the same functions but chooses a different accent
color and different content. Updating the shared footer changes both documents
on their next build, without editing either recipe.

Theme values passed explicitly by a recipe override the dataclass defaults.
For example, the proposal sets its own `company` and `accent`; edit those
arguments in the main recipe to change them. Its `pale` background and `font`
come from `company_blocks/theme.py` and can be changed there. Playground drafts
are isolated per example; changing a shared file in your local package updates
every recipe that imports it on its next execution.

```{literalinclude} ../examples/05_reusable_blocks/service_report.typ.py
:language: python
```

## Grow an ecosystem of blocks

Start with a package alongside the recipes. When several applications need it,
publish it as a normal Python distribution, for example `acme-document-blocks`,
with an import package such as `acme_documents` and a dependency on `genro-typst`.
That name is illustrative; no such distribution is supplied here. Consumers can
install a version from their package index and write ordinary imports:

```python
from acme_documents.brand import branded_document
from acme_documents.sales import item_table
from acme_documents.quality import measurement_summary
```

Keep the contracts small: parent node, data, explicit options, and a documented
return value. Use domain packages for sales, quality or maintenance, with a
separate brand/theme layer. Pass configuration explicitly instead of relying on
global mutable state. A block should not fetch business data or change the working
directory as a hidden side effect.

Version these packages and test them with representative documents: empty and
long tables, long names, literal markup characters, alternate themes and real
PDF/SVG compilation. Install external dependencies into the same interpreter used
by the CLI or the playground (`GENRO_TYPST_PYTHON`); Python imports are executable
code, so use trusted packages. Font files and images need their own packaging and
Typst resource paths; importing a Python package alone does not make its files
available to the browser compiler.

This complements Typst's own functions and packages: the Python blocks organize
application-side composition and emit ordinary Typst, which can still call Typst
functions or import Typst packages. The current example demonstrates a pattern
for reusable libraries, not a component marketplace or automatic package loader.
