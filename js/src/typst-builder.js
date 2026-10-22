// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { BuilderBase, SourceBag } from '@genrojs/builders';
import grammar from './typst.json' with { type: 'json' };
import catalog from './catalog.json' with { type: 'json' };
import { TypstRenderer } from './typst-renderer.js';

export class TypstBuilder extends BuilderBase {
    static _name = 'typst';
    static _defaultRenderMode = 'typst';
    static { this.defineGrammar(grammar); }

    get renderer_typst() { return new TypstRenderer(this); }

    setChild(bag, tag, value, attrs, parentOverride = null) {
        // Preserve initial native content when a leaf gains children, as Python does.
        if ((Object.hasOwn(catalog.native, tag) || tag === 'call')
            && value !== null && value !== undefined && !(value instanceof SourceBag)) {
            if (Object.hasOwn(attrs, 'content')) throw new TypeError('Use positional content or content=, not both');
            attrs = { ...attrs, content: value };
            value = null;
        }
        return super.setChild(bag, tag, value, attrs, parentOverride);
    }
}

BuilderBase.registerBuilder(TypstBuilder);
