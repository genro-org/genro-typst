# Documentation development

Documentation is written in English and built with
[Sphinx](https://www.sphinx-doc.org/) and [MyST](https://myst-parser.readthedocs.io/).
Markdown pages remain readable on GitHub; Sphinx adds navigation, search,
API documentation extracted from Python, and checked internal references.
The site uses `sphinx_rtd_theme`, matching the documentation of `genro-bag`
and `genro-builders`, with grouped sidebar navigation and GitHub source links.

## Build locally

From the repository root:

```bash
python -m pip install -e ".[docs]"
npm ci --prefix js --ignore-scripts
npm run build:playground --prefix js
python -m sphinx -n -W --keep-going -b html docs docs/_build/html
```

Node.js 22 builds the static playground, which Sphinx copies from
`js/dist/docs/` into the HTML output. For a prose-only build, the npm steps can
be omitted; the playground is included only when that directory exists.

Open `docs/_build/html/index.html` in a browser. Build output is ignored by Git.
The `-n -W --keep-going` flags check references and treat warnings as failures,
while collecting all diagnostics. No Typst compiler is required to build the
site; install the `pdf` or `dev` extra to regenerate PDFs or run compiler tests.

The GitHub Actions documentation job runs the same strict build and uploads
its HTML artifact. Hosting/deployment is separate from that build.

## Publish on Read the Docs

The repository includes `.readthedocs.yaml`, configured for Python 3.12 and
Node.js 22 on Ubuntu 24.04. It installs the package with its `docs` extra, checks
generated references, builds the static playground with npm, and builds HTML
using `docs/conf.py`. Warnings fail the build,
including unresolved references.

The connected project publishes `main` as
[latest](https://genro-typst.readthedocs.io/en/latest/). Keep the configuration
file path at `.readthedocs.yaml`. Pushes to `main` trigger documentation builds
through the GitHub integration. After pushing, check the
[build dashboard](https://app.readthedocs.org/projects/genro-typst/builds/): the
successful build must reference the commit you just pushed. A successful local
or GitHub Actions Sphinx build alone does not confirm publication on Read the Docs.

To configure another deployment, connect the GitHub repository, select `main`
as the default branch and use the same configuration file. Read the Docs serves
the Sphinx documentation and the static JavaScript playground. It does not host the
Python execution server: readers start that server locally using the
[playground setup instructions](browser.md#start-the-example).

See the [Read the Docs configuration reference](https://docs.readthedocs.com/platform/stable/config-file/v2.html).

## Update generated references

Edit `src/genro_typst/native_catalog.py` and `tests/native_cases.py`, then run:

```bash
python tools/generate_reference.py
python tools/generate_reference.py --check
```

This generates `native-reference.md`, `catalog-examples.md` and
`native-catalog.json`, plus `grammar-api.rst` from the grammar declarations. Change prose in the generator rather than editing its
output. The tests execute the documented recipes; see [verification](verification.md).

## Maintain the browser examples and module guide

The browser collection is separate from the application gallery below. Its
152 entries include the two recipes and shared modules in
`examples/05_reusable_blocks/`. After editing those files, regenerate their
bundled recipes and assets, and verify the result:

```bash
python tools/export_browser_examples.py
python tools/export_browser_examples.py --check
pytest -q tests/test_reusable_blocks.py tests/test_example_naming.py
npm test --prefix js
npm run test:browser-server --prefix js
```

These checks require the Python development dependencies and the JavaScript
dependencies installed with `npm ci --prefix js`. The Sphinx
[reusable blocks guide](reusable-blocks.md) includes the example source directly
with `literalinclude`. Keep the [module editor walkthrough](browser.md#edit-imported-python-modules)
in sync with file selectors, reset/download controls and draft lifetime.

## Export the application gallery

The separate application packages its own snapshot of all 149 examples,
including language and legacy cases, descriptions, editable recipes and assets.
Update the English text in `tools/export_app_examples.py`, then export:

```bash
python tools/export_app_examples.py --output ../genro-pdf-builder/src/genro_pdf_builder/studio/typst_examples.json
python tools/export_app_examples.py --output ../genro-pdf-builder/src/genro_pdf_builder/studio/typst_examples.json --check
```

Run the application tests after exporting. Saved user documents are independent
of this catalog and are not rewritten when examples change.
