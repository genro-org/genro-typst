# Acknowledgements and project scope

## Thank you to Typst's authors

Genro Typst exists because of **[Typst](https://typst.app/)**. We gratefully
acknowledge **Laurenz Mädje and Martin Haug**, the Typst team, and the wider
community of contributors who develop and maintain its language, compiler,
documentation and ecosystem.

The [Typst team's introduction](https://typst.app/about/) describes the people
behind the project. The [compiler repository](https://github.com/typst/typst)
records the work of its contributors. Credit for Typst's typography, page
layout, mathematics and compiled document output belongs to those authors.

## What Genro Typst contributes

**Genro Typst is a way to write Typst documents in Python.** Its contribution
is the authoring interface: methods for document elements, Python composition,
Bag data binding, serialization and conversion of the tree into readable Typst
source. Its compilation adapter sends that source to the existing Typst compiler.

| Project | Responsibility |
|---|---|
| Your Python recipe | Content, application data, loops, conditions and reusable functions |
| Genro Typst | Python document API and translation into Typst source |
| genro-builders and genro-bag | Builder infrastructure, document trees and data binding |
| Typst Python binding | Access to the Typst compiler from Python |
| **Typst** | **Language semantics, typography, layout and PDF/SVG compilation** |

The `.typ` output remains a Typst document. It can be inspected, edited or used
with Typst directly. When a Typst parameter, feature or language rule needs
explanation, the [official Typst documentation](https://typst.app/docs/) is
the authoritative reference; this documentation explains the Python interface.

## Explore and support the upstream project

- [Typst documentation](https://typst.app/docs/) — learn the language and standard library.
- [Typst compiler and contributors](https://github.com/typst/typst) — explore the implementation and contribute upstream.
- [Official Typst web app](https://typst.app/) — use the writing and collaboration environment developed by the Typst team.
- [Typst Universe](https://typst.app/universe/) — discover community packages.
- [Typst team](https://typst.app/about/) — meet the authors and learn about their work.

Bug reports about generated Python-to-Typst source belong in Genro Typst.
For a suspected Typst compiler issue, first reproduce it with a minimal `.typ`
file independently of the builder, then follow the upstream contribution guidance.

## Independent projects and licenses

Genro Typst is developed by Softwell S.r.l. and licensed under
[Apache-2.0](https://github.com/genro-org/genro-typst/blob/main/LICENSE).
Typst is a separate project, distributed under its own
[Apache-2.0 license](https://github.com/typst/typst/blob/main/LICENSE).
Their respective authors retain credit for their work.

Genro Typst is not an official Typst product. It is not affiliated with or
endorsed by Typst's authors. References to Typst identify the language and
compiler used by this Python authoring layer.
