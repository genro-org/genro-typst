# @genrojs/typst

Write ordinary **Typst source in JavaScript**, using `@genrojs/builders` and
the grammar exported from the Python `genro-typst` builder.

**Typst's language, typesetting and rendering are the work of Laurenz Mädje,
Martin Haug and the Typst team and contributors.** This independent Softwell
package is an authoring layer, not a Typst compiler or an official Typst
product. Visit [Typst](https://typst.app/), its
[documentation](https://typst.app/docs/) and
[source](https://github.com/typst/typst).

## Use from a checkout

Requires Node.js 22 or later. From this directory:

```bash
npm ci
npm test
node examples/report.typ.mjs /tmp/report.typ
```

To install in another project, run `npm install /path/to/genro-typst/js`.
These instructions do not assume an npm release.

```javascript
import { TypstBuilder, length } from '@genrojs/typst';

const builder = new TypstBuilder();
const doc = builder.root.document({ paper: 'a4' });
doc.set_rule({ target: 'text', size: length('11pt') });
doc.heading('Report', { level: 1 });
for (const name of ['Research', 'Support']) doc.par(name);
const source = builder.render();
```

The renderer generates `.typ` source; PDF/SVG compilation remains a separate
Typst operation. It is portable ESM with JSON imports, usable in Node and
browser applications with an ESM-aware bundler. Use host APIs for file output.

Read the [JavaScript guide](https://genro-typst.readthedocs.io/en/latest/javascript.html)
for data binding, custom recipes, output delivery, Python equivalence and
numeric representation limits.

The grammar, native mapping and Python test fixtures are generated. From the
repository root, use `python tools/export_js.py` and
`python tools/export_js_fixtures.py`; both support `--check` for CI.

Apache License 2.0. See LICENSE and NOTICE.
