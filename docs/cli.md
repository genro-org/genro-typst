# Command-line interface

`genro-typst` runs a Python builder recipe and generates ordinary Typst source,
a PDF or SVG pages. Typst compilation uses the optional Python `typst` binding;
the separate official Typst CLI is not required. The language, typesetting and
PDF/SVG output are provided by [Typst and its authors](acknowledgements.md).

## Install and run

From a repository checkout, install the package to register the command:

```bash
python -m pip install -e ".[pdf]"
genro-typst --help
```

For source generation only, `python -m pip install -e .` is enough. If you
already installed an earlier checkout, repeat the installation to register
the new console entry point. `python -m genro_typst` accepts the same arguments
as `genro-typst`.

```bash
genro-typst mydoc.typ.py
genro-typst mydoc.typ.py --typ -o output/document.typ
genro-typst mydoc.typ.py --pdf
genro-typst mydoc.typ.py --pdf -o output/document.pdf
genro-typst mydoc.typ.py --svg -o output/page.svg
```

Choose one format per invocation: `--typ` (the default), `--pdf` or `--svg`.
The format comes from the flag, not from the output filename extension.
PDF/SVG generation does not also save a `.typ` file.

## Recipe convention

The CLI loads a normal Python file, finds a builder class, instantiates it
without arguments, calls `create()` and renders the document. A recipe with a
single locally defined `TypstBuilder` subclass works without extra declarations:

```python
from genro_typst import TypstBuilder


class MyDocument(TypstBuilder):
    def main(self, root):
        doc = root.document()
        doc.heading("A document written in Python", level=1)
        for name in ("Research", "Development", "Support"):
            doc.par(f"Department: {name}")


if __name__ == "__main__":
    MyDocument.run()
```

Save this as `mydoc.typ.py`. Both entry points remain available:

```bash
genro-typst mydoc.typ.py --pdf
python mydoc.typ.py
python mydoc.typ.py output/document.typ
```

Direct execution through `MyDocument.run()` keeps its original behavior:
source generation only, with an optional positional destination. The new
console command adds PDF/SVG compilation and uses `-o` for the destination.

The CLI does **not** execute the `if __name__ == "__main__":` block, so the
direct entry point does not run a second time. Other top-level Python
statements execute normally during loading. Put the actual document creation
in the builder and guard any standalone script actions as shown above.

### Multiple or imported builders

Selection follows this order:

1. `--builder ClassName` selects that recipe namespace entry.
2. A module-level `BUILDER = MyDocument` selects that class.
3. Otherwise, exactly one locally defined `TypstBuilder` subclass is required.

```python
BUILDER = MyDocument
```

```bash
genro-typst reports.typ.py --builder Invoice --pdf
```

Imported subclasses are not chosen automatically, but can be selected with
`BUILDER` or `--builder`. The selected value must be a subclass, not an instance
or factory. Classes requiring constructor arguments need a no-argument recipe
subclass that prepares the necessary data in `setup()`.

## Output paths and SVG pages

Without `-o`, output is placed beside the recipe:

| Input | Default source | Default PDF | Default single-page SVG |
|---|---|---|---|
| `mydoc.typ.py` | `mydoc.typ` | `mydoc.pdf` | `mydoc.svg` |
| `mydoc.py` | `mydoc.typ` | `mydoc.pdf` | `mydoc.svg` |

Relative paths supplied with `-o` are resolved from the current working
directory. Missing parent directories are created. Existing destination files
are replaced; the recipe itself cannot be used as an output, including through
symlinks or hard links.

For SVG, a one-page document uses the exact destination path. A multipage
document adds a one-based suffix to every page:

```text
genro-typst mydoc.typ.py --svg -o output/page.svg

output/page-1.svg
output/page-2.svg
...
```

Existing files from earlier runs with a different page count are not removed
automatically. Use a dedicated output directory when collecting page previews.
Rendering and compilation complete before any output is written, so a compiler
error leaves existing outputs untouched. A filesystem error during delivery
can still leave partial output, especially for multipage SVG.

## Images, imports and working directory

For PDF/SVG, the Typst compilation root defaults to the recipe's directory.
Keep relative Typst images and imported `.typ` files there, or choose another
root explicitly:

```bash
genro-typst mydoc.typ.py --pdf --root /path/to/assets
```

The CLI does not change the working directory. Relative paths in your own
Python file operations keep ordinary Python semantics; use
`Path(__file__).parent` for recipe-relative data. The recipe directory is
available for sibling Python imports while loading and building.

The command prints generated paths to standard output. Diagnostics go to
standard error: exit status `0` means success, `1` means a recipe, rendering
or output error, and `2` means invalid command-line arguments.

## Try the included recipe

From the repository root:

```bash
genro-typst examples/04_python_recipe/mydoc.typ.py -o output/mydoc.typ
genro-typst examples/04_python_recipe/mydoc.typ.py --pdf -o output/mydoc.pdf
genro-typst examples/04_python_recipe/mydoc.typ.py --svg -o output/mydoc.svg
```
