// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import catalog from './catalog.json' with { type: 'json' };
import { identifier, isRecord, namedArguments, typstString, valueCode } from './values.js';

const statement = text => /^(set |show |let |import )/.test(text);
export function contentBlock(children, content = null) {
    const parts = content === null ? [] : [`#${valueCode(content)}`];
    for (const child of children) if (child) parts.push(`#${child}${statement(child) ? ';\n' : ''}`);
    return `[${parts.join('')}]`;
}
function options(attrs, reserved) {
    const opts = attrs.options ?? {};
    if (!isRecord(opts)) throw new TypeError('options must be an object');
    const extra = Object.fromEntries(Object.entries(attrs).filter(([key]) => !reserved.includes(key) && key !== '_meta'));
    if (Object.keys(opts).some(key => Object.hasOwn(extra, key))) throw new TypeError('Duplicate options');
    return { ...opts, ...extra };
}
export function renderCall(fn, mode, children, attrs) {
    identifier(fn);
    if (!['body', 'items', 'args', 'value', 'leaf'].includes(mode)) throw new TypeError(`Unknown call mode: ${mode}`);
    const args = attrs.args ?? [];
    if (!Array.isArray(args)) throw new TypeError('args must be an array');
    const parts = args.map(valueCode);
    parts.push(...namedArguments(options(attrs, ['content', 'args', 'options'])));
    const content = attrs.content ?? null;
    if (mode === 'body') {
        if (content !== null || children.length) parts.push(contentBlock(children, content));
    } else if (mode === 'items' || mode === 'args') {
        if (content !== null) parts.push(valueCode(content));
        for (const child of children) {
            if (statement(child)) throw new TypeError('Put rules inside a scope, not among call arguments');
            parts.push(child);
        }
    } else if (mode === 'value') {
        if (content !== null) parts.push(valueCode(content));
        if (children.length) parts.push(contentBlock(children));
    } else if (content !== null || children.length) throw new TypeError(`${fn} does not accept child content`);
    return `${fn}(${parts.join(', ')})`;
}
export function renderNative(tag, children, attrs) {
    if (Object.hasOwn(catalog.native, tag)) {
        const [fn, mode] = catalog.native[tag];
        return renderCall(fn, mode, children, attrs);
    }
    switch (tag) {
    case 'call': {
        const { function: fn, mode, ...params } = attrs;
        return renderCall(fn, mode, children, params);
    }
    case 'scope': case 'context': return (tag === 'context' ? 'context ' : '') + contentBlock(children);
    case 'set_rule': return `set ${identifier(attrs.target)}(${namedArguments(options(attrs, ['target', 'options'])).join(', ')})`;
    case 'show_rule': {
        const selector = typeof attrs.selector === 'string' ? identifier(attrs.selector) : valueCode(attrs.selector);
        const opts = options(attrs, ['selector', 'transform', 'target', 'options']);
        let transform;
        if (attrs.target !== null) {
            if (attrs.transform !== null) throw new TypeError('A show rule takes either transform or target');
            transform = `set ${identifier(attrs.target)}(${namedArguments(opts).join(', ')})`;
        } else {
            if (attrs.transform === null || Object.keys(opts).length) throw new TypeError('Show requires transform and no set options');
            transform = valueCode(attrs.transform);
        }
        return `show ${selector}: ${transform}`;
    }
    case 'equation': {
        const { formula, _meta, ...opts } = attrs;
        return `math.equation(${namedArguments(opts).join(', ')}, $${formula}$)`;
    }
    case 'label': return `label(${typstString(attrs.name)})`;
    case 'let': {
        if (identifier(attrs.name).includes('.')) throw new TypeError('A let binding needs a simple name');
        return `let ${attrs.name} = ${valueCode(attrs.value)}`;
    }
    case 'import_module': {
        let result = `import ${typstString(attrs.path)}`;
        if (attrs.alias !== null) {
            if (identifier(attrs.alias).includes('.')) throw new TypeError('An import alias needs a simple name');
            result += ` as ${attrs.alias}`;
        }
        if (attrs.names?.length) {
            if (attrs.names.length === 1 && attrs.names[0] === '*') result += ': *';
            else result += ': ' + attrs.names.map(name => {
                if (identifier(name).includes('.')) throw new TypeError('An imported binding needs a simple name');
                return name;
            }).join(', ');
        }
        return result;
    }
    case 'include': return `include ${typstString(attrs.path)}`;
    case 'typst_code': return `{${attrs.code}\n}`;
    case 'typst_markup': return `[${attrs.source}\n]`;
    default: throw new TypeError(`Unknown Typst element: ${tag}`);
    }
}
