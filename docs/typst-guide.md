# Guida a Genro Typst

Genro Typst costruisce un albero di documento in Python e produce sorgente Typst.
Il compilatore di riferimento è **Typst 0.15.0**. Il catalogo comprende testo,
struttura, layout, tabelle native, grafica, matematica e costrutti del linguaggio.

La [tabella completa](native-reference.md) è generata dallo stesso catalogo usato
per registrare la grammatica e scegliere le funzioni da emettere. Il
[catalogo JSON](native-catalog.json) è disponibile per strumenti esterni.

## Installazione e primo documento

```bash
python -m pip install -e ".[pdf]"
python examples/03_native_report/report.py
```

```python
from genro_typst import TypstBuilder, length, color

class Report(TypstBuilder):
    def main(self, root):
        doc = root.document(paper="a4", margin="18mm")
        doc.set_rule(target="text", size=length("11pt"), lang="it")
        doc.heading("Relazione", level=1)
        p = doc.par(justify=True)
        p.text("Un paragrafo con ")
        p.strong("testo importante")
        p.text(" e altro testo.")
        doc.rect("Nota", fill=color("#eeeeee"), inset=length("3mm"))

report = Report()
report.create()
report.render(target="report.typ")
report.render(mode="pdf", target="report.pdf")
```

`setup(self, data)` prepara i dati, `main(self, root)` costruisce il documento e
`create()` esegue entrambi. Tutti i normali cicli, funzioni e condizioni Python
restano disponibili. Gli attributi `^percorso` mantengono il binding Genro Bag;
per testi che iniziano letteralmente con `^`, consultare le regole di binding di
`genro-builders` anziché usarli come puntatori involontari.

I metodi nativi accettano `content=...` o una sola prima posizione equivalente.
Ulteriori argomenti posizionali Typst vanno in `args=[...]`. Gli elementi di
linguaggio (`set_rule`, `equation`, `import_module`, ecc.) usano i parametri
nominati della loro firma. Se un nome collide con proprietà di Bag/SourceNode,
il prefisso `typst_` forza la grammatica: `doc.typst_label(name="intro")`. Per le collisioni attuali usare anche
`typst_columns(...)` e `typst_move(...)`.

## Valori: testo, lunghezze, colori ed espressioni

Le stringhe Python sono sempre letterali: `"12pt"` non diventa automaticamente
una lunghezza e `"red"` non diventa un colore. Questo distingue il testo dei dati
dalle espressioni del linguaggio.

| Python | Sorgente Typst |
|---|---|
| `"Testo #non_codice"` | stringa con escaping |
| `True`, `False`, `None` | `true`, `false`, `none` |
| `12`, `1.5` | numero; NaN e infinito sono rifiutati |
| `["a", "b"]` | array `("a", "b",)` |
| `{"left": length("10mm")}` | dizionario con chiavi letterali |
| `length("12pt")` | `12pt` |
| `color("#167665")` | `rgb("#167665")` |
| `label("intro")` | `label("intro")` |
| `expr("center + horizon")` | espressione esplicita |
| `markup("*Titolo*")` | contenuto Typst con markup |

Importare questi helper da `genro_typst`. `length` accetta `mm`, `cm`, `pt`, `in`,
`em`, `%`, `fr` e `auto`. Per angoli, combinazioni di unità, funzioni, simboli,
selettori, gradienti, stroke e valori più complessi usare `expr`, per esempio
`expr('1pt + red')`, `expr('10deg')` o `expr('gradient.linear(red, blue)')`.

Gli helper restituiscono dizionari JSON/TYTX con la chiave riservata `$typst`;
non dipendono da oggetti Python personalizzati e conservano il tipo espressione
quando il documento viene serializzato. Quella chiave non va usata nei normali
dizionari di dati passati come valori Typst. `expr`, `markup`, formule e sorgenti
espliciti sono codice fidato; non usarli per convertire automaticamente testo
non fidato. Per tale testo basta una stringa normale.

I parametri nativi possono essere passati come keyword (`level=2`, `block=True`)
o con `options={...}`. Un underscore diventa un trattino e un underscore finale
può evitare una parola riservata Python. I nomi duplicati dopo questa conversione
sono rifiutati. `options` serve anche per nomi che coincidono con `content`,
`args`, `function` o `mode` del builder.

## Testo e stili

Le funzioni native includono `text`, `heading`, `par`, `strong`, `emph`, `quote`,
`raw`, `underline`, `highlight`, `smallcaps`, `sub`, `super` e le altre elencate
nel riferimento. `raw` mostra codice come testo, con eventuale `lang="python"`:
non lo esegue.

Un contenitore raccoglie `content` iniziale e figli nell'ordine di inserimento.
Aggiungere un figlio non cancella il contenuto iniziale. Tra figli inline non
vengono aggiunti spazi: sono intenzionali nelle stringhe dell'esempio iniziale.

```python
doc.set_rule(target="heading", numbering="1.")
doc.show_rule(selector="heading", target="text", fill=color("navy"))
local = doc.scope()
local.set_rule(target="text", size=length("14pt"))
local.text("Questo stile è locale")
doc.text("Qui torna lo stile precedente")
```

Le regole si applicano ai fratelli successivi nel loro scope. Un `scope()`
crea un blocco di contenuto; `context()` abilita la valutazione contestuale.
Una regola trasformativa usa ad esempio
`show_rule(selector="heading", transform=expr("it => underline(it)"))`.
Non combinare `transform` e `target` nella stessa regola.

## Documento, pagine e impaginazione

`document(paper="a4", flipped=False, margin="15mm")` mantiene il comportamento
storico. `metadata` configura il documento Typst; `page_options` completa o
sovrascrive le impostazioni di pagina iniziali:

```python
doc = root.document(
    metadata={"title": "Bilancio", "author": ["Softwell"], "keywords": ["report"]},
    page_options={
        "margin": {"left": length("20mm"), "right": length("15mm")},
        "header": markup("Bilancio annuale"),
        "footer": expr("context counter(page).display()"),
    },
)
```

`page`, `pagebreak`, `columns`, `colbreak`, `grid`, `stack`, `align`, `block`,
`box`, `pad`, `place`, `move`, `rotate`, `scale`, `skew`, `h` e `v` espongono
l'impaginazione nativa. Esempi:

```python
doc.align(args=[expr("center")]).heading("Centrato", level=2)
doc.typst_columns(args=[2], gutter=length("6mm")).par("Testo su due colonne")
doc.v(length("4mm"))
grid = doc.grid(columns=[length("1fr"), length("2fr")], gutter=length("2mm"))
grid.grid_cell("Sinistra")
grid.grid_cell("Destra")
```

## Tabelle native e tabelle dati

La tabella storica `table(data="^lines")` con figli `column` resta invariata.
`native_table` genera invece la funzione Typst `table`, senza imporre un modello
di righe Python:

```python
table = doc.native_table(columns=[length("1fr"), length("2fr")], inset=length("2mm"))
header = table.table_header(repeat=True)
header.table_cell("Voce")
header.table_cell("Valore")
table.table_cell("Sezione", colspan=2, fill=color("#eeeeee"))
for name, value in [("A", 12), ("B", 24)]:
    table.table_cell(name)
    table.table_cell(str(value))
```

Sono disponibili `table_cell`, `table_header`, `table_footer`, `table_hline`,
`table_vline` e gli equivalenti `grid_*`. `rowspan`, `colspan`, `align`, `fill`,
`stroke` e gli altri parametri nativi vengono inoltrati a Typst. Tipi, combinazioni
e collocazioni non valide sono segnalati dal compilatore.

## Figure, grafica, liste e riferimenti

`image` accetta percorsi di immagini raster o SVG. I file devono esistere sotto
il `root` di compilazione (vedi sotto). `figure` aggiunge didascalie e semantica:

```python
figure = doc.figure(caption=markup("Schema"), alt="Descrizione del disegno")
figure.image("schema.svg", width=length("40mm"))
doc.rect("Riquadro", fill=color("#eeeeee"), stroke=None)
```

`circle`, `ellipse`, `rect`, `square`, `line`, `polygon` e `curve` permettono
forme native. I segmenti `curve_move`, `curve_line`, `curve_quad`, `curve_cubic`
e `curve_close` sono figli/argomenti della curva. Gradienti e tiling sono valori
passabili tramite `expr`; per disegno avanzato si possono importare pacchetti.

`list`/`list_item`, `enum`/`enum_item` e `terms`/`terms_item` producono elenchi.
`terms_item(args=["Termine", "Definizione"])` prende due contenuti. Per link e
riferimenti:

```python
doc.heading("Introduzione", level=1)
doc.typst_label(name="intro")
doc.ref(label("intro"))
doc.link("https://typst.app").text("Typst")
doc.footnote("Una nota a piè di pagina")
doc.outline(title=markup("Indice"))
doc.cite(label("manuale"))
doc.bibliography("references.yml", title=markup("Bibliografia"))
```

Le citazioni richiedono un file bibliografico valido; il formato e gli stili
sono quelli di Typst. Per `ref` verso titoli numerati occorre impostare
`set_rule(target="heading", numbering="1.")`.

## Matematica

```python
doc.equation(formula="sum_(i=1)^n i = (n (n+1))/2", block=True, numbering="(1)")
eq = doc.math_equation(block=True)
eq.math_frac(args=[markup("$a^2$"), markup("$b$")])
eq.math_mat(args=[["1", "2"], ["3", "4"]])
eq.math_vec(args=["x", "y", "z"])
```

`equation` accetta sintassi matematica Typst senza i delimitatori `$` esterni.
Le chiamate strutturate `math_*` usano invece gli argomenti della modalità
**codice**, non il parser della modalità matematica. Le funzioni che vogliono
`content` richiedono stringhe o contenuti espliciti, non automaticamente numeri:
per questo la matrice sopra usa `"1"`, non `1`.

Il catalogo include frazioni, radici, matrici, vettori, casi, attacchi, accenti,
delimitatori, cancellazioni, dimensioni e varianti di carattere. Simboli e
operatori sono accessibili tramite `expr` o la sintassi di `equation`.

## Funzioni avanzate, moduli e codice

```python
doc.import_module(path="helpers.typ", names=["banner"])
doc.call(function="banner", content="Titolo")
doc.let(name="accent", value=color("navy"))
doc.text("Colore condiviso", fill=expr("accent"))
doc.context().text(content=expr("counter(page).display()"))
doc.include(path="appendice.typ")
```

`call(function=..., content=None, args=None, options=None, mode="body", **attrs)`
permette funzioni standard non elencate e funzioni importate. Le modalità sono
quelle del [catalogo](native-reference.md). `native_layout` è l'accesso alla
funzione Typst `layout`, che riceve una callback, mentre `layout` resta il
contenitore Genro a righe e celle.

`import_module(path, names=None, alias=None)` richiede parametri nominati;
`names=["*"]` importa tutti i nomi. Alias e nomi importati devono essere
identificatori semplici (senza punti). I pacchetti usano percorsi Typst versionati,
ad esempio `@preview/...:...`. Risoluzione, cache e disponibilità dei pacchetti
restano responsabilità del compilatore; i test della libreria usano file locali
e non richiedono pacchetti remoti.

`typst_markup(source=...)` inserisce markup completo nel proprio scope.
`typst_code(code=...)` inserisce un blocco di codice, anch'esso locale. Per legare
nomi usati dai fratelli successivi usare `let` o `import_module`, non una
variabile interna a `typst_code`. `expr` può rappresentare callback, selettori,
`query`, `state`, letture dati, simboli e altre espressioni. Questi accessi non
pretendono di validare o reinterpretare l'intero linguaggio Typst in Python.

## Compilazione, serializzazione e diagnostica

```python
from pathlib import Path
from genro_typst.compiler import TypstEngine

result = TypstEngine().compile(report.render(), root=Path("assets"), preview=True)
Path("report.pdf").write_bytes(result.pdf)
# result.svg_pages contiene le pagine SVG; result.pages il numero di pagine.
```

Anche `report.render(mode="pdf", root=Path("assets"))` usa quel filesystem root.
Il builder non è un sandbox di esecuzione per ricette Python. Senza compiler
extra si può comunque generare sorgente e ispezionare la grammatica.

`source.to_tytx()` conserva la struttura e i valori espliciti. La grammatica
completa è esportabile con `TypstBuilder.to_grammar("grammar.json")` secondo il
formato di `genro-builders`; il catalogo sintetico dei metodi è in questa cartella.

## Compatibilità e limiti verificabili

- `document`, `layout`, `row`, `cell`, `table`, `column`, `paragraph` e
  `pageNumber` conservano le firme storiche. `paragraph` e `cell` possono ora
  contenere anche elementi nativi. Il loro comportamento preesistente è testato.
- La libreria ammette tutti i parametri nativi tramite keyword/`options`; non
  replica tutte le firme e tutte le regole di composizione nel validatore Genro.
  Il compilatore verifica nomi, tipi, argomenti richiesti e contesto.
- Tutte le 129 chiamate del catalogo hanno un caso esplicito compilato in PDF
  e SVG, con round trip TYTX, controllo degli errori e confronto SVG con Typst
  scritto direttamente. Sono verificati anche i 12 costrutti di linguaggio e
  gli 8 elementi storici. Vedi [metodo e limiti](verification.md) e gli
  [esempi eseguibili](catalog-examples.md). Non vengono provate tutte le
  combinazioni possibili di parametri né tutti i pacchetti esterni.
- Non è un parser inverso di Typst: sorgente arbitrario non diventa automaticamente
  un albero visuale. L'app separata può offrire controlli visuali differenti per
  elementi storici e nativi; questo non limita l'API Python.
- La grammatica riguarda la generazione di documenti Typst/PDF. Le API HTML,
  bundle e ogni futura aggiunta alla libreria standard non sono dichiarate
  automaticamente coperte da metodi dedicati.

Fonti primarie: [riferimento Typst](https://typst.app/docs/reference/),
[stili](https://typst.app/docs/reference/styling/),
[modello](https://typst.app/docs/reference/model/),
[testo](https://typst.app/docs/reference/text/),
[layout](https://typst.app/docs/reference/layout/),
[grafica](https://typst.app/docs/reference/visualize/) e
[matematica](https://typst.app/docs/reference/math/).
