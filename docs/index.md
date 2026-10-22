# Genro Typst

Build print documents in Python, generate readable Typst source, and compile
the same source to PDF and SVG previews. Genro Typst is an Apache-2.0 library
built on `genro-builders` and `genro-bag`, targeting **Typst 0.15.0**.

Start with the [guide](typst-guide.md) for installation and your first document.
Use the [native reference](native-reference.md) to find any of the **129 native
calls**, with an executable Python recipe and a handwritten Typst counterpart
for each. The guide also covers **12 language constructs** and **eight legacy
business-document elements**.

The separate Genro PDF Builder application supplies the visual/Python editor,
interactive example gallery and MCP services. It depends on this library;
the library does not require an editor or web server.

```{toctree}
:maxdepth: 1
:caption: Documentation

typst-guide
api
grammar-api
native-reference
catalog-examples
examples
verification
repository-separation
documentation
```

[Source repository](https://github.com/genro-org/genro-typst) ·
[Machine-readable catalog](native-catalog.json) ·
[Apache-2.0 license](https://github.com/genro-org/genro-typst/blob/main/LICENSE)

Genro Typst is an independent Softwell project, not affiliated with or endorsed
by Typst's authors.
