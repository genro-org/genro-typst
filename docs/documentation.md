# Documentation development

Documentation is written in English and built with
[Sphinx](https://www.sphinx-doc.org/) and [MyST](https://myst-parser.readthedocs.io/).
Markdown pages remain readable on GitHub; Sphinx adds navigation, search,
API documentation extracted from Python, and checked internal references.

## Build locally

From the repository root:

```bash
python -m pip install -e ".[docs]"
python -m sphinx -n -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser. Build output is ignored by Git.
The `-n -W --keep-going` flags check references and treat warnings as failures,
while collecting all diagnostics. No Typst compiler is required to build the
site; install the `pdf` or `dev` extra to regenerate PDFs or run compiler tests.

The GitHub Actions documentation job runs the same strict build and uploads
its HTML artifact. Hosting/deployment is separate from that build.

## Publish on Read the Docs

The repository includes `.readthedocs.yaml`, configured for Python 3.12 on
Ubuntu 24.04. It installs the package with its `docs` extra, checks generated
references, and builds HTML using `docs/conf.py`. Warnings fail the build,
including unresolved references.

Connect your GitHub account to Read the Docs, import `genro-org/genro-typst`,
and select `main` as the default branch. Keep the configuration file path at
`.readthedocs.yaml`. Once the integration is connected, pushes can trigger
documentation builds automatically. Check the initial build in the Read the
Docs dashboard before sharing the published URL.

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
