Gotowe: **`levelup-jobs-wyniki.html`** — ekran wyników wyszukiwania LevelUp Jobs w stylu Panel & Piksel, jako jeden samodzielny plik (`tokens.css` i `components.css` wklejone bez zmian do `<style>`, style ekranu osobno w `<style id="screen">`).

**Co jest na ekranie**
- Przepis: „3. Wyniki wyszukiwania z filtrami” (`.layout-results`).
- 8 ofert w kartach `.card` z 8 fikcyjnych studiów (Pixel Forge Studio, Łódzkie Żetony, Krakowski Quest, 8-Bit Żubr Games, Gdańska Wyspa Interactive, Smocza Pieczara, Złota Kaczka, Rubin Bytes). Każda karta ma poziom, tryb pracy, datę dodania i tagi technologii (najwyżej 4 `.chip` plus `.chip-more`).
- Widełki w zł pokazuje `.amount` fontem pikselowym, z dopiskiem B2B/UoP. 3 oferty nie mają widełek i pokazują „Widełki nie podane” (`.amount.is-empty`).
- Nowa jest jedna oferta, Senior Gameplay Programmer, oznaczona `.badge-new` „Nowa”.
- Sortowanie: `.tabs` z opcjami Najnowsze / Najwyższe widełki / Trafność. Nad listą są chipy aktywnych filtrów, pod nią paginacja.
- Panel filtrów `.panel-filters` po prawej ma pole słów kluczowych i grupy: tryb pracy, poziom, technologia, widełki (pola od–do i opcja „Tylko z widełkami”). Na dole jest przycisk „Pokaż 42 oferty” i link „Wyczyść filtry”. Na mobile panel przechodzi nad wyniki.

**Głośny element:** zgodnie z przepisem ekran nie ma osobnej „sceny”. Akcentami są żółty badge „Nowa” i kolorowy cień wyszukiwarki z nagłówka. Nie ma ani `.is-featured`, ani podium.

**Nowe elementy spoza systemu** (zbudowane z tokenów, można je dopisać do design.md):
- `.card-meta` — wiersz meta w karcie (poziom, tryb, data).
- `.opt-n` — licznik ofert przy opcji filtra, fontem pikselowym.
- `.range` — dwa pola „od–do” dla widełek.
- `.active-filters` — wiersz chipów aktywnych filtrów.
- `.clear-link` — link „Wyczyść filtry”.
- Etykieta „Sortuj:” przy zakładkach.

**Sprawdzenie**
- `check_screen.py`: OK, bez ERROR i bez WARN.
- Render obejrzałem w headless Chrome w 1280 px i 390 px (390 px przez iframe, bo okno headless ma minimum 500 px). W obu szerokościach `scrollWidth` równa się szerokości okna, więc strona nie przewija się poziomo. Polskie znaki renderują się w obu fontach.
- Nie testowałem interakcji: sortowanie i filtry to statyczny HTML bez JS.
