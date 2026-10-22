// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { defaultRecipe, recipeSource } from './recipe.js';

const editor = document.querySelector('#recipe');
const source = document.querySelector('#source');
const preview = document.querySelector('#preview');
const status = document.querySelector('#status');
const error = document.querySelector('#error');
const run = document.querySelector('#run');
const reset = document.querySelector('#reset');
const typDownload = document.querySelector('#download-typ');
const svgDownload = document.querySelector('#download-svg');
let compilerPromise;
let svg = '';
let previewUrl;
let busy = false;
let renderedRecipe = '';

function compiler() {
    if (!compilerPromise) compilerPromise = import('./vendor/typst.js').then(({ $typst, loadFonts }) => {
        const fonts = ['Regular', 'Bold', 'Italic', 'BoldItalic'].map(
            weight => new URL(`./fonts/LibertinusSerif-${weight}.otf`, import.meta.url).href,
        );
        $typst.setCompilerInitOptions({
            getModule: () => window.$wasm$typst_compiler,
            beforeBuild: [loadFonts(fonts, { assets: false })],
        });
        return $typst;
    }).catch(reason => { compilerPromise = null; throw reason; });
    return compilerPromise;
}

function clearPreview() {
    preview.replaceChildren();
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = undefined;
    svg = '';
    svgDownload.disabled = true;
}

async function render() {
    if (busy) return;
    busy = true;
    run.disabled = reset.disabled = true;
    error.hidden = true;
    status.dataset.state = 'working';
    status.textContent = 'Building document…';
    clearPreview();
    source.value = '';
    typDownload.disabled = true;
    const code = editor.value;
    try {
        source.value = recipeSource(code);
        typDownload.disabled = false;
        status.textContent = compilerPromise ? 'Typesetting with Typst…' : 'Loading the local Typst compiler…';
        const typst = await compiler();
        const result = await typst.svg({ mainContent: source.value });
        if (typeof result !== 'string' || !result.includes('<svg')) {
            throw new Error('Typst could not produce SVG. Check the generated source.');
        }
        // typst.ts emits SVG for HTML embedding; serialize it as standalone XML.
        const parsed = new DOMParser().parseFromString(result, 'text/html');
        const svgElement = parsed.querySelector('svg');
        if (!svgElement) throw new Error('Typst returned no SVG element.');
        svg = new XMLSerializer().serializeToString(svgElement);
        // An image keeps generated SVG scripts and links out of the page DOM.
        previewUrl = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
        const image = new Image();
        image.alt = 'Document rendered by Typst';
        const loaded = new Promise((resolve, reject) => {
            image.onload = resolve;
            image.onerror = () => reject(new Error('The generated SVG could not be displayed.'));
        });
        image.src = previewUrl;
        await loaded;
        preview.replaceChildren(image);
        svgDownload.disabled = false;
        renderedRecipe = code;
        status.dataset.state = 'ready';
        status.textContent = editor.value === code ? 'Ready · rendered in your browser' : 'Recipe changed · run to update';
    } catch (reason) {
        clearPreview();
        error.textContent = reason instanceof Error ? reason.message : String(reason);
        error.hidden = false;
        status.dataset.state = 'error';
        status.textContent = 'Could not render · check the error below';
    } finally {
        busy = false;
        run.disabled = reset.disabled = false;
    }
}

function download(content, type, name) {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const link = document.createElement('a');
    link.href = url; link.download = name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}
run.addEventListener('click', render);
reset.addEventListener('click', () => { editor.value = defaultRecipe; render(); });
typDownload.addEventListener('click', () => download(source.value, 'text/plain;charset=utf-8', 'document.typ'));
svgDownload.addEventListener('click', () => download(svg, 'image/svg+xml', 'document.svg'));
editor.addEventListener('input', () => {
    if (!busy && editor.value !== renderedRecipe) {
        status.dataset.state = 'changed';
        status.textContent = 'Recipe changed · run to update';
    }
});
editor.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); render(); }
});
editor.value = defaultRecipe;
render();
