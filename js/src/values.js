// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import catalog from './catalog.json' with { type: 'json' };

export const isRecord = value => value !== null && typeof value === 'object'
    && [Object.prototype, null].includes(Object.getPrototypeOf(value));
export function pythonString(value) {
    if (value === null) return 'None';
    if (typeof value === 'boolean') return value ? 'True' : 'False';
    if (typeof value === 'string' || typeof value === 'number') return String(value);
    throw new TypeError('Expected scalar text');
}
export function typstString(value) {
    return '"' + pythonString(value).replaceAll('\\', '\\\\').replaceAll('"', '\\"')
        .replaceAll('\n', '\\n').replaceAll('\r', '\\r').replaceAll('\t', '\\t') + '"';
}
export function expr(code) {
    if (typeof code !== 'string' || !code.trim()) throw new TypeError('Expected nonempty Typst expression');
    return { $typst: code };
}
export function typstLength(value) {
    if (typeof value !== 'string' || !(value === 'auto'
        || /^-?\d+(\.\d+)?(mm|cm|pt|in|em|%|fr)$/.test(value))) {
        throw new TypeError('Expected a length with unit, or auto');
    }
    return value;
}
export function typstColor(value) {
    if (typeof value === 'string' && /^#([\da-fA-F]{6}|[\da-fA-F]{3})$/.test(value)) {
        return `rgb("${value}")`;
    }
    if (catalog.namedColors.includes(value)) return value;
    throw new TypeError('Expected named or hexadecimal color');
}
export const length = value => expr(typstLength(value));
export const color = value => expr(typstColor(value));
export const label = name => expr(`label(${typstString(name)})`);
export const markup = source => expr(`[${source}\n]`);
export function identifier(name) {
    if (typeof name !== 'string' || !/^[A-Za-z_][A-Za-z0-9_-]*(\.[A-Za-z_][A-Za-z0-9_-]*)*$/.test(name)) {
        throw new TypeError(`Invalid Typst identifier: ${name}`);
    }
    return name;
}
export function valueCode(value) {
    if (value === null) return 'none';
    if (typeof value === 'boolean') return value ? 'true' : 'false';
    if (typeof value === 'string') return typstString(value);
    if (typeof value === 'number') {
        if (!Number.isFinite(value)) throw new TypeError('Typst numbers must be finite');
        // Python uses scientific notation below 1e-4 and pads small exponents.
        const result = value !== 0 && Math.abs(value) < 1e-4 ? value.toExponential() : String(value);
        return result.replace(/e([+-])(\d)$/, 'e$10$2');
    }
    if (Array.isArray(value)) return '(' + value.map(valueCode).join(', ') + (value.length ? ',)' : ')');
    if (isRecord(value)) {
        const keys = Object.keys(value);
        if (Object.hasOwn(value, '$typst')) {
            if (keys.length !== 1) throw new TypeError('Expression marker cannot contain other keys');
            return expr(value.$typst).$typst;
        }
        if (!keys.length) return '(:)';
        return '(' + keys.map(key => `${typstString(key)}: ${valueCode(value[key])}`).join(', ') + ',)';
    }
    throw new TypeError(`Cannot encode ${typeof value} as a Typst value`);
}
export function namedArguments(options) {
    if (!isRecord(options)) throw new TypeError('Expected an options object');
    const seen = new Set();
    return Object.entries(options).map(([key, value]) => {
        const name = identifier(key.replace(/_$/, '').replaceAll('_', '-'));
        if (name.includes('.')) throw new TypeError('Argument name cannot be a dotted path');
        if (seen.has(name)) throw new TypeError(`Duplicate Typst argument: ${name}`);
        seen.add(name);
        return `${name}: ${valueCode(value)}`;
    });
}
export function typstWidth(value) {
    if (typeof value === 'number') {
        if (!Number.isFinite(value) || value < 0) throw new TypeError('Invalid column width');
        return value === 0 ? '1fr' : `${value}fr`;
    }
    return typstLength(value);
}
export function typstBool(value) {
    if (typeof value !== 'boolean') throw new TypeError('Expected a boolean');
    return value ? 'true' : 'false';
}
export function typstAlign(align, valign) {
    const parts = [];
    if (align != null) {
        if (!['left', 'center', 'right'].includes(align)) throw new TypeError('Invalid alignment');
        parts.push(align);
    }
    if (valign != null) {
        if (!['top', 'middle', 'bottom'].includes(valign)) throw new TypeError('Invalid vertical alignment');
        parts.push(valign === 'middle' ? 'horizon' : valign);
    }
    return parts.length ? parts.join(' + ') : null;
}
export const typstStroke = (width, color) => `${typstLength(width)} + ${typstColor(color)}`;
