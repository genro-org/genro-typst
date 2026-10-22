// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import catalog from './catalog.json' with { type: 'json' };
import { defaultRecipe } from './recipe.js';

export const sections = { overview: 'Getting started', ...catalog.sections };
export const examples = [{ id: 'welcome', title: 'Field notes', section: 'overview',
    description: 'A complete document with a table and a JavaScript loop.', code: defaultRecipe, assets: {} },
...catalog.examples.map(example => ({ ...example, compatibility: example.id === 'divider'
    ? 'divider requires a newer Typst compiler than typst.ts 0.7.0 provides. You can edit and download its source, but this browser runtime cannot preview it.'
    : '' }))];

export function filterExamples(query = '', section = '') {
    const words = query.toLowerCase().trim().split(/\s+/);
    return examples.filter(example => (!section || example.section === section)
        && words.every(word => `${example.id} ${example.title} ${example.description}`.toLowerCase().includes(word)));
}

// Drafts are scoped to the page session. Switching examples never loses edits.
export class RecipeDrafts {
    constructor() { this.drafts = new Map(); }
    read(example) { return this.drafts.get(example.id) ?? example.code; }
    save(example, code) { this.drafts.set(example.id, code); }
    reset(example) { this.drafts.delete(example.id); return example.code; }
}
