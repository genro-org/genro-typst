// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import { writeFile } from 'node:fs/promises';
import { TypstBuilder, length } from '../src/index.js';

class Report extends TypstBuilder {
    main(root) {
        const doc = root.document({ paper: 'a4', margin: '18mm' });
        doc.set_rule({ target: 'text', size: length('11pt') });
        doc.heading('Quarterly report', { level: 1 });
        for (const name of ['Research', 'Development', 'Support']) {
            doc.par(`Department: ${name}`);
        }
    }
}

const report = new Report();
report.create();
// Node owns filesystem delivery; the builder itself also runs in browsers.
await writeFile(process.argv[2] ?? new URL('./report.typ', import.meta.url), report.render(), 'utf8');
