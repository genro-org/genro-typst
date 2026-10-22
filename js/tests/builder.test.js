// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import test from 'node:test';
import { TypstBuilder, color, expr, label, length, markup } from '../src/index.js';
import { valueCode } from '../src/values.js';

test('fluent API preserves positional text, URLs and explicit content when nesting', () => {
    const b = new TypstBuilder(), doc = b.root.document();
    doc.heading('Title', { level: 1 }).emph(' suffix');
    doc.link('https://typst.app').strong('Typst');
    doc.par({ content: 'First' }).text(' second');
    assert.equal(b.render(), '#set page(paper: "a4", flipped: false, margin: 15mm)\n'
        + '#heading(level: 1, [#"Title"#emph([#" suffix"])])\n'
        + '#link("https://typst.app", [#strong([#"Typst"])])\n'
        + '#par([#"First"#text([#" second"])])\n');
    assert.throws(() => doc.text('a', { content: 'b' }), /positional content/);
});

test('subclass lifecycle, data binding, changing data and output delivery use genro-builders-js', () => {
    class Report extends TypstBuilder {
        setup(data) { data.setItem('title', 'First'); }
        main(root) {
            const doc = root.document();
            doc.heading({ content: '^title' });
            for (const department of ['Research', 'Support']) doc.par(department);
        }
    }
    const b = new Report(); b.create();
    assert.match(b.render(), /First/);
    b.data.setItem('title', 'Updated');
    assert.match(b.render(), /Updated/);
    assert.doesNotMatch(b.render(), /First/);
    for (const targetType of ['callable', 'writable', 'full']) {
        let output;
        const capture = value => { output = value; };
        const target = targetType === 'callable' ? capture : { [targetType === 'full' ? 'full' : 'write']: capture };
        b.render({ target });
        assert.equal(output, b.render());
    }
    assert.throws(() => b.render({ mode: 'pdf' }), /renderer_pdf/);
});

test('exported grammar enforces required attributes, allowed children and declared types', () => {
    const b = new TypstBuilder(), doc = b.root.document();
    assert.throws(() => doc.equation(), /formula/);
    assert.throws(() => doc.cell(), /parent|child|allowed/);
    assert.throws(() => doc.layout({ nonexistent: true }), /unknown attribute/);
    assert.throws(() => doc.equation({ formula: 123 }), /formula/);
    assert.throws(() => doc.linebreak().text('invalid'), /child|allowed/);
    assert.throws(() => doc.text({ args: false }), /args/);
    assert.throws(() => doc.text({ options: [] }), /options/);
});

test('collision-safe prefixed methods and helpers generate ordinary Typst', () => {
    const b = new TypstBuilder(), doc = b.root.document();
    doc.typst_columns({ args: [2], gutter: length('5mm') }).text('Columns');
    doc.typst_move('Moved', { dx: length('1mm') });
    doc.typst_label({ name: 'target' });
    doc.ref({ content: label('target') });
    doc.text('Blue', { fill: color('#167665') });
    doc.figure('Figure', { caption: markup('Caption // comment') });
    assert.match(b.render(), /columns\(2, gutter: 5mm/);
    assert.match(b.render(), /move\(dx: 1mm/);
    assert.match(b.render(), /ref\(label\("target"\)\)/);
    assert.match(b.render(), /rgb\("#167665"\)/);
    assert.match(b.render(), /Caption \/\/ comment\n\]/);
    assert.deepEqual(expr('red'), { $typst: 'red' });
});

test('invalid values and helper arguments fail explicitly', () => {
    for (const value of [undefined, NaN, Infinity, -Infinity, () => {}, new Date(), 1n]) {
        assert.throws(() => valueCode(value), TypeError);
    }
    for (const value of ['12', 12, true, '1px']) assert.throws(() => length(value));
    for (const value of ['#ff', 'not-a-color', 123]) assert.throws(() => color(value));
    for (const value of ['', ' ', null, 123]) assert.throws(() => expr(value));
    const b = new TypstBuilder();
    b.root.document().text('Text', { options: { 'font-size': 10 }, font_size: 12 });
    assert.throws(() => b.render(), /Duplicate/);
});

test('native arrays and dictionaries use content attribute, not positional options', () => {
    const b = new TypstBuilder(), doc = b.root.document();
    doc.metadata({ content: { answer: 42 } });
    doc.call({ function: 'example', mode: 'value', content: [1, 2] });
    assert.match(b.render(), /metadata\(\("answer": 42,\)\)/);
    assert.match(b.render(), /example\(\(1, 2,\)\)/);
});

test('no browser globals or compiler are needed for source generation', () => {
    for (const name of ['document', 'window', 'HTMLElement']) assert.equal(globalThis[name], undefined);
    const b = new TypstBuilder();
    b.root.document().par('Independent source generation');
    assert.match(b.render(), /Independent source generation/);
});
