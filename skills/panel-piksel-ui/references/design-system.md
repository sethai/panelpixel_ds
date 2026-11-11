# Panel & Piksel — design system

> Retro-pikselowy system dla katalogów, listingów, tabel, rankingów i sklepów.
> Wersja **1.11.0** · 2026-11-10 · status: **zaakceptowany; dokumentacja komponentów v1.2 zaakceptowana, wartości do walidacji w implementacji**

Ten plik jest samodzielną specyfikacją do użycia w kolejnych projektach. Zawiera zasady, tokeny, komponenty, wzorce układu, dostępność i gotowy kod CSS. Uzasadnienia i dowody (zrzuty, pomiary) są w materiałach badawczych:

- `research/direction-study.html` / `.pdf` — studium kierunku (źródło decyzji)
- `research/palette-comparison.html` / `.pdf` — porównanie palet SNES / PICO-8 / NES
- `research/moodboard.html` / `.pdf` — 10 przebadanych kierunków
- `research/evidence/manifest.json` — rejestr zrzutów i pomiarów CSS
- `docs/panel-piksel-komponenty-v2.html` — **dokumentacja komponentów dla designerów (v2.0, system 1.9)**: 29 kart rodzin z anatomią, wariantami, tokenami, dostępnością, statusem w systemie i wycinkami z ekranów oraz przykładów (poprzednia wersja v1.2: `docs/panel-piksel-komponenty-v1.html`)
- `docs/decyzje-v1-1.html` — decyzje z 2026-11-10 z działającymi porównaniami wariantów

### Start dla agenta budującego ekrany

Pakiet = ten plik (zasady) + fundament w kodzie + przykłady. Nie pisz własnych stylów komponentów — złóż ekran z gotowych klas.

| Co | Ścieżka (względem katalogu repozytorium) |
|---|---|
| Tokeny (kolory, typografia, odstępy, cienie, tryb ciemny) | `skills/panel-piksel-ui/assets/tokens.css` |
| Komponenty (klasy z §6) | `skills/panel-piksel-ui/assets/components.css` |
| Zachowanie list kart (sortowanie, filtry, licznik, przełączniki) | `skills/panel-piksel-ui/assets/list-controls.js` |
| Sortowanie tabel | `skills/panel-piksel-ui/assets/table-sort.js` |
| Ikony pikselowe (UI + przedmioty z gier) | `skills/panel-piksel-ui/assets/icons.css` (+ pojedyncze SVG w `assets/icons/`; źródło: `scripts/build_icons.py`) |
| Formularze (walidacja, kroki), okna, szuflada, menu, podpowiedzi, powiadomienia, zaznaczanie wierszy, postęp, nawigacja mobilna | `skills/panel-piksel-ui/assets/ui-controls.js` |
| Wykresy i minilinie | `skills/panel-piksel-ui/assets/charts.js` |
| Szablon strony | `skills/panel-piksel-ui/assets/starter.html` |
| **Katalog przykładów: wszystkie komponenty, warianty i stany, jasny i ciemny** | `skills/panel-piksel-ui/examples/komponenty.html` |
| Katalog ikon | `skills/panel-piksel-ui/examples/ikony.html` |
| Wzorce: formularz w krokach, zaznaczanie wierszy, ładowanie i „Pokaż więcej”, wykresy | `skills/panel-piksel-ui/examples/wzorce.html` |
| Złożone strony (przykłady całych ekranów) | `screens/landing/index.html` (landing), `skills/panel-piksel-ui-workspace/iteration-1/*/with_skill/outputs/*.html` (lista ofert, ranking, sklep, katalog, szczegóły, panel pracodawcy) |
| Przepisy ekranów | `skills/panel-piksel-ui/references/screen-recipes.md` |
| Kontrola | `scripts/check_screen.py` (zasady), `scripts/render_check.py` (render 1280/390 px + test klikania), `scripts/inline_css.py` (jeden przenośny plik) w `skills/panel-piksel-ui/` |

Import w HTML (fonty z Google Fonts mają polskie znaki):

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400&family=Press+Start+2P&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./panel-piksel/tokens.css">
<link rel="stylesheet" href="./panel-piksel/components.css">
<link rel="stylesheet" href="./panel-piksel/icons.css">
<!-- tylko gdy ekran ma listy kart z sortowaniem/filtrami lub sortowalne tabele -->
<script src="./panel-piksel/list-controls.js" defer></script>
<script src="./panel-piksel/table-sort.js" defer></script>
<!-- gdy ekran ma przełączniki, licznik −/+, pliki, okna, szufladę, menu, podpowiedzi, powiadomienia lub zwijaną nawigację -->
<script src="./panel-piksel/ui-controls.js" defer></script>
<!-- gdy ekran ma wykresy (figure.chart[data-chart]) lub minilinie w .stat -->
<script src="./panel-piksel/charts.js" defer></script>
```

Uruchomienie przykładów: otwórz plik HTML w przeglądarce (bez serwera i bez budowania). Tryb ciemny: `<html data-theme="dark">` albo `data-theme="auto"` (wg ustawień systemu).

**Granice rozszerzania:** nie edytuj `tokens.css` ani `components.css` w projekcie — style ekranu w osobnym bloku, tylko układ i dopasowania z użyciem `var(--…)`. Nowy element buduj z prymitywów (ramka `--border`, cień `--shadow-*`, promień 0, Archivo / pixel-font dla liczb) i opisz go jako kandydata do tego pliku. **Weryfikacja:** `check_screen.py` bez ERROR, `render_check.py` bez poziomego przewijania i bez martwych kontrolek, obejrzane zrzuty 1280 i 390 px.

---

## 0. Zarządzanie systemem (v1.9)

### 0.1 Statusy komponentów

| Status | Znaczenie | Czy używać w produkcie |
|---|---|---|
| **stabilny** | spełnia całą checklistę §0.2 | tak |
| **testowy** | w systemie, działa i ma przykład, ale brakuje części testów albo użycia na 2 ekranach | tak, ze świadomością, że szczegóły mogą się zmienić w wersji minor |
| **kandydat** | widziany na ekranach, poza systemem (aneks dokumentacji) | nie — zbuduj z prymitywów i zgłoś (§0.5) |
| **wycofywany** | zastąpiony; działa do wersji z kolumny „usunięcie”, `check_screen.py` ostrzega | nie w nowych ekranach; przenieś istniejące |

Źródłem jest `skills/panel-piksel-ui/assets/components.json`; tabela poniżej generuje się przez `sync_system.py` — nie edytuj jej ręcznie.

<!-- pp:registry -->
| Komponent | Status | Od | Klasy / skrypt | Opis | Brakuje do „stabilny” / zastąpione przez |
|---|---|---|---|---|---|
| Przycisk | **stabilny** | 1.0 | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-full` … | §6.1 | — |
| Przycisk kompaktowy 36 px | **stabilny** | 1.6 | `.btn-compact`, `.card-foot` | §6.1 | — |
| Badge | **stabilny** | 1.0 | `.badge`, `.badge-new`, `.badge-seg`, `.badge-sm` | §6.2 | — |
| Chip / tag | **stabilny** | 1.0 | `.chip`, `.chips`, `.chip-more` | §6.3 | — |
| Licznik | **stabilny** | 1.0 | `.count` | §6.4 | — |
| Awatar / monogram | **stabilny** | 1.0 | `.avatar`, `.avatar-xl` | §5 | — |
| Panel listy | **stabilny** | 1.0 | `.panel`, `.is-featured`, `.panel-head`, `.list` … | §6.5 | — |
| Karta | **stabilny** | 1.0 | `.card`, `.card-body`, `.card-head`, `.card-sub` … | §6.6 | — |
| Panel filtrów, pole, checkbox | **stabilny** | 1.0 | `.panel-filters`, `.field`, `.checkbox` | §6.7 | — |
| Wyszukiwarka główna | **stabilny** | 1.1 | `.search-main` | §6.11 | — |
| Zakładki (panele) i przełącznik sortowania | **stabilny** | 1.1 | `.tabs` | §6.11 | — |
| Tabela danych z sortowaniem | **stabilny** | 1.1 | `.table-wrap`, `.table`, `.sort`, `.sorted` … · `table-sort.js` | §6.11 | — |
| Paginacja | **stabilny** | 1.1 | `.pagination` | §6.11 | — |
| Podium | **stabilny** | 1.0 | `.podium` | §6.8 | jedno użycie z natury (ranking) |
| Pakiet i znacznik pakietu / rzadkości | **stabilny** | 1.0 | `.tier`, `.tier-tag` | §6.9 | — |
| Nagłówek, okruszki, nagłówek treści, sekcja, stopka | **stabilny** | 1.1 | `.container`, `.site-header`, `.logo`, `.site-nav` … | §6.11 | — |
| Callout (wskazówka) | **stabilny** | 1.0 | `.callout` | §6.10 | — |
| Pusty stan | **stabilny** | 1.0 | `.empty` | §6.10 | — |
| Fakty encji | **stabilny** | 1.1 | `.facts` | §6.11 | — |
| Detale graficzne | **stabilny** | 1.0 | `.dither`, `.list-square`, `.bg-dots` | §5 | — |
| Sterowanie listą kart (sortowanie, filtry, licznik, przełącznik) | **stabilny** | 1.4 | `list-controls.js` | §6.12 | — |
| Przycisk w trakcie wysyłania | **testowy** | 1.6 | `.is-loading` | §6.1 | użycie na 2 ekranach, test z czytnikiem |
| Przycisk-ikona | **testowy** | 1.7 | `.icon-btn` | §6.16 | użycie na 2 ekranach, test z czytnikiem |
| Pokaż więcej | **testowy** | 1.8 | `.load-more` · `list-controls.js` | §6.20 | użycie na 2 ekranach, test z czytnikiem |
| Błąd, ostrzeżenie, podpowiedź, zablokowane, tylko do odczytu | **testowy** | 1.6 | `.field.is-error`, `.field-error`, `.field.is-warning`, `.field-warning` … | §6.13, §6.14 | użycie na 2 ekranach, test z czytnikiem |
| Formularz z walidacją, podsumowaniem błędów i krokami | **testowy** | 1.8 | `.error-summary`, `.steps-progress`, `.wizard-step`, `.wizard-nav` · `ui-controls.js` | §6.18 | użycie na 2 ekranach, test z czytnikiem |
| Lista wyboru, radio, przełącznik, pole wielowierszowe, licznik −/+, plik | **testowy** | 1.7 | `.select`, `.radio`, `.switch`, `.field-count` … · `ui-controls.js` | §6.14 | użycie na 2 ekranach, test z czytnikiem |
| Powiadomienia (w treści i wyskakujące) | **testowy** | 1.7 | `.notice`, `.notice-info`, `.notice-success`, `.notice-warning` … · `ui-controls.js` | §6.15 | użycie na 2 ekranach, test z czytnikiem |
| Okno, szuflada, menu, podpowiedź | **testowy** | 1.7 | `dialog.modal`, `dialog.drawer`, `.menu`, `.menu-list` … · `ui-controls.js` | §6.16 | użycie na 2 ekranach, test z czytnikiem |
| Zwijana nawigacja i filtry w szufladzie | **testowy** | 1.7 | `.nav-toggle`, `.site-nav[data-collapsible]`, `.filters-toggle`, `[data-drawer-form]` · `ui-controls.js` | §6.17 | użycie na 2 ekranach, test na telefonie |
| Zaznaczanie wierszy i akcje zbiorcze | **testowy** | 1.8 | `.col-check`, `.bulk-bar`, `.bulk-count` · `ui-controls.js` | §6.19 | użycie na 2 ekranach, test z czytnikiem |
| Szkielet, błąd wczytania, postęp, ładowanie w miejscu | **testowy** | 1.6 | `.skel`, `.skel-row`, `.load-error`, `.progress` … · `ui-controls.js` | §6.13, §6.20 | użycie na 2 ekranach, test z czytnikiem |
| Wykresy i kafelki liczb | **testowy** | 1.8 | `.chart`, `.stats`, `.stat`, `.chart-spark` · `charts.js` | §6.21 | użycie na 2 ekranach, test z czytnikiem |
| Ikony pikselowe | **testowy** | 1.7 | `.icon`, `.sprite` | §5 | użycie na 2 ekranach |
| Tryb ciemny | **testowy** | 1.6 | `[data-theme=dark]`, `[data-theme=auto]` | §2.6 | sprawdzenie na 7 ekranach, potwierdzenie #F27961 w Jehkoba32 |
| Tryb wysokiego kontrastu | **testowy** | 1.7 | — | §8 | test na Windows z wysokim kontrastem |
| Liczba przy opcji filtra (liczona automatycznie) | **testowy** | 1.10 | `.opt-n`, `.is-zero` · `list-controls.js` | §6.7 | użycie na 2 ekranach, test z czytnikiem |
| Zakres od–do | **testowy** | 1.10 | `.range` · `list-controls.js` | §6.7 | użycie na 2 ekranach, test z czytnikiem |
| Wiersz meta w karcie | **testowy** | 1.10 | `.card-meta` | §6.6 | użycie na 2 ekranach, test z czytnikiem |
| Kod kraju | **testowy** | 1.11 | `.cc` | §6.11 | użycie na 2 ekranach, test z czytnikiem |
| Wyszukiwarka z listą wyboru | **testowy** | 1.11 | `.search-main.has-select`, `.search-main .select` | §6.11 | użycie na 2 ekranach, test z czytnikiem |
| Pionowa karta produktu | **testowy** | 1.11 | `.card-vertical`, `.card-art`, `.card-price` | §6.6 | użycie na 2 ekranach, test z czytnikiem |
| Sortowanie listy jako zakładki (role=tab) | **wycofywany** | 1.1 | — | — | → role=group + przyciski aria-pressed (§6.12) · wycofany w 1.6, usunięcie w 2.0 |
| Callout błędu | **wycofywany** | 1.6 | — | — | → .notice.notice-error (§6.15) · wycofany w 1.7, usunięcie w 2.0 |
| Rzadkość jako badge z kwadratem | **wycofywany** | — | — | — | → .tier-tag (§6.9) · wycofany w 1.6, usunięcie w 2.0 |
| Nadpisana wysokość przycisku w stylach ekranu | **wycofywany** | — | — | — | → .btn-compact (§6.1) · wycofany w 1.6, usunięcie w 2.0 |
<!-- /pp:registry -->

### 0.2 Checklista „gotowe” (testowy → stabilny)

**Projekt**
- [ ] tylko tokeny (kolor, typografia, odstępy, cienie) — żadnych wpisanych wartości
- [ ] komplet stanów z macierzy §6.22 (albo świadome „nie dotyczy”); rozmiar nie zmienia się w stanach
- [ ] zachowanie przy długiej treści, 390 px i 1280 px, polskie znaki
- [ ] tryb ciemny i tryb wysokiego kontrastu

**Kod**
- [ ] klasy w `components.css` (sekcja z numerem wersji), zachowanie w `assets/*.js` bez zależności, kontrakt `data-*` opisany w nagłówku pliku
- [ ] natywny element HTML tam, gdzie istnieje (`button`, `dialog`, `input`, `details`), ARIA tylko do uzupełnienia

**Dokumentacja**
- [ ] sekcja w `design.md` (przeznaczenie, anatomia, warianty, stany, zasady, kod)
- [ ] działający przykład w `examples/` i wpis w `components.json`
- [ ] wpis w historii zmian

**Testy**
- [ ] `check_screen.py` bez ERROR, `render_check.py` bez przewijania w poziomie i bez martwych kontrolek
- [ ] wzorzec wizualny zatwierdzony (`visual_regression.py --update`)
- [ ] przejście klawiaturą (Tab, Shift+Tab, Enter, Spacja, Esc, strzałki tam, gdzie wzorzec APG je przewiduje)
- [ ] czytnik ekranu: VoiceOver + Safari i NVDA + Chrome lub Firefox (§0.6)
- [ ] kontrast zmierzony narzędziem na wdrożeniu; tryb wysokiego kontrastu w Windows

**Użycie**
- [ ] użyty na co najmniej 2 ekranach produktu

### 0.3 Wersjonowanie

Numer w `skills/panel-piksel-ui/VERSION` (teraz **1.9.0**) według zasad semver:

| Zmiana | Przykład | Wersja |
|---|---|---|
| **patch** 1.9.x | poprawka błędu bez zmiany API (klasy, atrybuty, tokeny) | 1.9.0 → 1.9.1 |
| **minor** 1.x | nowy komponent, wariant, token, ikona; wycofanie czegoś (stara wersja nadal działa) | 1.9 → 1.10 |
| **major** x.0 | usunięcie wycofanego elementu, zmiana nazwy klasy lub tokenu, zmiana wyglądu wymagająca przeróbki ekranów | 1.x → 2.0 |

Każda wersja: wpis w §12 (co, dlaczego, czy wymaga zmian w ekranach), `sync_system.py`, `visual_regression.py`.

### 0.4 Wycofywanie

1. Wycofany element dostaje w `components.json` status `deprecated`, `deprecatedIn`, `removeIn` (najwcześniej następna wersja major), `replacedBy` i wyrażenie `detect`.
2. `check_screen.py` od razu ostrzega w każdym ekranie, który go używa, i podaje zamiennik.
3. Kod wycofanego elementu działa do `removeIn` (np. `list-controls.js` nadal obsługuje sortowanie zakładkami).
4. W §12 opis migracji: co zamienić na co.
5. W wersji `removeIn` kod jest usuwany, a ostrzeżenie zmienia się w błąd.

### 0.5 Zgłaszanie zmian i nowych komponentów

1. **Potrzeba** — ekran wymaga czegoś, czego nie ma. Najpierw sprawdź `examples/` i §6; często wystarczy złożyć istniejące klocki.
2. **Szkic w ekranie** — zbuduj element w stylach ekranu z prymitywów systemu (ramka, cień, tokeny); opisz go w odpowiedzi jako kandydata.
3. **Zgłoszenie** — wpis `draft` w `components.json` (nazwa, ekran, klasy) + krótki opis: problem, gdzie wystąpił, propozycja.
4. **Decyzja właściciela systemu** — przyjąć jako testowy, zastąpić istniejącym, odrzucić. Porównanie wariantów jak w `docs/decyzje-v1-1.html`.
5. **Testowy** — kod w `components.css`/`assets`, przykład, sekcja w design.md, wersja minor.
6. **Stabilny** — po checkliście §0.2.

Właściciel systemu: **Konrad Kosiorek** (konrad.kosiorek@gmail.com) — decyduje o statusach, wersjach, wycofaniach i kandydatach (od 2026-11-10).

### 0.6 Wspierane przeglądarki i testy

| Przeglądarka | Wersje | Uwagi |
|---|---|---|
| Chrome, Edge | 2 ostatnie | testy automatyczne działają w Chrome |
| Firefox | 2 ostatnie (min. 121) | `:has()` w kilku regułach kosmetycznych |
| Safari macOS i iOS | 2 ostatnie (min. 15.4) | `<dialog>`, maski ikon z prefiksem `-webkit-` |
| Windows, tryb wysokiego kontrastu | Edge, Chrome | reguły `@media (forced-colors: active)` |

**Testy automatyczne** (w katalogu projektu):

```bash
python3 skills/panel-piksel-ui/scripts/sync_system.py --check          # kopie systemu zgodne ze źródłem
python3 skills/panel-piksel-ui/scripts/check_screen.py ekran.html     # zasady, wycofywane wzorce
python3 skills/panel-piksel-ui/scripts/render_check.py ekran.html     # 1280/390 px, fonty, martwe kontrolki
python3 skills/panel-piksel-ui/scripts/visual_regression.py tests/visual skills/panel-piksel-ui/examples/*.html
```

Test wizualny porównuje zrzuty (1280 i 390 px, jasny i ciemny, bez ruchu) z wzorcami w `tests/visual/` blokami 8×8 px — drgania wygładzania liter są pomijane, zmiana koloru, ramki, odstępu czy tekstu nie. Wzorce zapisuj na tej samej maszynie i wersji Chrome, na której są sprawdzane; po zmianie wersji Chrome zatwierdź je ponownie (`--update`) po obejrzeniu różnic.

**Test z czytnikiem ekranu** (ręczny, przed statusem „stabilny”):
1. VoiceOver + Safari (macOS): Cmd+F5; nawigacja VO+strzałki, rotor (VO+U) — nagłówki, punkty orientacyjne, łącza, formularze.
2. NVDA + Chrome lub Firefox (Windows): tryb przeglądania (strzałki, H, D, F, T), tryb formularzy (Tab).
3. Dla każdego komponentu zapisz: co czytnik ogłasza (nazwa, rola, stan), czy zmiana stanu jest ogłaszana (zaznaczenie, rozwinięcie, błąd, wynik filtrowania, powiadomienie), czy fokus trafia we właściwe miejsce (okno, podsumowanie błędów, kolejny krok, „Pokaż więcej”).
4. Powiększenie 200% i szerokość 320 px (WCAG 1.4.10): nic nie znika, nie trzeba przewijać w poziomie (poza tabelą w ramce).

### 0.7 Jedno źródło kodu

Kod systemu ma jedno źródło: `skills/panel-piksel-ui/assets/`. Wszystko inne to kopie, które aktualizuje `sync_system.py` według `panel-piksel.config.json` w katalogu projektu:
- §9 tego pliku (kod CSS) i tabela statusów w §0.1,
- `skills/panel-piksel-ui/references/design-system.md` (kopia tego pliku dla skilla),
- `assets/tokens.json` — tokeny w formacie W3C Design Tokens (do Figmy Tokens Studio, Style Dictionary, aplikacji); wartości trybu ciemnego w `$extensions["panel-piksel.dark"]`,
- katalogi z kopią plików (`copies`), strony z wklejonym CSS (`builds`, `inlined`), zainstalowany skill (`installed`).

`--check` tylko sprawdza i kończy się błędem przy rozjeździe — do uruchamiania przed oddaniem pracy lub w CI. Nie edytuj kopii: zmiana w kopii zniknie przy następnej synchronizacji.

---

## 1. Esencja

**Katalog zbudowany z białych paneli z czarną ramką i twardym cieniem, w których mieszkają gęste, numerowane listy.** Tekst jest czytelny i nowoczesny (Archivo). Piksel pojawia się tam, gdzie się **nie czyta, tylko patrzy**: w liczbach, kwotach i rangach (Press Start 2P), w schodkowych narożnikach kontrolek, w ilustracjach i separatorach. Raz na ekran wolno zrobić „scenę” — podium albo wyróżniony panel.

### Pochodzenie

| Składnik | Źródło inspiracji |
|---|---|
| Panele list z licznikiem, karty, panel filtrów, twarde cienie | Bored.com |
| Czytelność, przycisk-klawisz, pikselowe ilustracje i separatory | Kizupi |
| Podium, tiery, kolor per miejsce | koncepty eventowe z Dribbble (Hackathon „Status Code 1”, WorkOS Launch Week) |
| Schodkowy narożnik, badge segmentowy, gramatyka pixel | NES.css |
| Paleta | SNES (Jehkoba32) + akcenty NES |

### 10 zasad

1. **Dane są spokojne, rama jest głośna.** Listy i tabele nie mają dekoracji; charakter dają ramki, cienie, nagłówki i ikony.
2. **Jedna rodzina tekstowa: Archivo.** Font pikselowy (Press Start 2P) tylko dla liczb, liczników, kwot, rang i etykiet ≤ 3 słów.
3. **Ramka zawsze 2 px.** Nigdy 1 px, nigdy 4 px.
4. **Głębia tylko przez twardy cień bez rozmycia**: 2 / 4 / 6 px. Żadnych `blur`, gradientów elewacji ani miękkich cieni.
5. **Kontenery mają proste rogi (0).** Małe kontrolki mają **schodkowy narożnik 2 px**. Nie używamy `border-radius` > 0.
6. **Jeden kolor akcji** (zieleń `#17735F`). Żółty `#F7C93E` znaczy wyłącznie „nowe / wyróżnione”.
7. **Jeden „głośny” element na ekran**: podium, wyróżniony panel albo ilustracja — nigdy kilka naraz.
8. **Stany nie zmieniają rozmiaru.** Najechanie, wciśnięcie, fokus i blokada zmieniają tylko cień, kolor i `transform`.
9. **Kolor nigdy nie jest jedynym nośnikiem znaczenia** (ranga = numer + wysokość + kolor; tier = nazwa + kolor).
10. **Piksele w skali całkowitej.** Ikony i ilustracje skalujemy ×2, ×3, ×4 z `image-rendering: pixelated`.

### Kiedy używać

- Katalogi, directory, job boardy, marketplace'y, rankingi, leaderboardy, sklepy z pakietami, produkty z „grywalnym” tonem.
- Treść głównie tekstowa (nazwy, kwoty, tagi), mało własnych zdjęć.

### Kiedy nie używać

- Produkty, w których dominuje długa lektura (blog, dokumentacja) — wtedy tylko tokeny koloru i typografii, bez „sceny”.
- Kontekst wymagający powagi (zdrowie, finanse osobiste, prawo).

---

## 2. Kolor

Paleta systemu: **SNES (Jehkoba32)**. Akcenty z palety **NES** wyłącznie w scenie rankingu, w pakietach (tierach) i jako neutralna szarość stanu zablokowanego. Jedyny kolor spoza palet: czysta biel `#FFFFFF` dla paneli.

### 2.1 Tokeny semantyczne

| Token | Hex | Rola | Kontrast (WCAG 2.x) |
|---|---|---|---|
| `--paper` | `#F0EDD8` | Tło strony | — |
| `--paper-dots` | `rgba(217,76,135,.22)` | Kropki 1.5 px co 16 px na tle strony (opcjonalnie) | dekoracja |
| `--surface` | `#FFFFFF` | Panele, karty, pola formularzy | — |
| `--ink` | `#00021C` | Tekst, ramki, cienie | 17.4:1 na `--paper`, 20.5:1 na `--surface` |
| `--ink-2` | `#1C284D` | Opisy, tekst drugorzędny | 14.4:1 na `--surface` |
| `--ink-3` | `#2D5280` | Meta, numery wierszy, „Zobacz wszystkie” | 8.0:1 na `--surface` |
| `--on-ink` | `#F0EDD8` | Tekst na tle `--ink` (liczniki) | 17.4:1 |
| `--action` | `#17735F` | Jedyny kolor akcji (CTA) | biały tekst 5.7:1 |
| `--action-edge` | `#00021C` | Dolna krawędź przycisku akcji | — |
| `--on-action` | `#FFFFFF` | Tekst na `--action` | 5.7:1 |
| `--highlight` | `#F7C93E` | „Nowa”, wyróżnione, zaznaczenie w checkboxie | `--ink` na nim 13.0:1 |
| `--mint` | `#96E3C9` | Callout, zakreślenie słowa w nagłówku | `--ink` na nim ≥ 12:1 |
| `--link` | `#2469B3` | Linki, okruszki | 5.6:1 na `--surface` |
| `--focus` | `#2469B3` | Pierścień fokusu | 4.8:1 na `--paper` (wymagane 3:1) |
| `--focus-deco` | `#0BAFE6` | Kolorowy cień wyszukiwarki — **tylko dekoracja** | 2.2:1 — nie używać jako fokusu |
| `--danger` | `#D9214F` | Błąd, usuwanie | 4.9:1 na `--surface`, biały na nim 4.9:1 |
| `--featured` | `#D94C87` | Cień wyróżnionego panelu (1× na ekran) | dekoracja |
| `--chip` | `#A3CCD9` | Tło chipów/tagów | `--ink` 11.9:1 |
| `--chip-more` | `#F0BB90` | Licznik „+N” przy chipach | `--ink` ≥ 11:1 |
| `--btn-secondary-edge` | `#A3CCD9` | Dolna krawędź przycisku drugorzędnego | dekoracja |
| `--line-soft` | `#A3CCD9` | Linie pomocnicze (przerywana linia panelu, separator fieldsetów) | dekoracja |
| `--disabled-bg` | `#BCBCBC` | Tło zablokowanego przycisku (NES) | — |
| `--disabled-ink` | `#1C284D` | Tekst zablokowanego przycisku | 7.6:1 na `--disabled-bg` |
| `--disabled-line` | `#2D5280` | Ramka zablokowanego przycisku | 4.2:1 |

### 2.2 Akcenty NES (tylko scena rankingu i pakiety)

| Token | Hex | Rola | Kontrast |
|---|---|---|---|
| `--podium` | `#0000BC` | Tło sceny rankingu | biały 11.9:1 |
| `--gold` | `#F8B800` | 1. miejsce, punkty zwycięzcy | na `--podium` 6.9:1; `--ink` na nim 11.6:1 |
| `--silver` | `#BCBCBC` | 2. miejsce | `--ink` na nim 10.8:1 |
| `--bronze` | `#E45C10` | 3. miejsce | `--ink` na nim 5.7:1 |
| `--tier-legendary` | `#AC7C00` | Pakiet Legendarny (pasek) | 3.7:1 na bieli |
| `--tier-epic` | `#6844FC` | Pakiet Epicki (pasek) | 5.5:1 |
| `--tier-rare` | `#0078F8` | Pakiet Rzadki (pasek) | 4.2:1 |
| `--tier-common` | `#7C7C7C` | Pakiet Zwykły (pasek) | 4.2:1 |

### 2.3 Kolory awatarów / monogramów

Tła monogramów firm i kategorii (biały tekst w Press Start 2P): `--avatar-1 #17735F`, `--avatar-2 #2469B3`, `--avatar-3 #993649`, `--avatar-4 #732866`, `--avatar-5 #00021C`, `--avatar-6 #D9214F`. Przypisanie deterministyczne (np. hash nazwy % 6).

### 2.4 Pełna paleta ilustracji (SNES Jehkoba32)

Ilustracje, ikony i pixel-art używają **wyłącznie** tej palety (31 kolorów odczytanych ze źródła; źródło podaje 32):

```
00021C 1C284D 343473 2D5280 4D7A99 7497A6 A3CCD9 F0EDD8
732866 A6216E D94C87 D9214F F25565 F27961 993649 B36159
F09C60 B38F24 B3B324 F7C93E 17735F 119955 67B31B 1BA683
47CCA9 96E3C9 2469B3 0B8BE6 0BAFE6 F28D85 F0BB90
```

Źródło: [Sprite Fusion — Pixel Art Color Palettes](https://www.spritefusion.com/pixel-art-color-palettes) (SNES — autor Jehkoba; NES — paleta sprzętowa).

### 2.5 Zasady koloru

- Na ekranie najwyżej **jeden** element w `--action` o dużej powierzchni (główne CTA). Pozostałe akcje są drugorzędne.
- `--highlight` nie jest kolorem akcji — nie robimy żółtych przycisków.
- `--featured` (różowy cień) i `--focus-deco` (niebieski cień) — maksymalnie jeden z nich na ekran.
- Kolory NES nie pojawiają się poza podium, tierami i stanem zablokowanym.
- Tryb ciemny: **niezdefiniowany** (patrz §11).

---

### 2.6 Tryb ciemny (v1.6)

Te same komponenty, inne tokeny. Włączenie: `data-theme="dark"` (lub `"auto"`) na `<html>`. Kontrasty wyliczone z wartości hex.

| Token | Jasny | Ciemny | Kontrast w ciemnym |
|---|---|---|---|
| `--paper` | `#F0EDD8` | `#00021C` | — |
| `--surface` | `#FFFFFF` | `#1C284D` | — |
| `--ink` | `#00021C` | `#F0EDD8` | 12.2:1 na surface, 17.4:1 na paper |
| `--ink-2` / `--ink-3` | `#1C284D` / `#2D5280` | `#A3CCD9` / `#96E3C9` | 8.4:1 / 9.7:1 |
| `--line` (ramki, nowy) | = `--ink` | `#F0EDD8` | — |
| `--shadow-color` (nowy) | = `--ink` | `#2469B3` | 3.7:1 względem paper |
| `--on-light` (nowy) | `#00021C` | `#00021C` | tekst na żółtym, mięcie, złocie, „+N” |
| `--row-hover` (nowy) | `#F8F6EC` | `#2D5280` | — |
| `--link` | `#2469B3` | `#0BAFE6` | 5.7:1 na surface |
| `--focus` | `#2469B3` | `#F7C93E` | 9.2:1 |
| `--danger` | `#D9214F` | `#F27961` | 5.3:1 |
| `--chip` / `--line-soft` / `--btn-secondary-edge` | `#A3CCD9` | `#2D5280` | tekst chipa 6.8:1 |
| `--tier-legendary/epic/rare/common` | `#AC7C00 #6844FC #0078F8 #7C7C7C` | `#F8B800 #9878F8 #3CBCFC #BCBCBC` (NES) | 8.1 / 4.4 / 6.7 / 7.6:1 |
| `--avatar-5` | `#00021C` | `#2D5280` | — |

Bez zmian: `--action`, `--highlight`, `--mint`, `--featured`, akcenty podium, stan zablokowany. Do potwierdzenia: czy `#F27961` należy do Jehkoba32.

### 2.7 Statusy (v1.7)

Cztery statusy komunikatów. Zawsze **kolor + ikona + tekst**. Kolor wypełnia kafelek ikony i lewą krawędź 10 px; tło komunikatu zostaje białe.

| Status | Token | Jasny | Znak na kafelku | Ciemny | Ikona |
|---|---|---|---|---|---|
| Informacja | `--status-info` | `#2469B3` | biały 5.6:1 | `#0BAFE6` + granat | `i-info` |
| Sukces | `--status-success` | `#17735F` | biały 5.7:1 | `#96E3C9` + granat | `i-success` |
| Ostrzeżenie | `--status-warning` | `#E45C10` (NES) | granat 5.7:1 | `#E45C10` + granat | `i-warning` |
| Błąd | `--status-error` | `= --danger` `#D9214F` | biały 4.9:1 | `#F27961` + granat | `i-error` |

Kolor znaku: `--on-status-*`. Ostrzeżenie nie jest żółte, bo żółty (`--highlight`) znaczy w systemie „nowe/wyróżnione”. Pomarańcz NES rozszerza akcenty NES o jeden status.

## 3. Typografia

### 3.1 Rodziny

| Token | Rodzina | Zastosowanie | Licencja |
|---|---|---|---|
| `--font-sans` | **Archivo** (variable, 100–900) | Cały tekst do czytania, nagłówki, przyciski, formularze | OFL, Google Fonts |
| `--font-pixel` | **Press Start 2P** (400) | Liczby, liczniki, kwoty, rangi, odliczanie, monogramy, etykiety ≤ 3 słów | OFL, Google Fonts |

Obie wersje z Google Fonts zawierają polskie znaki (subset `latin-ext`, sprawdzone renderowaniem „Zażółć gęślą jaźń”). Alternatywa pixel-fontu, gdy Press Start 2P jest za szeroki: **VT323**.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800;900&family=Press+Start+2P&display=swap" rel="stylesheet">
```

### 3.2 Skala

| Token | Rodzina · rozmiar/linia · waga · tracking | Użycie |
|---|---|---|
| `display` | Archivo 40/44 · 900 · −1px | Hero, nagłówek strony głównej |
| `h1` | Archivo 24/32 · 900 · −0.6px | Tytuł strony |
| `panel-title` | Archivo 18/28 · 900 · −0.45px | Tytuł panelu, panelu filtrów |
| `card-title` | Archivo 18/24 · 800 | Tytuł karty |
| `body` | Archivo 16/24 · 400 | Tekst |
| `row` | Archivo 14/20 · 600 | Nazwa w wierszu listy |
| `small` | Archivo 14/20 · 400 | Opis karty, okruszki, opis pola |
| `label` | Archivo 12/16 · 700 · UPPERCASE · +0.3px | Badge |
| `legend` | Archivo 14 · 800 | Nazwa grupy filtrów |
| `pixel-xs` | Press Start 2P 10/16 · +1px | Liczniki, meta, kwoty w wierszach |
| `pixel-sm` | Press Start 2P 12 | Kwoty na kartach, punkty, ceny pakietów |
| `pixel-md` | Press Start 2P 16 | Duże liczby w modułach |
| `pixel-lg` | Press Start 2P 20–32 | Miejsca na podium, odliczanie |

### 3.3 Zasady typografii

- **Nigdy** nie składamy akapitów, opisów ani etykiet formularzy w Press Start 2P.
- Press Start 2P tylko w rozmiarach będących wielokrotnością 2 px (10, 12, 16, 20, 24, 32) — mniej rozmycia.
- Liczby w kolumnach wyrównujemy do prawej.
- Długie tytuły w listach: jedna linia z wielokropkiem + pełny tekst w `title`; w kartach — dowolna liczba linii.
- Kursywa tylko dla motta panelu i stanów „brak danych” („Widełki nie podane”).

---

## 4. Przestrzeń, siatka, kształt, głębia

### 4.1 Odstępy

Siatka **4 px**: `--space-1 4` · `--space-2 8` · `--space-3 12` · `--space-4 16` · `--space-6 24` · `--space-8 32` · `--space-12 48`.

| Element | Wartość |
|---|---|
| Padding panelu listy | 16 / 16 / 20 px |
| Padding karty, panelu filtrów | 16 px |
| Odstęp między panelami | 28 px |
| Odstęp między kartami | 20 px |
| Wysokość wiersza listy | 32 px (desktop) · 40 px (mobile / dotyk) |
| Wysokość przycisku | **44 px**, stała we wszystkich stanach |

### 4.2 Siatka strony

| Widok | Układ |
|---|---|
| Kontener | max 1216 px, margines boczny 16 px (mobile) / 24 px (desktop) |
| Strona główna katalogu | siatka paneli kategorii: 4 kolumny ≥ 1200 px → 3 → 2 → 1 (< 600 px) |
| Strona kategorii | panel z pełną listą (≈ 2/3) + kolumna paneli powiązanych (≈ 1/3) |
| Wyniki wyszukiwania | karty `1fr` + panel filtrów `280px`; < 900 px filtry nad listą lub w szufladzie |
| Ranking | podium (3 miejsca) + panel listy od miejsca 4 |

### 4.3 Kształt

| Token | Wartość | Użycie |
|---|---|---|
| `--border` | `2px solid var(--ink)` | Wszystkie kontenery i kontrolki |
| promień | `0` | Panele, karty, pola, badge |
| `--notch` | `clip-path` ze schodkiem 2 px | Przyciski, chipy (małe kontrolki) |

### 4.4 Głębia

| Token | Wartość | Użycie |
|---|---|---|
| `--shadow-sm` | `2px 2px 0 var(--ink)` | Badge, pola tekstowe |
| `--shadow-md` | `4px 4px 0 var(--ink)` | Karty, panel filtrów |
| `--shadow-lg` | `6px 6px 0 var(--ink)` | Panele list, formularze, podium |
| wariant wyróżniony | `6px 6px 0 var(--featured)` | Jeden panel na ekran |
| krawędź klawisza | `inset 0 -4px 0 <edge>` (hover: −6px) | Przyciski |

Wiersze list, chipy i liczniki **nie mają** cienia.

### 4.5 Ruch

| Token | Wartość | Do czego |
|---|---|---|
| `--motion-fast` (= `--motion`) | 60 ms | przyciski, przełączniki |
| `--motion-base` | 120 ms | menu, podpowiedź, suwak przełącznika |
| `--motion-slow` | 200 ms | okno, szuflada, powiadomienie |
| `--ease-steps` | `steps(3, end)` | wejścia nakładek — „klatkowo”, jak w grze |

- Przejścia tylko `transform`, `box-shadow`, `opacity`; bez easingu sprężynowego.
- Brak animacji wejścia, paralaksy, tickerów w produkcie (ticker z Bored.com świadomie odrzucony).
- `@media (prefers-reduced-motion: reduce)` → wszystkie tokeny ruchu = 0 ms, animacje szkieletu i ładowania wyłączone.

### 4.6 Warstwy i punkty przełamania (v1.7)

| Warstwa | Token | Wartość |
|---|---|---|
| przyklejone nagłówki | `--z-sticky` | 10 |
| menu rozwijane | `--z-dropdown` | 100 |
| szuflada | `--z-drawer` | 200 |
| okno modalne | `--z-modal` | 300 |
| powiadomienia | `--z-toast` | 400 |
| podpowiedź | `--z-tooltip` | 500 |

Okno i szuflada to natywny `<dialog>` (warstwa top layer, z-index ich nie dotyczy). Punkty przełamania: `--bp-sm` 600 px (telefon: 1 kolumna, wiersze 40 px, zwijana nawigacja), `--bp-md` 900 px (filtry w szufladzie, układ jednokolumnowy), `--bp-lg` 1200 px (siatka paneli 4 → 3). W `@media` wpisuje się liczbę — CSS nie przyjmuje tam zmiennych.

---

## 5. Grafika i ikonografia

- **Ikony (v1.7)** — zestaw w `assets/icons.css`, katalog: `examples/ikony.html`. Siatka **12×12**, rysowane piksel po pikselu w duchu ikon z gier 8/16-bit, rozmiary tylko całkowite: 12 / **24 (domyślnie)** / 36 / 48 px.
  - **Ikony interfejsu** `<span class="icon i-search" aria-hidden="true"></span>` — jeden kolor = `currentColor` (działają w jasnym, ciemnym i wysokim kontraście). 39 ikon: search, close, menu, more, filter, sort, chevron-left/right/up/down, plus, minus, check, edit, trash, upload, download, external, eye, lock, list, grid, home, user, mail, bell, pin, calendar, hourglass, cart, heart-outline, heart, star, coin, trophy, info, success, warning, error.
  - **Kolorowe wersje ikon interfejsu** `<span class="sprite s-search" aria-hidden="true"></span>` — 35 ikon (wszystkie poza sercem, gwiazdą, monetą i pucharem, które mają ręcznie rysowane przedmioty) w kolorze znaczenia z twardym cieniem 1 px w prawo-dół, jak w menu gier 16-bit: niebieski — informacja, nawigacja, konto; zielony — dodanie, sukces, wgrywanie, koszyk; czerwony — usunięcie, błąd, lokalizacja; pomarańczowy — edycja, ostrzeżenie; fioletowy — filtry, sortowanie; złoty — czas, powiadomienia; śliwkowy — start, kalendarz; łupkowy — menu, strzałki, widoki, blokada. W trybie ciemnym kolor jaśnieje. Do akcentów (nagłówki kategorii, puste stany, listy cech) — w przyciskach i polach zostają ikony interfejsu, bo tam kolor znaczy stan.
  - **Przedmioty z gier** `<span class="sprite s-coin" aria-hidden="true"></span>` — kolorowe, z palety SNES/NES, obrys jaśnieje w trybie ciemnym. 12 przedmiotów: coin (kwota, cena), heart (zapisane), star (polecane), gem (pakiet), trophy (ranking), potion, sword, shield (weryfikacja), chest (nagroda), key (dostęp), scroll (CV, dokument), flag (cel, punkt kontrolny). Tylko jako akcent obok tekstu — nigdy jedyny nośnik znaczenia.
  - Ikona obok tekstu: `aria-hidden="true"`. Przycisk z samą ikoną: `.icon-btn` 36 px + `aria-label`.
  - Nie kopiujemy grafik z konkretnych gier (postaci, przedmiotów znaków towarowych) — tylko ogólne motywy.
  - Nowa ikona: dopisz rysunek ASCII w `scripts/build_icons.py` (i kolor w `TINT`) i uruchom skrypt — powstaną wersja w kolorze tekstu, wersja kolorowa i strona `examples/ikony.html`.
- **Monogram / awatar**: kwadrat z kolorem `--avatar-n`, 1–2 litery w Press Start 2P, biały tekst. Rozmiary: 20 px (wiersz), 56 px z ramką 2 px (karta, podium). Polskie znaki dozwolone (np. „ŁŻ”).
- **Ilustracje**: pixel-art tylko w hero, pustych stanach, onboardingu i 404. Wyłącznie paleta SNES.
- **Separator „dither”**: pas szachownicy 8 px pod pełnym pasem 8 px, kolor `--action`; tylko między dużymi sekcjami strony.
- **Punktor**: kwadrat 6 px w `--action` zamiast kropki.
- **Tło strony**: opcjonalnie kropki `--paper-dots` 1.5 px co 16 px.
- Ikona **kłódki** (8×9 px ×2) dla zablokowanych akcji — przetestowana: kojarzy się z „zablokowane”, nie z płatną funkcją (test nieformalny, 2026-11-09).

---

## 6. Komponenty

Każdy komponent: anatomia → warianty → stany → zasady. Pełny CSS w §9, przykłady HTML przy komponentach.

### 6.1 Przycisk

**Anatomia:** ramka 2 px (rysowana `inset box-shadow`, bo `clip-path` obcina obramowanie), schodkowy narożnik 2 px, dolna krawędź-klawisz 4 px, etykieta Archivo 15/700, opcjonalna ikona 16 px po lewej. Wysokość **44 px**, padding poziomy 18 px.

| Wariant | Tło | Tekst | Krawędź klawisza |
|---|---|---|---|
| Główny (`.btn-primary`) | `--action` | `--on-action` | `--action-edge` |
| Drugorzędny (`.btn-secondary`) | `--surface` | `--ink` | `--btn-secondary-edge` |
| Pełna szerokość (`.btn-full`) | jak wariant | — | — |
| **Kompaktowy (`.btn-compact`, v1.6)** | jak wariant | etykieta 14 px | wysokość **36 px**, padding 14 px; stany jak w 44 px |

| Stan | Zmiana (rozmiar zawsze bez zmian) |
|---|---|
| Domyślny | krawędź 4 px |
| Najechanie | krawędź 6 px, `translateY(-2px)` |
| Wciśnięty (`:active`, `.is-pressed`, `aria-pressed="true"`) | krawędź znika, etykieta schodzi 4 px w dół wewnątrz przycisku |
| Fokus (`:focus-visible`) | **wewnętrzny** pierścień: 2 px ramka + 3 px `--focus` + 2 px biały (zewnętrzny `outline` byłby obcięty przez `clip-path`) |
| Zablokowany | patrz niżej |

**Zablokowany (wariant A — zaakceptowany):** płaskie tło `--disabled-bg` `#BCBCBC`, ramka `--disabled-line`, tekst `--disabled-ink` (7.6:1), bez krawędzi i cienia, kłódka po lewej, **powód pod przyciskiem**. Ten sam wygląd dla wariantu głównego i drugorzędnego. Nie reaguje na najechanie, kursor `not-allowed`.

```html
<button class="btn btn-primary" type="button">Aplikuj teraz</button>
<button class="btn btn-secondary" type="button">Zapisz ofertę</button>

<!-- zablokowany: aria-disabled zamiast disabled, żeby zachować fokus i odczytać powód -->
<button class="btn btn-primary" type="button" aria-disabled="true" aria-describedby="why-apply">
  <span class="lock" aria-hidden="true"></span>Aplikuj teraz
</button>
<p class="btn-reason" id="why-apply">Uzupełnij CV, aby aplikować.</p>
```

**Kompaktowy 36 px** — tylko dla przycisku powtarzanego w każdej pozycji listy: stopka karty (`.card-foot`), wiersz tabeli, koszyk. Akcja sekcji (Aplikuj, Pokaż wyniki, Wybierz pakiet) zostaje 44 px. Oba rozmiary spełniają WCAG 2.2 2.5.8.

```html
<div class="card-foot"><span>dodano 2 godz. temu</span>
  <button class="btn btn-secondary btn-compact" type="button" aria-pressed="false" data-label-on="Zapisano" data-label-off="Zapisz">Zapisz</button></div>
```

**Ładowanie (v1.6):** `.is-loading` + `aria-disabled="true"` + `aria-busy="true"`; etykieta znika, w środku migają 3 piksele, przycisk „wciśnięty”, rozmiar bez zmian; komunikat „Wysyłanie…” w regionie `aria-live`.

**Zasady:** jeden przycisk główny na sekcję; etykieta = czasownik („Aplikuj”, „Pokaż 42 oferty”); przy `aria-disabled` obsługa kliknięcia w JS musi być zablokowana; nie używać żółtego jako tła przycisku.

### 6.2 Badge

Prostokąt z ramką 2 px i cieniem 2 px, etykieta `label` (12/700, wersaliki).

| Wariant | Wygląd | Użycie |
|---|---|---|
| `.badge` | biały | status neutralny |
| `.badge-new` | `--highlight` | „Nowa”, „Promo” |
| `.badge-sm` | 10 px, bez cienia | w wierszu listy, wyrównany do prawej |
| `.badge-seg` | dwa segmenty: jasny klucz + `--ink` wartość | „Zdalnie | 100%”, „Poziom | Senior” |

```html
<span class="badge badge-new">Nowa</span>
<span class="badge badge-seg"><span>Zdalnie</span><span>100%</span></span>
```

### 6.3 Chip / tag

Tło `--chip`, schodkowy narożnik, Archivo 13/600, **bez cienia i ramki** (w listach jest ich wiele). Nadmiar → licznik `.chip-more` „+N” (kwadrat 32 px z ramką, `--chip-more`). Maks. 4 chipy + „+N” na karcie.

```html
<div class="chips"><span class="chip">React</span><span class="chip">B2B</span><span class="chip-more">+3</span></div>
```

### 6.4 Licznik

Press Start 2P 10 px, tło `--ink`, tekst `--on-ink`, bez ramki. Liczba pozycji w panelu / kategorii / filtrze.

```html
<span class="count">128</span>
```

### 6.5 Panel listy — główna jednostka katalogu

**Anatomia:** panel (`--surface`, ramka 2 px, cień 6 px) → nagłówek (tytuł `panel-title` + licznik) → opcjonalne motto (kursywa, `--ink-3`) → numerowana lista → przerywana linia `--line-soft` → „Zobacz wszystkie”.

**Wiersz listy:** numer (12 px, `--ink-3`, wyrównany do prawej, 22 px) · monogram 20 px · nazwa (`row`, wielokropek) · wartość po prawej (kwota w `pixel-xs` albo `badge-sm`). Wysokość 32 px / 40 px na dotyk. Cały wiersz jest linkiem; najechanie podkreśla nazwę.

| Wariant | Różnica |
|---|---|
| domyślny | cień `--ink` |
| wyróżniony (`.is-featured`) | cień `--featured` — max 1 na ekran |
| skrócony | 5–8 pozycji + „Zobacz wszystkie” (strona główna, mobile) |
| pełny | wszystkie pozycje (strona kategorii) |

```html
<section class="panel" aria-labelledby="cat-frontend">
  <header class="panel-head"><h2 id="cat-frontend">Frontend</h2><span class="count">128</span></header>
  <p class="panel-motto">„Piksele, które klikają się same”</p>
  <ol class="list">
    <li><a href="/oferta/1"><span class="list-n">1.</span><span class="avatar" style="--av:var(--avatar-1)">PF</span>
      <span class="list-name" title="Senior Frontend Developer (React)">Senior Frontend Developer (React)</span>
      <span class="list-value">24 000 zł</span></a></li>
    <li><a href="/oferta/2"><span class="list-n">2.</span><span class="avatar" style="--av:var(--avatar-3)">KQ</span>
      <span class="list-name">Junior Frontend</span><span class="list-value" aria-label="brak widełek">—</span></a></li>
  </ol>
  <a class="panel-more" href="/kategoria/frontend">Zobacz wszystkie</a>
</section>
```

**Kwota w wierszu na wąskim ekranie (v1.6):** poniżej 600 px kwota jest skracana („18–24 tys.”), żeby nie ucinała nazwy; pełna wartość zostaje dla czytnika ekranu. Na desktopie pełna kwota.

```html
<span class="list-value"><span class="amt-full">18 000–24 000</span><span class="amt-short" aria-hidden="true">18–24 tys.</span></span>
```

**Stany brzegowe:** brak wartości → „—” z `aria-label`; brak logo → monogram; długi tytuł → wielokropek + `title`; polskie znaki w monogramie dozwolone.

### 6.6 Karta (wynik wyszukiwania / oferta)

Ramka 2 px, cień 4 px, padding 16 px. Układ: monogram/logo 56 px w ramce · treść (tytuł `card-title` + badge w prawym górnym rogu, podtytuł `small` `--ink-2`, kwota `pixel-sm` + jednostka Archivo 12/600, chipy).

```html
<article class="card">
  <span class="avatar avatar-xl" style="--av:var(--avatar-1)">PF</span>
  <div class="card-body">
    <div class="card-head"><h3>Senior Frontend Developer</h3><span class="badge badge-new">Nowa</span></div>
    <p class="card-sub">Pixel Forge · Kraków / zdalnie</p>
    <p class="amount">18 000–24 000 <small>zł netto B2B</small></p>
    <div class="chips"><span class="chip">React</span><span class="chip">TypeScript</span></div>
  </div>
</article>
```

Brak kwoty → `<p class="amount is-empty">Widełki nie podane</p>` (kursywa Archivo).

**Wiersz meta (v1.10):** opcjonalnie pod podtytułem karty 3–4 kluczowe atrybuty — `<ul class="card-meta"><li><span class="icon icon-sm i-user" aria-hidden="true"></span>Poziom: <b>Senior</b></li><li>Tryb: <b>Zdalnie</b></li><li>Dodano: <b>dziś</b></li></ul>` (13 px `--ink-3`, wartość 700 `--ink-2`, ikony 12 px nieobowiązkowe; na telefonie zawija się).

**Pionowa karta produktu (v1.11):** do siatek sklepu, katalogu produktów i galerii — ilustracja nad nazwą. Modyfikator `.card-vertical` (kolumna, odstęp 10 px) → `.card-art` (pole 88 px, tło `--paper`, ramka 2 px, sprite `-xl` lub obrazek ≤ 64 px) → `h3` → `.tier-tag` (opcjonalnie) → `.card-meta` z atrybutami → `.card-foot` przyklejona do dołu (`margin-top: auto`), w niej cena `.card-price` (sprite waluty + liczba w pixel-foncie + jednostka Archivo) i przycisk `.btn-compact`. Karty w siatce `repeat(auto-fill, minmax(210px, 1fr))` mają równą wysokość, więc ceny stoją w jednej linii. Pole ilustracji nigdy w kolorze akcentu — to nie jest „głośny element”.

```html
<article class="card card-vertical">
  <div class="card-art"><span class="sprite sprite-xl s-sword" aria-hidden="true"></span></div>
  <h3>Ostrze Zmierzchu</h3>
  <span class="tier-tag tier-legendary">Legendarny</span>
  <ul class="card-meta"><li>Broń</li><li>Obrażenia <b>+48</b></li></ul>
  <div class="card-foot">
    <span class="card-price"><span class="sprite sprite-sm s-coin" aria-hidden="true"></span>1 800<small>monet</small></span>
    <button class="btn btn-secondary btn-compact" type="button" aria-pressed="false">Do koszyka</button>
  </div>
</article>
```

### 6.7 Panel filtrów i formularze

- **Panel filtrów**: jak karta (cień 4 px), tytuł `panel-title`, grupy jako `<fieldset>` z linią `--line-soft` i `<legend>` 14/800, na dole przycisk główny pełnej szerokości z liczbą wyników („Pokaż 42 oferty”).
- **Pole tekstowe**: ramka 2 px, cień 2 px, promień 0, Archivo 14; fokus = obrys 3 px `--focus` + kolorowy cień `--focus-deco`.
- **Checkbox**: kwadrat 16 px, ramka 2 px; zaznaczony = tło `--ink` + kwadrat 6 px `--highlight` w środku.
- **Wyszukiwarka główna** (1 na stronę): pole z ramką 2 px i cieniem 6 px w `--focus-deco`.

```html
<aside class="panel-filters" aria-label="Filtry">
  <h2>Filtry</h2>
  <label class="field"><span class="sr-only">Słowa kluczowe</span><input type="search" placeholder="Słowa kluczowe"></label>
  <fieldset><legend>Tryb pracy</legend>
    <label class="checkbox"><input type="checkbox" checked> Zdalnie</label>
    <label class="checkbox"><input type="checkbox"> Hybrydowo</label>
  </fieldset>
  <button class="btn btn-primary btn-full" type="button">Pokaż 42 oferty</button>
</aside>
```

**Liczba przy opcji i zakres (v1.10):**
- `<label class="checkbox"><input type="checkbox" name="tryb" value="zdalnie"> Zdalnie <span class="opt-n"></span></label>` — `list-controls.js` wpisuje, ile pozycji zostanie po zaznaczeniu tej opcji (przy pozostałych filtrach; w obrębie grupy liczona sama opcja). Opcja z 0 dostaje `.is-zero` — wyszarzona, ale klikalna. Liczb nie wpisuje się ręcznie.
- `<div class="range"><label class="field"><span>Od</span><input type="number" data-min="salary"></label><span class="dash" aria-hidden="true">–</span><label class="field"><span>Do</span><input type="number" data-max="salary"></label></div>` — gdy „Od” > „Do”, pod zakresem pojawia się `.field-error` z `aria-invalid` na obu polach, a zakres nie jest stosowany. Suwaka z dwoma uchwytami nie używamy (klawiatura, telefon).

### 6.8 Podium (scena rankingu)

Tło `--podium`, ramka 2 px, cień 6 px. Trzy kolumny; **kolejność w DOM 1, 2, 3**, wizualnie 2–1–3 (`order`). Każde miejsce: monogram 56 px, nazwa, punkty (`pixel-sm`, zwycięzca w `--gold`), stopień z numerem (`pixel-lg`): wysokości 96 / 64 / 44 px, kolory `--gold` / `--silver` / `--bronze`. **Max jedno podium na stronę.** Mobile: ten sam układ do 360 px; węższe → lista 1–3.

```html
<ol class="podium" aria-label="Top pracodawcy tygodnia">
  <li class="podium-1"><span class="avatar avatar-xl" style="--av:var(--avatar-1)">PF</span><b>Pixel Forge</b><span class="podium-pts">1 980</span><span class="podium-step">1</span></li>
  <li class="podium-2"><span class="avatar avatar-xl" style="--av:var(--avatar-2)">8B</span><b>8-Bit Labs</b><span class="podium-pts">1 240</span><span class="podium-step">2</span></li>
  <li class="podium-3"><span class="avatar avatar-xl" style="--av:var(--avatar-3)">KQ</span><b>Kwadrat Quest</b><span class="podium-pts">960</span><span class="podium-step">3</span></li>
</ol>
```

### 6.9 Tiery (pakiety jako rzadkość)

Karta z ramką 2 px, cieniem 2 px i **lewą krawędzią 10 px** w kolorze tieru. Nazwa (Archivo 16/900), cena (`pixel-sm`, prawa strona), opis (`small`). Nazwy: **Legendarny / Epicki / Rzadki / Zwykły**. Kolor zawsze z nazwą.

```html
<div class="tier tier-legendary"><span class="tier-name">Legendarny</span><span class="tier-price">899 zł</span><span class="tier-desc">Podium + wyróżniony panel 30 dni</span></div>
```

**Znacznik tieru (`.tier-tag .tier-legendary|epic|rare|common`)** — kompaktowa wersja do kart, wierszy tabeli i koszyka: wysokość 24 px, ramka 2 px, lewa krawędź 10 px w kolorze tieru, nazwa wersalikami 12/700.

```html
<span class="tier-tag tier-epic">Epicki</span>
```

**Rzadkość przedmiotu (v1.6):** zawsze `.tier-tag` — w karcie sklepu, tabeli i koszyku. Badge z kwadratem 8 px (z pierwszej wersji sklepu) jest odrzucony: kwadrat słabo odróżnia Epicki od Rzadkiego, a cień badge’a sugeruje klikalność.

### 6.10 Pozostałe

| Komponent | Specyfikacja |
|---|---|
| Okruszki | Archivo 14, link `--link`, separator „/” w `--ink-3` |
| Motto panelu | Archivo 14 kursywa, `--ink-3`, w cudzysłowie „…” |
| Callout | tło `--mint` (jasny wariant `#EAFBC8` dopuszczalny jako tint), ramka 2 px, promień 0 |
| Pusty stan | pixel-ilustracja + nagłówek `h1` + jedno zdanie + przycisk główny |
| Separator | `.dither` (§5) |
| Lista z punktorami | `.list-square` (§5) |

### 6.11 Elementy ekranu (v1.1)

| Element | Klasa | Specyfikacja |
|---|---|---|
| Kontener | `.container` | max 1216 px, padding 24 px (16 px < 600 px) |
| Nagłówek serwisu | `.site-header` | tło `--paper`, dolna ramka 2 px, min. 72 px; logo `.logo` w Press Start 2P 14 px (drugi człon w `--action`), nawigacja `.site-nav` Archivo 15/700 — aktywna pozycja podkreślona 2 px (`aria-current="page"`) |
| Wyszukiwarka główna | `.search-main` | pole + przycisk w jednej ramce 2 px, cień 6 px `--focus-deco` (tylko ramka — pole nie ma własnego cienia, poprawka v1.11); przycisk 48 px na `--ink`; max jedna na ekran |
| Wyszukiwarka z listą wyboru (v1.11) | `.search-main.has-select` + `.select > select` | jedna lista (miasto, kategoria) między polem a przyciskiem, oddzielona lewą ramką 2 px, bez własnego cienia; przycisk z tekstem („Szukaj”); < 600 px pole na całą szerokość, lista i przycisk w drugim rzędzie. Więcej niż jedna lista → filtry idą do `.panel-filters` |
| Okruszki | `.breadcrumbs` | Archivo 14, separator „/”, link `--link` |
| Nagłówek treści | `.page-head` | `h1` 24/900 + opis `--ink-2`; po prawej akcje lub zakładki |
| Zakładki / przełącznik | `.tabs` | segmenty w ramce 2 px z cieniem 2 px, wysokość 36 px; wybrany = `--ink` + `--on-ink`. **Dwie semantyki (v1.6):** przełączanie paneli treści (okres rankingu, statusy) → `role="tablist"` + `role="tab"` + `aria-selected`; **sortowanie listy** → `role="group"` + `aria-label="Sortuj …"` + przyciski `aria-pressed` |
| Tabela danych | `.table-wrap` + `.table` | ramka 2 px, cień 6 px; nagłówek na `--paper` (12/800 wersaliki, przyklejony), wiersze 44 px oddzielone linią 2 px `--paper`; liczby `.num` w Press Start 2P 10 px, do prawej; nazwa `.name` 600; na wąskim ekranie przewija się w ramce |
| Sortowanie kolumny | `.sort` / `.sorted` | **`<button class="sort">` tylko wtedy, gdy sortowanie działa** i **dla każdej kolumny z danymi** (poza „#”, „Akcje”); kliknąć można całą komórkę nagłówka; puste wartości zawsze na końcu; wartości porządkowe przez `data-sort-value` + `data-sort-first` (`table-sort.js` dla wierszy w DOM albo własny kod na danych). Kolejność stała (np. ranking po wyniku) → `<span class="sorted">` bez wyglądu przycisku. Kierunek zawsze w `aria-sort` na `<th>`; system rysuje ▲/▼, ◆ = kolumna sortowalna nieaktywna |
| Kod kraju (v1.11) | `.cc` | kwadrat min. 28 × 20 px, ramka 2 px, tło `--paper`, kod ISO 3166-1 alfa-2 w pixel-foncie 7 px; **zawsze z pełną nazwą kraju obok**, sam kod `aria-hidden="true"`; zamiast flag-emoji (na Windows wyświetlają się jako litery i łamią paletę) |
| Miejsce w rankingu | `.rank`, `.rank-1/2/3` | kwadrat 28 px z numerem w pixel-foncie; 1–3 w `--gold/--silver/--bronze` |
| Zmiana wartości | `.delta-up`, `.delta-down` | ▲ w `--action`, ▼ w `--danger` + liczba (kierunek także znakiem, nie tylko kolorem) |
| Paginacja | `.pagination` | kwadraty 36 px z ramką i cieniem 2 px, numery w pixel-foncie; bieżąca strona `--ink`, `aria-current="page"` |
| Callout | `.callout` | tło `--mint`, ramka 2 px, bez cienia |
| Pusty stan | `.empty` | panel z cieniem 6 px, opcjonalna pixel-ilustracja 96 px, `h2`, jedno zdanie, przycisk główny |
| Sekcja | `.section`, `.section-title` | odstęp 40 px; tytuł 18/900 + akcja po prawej |
| Fakty encji | `.facts` | siatka definicji w ramce 2 px; etykieta 11/800 wersaliki `--ink-3`, wartość 15/600 (liczby `.num` w pixel-foncie) |
| Treść długa | `.prose` | max 70 znaków w linii, nagłówki 18/900 |
| Siatki | `.grid-panels`, `.layout-main-side`, `.layout-results`, `.stack` | 4→3→2→1 kolumny; 2/3 + 1/3; karty + filtry 280 px (filtry nad wynikami < 900 px) |
| Stopka | `.site-footer` | górna ramka 2 px, tekst 14 px `--ink-2` |

### 6.12 Interakcje (v1.4)

**Zasada: wszystko, co wygląda na klikalne, działa.** Zakładki sortowania, filtry, liczniki wyników, przełączniki i nagłówki sortowania tabel mają działającą obsługę — inaczej nie umieszczamy ich na ekranie. Liczby w interfejsie zgadzają się z tym, co widać.

| Interakcja | Mechanizm | Zachowanie |
|---|---|---|
| Sortowanie listy kart | `.tabs[role=group][data-sort-for]` + `button[aria-pressed][data-sort-key][data-sort-dir]`; karty `data-sort-<klucz>` | wybrany przycisk `aria-pressed="true"` (v1.6; wcześniej zakładki — skrypt obsługuje oba); pozycje bez wartości na końcu; `data-sort-key="order"` = kolejność z HTML |
| Filtry | `form[data-filter-for]`; checkboxy `name`/`value` ↔ karty `data-f-<name>`; `data-min/max` ↔ `data-n-<name>="od do"`; `data-require`; `data-search` | na żywo; ta sama nazwa = LUB, różne = I; ukryte karty mają `hidden` |
| Licznik wyników | `[data-count-for]` + `data-count-forms="oferta|oferty|ofert"` | polska odmiana; w nagłówku i na przycisku „Pokaż N ofert” |
| Aktywne filtry | `[data-active-for]` | chipy z ×, klik usuwa filtr; wiersz znika, gdy pusto |
| Pusty stan | `[data-empty-for]` + `[data-clear-for]` | pokazywany przy 0 wynikach, z akcją „Wyczyść filtry” |
| Przełącznik | `button[aria-pressed][data-label-on][data-label-off]` | wygląda jak wciśnięty klawisz, zmienia etykietę („Zapisz ofertę” ↔ „Zapisano”) |
| Sortowanie tabeli | `th > button.sort` + `table-sort.js`; stała kolejność → `span.sorted` | patrz §6.11 |

```html
<div class="tabs" role="group" aria-label="Sortuj oferty" data-sort-for="oferty">
  <button type="button" aria-pressed="true" data-sort-key="date" data-sort-dir="desc">Najnowsze</button>
  <button type="button" aria-pressed="false" data-sort-key="salary" data-sort-dir="desc">Najwyższe widełki</button>
</div>
```

Implementacja referencyjna: `list-controls.js` i `table-sort.js` w skillu `panel-piksel-ui` (bez zależności; ogłaszają zmiany przez `aria-live`). Reguła CSS `[hidden] { display: none !important; }` jest częścią systemu — klasy z `display: flex/grid` nie mogą nadpisać ukrycia.

### 6.13 Stany błędu i ładowania (v1.6)

Reguły: stan nie zmienia rozmiaru; kolor nigdy nie jest jedynym sygnałem (ikona „!” + tekst); ruch skokowy (`steps`), przy `prefers-reduced-motion` bez animacji.

| Stan | Klasa / atrybuty | Specyfikacja |
|---|---|---|
| Błąd pola | `.field.is-error` lub `input[aria-invalid="true"]` + `.field-error` (id w `aria-describedby`) | ramka i cień pola w `--danger` (grubość bez zmian); komunikat pod polem 13/600 w kolorze tekstu z ikoną „!” 18 px na `--danger` (czerwony tekst na papierze miałby 4.2:1) |
| Podpowiedź pola | `.field-hint` | 13 px `--ink-3` |
| Ładowanie przycisku | `.btn.is-loading` + `aria-disabled` + `aria-busy` | patrz §6.1 |
| Wczytywanie listy | `.skel`, `.skel-row`, `.skel-n`, `.skel-av`; kontener `aria-busy="true"` + tekst `.sr-only` „Wczytywanie…” | szkielet z ditheru 4 px w `--line-soft`, wiersze mają docelową wysokość |
| Błąd wczytania | `.load-error` + `role="alert"` | jak pusty stan, lewa krawędź 10 px `--danger`, przycisk „Spróbuj ponownie” (`.btn-compact`), kod błędu w pixel-foncie |
| Błąd w treści | `.callout.callout-danger` | biały z lewą krawędzią 10 px `--danger` i „!”; miętowy callout zostaje dla wskazówek |

```html
<div class="field is-error"><label for="mail">E-mail</label>
  <input id="mail" type="email" aria-invalid="true" aria-describedby="mail-err">
  <p class="field-error" id="mail-err">Dokończ adres e-mail — brakuje domeny, np. @firma.pl.</p></div>
```

### 6.14 Formularze — pozostałe pola (v1.7)

| Pole | Klasa / atrybuty | Specyfikacja |
|---|---|---|
| Lista wyboru | `.field > .select > select` | jak pole tekstowe, wysokość 40 px, pikselowa strzałka `i-chevron-down` po prawej |
| Radio | `.radio > input[type=radio]` | 18 px, pikselowe koło (schodkowe narożniki 4 px), zaznaczenie = kwadrat 6 px `--ink` z żółtą obwódką |
| Przełącznik | `button.switch[role=switch][aria-checked]` + `.switch-track` + `.switch-state` | tor 44×24, suwak 16 px skokowo; włączony = tor `--action`; napis **WŁ / WYŁ** w pixel-foncie (stan nie tylko kolorem). Zmiana działa od razu — w formularzu z „Zapisz” użyj checkboxa |
| Pole wielowierszowe | `.field textarea` + `maxlength` + `data-count` → `.field-count` | min. 96 px, `resize: vertical`; licznik „45 / 300” w pixel-foncie, czerwony przy ≤ 5% |
| Licznik −/+ | `.stepper` z `button[data-step]` i `input[type=number][min][max]` | przyciski 36 px; na granicy zakresu `aria-disabled` |
| Plik | `label.upload[data-max-mb] > input[type=file][accept]` + `ul.file-list[data-files-for]` + `p.field-error[data-upload-error]` | strefa z przerywaną ramką, ikona `i-upload`, „Przeciągnij plik albo wybierz z dysku”; lista plików z `s-scroll`, rozmiarem i usuwaniem `i-trash`; błąd typu/rozmiaru pod strefą |
| Wymagane | `<span class="req" aria-hidden="true">*</span>` w etykiecie + `required` | gwiazdka w `--danger` |
| Zablokowane | `:disabled` | tło `--disabled-bg`, ramka `--disabled-line`, bez cienia + zdanie dlaczego w `.field-hint` |
| Tylko do odczytu | `[readonly]` | tło `--paper`, ramka przerywana, bez cienia; wartość można zaznaczyć i skopiować |

### 6.15 Powiadomienia (v1.7)

| Rodzaj | Klasa | Kiedy | Zachowanie |
|---|---|---|---|
| W treści | `.notice.notice-info/success/warning/error` | stan strony lub sekcji (weryfikacja oferty, wygasające oferty) | zostaje; opcjonalnie `button[data-dismiss]` (`.icon-btn` z `i-close`) i akcje `.notice-actions` (`.btn-compact`) |
| Wyskakujące | `ppToast({status, title, text})` → `.toasts > .notice.toast` | potwierdzenie akcji (zapisano, wysłano) | prawy dolny róg, max ~3 linie; sukces/informacja znikają po 6 s z pauzą po najechaniu i fokusie; ostrzeżenie i błąd zostają do zamknięcia i są ogłaszane przez `role="alert"` |
| Błąd pola | `.field-error` | walidacja | §6.13 |

Anatomia: kafelek 28 px w kolorze statusu z ikoną 24 px → tytuł 15/800 → zdanie `--ink-2` → akcje. Lewa krawędź 10 px w kolorze statusu. `.callout-danger` z v1.6 zostaje dla krótkich ostrzeżeń w treści; nowe ekrany używają `.notice-error`.

### 6.16 Nakładki (v1.7)

| Element | Kod | Zasady |
|---|---|---|
| Okno modalne | `<dialog class="modal" aria-labelledby>` + `.modal-head` (h2 + `.icon-btn[data-dialog-close]`) + `.modal-body` + `.modal-foot`; otwiera `button[data-dialog-open="id"]` | natywny `showModal()`: fokus w środku, Esc i klik w tło zamykają, fokus wraca na przycisk; szerokość do 560 px, cień 6 px, tło przyciemnione ditherem; jedna akcja główna w stopce; tylko dla zadań, które muszą przerwać pracę |
| Szuflada | `<dialog class="drawer" data-drawer-source="id-formularza">` + `[data-drawer-slot]` | od prawej, do 380 px; formularz z `data-drawer-form` przenoszony do szuflady na czas otwarcia (ten sam stan filtrów); „Pokaż N ofert” zamyka szufladę |
| Menu „więcej” | `.menu > button.icon-btn[aria-expanded][aria-controls]` + `ul.menu-list[hidden]` | wzorzec disclosure (nie `role="menu"`); strzałka w dół otwiera i ustawia fokus, strzałki przechodzą, Esc zamyka i wraca fokusem; akcja niszcząca `.is-danger` na końcu za `<hr>` |
| Podpowiedź | `.tip > button[aria-describedby] + .tip-body[role=tooltip]` | po najechaniu i fokusie; Esc chowa; dymek można najechać; max 260 px; tylko dodatkowa informacja — nic, czego nie da się zrobić bez niej |
| Przycisk-ikona | `.icon-btn` (+ `.is-boxed`) | 36×36 px, zawsze z `aria-label` |

### 6.17 Nawigacja mobilna i filtry w szufladzie (v1.7)

- **Nawigacja** < 600 px: `<button class="icon-btn is-boxed nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu">` + `<nav class="site-nav" id="nav" data-collapsible>` — lista pod nagłówkiem, Esc zamyka. Bez `data-collapsible` nawigacja zawija się jak dotąd (dla 2–3 pozycji).
- **Filtry** < 900 px: przycisk `.filters-toggle` (`.btn-secondary.btn-compact` + `i-filter`, opcjonalnie liczba aktywnych filtrów) obok sortowania otwiera `dialog.drawer`; na desktopie panel filtrów zostaje w kolumnie.

### 6.18 Formularz — wzorzec (v1.8)

Przykład: `examples/wzorce.html#formularz`. Kod: `<form data-validate>` + `ui-controls.js`.

| Zasada | Jak |
|---|---|
| Etykieta zawsze nad polem | `.field > label`; placeholder tylko jako przykład wartości („https://”), nigdy zamiast etykiety |
| Pola wymagane | `required` + `<span class="req" aria-hidden="true">*</span>`; gdy wymagane są prawie wszystkie — oznacz opcjonalne słowem „(opcjonalnie)” |
| Kiedy walidować | po opuszczeniu pola (jeśli coś wpisano) i przy wysłaniu / „Dalej”; **nigdy w trakcie pisania** — w trakcie pisania tylko gasimy naprawiony błąd |
| Błąd pola | `.field.is-error` + `.field-error` pod polem + `aria-invalid` + `aria-describedby` (skrypt robi to sam) |
| Treść błędu | co zrobić, nie co jest źle: „Wpisz adres e-mail w formacie nazwa@domena.pl.”, „Wpisz co najmniej 5 znaków (teraz 3).” Własne komunikaty: `data-msg-required`, `-email`, `-minlength`, `-pattern`, `-min`, `-max`, `-match` |
| Podsumowanie błędów | przy wysłaniu z błędami: `.notice-error.error-summary` na górze formularza („Popraw 3 pola, żeby przejść dalej”) z linkami do pól; dostaje fokus i `role="alert"`; miejsce wskazuje `<div data-error-summary>` |
| Ostrzeżenie | `data-warn-empty="…"` → `.field.is-warning` + `.field-warning` (pomarańczowy trójkąt); nie blokuje wysłania |
| Kroki | `data-wizard` + `ol.steps-progress` (zrobione ✓ / bieżący `aria-current="step"` / kolejne przerywane) + `section.wizard-step` + `.wizard-nav` (Wstecz / Dalej / wyślij); „Dalej” sprawdza tylko bieżący krok, fokus przechodzi na nagłówek kroku, zmiana ogłaszana („Krok 2 z 3: Wymagania”). 3–5 kroków; na telefonie widać tylko nazwę bieżącego |
| Po wysłaniu | zdarzenie `pp:valid` → `ppToast({status:'success', …})` albo przejście na stronę potwierdzenia |
| Przycisk wysyłki | zawsze aktywny (błędy pokazuje walidacja); zablokowany tylko z powodem (`.btn-reason`), np. brak CV |

### 6.19 Zaznaczanie wierszy i akcje zbiorcze (v1.8)

`<table id="…" data-selectable>`: pierwsza kolumna `.col-check` z checkboxem w nagłówku (`data-select-all`, stan „częściowo” = `indeterminate`) i w każdym wierszu (`data-select-row` + `aria-label="Zaznacz: <nazwa>"`). Zaznaczony wiersz: `aria-selected="true"`, tło `--row-selected` i lewa krawędź 4 px `--focus`. Pasek `.bulk-bar[data-bulk-for]` pojawia się przy pierwszym zaznaczeniu, przykleja się do dołu ekranu, pokazuje „Zaznaczono 3 oferty” (odmiana w `data-forms`) i 2–3 akcje `.btn-compact` + „Odznacz”. Akcja niszcząca (Usuń) zawsze z oknem potwierdzenia z liczbą pozycji.

### 6.20 Ładowanie i postęp (v1.8)

| Czas oczekiwania | Wskaźnik |
|---|---|
| < 1 s | nic (bez migania) |
| 1–3 s, lista / tabela / karty | szkielet `.skel-row` (§6.13) w docelowej wysokości |
| 1–3 s, jedna akcja | przycisk `.is-loading` (§6.1) albo `.inline-loading` „Zapisywanie…” → `.is-done` „Zapisano” (`role="status"`) |
| > 3 s, znany postęp | `.progress` z procentem: `role="progressbar"` + `aria-valuenow`; `ppProgress(el, 40)` |
| > 3 s, nieznany | `.progress.is-indeterminate` z opisem, co się dzieje |
| minuty | pozwól pracować dalej, wynik jako `ppToast` |
| błąd | `.load-error` z „Spróbuj ponownie” (§6.13) lub `.inline-loading.is-error` |

**Pokaż więcej** zamiast paginacji, gdy użytkownik przegląda (nowe oferty, sklep): `data-page-size="N"` na liście + `.load-more[data-more-for]`; przycisk „Pokaż więcej (4)”, informacja „8 z 12”, fokus przechodzi na pierwszą dołożoną pozycję; filtr i sortowanie wracają do pierwszej porcji. Paginacja (§6.11) zostaje tam, gdzie wraca się do konkretnej strony (ranking, wyniki wyszukiwania).

### 6.21 Wykresy (v1.8)

Kod: `assets/charts.js`; przykład: `examples/wzorce.html#wykresy`. Metoda: najpierw forma, potem kolor; paleta sprawdzona skryptem (`validate_palette.js`: separacja dla daltonizmu, kontrast z tłem, jasność) w trybie jasnym i ciemnym.

| Zadanie danych | Forma | Kod |
|---|---|---|
| jedna liczba + kierunek | kafelek `.stat` (etykieta, wartość w pixel-foncie, zmiana ▲/▼ „vs poprzedni tydzień”, opcjonalna minilinia) | `.stats > .stat` + `.chart-spark[data-chart="spark"]` |
| jedna seria w czasie (dni) | słupki pionowe | `figure.chart[data-chart="columns"]` |
| jedna seria w czasie (tygodnie, trend) | linia 2 px + znacznik ostatniej wartości | `data-chart="line"` |
| ranking kategorii, długie nazwy | słupki poziome, od największego | `data-chart="bars"` |
| części całości, ≤ 4 kategorie | jeden pasek 100% + legenda z % | `data-chart="segments"` |

Dane: `<script type="application/json">{"labels":[…],"values":[…],"unit":"wyświetleń","labelHeader":"Dzień","valueHeader":"Wyświetlenia"}</script>` wewnątrz `figure`, tytuł i podtytuł w `figcaption` (`.chart-title`, `.chart-sub`).

| Token | Jasny | Ciemny | Użycie |
|---|---|---|---|
| `--chart-single` | `#2D5280` | `#A3CCD9` | jedna seria (słupki, linia, ranking, minilinia) — łupkowy, kontrast 8:1 |
| `--chart-1` | `#B36159` terakota | ten sam | pierwsza kategoria (segments) |
| `--chart-2` | `#1BA683` morski | ten sam | druga |
| `--chart-3` | `#A6216E` malinowy | ten sam | trzecia |
| `--chart-4` | `#119955` zielony | ten sam | czwarta |
| `--chart-grid` | `#E6E2CC` | `#2D5280` | linie siatki 1 px |

Zasady: słupki ≤ 24 px, proste narożniki (wyjątek od ogólnej metody wykresów z zaokrąglonym końcem — w systemie nie ma promieni), odstęp 2 px między segmentami, linia 2 px, znacznik 8 px z obwódką w kolorze tła; podpisy tylko przy maksimum i ostatniej wartości, reszta w dymku i w tabeli („Pokaż dane w tabeli” generowana automatycznie); tekst nigdy w kolorze serii; jedna oś Y — dwie miary to dwa wykresy; kolory w stałej kolejności, kolor należy do kategorii, nie do miejsca w rankingu; statusy (§2.7) nie są kolorami serii; więcej niż 4 części → „Inne”. SVG ma `role="img"` i `aria-label` ze streszczeniem (maksimum, ostatnia wartość). Kolory kategorii nie są kolorami pakietów (NES) ani statusów (§2.7) — różnica min. ΔE 10 (decyzja 2026-11-10; wcześniej fiolet/złoto/niebieski mylił się z pakietami Epicki/Legendarny/Rzadki). To jedyna czwórka z palety SNES, która przechodzi wszystkie testy w obu trybach; morski i zielony stoją na pozycjach 2 i 4, a legenda zawsze podaje nazwę.

### 6.23 Koszyk sklepu — złożenie (v1.10)

Koszyk nie jest osobnym komponentem — składa się z klocków systemu (decyzja 2026-11-10): panel `.panel` z licznikiem → wiersze: nazwa + `.tier-tag` w pierwszej linii, `.stepper` (36 px) i cena w pixel-foncie w drugiej → podsumowanie `.facts` (pozycja „Brakuje” w `--danger`) → `.progress` „Masz 59% potrzebnych monet” → przycisk zakupu, zablokowany z powodem (`.btn-reason`), gdy brakuje środków. Przykład: ekran sklepu (S13). Przepis: `screen-recipes.md` „Sklep / koszyk”.

### 6.24 Saldo / portfel — złożenie (v1.11)

Saldo użytkownika (monety, punkty, kredyty) w nagłówku nie jest osobnym komponentem (decyzja 2026-11-10): `.badge.badge-seg` → lewa część: sprite waluty `sprite-sm` + nazwa („Twoje monety”), prawa część: saldo w pixel-foncie 10 px z `aria-live="polite"`, bo zmienia się po zakupie. Stoi w nagłówku obok koszyka; ta sama wartość może się powtórzyć w `.facts` koszyka. Klasa `.wallet` nie istnieje — nie dodawaj własnych stylów poza odstępem sprite’a i fontem salda.

```html
<p class="badge badge-seg"><span style="display:inline-flex;align-items:center;gap:6px"><span class="sprite sprite-sm s-coin" aria-hidden="true"></span>Twoje monety</span><span aria-live="polite" style="font:10px/1 var(--font-pixel)">1 250</span></p>
```

### 6.22 Macierz stanów (v1.8)

Każdy interaktywny komponent ma komplet stanów albo świadome „nie dotyczy”. Rozmiar nigdy się nie zmienia.

| Komponent | Najechanie | Fokus | Wciśnięty / wybrany | Zablokowany | Tylko odczyt | Błąd | Ostrzeżenie | Ładowanie |
|---|---|---|---|---|---|---|---|---|
| Przycisk | krawędź 6 px, −2 px | pierścień wewn. | krawędź 0 / `aria-pressed` | szary + kłódka + powód | — | — | — | `.is-loading` |
| Przycisk-ikona | tło `--paper` + ramka | pierścień wewn. | `aria-expanded` → `--ink` | `aria-disabled` | — | — | — | — |
| Pole / lista / pole wielowierszowe | — | obwódka 3 px + cień `--focus-deco` | — | `:disabled` szare | `[readonly]` przerywana ramka | `.is-error` | `.is-warning` | — |
| Checkbox / radio | — | obwódka 3 px | zaznaczony | `:disabled` | — | `aria-invalid` + błąd grupy | — | — |
| Przełącznik | — | obwódka 3 px | `aria-checked` WŁ | `aria-disabled` | — | — | — | — |
| Zakładki / przyciski sortowania | podkreślenie | obwódka wewn. | `aria-selected` / `aria-pressed` → `--ink` | — | — | — | — | — |
| Wiersz tabeli | `--row-hover` | link w komórce | `aria-selected` + krawędź | — | — | — | wiersz wygasający (krawędź `--danger`) | szkielet |
| Karta / panel listy | podkreślenie nazwy | obwódka linku | — | — | — | — | — | szkielet |
| Plik | ramka ciągła, tło `--paper` | obwódka strefy | `.is-drag` | — | — | `.is-error` | — | `.progress` |
| Powiadomienie | — | przycisk zamknij | — | — | — | `.notice-error` | `.notice-warning` | — |

---

## 6A. Treści i język interfejsu (v1.8)

| Temat | Zasada | Przykład |
|---|---|---|
| Ton | rzeczowo, życzliwie, na „Ty”; bez żartów w błędach i pieniądzach; growy klimat w grafice i nazwach pakietów, nie w komunikatach | „Nie udało się zapisać zmian” — nie „Ups! Game over” |
| Wielkie litery | zdania i etykiety wielką literą tylko na początku; WERSALIKI tylko w badge, nagłówkach tabel i znacznikach (CSS `text-transform`, w treści zwykły zapis) | „Najwyższe widełki”, nie „Najwyższe Widełki” |
| Przyciski | czasownik + obiekt, do ~3 słów; ta sama nazwa akcji w przycisku, oknie i potwierdzeniu | „Wyślij aplikację” → toast „Aplikacja wysłana” |
| Liczby | spacja co 3 cyfry od 10 000 (w pixel-foncie także 1 128), przecinek dziesiętny | 1 128 · 24 500 · 2,4 dnia |
| Kwoty | „22 000–28 000 zł” (półpauza bez spacji), na wąskich listach „22–28 tys.”; zawsze z informacją netto/brutto, B2B/UoP, gdy to istotne | „22 000–28 000 zł netto B2B” |
| Daty | listy: względnie („dodano 2 godz. temu”, „wczoraj”) do 7 dni, potem 12.11.2026; tabele: zawsze dd.mm.rrrr (sortowanie) | „wygasa za 2 dni”, „14.11.2026” |
| Odmiana liczebników | zawsze 3 formy (1 / 2–4 / 5+) przez `data-count-forms` / `data-forms` | 1 oferta · 3 oferty · 5 ofert · 22 oferty |
| Brak danych | słownie zamiast zera: „Widełki nie podane”, w tabeli „—” z `aria-label` | — |
| Błędy | co zrobić + jak; bez „niepoprawny”, „błędny”, bez winy użytkownika; kod błędu na końcu, drobno | „Sprawdź połączenie i spróbuj jeszcze raz. BŁĄD 503” |
| Puste stany | co tu będzie + jedna akcja | „Zapisane oferty pojawią się tutaj. Przeglądaj oferty” |
| Potwierdzenia | czas przeszły, krótko; szczegół w drugim zdaniu | „Zapisano ofertę. Znajdziesz ją w zakładce Zapisane.” |
| Długość | tytuł powiadomienia ≤ 6 słów, treść ≤ 2 zdania; etykieta pola ≤ 4 słowa; badge ≤ 2 słowa | — |
| Słownik | oferta (nie „ogłoszenie” w UI), widełki, aplikacja / aplikować, pakiet (Zwykły / Rzadki / Epicki / Legendarny), pracodawca, kandydat | — |

## 7. Wzorce ekranów

1. **Strona główna katalogu** — okruszki → `h1` + opis → wyszukiwarka główna → siatka paneli kategorii (skrócone, 5–8 pozycji); jeden panel `.is-featured` („Świeżo dodane”).
2. **Kategoria** — okruszki → `h1` + opis + udostępnianie → panel z pełną listą + kolumna paneli powiązanych kategorii (nagłówek, 5 monogramów, „+N”).
3. **Wyniki / wyszukiwarka** — sortowanie → sekcje → karty 2 kol. (desktop) / 1 kol. (mobile) + panel filtrów.
4. **Ranking** — podium + panel listy od miejsca 4 + przełącznik okresu („Ten tydzień / Ogółem”).
5. **Cennik / pakiety** — tiery w kolumnie lub 4 kolumnach, przycisk główny pod rekomendowanym.

**Mobile (< 600 px):** wszystkie siatki → 1 kolumna; panele skrócone do 7 pozycji; wiersz 40 px; podium bez zmian do 360 px; filtry nad wynikami lub w szufladzie (**do zaprojektowania** — brak wzorca w źródłach).

---

## 8. Dostępność

- Kontrast tekstu ≥ 4.5:1, elementów UI ≥ 3:1 — wszystkie tokeny w §2 spełniają (policzone z hex; zmierzyć na implementacji).
- **Fokus zawsze widoczny**: przyciski — pierścień wewnętrzny; pola, linki, checkboxy — `outline: 3px solid var(--focus)` z `outline-offset`.
- Zablokowane akcje: `aria-disabled="true"` + `aria-describedby` z powodem; nie `disabled`.
- Cel dotykowy ≥ 44 px (przyciski), wiersze list 40 px na mobile.
- Ranga i tier: zawsze numer/nazwa obok koloru. Podium w DOM w kolejności 1–2–3.
- Ikony dekoracyjne `aria-hidden="true"`; monogramy z pełną nazwą firmy w tekście obok.
- `prefers-reduced-motion` wyłącza przejścia.
- Liczby w Press Start 2P: zawsze prawdziwy tekst (nie obraz), możliwy do skopiowania i odczytania.
- **Tryb wysokiego kontrastu (Windows, `forced-colors`, v1.7)**: przeglądarka usuwa wtedy cienie i tła, a nasze przyciski rysują ramkę cieniem — dlatego `components.css` dodaje w tym trybie prawdziwe ramki `ButtonText`, zaznaczenia (`aria-pressed`, `aria-selected`, bieżąca strona, checkbox, radio, przełącznik) w kolorze `Highlight`, fokus `Highlight`, a ikony biorą kolor tekstu. Do sprawdzenia na prawdziwym Windowsie (emulacja w Chrome włącza tylko zapytanie `@media`).
- Nakładki: okno i szuflada na natywnym `<dialog>`; podpowiedzi zamykane Esc (WCAG 1.4.13); powiadomienia o błędach ogłaszane `role="alert"`, potwierdzenia przez `aria-live="polite"`; błędy i ostrzeżenia nie znikają same.

---

## 9. Kod

### 9.1 `tokens.css`

```css
/* Panel & Piksel — tokens v1.10 (z design.md §9.1)
 * Tryb ciemny: <html data-theme="dark"> (opt-in). Automatycznie wg systemu: <html data-theme="auto">. */
:root {
  /* kolor — SNES (Jehkoba32) */
  --paper: #F0EDD8;
  --paper-dots: rgba(217, 76, 135, .22);
  --surface: #FFFFFF;
  --ink: #00021C;
  --ink-2: #1C284D;
  --ink-3: #2D5280;
  --on-ink: #F0EDD8;
  --action: #17735F;
  --action-edge: #00021C;
  --on-action: #FFFFFF;
  --highlight: #F7C93E;
  --mint: #96E3C9;
  --link: #2469B3;
  --focus: #2469B3;
  --focus-deco: #0BAFE6;
  --danger: #D9214F;
  --featured: #D94C87;
  --chip: #A3CCD9;
  --chip-more: #F0BB90;
  --btn-secondary-edge: #A3CCD9;
  --line-soft: #A3CCD9;
  --line: var(--ink);            /* v1.6: kolor ramek (osobno od tekstu) */
  --shadow-color: var(--ink);    /* v1.6: kolor twardych cieni */
  --on-light: #00021C;           /* v1.6: tekst na jasnych wypełnieniach (żółty, mięta, złoto…) */
  --row-hover: #F8F6EC;          /* v1.6: tło wiersza tabeli po najechaniu */
  --row-selected: #E4ECFF;       /* v1.8: zaznaczony wiersz (z lewą krawędzią --focus) */
  /* v1.7: statusy (informacja / sukces / ostrzeżenie / błąd) — kolor kafelka ikony i lewej krawędzi + kolor znaku na nim */
  --status-info: #2469B3;    --on-status-info: #FFFFFF;     /* 5.6:1 */
  --status-success: #17735F; --on-status-success: #FFFFFF;  /* 5.7:1 */
  --status-warning: #E45C10; --on-status-warning: #00021C;  /* NES; 5.7:1, krawędź 3.6:1 na bieli */
  --status-error: var(--danger); --on-status-error: #FFFFFF; /* 4.9:1 */
  /* v1.10: wykresy — kategorie w stałej kolejności (bez kolorów pakietów i statusów); ten sam zestaw w obu trybach,
     sprawdzony validate_palette.js (CVD, kontrast, jasność) na #FFFFFF i #1C284D. Jedna seria: --chart-single. */
  --chart-1: #B36159; --chart-2: #1BA683; --chart-3: #A6216E; --chart-4: #119955;
  --chart-single: #2D5280;
  --chart-grid: #E6E2CC; --chart-axis: var(--ink-3);
  /* v1.7: warstwy */
  --z-sticky: 10; --z-dropdown: 100; --z-drawer: 200; --z-modal: 300; --z-toast: 400; --z-tooltip: 500;
  /* v1.7: ruch — skokowy, krótki */
  --motion-fast: 60ms;   /* przyciski, przełączniki */
  --motion-base: 120ms;  /* menu, podpowiedzi, dymki */
  --motion-slow: 200ms;  /* okno, szuflada, powiadomienie */
  --ease-steps: steps(3, end);
  /* v1.7: punkty przełamania (do @media trzeba wpisać liczbę — CSS nie przyjmuje tu zmiennych) */
  --bp-sm: 600px; --bp-md: 900px; --bp-lg: 1200px;
  --disabled-bg: #BCBCBC;   /* NES */
  --disabled-ink: #1C284D;
  --disabled-line: #2D5280;
  --avatar-1: #17735F; --avatar-2: #2469B3; --avatar-3: #993649;
  --avatar-4: #732866; --avatar-5: #00021C; --avatar-6: #D9214F;

  /* akcenty NES — tylko ranking i pakiety */
  --podium: #0000BC;
  --gold: #F8B800;
  --silver: #BCBCBC;
  --bronze: #E45C10;
  --tier-legendary: #AC7C00;
  --tier-epic: #6844FC;
  --tier-rare: #0078F8;
  --tier-common: #7C7C7C;

  /* typografia */
  --font-sans: "Archivo", system-ui, sans-serif;
  --font-pixel: "Press Start 2P", ui-monospace, monospace;

  /* odstępy */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px;

  /* kształt i głębia */
  --border: 2px solid var(--line);
  --shadow-sm: 2px 2px 0 var(--shadow-color);
  --shadow-md: 4px 4px 0 var(--shadow-color);
  --shadow-lg: 6px 6px 0 var(--shadow-color);
  --notch: polygon(0 2px, 2px 2px, 2px 0, calc(100% - 2px) 0, calc(100% - 2px) 2px, 100% 2px,
                   100% calc(100% - 2px), calc(100% - 2px) calc(100% - 2px), calc(100% - 2px) 100%,
                   2px 100%, 2px calc(100% - 2px), 0 calc(100% - 2px));
  --btn-h: 44px;
  --row-h: 32px;
  --motion: 60ms;
}
@media (max-width: 600px) { :root { --row-h: 40px; } }
@media (prefers-reduced-motion: reduce) { :root { --motion: 0ms; --motion-fast: 0ms; --motion-base: 0ms; --motion-slow: 0ms; } }

/* ---------- tryb ciemny (v1.6) — te same komponenty, inne tokeny ----------
   Tokeny złożone (--border, --shadow-*) są powtórzone, bo custom properties liczą się tam, gdzie je zadeklarowano. */
[data-theme="dark"] {
  --paper: #00021C; --paper-dots: rgba(217, 76, 135, .18);
  --surface: #1C284D;
  --ink: #F0EDD8; --ink-2: #A3CCD9; --ink-3: #96E3C9; --on-ink: #00021C;
  --link: #0BAFE6; --focus: #F7C93E; --focus-deco: #2469B3;
  --danger: #F27961;
  --chip: #2D5280; --line-soft: #2D5280; --btn-secondary-edge: #2D5280;
  --line: #F0EDD8; --shadow-color: #2469B3; --row-hover: #2D5280; --row-selected: #1F3A6B;
  --avatar-5: #2D5280;
  --status-info: #0BAFE6; --on-status-info: #00021C;
  --status-success: #96E3C9; --on-status-success: #00021C;
  --status-warning: #E45C10; --on-status-warning: #00021C;
  --status-error: #F27961; --on-status-error: #00021C;
  --chart-single: #A3CCD9; --chart-grid: #2D5280;
  --tier-legendary: #F8B800; --tier-epic: #9878F8; --tier-rare: #3CBCFC; --tier-common: #BCBCBC;
  --border: 2px solid var(--line);
  --shadow-sm: 2px 2px 0 var(--shadow-color); --shadow-md: 4px 4px 0 var(--shadow-color); --shadow-lg: 6px 6px 0 var(--shadow-color);
  color-scheme: dark;
}
@media (prefers-color-scheme: dark) {
  [data-theme="auto"] {
    --paper: #00021C; --paper-dots: rgba(217, 76, 135, .18);
    --surface: #1C284D;
    --ink: #F0EDD8; --ink-2: #A3CCD9; --ink-3: #96E3C9; --on-ink: #00021C;
    --link: #0BAFE6; --focus: #F7C93E; --focus-deco: #2469B3;
    --danger: #F27961;
    --chip: #2D5280; --line-soft: #2D5280; --btn-secondary-edge: #2D5280;
    --line: #F0EDD8; --shadow-color: #2469B3; --row-hover: #2D5280; --row-selected: #1F3A6B;
    --avatar-5: #2D5280;
    --status-info: #0BAFE6; --on-status-info: #00021C;
    --status-success: #96E3C9; --on-status-success: #00021C;
    --status-warning: #E45C10; --on-status-warning: #00021C;
    --status-error: #F27961; --on-status-error: #00021C;
    --chart-single: #A3CCD9; --chart-grid: #2D5280;
    --tier-legendary: #F8B800; --tier-epic: #9878F8; --tier-rare: #3CBCFC; --tier-common: #BCBCBC;
    --border: 2px solid var(--line);
    --shadow-sm: 2px 2px 0 var(--shadow-color); --shadow-md: 4px 4px 0 var(--shadow-color); --shadow-lg: 6px 6px 0 var(--shadow-color);
    color-scheme: dark;
  }
}
```

### 9.2 `components.css`

```css
/* Panel & Piksel — components v1.11 (z design.md §9.2) */
/* ---------- baza ---------- */
body { margin: 0; background: var(--paper); color: var(--ink); font: 400 16px/24px var(--font-sans); }
.bg-dots { background-image: radial-gradient(var(--paper-dots) 1.5px, transparent 1.6px); background-size: 16px 16px; }
[hidden] { display: none !important; } /* klasy z display:flex/grid nie mogą nadpisać hidden */
.sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; border: 0; overflow: hidden; clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap; }

/* ---------- przycisk ---------- */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  box-sizing: border-box; height: var(--btn-h); padding: 0 18px 4px;
  font: 700 15px/1 var(--font-sans); white-space: nowrap; vertical-align: middle;
  border: 0; cursor: pointer; clip-path: var(--notch); text-decoration: none;
  transition: transform var(--motion), box-shadow var(--motion);
}
.btn-primary   { background: var(--action);  color: var(--on-action); box-shadow: inset 0 -4px 0 var(--action-edge), inset 0 0 0 2px var(--line); }
.btn-secondary { background: var(--surface); color: var(--ink);       box-shadow: inset 0 -4px 0 var(--btn-secondary-edge), inset 0 0 0 2px var(--line); }
.btn-full { width: 100%; }

.btn:not([aria-disabled="true"]):not(.is-pressed):not(:active):hover { transform: translateY(-2px); padding-bottom: 6px; }
.btn-primary:not([aria-disabled="true"]):not(.is-pressed):not(:active):hover   { box-shadow: inset 0 -6px 0 var(--action-edge), inset 0 0 0 2px var(--line); }
.btn-secondary:not([aria-disabled="true"]):not(.is-pressed):not(:active):hover { box-shadow: inset 0 -6px 0 var(--btn-secondary-edge), inset 0 0 0 2px var(--line); }

.btn:active, .btn.is-pressed, .btn[aria-pressed="true"] { padding: 4px 18px 0; transform: none; box-shadow: inset 0 0 0 2px var(--line); }

.btn:focus-visible {
  outline: none; /* clip-path obcina outline — rysujemy pierścień do środka */
  box-shadow: inset 0 0 0 2px var(--line), inset 0 0 0 5px var(--focus), inset 0 0 0 7px var(--surface) !important;
}

.btn:disabled, .btn[aria-disabled="true"],
.btn[aria-disabled="true"]:active {
  background: var(--disabled-bg); color: var(--disabled-ink); cursor: not-allowed;
  padding: 0 18px; transform: none; box-shadow: inset 0 0 0 2px var(--disabled-line);
}
.btn-reason { margin: 8px 0 0; font: 600 13px var(--font-sans); color: var(--ink-2); }

/* pikselowa kłódka 8×9, piksel 2 px */
.lock { position: relative; display: inline-block; flex: none; width: 16px; height: 18px; }
.lock::before {
  content: ""; position: absolute; left: 0; top: 0; width: 2px; height: 2px;
  box-shadow: 4px 0 currentColor, 6px 0 currentColor, 8px 0 currentColor, 10px 0 currentColor,
    2px 2px currentColor, 12px 2px currentColor, 2px 4px currentColor, 12px 4px currentColor,
    2px 6px currentColor, 12px 6px currentColor,
    0 8px currentColor, 2px 8px currentColor, 4px 8px currentColor, 6px 8px currentColor, 8px 8px currentColor, 10px 8px currentColor, 12px 8px currentColor, 14px 8px currentColor,
    0 10px currentColor, 2px 10px currentColor, 4px 10px currentColor, 6px 10px currentColor, 8px 10px currentColor, 10px 10px currentColor, 12px 10px currentColor, 14px 10px currentColor,
    0 12px currentColor, 2px 12px currentColor, 4px 12px currentColor, 10px 12px currentColor, 12px 12px currentColor, 14px 12px currentColor,
    0 14px currentColor, 2px 14px currentColor, 4px 14px currentColor, 10px 14px currentColor, 12px 14px currentColor, 14px 14px currentColor,
    0 16px currentColor, 2px 16px currentColor, 4px 16px currentColor, 6px 16px currentColor, 8px 16px currentColor, 10px 16px currentColor, 12px 16px currentColor, 14px 16px currentColor;
}

/* ---------- badge, chip, licznik ---------- */
.badge { display: inline-flex; align-items: center; padding: 5px 8px; font: 700 12px/1 var(--font-sans); letter-spacing: .3px; text-transform: uppercase; background: var(--surface); border: var(--border); box-shadow: var(--shadow-sm); }
.badge-new { background: var(--highlight); color: var(--on-light); }
.badge-sm { font-size: 10px; padding: 3px 6px; box-shadow: none; }
.badge-seg { padding: 0; }
.badge-seg > span { padding: 5px 8px; }
.badge-seg > span + span { background: var(--ink); color: var(--on-ink); }

.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { display: inline-block; padding: 6px 8px; font: 600 13px/1 var(--font-sans); color: var(--ink); background: var(--chip); clip-path: var(--notch); }
.chip-more { display: inline-grid; place-items: center; width: 32px; height: 32px; box-sizing: border-box; font: 700 12px var(--font-sans); color: var(--on-light); background: var(--chip-more); border: var(--border); }

.count { display: inline-block; padding: 7px 6px 6px; font: 10px/1 var(--font-pixel); letter-spacing: 1px; background: var(--ink); color: var(--on-ink); }

/* ---------- awatar / monogram ---------- */
.avatar { display: inline-grid; place-items: center; flex: none; width: 20px; height: 20px; font: 7px/1 var(--font-pixel); color: #fff; background: var(--av, var(--avatar-1)); }
.avatar-xl { width: 56px; height: 56px; font-size: 14px; border: var(--border); box-sizing: border-box; }

/* ---------- panel listy ---------- */
.panel { min-width: 0; padding: 16px 16px 20px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-lg); }
.panel.is-featured { box-shadow: 6px 6px 0 var(--featured); }
.panel-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.panel-head h2 { margin: 0; font: 900 18px/28px var(--font-sans); letter-spacing: -.45px; }
.panel-motto { margin: 2px 0 8px; font-size: 14px; font-style: italic; color: var(--ink-3); }
.list { list-style: none; margin: 8px 0 0; padding: 0; }
.list a { display: flex; align-items: center; gap: 8px; height: var(--row-h); color: var(--ink); text-decoration: none; font: 600 14px/20px var(--font-sans); }
.list a:hover .list-name { text-decoration: underline; }
.list a:focus-visible { outline: 3px solid var(--focus); outline-offset: 1px; }
.list-n { flex: none; width: 22px; text-align: right; font: 500 12px var(--font-sans); color: var(--ink-3); }
.list-name { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.list-value { flex: none; font: 10px/1 var(--font-pixel); letter-spacing: .5px; color: var(--ink-2); }
.list .badge-sm { margin-left: auto; }
.panel-more { display: block; margin-top: 10px; padding-top: 12px; text-align: center; border-top: 2px dashed var(--line-soft); font: 600 14px var(--font-sans); letter-spacing: .35px; color: var(--ink-3); text-decoration: none; }

/* ---------- karta ---------- */
.card { display: flex; gap: 16px; min-width: 0; padding: 16px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-md); }
.card-body { flex: 1; min-width: 0; }
.card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
.card-head h3 { margin: 0; font: 800 18px/24px var(--font-sans); }
.card-sub { margin: 4px 0 8px; font-size: 14px; color: var(--ink-2); }
.amount { margin: 0 0 10px; font: 12px/1.6 var(--font-pixel); }
.amount small { font: 600 12px var(--font-sans); color: var(--ink-3); }
.amount.is-empty { font: italic 14px var(--font-sans); color: var(--ink-3); }

/* ---------- filtry i formularze ---------- */
.panel-filters { padding: 16px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-md); }
.panel-filters h2 { margin: 0 0 10px; font: 900 18px/28px var(--font-sans); letter-spacing: -.45px; }
.panel-filters .btn-full { margin-top: 12px; }
.field input { box-sizing: border-box; width: 100%; padding: 8px 10px; font: 400 14px var(--font-sans); background: var(--surface); border: var(--border); border-radius: 0; box-shadow: var(--shadow-sm); }
.field input:focus { outline: 3px solid var(--focus); outline-offset: 2px; box-shadow: 3px 3px 0 var(--focus-deco); }
fieldset { margin: 14px 0 0; padding: 10px 0 0; border: 0; border-top: 2px solid var(--line-soft); }
legend { padding: 0; font: 800 14px var(--font-sans); }
.checkbox { display: flex; align-items: center; gap: 8px; margin: 6px 0; font-size: 14px; }
.checkbox input { appearance: none; display: grid; place-items: center; width: 16px; height: 16px; margin: 0; background: var(--surface); border: var(--border); }
.checkbox input:checked { background: var(--ink); }
.checkbox input:checked::after { content: ""; width: 6px; height: 6px; background: var(--highlight); }
.checkbox input:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }

/* ---------- podium ---------- */
.podium { display: grid; grid-template-columns: repeat(3, 1fr); align-items: end; gap: 10px; margin: 0; padding: 20px 14px 0; list-style: none; color: #fff; background: var(--podium); border: var(--border); box-shadow: var(--shadow-lg); }
.podium li { display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center; font-size: 13px; }
.podium-2 { order: -1; }
.podium-pts { font: 12px var(--font-pixel); }
.podium-1 .podium-pts { color: var(--gold); }
.podium-step { display: grid; place-items: center; width: 100%; font: 20px var(--font-pixel); color: var(--on-light); border: var(--border); border-bottom: 0; box-sizing: border-box; }
.podium-1 .podium-step { height: 96px; background: var(--gold); }
.podium-2 .podium-step { height: 64px; background: var(--silver); }
.podium-3 .podium-step { height: 44px; background: var(--bronze); }

/* ---------- tiery ---------- */
.tier { display: grid; grid-template-columns: 1fr auto; gap: 2px 12px; padding: 10px 12px; background: var(--surface); border: var(--border); border-left-width: 10px; box-shadow: var(--shadow-sm); }
.tier-name { font: 900 16px var(--font-sans); }
.tier-price { grid-row: span 2; font: 12px/1.8 var(--font-pixel); }
.tier-desc { font-size: 13px; color: var(--ink-2); }
.tier-legendary { border-left-color: var(--tier-legendary); }
.tier-epic      { border-left-color: var(--tier-epic); }
.tier-rare      { border-left-color: var(--tier-rare); }
.tier-common    { border-left-color: var(--tier-common); }
/* kompaktowy znacznik tieru — do kart, wierszy tabeli i koszyka */
.tier-tag { display: inline-flex; align-items: center; height: 24px; padding: 0 8px; box-sizing: border-box; font: 700 12px/1 var(--font-sans); letter-spacing: .3px; text-transform: uppercase; white-space: nowrap; color: var(--ink); background: var(--surface); border: var(--border); border-left-width: 10px; }
.tier-tag.tier-legendary { border-left-color: var(--tier-legendary); }
.tier-tag.tier-epic      { border-left-color: var(--tier-epic); }
.tier-tag.tier-rare      { border-left-color: var(--tier-rare); }
.tier-tag.tier-common    { border-left-color: var(--tier-common); }

/* ---------- detale ---------- */
.dither { height: 16px; margin: 4px 0 16px; border-top: 8px solid var(--action); background: conic-gradient(var(--action) 25%, transparent 0 50%, var(--action) 0 75%, transparent 0) 0 0 / 8px 8px; }
.list-square { list-style: none; margin: 0; padding: 0; }
.list-square li { position: relative; margin: 6px 0; padding-left: 18px; }
.list-square li::before { content: ""; position: absolute; left: 0; top: .55em; width: 6px; height: 6px; background: var(--action); }
.pixel-art { image-rendering: pixelated; }

/* ========== v1.1 — elementy ekranu ========== */

/* ---------- kontener i nagłówek strony ---------- */
.container { max-width: 1216px; margin: 0 auto; padding: 0 24px; }
@media (max-width: 600px) { .container { padding: 0 16px; } }
.site-header { background: var(--paper); border-bottom: var(--border); }
.site-header .container { display: flex; align-items: center; gap: 24px; min-height: 72px; flex-wrap: wrap; padding-top: 8px; padding-bottom: 8px; }
.logo { font: 14px/1 var(--font-pixel); color: var(--ink); text-decoration: none; letter-spacing: 1px; }
.logo span { color: var(--action); }
.site-nav { display: flex; gap: 20px; }
.site-nav a { font: 700 15px var(--font-sans); color: var(--ink); text-decoration: none; padding: 4px 0; border-bottom: 2px solid transparent; }
.site-nav a:hover, .site-nav a[aria-current="page"] { border-bottom-color: var(--ink); }
.site-nav a:focus-visible, .logo:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.site-header .search-main { margin-left: auto; min-width: 280px; flex: 0 1 420px; }

/* wyszukiwarka główna: pole + przycisk w jednej ramce */
.search-main { display: flex; border: var(--border); box-shadow: 6px 6px 0 var(--focus-deco); background: var(--surface); }
.search-main input { flex: 1; min-width: 0; height: 44px; padding: 0 12px; border: 0; font: 400 15px var(--font-sans); background: transparent; color: var(--ink); }
.search-main input:focus { outline: 3px solid var(--focus); outline-offset: -3px; }
.search-main button { width: 48px; border: 0; border-left: var(--border); background: var(--ink); color: var(--on-ink); font: 14px var(--font-pixel); cursor: pointer; }
.search-main button:focus-visible { outline: 3px solid var(--focus); outline-offset: -5px; }

/* ---------- okruszki i nagłówek treści ---------- */
.breadcrumbs { display: flex; flex-wrap: wrap; gap: 6px; margin: 16px 0 0; padding: 0; list-style: none; font-size: 14px; color: var(--ink-3); }
.breadcrumbs li + li::before { content: "/"; margin-right: 6px; color: var(--ink-3); }
.breadcrumbs a { color: var(--link); }
.page-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px; margin: 8px 0 24px; }
.page-head h1 { margin: 0; font: 900 24px/32px var(--font-sans); letter-spacing: -.6px; }
.page-head p { margin: 4px 0 0; max-width: 720px; color: var(--ink-2); }
.display { font: 900 40px/44px var(--font-sans); letter-spacing: -1px; margin: 0; }
.mark { background: var(--mint); color: var(--on-light); padding: 0 .15em; }

/* ---------- siatki ekranów ---------- */
.grid-panels { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 28px; align-items: start; }
@media (max-width: 1200px) { .grid-panels { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 900px)  { .grid-panels { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 600px)  { .grid-panels { grid-template-columns: 1fr; } }
.layout-main-side { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 28px; align-items: start; }
.layout-results { display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 28px; align-items: start; }
@media (max-width: 900px) { .layout-main-side, .layout-results { grid-template-columns: 1fr; } .layout-results .panel-filters { order: -1; } }
.stack { display: grid; gap: 20px; }

/* ---------- zakładki / przełącznik okresu ---------- */
.tabs { display: inline-flex; max-width: 100%; overflow-x: auto; border: var(--border); background: var(--surface); box-shadow: var(--shadow-sm); }
.tabs button, .tabs a { flex: none; height: 36px; padding: 0 14px; border: 0; background: transparent; font: 700 14px var(--font-sans); color: var(--ink); cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; }
.tabs > * + * { border-left: var(--border); }
.tabs [aria-selected="true"], .tabs [aria-current="page"] { background: var(--ink); color: var(--on-ink); }
.tabs button:focus-visible, .tabs a:focus-visible { outline: 3px solid var(--focus); outline-offset: -5px; }

/* ---------- tabela danych ---------- */
.table-wrap { position: relative; overflow-x: auto; background: var(--surface); border: var(--border); box-shadow: var(--shadow-lg); }
.table { width: 100%; border-collapse: collapse; font: 400 14px/20px var(--font-sans); }
.table th { position: sticky; top: 0; height: 40px; padding: 0 12px; text-align: left; background: var(--paper); border-bottom: var(--border); font: 800 12px var(--font-sans); letter-spacing: .3px; text-transform: uppercase; white-space: nowrap; }
.table td { height: 44px; padding: 0 12px; border-bottom: 2px solid var(--paper); vertical-align: middle; }
.table tbody tr:last-child td { border-bottom: 0; }
.table tbody tr:hover { background: var(--row-hover); }
.table .num { text-align: right; font: 10px/1 var(--font-pixel); letter-spacing: .5px; white-space: nowrap; }
.table th.num { font: 800 12px var(--font-sans); }
.table .name { font-weight: 600; }
.table .name a { color: var(--ink); text-decoration: none; }
.table .name a:hover { text-decoration: underline; }
.table .name a:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.table .cell-entity { display: flex; align-items: center; gap: 8px; }
/* sortowanie: .sort = przycisk (TYLKO z działającym skryptem, np. table-sort.js);
   .sorted = statyczny znacznik kolejności, gdy tabeli nie da się sortować (np. ranking).
   Kierunek zawsze w aria-sort na <th>. */
.sort { all: unset; cursor: pointer; display: inline-flex; gap: 6px; align-items: center; }
/* cała komórka nagłówka jest polem kliknięcia (th ma padding 0 12px i 40 px wysokości) */
th > .sort { box-sizing: border-box; display: flex; width: calc(100% + 24px); min-height: 40px; margin: 0 -12px; padding: 0 12px; }
th.num > .sort { justify-content: flex-end; }
.sort::after { content: "◆"; font-size: 8px; color: var(--ink-3); }
th[aria-sort="ascending"] .sort::after, .sort[aria-sort="ascending"]::after { content: "▲"; color: var(--ink); }
th[aria-sort="descending"] .sort::after, .sort[aria-sort="descending"]::after { content: "▼"; color: var(--ink); }
.sort:hover { text-decoration: underline; text-underline-offset: 3px; }
.sort:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.sorted { display: inline-flex; gap: 6px; align-items: center; cursor: default; }
.sorted::after { content: "▼"; font-size: 8px; color: var(--ink); }
th[aria-sort="ascending"] .sorted::after { content: "▲"; }
/* miejsce w rankingu: kwadrat z numerem, top 3 w kolorach NES */
.rank { display: inline-grid; place-items: center; min-width: 28px; padding: 0 4px; height: 28px; font: 10px/1 var(--font-pixel); border: var(--border); background: var(--surface); box-sizing: border-box; }
.rank-1 { background: var(--gold); } .rank-2 { background: var(--silver); } .rank-3 { background: var(--bronze); }
.rank-1, .rank-2, .rank-3 { color: var(--on-light); }
/* zmiana wartości */
.delta-up::before { content: "▲ "; color: var(--action); } .delta-down::before { content: "▼ "; color: var(--danger); }

/* ---------- paginacja ---------- */
.pagination { display: flex; flex-wrap: wrap; gap: 8px; margin: 24px 0 0; padding: 0; list-style: none; }
.pagination a, .pagination span { display: inline-grid; place-items: center; min-width: 36px; height: 36px; padding: 0 8px; box-sizing: border-box; font: 10px/1 var(--font-pixel); color: var(--ink); text-decoration: none; background: var(--surface); border: var(--border); box-shadow: var(--shadow-sm); }
.pagination [aria-current="page"] { background: var(--ink); color: var(--on-ink); box-shadow: none; }
.pagination a:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.pagination .gap { border: 0; box-shadow: none; background: transparent; }
.pagination [aria-disabled="true"] { color: var(--ink-3); border-color: var(--ink-3); box-shadow: none; cursor: not-allowed; }

/* ---------- callout, pusty stan, sekcje ---------- */
.callout { padding: 14px 16px; background: var(--mint); border: var(--border); color: var(--on-light); }
.callout strong { font-weight: 800; }
.empty { display: grid; justify-items: center; gap: 12px; padding: 40px 24px; text-align: center; background: var(--surface); border: var(--border); box-shadow: var(--shadow-lg); }
.empty h2 { margin: 0; font: 900 24px/32px var(--font-sans); letter-spacing: -.6px; }
.empty p { margin: 0; max-width: 46ch; color: var(--ink-2); }
.empty-art { width: 96px; height: 96px; image-rendering: pixelated; }
.section { margin: 40px 0; }
.section-title { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; margin: 0 0 16px; }
.section-title h2 { margin: 0; font: 900 18px/28px var(--font-sans); letter-spacing: -.45px; }

/* ---------- opisy / listy definicji (szczegóły encji) ---------- */
.facts { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0; margin: 0; border: var(--border); background: var(--surface); }
.facts div { padding: 10px 12px; border-right: 2px solid var(--paper); border-bottom: 2px solid var(--paper); }
.facts dt { font: 800 11px var(--font-sans); letter-spacing: .3px; text-transform: uppercase; color: var(--ink-3); }
.facts dd { margin: 4px 0 0; font: 600 15px var(--font-sans); }
.facts dd.num { font: 12px/1.6 var(--font-pixel); }
.prose { max-width: 70ch; }
.prose h2 { font: 900 18px/28px var(--font-sans); letter-spacing: -.45px; margin: 24px 0 8px; }
.prose p, .prose li { color: var(--ink-2); }

/* ---------- stopka ---------- */
.site-footer { margin-top: 64px; border-top: var(--border); padding: 24px 0 40px; font-size: 14px; color: var(--ink-2); }
.site-footer a { color: var(--link); }

/* ========== v1.6 — decyzje z dokumentacji komponentów (2026-11-10) ========== */

/* ---------- przycisk kompaktowy 36 px: przycisk powtarzany w każdej pozycji listy (stopka karty, wiersz tabeli, koszyk) ---------- */
.btn.btn-compact { height: 36px; padding: 0 14px 4px; font-size: 14px; }
.btn.btn-compact:not([aria-disabled="true"]):not(.is-pressed):not(:active):hover { padding-bottom: 6px; }
.btn.btn-compact:active, .btn.btn-compact.is-pressed, .btn.btn-compact[aria-pressed="true"] { padding: 4px 14px 0; }
.btn.btn-compact[aria-disabled="true"] { padding: 0 14px; }
.card-foot { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 12px; padding-top: 12px; border-top: 2px dashed var(--line-soft); font-size: 13px; color: var(--ink-3); }

/* ---------- sortowanie listy = grupa przycisków przełączających w wyglądzie .tabs ----------
   kontener: role group + aria-label; przyciski: aria-pressed (wzór w design.md §6.12).
   Zakładki (role tab + aria-selected) tylko gdy przełączają panele treści. */
.tabs [aria-pressed="true"] { background: var(--ink); color: var(--on-ink); }

/* ---------- kwota w wierszu listy: pełna na desktopie, skrócona < 600 px ----------
   wewnątrz .list-value: .amt-full (pełna) + .amt-short z aria-hidden (skrót „18–24 tys.”); wzór w design.md §6.5 */
.amt-short { display: none; }
@media (max-width: 600px) {
  .amt-short { display: inline; }
  .amt-full { position: absolute; width: 1px; height: 1px; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap; }
}

/* ---------- stany: błąd pola ---------- */
.field label { display: block; margin: 0 0 6px; font: 700 14px var(--font-sans); }
.field.is-error input, .field input[aria-invalid="true"] { border-color: var(--danger); box-shadow: 2px 2px 0 var(--danger); }
.field-error { display: flex; gap: 8px; align-items: flex-start; margin: 8px 0 0; font: 600 13px/18px var(--font-sans); color: var(--ink); }
.field-error::before { content: "!"; flex: none; display: grid; place-items: center; width: 18px; height: 18px; font: 10px/1 var(--font-pixel); color: #fff; background: var(--danger); clip-path: var(--notch); }
.field-hint { margin: 6px 0 0; font-size: 13px; color: var(--ink-3); }

/* ---------- stany: ładowanie przycisku (rozmiar bez zmian; aria-disabled + aria-busy) ---------- */
.btn.is-loading { position: relative; color: transparent !important; cursor: progress; padding: 4px 18px 0; transform: none; }
.btn-compact.is-loading { padding: 4px 14px 0; }
.btn-primary.is-loading[aria-disabled="true"] { background: var(--action); box-shadow: inset 0 0 0 2px var(--line); }
.btn-secondary.is-loading[aria-disabled="true"] { background: var(--surface); box-shadow: inset 0 0 0 2px var(--line); }
.btn.is-loading::after { content: ""; position: absolute; left: 50%; top: calc(50% - 2px); width: 4px; height: 4px; margin-left: -14px;
  background: var(--on-action); box-shadow: 12px 0 0 0 var(--on-action), 24px 0 0 0 var(--on-action); animation: pp-dots 900ms steps(1) infinite; }
.btn-secondary.is-loading::after { background: var(--ink); box-shadow: 12px 0 0 0 var(--ink), 24px 0 0 0 var(--ink); }
@keyframes pp-dots { 0% { opacity: 1; } 33% { opacity: .35; } 66% { opacity: .7; } }

/* ---------- stany: szkielet wczytywania (dither 4 px) ---------- */
.skel { display: block; height: 12px; background: conic-gradient(var(--line-soft) 25%, transparent 0 50%, var(--line-soft) 0 75%, transparent 0) 0 0 / 4px 4px; animation: pp-skel 600ms steps(2) infinite; }
@keyframes pp-skel { to { background-position: 4px 0; } }
.skel-row { display: flex; align-items: center; gap: 8px; height: var(--row-h); }
.skel-n { flex: none; width: 22px; height: 10px; }
.skel-av { flex: none; width: 20px; height: 20px; }
@media (prefers-reduced-motion: reduce) { .btn.is-loading::after, .skel { animation: none; } }

/* ---------- stany: błąd wczytania i komunikat błędu w treści ---------- */
.load-error { display: grid; gap: 10px; justify-items: start; padding: 16px; background: var(--surface); border: var(--border); border-left: 10px solid var(--danger); box-shadow: var(--shadow-lg); }
.load-error h2, .load-error h3 { margin: 0; font: 900 18px/24px var(--font-sans); }
.load-error p { margin: 0; color: var(--ink-2); font-size: 14px; }
.load-error .code { font: 10px/1 var(--font-pixel); color: var(--ink-3); }
.callout.callout-danger { background: var(--surface); color: var(--ink); border-left: 10px solid var(--danger); }
.callout-danger strong::before { content: "! "; font-family: var(--font-pixel); font-size: 11px; color: var(--danger); }

/* ========== v1.7 — statusy, formularze, nakładki, nawigacja mobilna, wysoki kontrast ========== */

/* ---------- przycisk-ikona (zamknij, więcej, menu): kwadrat 36 px ---------- */
.icon-btn { display: inline-grid; place-items: center; flex: none; width: 36px; height: 36px; padding: 0; color: var(--ink); background: transparent; border: 2px solid transparent; cursor: pointer; clip-path: var(--notch); }
.icon-btn:hover { background: var(--paper); border-color: var(--line); }
.icon-btn:focus-visible { outline: 3px solid var(--focus); outline-offset: -5px; }
.icon-btn.is-boxed { background: var(--surface); border-color: var(--line); box-shadow: inset 0 -3px 0 var(--btn-secondary-edge); }
.icon-btn[aria-expanded="true"] { background: var(--ink); color: var(--on-ink); }
.btn .icon { margin-left: -4px; }

/* ---------- powiadomienia: w treści (.notice) i wyskakujące (.toast) ---------- */
.notice { display: grid; grid-template-columns: auto 1fr auto; gap: 4px 12px; align-items: start; padding: 12px 12px 12px 14px; color: var(--ink);
  background: var(--surface); border: var(--border); border-left: 10px solid var(--st, var(--status-info)); }
.notice-icon { display: grid; place-items: center; width: 28px; height: 28px; color: var(--on-st, var(--on-status-info)); background: var(--st, var(--status-info)); clip-path: var(--notch); }
.notice-icon .icon { width: 24px; height: 24px; }
.notice-body { min-width: 0; padding-top: 3px; font-size: 14px; line-height: 20px; }
.notice-title { display: block; font: 800 15px/20px var(--font-sans); }
.notice-body p { margin: 2px 0 0; color: var(--ink-2); }
.notice-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.notice > .icon-btn { margin: -6px -6px 0 0; }
.notice-info    { --st: var(--status-info);    --on-st: var(--on-status-info); }
.notice-success { --st: var(--status-success); --on-st: var(--on-status-success); }
.notice-warning { --st: var(--status-warning); --on-st: var(--on-status-warning); }
.notice-error   { --st: var(--status-error);   --on-st: var(--on-status-error); }
.toasts { position: fixed; z-index: var(--z-toast); right: 16px; bottom: 16px; display: grid; gap: 12px; width: min(400px, calc(100vw - 32px)); margin: 0; padding: 0; list-style: none; }
.toast { box-shadow: var(--shadow-md); animation: pp-toast-in var(--motion-slow) var(--ease-steps); }
@keyframes pp-toast-in { from { transform: translateY(12px); opacity: 0; } }

/* ---------- formularze: lista wyboru, radio, przełącznik, pole wielowierszowe, licznik, plik ---------- */
.field textarea, .field select { box-sizing: border-box; width: 100%; padding: 8px 10px; font: 400 14px/20px var(--font-sans); color: var(--ink); background: var(--surface); border: var(--border); border-radius: 0; box-shadow: var(--shadow-sm); }
.field textarea { min-height: 96px; resize: vertical; }
.field input, .field textarea, .field select { color: var(--ink); }
.field textarea:focus, .field select:focus { outline: 3px solid var(--focus); outline-offset: 2px; box-shadow: 3px 3px 0 var(--focus-deco); }
.select { position: relative; }
.field .select select { appearance: none; padding-right: 40px; height: 40px; cursor: pointer; }
.select::after { content: ""; position: absolute; right: 10px; bottom: 8px; width: 24px; height: 24px; pointer-events: none; background: currentColor; color: var(--ink);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' shape-rendering='crispEdges'%3E%3Cpath d='M1 3h1v1h-1zM10 3h1v1h-1zM1 4h2v1h-2zM9 4h2v1h-2zM2 5h2v1h-2zM8 5h2v1h-2zM3 6h2v1h-2zM7 6h2v1h-2zM4 7h4v1h-4zM5 8h2v1h-2z'/%3E%3C/svg%3E") center / 100% no-repeat; mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' shape-rendering='crispEdges'%3E%3Cpath d='M1 3h1v1h-1zM10 3h1v1h-1zM1 4h2v1h-2zM9 4h2v1h-2zM2 5h2v1h-2zM8 5h2v1h-2zM3 6h2v1h-2zM7 6h2v1h-2zM4 7h4v1h-4zM5 8h2v1h-2z'/%3E%3C/svg%3E") center / 100% no-repeat; }
.field-count { margin: 6px 0 0; font: 10px/1 var(--font-pixel); color: var(--ink-3); text-align: right; }
.field-count.is-over { color: var(--danger); }
.field label .req { color: var(--danger); font-weight: 800; }
.field input:disabled, .field textarea:disabled, .field select:disabled { color: var(--disabled-ink); background: var(--disabled-bg); border-color: var(--disabled-line); box-shadow: none; cursor: not-allowed; }
.field input[readonly], .field textarea[readonly] { background: var(--paper); border-style: dashed; box-shadow: none; }
.radio { display: flex; align-items: center; gap: 8px; margin: 6px 0; font-size: 14px; }
.radio input { appearance: none; display: grid; place-items: center; width: 18px; height: 18px; margin: 0; background: var(--surface); border: var(--border);
  clip-path: polygon(4px 0, calc(100% - 4px) 0, calc(100% - 4px) 2px, calc(100% - 2px) 2px, calc(100% - 2px) 4px, 100% 4px, 100% calc(100% - 4px), calc(100% - 2px) calc(100% - 4px), calc(100% - 2px) calc(100% - 2px), calc(100% - 4px) calc(100% - 2px), calc(100% - 4px) 100%, 4px 100%, 4px calc(100% - 2px), 2px calc(100% - 2px), 2px calc(100% - 4px), 0 calc(100% - 4px), 0 4px, 2px 4px, 2px 2px, 4px 2px); }
.radio input:checked::after { content: ""; width: 6px; height: 6px; background: var(--ink); box-shadow: 0 0 0 2px var(--highlight); }
.radio input:focus-visible, .checkbox input:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; clip-path: none; }
.checkbox input:disabled, .radio input:disabled { background: var(--disabled-bg); border-color: var(--disabled-line); cursor: not-allowed; }
.checkbox:has(input:disabled), .radio:has(input:disabled) { color: var(--ink-3); }
.switch { display: inline-flex; align-items: center; gap: 10px; min-height: 36px; padding: 0; font: 600 14px var(--font-sans); color: var(--ink); background: none; border: 0; cursor: pointer; text-align: left; }
.switch-track { position: relative; flex: none; width: 44px; height: 24px; box-sizing: border-box; background: var(--paper); border: var(--border); }
.switch-track::after { content: ""; position: absolute; left: 2px; top: 2px; width: 16px; height: 16px; background: var(--ink); transition: transform var(--motion-base) var(--ease-steps); }
.switch[aria-checked="true"] .switch-track { background: var(--action); }
.switch[aria-checked="true"] .switch-track::after { transform: translateX(20px); background: var(--surface); }
.switch-state { font: 10px/1 var(--font-pixel); color: var(--ink-3); min-width: 3.5em; }
.switch:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.stepper { display: inline-flex; align-items: stretch; border: var(--border); background: var(--surface); box-shadow: var(--shadow-sm); }
.stepper button { width: 36px; height: 36px; padding: 0; display: grid; place-items: center; color: var(--ink); background: var(--surface); border: 0; cursor: pointer; }
.stepper button:hover { background: var(--paper); }
.stepper button:focus-visible, .stepper input:focus-visible { outline: 3px solid var(--focus); outline-offset: -3px; }
.stepper button[aria-disabled="true"] { color: var(--ink-3); cursor: not-allowed; background: var(--paper); }
.stepper input { width: 52px; height: 36px; box-sizing: border-box; padding: 0; text-align: center; font: 12px var(--font-pixel); color: var(--ink); background: var(--surface); border: 0; border-left: var(--border); border-right: var(--border); -moz-appearance: textfield; }
.stepper input::-webkit-inner-spin-button, .stepper input::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
.upload, .field .upload { position: relative; display: grid; margin: 0; font: 400 14px/20px var(--font-sans); justify-items: center; gap: 6px; padding: 20px 16px; text-align: center; background: var(--surface); border: 2px dashed var(--line-soft); cursor: pointer; }
.upload:hover, .upload.is-drag { border-color: var(--line); background: var(--paper); }
.upload:focus-within { outline: 3px solid var(--focus); outline-offset: 2px; }
.upload input[type="file"] { position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; }
.upload-title { font: 800 15px var(--font-sans); }
.upload-title u { color: var(--link); }
.upload-hint { font-size: 13px; color: var(--ink-3); }
.upload.is-error { border-color: var(--danger); border-style: solid; }
.file-list { display: grid; gap: 8px; margin: 10px 0 0; padding: 0; list-style: none; }
.file-list li { display: flex; align-items: center; gap: 10px; padding: 6px 6px 6px 10px; background: var(--surface); border: var(--border); font-size: 14px; }
.file-list .file-name { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-weight: 600; }
.file-list .file-size { font: 10px/1 var(--font-pixel); color: var(--ink-3); }

/* ---------- nakładki: okno, szuflada, menu, podpowiedź ---------- */
dialog.modal, dialog.drawer { padding: 0; color: var(--ink); background: var(--surface); border: var(--border); box-shadow: var(--shadow-lg); }
dialog.modal { width: min(560px, calc(100vw - 32px)); max-height: calc(100vh - 64px); }
dialog.modal[open] { animation: pp-pop var(--motion-slow) var(--ease-steps); }
dialog.drawer { position: fixed; inset: 0 0 0 auto; width: min(380px, 92vw); height: 100%; max-height: none; margin: 0; border-width: 0 0 0 2px; box-shadow: -6px 0 0 var(--shadow-color); }
dialog.drawer[open] { display: flex; flex-direction: column; animation: pp-slide var(--motion-slow) var(--ease-steps); }
dialog.modal::backdrop, dialog.drawer::backdrop { background: rgba(0, 2, 28, .55); background-image: conic-gradient(rgba(0, 2, 28, .35) 25%, transparent 0 50%, rgba(0, 2, 28, .35) 0 75%, transparent 0); background-size: 4px 4px; }
@keyframes pp-pop { from { transform: translateY(8px); opacity: 0; } }
@keyframes pp-slide { from { transform: translateX(24px); opacity: 0; } }
.modal-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 12px 12px 20px; border-bottom: var(--border); background: var(--paper); }
.modal-head h2 { margin: 0; font: 900 18px/28px var(--font-sans); letter-spacing: -.45px; }
.modal-body { padding: 20px; overflow: auto; }
dialog.drawer .modal-body { flex: 1; }
.modal-body > :first-child { margin-top: 0; }
.modal-foot { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 12px; padding: 16px 20px; border-top: 2px dashed var(--line-soft); }
dialog.drawer .panel-filters { border: 0; box-shadow: none; padding: 0; }
dialog.drawer .panel-filters h2 { display: none; }
.menu { position: relative; display: inline-block; }
.menu-list { position: absolute; z-index: var(--z-dropdown); right: 0; top: calc(100% + 4px); min-width: 200px; margin: 0; padding: 4px; list-style: none; background: var(--surface); border: var(--border); box-shadow: var(--shadow-md); }
.menu-list button, .menu-list a { display: flex; align-items: center; gap: 10px; width: 100%; min-height: 36px; padding: 0 10px; box-sizing: border-box; font: 600 14px var(--font-sans); color: var(--ink); text-align: left; text-decoration: none; background: none; border: 0; cursor: pointer; }
.menu-list button:hover, .menu-list a:hover, .menu-list button:focus-visible, .menu-list a:focus-visible { background: var(--ink); color: var(--on-ink); outline: none; }
.menu-list .is-danger { color: var(--danger); }
.menu-list hr { margin: 4px 0; border: 0; border-top: 2px dashed var(--line-soft); }
.tip { position: relative; display: inline-flex; vertical-align: middle; }
.tip-body { position: absolute; z-index: var(--z-tooltip); left: 50%; bottom: 100%; width: max-content; max-width: min(260px, calc(100vw - 32px)); padding: 8px 10px; transform: translateX(calc(-50% + var(--tip-shift, 0px)));
  font: 600 13px/18px var(--font-sans); color: var(--on-ink); background: var(--ink); border: 2px solid var(--ink); box-shadow: var(--shadow-sm); display: none; }
.tip-body::after { content: ""; position: absolute; left: calc(50% - 4px - var(--tip-shift, 0px)); top: 100%; width: 8px; height: 6px; background: var(--ink); clip-path: polygon(0 0, 100% 0, 50% 100%); }
.tip:hover .tip-body, .tip:focus-within .tip-body { display: block; }
.tip.is-dismissed .tip-body { display: none; }

/* ---------- nawigacja mobilna (opt-in: data-collapsible na .site-nav) ---------- */
.nav-toggle { display: none; }
@media (max-width: 600px) {
  .nav-toggle { display: inline-grid; margin-left: auto; }
  .site-nav[data-collapsible] { display: none; order: 10; flex-basis: 100%; flex-direction: column; gap: 0; border-top: 2px dashed var(--line-soft); }
  .site-nav[data-collapsible].is-open { display: flex; }
  .site-nav[data-collapsible] a { padding: 12px 0; border-bottom: 2px solid transparent; }
}
/* filtry w szufladzie poniżej 900 px: formularz z data-drawer-form chowa się w stronie i jest przenoszony do <dialog class="drawer"> */
.filters-toggle { display: none; }
@media (max-width: 900px) {
  .filters-toggle { display: inline-flex; }
  [data-drawer-form] { display: none; }
  dialog [data-drawer-form] { display: block; }
}

/* ========== v1.8 — wzorce: formularz, wybór wierszy, ładowanie, wykresy ========== */

/* ---------- podsumowanie błędów formularza (na górze, fokus po wysłaniu) ---------- */
.error-summary:focus { outline: 3px solid var(--focus); outline-offset: 2px; }
.error-summary ul { margin: 6px 0 0; padding: 0; list-style: none; }
.error-summary li { margin: 4px 0; }
.error-summary a { color: var(--ink); font-weight: 700; text-decoration: underline; text-underline-offset: 3px; }

/* ---------- ostrzeżenie pola (podpowiada, nie blokuje wysłania) ---------- */
.field.is-warning input, .field.is-warning textarea, .field.is-warning select { border-color: var(--status-warning); box-shadow: 2px 2px 0 var(--status-warning); }
.field-warning { display: flex; gap: 8px; align-items: flex-start; margin: 8px 0 0; font: 600 13px/18px var(--font-sans); color: var(--ink); }
.field-warning::before { content: "!"; flex: none; display: grid; place-items: end center; width: 18px; height: 18px; padding-bottom: 1px; box-sizing: border-box; font: 9px/1 var(--font-pixel); color: var(--on-status-warning); background: var(--status-warning); clip-path: polygon(50% 0, 100% 100%, 0 100%); }

/* ---------- kroki formularza (postęp) ---------- */
.steps-progress { display: flex; margin: 0 0 24px; padding: 0; list-style: none; counter-reset: step; }
.steps-progress li { position: relative; flex: 1; display: grid; justify-items: center; align-content: start; gap: 6px; text-align: center; font: 600 13px/18px var(--font-sans); color: var(--ink-3); counter-increment: step; }
.steps-progress li::before { content: counter(step); position: relative; z-index: 1; display: grid; place-items: center; width: 28px; height: 28px; box-sizing: border-box; font: 10px/1 var(--font-pixel); color: var(--ink-3); background: var(--surface); border: 2px dashed var(--line-soft); }
.steps-progress li + li::after { content: ""; position: absolute; top: 13px; right: 50%; width: 100%; height: 2px; background: var(--line-soft); }
.steps-progress li.is-done { color: var(--ink-2); }
.steps-progress li.is-done::before { content: "✓"; font: 900 14px/1 var(--font-sans); color: var(--on-action); background: var(--action); border: var(--border); }
.steps-progress li.is-done + li::after { background: var(--line); }
.steps-progress li[aria-current="step"] { color: var(--ink); font-weight: 800; }
.steps-progress li[aria-current="step"]::before { color: var(--on-ink); background: var(--ink); border: var(--border); }
@media (max-width: 600px) { .steps-progress .step-label { display: none; } .steps-progress li[aria-current="step"] .step-label { display: block; } }
.wizard-step > h2:first-child, .wizard-step > legend:first-child { margin-top: 0; }
.wizard-nav { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 2px dashed var(--line-soft); }
.wizard-nav .btn-primary { margin-left: auto; }

/* ---------- wybór wierszy tabeli + pasek akcji zbiorczych ---------- */
.table .col-check { width: 40px; padding-right: 0; }
.table .col-check .checkbox { margin: 0; }
.table tbody tr[aria-selected="true"] { background: var(--row-selected); box-shadow: inset 4px 0 0 var(--focus); }
.bulk-bar { position: sticky; bottom: 16px; z-index: var(--z-sticky); display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin-top: 12px; padding: 10px 12px; color: var(--on-ink); background: var(--ink); border: var(--border); box-shadow: var(--shadow-md); }
.bulk-count { margin-right: auto; font: 11px/1.6 var(--font-pixel); }

/* ---------- ładowanie: pasek postępu, ładowanie w miejscu, „Pokaż więcej” ---------- */
.progress { display: grid; gap: 6px; }
.progress-label { display: flex; justify-content: space-between; gap: 12px; font: 600 13px var(--font-sans); }
.progress-label .num { font: 10px/1.6 var(--font-pixel); color: var(--ink-2); }
.progress-track { height: 16px; box-sizing: border-box; padding: 2px; overflow: hidden; background: var(--surface); border: var(--border); }
.progress-fill { height: 100%; width: var(--value, 0%); background: repeating-linear-gradient(90deg, var(--action) 0 8px, transparent 8px 10px); transition: width var(--motion-base) var(--ease-steps); }
.progress.is-indeterminate .progress-fill { width: 30%; animation: pp-indet 1.2s steps(8) infinite; }
@keyframes pp-indet { from { transform: translateX(-100%); } to { transform: translateX(340%); } }
.inline-loading { display: inline-flex; align-items: center; gap: 10px; min-height: 24px; font: 600 14px var(--font-sans); color: var(--ink-2); }
.inline-loading::before { content: ""; flex: none; width: 4px; height: 4px; margin-right: 18px; background: var(--ink); box-shadow: 8px 0 0 var(--ink), 16px 0 0 var(--ink); animation: pp-dots 900ms steps(1) infinite; }
.inline-loading.is-done::before { animation: none; width: 18px; height: 18px; margin-right: 0; box-shadow: none; background: var(--status-success); clip-path: var(--notch); }
.inline-loading.is-error::before { animation: none; width: 18px; height: 18px; margin-right: 0; box-shadow: none; background: var(--status-error); clip-path: var(--notch); }
.load-more { display: grid; justify-items: center; gap: 8px; margin-top: 20px; }
.load-more[hidden] { display: none !important; }
.load-more-info { font: 10px/1.6 var(--font-pixel); color: var(--ink-3); }
@media (prefers-reduced-motion: reduce) { .progress.is-indeterminate .progress-fill { animation: none; width: 100%; opacity: .5; } .inline-loading::before { animation: none; } }

/* ---------- wykresy (charts.js rysuje SVG; tu rama, legenda, dymek, tabela danych) ---------- */
.chart { position: relative; min-width: 0; margin: 0; padding: 16px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-md); }
.chart-title { margin: 0; font: 800 15px/20px var(--font-sans); }
.chart-sub { margin: 2px 0 12px; font-size: 13px; color: var(--ink-3); }
.chart-plot { position: relative; }
.chart svg { display: block; width: 100%; height: auto; overflow: visible; }
.chart svg text { font: 8px var(--font-pixel); fill: var(--chart-axis); }
.chart svg .lbl-strong { fill: var(--ink); }
.chart .hit { fill: transparent; cursor: default; }
.chart-legend { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 12px 0 0; padding: 0; list-style: none; font: 600 13px var(--font-sans); color: var(--ink-2); }
.chart-legend li { display: inline-flex; align-items: center; gap: 6px; }
.chart-legend .swatch { flex: none; width: 12px; height: 12px; background: var(--c); }
.chart-legend .num { font: 9px/1.6 var(--font-pixel); color: var(--ink); }
.chart-tip { position: absolute; z-index: var(--z-tooltip); pointer-events: none; padding: 6px 8px; font: 600 13px/18px var(--font-sans); color: var(--on-ink); background: var(--ink); border: 2px solid var(--ink); box-shadow: var(--shadow-sm); white-space: nowrap; transform: translate(-50%, calc(-100% - 8px)); }
.chart-tip[hidden] { display: none; }
.chart-tip b { display: block; font: 10px/1.6 var(--font-pixel); }
.chart-data { margin-top: 12px; font-size: 13px; }
.chart-data summary { cursor: pointer; font-weight: 700; color: var(--link); }
.chart-data summary:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.chart-data .table-wrap { margin-top: 8px; box-shadow: none; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 210px), 1fr)); gap: 16px; }
.stat { display: grid; align-content: start; gap: 4px; padding: 14px 16px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-sm); }
.stat-label { font: 600 13px var(--font-sans); color: var(--ink-2); }
.stat-value { font: 20px/1.4 var(--font-pixel); color: var(--ink); }
.stat-delta { font: 600 13px var(--font-sans); color: var(--ink-2); }
.stat-delta .up::before { content: "▲ "; color: var(--action); }
.stat-delta .down::before { content: "▼ "; color: var(--danger); }
.stat .chart-spark { margin-top: 6px; }

/* ========== v1.10 — kandydaci przyjęci 2026-11-10 ========== */

/* ---------- wiersz meta w karcie: 3–4 kluczowe atrybuty (Poziom, Tryb, Dodano) ----------
   <ul class="card-meta"><li><span class="icon icon-sm i-user" aria-hidden="true"></span>Poziom: <b>Senior</b></li>…</ul> */
.card-meta { display: flex; flex-wrap: wrap; gap: 6px 14px; margin: 0 0 10px; padding: 0; list-style: none; font-size: 13px; color: var(--ink-3); }
.card-meta li { display: inline-flex; align-items: center; gap: 6px; }
.card-meta b { font-weight: 700; color: var(--ink-2); }

/* ---------- liczba pasujących pozycji przy opcji filtra (wylicza list-controls.js) ---------- */
.checkbox .opt-n { margin-left: auto; font: 9px/1 var(--font-pixel); color: var(--ink-3); }
.checkbox.is-zero { color: var(--ink-3); }
.checkbox.is-zero input { border-color: var(--ink-3); }

/* ---------- zakres od–do ---------- */
.range { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: end; gap: 8px; margin-top: 8px; }
.range .field > span, .range .field > label { display: block; margin: 0 0 4px; font: 700 12px var(--font-sans); color: var(--ink-3); }
.range .dash { padding-bottom: 10px; font-weight: 800; }
.range + .field-error { margin-top: 8px; }

/* ========== v1.11 — kandydaci z testów skilla przyjęci 2026-11-10 ========== */

/* ---------- kod kraju: zamiast flag-emoji, zawsze z pełną nazwą obok ----------
   <td><span class="cc" aria-hidden="true">PL</span>Polska</td> */
.cc { display: inline-grid; place-items: center; min-width: 28px; height: 20px; margin-right: 6px; padding: 0 3px; box-sizing: border-box; font: 7px/1 var(--font-pixel); letter-spacing: .5px; color: var(--ink); background: var(--paper); border: var(--border); vertical-align: middle; }

/* ---------- wyszukiwarka z listą wyboru (miasto, kategoria) ----------
   <form class="search-main has-select" role="search"><input …><div class="select"><select …></select></div><button type="submit">Szukaj</button></form> */
.search-main .select { flex: none; border-left: var(--border); }
.search-main .select select { appearance: none; height: 100%; min-height: 44px; padding: 0 40px 0 12px; border: 0; border-radius: 0; background: transparent; font: 600 15px var(--font-sans); color: var(--ink); cursor: pointer; }
.search-main .select select:focus-visible { outline: 3px solid var(--focus); outline-offset: -3px; }
.search-main .select::after { bottom: auto; top: 50%; transform: translateY(-50%); }
.search-main.has-select button { width: auto; padding: 0 18px; font-size: 12px; }
@media (max-width: 600px) {
  .search-main.has-select { flex-wrap: wrap; }
  .search-main.has-select input { flex: 1 1 100%; }
  .search-main.has-select .select { flex: 1 1 auto; border-left: 0; border-top: var(--border); }
  .search-main.has-select .select select { width: 100%; }
  .search-main.has-select button { border-top: var(--border); }
}

/* ---------- pionowa karta produktu (sklep, katalog, galeria) ----------
   <article class="card card-vertical"><div class="card-art"><span class="sprite sprite-xl s-sword" aria-hidden="true"></span></div>
   <h3>Nazwa</h3><span class="tier-tag tier-legendary">Legendarny</span><ul class="card-meta">…</ul>
   <div class="card-foot"><span class="card-price">…</span><button class="btn btn-secondary btn-compact">…</button></div></article> */
.card-vertical { flex-direction: column; gap: 10px; }
.card-vertical > h3, .card-vertical .card-head h3 { margin: 0; font: 800 18px/24px var(--font-sans); }
.card-vertical > .tier-tag { align-self: flex-start; }
.card-vertical .card-meta { margin: 0; }
.card-vertical .card-foot { flex-wrap: wrap; gap: 8px 12px; margin-top: auto; }
.card-art { display: grid; place-items: center; height: 88px; background: var(--paper); border: var(--border); }
.card-art img { max-height: 64px; image-rendering: pixelated; }
.card-price { display: inline-flex; align-items: center; gap: 6px; font: 12px/1 var(--font-pixel); color: var(--ink); white-space: nowrap; }
.card-price small { font: 600 12px var(--font-sans); color: var(--ink-3); }

/* ---------- tryb wysokiego kontrastu (Windows, forced-colors) ----------
   Przeglądarka usuwa wtedy cienie i tła — ramki i stany rysujemy kolorami systemowymi. */
@media (forced-colors: active) {
  .btn, .icon-btn, .tabs button, .pagination a, .switch-track { border: 2px solid ButtonText; }
  .btn:focus-visible, .icon-btn:focus-visible { outline: 3px solid Highlight; outline-offset: -6px; }
  .btn[aria-disabled="true"], .btn:disabled { color: GrayText; border-color: GrayText; }
  .tabs [aria-selected="true"], .tabs [aria-pressed="true"], .pagination [aria-current="page"], .btn[aria-pressed="true"],
  .icon-btn[aria-expanded="true"], .menu-list button:hover, .menu-list a:hover {
    forced-color-adjust: none; background: Highlight; color: HighlightText; }
  .checkbox input:checked, .radio input:checked { forced-color-adjust: none; background: Highlight; border-color: Highlight; }
  .checkbox input:checked::after, .radio input:checked::after { background: HighlightText; box-shadow: none; }
  .switch[aria-checked="true"] .switch-track { forced-color-adjust: none; background: Highlight; }
  .switch-track::after { forced-color-adjust: none; background: ButtonText; }
  .notice, .tier-tag, .tier, .load-error, .callout-danger { border-left-width: 10px; border-left-style: double; }
  .rank-1, .rank-2, .rank-3 { border-width: 4px; }
  .field.is-error input, .field input[aria-invalid="true"] { border-width: 4px; }
  .skel { forced-color-adjust: none; background: GrayText; }
  .table tbody tr[aria-selected="true"] { forced-color-adjust: none; background: Highlight; color: HighlightText; }
  .steps-progress li[aria-current="step"]::before, .steps-progress li.is-done::before { forced-color-adjust: none; background: Highlight; color: HighlightText; }
  .progress-fill { forced-color-adjust: none; background: Highlight; }
  .chart svg { forced-color-adjust: none; }
}
```

### 9.3 Pozostałe pliki

`icons.css` (generowany, ok. 100 KB — nie wklejamy tutaj), `list-controls.js`, `table-sort.js`, `ui-controls.js`, `charts.js` — w `skills/panel-piksel-ui/assets/`.

---

## 10. Czego nie robić

| Nie | Zamiast |
|---|---|
| `border-radius` na czymkolwiek | proste rogi / `--notch` |
| Rozmyte cienie (`box-shadow: 0 4px 12px …`) | `--shadow-sm/md/lg` |
| Ramki 1 px lub 4 px | 2 px |
| Akapity w Press Start 2P | Archivo |
| Żółte przyciski | `--highlight` tylko dla „Nowa” / wyróżnień |
| Kilka wyróżnionych paneli / dwa podia na ekranie | jeden „głośny” element |
| Zmiana `padding`, `height`, `border-width` w stanach przycisku | cień, kolor, `transform` |
| `outline` na elementach z `clip-path` | pierścień `inset box-shadow` |
| `disabled` bez wyjaśnienia | `aria-disabled` + powód pod przyciskiem |
| Kolory spoza SNES w ilustracjach | paleta z §2.4 |
| Kolory NES poza rankingiem/tierami/blokadą | tokeny SNES |
| Skalowanie pixel-artu o 150% | wielokrotności całkowite |
| Ticker, paralaksa, animacje wejścia | statyczny układ |
| Zakładki (`role="tab"`) do sortowania listy | grupa przycisków `aria-pressed` |
| Rzadkość jako badge z kwadratem | `.tier-tag` |
| Ukrywanie kwot za ikoną/dymkiem | skrót „18–24 tys.” < 600 px |
| Wpisane kolory ramek/cieni (`#00021C`) w stylach ekranu | `var(--line)`, `var(--shadow-color)` — inaczej tryb ciemny się psuje |
| Czerwony tekst komunikatu błędu | tekst w `--ink` + ikona „!” na `--danger` |
| Emoji lub ikony z innych zestawów (Material, Font Awesome) | ikony pikselowe z `icons.css`; brakującą dorysuj w `build_icons.py` |
| Ikony w rozmiarze 16 / 20 px | 12 / 24 / 36 / 48 px |
| Żółte ostrzeżenie | `--status-warning` (pomarańcz) |
| Własne okno z `div` i `z-index: 9999` | `<dialog class="modal">` i tokeny `--z-*` |
| Powiadomienie o błędzie, które znika samo | błąd zostaje do zamknięcia |
| Podpowiedź z treścią niezbędną do zadania | treść w etykiecie lub `.field-hint` |
| Walidacja w trakcie pisania, czerwone pola od razu po wejściu na stronę | błąd po opuszczeniu pola lub przy wysłaniu (§6.18) |
| Natywne dymki przeglądarki przy `required` | `<form data-validate>` |
| Wykres z dwiema osiami Y, kołowy z 8 kawałkami, liczba przy każdym słupku | dwa wykresy; `segments` do 4 części; podpisy przy maksimum i ostatniej |
| Kolory statusów jako kolory serii wykresu | `--chart-1…4` |
| Spinner w kółko przy każdej akcji | tabela czasów w §6.20 |

---

## 11. Otwarte decyzje

- **Tryb ciemny** — tokeny zaakceptowane (§2.6); do sprawdzenia na pełnych ekranach i z czytnikiem; przynależność `#F27961` do Jehkoba32.
- **`aria-sort="none"`** na nieaktywnych kolumnach zostaje (decyzja 2026-11-10) — sprawdzić z czytnikiem, czy nie jest nadmiarowo ogłaszane.
- **Wariant „100% palety”** (panel `#F0EDD8` na tle `#A3CCD9`) — nieprzetestowany.
- **Nagłówki-komendy terminala** („$ ls -a OFERTY”) — tylko dla produktów dla programistów; niezdecydowane.
- Kontrasty policzone z wartości hex; **do zmierzenia narzędziem** na implementacji i z czytnikiem ekranu (testowano tylko Chrome).

## 12. Historia zmian

| Wersja | Data | Zmiana |
|---|---|---|
| 1.11.0 | 2026-11-10 | Kandydaci z testów skilla (iteracja 2), decyzje właściciela: przyjęte jako testowe kod kraju `.cc` (§6.11), wyszukiwarka z listą wyboru `.search-main.has-select` (§6.11), pionowa karta produktu `.card-vertical` + `.card-art` + `.card-price` (§6.6); saldo w nagłówku jako złożenie z `.badge-seg` (§6.24), bez klasy `.wallet`. **Poprawka:** usunięty własny cień pola w `.search-main` (dawał podwójny, schodkowy cień obok listy wyboru i przycisku). Porównanie: `docs/kandydaci.html`. |
| 1.10.0 | 2026-11-10 | Decyzje właściciela: paleta wykresów bez kolorów pakietów i statusów (`--chart-1…4` = terakota, morski, malinowy, zielony; nowy `--chart-single` dla jednej serii); przyjęte jako testowe: wiersz meta karty `.card-meta`, liczba przy opcji filtra `.opt-n` liczona automatycznie przez `list-controls.js`, zakres `.range` z błędem „Od > Do”; koszyk jako złożenie z istniejących klocków (§6.23), ekran sklepu przebudowany. |
| 1.9.1 | 2026-11-10 | Właściciel systemu: Konrad Kosiorek. Skrócone kwoty w wierszach list zapisujemy „18–24 tys.” zamiast „18–24K” (decyzja właściciela; dotyczy też osi wykresów ≥ 10 000). |
| 1.9.0 | 2026-11-10 | Priorytet 3 — zarządzanie (§0): statusy komponentów i rejestr `components.json` (tabela generowana), checklista „gotowe”, wersjonowanie semver (`VERSION`), zasady wycofywania z ostrzeżeniami w `check_screen.py` (sortowanie zakładkami, `.callout-danger`, rzadkość z kwadratem, nadpisana wysokość przycisku), proces zgłaszania zmian, wspierane przeglądarki, procedura testu z czytnikiem; jedno źródło kodu (`sync_system.py` + `panel-piksel.config.json`, `--check`), tokeny w formacie W3C (`tokens.json`), test wizualny (`visual_regression.py`, wzorce w `tests/visual/`). **Migracja:** `.callout.callout-danger` → `.notice.notice-error`. |
| 1.8 | 2026-11-10 | Priorytet 2: wzorzec formularza z walidacją, podsumowaniem błędów, ostrzeżeniem i krokami (§6.18); zaznaczanie wierszy i akcje zbiorcze (§6.19); ładowanie, postęp, ładowanie w miejscu i „Pokaż więcej” (§6.20); wykresy pikselowe z paletą sprawdzoną skryptem (§6.21, `charts.js`, tokeny `--chart-*`); macierz stanów (§6.22); treści i język interfejsu (§6A); przykłady `examples/wzorce.html`. |
| 1.7.1 | 2026-11-10 | Kolorowe wersje wszystkich ikon interfejsu (35, `.sprite .s-…`, cień 1 px, kolor wg znaczenia, wersje dla trybu ciemnego); galeria `examples/ikony.html` generowana przez `build_icons.py`. |
| 1.7 | 2026-11-10 | Priorytet 1 z porównania z IBM Carbon: tokeny statusów (§2.7), ruchu, warstw i punktów przełamania (§4.5–4.6); zestaw ikon pikselowych 39 + 12 przedmiotów (§5, `icons.css`, `build_icons.py`); pola: lista wyboru, radio, przełącznik, pole wielowierszowe z licznikiem, licznik −/+, plik, wymagane, zablokowane, tylko do odczytu (§6.14); powiadomienia w treści i wyskakujące (§6.15); okno, szuflada, menu, podpowiedź, przycisk-ikona (§6.16); zwijana nawigacja i filtry w szufladzie (§6.17); tryb wysokiego kontrastu (§8); `ui-controls.js`; `.section-title` zawija się. |
| 1.6 | 2026-11-10 | Decyzje z dokumentacji komponentów v1.2: przycisk kompaktowy `.btn-compact` 36 px + `.card-foot`; sortowanie listy jako grupa przycisków `aria-pressed`; rzadkość zawsze `.tier-tag`; skrócona kwota < 600 px (`.amt-full` / `.amt-short`); tryb ciemny (§2.6) z nowymi tokenami `--line`, `--shadow-color`, `--on-light`, `--row-hover`; stany błędu i ładowania (§6.13); sekcja „Start dla agenta”. |
| 1.5 | 2026-11-09 | Sortowanie tabel: każda kolumna z danymi sortowalna, cała komórka nagłówka klikalna, puste („—”) na końcu, liczby wyciągane tylko w kolumnach `.num`, `data-sort-first`. Powód: w panelu pracodawcy i leaderboardzie część kolumn i zakładek nie sortowała. |
| 1.4 | 2026-11-09 | Interakcje list (§6.12): zasada „klikalne działa”, sortowanie i filtry kart na atrybutach `data-*`, licznik z polską odmianą, aktywne filtry, pusty stan, przełącznik „Zapisz”, reguła `[hidden]`. Powód: martwe sortowanie i filtry na liście ofert, martwe sortowanie w sklepie, martwe „Zapisz ofertę”. |
| 1.3 | 2026-11-09 | Sortowanie tabel: zasada „przycisk sortowania tylko gdy działa”, statyczny znacznik `.sorted`, `aria-sort` na `<th>`, skrypt `table-sort.js` w skillu (powód: martwe przyciski sortowania w 2 z 6 ekranów testowych). |
| 1.2 | 2026-11-09 | Poprawki z testów skillu na 6 ekranach: `.sr-only` nie rozpycha strony (pełny wzorzec + `position: relative` na `.table-wrap`), `a.btn` bez podkreślenia, `.tabs` przewijają się w ramce na wąskim ekranie, `.rank` mieści liczby 3-cyfrowe, paginacja ma `.gap` i wyłączoną strzałkę, `.facts` min. 180 px kolumny, nowy `.tier-tag`. |
| 1.1 | 2026-11-09 | Elementy ekranu: kontener, nagłówek serwisu, wyszukiwarka główna, okruszki, nagłówek treści, zakładki, **tabela danych**, miejsce w rankingu, zmiana wartości, paginacja, callout, pusty stan, sekcja, fakty encji, treść długa, siatki, stopka. |
| 1.0 | 2026-11-09 | Pierwsza wersja na podstawie studium kierunku „Panel & Piksel”: paleta SNES + akcenty NES, przycisk zablokowany (wariant A), stała wysokość przycisku 44 px, wewnętrzny pierścień fokusu, korekta tokenu fokusu (jasny błękit miał 1.7–2.2:1). |
