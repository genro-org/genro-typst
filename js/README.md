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
[localhost:8172](http://127.0.0.1:8172/). Edit either recipe and click
**Run Python** or **Run JavaScript** to see the generated `.typ` source and SVG side by side.
The collection includes 149 element recipes plus a complete introductory
document, plus a technical proposal and a service report built from shared Python
modules. Search by element or category, edit with CodeMirror and use live
preview. Each example has Python and JavaScript tabs sharing one preview;
both recipes are editable and the active tab drives live rendering.
Switching tabs or examples preserves separate drafts until the page is reloaded.
Edits in one language do not rewrite the other.
The pinned browser compiler renders 151 of the 152 documents; `divider` is
marked as requiring a newer compiler. The active language's **Check all** button verifies the collection in your browser.
The example imports this builder and compiles through Typst WebAssembly using
`typst.ts`. After the first build downloads the bundled fonts, the supplied
example uses local resources only. The Node process serves the page and executes trusted Python recipes locally.
Install Genro Typst into the repository's `venv` first, or set
`GENRO_TYPST_PYTHON` to an interpreter with the package installed.
Python runs with your user permissions; this server is for local use only.

The editable files are in `examples/browser/`; `npm run build:browser` creates
the browser output in `dist/browser/`. Static hosting supports JavaScript;
Python previews require the local server. See the
[browser guide](https://genro-typst.readthedocs.io/en/latest/browser.html)
for dependencies, limits and upstream credits.

The grammar, native mapping and Python test fixtures are generated. From the
repository root, use `python tools/export_js.py` and
`python tools/export_js_fixtures.py`. Export the browser collection with
`python tools/export_browser_examples.py`. All three support `--check` for CI.

Apache License 2.0. See LICENSE and NOTICE.
