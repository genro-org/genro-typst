// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
let compilerPromise;

export function compiler() {
    if (!compilerPromise) compilerPromise = import('./vendor/typst.js').then(({ $typst, loadFonts }) => {
        const names = ['Regular', 'Bold', 'Italic', 'BoldItalic'].map(w => `LibertinusSerif-${w}.otf`);
        names.push('NewCMMath-Regular.otf');
        $typst.setCompilerInitOptions({
            getModule: () => window.$wasm$typst_compiler,
            beforeBuild: [loadFonts(names.map(name => new URL(`./fonts/${name}`, import.meta.url).href), { assets: false })],
        });
        return $typst;
    }).catch(reason => { compilerPromise = null; throw reason; });
    return compilerPromise;
}

export async function compileSvg(source, assets = {}) {
    const typst = await compiler();
    // Isolate virtual files: an import from the previous example must not leak.
    await typst.resetShadow();
    for (const [path, content] of Object.entries(assets)) {
        await typst.mapShadow('/' + path, new TextEncoder().encode(content));
    }
    await typst.addSource('/main.typ', source);
    const result = await typst.svg({ mainFilePath: '/main.typ', root: '/' });
    if (typeof result !== 'string' || !result.includes('<svg')) {
        throw new Error('Typst could not produce SVG. Check the generated source.');
    }
    const element = new DOMParser().parseFromString(result, 'text/html').querySelector('svg');
    if (!element) throw new Error('Typst returned no SVG element.');
    return new XMLSerializer().serializeToString(element);
}
