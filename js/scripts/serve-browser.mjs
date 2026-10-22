// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { context } from 'esbuild';
import { fileURLToPath } from 'node:url';

const ctx = await context({});
const server = await ctx.serve({
    servedir: fileURLToPath(new URL('../dist/browser', import.meta.url)),
    host: '127.0.0.1', port: Number(process.env.PORT || 8172),
});
console.log(`Genro Typst playground: http://127.0.0.1:${server.port}/`);
