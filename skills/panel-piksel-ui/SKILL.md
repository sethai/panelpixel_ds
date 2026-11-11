---
name: panel-piksel-ui
description: Buduje ekrany i komponenty w retro-pikselowym stylu „Panel & Piksel” — białe panele z czarną ramką 2 px i twardym cieniem, gęste numerowane listy, Archivo + Press Start 2P dla liczb, paleta SNES z akcentami NES, podium i tiery rzadkości. Używaj zawsze, gdy użytkownik chce zbudować, zaprojektować, zakodować lub poprawić ekran w stylu Panel & Piksel / „naszego design systemu” / retro pixel / 8-bit / 16-bit — zwłaszcza job board, marketplace, katalog, directory, listing ofert, tabelę danych, ranking, leaderboard, high score, cennik z pakietami, sklep, profil firmy, stronę szczegółów albo pusty stan — nawet jeśli nie poda nazwy systemu, a w projekcie istnieje design.md „Panel & Piksel”. Używaj też, gdy użytkownik chce przenieść (zmigrować, przestylować, „zmienić design”) istniejącą stronę lub aplikację — HTML, React, Vue, Tailwind — na Panel & Piksel. Nie do ilustracji pixel-art ani do gier.
---

# Panel & Piksel — budowanie ekranów

Ten skill zamienia prośbę o ekran w gotowy, dostępny HTML/CSS (lub komponenty we frameworku użytkownika) zgodny z design systemem „Panel & Piksel”. System jest już zaprojektowany i przebadany — Twoim zadaniem jest **komponować z istniejących klocków**, a nie wymyślać nowy styl.

## Pliki skillu

| Plik | Kiedy czytać |
|---|---|
| `assets/tokens.css`, `assets/components.css` | Zawsze — to jest system w kodzie. Kopiujesz je do projektu bez zmian. |
| `assets/list-controls.js` | Gdy lista kart ma sortowanie (zakładki), filtry, licznik wyników albo przełączniki typu „Zapisz” — dołącz skrypt i oznacz elementy atrybutami `data-*` (kontrakt w nagłówku pliku i w `references/screen-recipes.md` §3). |
| `assets/table-sort.js` | Gdy tabela ma sortowalne kolumny (wiersze w HTML) — dołącz skrypt, a przyciski `.sort` zaczną działać. |
| `assets/starter.html` | Gdy budujesz samodzielną stronę HTML — zacznij od niego. |
| `references/screen-recipes.md` | Zawsze przed złożeniem ekranu — przepis dla danego typu ekranu (struktura + HTML). |
| `references/design-system.md` | Gdy potrzebujesz szczegółu: wartości tokenów, kontrastów, stanów komponentu, zasad „czego nie robić”. To pełna specyfikacja (design.md v1.11: zarządzanie §0, tryb ciemny §2.6, statusy §2.7, komponenty i wzorce §6.1–6.24, treści §6A, czego nie robić §10). |
| `assets/icons.css`, `assets/ui-controls.js` | Ikony pikselowe (`.icon .i-…`, `.sprite .s-…`) oraz zachowanie formularzy, okien, szuflady, menu, podpowiedzi, powiadomień i zwijanej nawigacji (v1.7). Dołącz, gdy ekran ich używa. |
| `examples/ikony.html` | Gdy potrzebujesz ikony — pełna lista nazw. Brakującą dorysuj w `scripts/build_icons.py` (ASCII 12×12) i uruchom skrypt. |
| `assets/charts.js`, `examples/wzorce.html` | Formularz w krokach z walidacją, zaznaczanie wierszy z akcjami zbiorczymi, ładowanie i „Pokaż więcej”, wykresy i kafelki liczb (v1.8) — gotowe wzorce do skopiowania. |
| `examples/komponenty.html` | Gdy nie wiesz, jak złożyć komponent, wariant albo stan (kompaktowy przycisk, błąd pola, ładowanie, szkielet, tryb ciemny) — działające wzorce HTML do skopiowania. |
| `scripts/inline_css.py` | Gdy oddajesz jeden przenośny plik — wkleja aktualny CSS systemu w miejsce linków. |
| `scripts/check_screen.py` | Na końcu — statycznie sprawdza najczęstsze złamania zasad. |
| `scripts/render_check.py` | Na końcu — render w 1280 i 390 px przez headless Chrome: szerokość dokumentu, fonty z polskimi znakami, zrzuty. |
| `assets/components.json` | Przed użyciem komponentu — jego status: stabilny / testowy / kandydat / wycofywany (z zamiennikiem). Nie używaj wycofywanych ani kandydatów. |
| `scripts/sync_system.py`, `scripts/visual_regression.py` | Gdy zmieniasz sam system (nie ekran): po edycji `assets/` uruchom `sync_system.py` w katalogu projektu (kopie, design.md §9, tokens.json), a potem test wizualny (§0 w design.md). |

## Esencja (zapamiętaj, zanim zaczniesz)

Katalog z **białych paneli z czarną ramką 2 px i twardym cieniem**, w których są gęste, numerowane listy. Tekst czytelny (Archivo). Piksel tam, gdzie się **patrzy, a nie czyta**: liczby, kwoty, rangi, liczniki (Press Start 2P), schodkowe narożniki małych kontrolek, ilustracje, separatory. **Jeden „głośny” element na ekran** (podium albo wyróżniony panel albo ilustracja).

Dlaczego tak: system powstał dla gęstych listingów. Gdyby piksel był wszędzie (np. akapity w Press Start 2P), listy stają się nieczytelne; gdyby nie było go wcale, znika charakter. Podział „spokojne dane, głośna rama” to kompromis, który działa.

## Proces

### 0. Gdy przenosisz istniejącą stronę (migracja)

Użytkownik ma działającą stronę w innym designie i chce ją przestawić na Panel & Piksel. Cel: **zmienia się wygląd, nie zmienia się treść ani działanie.**

1. **Rozpoznaj, nie zmieniaj.** Stos (czysty HTML, React/Vue/Svelte, Tailwind, CSS-in-JS, Bootstrap), strony, wspólny layout, obecne kolory/fonty/komponenty, skrypty i formularze. Zanim cokolwiek zmienisz, pokaż użytkownikowi mapę: *obecny element → komponent Panel & Piksel* (np. „karta produktu → `.card` + `.tier-tag`”, „pasek filtrów → `.panel-filters` + `.opt-n`”, „toast biblioteki X → `.notice` / `ppToast`”) oraz listę elementów, których w systemie brakuje. Poproś o akceptację planu.
2. **Gałąź i fundament.** Pracuj na nowej gałęzi git. Skopiuj pliki systemu do projektu bez zmian (`assets/` → np. `public/panel-piksel/`), podepnij globalnie fonty i CSS. W Tailwind przenieś tokeny do `theme.extend` (kolory, `boxShadow` 2/4/6 px bez rozmycia, `borderRadius: 0`), ale nadal używaj klas systemu tam, gdzie istnieją.
3. **Wyłącz stary design świadomie.** Usuń lub zneutralizuj stare arkusze i motyw UI-kitu (Bootstrap, MUI…) tylko w zakresie, który migrujesz — nie zostawiaj dwóch systemów walczących o te same elementy (zaokrąglenia, rozmyte cienie, inne fonty przebijające się przez nowe style).
4. **Strona po stronie, komponent po komponencie.** Zachowaj teksty co do znaku, linki, adresy, atrybuty formularzy (`name`, `action`, walidację serwera), identyfikatory używane przez skrypty i testy, dane i routing. **Nie poprawiaj treści** nawet tam, gdzie łamie zasady §6A (np. „22 000 – 28 000” zamiast „22 000–28 000”, wielkie litery, nazwy przycisków) — wypisz takie miejsca jako propozycje w odpowiedzi. Kontrolki, które w starej stronie nic nie robiły (np. filtry bez obsługi), podłącz skryptami systemu tylko wtedy, gdy nie zmienia to tego, co trafia na serwer, i zgłoś to wprost; w przeciwnym razie zostaw je i opisz. Zmieniaj znaczniki tylko tyle, ile wymaga komponent systemu (np. etykieta nad polem, `aria-pressed` w przełączniku). Logikę aplikacji (stan, zapytania) zostaw; zachowanie interfejsu zapewniają skrypty systemu albo istniejący kod frameworka.
5. **Sprawdź każdą stronę** jak nowy ekran (krok 5) na zbudowanym HTML (w frameworku: `npm run build` / podgląd i pliki z wyniku) i porównaj z wersją przed migracją: ta sama treść, te same linki, formularze dalej wysyłają te same pola.
6. **Oddaj** listę zmienionych plików, mapę komponentów, elementy spoza systemu (kandydaci — design.md §0.5) i to, czego nie dało się sprawdzić.

### 1. Zrozum ekran

Ustal z prośby (dopytaj tylko, jeśli naprawdę brakuje czegoś, bez czego nie da się zacząć):
- **typ ekranu** → wybierz przepis z `references/screen-recipes.md` (katalog, kategoria, wyniki z filtrami, szczegóły, ranking, cennik/pakiety, profil, formularz, pusty stan, panel użytkownika);
- **domenę i dane** — jakie encje (oferty, produkty, firmy, gracze), jakie liczby (kwoty, punkty, liczniki);
- **format wyniku** — samodzielny HTML (domyślnie) albo komponenty w istniejącym projekcie (React/Vue/Tailwind) — wtedy dopasuj się do jego konwencji, ale zachowaj tokeny i wygląd.

Treść pisz po polsku, chyba że użytkownik pisze w innym języku. Używaj realistycznych danych (nazwy, kwoty z „zł”, polskie znaki), bo puste „Lorem ipsum” ukrywa problemy z długością tekstu.

### 2. Przygotuj fundament

- **Samodzielny HTML:** skopiuj `assets/starter.html` jako plik wynikowy oraz `assets/tokens.css`, `assets/components.css`, `assets/icons.css` do katalogu `panel-piksel/` obok, a skrypty tylko te, których ekran potrzebuje: `list-controls.js` (listy kart, filtry, „Pokaż więcej”), `table-sort.js` (sortowalne tabele), `ui-controls.js` (formularze z walidacją, okna, szuflada, menu, podpowiedzi, powiadomienia, zaznaczanie wierszy, zwijana nawigacja), `charts.js` (wykresy i minilinie). Jeśli użytkownik chce jeden przenośny plik, zbuduj ekran z linkami, a na końcu uruchom `python3 <ścieżka-skillu>/scripts/inline_css.py ekran.html` — wklei aktualny CSS systemu w miejsce linków (nie przepisuj CSS ręcznie).
- **Istniejący projekt:** dołącz oba pliki CSS globalnie (albo przenieś tokeny do jego systemu motywów — np. `theme.extend` w Tailwind) i buduj komponenty na tych samych klasach/wartościach.
- **Nie edytuj** `tokens.css` ani `components.css`. Własne style ekranu dopisz w osobnym bloku `<style>` / pliku — tylko układ i drobne dopasowania, z użyciem tokenów (`var(--…)`), nigdy z nowymi kolorami czy cieniami.

### 3. Złóż ekran z komponentów

Korzystaj z klas z `components.css` (pełna lista i anatomia w `references/design-system.md` §6):

- przyciski `.btn .btn-primary/.btn-secondary` (stała wysokość 44 px; `.btn-compact` 36 px dla przycisku powtarzanego w każdej pozycji listy — stopka karty `.card-foot`, wiersz tabeli, koszyk; zablokowany = `aria-disabled="true"` + `.lock` + `.btn-reason` z powodem; ładowanie = `.is-loading` + `aria-busy`),
- `.badge`, `.badge-new`, `.badge-seg`, `.chip`, `.chip-more`, `.count`, `.avatar`,
- `.panel` (+ `.is-featured`), `.list`, `.card`, `.panel-filters`, `.field`, `.checkbox`,
- `.podium`, `.tier` (karta pakietu), `.tier-tag` (kompaktowy znacznik tieru — **jedyny zapis rzadkości/pakietu** w kartach, tabelach, koszyku), `.table-wrap/.table`, `.rank`, `.tabs` (zakładki `role="tab"` tylko gdy przełączają panele; **sortowanie = `role="group"` + przyciski `aria-pressed`**), `.pagination`, `.callout`, `.empty`, `.facts`,
- pola (v1.7): `.select`, `.radio`, `.switch[role=switch]`, `textarea` + `.field-count`, `.stepper`, `.upload` + `.file-list`, `[readonly]`, `:disabled`, `.req`; nakładki: `dialog.modal`, `dialog.drawer`, `.menu`, `.tip`, `.icon-btn`; powiadomienia: `.notice.notice-info|success|warning|error`, `ppToast({...})`; nawigacja: `.nav-toggle` + `.site-nav[data-collapsible]`, filtry w szufladzie `.filters-toggle`,
- ikony: `.icon .i-…` (kolor tekstu — przyciski, pola, nawigacja), `.sprite .s-…` (kolorowe wersje tych samych ikon z cieniem 1 px — akcenty w nagłówkach kategorii, pustych stanach, listach cech; oraz ręcznie rysowane przedmioty z gier: moneta, serce, gwiazda, klejnot, puchar…) — zamiast emoji i obcych zestawów ikon,
- wzorce (v1.8): formularz `<form data-validate>` (błąd po opuszczeniu pola i przy wysłaniu, podsumowanie `.error-summary`, ostrzeżenie `data-warn-empty`, kroki `data-wizard` + `.steps-progress`), tabela `data-selectable` + `.bulk-bar`, `.progress` / `.inline-loading`, lista `data-page-size` + `.load-more`, kafelki `.stats > .stat`, wykresy `figure.chart[data-chart=columns|line|bars|segments]` (`charts.js`; jedna seria `--chart-single`, kategorie `--chart-1…4` — nigdy kolory statusów ani pakietów), `.card-meta`, `.opt-n` (liczby wylicza skrypt), `.range`, koszyk z klocków (design.md §6.23),
- v1.11: kod kraju `.cc` (zamiast flag-emoji, zawsze z nazwą), wyszukiwarka z listą `form.search-main.has-select` + `.select > select`, pionowa karta produktu `.card.card-vertical` + `.card-art` + `.card-price`, saldo w nagłówku z `.badge.badge-seg` + sprite waluty (§6.24 — bez własnej klasy),
- treści: §6A w design.md — ton, wielkie litery, liczby „1 128”, kwoty „22 000–28 000 zł”, daty względne na listach, odmiana 1/2–4/5+, błędy mówią co zrobić,
- stany: `.field.is-error` + `.field-error`, `.field-hint`, `.skel`/`.skel-row`, `.load-error`, `.callout-danger`; kwota w wierszu listy jako `.amt-full` + `.amt-short` (skrót „18–24 tys.” < 600 px),
- tryb ciemny: `data-theme="dark"`/`"auto"` na `<html>` — działa tylko z tokenami, bez wpisanych kolorów,
- układ: `.container`, `.site-header`, `.search-main`, `.breadcrumbs`, `.page-head`, `.grid-panels`, `.layout-main-side`, `.layout-results`, `.section`, `.site-footer`.

Jeśli ekran potrzebuje czegoś, czego nie ma w systemie, zbuduj to z tych samych prymitywów: ramka `var(--border)`, cień `--shadow-sm/md/lg`, promień 0, Archivo dla tekstu, `--font-pixel` tylko dla liczb. Opisz w odpowiedzi, że to nowy element (kandydat), żeby można go było zgłosić według design.md §0.5 — nie dopisuj go samodzielnie do `components.css`.

**Typowe pułapki z testów:** linki-przyciski (`<a class="btn">`) i linki w tytułach kart dziedziczą kolor/podkreślenie — przyciski są już obsłużone w systemie, tytuły kart ustaw w stylach ekranu na `color: var(--ink); text-decoration: none` (podkreślenie na hover); własne paski przewijane poziomo (zakładki, chipy) potrzebują `min-width: 0` / `overflow-x: auto`, żeby nie rozpychały strony na telefonie; tekst `.sr-only` w komórkach tabel jest bezpieczny tylko wewnątrz `.table-wrap` (ma `position: relative`).

### 4. Zasady, których pilnujesz (i dlaczego)

1. **Ramka zawsze 2 px, rogi proste.** Spójny „kartridżowy” kształt to główny nośnik stylu; 1 px wygląda jak zwykły web, 4 px jest za ciężki w gęstych listach.
2. **Tylko twarde cienie 2/4/6 px** (badge·pole / karta·filtry / panel·podium). Rozmyty cień natychmiast psuje retro-wygląd.
3. **Archivo dla wszystkiego, co się czyta; Press Start 2P tylko dla liczb, liczników, kwot, rang i etykiet ≤ 3 słów.** Pixel-font w akapitach jest nieczytelny.
4. **Jeden kolor akcji** (`--action`) i **jeden głośny element na ekran** (podium *albo* `.is-featured` *albo* ilustracja *albo* `.search-main` z kolorowym cieniem jako jedyny akcent). Kilka akcentów naraz to chaos, w którym nic się nie wyróżnia.
5. **Żółty (`--highlight`) znaczy tylko „nowe/wyróżnione”** — nie rób żółtych przycisków.
6. **Akcenty NES (`--podium`, `--gold`…, `--tier-*`) tylko w rankingu, pakietach i stanie zablokowanym.** Poza tym paleta SNES.
7. **Stany nie zmieniają rozmiaru** — hover/active/focus tylko przez kolor, cień i `transform`. Inaczej elementy wokół „skaczą” (tak było w pierwszej wersji systemu).
8. **Kolor nigdy nie jest jedynym nośnikiem znaczenia**: ranga = numer + kolor, tier = nazwa + kolor, zmiana = ▲/▼ + kolor.
9. **Dostępność:** widoczny fokus (przyciski mają wewnętrzny pierścień, bo `clip-path` obcina `outline`), etykiety pól (`<label>` lub `.sr-only`), `lang="pl"`, sensowne nagłówki, tabele z `<th>`, kolejność DOM podium 1-2-3.
10. **Każdy element, który wygląda na klikalny, musi działać** — zakładki sortowania, filtry, licznik „Pokaż N ofert”, przełączniki „Zapisz”, sortowanie tabel. Statyczna makieta z martwymi kontrolkami to dla użytkownika błąd, nie szkic (w testach martwe były: sortowanie i filtry listy ofert, sortowanie sklepu, „Zapisz ofertę”, sortowanie tabel). Listy kart: `assets/list-controls.js` + atrybuty `data-list`, `data-item`, `data-sort-for`, `data-filter-for`, `data-count-for`. Tabele: jeśli sortujesz, to **każdą kolumnę z danymi** (poza „#” i „Akcje”) i w **każdej** tabeli na ekranie (także w ukrytych zakładkach) — połowiczne sortowanie użytkownik odbiera jako „nie działa”. Kolumny z wartością porządkową (pakiet, ranga, status) sortuj po znaczeniu przez `data-sort-value` + `data-sort-first="descending"` na `<th>`. Przycisk sortowania `.sort` tylko z działającym sortowaniem: dołącz `assets/table-sort.js` (wiersze w HTML) albo, gdy wiersze buduje Twój kod (np. paginacja z danych), oznacz tabelę `data-sort-manual` i sortuj dane sam. Gdy kolejność jest stała (ranking po wyniku), użyj statycznego `<span class="sorted">` — bez wyglądu przycisku. Kierunek zawsze w `aria-sort` na `<th>`. Liczby w interfejsie mają się zgadzać z tym, co widać (licznik wyników = liczba widocznych kart, liczby przy opcjach filtrów = liczba pasujących pozycji). Paginacji do nieistniejących stron nie dodawaj — jeśli jest potrzebna, a nie działa, napisz to wprost w odpowiedzi. (W pierwszych testach 2 z 6 ekranów miały martwe przyciski sortowania — użytkownik klikał i nic się nie działo.)
11. **Mobile:** siatki przechodzą do jednej kolumny, panele skrócone do 5–8 pozycji, tabela przewija się w swojej ramce, filtry nad wynikami.

### 5. Sprawdź

1. Uruchom: `python3 <ścieżka-skillu>/scripts/check_screen.py <plik.html>` — raport błędów (ERROR) i ostrzeżeń (WARN). Popraw wszystkie ERROR; każde WARN albo popraw, albo świadomie uzasadnij.
2. Uruchom `python3 <ścieżka-skillu>/scripts/render_check.py <plik.html> [katalog_na_zrzuty]` — poda szerokość dokumentu w 1280 i 390 px (czy strona przewija się poziomo), czy fonty z polskimi znakami się ładują, zapisze zrzuty i **kliknie każdą kontrolkę w `<main>`**: każda zgłoszona jako `MARTWA` musi zostać naprawiona (albo usunięta). To jedyny sposób, żeby wyłapać np. zakładki sortowania bez obsługi na stronie, która ma inne skrypty. Test klika tylko kontrolki **widoczne** po załadowaniu — kontrolki w ukrytych zakładkach, szufladach i oknach dialogowych sprawdź osobno (przełącz zakładkę i kliknij). Okno headless Chrome nie zwęża się poniżej ~500 px, dlatego skrypt renderuje 390 px w ramce — nie musisz tego obchodzić samodzielnie. **Obejrzyj oba zrzuty** (Read na pliku PNG): nic nie nachodzi na siebie, długie nazwy ucinają się wielokropkiem, a nic nie wystaje. Gdy Chrome jest niedostępny, użyj dowolnej przeglądarki, którą masz, albo napisz, że renderu nie sprawdziłeś.
3. Przejrzyj listę „Czego nie robić” w `references/design-system.md` §10.

Jeśli w projekcie jest `panel-piksel.config.json`, uruchom też `python3 <ścieżka-skillu>/scripts/sync_system.py --check` — kopie systemu muszą być zgodne ze źródłem.

### 6. Oddaj

W odpowiedzi podaj: ścieżkę do pliku, jakiego przepisu użyłeś, który element jest „głośnym” elementem ekranu, czego nie dało się zrobić z istniejących komponentów (nowe elementy — z krótką specyfikacją, żeby dało się je dopisać do design.md), wynik `check_screen.py` i `render_check.py`. Nie twierdź, że coś sprawdziłeś, jeśli tego nie zrobiłeś.

## Szybka ściąga tokenów

| Rola | Token | Wartość (jasny / ciemny) |
|---|---|---|
| tło strony / panel | `--paper` / `--surface` | `#F0EDD8` / `#FFFFFF` · ciemny `#00021C` / `#1C284D` |
| tekst / opis / meta | `--ink` / `--ink-2` / `--ink-3` | `#00021C` / `#1C284D` / `#2D5280` |
| ramki / cienie / tekst na jasnych tłach | `--line` / `--shadow-color` / `--on-light` | jak `--ink` · ciemny `#F0EDD8` / `#2469B3` / `#00021C` |
| akcja | `--action` | `#17735F` |
| nowe / wyróżnione | `--highlight` | `#F7C93E` (tylko „Nowa”, nie przyciski) |
| link / fokus | `--link` / `--focus` | `#2469B3` · ciemny `#0BAFE6` / `#F7C93E` |
| statusy: informacja / sukces / ostrzeżenie / błąd | `--status-info/success/warning/error` | `#2469B3` / `#17735F` / `#E45C10` / `#D9214F` (zawsze z ikoną i tekstem) |
| chip / „+N” | `--chip` / `--chip-more` | `#A3CCD9` / `#F0BB90` |
| wyróżniony panel (cień) | `--featured` | `#D94C87` |
| podium / złoto / srebro / brąz | `--podium` / `--gold` / `--silver` / `--bronze` | `#0000BC` / `#F8B800` / `#BCBCBC` / `#E45C10` |
| pakiety (NES) | `--tier-legendary/epic/rare/common` | `#AC7C00` / `#6844FC` / `#0078F8` / `#7C7C7C` |
| wykresy | `--chart-single` · `--chart-1…4` | `#2D5280` (ciemny `#A3CCD9`) · `#B36159` `#1BA683` `#A6216E` `#119955` — nie kolory pakietów ani statusów |
| fonty | `--font-sans` / `--font-pixel` | Archivo / Press Start 2P |
| cienie | `--shadow-sm/md/lg` | 2 / 4 / 6 px, bez rozmycia |
| ruch | `--motion-fast/base/slow` · `--ease-steps` | 60 / 120 / 200 ms · `steps(3)` |
| warstwy | `--z-dropdown/drawer/modal/toast/tooltip` | 100 / 200 / 300 / 400 / 500 |
| kwoty w wierszach < 600 px | `.amt-full` + `.amt-short` | „18 000–24 000 zł” → „18–24 tys.” |
