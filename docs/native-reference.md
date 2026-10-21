# Riferimento degli elementi nativi

Generato da `native_catalog.py` con `tools/generate_reference.py`. Non modificare a mano.

**129 chiamate native**, verificate su Typst **0.15.0**, oltre ai costrutti
di linguaggio elencati sotto e agli otto elementi storici per documenti commerciali.

Per i tipi dei parametri e i relativi valori predefiniti, seguire i collegamenti
alla documentazione ufficiale. Le pagine online possono descrivere versioni più
recenti: il riferimento eseguibile di questo progetto resta Typst 0.15.0.

## Firma comune

```python
node.heading(content=None, args=None, options=None, **parametri_typst)
```

`content` accetta anche la prima posizione (`node.heading('Titolo')`).
`args` è una lista di argomenti posizionali Typst; `options` permette nomi che
collidono con quelli del builder. I parametri aggiuntivi sono inoltrati a Typst:
i loro nomi e tipi vengono verificati dal compilatore, non tutti dallo schema Python.

| Modalità | Significato |
|---|---|
| `body` | Testo iniziale e figli formano un unico contenuto; nessuno spazio implicito tra figli. |
| `items` | Ogni figlio diventa un argomento distinto, ad esempio una cella. |
| `args` | Argomenti e figli sono passati separatamente; segue i tipi della funzione. |
| `value` | Il contenuto iniziale è un valore posizionale, ad esempio URL o percorso; i figli formano un eventuale corpo. |
| `leaf` | Senza contenuto/figli; restano disponibili `args` e parametri nominati. |

Le stringhe restano stringhe. Usare `length`, `color`, `label`, `expr` e `markup`
per valori Typst non testuali. I metodi con underscore corrispondono ai percorsi
puntati di Typst (`table_cell` → `table.cell`); gli underscore nei parametri
diventano trattini (`column_gutter` → `column-gutter`).

## text

[Riferimento ufficiale](https://typst.app/docs/reference/text/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`text`](catalog-examples.md#text) | `text` | `body` |
| [`underline`](catalog-examples.md#underline) | `underline` | `body` |
| [`overline`](catalog-examples.md#overline) | `overline` | `body` |
| [`strike`](catalog-examples.md#strike) | `strike` | `body` |
| [`highlight`](catalog-examples.md#highlight) | `highlight` | `body` |
| [`smallcaps`](catalog-examples.md#smallcaps) | `smallcaps` | `body` |
| [`sub`](catalog-examples.md#sub) | `sub` | `body` |
| [`super`](catalog-examples.md#super) | `super` | `body` |
| [`lower`](catalog-examples.md#lower) | `lower` | `body` |
| [`upper`](catalog-examples.md#upper) | `upper` | `body` |
| [`raw`](catalog-examples.md#raw) | `raw` | `value` |
| [`lorem`](catalog-examples.md#lorem) | `lorem` | `value` |
| [`linebreak`](catalog-examples.md#linebreak) | `linebreak` | `leaf` |
| [`smartquote`](catalog-examples.md#smartquote) | `smartquote` | `leaf` |

## model

[Riferimento ufficiale](https://typst.app/docs/reference/model/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`heading`](catalog-examples.md#heading) | `heading` | `body` |
| [`strong`](catalog-examples.md#strong) | `strong` | `body` |
| [`emph`](catalog-examples.md#emph) | `emph` | `body` |
| [`par`](catalog-examples.md#par) | `par` | `body` |
| [`quote`](catalog-examples.md#quote) | `quote` | `body` |
| [`figure`](catalog-examples.md#figure) | `figure` | `body` |
| [`footnote`](catalog-examples.md#footnote) | `footnote` | `body` |
| [`title`](catalog-examples.md#title) | `title` | `body` |
| [`list`](catalog-examples.md#list) | `list` | `items` |
| [`enum`](catalog-examples.md#enum) | `enum` | `items` |
| [`terms`](catalog-examples.md#terms) | `terms` | `items` |
| [`list_item`](catalog-examples.md#list_item) | `list.item` | `body` |
| [`enum_item`](catalog-examples.md#enum_item) | `enum.item` | `body` |
| [`terms_item`](catalog-examples.md#terms_item) | `terms.item` | `args` |
| [`link`](catalog-examples.md#link) | `link` | `value` |
| [`ref`](catalog-examples.md#ref) | `ref` | `value` |
| [`cite`](catalog-examples.md#cite) | `cite` | `value` |
| [`bibliography`](catalog-examples.md#bibliography) | `bibliography` | `value` |
| [`numbering`](catalog-examples.md#numbering) | `numbering` | `value` |
| [`outline`](catalog-examples.md#outline) | `outline` | `leaf` |
| [`parbreak`](catalog-examples.md#parbreak) | `parbreak` | `leaf` |
| [`divider`](catalog-examples.md#divider) | `divider` | `leaf` |
| [`table_header`](catalog-examples.md#table_header) | `table.header` | `items` |
| [`table_footer`](catalog-examples.md#table_footer) | `table.footer` | `items` |
| [`table_cell`](catalog-examples.md#table_cell) | `table.cell` | `body` |
| [`table_hline`](catalog-examples.md#table_hline) | `table.hline` | `leaf` |
| [`table_vline`](catalog-examples.md#table_vline) | `table.vline` | `leaf` |
| [`native_table`](catalog-examples.md#native_table) | `table` | `items` |

## layout

[Riferimento ufficiale](https://typst.app/docs/reference/layout/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`align`](catalog-examples.md#align) | `align` | `body` |
| [`block`](catalog-examples.md#block) | `block` | `body` |
| [`box`](catalog-examples.md#box) | `box` | `body` |
| [`columns`](catalog-examples.md#columns) | `columns` | `body` |
| [`hide`](catalog-examples.md#hide) | `hide` | `body` |
| [`move`](catalog-examples.md#move) | `move` | `body` |
| [`pad`](catalog-examples.md#pad) | `pad` | `body` |
| [`page`](catalog-examples.md#page) | `page` | `body` |
| [`place`](catalog-examples.md#place) | `place` | `body` |
| [`repeat`](catalog-examples.md#repeat) | `repeat` | `body` |
| [`rotate`](catalog-examples.md#rotate) | `rotate` | `body` |
| [`scale`](catalog-examples.md#scale) | `scale` | `body` |
| [`skew`](catalog-examples.md#skew) | `skew` | `body` |
| [`grid`](catalog-examples.md#grid) | `grid` | `items` |
| [`stack`](catalog-examples.md#stack) | `stack` | `items` |
| [`grid_header`](catalog-examples.md#grid_header) | `grid.header` | `items` |
| [`grid_footer`](catalog-examples.md#grid_footer) | `grid.footer` | `items` |
| [`grid_cell`](catalog-examples.md#grid_cell) | `grid.cell` | `body` |
| [`pagebreak`](catalog-examples.md#pagebreak) | `pagebreak` | `leaf` |
| [`colbreak`](catalog-examples.md#colbreak) | `colbreak` | `leaf` |
| [`grid_hline`](catalog-examples.md#grid_hline) | `grid.hline` | `leaf` |
| [`grid_vline`](catalog-examples.md#grid_vline) | `grid.vline` | `leaf` |
| [`h`](catalog-examples.md#h) | `h` | `value` |
| [`v`](catalog-examples.md#v) | `v` | `value` |
| [`measure`](catalog-examples.md#measure) | `measure` | `value` |
| [`native_layout`](catalog-examples.md#native_layout) | `layout` | `value` |

## visualize

[Riferimento ufficiale](https://typst.app/docs/reference/visualize/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`circle`](catalog-examples.md#circle) | `circle` | `body` |
| [`ellipse`](catalog-examples.md#ellipse) | `ellipse` | `body` |
| [`rect`](catalog-examples.md#rect) | `rect` | `body` |
| [`square`](catalog-examples.md#square) | `square` | `body` |
| [`image`](catalog-examples.md#image) | `image` | `value` |
| [`line`](catalog-examples.md#line) | `line` | `args` |
| [`polygon`](catalog-examples.md#polygon) | `polygon` | `args` |
| [`curve`](catalog-examples.md#curve) | `curve` | `args` |
| [`curve_move`](catalog-examples.md#curve_move) | `curve.move` | `args` |
| [`curve_line`](catalog-examples.md#curve_line) | `curve.line` | `args` |
| [`curve_quad`](catalog-examples.md#curve_quad) | `curve.quad` | `args` |
| [`curve_cubic`](catalog-examples.md#curve_cubic) | `curve.cubic` | `args` |
| [`curve_close`](catalog-examples.md#curve_close) | `curve.close` | `args` |

## math

[Riferimento ufficiale](https://typst.app/docs/reference/math/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`math_equation`](catalog-examples.md#math_equation) | `math.equation` | `body` |
| [`math_upright`](catalog-examples.md#math_upright) | `math.upright` | `body` |
| [`math_italic`](catalog-examples.md#math_italic) | `math.italic` | `body` |
| [`math_bold`](catalog-examples.md#math_bold) | `math.bold` | `body` |
| [`math_serif`](catalog-examples.md#math_serif) | `math.serif` | `body` |
| [`math_sans`](catalog-examples.md#math_sans) | `math.sans` | `body` |
| [`math_cal`](catalog-examples.md#math_cal) | `math.cal` | `body` |
| [`math_frak`](catalog-examples.md#math_frak) | `math.frak` | `body` |
| [`math_mono`](catalog-examples.md#math_mono) | `math.mono` | `body` |
| [`math_bb`](catalog-examples.md#math_bb) | `math.bb` | `body` |
| [`math_display`](catalog-examples.md#math_display) | `math.display` | `body` |
| [`math_inline`](catalog-examples.md#math_inline) | `math.inline` | `body` |
| [`math_script`](catalog-examples.md#math_script) | `math.script` | `body` |
| [`math_sscript`](catalog-examples.md#math_sscript) | `math.sscript` | `body` |
| [`math_frac`](catalog-examples.md#math_frac) | `math.frac` | `args` |
| [`math_root`](catalog-examples.md#math_root) | `math.root` | `args` |
| [`math_sqrt`](catalog-examples.md#math_sqrt) | `math.sqrt` | `args` |
| [`math_binom`](catalog-examples.md#math_binom) | `math.binom` | `args` |
| [`math_vec`](catalog-examples.md#math_vec) | `math.vec` | `args` |
| [`math_mat`](catalog-examples.md#math_mat) | `math.mat` | `args` |
| [`math_cases`](catalog-examples.md#math_cases) | `math.cases` | `args` |
| [`math_lr`](catalog-examples.md#math_lr) | `math.lr` | `args` |
| [`math_attach`](catalog-examples.md#math_attach) | `math.attach` | `args` |
| [`math_accent`](catalog-examples.md#math_accent) | `math.accent` | `args` |
| [`math_cancel`](catalog-examples.md#math_cancel) | `math.cancel` | `args` |
| [`math_class`](catalog-examples.md#math_class) | `math.class` | `args` |
| [`math_op`](catalog-examples.md#math_op) | `math.op` | `args` |
| [`math_limits`](catalog-examples.md#math_limits) | `math.limits` | `args` |
| [`math_scripts`](catalog-examples.md#math_scripts) | `math.scripts` | `args` |
| [`math_abs`](catalog-examples.md#math_abs) | `math.abs` | `args` |
| [`math_norm`](catalog-examples.md#math_norm) | `math.norm` | `args` |
| [`math_floor`](catalog-examples.md#math_floor) | `math.floor` | `args` |
| [`math_ceil`](catalog-examples.md#math_ceil) | `math.ceil` | `args` |
| [`math_round`](catalog-examples.md#math_round) | `math.round` | `args` |
| [`math_stretch`](catalog-examples.md#math_stretch) | `math.stretch` | `args` |
| [`math_underbrace`](catalog-examples.md#math_underbrace) | `math.underbrace` | `args` |
| [`math_overbrace`](catalog-examples.md#math_overbrace) | `math.overbrace` | `args` |
| [`math_underbracket`](catalog-examples.md#math_underbracket) | `math.underbracket` | `args` |
| [`math_overbracket`](catalog-examples.md#math_overbracket) | `math.overbracket` | `args` |
| [`math_underline`](catalog-examples.md#math_underline) | `math.underline` | `args` |
| [`math_overline`](catalog-examples.md#math_overline) | `math.overline` | `args` |
| [`math_underparen`](catalog-examples.md#math_underparen) | `math.underparen` | `args` |
| [`math_overparen`](catalog-examples.md#math_overparen) | `math.overparen` | `args` |
| [`math_undershell`](catalog-examples.md#math_undershell) | `math.undershell` | `args` |
| [`math_overshell`](catalog-examples.md#math_overshell) | `math.overshell` | `args` |
| [`math_primes`](catalog-examples.md#math_primes) | `math.primes` | `args` |

## introspection

[Riferimento ufficiale](https://typst.app/docs/reference/introspection/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`metadata`](catalog-examples.md#metadata) | `metadata` | `value` |

## pdf

[Riferimento ufficiale](https://typst.app/docs/reference/pdf/)

| Metodo builder (esempio verificato) | Funzione Typst | Modalità |
|---|---|---|
| [`pdf_artifact`](catalog-examples.md#pdf_artifact) | `pdf.artifact` | `body` |

## Costrutti del linguaggio

`call`, `set_rule`, `show_rule`, `scope`, `context`, `equation`, `label`, `let`, `import_module`, `include`, `typst_code`, `typst_markup`

Firme, esempi e limiti sono descritti nella [guida](typst-guide.md).
