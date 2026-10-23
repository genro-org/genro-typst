// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { EditorState } from '@codemirror/state';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';

export function createEditor(parent, { label, readOnly = false, language, onChange = () => {}, onRun = () => {} }) {
    const extensions = [basicSetup, EditorView.lineWrapping,
        EditorView.contentAttributes.of({ 'aria-label': label, 'aria-readonly': String(readOnly) }),
        EditorView.updateListener.of(update => { if (update.docChanged) onChange(); }),
        keymap.of([{ key: 'Mod-Enter', run: () => { onRun(); return true; } }]),
        EditorState.readOnly.of(readOnly), EditorView.editable.of(!readOnly),
    ];
    if (language === 'python') extensions.push(python());
    else if (!readOnly) extensions.push(javascript());
    const view = new EditorView({ parent, extensions });
    return {
        get value() { return view.state.doc.toString(); },
        set value(doc) { view.setState(EditorState.create({ doc, extensions })); },
        measure() { view.requestMeasure(); },
    };
}
