// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { EditorState } from '@codemirror/state';
import { javascript } from '@codemirror/lang-javascript';

export function createEditor(parent, { label, readOnly = false, onChange = () => {}, onRun = () => {} }) {
    const extensions = [basicSetup, EditorView.lineWrapping,
        EditorView.contentAttributes.of({ 'aria-label': label }),
        EditorView.updateListener.of(update => { if (update.docChanged) onChange(); }),
        keymap.of([{ key: 'Mod-Enter', run: () => { onRun(); return true; } }]),
        EditorState.readOnly.of(readOnly), EditorView.editable.of(!readOnly),
    ];
    if (!readOnly) extensions.push(javascript());
    const view = new EditorView({ parent, extensions });
    return {
        get value() { return view.state.doc.toString(); },
        set value(doc) { view.setState(EditorState.create({ doc, extensions })); },
    };
}
