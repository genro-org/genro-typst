// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import test from 'node:test';
import { defaultRecipe, recipeSource } from '../examples/browser/recipe.js';
import catalog from '../examples/browser/catalog.json' with { type: 'json' };
import grammar from '../src/catalog.json' with { type: 'json' };
import { examples, filterExamples, RecipeDrafts } from '../examples/browser/collection.js';

test('browser collection covers every native and language element plus Genro document elements', () => {
    assert.deepEqual(catalog.examples.filter(e => e.section !== 'language' && e.section !== 'legacy').map(e => e.id).sort(), Object.keys(grammar.native).sort());
    assert.deepEqual(catalog.examples.filter(e => e.section === 'language').map(e => e.id).sort(),
        ['call', 'set_rule', 'show_rule', 'scope', 'context', 'equation', 'label', 'let', 'import_module', 'include', 'typst_code', 'typst_markup'].sort());
    assert.deepEqual(catalog.examples.filter(e => e.section === 'legacy').map(e => e.id).sort(),
        ['document', 'layout', 'row', 'cell', 'paragraph', 'pageNumber', 'table', 'column'].sort());
    assert.equal(new Set(examples.map(e => e.id)).size, examples.length);
});

for (const example of catalog.examples) {
    test(`editable browser recipe matches Python: ${example.id}`, () => {
        assert.equal(recipeSource(example.code), example.source);
    });
}

test('search combines words with categories and handles no matches', () => {
    assert.ok(filterExamples('MATH frac', 'math').some(e => e.id === 'math_frac'));
    assert.equal(filterExamples('MATH frac', 'text').length, 0);
    assert.equal(filterExamples('no-such-example').length, 0);
    assert.equal(filterExamples('').length, examples.length);
});

test('example drafts survive switching and reset affects only the selected recipe', () => {
    const drafts = new RecipeDrafts();
    const [a, b] = examples;
    drafts.save(a, a.code + '\n// draft A');
    drafts.save(b, b.code + '\n// draft B');
    assert.match(drafts.read(a), /draft A/);
    assert.equal(drafts.reset(a), a.code);
    assert.equal(drafts.read(a), a.code);
    assert.match(drafts.read(b), /draft B/);
});

test('asset examples contain the exact files needed by their recipes', () => {
    for (const [id, path] of [['image', 'logo.svg'], ['cite', 'refs.yml'], ['bibliography', 'refs.yml'],
        ['import_module', 'helper.typ'], ['include', 'extra.typ']]) {
        const example = examples.find(e => e.id === id);
        assert.ok(example.assets[path]);
        assert.ok(example.source.includes(path));
    }
});

test('the browser default recipe creates real Typst with its table and explicit lengths', () => {
    const source = recipeSource(defaultRecipe);
    assert.match(source, /^#set page\(paper: "a5"/);
    assert.match(source, /#v\(5mm\)/);
    assert.match(source, /table\.cell\(\[#"Development"\]\)/);
    assert.equal(recipeSource(defaultRecipe), source);
});

test('editing a recipe changes the generated document, retaining escaping', () => {
    const code = "const builder = new TypstBuilder(); builder.root.document().text('A \\\"quote\\\" #literal');";
    const result = recipeSource(code);
    assert.match(result, /A \\"quote\\" #literal/);
    assert.doesNotMatch(result, /Development/);
});

test('bad JavaScript or a missing builder is reported instead of an empty document', () => {
    assert.throws(() => recipeSource('const builder = ;'), SyntaxError);
    assert.throws(() => recipeSource('const builder = {};'), /TypstBuilder named builder/);
    assert.throws(() => recipeSource('throw new Error("Recipe failed");'), /Recipe failed/);
});
