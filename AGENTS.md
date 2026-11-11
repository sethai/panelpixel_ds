# Instrukcje dla agentów — repozytorium Panel & Piksel

Repozytorium zawiera design system **Panel & Piksel** (specyfikacja, kod CSS/JS, skill dla agentów, dokumentację, stronę dla Cloudflare). Opis dla ludzi: [README.md](README.md). Pisz po polsku (treści, komunikaty, commity), chyba że użytkownik pisze inaczej.

## Źródła prawdy — edytuj tylko te pliki

| Co zmieniasz | Gdzie |
|---|---|
| zasady, specyfikacje, decyzje, historia zmian | `design.md` (poza sekcjami generowanymi — niżej) |
| kod systemu: tokeny, komponenty, ikony, skrypty, szablon | `skills/panel-piksel-ui/assets/` (`tokens.css`, `components.css`, `icons.css`, `*.js`, `starter.html`) |
| ikony | `skills/panel-piksel-ui/scripts/build_icons.py` (generuje `icons.css`, `assets/icons/*.svg`, `examples/ikony.html`) |
| rejestr komponentów (status, wersja „od”, brakujące testy, wycofania) | `skills/panel-piksel-ui/assets/components.json` |
| wersja | `skills/panel-piksel-ui/VERSION` + pole `version` w `components.json` |
| skill (instrukcje dla agenta budującego ekrany) | `skills/panel-piksel-ui/SKILL.md`, `references/screen-recipes.md`, `scripts/` |
| przykłady na żywo | `skills/panel-piksel-ui/examples/komponenty.html`, `wzorce.html` |
| karty dokumentacji dla designerów | `tools/doc_cards.py`, `tools/docgen.py` (aneks, kwestie, mapa kart → rejestr `STATUS_OF`) |
| strona dokumentacji | `tools/build_site.py` |
| paczka do dzielenia się | `tools/build_zip.py` |
| ekran przykładowy (landing) | `screens/landing/index.html` |

## Pliki generowane — nie edytuj ręcznie (nadpisze je build)

- `design.md`: tabela rejestru między `<!-- pp:registry -->` a `<!-- /pp:registry -->`, kod w §9.1/§9.2 i numer wersji w nagłówku.
- `skills/panel-piksel-ui/references/design-system.md` (kopia `design.md`), `skills/panel-piksel-ui/assets/tokens.json`.
- `screens/landing/panel-piksel/*`, `screens/landing/landing-portal-pracy.html`, wklejone bloki `<style id="pp-…">` w `skills/panel-piksel-ui-workspace/iteration-1/**`.
- `docs/panel-piksel-komponenty-v2.html`, cały katalog `site/`, cały katalog `dist/` (poza repozytorium).

## Budowanie

```bash
python3 tools/build_all.py          # pełna odbudowa
python3 tools/build_all.py --check  # czy kopie są zgodne ze źródłem (bez zapisu)
```

Kolejność w środku (gdy potrzebujesz pojedynczego kroku): `skills/panel-piksel-ui/scripts/sync_system.py` → `tools/docgen.py` → `tools/build_zip.py` → `tools/build_site.py` → ZIP katalogu `site/`.

Wyniki:
- `dist/panel-piksel-<wersja>.zip` — paczka do dzielenia się (README, `design.md`, `panel-piksel/`, przykłady, dokumentacja, skill).
- `dist/panel-piksel-site-<wersja>.zip` — strona do wgrania w Cloudflare Pages (Upload assets).
- `site/` — ta sama strona; jest w repozytorium, żeby Cloudflare Pages mógł publikować z Gita (Build command: puste, output: `site`). **Po każdej zmianie systemu odbuduj i commituj `site/` razem ze źródłami.**

Uwaga: `sync_system.py` synchronizuje też skill zainstalowany w `~/.claude/skills/panel-piksel-ui` (`rsync --delete`), jeśli ten katalog istnieje — ścieżka w `panel-piksel.config.json` (`installed`). Na cudzej maszynie usuń to pole, jeśli nie chcesz nadpisywać lokalnego skilla.

Uruchamiaj wszystko z katalogu głównego repozytorium (skrypty czytają `panel-piksel.config.json` z bieżącego katalogu).

## Testy — zanim powiesz, że gotowe

```bash
python3 skills/panel-piksel-ui/scripts/check_screen.py <plik.html>          # zasady systemu, wycofywane wzorce (ERROR = do poprawy)
python3 skills/panel-piksel-ui/scripts/render_check.py <plik.html> <katalog> # 1280 i 390 px, fonty, klika kontrolki (MARTWA = do poprawy)
python3 skills/panel-piksel-ui/scripts/visual_regression.py tests/visual skills/panel-piksel-ui/examples/*.html
```

- Po zmianie CSS uruchom test wizualny. Różnica jest spodziewana tylko tam, gdzie zmieniałeś; **obejrzyj zrzuty** (jasny/ciemny, 1280/390) i dopiero wtedy zatwierdź nowe wzorce: dopisz `--update` dla tej jednej strony. Nigdy nie aktualizuj wzorców „na ślepo”.
- Wzorce w `tests/visual/` zależą od wersji Chrome i maszyny — po zmianie Chrome zatwierdź je ponownie po obejrzeniu różnic.
- Testy renderu wymagają Google Chrome w `/Applications`. Jeśli go nie ma, napisz wprost, że renderu nie sprawdziłeś.

## Jak zmieniać system

1. **Nowy element / kandydat.** Najpierw jako `draft` w `components.json` (kandydat, design.md §0.5). Do systemu wchodzi dopiero po decyzji właściciela (Konrad Kosiorek) — nie dopisuj go do `components.css` na własną rękę. Pokaż porównanie (np. strona w `docs/` jak `docs/kandydaci.html`).
2. **Po decyzji:** styl w `components.css` (blok z komentarzem wersji i przykładowym HTML), wpis w `components.json` (`preview`, `since`, `docs`, `example`, `missing`), specyfikacja w `design.md` §6, przykład w `examples/komponenty.html`, ściąga w `SKILL.md` i przepis w `screen-recipes.md`, ewentualnie reguła w `scripts/check_screen.py`, wiersze w `tools/docgen.py` (aneks/kwestie/`STATUS_OF`).
3. **Wersja (semver):** poprawka → `1.x.Y`; nowy element lub wycofanie → `1.X.0`; usunięcie wycofanego → `X.0.0`. Zmień `VERSION` i `components.json` → `version`, dopisz wiersz w `design.md` §12 (Historia zmian), zaktualizuj odwołania „v1.x” w nagłówku `components.css` i w `SKILL.md`.
4. **Wycofanie:** status `deprecated` + `deprecatedIn`, `removeIn`, `replacedBy`, `detect` (regex) — `check_screen.py` zacznie ostrzegać automatycznie.
5. `python3 tools/build_all.py`, testy, obejrzane zrzuty, commit źródeł + `site/` + wzorców testu.

## Zasady systemu, których pilnujesz w każdej zmianie

Ramka zawsze 2 px, rogi proste; tylko twarde cienie 2/4/6 px bez rozmycia; Archivo dla tekstu, Press Start 2P tylko dla liczb i etykiet ≤ 3 słów; jeden kolor akcji (`--action`) i jeden „głośny” element na ekran; żółty tylko „nowe”; akcenty NES tylko w rankingu, pakietach i stanie zablokowanym; stany nie zmieniają rozmiaru; kolor nigdy jedynym nośnikiem znaczenia; kolory zawsze przez tokeny (inaczej psuje się tryb ciemny); każda klikalna kontrolka musi działać. Pełna lista: `design.md` §1 i §10.

## Czego nie robić

- Nie edytuj plików generowanych (lista wyżej) ani kopii systemu poza `skills/panel-piksel-ui/assets/`.
- Nie zmieniaj treści przykładów i ekranów testowych przy okazji zmian stylu.
- Nie commituj `dist/`, plików `*.diff.png`, `.DS_Store`.
- `research/` jest poza repozytorium (zrzuty cudzych stron i gier, repozytorium publiczne) — nie usuwaj go z `.gitignore` i nie dodawaj takich zrzutów gdzie indziej bez zgody właściciela.
- Nie publikuj strony (Cloudflare) ani nie wypychaj zmian bez prośby użytkownika.

## Struktura

```
design.md                    specyfikacja (źródło prawdy)
panel-piksel.config.json     co synchronizuje sync_system.py
skills/panel-piksel-ui/      skill + kod systemu (assets/), przykłady, skrypty, evals
skills/panel-piksel-ui-workspace/  wyniki testów skilla (iteracje)
tools/                       docgen, doc_cards, build_zip, build_site, build_all, crops.js (wycinki do docs/evidence, wymaga puppeteer-core w PUPPETEER_CORE)
docs/                        dokumentacja dla designerów, decyzje, kandydaci, wycinki (evidence/), grafiki (showcase/)
screens/landing/             przykładowy ekran
tests/visual/                wzorce testu wizualnego
site/                        wygenerowana strona (Cloudflare Pages)
research/                    (tylko lokalnie, w .gitignore) studium kierunku, palety, moodboard
```
