// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { TypstBuilder, color, expr, label, length, markup } from '../../src/index.js';

export const defaultRecipe = `const builder = new TypstBuilder();
const doc = builder.root.document({
  paper: 'a5', margin: '14mm'
});
doc.set_rule({ target: 'text',
  font: 'Libertinus Serif', size: length('10pt')
});
doc.text('GENRO / FIELD NOTES', {
  size: length('8pt'), fill: color('#526b60')
});
doc.heading('Small ideas,\\nbeautiful documents.', { level: 1 });
doc.par('Written in JavaScript. Typeset by Typst.');
doc.v({ content: length('5mm') });

const table = doc.native_table({
  columns: [length('1fr'), length('auto')],
  inset: length('3mm'), stroke: expr('0.4pt + gray')
});
const header = table.table_header();
header.table_cell('Work item').strong('');
header.table_cell('Hours');
for (const [name, hours] of [
  ['Research', 4], ['Design', 6], ['Development', 12]
]) {
  table.table_cell(name);
  table.table_cell(String(hours));
}
doc.v({ content: length('5mm') });
doc.par('Change this recipe and run it again.');`;

export function recipeSource(code) {
    // This local playground deliberately executes the JavaScript the user edits.
    const execute = new Function('TypstBuilder', 'color', 'expr', 'label', 'length', 'markup',
        '"use strict";\n' + code + '\nreturn builder;');
    const builder = execute(TypstBuilder, color, expr, label, length, markup);
    if (!(builder instanceof TypstBuilder)) throw new TypeError('Define a TypstBuilder named builder.');
    return builder.render();
}
