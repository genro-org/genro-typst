// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import test from 'node:test';
import { Bag } from '@genrojs/bag';
import { TypstBuilder } from '../src/index.js';
import { valueCode } from '../src/values.js';
import fixtures from './python-fixtures.json' with { type: 'json' };
import catalog from '../src/catalog.json' with { type: 'json' };

function decode(value) {
    if (value && typeof value === 'object' && Object.hasOwn(value, '$bag')) {
        const bag = new Bag();
        for (const [name, child] of value.$bag) bag.setItem(name, decode(child));
        return bag;
    }
    if (Array.isArray(value)) return value.map(decode);
    if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, decode(v)]));
    return value;
}
function build(fixture, qualified = false) {
    const builder = new TypstBuilder();
    for (const [key, value] of fixture.data.$bag) builder.data.setItem(key, decode(value));
    function walk(parent, nodes) {
        for (const node of nodes) {
            const method = qualified ? `typst_${node.tag}` : (catalog.authoringAliases[node.tag] ?? node.tag);
            const child = parent[method](decode(node.value), decode(node.attrs));
            walk(child, node.children);
        }
    }
    walk(builder.root, fixture.tree);
    return builder;
}

test('Python fixtures cover the complete native catalog', () => {
    assert.deepEqual(fixtures.cases.filter(c => c.name.startsWith('native/')).map(c => c.name.slice(7)).sort(), Object.keys(catalog.native).sort());
});
for (const fixture of fixtures.cases) {
    test(`Python equivalence: ${fixture.name}`, () => {
        if (fixture.error) assert.throws(() => build(fixture).render());
        else {
            const builder = build(fixture);
            assert.equal(builder.render(), fixture.source);
            assert.equal(builder.render(), fixture.source, 'repeat rendering must not change the source');
            assert.equal(build(fixture, true).render(), fixture.source, 'qualified aliases remain compatible');
        }
    });
}
for (const [index, fixture] of fixtures.values.entries()) {
    test(`Python value encoding: ${index}`, () => assert.equal(valueCode(fixture.value), fixture.source));
}
