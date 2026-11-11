#!/usr/bin/env python3
"""Paczka do dzielenia się systemem między projektami: dist/panel-piksel-<wersja>.zip

Uruchom z katalogu projektu:  python3 tools/build_zip.py
Zawartość (ścieżki w przykładach i dokumentach przepisane tak, żeby działały po rozpakowaniu):
  README.md, design.md, VERSION
  panel-piksel/      — CSS, JS, ikony (SVG), tokens.json, components.json, starter.html
  examples/          — katalog komponentów, wzorce, ikony
  docs/              — dokumentacja dla designerów (v2, jeden plik), decyzje, kwestie otwarte, zrzuty
  skill/panel-piksel-ui/ — skill dla Claude Code (skopiuj do ~/.claude/skills/)
"""
import os
import re
import zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SK = os.path.join(ROOT, 'skills', 'panel-piksel-ui')
VERSION = open(os.path.join(SK, 'VERSION')).read().strip()
BASE = f'panel-piksel-{VERSION}'
OUT = os.path.join(ROOT, 'dist', BASE + '.zip')

README = f'''# Panel & Piksel {VERSION}

Retro-pikselowy design system dla katalogów, list ofert, tabel, rankingów i sklepów: białe panele z czarną ramką 2 px
i twardym cieniem, gęste numerowane listy, czytelne Archivo, piksel (Press Start 2P, ikony 12×12) tam, gdzie się patrzy,
a nie czyta. Paleta SNES (Jehkoba32) z akcentami NES, tryb jasny, ciemny i wysokiego kontrastu.

Właściciel systemu: Konrad Kosiorek. Źródło prawdy: `design.md`.

## Co jest w paczce

| Katalog / plik | Do czego |
|---|---|
| `design.md` | Pełna specyfikacja: zarządzanie (§0), zasady, tokeny, komponenty i wzorce (§6), treści (§6A), dostępność (§8), kod (§9), historia zmian (§12) |
| `panel-piksel/` | Kod systemu — kopiujesz do projektu bez zmian |
| `panel-piksel/tokens.css`, `components.css`, `icons.css` | Style (tokeny, komponenty, ikony) |
| `panel-piksel/list-controls.js`, `table-sort.js`, `ui-controls.js`, `charts.js` | Zachowanie: listy i filtry, sortowanie tabel, formularze i nakładki, wykresy — bez zależności |
| `panel-piksel/tokens.json` | Tokeny w formacie W3C Design Tokens (Tokens Studio dla Figmy, Style Dictionary) |
| `panel-piksel/components.json` | Rejestr komponentów ze statusami (stabilny / testowy / wycofywany) |
| `panel-piksel/icons/` | Ikony jako pojedyncze pliki SVG |
| `panel-piksel/starter.html` | Szablon nowej strony |
| `examples/` | Działające przykłady: wszystkie komponenty i stany, wzorce, galeria ikon — otwórz w przeglądarce |
| `docs/panel-piksel-komponenty-v2.html` | Dokumentacja dla designerów: 29 kart rodzin (jeden plik, działa offline) |
| `skill/panel-piksel-ui/` | Skill dla Claude Code: agent buduje ekrany z tych klocków i sprawdza je skryptami |

## Szybki start (HTML)

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400&family=Press+Start+2P&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./panel-piksel/tokens.css">
<link rel="stylesheet" href="./panel-piksel/components.css">
<link rel="stylesheet" href="./panel-piksel/icons.css">
<!-- skrypty tylko gdy ekran ich potrzebuje -->
<script src="./panel-piksel/list-controls.js" defer></script>
<script src="./panel-piksel/table-sort.js" defer></script>
<script src="./panel-piksel/ui-controls.js" defer></script>
<script src="./panel-piksel/charts.js" defer></script>
```

Tryb ciemny: `<html data-theme="dark">` albo `data-theme="auto"` (wg ustawień systemu).
Zasady, których pilnujemy: ramka 2 px, tylko twarde cienie 2/4/6 px, jeden kolor akcji, jeden „głośny” element na ekran,
pixel-font tylko dla liczb i krótkich etykiet, stany nie zmieniają rozmiaru, wszystko co wygląda na klikalne — działa.

## Z agentem AI (Claude Code)

```bash
cp -r skill/panel-piksel-ui ~/.claude/skills/
```

Potem poproś np. „zbuduj ekran listy ofert w stylu Panel & Piksel”. Skill ma przepisy ekranów, kontrolę zasad
(`scripts/check_screen.py`), render w 1280/390 px z testem klikania (`scripts/render_check.py`), test wizualny
(`scripts/visual_regression.py`) i synchronizację kopii (`scripts/sync_system.py`).

## Wersje i zmiany

Semver w `VERSION`: poprawka (1.11.x) · nowy element lub wycofanie (1.x) · usunięcie wycofanego elementu (x.0).
Wycofane elementy działają do następnej wersji głównej, a `check_screen.py` podaje zamiennik. Nowe komponenty zgłaszaj
według `design.md` §0.5 — decyduje właściciel systemu.

## Licencja

Do ustalenia przez właściciela systemu. Fonty: Archivo i Press Start 2P — SIL Open Font License (Google Fonts).
'''


def add_tree(z, src, dst, rewrite=None, skip=()):
    for base, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ('__pycache__',)]
        for f in sorted(files):
            if f in skip or f.startswith('.'):
                continue
            p = os.path.join(base, f)
            arc = os.path.join(dst, os.path.relpath(p, src))
            if rewrite and f.endswith('.html'):
                z.writestr(arc, rewrite(open(p, encoding='utf-8').read()))
            else:
                z.write(p, arc)


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(f'{BASE}/README.md', README)
        z.write(os.path.join(ROOT, 'design.md'), f'{BASE}/design.md')
        z.write(os.path.join(SK, 'VERSION'), f'{BASE}/VERSION')
        add_tree(z, os.path.join(SK, 'assets'), f'{BASE}/panel-piksel')
        # przykłady: ../assets/ → ../panel-piksel/
        add_tree(z, os.path.join(SK, 'examples'), f'{BASE}/examples', rewrite=lambda h: h.replace('../assets/', '../panel-piksel/'))
        # dokumentacja: ../skills/panel-piksel-ui/assets/ → ../panel-piksel/; tylko wersja v2 i strony decyzji
        fix_docs = lambda h: h.replace('../skills/panel-piksel-ui/assets/', '../panel-piksel/').replace('../skills/panel-piksel-ui/examples/', '../examples/')
        for f in sorted(os.listdir(os.path.join(ROOT, 'docs', 'kandydaci'))):
            z.write(os.path.join(ROOT, 'docs', 'kandydaci', f), f'{BASE}/docs/kandydaci/{f}')
        for f in ('panel-piksel-komponenty-v2.html', 'decyzje-v1-1.html', 'kwestie-otwarte.html', 'kandydaci.html'):
            z.writestr(f'{BASE}/docs/{f}', fix_docs(open(os.path.join(ROOT, 'docs', f), encoding='utf-8').read()))
        for f in sorted(os.listdir(os.path.join(ROOT, 'docs', 'evidence'))):
            if f.endswith('.png') and not f.endswith('.diff.png'):
                z.write(os.path.join(ROOT, 'docs', 'evidence', f), f'{BASE}/docs/evidence/{f}')
        add_tree(z, SK, f'{BASE}/skill/panel-piksel-ui')
    print(f'{OUT} · {os.path.getsize(OUT) / 1e6:.1f} MB')


if __name__ == '__main__':
    main()
