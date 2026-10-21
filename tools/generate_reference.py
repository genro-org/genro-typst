#!/usr/bin/env python3
"""Regenerate the native API reference and machine-readable catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from genro_typst.native_catalog import NATIVE, SPECIAL

ROOT = Path(__file__).resolve().parents[1]


def reference() -> tuple[str, str]:
    lines = [
        "# Riferimento degli elementi nativi",
        "",
        "Generato da `native_catalog.py` con `tools/generate_reference.py`. Non modificare a mano.",
        "",
        f"**{len(NATIVE)} chiamate native**, verificate su Typst **0.15.0**, oltre ai costrutti",
        "di linguaggio elencati sotto e agli otto elementi storici per documenti commerciali.",
        "",
        "Per i tipi dei parametri e i relativi valori predefiniti, seguire i collegamenti",
        "alla documentazione ufficiale. Le pagine online possono descrivere versioni più",
        "recenti: il riferimento eseguibile di questo progetto resta Typst 0.15.0.",
        "",
        "## Firma comune",
        "",
        "```python",
        "node.heading(content=None, args=None, options=None, **parametri_typst)",
        "```",
        "",
        "`content` accetta anche la prima posizione (`node.heading('Titolo')`).",
        "`args` è una lista di argomenti posizionali Typst; `options` permette nomi che",
        "collidono con quelli del builder. I parametri aggiuntivi sono inoltrati a Typst:",
        "i loro nomi e tipi vengono verificati dal compilatore, non tutti dallo schema Python.",
        "",
        "| Modalità | Significato |",
        "|---|---|",
        "| `body` | Testo iniziale e figli formano un unico contenuto; nessuno spazio implicito tra figli. |",
        "| `items` | Ogni figlio diventa un argomento distinto, ad esempio una cella. |",
        "| `args` | Argomenti e figli sono passati separatamente; segue i tipi della funzione. |",
        "| `value` | Il contenuto iniziale è un valore posizionale, ad esempio URL o percorso; i figli formano un eventuale corpo. |",
        "| `leaf` | Senza contenuto/figli; restano disponibili `args` e parametri nominati. |",
        "",
        "Le stringhe restano stringhe. Usare `length`, `color`, `label`, `expr` e `markup`",
        "per valori Typst non testuali. I metodi con underscore corrispondono ai percorsi",
        "puntati di Typst (`table_cell` → `table.cell`); gli underscore nei parametri",
        "diventano trattini (`column_gutter` → `column-gutter`).",
        "",
    ]
    entries = []
    for section in dict.fromkeys(section for _, _, section in NATIVE.values()):
        url = f"https://typst.app/docs/reference/{'pdf' if section == 'pdf' else section}/"
        lines += [
            f"## {section}",
            "",
            f"[Riferimento ufficiale]({url})",
            "",
            "| Metodo builder (esempio verificato) | Funzione Typst | Modalità |",
            "|---|---|---|",
        ]
        for tag, (function, mode, group) in NATIVE.items():
            if group != section:
                continue
            lines.append(f"| [`{tag}`](catalog-examples.md#{tag}) | `{function}` | `{mode}` |")
            entries.append({"tag": tag, "function": function, "mode": mode, "section": group})
        lines += [""]
    lines += [
        "## Costrutti del linguaggio",
        "",
        ", ".join(f"`{s}`" for s in SPECIAL),
        "",
        "Firme, esempi e limiti sono descritti nella [guida](typst-guide.md).",
        "",
    ]
    catalog = {
        "typst_version": "0.15.0",
        "native_elements": entries,
        "language_elements": list(SPECIAL),
    }
    return "\n".join(lines), json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def examples() -> str:
    # Development-only fixtures: no test dependency is imported by the package.
    sys.path.insert(0, str(ROOT / "tests"))
    from native_cases import CASES, build_case, example_python

    if set(CASES) != set(NATIVE):
        raise ValueError("Every catalog entry needs an explicit executable example")
    lines = [
        "# Esempi verificati del catalogo",
        "",
        "Generato da `tests/native_cases.py` con `tools/generate_reference.py`.",
        "Ogni ricetta è eseguita nei test; il sorgente prodotto compila in PDF e SVG",
        "con Typst 0.15.0. Gli SVG coincidono con quelli del riferimento Typst",
        "scritto direttamente, nel medesimo contesto. Vedi [verifica](verification.md).",
        "",
        "Le ricette sono autonome, salvo i file locali indicati qui sotto. Per compilare:",
        "",
        "```python",
        "from pathlib import Path",
        "from genro_typst.compiler import TypstEngine",
        'result = TypstEngine().compile(source, root=Path("assets"), preview=True)',
        'Path("example.pdf").write_bytes(result.pdf)',
        "```",
        "",
        "Creare la cartella `assets`. `image` richiede `assets/logo.svg`:",
        "",
        "```xml",
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">',
        '  <circle cx="10" cy="10" r="8" fill="blue"/>',
        "</svg>",
        "```",
        "",
        "`cite` e `bibliography` richiedono `assets/refs.yml`:",
        "",
        "```yaml",
        "manual:",
        "  type: Book",
        "  title: Test manual",
        "  author: Example, Alice",
        "  date: 2026",
        "```",
        "",
        "I prefissi `typst_` evitano collisioni con metodi/proprietà di SourceBag.",
        "`expr` rende espliciti i valori Typst; i dizionari e le liste restano dati Python.",
        "",
    ]
    for tag in NATIVE:
        case = CASES[tag]
        builder, _, reference = build_case(case)
        lines += [
            f"## {tag}",
            "",
            f"Contesto del caso: `{case.context}`.",
            "",
            "```python",
            example_python(builder),
            "```",
            "",
            "Riferimento Typst indipendente:",
            "",
            "```typst",
            reference.rstrip(),
            "```",
            "",
        ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    check = parser.parse_args().check
    markdown, catalog = reference()
    for name, content in [
        ("native-reference.md", markdown),
        ("native-catalog.json", catalog),
        ("catalog-examples.md", examples()),
    ]:
        path = ROOT / "docs" / name
        if check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"Regenerate {path} with tools/generate_reference.py")
        else:
            path.write_text(content)


if __name__ == "__main__":
    main()
