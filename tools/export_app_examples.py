#!/usr/bin/env python3
"""Export the verified Typst examples as a self-contained app resource.

The application ships the resulting JSON and has no runtime dependency on
this checkout, its tests, or pytest. Re-run when the catalog changes.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

from genro_typst.native_catalog import NATIVE, SPECIAL

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from native_cases import CASES, build_case, example_python

SECTIONS = {
    "text": "Testo e stili",
    "model": "Struttura del documento",
    "layout": "Impaginazione",
    "visualize": "Grafica e immagini",
    "math": "Matematica",
    "introspection": "Metadati",
    "pdf": "PDF",
    "language": "Linguaggio Typst",
    "legacy": "Documenti e dati Genro",
}
DESCRIPTIONS = {
    "text": "Testo e parametri tipografici.",
    "underline": "Sottolineatura del testo.",
    "overline": "Linea sopra il testo.",
    "strike": "Testo barrato.",
    "highlight": "Evidenziatore sul testo.",
    "smallcaps": "Maiuscoletto.",
    "sub": "Pedice nel testo.",
    "super": "Apice nel testo.",
    "lower": "Conversione in minuscolo.",
    "upper": "Conversione in maiuscolo.",
    "raw": "Codice e testo letterale, senza interpretare il markup.",
    "lorem": "Testo segnaposto con numero di parole modificabile.",
    "linebreak": "Interruzione della riga.",
    "smartquote": "Virgolette tipografiche.",
    "heading": "Titoli e livelli delle sezioni.",
    "strong": "Grassetto.",
    "emph": "Enfasi tipografica.",
    "par": "Paragrafo e composizione del testo.",
    "quote": "Citazione nel documento.",
    "figure": "Figura con didascalia e numerazione.",
    "footnote": "Nota a piè di pagina.",
    "title": "Titolo del documento.",
    "list": "Elenco puntato.",
    "enum": "Elenco numerato.",
    "terms": "Glossario di termini e definizioni.",
    "list_item": "Elemento di un elenco puntato.",
    "enum_item": "Elemento di un elenco numerato.",
    "terms_item": "Termine e relativa definizione.",
    "link": "Collegamento con testo modificabile.",
    "ref": "Riferimento a una sezione etichettata.",
    "cite": "Citazione da una bibliografia locale inclusa.",
    "bibliography": "Bibliografia con file YAML incluso.",
    "numbering": "Formato di numerazione.",
    "outline": "Indice delle sezioni.",
    "parbreak": "Separazione tra paragrafi.",
    "divider": "Separatore del documento.",
    "native_table": "Tabella nativa Typst con celle esplicite.",
    "align": "Allineamento del contenuto.",
    "block": "Blocco con spaziatura interna.",
    "box": "Riquadro in linea di larghezza definita.",
    "columns": "Testo su più colonne.",
    "hide": "Contenuto invisibile che conserva lo spazio.",
    "move": "Spostamento del contenuto.",
    "pad": "Spaziatura interna.",
    "page": "Pagina con un formato diverso.",
    "place": "Posizionamento rispetto alla pagina.",
    "repeat": "Ripetizione di un contenuto.",
    "rotate": "Rotazione.",
    "scale": "Ridimensionamento.",
    "skew": "Inclinazione.",
    "grid": "Griglia di contenuti.",
    "stack": "Sequenza di blocchi con direzione e distanza.",
    "pagebreak": "Interruzione di pagina: osserva le due pagine nell’anteprima.",
    "colbreak": "Interruzione di colonna dentro un contenitore a colonne.",
    "h": "Spazio orizzontale.",
    "v": "Spazio verticale.",
    "measure": "Misurazione contestuale del contenuto; il risultato è un dizionario.",
    "native_layout": "Callback che riceve le dimensioni disponibili.",
    "circle": "Cerchio con contenuto.",
    "ellipse": "Ellisse con contenuto.",
    "rect": "Rettangolo con riempimento.",
    "square": "Quadrato con contenuto.",
    "image": "Immagine SVG locale già inclusa.",
    "line": "Linea tra due punti.",
    "polygon": "Poligono con vertici e riempimento.",
    "curve": "Curva costruita con segmenti.",
    "metadata": "Dati non visibili inseriti nel documento.",
    "pdf_artifact": "Contenuto decorativo marcato come artefatto nel PDF.",
}
for family in ("table", "grid"):
    for part, meaning in {
        "header": "Intestazione",
        "footer": "Piè di tabella, dopo le celle del corpo",
        "cell": "Cella estesa su più colonne",
        "hline": "Linea orizzontale",
        "vline": "Linea verticale",
    }.items():
        DESCRIPTIONS[f"{family}_{part}"] = (
            f"{meaning} nella {'tabella' if family == 'table' else 'griglia'} nativa."
        )
for name, meaning in {
    "move": "Sposta il punto iniziale",
    "line": "Segmento rettilineo",
    "quad": "Curva quadratica",
    "cubic": "Curva cubica",
    "close": "Chiude il percorso",
}.items():
    DESCRIPTIONS[f"curve_{name}"] = meaning + " all’interno di curve."

LANGUAGE = {
    "call": (
        "Chiamata a una funzione Typst o importata.",
        'doc.call(function="strong", content="Funzione personalizzabile")',
    ),
    "set_rule": (
        "Regola di stile per gli elementi successivi.",
        'doc.set_rule(target="text", fill=color("blue"))\ndoc.text("Questo testo è blu")',
    ),
    "show_rule": (
        "Trasformazione o stile degli elementi selezionati.",
        'doc.show_rule(selector="heading", target="text", fill=color("blue"))\ndoc.heading("Titolo trasformato")',
    ),
    "scope": (
        "Stili locali a un contenitore.",
        'scope = doc.scope()\nscope.set_rule(target="text", fill=color("blue"))\nscope.text("Stile locale")\ndoc.text("Stile esterno")',
    ),
    "context": (
        "Valori che richiedono il contesto della pagina.",
        'doc.context().text(content=expr("counter(page).display()"))',
    ),
    "equation": (
        "Formula scritta con la sintassi matematica Typst.",
        'doc.equation(formula="sum_(i=1)^n i = (n (n+1))/2", numbering="(1)")',
    ),
    "label": (
        "Etichetta e riferimento a una sezione.",
        'doc.set_rule(target="heading", numbering="1.")\ndoc.heading("Sezione di esempio")\ndoc.typst_label(name="example")\ndoc.ref(label("example"))',
    ),
    "let": (
        "Variabile Typst usata dagli elementi successivi.",
        'doc.let(name="message", value="Ciao da una variabile Typst")\ndoc.text(content=expr("message"))',
    ),
    "import_module": (
        "Import di una funzione da helper.typ, incluso nell’esempio.",
        'doc.import_module(path="helper.typ", names=["greeting"])\ndoc.call(function="greeting", args=["Lettore"], mode="value")',
    ),
    "include": (
        "Inclusione di extra.typ, già disponibile nell’esempio.",
        'doc.include(path="extra.typ")',
    ),
    "typst_code": (
        "Blocco di codice Typst con variabili locali.",
        "doc.typst_code(code='let name = \"Lettore\"; [Ciao #name]')",
    ),
    "typst_markup": (
        "Markup Typst all’interno della ricetta Python.",
        'doc.typst_markup(source="*Grassetto*, _enfasi_ e $x^2$. // commento finale")',
    ),
}
LEGACY = {
    "document": (
        "Impostazioni di pagina e metadati del documento.",
        'doc = root.document(paper="a5", margin="12mm", metadata={"title": "Esempio documento"})\ndoc.paragraph(content="Modifica formato e margini della pagina.")',
    ),
    "layout": (
        "Contenitore Genro a righe e celle.",
        'doc = root.document()\nlayout = doc.layout(border_width="0.5pt")\nfor name in ("Prima riga", "Seconda riga"):\n    row = layout.row()\n    row.cell(content=name)\n    row.cell(content="Valore", width="40mm")',
    ),
    "row": (
        "Righe con altezza e bordi configurabili.",
        'doc = root.document()\nlayout = doc.layout(border_width="0.5pt")\nlayout.row(height="18mm").cell(content="Riga alta 18 mm")\nlayout.row().cell(content="Altezza automatica")',
    ),
    "cell": (
        "Celle con etichetta, larghezza e contenuti nativi.",
        'doc = root.document()\nrow = doc.layout(border_width="0.5pt").row()\nrow.cell(content="Cliente", lbl="Anagrafica", width=2)\nrow.cell(lbl="Contenuto nativo", background="#eeeeee").strong("Grassetto")',
    ),
    "paragraph": (
        "Paragrafo Genro con binding ai dati.",
        'doc = root.document()\ndoc.paragraph(content="^customer.name")\ndoc.paragraph().strong("Contenuto nativo nel paragrafo")',
    ),
    "pageNumber": (
        "Numero della pagina e totale, aggiornati in automatico.",
        'doc = root.document()\nfor index in range(2):\n    if index:\n        doc.pagebreak()\n    doc.paragraph(content=f"Pagina di prova {index + 1}")\n    doc.pageNumber(template="Pagina {page} di {total}")',
    ),
    "table": (
        "Tabella dai dati Bag, con intestazioni e totali.",
        'doc = root.document()\ntable = doc.table(data="^lines", totalize_footer="Totale")\ntable.column(field="description", name="Descrizione", width=3)\ntable.column(field="quantity", name="Quantità", totalize=True)\ntable.column(field="amount", name="Importo", totalize=True)',
    ),
    "column": (
        "Colonne della tabella dati: larghezza, allineamento e totale.",
        'doc = root.document()\ntable = doc.table(data="^lines", totalize_footer="Totale")\ntable.column(field="description", name="Descrizione", width="80mm")\ntable.column(field="quantity", name="Quantità", align="right")\ntable.column(field="amount", name="Importo", align="right", totalize=True)',
    ),
}
ASSETS = {
    "logo.svg": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><circle cx="10" cy="10" r="8" fill="blue"/></svg>',
    "refs.yml": "manual:\n  type: Book\n  title: Test manual\n  author: Example, Alice\n  date: 2026\n",
    "helper.typ": "#let greeting(name) = [Ciao #name]",
    "extra.typ": "= Contenuto incluso\nQuesto testo proviene da extra.typ.\n",
}


def recipe(body: str, description: str, setup: str = "") -> str:
    imports = "from genro_typst import TypstBuilder, expr, length, color, label, markup\nfrom genro_bag import Bag\n"
    code = imports + "\n\nclass Document(TypstBuilder):\n"
    if setup:
        code += "    def setup(self, data):\n" + textwrap.indent(setup, "        ") + "\n\n"
    code += "    def main(self, root):\n"
    code += (
        textwrap.indent(
            "# "
            + description
            + "\n# Modifica la ricetta: l’anteprima si aggiorna automaticamente.\n"
            + body,
            "        ",
        )
        + "\n"
    )
    return code


def catalog() -> dict:
    entries = []
    for tag, (function, _mode, section) in NATIVE.items():
        case = CASES[tag]
        builder, _, reference = build_case(case)
        body = (
            example_python(builder)
            .split("builder = TypstBuilder()\n", 1)[1]
            .rsplit("\n\nsource = builder.render()", 1)[0]
            .replace("builder.source", "root")
        )
        description = DESCRIPTIONS.get(tag, f"Funzione matematica {function}, dentro un’equazione.")
        files = {"image": ["logo.svg"], "cite": ["refs.yml"], "bibliography": ["refs.yml"]}.get(
            tag, []
        )
        entries.append(
            {
                "id": tag,
                "title": function,
                "section": section,
                "description": description,
                "code": recipe(body, description),
                "reference": reference,
                "assets": {name: ASSETS[name] for name in files},
            }
        )
    assert set(LANGUAGE) == set(SPECIAL)
    for tag, (description, body) in LANGUAGE.items():
        files = {"import_module": ["helper.typ"], "include": ["extra.typ"]}.get(tag, [])
        entries.append(
            {
                "id": tag,
                "title": tag,
                "section": "language",
                "description": description,
                "code": recipe("doc = root.document()\n" + body, description),
                "reference": "",
                "assets": {name: ASSETS[name] for name in files},
            }
        )
    setup = """data["customer.name"] = "Rossi & Figli"
lines = Bag()
for index, (description, quantity, amount) in enumerate([
    ("Analisi", 2, 240), ("Template", 3, 150),
]):
    row = Bag()
    row["description"] = description
    row["quantity"] = quantity
    row["amount"] = amount
    lines[f"r{index}"] = row
data["lines"] = lines"""
    for tag, (description, body) in LEGACY.items():
        entries.append(
            {
                "id": tag,
                "title": tag,
                "section": "legacy",
                "description": description,
                "code": recipe(
                    body, description, setup if tag in ("table", "column", "paragraph") else ""
                ),
                "reference": "",
                "assets": {},
            }
        )
    return {"typst_version": "0.15.0", "sections": SECTIONS, "examples": entries}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    exported = catalog()
    content = json.dumps(exported, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != content:
            raise SystemExit("The app catalog is out of date: regenerate it with this tool.")
        print(f"Verified {len(exported['examples'])} packaged examples.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
        print(f"Exported {len(exported['examples'])} examples to {args.output}")
