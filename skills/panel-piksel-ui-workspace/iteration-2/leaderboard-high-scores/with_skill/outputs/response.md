Leaderboard „Kosmicznego Kreta” jest gotowy jako jeden plik:

**`leaderboard.html`** — CSS systemu Panel & Piksel jest wklejony w plik przez `inline_css.py`. Z zewnątrz ładują się tylko fonty Google (Archivo, Press Start 2P).

## Co jest na ekranie

- **Przepis:** `screen-recipes.md` §5, czyli ranking / leaderboard / high score.
- **Głośny element:** podium z miejscami 1–3. Na ekranie nie ma innych akcentów, a puchar przy tytule to tylko mały sprite.
  - W DOM miejsca idą w kolejności 1-2-3, a na ekranie widać 2–1–3.
  - Każde miejsce ma monogram, nick, kraj i wynik (zwycięzca na złoto) oraz stopień z numerem.
- **Przełącznik Dziś / Ten tydzień / Wszech czasów:**
  - Zbudowany jako `.tabs` z `role="tablist"`, bo przełącza panel treści.
  - Działa myszką i strzałkami ←/→ oraz klawiszami Home/End.
  - Każdy okres ma własne podium, tabelę i opis zmiany pozycji (np. „względem wczoraj”).
- **Tabela z miejscami 4–20** (`.table-wrap` + `.table`). Kolumny:
  - **#** — `.rank`;
  - **Gracz** — monogram i nick jako link; długi nick ucina się wielokropkiem;
  - **Kraj** — kod ISO i nazwa;
  - **Wynik** — stały porządek malejący, oznaczony `.sorted` i `aria-sort="descending"`;
  - **Rozgrywki**;
  - **Zmiana** — ▲/▼ z liczbą (`.delta-up`/`.delta-down`), „—” gdy pozycja się nie zmieniła, odznaka „Nowy” (`.badge-new`) dla nowych graczy. Czytniki ekranu dostają opis słowny, np. „w górę o 3”.
  - Liczby są wyrównane do prawej i zapisane w foncie pikselowym, z separatorem tysięcy („61 875”).
- **Paginacja** (`.pagination`) działa naprawdę:
  - strona 1 to miejsca 4–20, kolejne strony to 21–40 … 81–100 (5 stron);
  - strzałki są wyłączone (`aria-disabled`) na pierwszej i ostatniej stronie;
  - zmiana okresu wraca do strony 1;
  - licznik „Ten tydzień: miejsca 4–20 ze 100” ogłasza zmianę (`aria-live`).
- **Dane:** przykładowe — 100 graczy na okres, generowane deterministycznie w skrypcie, z polskimi znakami w nickach i jednym bardzo długim nickiem do testu. Żeby podłączyć API, wystarczy podmienić obiekt `DATA`. Linki `/gracz/…` oraz adresy w nagłówku i stopce prowadzą do stron, których jeszcze nie ma.
- **Telefon (390 px):**
  - podium zostaje w trzech kolumnach;
  - w kolumnie „Kraj” widać tylko kod, a pełna nazwa jest dostępna dla czytników ekranu;
  - tabela przewija się poziomo wewnątrz swojej ramki.

## Nowy element spoza systemu (kandydat, design.md §0.5)

**Kod kraju `.cc`:** kwadrat z ramką 2 px (`var(--border)`), tło `--paper`, wysokość 20 px, min. szerokość 28 px, kod ISO w `--font-pixel` 7 px. Obok stoi nazwa kraju w Archivo; poniżej 600 px nazwa jest ukryta wizualnie, ale zostaje dla czytników ekranu. Ten zapis zastępuje flagi-emoji, których system zabrania. Nie dopisałem go do `components.css`. Jeśli ma zostać, warto go zgłosić jako element tabeli.

Poza tym style ekranu to tylko układ (zbudowany na tokenach) i wielokropek dla długich nicków na podium i w tabeli. W stylach ekranu nie ma żadnych nowych kolorów ani cieni.

## Wyniki sprawdzenia

- **`check_screen.py`:** „OK — brak uwag”, bez żadnych ERROR ani WARN.
- **`render_check.py`:**
  - 1280 px: szerokość dokumentu 1280 px (OK);
  - 390 px: szerokość 390 px (OK);
  - fonty Archivo i Press Start 2P z polskimi znakami ładują się w obu szerokościach;
  - test klikania: 3 z 3 kontrolek reaguje, martwych 0.
- **Poprawki po pierwszym renderze:** w pierwszym przebiegu podium z długim nickiem rozpychało stronę do 567 px. Poprawiłem to (`minmax(0, 1fr)` w siatce) i zweryfikowałem kolejnym renderem.
- **Zrzuty:** obejrzałem `zrzuty/leaderboard-1280.png` i `zrzuty/leaderboard-390.png`. Nic na siebie nie nachodzi i nic nie wystaje poza ekran.
- **Paginacja i strzałki w zakładkach:** `render_check` klika tylko przyciski, więc paginację i nawigację strzałkami sprawdziłem osobnym testem w headless Chrome. Wyniki:
  - strona 3 pokazuje miejsca 41–60 (20 wierszy), a fokus zostaje na bieżącej stronie;
  - na ostatniej stronie są miejsca 81–100, a strzałka „dalej” jest wyłączona;
  - przełączenie na „Wszech czasów” wraca do miejsc 4–20 i zmienia podium;
  - strzałka → przenosi zaznaczenie i fokus na kolejną zakładkę.
- **Czego nie sprawdzałem:** trybu ciemnego. Style ekranu używają wyłącznie tokenów, więc powinien działać po dodaniu `data-theme="dark"`.
