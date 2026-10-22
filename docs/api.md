# Python API

## Builder lifecycle

Import `TypstBuilder` from `genro_typst`, subclass it, and implement
`main(self, root)`. An optional `setup(self, data)` fills the data Bag.
Call `create()` before rendering. `render()` returns Typst source;
`render(mode="pdf")` returns PDF bytes. Supplying `target` writes to a file
or compatible stream instead. PDF compilation requires the `pdf` extra.

Grammar methods are called on source nodes such as `root.document()` and
`doc.heading(...)`. See the [native reference](native-reference.md) for their
shared calling convention and the [guide](typst-guide.md) for data binding,
serialization and scoped styles.

```{eval-rst}
.. autoclass:: genro_typst.TypstBuilder
```

## Explicit Typst values

These helpers are exported from `genro_typst`. Each returns a serializable
`{"$typst": "..."}` marker. Ordinary Python strings remain literal text.

```{eval-rst}
.. autofunction:: genro_typst.expr
```

```{eval-rst}
.. autofunction:: genro_typst.length
```

```{eval-rst}
.. autofunction:: genro_typst.color
```

```{eval-rst}
.. autofunction:: genro_typst.label
```

```{eval-rst}
.. autofunction:: genro_typst.markup
```

## Compilation and previews

`TypstEngine` is an adapter to the Typst Python binding. Typst's compiler
performs the typesetting and generates the PDF/SVG output; Genro Typst passes
the source and compilation options to it.

```{eval-rst}
.. autoclass:: genro_typst.compiler.TypstEngine
   :members: compile
   :undoc-members:
```

`compile(source, root=None, preview=False)` compiles UTF-8 Typst source to PDF.
`root` sets the compiler's filesystem root for images, imports and other files.
With `preview=True`, it also generates SVG pages using the same source and
timestamp. Without previews, `pages` is `None` and `svg_pages` is empty.
Compiler errors propagate to the caller. Missing optional compiler dependencies
raise `RuntimeError` with installation instructions.

```{eval-rst}
.. autoclass:: genro_typst.compiler.CompiledDocument
   :members:
   :undoc-members:
```

| Field | Value |
|---|---|
| `pdf` | Compiled PDF bytes |
| `pages` | Page count when previews are requested, otherwise `None` |
| `svg_pages` | Tuple of SVG page bytes, in document order |

## Grammar methods

The [declared grammar signatures](grammar-api.rst) document the eight legacy
and 12 language elements. These declarations are extracted from source because
the builder registers them dynamically. Call them on source nodes such as
`doc.document(...)`; they are not standalone module functions.

See the [native reference](native-reference.md) for all 129 native calls.
