// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import catalog from './catalog.json' with { type: 'json' };
import { defaultRecipe } from './recipe.js';

export const sections = { overview: 'Getting started', documents: 'Real-world documents', ...catalog.sections };
export const examples = [{ id: 'welcome', title: 'Field notes', section: 'overview',
    description: 'A complete document with a table and a loop in both languages.',
    code: defaultRecipe, ...catalog.welcome, assets: {} },
...catalog.documents,
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
    read(example, language = 'javascript') {
        return this.drafts.get(`${example.id}/${language}`) ?? (language === 'python' ? example.python : example.code);
    }
    save(example, code, language = 'javascript') { this.drafts.set(`${example.id}/${language}`, code); }
    reset(example, language = 'javascript') {
        this.drafts.delete(`${example.id}/${language}`);
        return this.read(example, language);
    }
}
