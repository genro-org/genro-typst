// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { recipeSource } from './recipe.js';
import { examples, sections, filterExamples, RecipeDrafts } from './collection.js';
import { compileSvg } from './compiler.js';
import { createEditor } from './editor.js';

const $ = selector => document.querySelector(selector);
const preview = $('#preview'), status = $('#status'), error = $('#error');
const run = $('#run'), reset = $('#reset'), check = $('#check-all');
const typDownload = $('#download-typ'), svgDownload = $('#download-svg');
const search = $('#example-search'), category = $('#category'), list = $('#example-list');
const drafts = new RecipeDrafts();
let selected = examples[0], svg = '', previewUrl, busy = false, renderedRecipe = '', renderTimer;
function scheduleRender() {
    clearTimeout(renderTimer);
    if ($('#live-preview').checked) renderTimer = setTimeout(render, 650);
}
const editor = createEditor($('#recipe'), { label: 'JavaScript recipe', onRun: render, onChange() {
    drafts.save(selected, editor.value);
    if (!busy && editor.value !== renderedRecipe) {
        status.dataset.state = 'changed';
        status.textContent = 'Recipe changed · run to update';
    }
    scheduleRender();
}});
const source = createEditor($('#source'), { label: 'Generated Typst source', readOnly: true });

function setBusy(value) {
    busy = value;
    run.disabled = reset.disabled = check.disabled = value;
    for (const button of list.querySelectorAll('button')) button.disabled = value;
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
    clearTimeout(renderTimer);
    setBusy(true);
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
        status.textContent = 'Typesetting with the local Typst compiler…';
        svg = await compileSvg(source.value, selected.assets);
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
        setBusy(false);
        if (editor.value !== code) scheduleRender();
    }
}
function download(content, type, name) {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const link = document.createElement('a');
    link.href = url; link.download = name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function updateList() {
    list.replaceChildren();
    const matches = filterExamples(search.value, category.value);
    $('#example-count').textContent = `${matches.length} / ${examples.length} examples`;
    for (const example of matches) {
        const button = document.createElement('button');
        button.textContent = example.title + (example.compatibility ? ' ⚠' : '');
        button.dataset.id = example.id;
        button.setAttribute('aria-pressed', String(example.id === selected.id));
        button.disabled = busy;
        button.addEventListener('click', () => select(example));
        list.append(button);
    }
    if (!matches.length) list.textContent = 'No matching examples.';
}
function select(example) {
    if (busy) return;
    drafts.save(selected, editor.value);
    selected = example;
    editor.value = drafts.read(example);
    $('#example-title').textContent = example.title;
    $('#example-description').textContent = example.description;
    $('#compatibility').textContent = example.compatibility || '';
    $('#compatibility').hidden = !example.compatibility;
    const assets = $('#assets');
    assets.replaceChildren();
    const files = Object.entries(example.assets);
    assets.hidden = !files.length;
    for (const [name, content] of files) {
        const details = document.createElement('details');
        const summary = document.createElement('summary');
        summary.textContent = `Included file: ${name}`;
        const code = document.createElement('pre'); code.textContent = content;
        const save = document.createElement('button');
        save.textContent = 'Download ' + name;
        save.addEventListener('click', () => download(content, 'text/plain;charset=utf-8', name));
        details.append(summary, code, save); assets.append(details);
    }
    updateList();
    render();
}
for (const [value, title] of Object.entries(sections)) {
    const option = document.createElement('option'); option.value = value; option.textContent = title;
    category.append(option);
}
search.addEventListener('input', updateList);
category.addEventListener('change', updateList);
$('#live-preview').addEventListener('change', scheduleRender);
run.addEventListener('click', render);
reset.addEventListener('click', () => { editor.value = drafts.reset(selected); render(); });
typDownload.addEventListener('click', () => download(source.value, 'text/plain;charset=utf-8', `${selected.id}.typ`));
svgDownload.addEventListener('click', () => download(svg, 'image/svg+xml', `${selected.id}.svg`));
check.addEventListener('click', async () => {
    if (busy) return;
    setBusy(true);
    clearTimeout(renderTimer);
    const results = $('#check-results');
    results.hidden = false;
    results.replaceChildren();
    let passed = 0, unavailable = 0, failed = 0;
    try {
        for (const example of examples) {
            status.dataset.state = 'working';
            status.textContent = `Checking ${example.title}…`;
            try {
                await compileSvg(recipeSource(example.code), example.assets);
                passed++;
            } catch (reason) {
                const message = reason instanceof Error ? reason.message : String(reason);
                const knownLimit = example.compatibility && message.includes('unknown variable: divider');
                if (knownLimit) unavailable++; else failed++;
                const item = document.createElement('li');
                item.textContent = knownLimit ? example.compatibility : `${example.title}: ${message}`;
                results.append(item);
            }
            $('#check-summary').textContent = `${passed} passed · ${unavailable} unavailable · ${failed} failed · ${examples.length} total`;
            await new Promise(resolve => setTimeout(resolve, 0));
        }
    } finally {
        setBusy(false);
        // Restore the selected document and its virtual files after validation.
        await render();
    }
});
editor.value = selected.code;
select(selected);
