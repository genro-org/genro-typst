# genro-typst

Print documents (invoices, delivery notes, quotes, labels, schemas) described
with a genro-builders grammar and typeset by [Typst](https://typst.app).

Status: prototype. The grammar has `document`, `layout`, `row`, `cell`,
`paragraph`, `pageNumber`. Two render modes: `typst` (source code) and
`pdf`. Example: `examples/01_invoice_header/`.
The design proposal is in `xmldocs/proposal/typst-backend.md`.

## Pinned versions

- Python binding `typst` 0.15.0 (PyPI), which bundles Typst 0.15.0.

## License

Apache License 2.0. See `LICENSE` and `NOTICE`.
