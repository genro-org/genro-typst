// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { RendererBase, SourceBag } from '@genrojs/builders';
import { Bag } from '@genrojs/bag';
import catalog from './catalog.json' with { type: 'json' };
import { contentBlock, renderNative } from './native-renderer.js';
import {
    namedArguments, typstAlign, typstBool, typstColor, typstLength,
    typstString, typstStroke, typstWidth,
} from './values.js';

export class TypstRenderer extends RendererBase {
    static mode = 'typst';

    withDefaults(node, attrs) {
        const params = node.builder.schema[node.nodeTag].attributes?.parameters ?? [];
        return { ...Object.fromEntries(params.filter(p => p.has_default).map(p => [p.name, p.default])), ...attrs };
    }
    childAttrs(node) {
        return node.value instanceof SourceBag ? node.value.getNodes().map(
            child => this.withDefaults(child, child.builder.runtimeValues(child)[1]),
        ) : [];
    }
    parentAttrs(node) {
        const parent = node.parentBag.parentNode;
        return this.withDefaults(parent, parent.builder.runtimeValues(parent)[1]);
    }
    inherited(key, ...levels) {
        for (const attrs of levels) if (attrs[key] !== null && attrs[key] !== undefined) return Boolean(attrs[key]);
        throw new TypeError(`No level defines ${key}`);
    }
    renderedItem(node, item, runtimeAttrs, { tag }) {
        const children = Array.isArray(item) ? item : [];
        const attrs = this.withDefaults(node, runtimeAttrs);
        if ((Object.hasOwn(catalog.native, tag) || tag === 'call') && item != null && !Array.isArray(item)) {
            if (attrs.content != null) throw new TypeError('Use positional content or content=, not both');
            attrs.content = item;
        }
        const method = this[`render_${tag}`];
        return method ? method.call(this, node, children, attrs) : renderNative(tag, children, attrs);
    }
    render_document(_node, children, attrs) {
        const settings = [`#set page(paper: ${typstString(attrs.paper)}, flipped: ${typstBool(attrs.flipped)}, margin: ${typstLength(attrs.margin)})`];
        for (const [key, fn] of [['page_options', 'page'], ['metadata', 'document']]) {
            if (attrs[key] && Object.keys(attrs[key]).length) settings.push(`#set ${fn}(${namedArguments(attrs[key]).join(', ')})`);
        }
        return [...settings, ...children.map(child => `#${child}`)].join('\n') + '\n';
    }
    layoutStroke(attrs) {
        return attrs.border_width == null ? null : typstStroke(attrs.border_width, attrs.border_color);
    }
    render_layout(node, children, attrs) {
        const stroke = this.layoutStroke(attrs), rows = this.childAttrs(node), parts = [];
        children.forEach((fragment, index) => {
            parts.push(fragment);
            if (stroke && index < children.length - 1 && this.inherited('row_border', rows[index], attrs)) {
                parts.push(`grid.hline(stroke: ${stroke})`);
            }
        });
        const body = `grid(columns: (1fr,), ${parts.join(', ')})`;
        return stroke === null ? body : `block(width: 100%, stroke: ${stroke}, ${body})`;
    }
    render_row(node, children, attrs) {
        if (!children.length) return '[]';
        const layout = this.parentAttrs(node), stroke = this.layoutStroke(layout);
        const cells = this.childAttrs(node), parts = [];
        const columns = cells.map(cell => typstWidth(cell.width)).join(', ');
        children.forEach((fragment, index) => {
            parts.push(fragment);
            if (stroke && index < children.length - 1 && this.inherited('cell_border', cells[index], attrs, layout)) {
                parts.push(`grid.vline(x: ${index + 1}, stroke: ${stroke})`);
            }
        });
        const height = attrs.height == null ? 'auto' : typstLength(attrs.height);
        return `grid(columns: (${columns},), rows: (${height},), inset: ${typstLength(layout.inset)}, ${parts.join(', ')})`;
    }
    render_cell(_node, children, attrs) {
        const bodyParts = attrs.content == null ? [] : [`#${typstString(attrs.content)}`];
        bodyParts.push(...children.map(child => `#${child}`));
        let body = `[${bodyParts.join('\n')}]`;
        if (attrs.lbl != null) body = `stack(spacing: 0.8mm, text(size: 0.7em, fill: luma(90), ${typstString(attrs.lbl)}), ${body})`;
        const params = [];
        if (attrs.background != null) params.push(`fill: ${typstColor(attrs.background)}`);
        const align = typstAlign(attrs.align, attrs.valign);
        if (align !== null) params.push(`align: ${align}`);
        return `grid.cell(${[...params, body].join(', ')})`;
    }
    render_table(node, _children, attrs) {
        const columns = this.childAttrs(node), rows = attrs.data;
        if (!columns.length) throw new TypeError('A table needs at least one column');
        if (!(rows instanceof Bag)) throw new TypeError('table data must resolve to a Bag');
        const values = rows.values();
        const body = values.flatMap(row => columns.map(column => typstString(row.getItem(column.field) ?? '')));
        const parts = [
            `columns: (${columns.map(c => typstWidth(c.width)).join(', ')},)`,
            `align: (${columns.map(c => typstAlign(c.align, null) ?? 'auto').join(', ')},)`,
            `stroke: ${typstStroke(attrs.border_width, attrs.border_color)}`,
            `inset: ${typstLength(attrs.inset)}`,
            'fill: (x, y) => if y == 0 { luma(230) }',
            `table.header(repeat: ${typstBool(attrs.headerRepeat)}, ${columns.map(c => `strong(${typstString(c.name)})`).join(', ')})`,
            ...body,
        ];
        if (attrs.totalize_footer !== false) parts.push(this.totalFooter(columns, values, attrs.totalize_footer));
        return `table(${parts.join(', ')})`;
    }
    render_column() { return ''; }
    totalFooter(columns, rows, caption) {
        const cells = [];
        let run = 0, captioned = false;
        for (const column of [...columns, null]) {
            if (column !== null && !column.totalize) { run++; continue; }
            if (run) {
                const text = typeof caption === 'string' && !captioned ? caption : '';
                captioned = true;
                cells.push(`table.cell(colspan: ${run}, strong(${typstString(text)}))`);
                run = 0;
            }
            if (column !== null) {
                const total = rows.reduce((sum, row) => {
                    const value = row.getItem(column.field);
                    if (value == null) return sum;
                    if (typeof value !== 'number' && typeof value !== 'boolean') throw new TypeError('Totals require numeric values');
                    return sum + Number(value);
                }, 0);
                cells.push(`strong(${typstString(total)})`);
            }
        }
        return `table.footer(repeat: false, ${cells.join(', ')})`;
    }
    render_paragraph(_node, children, attrs) {
        return `par(${children.length ? contentBlock(children, attrs.content) : typstString(attrs.content)})`;
    }
    render_pageNumber(_node, _children, attrs) {
        const parts = attrs.template.split(/(\{page\}|\{total\})/).filter(Boolean).map(part => {
            if (part === '{page}') return '#counter(page).display()';
            if (part === '{total}') return '#counter(page).final().first()';
            return `#${typstString(part)}`;
        });
        return `context [${parts.join('')}]`;
    }
}
