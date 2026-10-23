// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import assert from 'node:assert/strict';
import test from 'node:test';
import { once } from 'node:events';
import { request as httpRequest } from 'node:http';
import { createPlaygroundServer, executePython } from '../../scripts/serve-browser.mjs';

const code = `from genro_typst import TypstBuilder
class Document(TypstBuilder):
    def main(self, root):
        root.document().heading("Café 世界")
`;

test('local Python API renders edits and rejects cross-origin execution', async () => {
    const server = createPlaygroundServer();
    server.listen(0, '127.0.0.1');
    await once(server, 'listening');
    const origin = `http://127.0.0.1:${server.address().port}`;
    try {
        const session = await fetch(`${origin}/api/python/session`).then(r => r.json());
        const request = overrides => fetch(`${origin}/api/python/render`, {
            method: 'POST', headers: { 'Content-Type': 'application/json', Origin: origin,
                'X-Playground-Token': session.token, ...overrides }, body: JSON.stringify({code, assets: {}}),
        });
        assert.equal((await request({Origin:'https://elsewhere.example'})).status, 403);
        assert.equal((await request({'X-Playground-Token':'invalid'})).status, 403);
        const badHost = await new Promise((resolve, reject) => {
            const req = httpRequest(`${origin}/api/python/session`, { headers: {Host:'elsewhere.example'} }, res => {
                res.resume(); resolve(res.statusCode);
            });
            req.on('error', reject); req.end();
        });
        assert.equal(badHost, 403);
        const response = await request({});
        assert.equal(response.status, 200);
        assert.match((await response.json()).source, /Café 世界/);
        const edited = await fetch(`${origin}/api/python/render`, {
            method: 'POST', headers: { 'Content-Type': 'application/json', Origin: origin,
                'X-Playground-Token':session.token }, body: JSON.stringify({code:code.replace('Café 世界','Edited'), assets:{}}),
        });
        assert.match((await edited.json()).source, /Edited/);
    } finally { await new Promise(resolve => server.close(resolve)); }
});

test('Python timeout and syntax errors do not prevent later renders', async () => {
    await assert.rejects(executePython({code:'while True: pass',assets:{}}, {timeoutMs:1000}), /time limit/);
    await assert.rejects(executePython({code:'def broken(',assets:{}}), /SyntaxError/);
    assert.match(await executePython({code,assets:{}}), /Café 世界/);
});

test('Python module state cannot leak between worker requests', async () => {
    const withImport = code.replace('class Document', 'import local_helper\nclass Document');
    await executePython({code:withImport,assets:{'local_helper.py':'value = 1'}});
    await assert.rejects(executePython({code:withImport,assets:{}}), /ModuleNotFoundError/);
});

test('editing imported modules and data changes the main recipe on the next run', async () => {
    const recipe = `from genro_typst import TypstBuilder
from blocks.header import heading
from data import TITLE
class Document(TypstBuilder):
    def main(self, root):
        heading(root.document(), TITLE)
`;
    const assets = {'blocks/__init__.py': '', 'blocks/header.py':
        'def heading(parent, title):\n    parent.heading("First: " + title)\n', 'data.py':'TITLE = "Original"'};
    assert.match(await executePython({code:recipe, assets}), /First: Original/);
    assets['blocks/header.py'] = 'def heading(parent, title):\n    parent.heading("Edited: " + title)\n';
    assets['data.py'] = 'TITLE = "Updated"';
    assert.match(await executePython({code:recipe, assets}), /Edited: Updated/);
    assets['blocks/header.py'] = 'def invalid(';
    await assert.rejects(executePython({code:recipe, assets}), /SyntaxError/);
    assets['blocks/header.py'] = 'def heading(parent, title):\n    parent.heading(title)\n';
    assert.match(await executePython({code:recipe, assets}), /Updated/);
});

test('worker preserves Unicode across output chunks and bounds excessive prints', async () => {
    const text = 'Café 世界'.repeat(12000);
    assert.ok((await executePython({code:code.replace('Café 世界',text),assets:{}})).includes(text));
    await assert.rejects(executePython({code:'print("x" * 2000000)\n' + code,assets:{}}), /too much output/);
});
