# Renderer verification

Verification targets **Typst 0.15.0**, pinned in the `pdf` extra. It covers all
**129 registered native calls**, **12 language constructs** and **eight legacy
builder elements**. This does not mean that every parameter combination or the
entire Typst standard library has been tested.

## Verification contract

For every native call, `tests/native_cases.py` defines an explicit case with
valid parameters, the required context and Typst reference source written
independently of the renderer. `tests/test_catalog_compilation.py`:

1. Checks exact agreement between cases and catalog: adding an element without
   an example fails the suite.
2. Builds the tree and validates its grammar.
3. Executes the Python recipe published in the documentation and checks that
   it produces the same source.
4. Saves and reloads the TYTX tree, preserving structure and source.
5. Compiles the source to PDF and SVG through `TypstEngine`.
6. Checks the expected page count, SVG XML and dimensions.
7. Compares **every SVG page byte for byte** against the handwritten reference
   compiled in the same environment.
8. Supplies an unknown parameter and checks the compiler error.

Test Typst files remain in pytest's temporary directory. Failed comparisons
also save actual and expected SVGs. Comparisons use the same compiler version
and fonts; they do not impose binary snapshots tied to a machine or future
Typst version. PDF output is compiled, but is not compared byte for byte with
SVG, and not every PDF property is automatically checked (tagging,
accessibility, links and metadata).

The [catalog examples](catalog-examples.md) include Python recipes and complete
Typst references with the required containers.

## Required contexts and behavior

- `table_footer` and `grid_footer` must end at the final row. Add body cells
  **before** the footer. The suite also exercises invalid ordering.
- Table/grid cells, headers and lines belong in their corresponding container;
  `curve_*` elements belong in `curve`.
- Math elements are tested inside `math_equation`. In code mode, arguments to
  functions such as `math_vec` and `math_mat` are content/strings, not Python
  numbers implicitly converted to displayed text.
- `measure` requires Typst context and returns a dictionary. Its example uses
  `context` and `call(function="repr", mode="args")` to display the result.
- `native_layout` receives an explicit callback; `metadata` inserts invisible
  data. `hide` and structural elements need not produce visible content themselves.
- `columns`, `move` and `label` collide with SourceBag names: use
  `typst_columns`, `typst_move` and `typst_label` in both Python and JavaScript.
  Examples use short names for other elements. Qualified aliases remain valid
  for compatibility; `typst_code` and `typst_markup` are actual grammar names.

## Language, data and regressions

`tests/test_language_compilation.py` exercises every language construct with
PDF/SVG compilation and round trips, all five `call` modes, local imports by
name, wildcard and alias, literal values compared with Typst's JSON parser,
expected errors, and a document combining every legacy element with Bag data
and native elements. Existing tests also cover multipage tables, totals,
style inheritance, references, local rules and dynamic binding.

Regressions covered during verification:

- `markup("... // comment")` preserves the closing delimiter by adding a final
  newline, matching `typst_markup`.
- `options` and `args` distinguish `None` from empty values of the wrong type.
  Lists supplied as `options`, dictionaries supplied as `args`, booleans and
  strings raise `TypeError` instead of being silently ignored.
- Imported names and aliases must be simple identifiers. Dotted names raise
  `ValueError`; dotted paths remain valid for function calls such as
  `call(function="helper.greeting", ...)`.

The three elements `dataSetter`, `dataFormula` and `dataController` inherited
from `genro-builders` belong to the data runtime. They are not Typst calls and
are excluded from the 149 document elements above.

## Reproducing the checks

From the repository root, with the development environment installed:

```bash
venv/bin/pytest -q
venv/bin/ruff check src tests tools
venv/bin/mypy
venv/bin/python tools/generate_reference.py --check
```

To check a single call:

```bash
venv/bin/pytest -q tests/test_catalog_compilation.py -k table_footer
```

To regenerate the reference and examples:

```bash
venv/bin/python tools/generate_reference.py
```

See [documentation development](documentation.md) for the Sphinx build and
packaged application catalog checks.

Outside this catalog-wide verification: every possible parameter combination,
remote packages, unavailable external fonts, other operating systems/compiler
versions, and targets other than PDF/SVG. The Python validator does not
replicate the compiler's type system; Typst intentionally diagnoses many
native parameter errors.
