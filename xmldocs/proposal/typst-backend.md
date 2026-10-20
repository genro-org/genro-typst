<!-- generated from typst-backend.xml by xmldocs: do not edit, edit the XML -->

## Stampe con genro-builders e Typst
*Proposal · proposal/typst-backend · 2026-10-20 · draft*

### Problem

Le stampe commerciali (fatture, DDT, preventivi, etichette) e gli schemi oggi passano da HTML a PDF, oppure da ReportLab in genro-print.

Typst è un motore di composizione tipografica scritto in Rust, licenza Apache-2.0. Compila un sorgente testuale in PDF, SVG, PNG.

Questo progetto descrive il documento con una grammatica genro-builders e lo fa comporre a Typst.

Obiettivo finale: in gramlot, un editor di carte intestate analogo a quello di GenroPy e un editor di stampe per applicazioni business: liste, pagine, moduli. Gli editor non fanno parte di questo progetto. genro-typst fornisce la grammatica, il formato salvato e il renderer.

### Current state

- `READ` `genro-print/src/genro_print/builders/print_lrc_builder.py` · 2026-10-20 — genro-print separa la grammatica (builder con mixin: document, platypus, canvas, lrc, styled, charts) dai renderer ReportLab. Ogni builder espone il renderer con la property `renderer_reportlab` e `_default_render_mode = "reportlab"`.
- `RUN` `genro-print (git status)` · 2026-10-20 — In genro-print lo spostamento da `compilers/` a `renderers/` è nel working tree, non committato. L'ultimo commit è del 2026-04-07.
- `READ` `genro-builders/src/genro_builders/contrib/svg/svg_builder.py` · 2026-10-20 — Il dialetto SVG di genro-builders ha tre parti: `SvgBuilder` (grammatica, `_name = "svg"`), `SvgElements` (elementi dichiarati con `@element`), `SvgRenderer` (sottoclasse di `RendererBase`, `mode = "svg"`, metodo `rendered_item`) esposto dalla property `renderer_svg`.

### Proposed solution

#### Principio

- **must** — La grammatica descrive il documento commerciale, non il linguaggio Typst. Non si avvolge l'intero linguaggio Typst.
- **must** — Il renderer emette costrutti Typst fissi. Chi usa il builder non scrive mai codice Typst.

Il modello è quello di Layout/Row/Cell di GenroPy: un inventario di funzionalità, ognuna associata a un oggetto astratto. Esempio: "pagina X di Y" è un elemento dedicato; il suo renderer emette uno snippet `context`.

#### Inventario provvisorio

*Funzionalità e costrutto Typst emesso*

| Funzionalità | Costrutto Typst | Stato |
|---|---|---|
| documento, pagina (formato, orientamento, margini) | `set page(...)` | verificato |
| header/footer ripetuti, prima pagina diversa | `page(header:, footer:)` + `context` | verificato |
| numero pagina X di Y | `counter(page).display()`, `counter(page).final()` in `context` | verificato |
| layout/row/cell elastici | `grid` con colonne `auto`, `1fr`, fisse | verificato |
| paragrafo, stile | `text`, `par`, `set` | da verificare |
| campo formattato dai dati | formattazione in Python, `text` in Typst | da verificare |
| tabella dati con intestazione ripetuta | `table` + `table.header(repeat: true)` | verificato |
| totali, subtotali | `table.footer` | footer ripetuto verificato; riporto tra pagine non verificato |
| tieni insieme, salto pagina | `block(breakable: false)`, `pagebreak()` | compila; effetto non verificato |
| immagine | `image` | da verificare |
| barcode, QR | pacchetto esterno `@preview/tiaoma` | import 0.3.0 compila |
| bordi, riquadri, linee | `box`, `rect`, `line`, `stroke` | da verificare |
| schemi | SVG del dialetto svg di genro-builders, incluso con `image` | da verificare |

#### Grammatica di prova

Base: Layout/Row/Cell di GenroPy (`gnr/core/gnrhtml.py`). Nel legacy ogni elemento ha posizione assoluta in `um` (millimetri) e `width=0`/`height=0` divide lo spazio libero in parti uguali. Qui il layout segue il flusso e può continuare nella pagina successiva.

- Una riga senza `height` prende l'altezza del contenuto (`auto`). `'1fr'` è ammesso solo se il layout ha un'altezza.
- Una larghezza è una lunghezza, una percentuale o una frazione: `'25mm'`, `'30%'`, `'2fr'`, `'auto'`. Un numero è una frazione; `width=0` vale `1fr`, come nel legacy.
- Spariscono `um` e `lbl_height`. `top/left/bottom/right` diventano `inset`.

*Elementi*

| Elemento | Attributi | Costrutto Typst |
|---|---|---|
| `document` | `paper`, `flipped`, `margin` | `set page` |
| `header`, `footer` | `pages='all'|'first'|'others'` | `page(header:, footer:)` + `context` |
| `pageNumber` | `template='Pagina {page} di {total}'` | `counter(page)` in `context` |
| `style` | `name`, `font`, `size`, `weight`, `color`, `align` | parametri di `text`/`par` |
| `layout` | `border_width`, `border_color`, `border_style`, `row_border`, `cell_border`, `lbl_class`, `content_class`, `inset` | `grid` |
| `row` | `height`, `row_border`, `cell_border`, `lbl_class`, `content_class`, `breakable` | riga di `grid` |
| `cell` | `content`, `width`, `lbl`, `lbl_class`, `content_class`, `cell_border`, `align`, `valign`, `background`, `colspan` | `grid.cell` |
| `paragraph` | `content`, `style` | `text` + `par` |
| `field` | `value`, `dtype`, `format`, `style` | formattazione in Python, testo con escape |
| `image` | `src` (anche un `SvgBuilder`), `width`, `height`, `fit` | `image` |
| `barcode` | `value`, `kind='qr'|'ean13'|'code128'` | `tiaoma` |
| `spacer`, `hline`, `pageBreak` | `height` per `spacer` | `v`, `line`, `pagebreak` |
| `table` | `data`, `headerRepeat` | `table` + `table.header(repeat: true)` |
| `column` | `field`, `name`, `width`, `dtype`, `format`, `align`, `totalize`, `subtotal`, `background`, `color` | colonna di `table`; `totalize` produce `table.footer` |

Una `cell` può contenere un `layout` annidato. `colspan` non esiste nel legacy. Gli attributi di `column` vengono dalla grid struct legacy (`gnr/web/gnrbaseclasses.py`); `mm_width` diventa `width`.

I nomi legacy restano: `lbl`, `lbl_class`, `content_class`, `border_width`, `row_border`, `cell_border`, `totalize`. I nomi nuovi sono in camelCase.

#### Vincoli posti dagli editor

1. Tutto è dato. Carte intestate e stampe sono Bag serializzate con TYTX. Ogni attributo della grammatica è un valore che un editor può impostare. Nessun elemento richiede codice Python (nel legacy servivano `calcRowHeight` e `prepareRow`).
2. Testo formattato. Il legacy salvava l'HTML di `ckEditor` per ogni regione. La grammatica di prova non ha ancora un elemento inline per grassetto, corsivo o campo dentro una frase.
3. Campi dei dati. Il legacy usava `$campo` nell'HTML, riempito da `templateReplace`. Qui si usano i puntatori `^` di genro-builders; l'editor offre la scelta dei campi dal modello della tabella.
4. Moduli prestampati. Liste e pagine usano il layout elastico. Un modulo prestampato ha campi in posizioni fisse in mm: serve un elemento di posizione assoluta (`place` con `dx`/`dy` in Typst).
5. Anteprima nel browser. Il renderer Bag → codice Typst è in Python. Il browser compila il codice Typst con typst.ts.

*Tipi di stampa*

| Stampa | Struttura | Legacy |
|---|---|---|
| Lista | `table` + `column` | `TableScriptToHtml` con `gridStruct` |
| Pagina (record) | LRC elastico | `TableScriptToHtml` con `prepareRow` |
| Modulo | posizioni assolute in mm | LRC in mm su prestampato |

#### Carta intestata

#### Come funziona in GenroPy

- `READ` `gnrcore/packages/adm/model/htmltemplate.py` · 2026-10-20 — La carta intestata è un record di `adm.htmltemplate`. La colonna `data` è una Bag: `main.page.{height,width,top,left,right,bottom}` in mm, `main.design` (`headline` o `sidebar`), e per ogni regione una dimensione e un HTML con variabili `$campo`. Il contenuto della stampa va nella regione `center_center`.
- `READ` `gnrcore/packages/adm/model/htmltemplate.py` · 2026-10-20 — `based_on` collega una carta a quella da cui deriva; `letterheadChain` costruisce la catena e ogni carta diventa un livello sovrapposto. `next_letterhead` indica la carta delle pagine dopo la prima (`gnr/core/gnrhtml.py`, `newPage`).
- `READ` `gnrcore/packages/adm/resources/tables/htmltemplate/th_htmltemplate.py` · 2026-10-20 — L'editor legacy ha un form con le misure della pagina, una scheda per `design`, un'anteprima con le regioni ridimensionabili e `ckEditor` sull'HTML della regione selezionata.

#### Proposta

```python
letterhead(name='fattura', paper='a4', flipped=False,
           margin_top='30mm', margin_bottom='20mm',
           margin_left='35mm', margin_right='15mm',
           basedOn='base')
    region(name='top', pages='first', size='30mm')    # contenuto LRC con puntatori ^
    region(name='top', pages='others', size='15mm')
    region(name='left', size='25mm')
    region(name='background')
document(letterhead='fattura')
```

- `top` → `header`; `bottom` → `footer`; `left`, `right`, `background` → `background` con `place`; filigrana → `foreground`.
- `pages='first'|'others'` sostituisce `next_letterhead`: `context` su `counter(page)`.
- `basedOn` sostituisce `based_on`: le regioni con lo stesso `name` e `pages` sostituiscono quelle della base; le regioni `background` si sommano.
- `main.design` sparisce: `headline` e `sidebar` sono una scelta di regioni.
- La carta intestata è una Bag serializzata con TYTX (`Bag.to_tytx`, `Bag.from_tytx`). Il documento la carica e la innesta nel proprio sorgente.

- `RUN` `scratch lh.py` · 2026-10-20 — Typst 0.15.0: header diverso tra la prima pagina e le successive con `context`, banda laterale con `background` + `place`. Entrambi compaiono nel PDF su 2 pagine.
- `RUN` `scratch lh.py` · 2026-10-20 — Typst non allarga il margine superiore per un header più alto: un header di 40 mm con margine di 10 mm si sovrappone al corpo. Il margine di ogni regione va dichiarato come lunghezza.

Una Bag di builder deve ricaricarsi da TYTX con i suoi tag ed essere validata dalla grammatica. Non è verificato.

#### Editor Typst esistenti

- `RUN` `github.com/Myriad-Dreamin/typst.ts` · 2026-10-20 — typst.ts compila Typst nel browser via WASM. Licenza Apache-2.0, release v0.7.0 del 2026-06-01.
- `RUN` `github.com/tyx-editor/TyX` · 2026-10-20 — Gli editor visuali open source per Typst sono giovani: TyX (MIT), typster (MIT), ortic/typst-wysiwyg (MIT, prototipo). TyX lavora su un JSON di TipTap e lo compila in codice Typst: lo stesso schema di questo progetto.

Il renderer produce codice Typst vero. Il percorso è in un solo senso: una modifica fatta al codice Typst non torna nella Bag.

#### Compiti del renderer

- Escape del testo: `#` `*` `_` `$` `@` `<` e gli altri caratteri di markup.
- Conversione dei tipi Python in tipi Typst: lunghezze (`2cm`, `1fr`, `50%`), colori, `none`/`auto`, allineamenti, identificatori distinti dalle stringhe.

#### Binding Python verificato

- `RUN` `venv: pip install typst` · 2026-10-20 — Il pacchetto PyPI `typst` 0.15.0 include Typst 0.15.0 (`sys.version` nel documento stampa 0.15.0).
- `READ` `typst/__init__.pyi` · 2026-10-20 — API pubblica: `compile`, `compile_with_warnings`, `query`, `eval`, `Compiler`, `Fonts`, `FontInfo`, `TypstError`, `TypstWarning`. `compile` accetta il sorgente come bytes, percorso o stringa; formati `pdf`, `svg`, `png`, `html`; parametri `sys_inputs`, `pdf_standards` (anche PDF/A), `timestamp`, `root`. `Compiler` accetta `font_paths`, `ignore_system_fonts`, `package_path`, `package_cache_path`.
- `RUN` `scratch probe.py` · 2026-10-20 — Un documento di 3 pagine con tabella da 120 righe compila senza file: `typst.compile(bytes, format="pdf")`. Prima chiamata 0,62 s; con un `Compiler` già creato 0,014 s.
- `RUN` `scratch probe.py` · 2026-10-20 — `TypstError` espone `message`, `hints`, `trace`.
- **must** — La versione del binding è fissata con `==` in `pyproject.toml`. *(Typst è pre-1.0; la sintassi cambia tra versioni minori.)*

#### Anteprima nel browser

typst.ts (WASM) compila lo stesso sorgente nel browser. Non è verificato.

### Decisions

- **d-carryover** `open` — Il riporto dei totali tra pagine (a riportare / riporto) si fa con codice `context` generato dal renderer, o con un calcolo in Python prima della composizione?
- **d-grammar** `open` — La grammatica riusa i nomi di genro-print (`layout`, `row`, `cell`, `paragraph`, `table`) o ne definisce di propri?
- **d-packages** `open` — I pacchetti Typst esterni (es. `tiaoma`) si scaricano alla prima compilazione o si distribuiscono con il progetto tramite `package_path`?
- **d-fonts** `open` — Si usano i font di sistema o una cartella di font distribuita con il progetto (`ignore_system_fonts=True`) per avere lo stesso PDF su ogni server?
- **d-inline** `open` — Il testo formattato nelle regioni e nelle celle si descrive con elementi inline della grammatica, o il renderer converte il formato dell'editor di testo scelto in gramlot?
- **d-preview** `open` — L'anteprima in gramlot chiede al server il codice Typst, o il renderer viene portato su genro-builders-js per lavorare tutto nel browser?

### Consequences

Le stampe non dipendono più da ReportLab né da un browser headless. Dipendono da una libreria Rust pre-1.0 con versione fissata.
