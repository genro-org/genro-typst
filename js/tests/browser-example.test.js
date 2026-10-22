// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import test from 'node:test';
import { defaultRecipe, recipeSource } from '../examples/browser/recipe.js';

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
