# JavaScript builder

The JavaScript package in `js/` writes **ordinary Typst source** using
`@genrojs/builders` (the `genro-builders-js` project). Its grammar is exported
from the Python `TypstBuilder`; it is not a separately maintained grammar.
The same Python catalog also supplies the mapping from element names to
Typst functions and their argument modes.

**Typst's language, typesetting engine and PDF/SVG output are the work of
Laurenz Mädje, Martin Haug and the Typst team and contributors.** This package
only adds a JavaScript way of authoring that source. See
[acknowledgements](acknowledgements.md).

## Install from the repository

The package is named `@genrojs/typst`. These instructions use the repository
checkout; they do not assume that this package has been published to npm.
Node.js 22 or later is required for development and the examples.

```bash
cd js
npm ci
npm test
node examples/report.typ.mjs
node examples/report.typ.mjs /tmp/report.typ
```

To use the package in another JavaScript project, install the local package:

```bash
npm install /path/to/genro-typst/js
```

## Author a document

For an interactive HTML example with editable JavaScript and Python recipes,
generated Typst source and a shared SVG preview, see the [browser playground](browser.md).
The Python tab also edits imported modules through its **Python file** selector.
JavaScript executes in the browser; Python recipes and modules execute through
the local server using your installed Python interpreter.

```javascript
import { TypstBuilder, length, color } from '@genrojs/typst';

class Report extends TypstBuilder {
    setup(data) {
        data.setItem('title', 'Quarterly report');
    }

    main(root) {
        const doc = root.document({ paper: 'a4', margin: '18mm' });
        doc.set_rule({ target: 'text', size: length('11pt') });
        doc.heading({ content: '^title', level: 1 });
        for (const name of ['Research', 'Development', 'Support']) {
            doc.par(`Department: ${name}`);
        }
        doc.text('Prepared with Typst', { fill: color('#167665') });
    }
}

const report = new Report();
report.create();
const source = report.render();
```

You can also build directly with `new TypstBuilder().root.document()` and
render the resulting builder without a subclass. Use `builder.root` for
fluent authoring; `builder.source` is the underlying Genro SourceBag.

Native calls accept a scalar positional content value followed by an options
object, or a single object containing `content` and other attributes:

```javascript
doc.heading('Title', { level: 1 });
doc.link('https://typst.app').strong('Typst');
doc.metadata({ content: { answer: 42 } });
doc.math_frac({ args: ['1', '2'] });
```

Put arrays and dictionaries inside `content` or `args` to distinguish them
from the attribute object. Initial content is retained when children are
added. Python and JavaScript use the same element and attribute names:

```python
table = doc.native_table(columns=2)
table.table_hline(stroke=expr("2pt + blue"))
table.text("A")
table.text("B")
```

```javascript
const table = doc.native_table({ columns: 2 });
table.table_hline({ stroke: expr('2pt + blue') });
table.text('A');
table.text('B');
```

Only the call syntax changes: Python keyword arguments become a JavaScript
attribute object. Use the same qualified names in both languages when a
name collides with the container API in either runtime:
`doc.typst_columns({ args: [2] })`, `doc.typst_move(...)`,
`doc.typst_label({ name: 'intro' })`. All declared grammar methods are available
through this prefix, but examples prefer the short names everywhere else.
`typst_code` and `typst_markup` are actual grammar names, so they retain
`typst_` in both languages. `native_table` and `native_layout` distinguish
Typst's native elements from the Genro `table` and `layout` elements.

The `expr`, `length`, `color`, `label` and `markup` helpers use the same
JSON-compatible `{"$typst": "..."}` representation as Python. Plain strings
stay literal text; `expr` and `markup` contain trusted Typst code.

## Rendering and data

`render()` returns a UTF-8-compatible JavaScript string. In Node, write it
with `node:fs/promises`; in a browser, pass it to an editor, download it as a
Blob or send it to a compilation service. The library uses ESM and JSON
modules and can be included in a browser application using an ESM-aware
bundler. It does not depend on DOM globals.

```javascript
import { writeFile } from 'node:fs/promises';

await writeFile('report.typ', report.render(), 'utf8');
```

The portable renderer also supports `render({ target: callback })`, writable
objects with `write(text)`, and targets with `full(text)`. Filesystem path
targets belong to the host application. Unlike the Python builder, this
package does not provide `render({ mode: 'pdf' })`: compile the generated
source separately with Typst.

Data binding uses the existing Genro builder and Bag APIs:

```javascript
report.data.setItem('title', 'Revised report');
const updated = report.render();
```

The legacy `table` element requires a Bag of row Bags, just like Python:

```javascript
import { Bag } from '@genrojs/bag';

const rows = new Bag();
const row = new Bag();
row.setItem('description', 'Consulting');
row.setItem('quantity', 2);
rows.setItem('r1', row);
report.data.setItem('lines', rows);

const table = doc.table({ data: '^lines', totalize_footer: 'Total' });
table.column({ field: 'description', name: 'Description' });
table.column({ field: 'quantity', name: 'Quantity', totalize: true });
```

For native Typst tables, use `native_table`, `table_header`, `table_cell`,
etc., as described in the [native reference](native-reference.md).

## Equivalence and limits

The tests compare JavaScript output byte for byte with Python-generated
fixtures for all **129 native elements**, **12 language constructs**, all
**eight legacy elements**, nested content, bound data, escaping and value
serialization. Invalid constructs must fail in both implementations. Repeated
rendering must preserve the output. Separate tests exercise the JavaScript
fluent API, lifecycle, validation and output delivery.

The grammar is shared, but host-language values still have differences:

- JavaScript `Number` does not distinguish `1` from `1.0`. Use `expr('1.0')`
  when the exact Typst numeric type matters. Python float formatting can
  differ from JavaScript for integral values and large exponents.
- JavaScript integers outside the safe integer range cannot preserve arbitrary
  Python integer precision. Use an explicit Typst expression when needed;
  `BigInt` is not implicitly converted.
- JavaScript objects enumerate integer-like keys in numeric order. Output
  dictionary ordering can therefore differ from Python insertion order.
- Use `null` for Python `None`. Undefined values, non-finite numbers, functions
  and arbitrary class instances are not Typst literals.
- Python-specific recipe logic is not translated into JavaScript. The shared
  artifact is the grammar; each language runs its own recipe code.

As with Python, Typst validates native parameter combinations and placement
during compilation. Source equivalence tests do not imply that every possible
combination is valid Typst.

## Regenerate and verify

From the repository root, with the Python `dev` extra installed:

```bash
python tools/export_js.py
python tools/export_js_fixtures.py
npm ci --prefix js
npm test --prefix js
```

`export_js.py` calls `TypstBuilder.to_grammar(...)` and exports renderer
metadata and license notices. `export_js_fixtures.py` runs the existing Python
catalog cases and additional equivalence cases, retaining authored attributes
and Bag data for JavaScript to build independently.

Both scripts accept `--check`. CI checks that committed generated files match
the current Python implementation, runs the Python suite and compares the
JavaScript renderer against those fixtures. A Python change therefore cannot
leave a stale grammar or stale expected output unnoticed.
