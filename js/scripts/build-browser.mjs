// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { build } from 'esbuild';
import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const output = resolve(root, 'dist/browser');
await mkdir(resolve(output, 'vendor'), { recursive: true });
await mkdir(resolve(output, 'fonts'), { recursive: true });
await build({
    entryPoints: [resolve(root, 'examples/browser/main.js')],
    outfile: resolve(output, 'main.js'), bundle: true, format: 'esm', platform: 'browser',
    target: ['es2022'], external: ['./vendor/typst.js'], legalComments: 'linked',
});
for (const name of ['index.html', 'style.css']) {
    await copyFile(resolve(root, 'examples/browser', name), resolve(output, name));
}
await copyFile(resolve(root, 'node_modules/@myriaddreamin/typst-all-in-one.ts/dist/esm/index.js'),
    resolve(output, 'vendor/typst.js'));
const origin = 'https://raw.githubusercontent.com/typst/typst-assets/v0.13.1/';
async function asset(relative, target) {
    try { return await readFile(target); } catch (error) { if (error.code !== 'ENOENT') throw error; }
    const response = await fetch(origin + relative);
    if (!response.ok) throw new Error(`Cannot download ${relative}: HTTP ${response.status}`);
    const bytes = new Uint8Array(await response.arrayBuffer());
    await writeFile(target, bytes);
    return bytes;
}
await Promise.all(['Regular', 'Bold', 'Italic', 'BoldItalic'].map(weight => {
    const name = `LibertinusSerif-${weight}.otf`;
    return asset(`files/fonts/${name}`, resolve(output, 'fonts', name));
}));
await asset('files/fonts/NewCMMath-Regular.otf', resolve(output, 'fonts/NewCMMath-Regular.otf'));
const notices = await asset('NOTICE', resolve(output, 'fonts/NOTICE'));
const license = await readFile(resolve(root, 'LICENSE'), 'utf8');
await writeFile(resolve(output, 'THIRD_PARTY_NOTICES.txt'),
    'Genro Typst JavaScript browser example\n\n'
    + 'Typst: Laurenz Mädje, Martin Haug and the Typst team and contributors. https://typst.app/\n'
    + 'typst.ts 0.7.0: Myriad-Dreamin and contributors. https://github.com/Myriad-Dreamin/typst.ts\n'
    + 'Genro Typst, genro-builders-js and genro-bag-js: Softwell S.r.l.\n'
    + 'These projects are licensed under Apache-2.0.\n\n' + license
    + '\nFonts are from typst-assets v0.13.1 and retain their own licenses:\n\n'
    + new TextDecoder().decode(notices)
    + '\nCodeMirror (MIT): https://codemirror.net/\n'
    + await readFile(resolve(root, 'node_modules/codemirror/LICENSE'), 'utf8'));
console.log(`Browser example built in ${output}`);
