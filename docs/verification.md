# Verifica del renderer Typst

La verifica si riferisce a **Typst 0.15.0**, la versione fissata nell'extra `pdf`.
Copre tutte le **129 chiamate native registrate**, i **12 costrutti di linguaggio**
e gli **8 elementi storici** del builder. Non significa che ogni combinazione
possibile dei parametri o l'intera libreria standard Typst sia stata provata.

## Contratto verificato

Per ciascuna chiamata nativa, `tests/native_cases.py` contiene un caso esplicito
con parametri validi, il contesto necessario e un riferimento Typst scritto
indipendentemente dal renderer. Il test in `tests/test_catalog_compilation.py`:

1. controlla che i casi corrispondano esattamente al catalogo: un nuovo elemento
   senza esempio fa fallire la suite;
2. costruisce l'albero e ne verifica la grammatica;
3. esegue la ricetta Python pubblicata nella documentazione e verifica che
   produca lo stesso sorgente;
4. salva e ricarica l'albero TYTX, conservando struttura e sorgente;
5. compila il sorgente con `TypstEngine` in PDF e SVG;
6. verifica il numero atteso di pagine, XML e dimensioni degli SVG;
7. confronta **tutte le pagine SVG byte per byte** con il riferimento Typst,
   compilato nello stesso ambiente;
8. prova un parametro inesistente e verifica l'errore del compilatore.

I file Typst di prova sono conservati nella directory temporanea pytest. Se il
confronto fallisce, vengono salvati anche gli SVG effettivi e attesi. Il confronto
è tra due compilazioni della stessa versione, con gli stessi font: non impone
snapshot binari che dipendano dalla macchina o da una versione futura di Typst.
Il PDF viene realmente compilato, ma non viene confrontato byte per byte con
l'SVG né viene verificata automaticamente ogni proprietà del PDF (tagging,
accessibilità, link e metadati).

Gli [esempi del catalogo](catalog-examples.md) riportano ricetta Python e
riferimento Typst completo, inclusi i contenitori richiesti.

## Contesti e comportamenti da rispettare

- `table_footer` e `grid_footer` devono terminare all'ultima riga: le celle del
  corpo vanno aggiunte **prima** del footer. La suite prova anche il caso errato.
- `table_cell`, `grid_cell`, intestazioni e linee vanno usati nel contenitore
  corrispondente; gli elementi `curve_*` dentro `curve`.
- Gli elementi matematici sono provati dentro `math_equation`; in modalità codice
  argomenti come quelli di `math_vec` e `math_mat` sono contenuti/stringhe,
  non numeri Python da visualizzare implicitamente.
- `measure` richiede un contesto Typst e restituisce un dizionario. L'esempio
  usa `context` e `call(function="repr", mode="args")` per visualizzarlo.
- `native_layout` riceve una callback esplicita; `metadata` inserisce dati
  invisibili. `hide` e gli elementi strutturali non producono necessariamente
  contenuto visibile proprio.
- `columns`, `move` e `label` collidono con nomi di SourceBag: usare i prefissi
  `typst_columns`, `typst_move`, `typst_label`. Gli esempi usano il prefisso
  sistematicamente, valido anche per gli altri metodi.

## Linguaggio, dati e regressioni

`tests/test_language_compilation.py` esercita tutti i costrutti di linguaggio con
PDF/SVG e round trip, le cinque modalità di `call`, import locali per nome,
wildcard e alias, valori letterali confrontati con il parser JSON di Typst,
errori attesi e un documento che combina tutti gli elementi storici con dati
Bag ed elementi nativi. I test preesistenti coprono anche tabelle su più pagine,
totali, ereditarietà di stili, riferimenti, regole locali e binding dinamici.

Difetti corretti durante la verifica:

- `markup("... // commento")` conserva ora il delimitatore di chiusura grazie
  a una nuova riga finale, come già faceva `typst_markup`.
- `options` e `args` distinguono `None` dai valori vuoti di tipo errato: liste
  passate come `options`, dizionari passati come `args`, booleani e stringhe non
  vengono più ignorati silenziosamente. Gli errori sono `TypeError`.
- Alias e nomi importati devono essere identificatori semplici; percorsi puntati
  vengono rifiutati con `ValueError`. I percorsi puntati restano validi per
  chiamare funzioni, ad esempio `call(function="helper.greeting", ...)`.

I tre elementi `dataSetter`, `dataFormula` e `dataController` ereditati da
`genro-builders` riguardano il runtime dei dati: non sono chiamate Typst e non
sono contati tra i 149 elementi documentali sopra indicati.

## Riprodurre la verifica

Dalla radice del repository, con l'ambiente di sviluppo installato:

```bash
venv/bin/pytest -q
venv/bin/ruff check src tests tools
venv/bin/mypy
venv/bin/python tools/generate_reference.py --check
```

Per una singola chiamata:

```bash
venv/bin/pytest -q tests/test_catalog_compilation.py -k table_footer
```

Per rigenerare riferimento ed esempi:

```bash
venv/bin/python tools/generate_reference.py
```

Restano fuori da questa verifica esaustiva del catalogo: tutte le combinazioni
di parametri, i pacchetti remoti, i font esterni non installati, altri sistemi
operativi/versioni del compilatore e i target Typst diversi da PDF/SVG. Il
validatore Python non replica il sistema di tipi del compilatore: molti errori
su parametri nativi sono intenzionalmente diagnosticati da Typst.
