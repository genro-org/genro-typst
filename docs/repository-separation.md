# Library and application repositories

`genro-typst` is the Apache-2.0 Python library. Its public entry point remains
`from genro_typst import TypstBuilder`. The grammar, source renderer, PDF
renderer, compiler and value conversion live here, together with their tests,
examples and design documentation.

`genro-pdf-builder` is the separate application repository. It depends on
`genro-typst[pdf]>=0.0.1` and contains the HTML/SVG builder with WeasyPrint,
legacy PdfBuilder compatibility, visual edits, Kajenn/Gramlot UI, CodeMirror,
PDF.js assets, CLI and MCP/REST services. Its wheel owns only the
`genro_pdf_builder` package. The dependency direction is always application to
library; the library never imports the application.

For local development with sibling checkouts, install both editable packages
in the application's environment:

```bash
cd ../genro-pdf-builder
uv venv venv --python 3.12
uv pip install --python venv/bin/python -e "../genro-typst[pdf]" -e ".[studio,weasyprint,dev]"
venv/bin/genro-pdf-builder serve --workspace ./.typst-studio --port 8170
```

During the split, the existing `.typst-studio` workspace is moved intact to
the application repository, including project IDs, Python recipes and artifact
IDs. No document is converted or regenerated. Backups are kept outside Git.
The local MCP address stays `http://127.0.0.1:8170/api/mcp`.

New Typst recipes import the library directly. Application exports may also
import `genro_pdf_builder.visual_edits` when they contain visual adjustments.
The application worker accepts the previous generated import
`genro_typst.studio.visual_edits` without rewriting saved recipes. To run such
an old script independently, change that import to
`genro_pdf_builder.visual_edits`. This compatibility code belongs to the app.

The old `genro-typst serve` command is retained only as an application CLI
alias. Installing the library alone does not install a web server or CLI.
Neither repository is automatically published or pushed by this separation.
