// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { createServer } from 'node:http';
import { spawn } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { existsSync } from 'node:fs';
import { readFile, realpath } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, extname, sep } from 'node:path';

const root = fileURLToPath(new URL('../../', import.meta.url));
const staticRoot = resolve(root, 'js/dist/browser');
const defaultPython = process.env.GENRO_TYPST_PYTHON
    || (existsSync(resolve(root, 'venv/bin/python')) ? resolve(root, 'venv/bin/python') : 'python3');
const limit = 1024 * 1024;

export function executePython(payload, { python = defaultPython, timeoutMs = 15000 } = {}) {
    return new Promise((resolveResult, reject) => {
        const child = spawn(python, ['-m', 'genro_typst.playground_worker'], { cwd: root, stdio: ['pipe', 'pipe', 'pipe'] });
        let output = '', diagnostics = '', size = 0, failure;
        const stop = message => { failure = new Error(message); child.kill('SIGKILL'); };
        const timer = setTimeout(() => stop('Python recipe exceeded the execution time limit.'), timeoutMs);
        for (const [stream, append] of [[child.stdout, text => { output += text; }], [child.stderr, text => { diagnostics += text; }]]) {
            stream.setEncoding('utf8');
            stream.on('data', chunk => {
                size += Buffer.byteLength(chunk);
                if (size > limit) stop('Python recipe produced too much output.');
                else append(chunk.toString());
            });
        }
        child.stdin.on('error', () => {}); // Early process exit is handled below.
        child.on('error', error => { clearTimeout(timer); reject(new Error(`Cannot start Python: ${error.message}`)); });
        child.on('close', code => {
            clearTimeout(timer);
            if (failure) return reject(failure);
            if (code !== 0) return reject(new Error(diagnostics || `Python exited with status ${code}.`));
            try {
                const result = JSON.parse(output);
                if (result.error) throw new Error(result.error);
                if (typeof result.source !== 'string') throw new Error('Python returned no Typst source.');
                resolveResult(result.source);
            } catch (error) { reject(error); }
        });
        child.stdin.end(JSON.stringify(payload));
    });
}

export function createPlaygroundServer(options = {}) {
    const token = randomBytes(32).toString('hex');
    let running = false;
    const server = createServer(async (req, res) => {
        const json = (status, data) => {
            res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
            res.end(JSON.stringify(data));
        };
        // Same-origin requests only, including protection against DNS rebinding.
        const host = `127.0.0.1:${server.address().port}`;
        if (req.headers.host !== host) return json(403, { error: 'Unexpected Host header.' });
        const path = new URL(req.url, `http://${host}`).pathname;
        if (path === '/api/python/session' && req.method === 'GET') return json(200, { token });
        if (path === '/api/python/render') {
            if (req.method !== 'POST') return json(405, { error: 'Use POST.' });
            if (req.headers.origin !== `http://${host}` || req.headers['x-playground-token'] !== token
                || req.headers['content-type']?.split(';')[0] !== 'application/json') {
                return json(403, { error: 'Python execution requires the local playground session.' });
            }
            if (running) return json(409, { error: 'A Python recipe is already running. Try again shortly.' });
            running = true;
            try {
                let body = '', size = 0;
                req.setEncoding('utf8');
                for await (const chunk of req) {
                    size += Buffer.byteLength(chunk);
                    if (size > limit) { json(413, { error: 'Recipe request is too large.' }); return; }
                    body += chunk.toString();
                }
                const payload = JSON.parse(body);
                if (!payload || typeof payload.code !== 'string' || payload.code.length > 256 * 1024
                    || !payload.assets || typeof payload.assets !== 'object' || Array.isArray(payload.assets)
                    || Object.values(payload.assets).some(value => typeof value !== 'string')) {
                    return json(400, { error: 'Expected a Python recipe and a dictionary of text assets.' });
                }
                const source = await executePython(payload, options);
                json(200, { source });
            } catch (error) { json(422, { error: error.message }); }
            finally { running = false; }
            return;
        }
        if (!['GET', 'HEAD'].includes(req.method)) return json(405, { error: 'Use GET.' });
        try {
            const file = await realpath(resolve(staticRoot, '.' + decodeURIComponent(path === '/' ? '/index.html' : path)));
            if (!file.startsWith(staticRoot + sep)) return json(403, { error: 'Invalid path.' });
            const content = await readFile(file);
            const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.otf': 'font/otf', '.txt': 'text/plain', '.json': 'application/json', '.wasm': 'application/wasm' };
            res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
            res.end(req.method === 'HEAD' ? undefined : content);
        } catch { json(404, { error: 'Not found. Run npm run build:browser first.' }); }
    });
    server.requestTimeout = 20000;
    return server;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
    const server = createPlaygroundServer();
    server.listen(Number(process.env.PORT || 8172), '127.0.0.1', () => {
        console.log(`Genro Typst playground: http://127.0.0.1:${server.address().port}/`);
        console.log(`Local trusted Python recipes execute with: ${defaultPython}`);
    });
}
