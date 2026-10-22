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

## HTML playground

From this directory, run `npm run demo`, then open
[localhost:8172](http://127.0.0.1:8172/). Edit the JavaScript recipe and click
**Run recipe** to see the generated `.typ` source and SVG side by side.
The collection includes 149 element recipes plus a complete introductory
document. Search by element or category, edit with CodeMirror and use live
preview. Switching examples preserves drafts until the page is reloaded.
The pinned browser compiler renders 149 of the 150 documents; `divider` is
marked as requiring a newer compiler. **Check all examples** verifies the
collection in your browser.
The example imports this builder and compiles through Typst WebAssembly using
`typst.ts`. After the first build downloads the bundled fonts, the supplied
example uses local resources only. The Node process serves static files.

The editable files are in `examples/browser/`; `npm run build:browser` creates
the self-contained static output in `dist/browser/`. See the
[browser guide](https://genro-typst.readthedocs.io/en/latest/browser.html)
for dependencies, limits and upstream credits.

The grammar, native mapping and Python test fixtures are generated. From the
repository root, use `python tools/export_js.py` and
`python tools/export_js_fixtures.py`. Export the browser collection with
`python tools/export_browser_examples.py`. All three support `--check` for CI.

Apache License 2.0. See LICENSE and NOTICE.
