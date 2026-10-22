# genro-typst

**Write Typst documents in Python.**

Genro Typst lets you describe Typst documents with Python methods, loops,
functions and application data. It generates ordinary Typst source that you
can inspect, save, edit and compile with Typst.

## Built on Typst

**The language, typesetting engine and PDF/SVG output are provided by
[Typst](https://typst.app/).** We gratefully acknowledge **Laurenz Mädje,
Martin Haug, the Typst team and all Typst contributors** for creating and
maintaining this technology.

Genro Typst adds a Python authoring layer. Typst performs the typography,
page layout and compilation. Learn about the upstream project through its
[documentation](https://typst.app/docs/),
[source code](https://github.com/typst/typst),
[team](https://typst.app/about/) and [official web app](https://typst.app/).
Our [acknowledgements](acknowledgements.md) explain each project's role.

## How it works

```text
Python recipe -> Genro Typst -> Typst source -> Typst compiler -> PDF / SVG
```

A builder turns your Python recipe into a document tree, using `genro-builders`
and `genro-bag`. Genro Typst translates the tree into `.typ` source. The
optional compilation adapter passes that source to Typst through its Python
binding. You can also use the generated source directly in a Typst workflow.

## Start here

Follow the [guide](typst-guide.md) to install the library and write your first
document. It covers literal text, explicit Typst values, styles, tables,
graphics, mathematics, references and data binding.

| Looking for | Read |
|---|---|
| Installation and a first recipe | [Genro Typst guide](typst-guide.md) |
| Builder and compiler entry points | [Python API](api.md) |
| A specific Typst function | [Native call reference](native-reference.md) |
| A recipe beside its Typst equivalent | [Verified catalog examples](catalog-examples.md) |
| A complete invoice or report | [Document examples](examples.md) |
| What is tested and what is not | [Renderer verification](verification.md) |

The catalog targets **Typst 0.15.0** and exposes **129 native calls**, alongside
**12 language constructs** and **eight legacy document elements**. Typst
validates native parameters and their context; see the verification page for
coverage and limits.

## Project scope

This repository contains the Python library, examples, tests and documentation.
The separate Genro PDF Builder application supplies the visual/Python editor
and MCP services. See [repository boundaries](repository-separation.md).

Genro Typst is an independent Softwell project under Apache-2.0. It is not an
official Typst product and is not affiliated with or endorsed by Typst's authors.

```{toctree}
:maxdepth: 1
:caption: Start Here
:hidden:

typst-guide
cli
acknowledgements
```

```{toctree}
:maxdepth: 1
:caption: Reference
:hidden:

api
javascript
grammar-api
native-reference
```

```{toctree}
:maxdepth: 1
:caption: Examples
:hidden:

browser
catalog-examples
examples
```

```{toctree}
:maxdepth: 1
:caption: Development
:hidden:

verification
repository-separation
documentation
```
