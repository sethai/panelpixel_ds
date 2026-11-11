Gotowe: **`oferta-senior-unity-developer.html`** (jeden samodzielny plik; `tokens.css` i `components.css` są wklejone bez zmian do `<style>`, style ekranu w osobnym `<style id="screen">`, tylko z tokenami).

**Przepis:** §4 „Szczegóły encji” (`.layout-main-side`).

**Co jest na ekranie**
- Nagłówek oferty (`.card` + `.avatar-xl` „SJ”, badge „Nowa”, `.badge-seg` „Dodano | 3 dni temu” i „Aplikacje | 27”).
- Fakty (`.facts`): widełki 22 000–28 000 zł, B2B netto, Wrocław, hybrydowo 2 dni w biurze, Senior, zespół, start, rekrutacja. Liczby w Press Start 2P.
- Panele `.prose`: O projekcie + „Czym się zajmiesz”, Wymagania (chipy technologii z `+2`, „Musisz mieć” / „Mile widziane” w dwóch kolumnach) i Benefity. Cały tekst w Archivo.
- Panel boczny: kwota `22 000–28 000 zł`, **Aplikuj teraz** zablokowany (`aria-disabled="true"`, pikselowa `.lock`, `aria-describedby` na `.btn-reason`: „Dodaj CV do profilu, aby aplikować.” z linkiem „Dodaj CV”), **Zapisz ofertę** (`.btn-secondary`, `aria-pressed`), licznik dni do końca ważności.
- Podobne oferty: `.panel` z `.list` (5 pozycji, `.count`, kwoty w `.list-value`, długie nazwy ucinane wielokropkiem).

**Głośny element:** panel akcji z kwotą (`.panel.is-featured`, różowy twardy cień), czyli jedyny wyróżniony panel na ekranie.

**Nowe elementy (spoza komponentów systemu, złożone z prymitywów):**
- `.req-cols`: dwie kolumny wymagań, na mobile jedna.
- Drobne układowe dopasowania w panelu akcji: etykieta „Wynagrodzenie”, większa kwota (16 px), linia „Oferta ważna jeszcze N dni” z przerywanym separatorem jak `.panel-more`.
- `<h1>` w `.card-head`: ten sam krój co `.page-head h1`.

**Sprawdzenie**
- `check_screen.py`: „OK — brak uwag” (0 błędów, 0 ostrzeżeń).
- Render obejrzałem w headless Chrome przy 1280 px oraz 390 px (w iframe). Przy 390 px szerokość dokumentu to 390, więc nie ma poziomego przewijania. Siatka przechodzi do jednej kolumny, polskie znaki renderują się w obu fontach.

**Do decyzji**
- Na mobile panel z kwotą i przyciskami ląduje pod całym opisem, bo tak działa `.layout-main-side`. Warto rozważyć przeniesienie bloku akcji zaraz pod fakty albo lepki pasek „Aplikuj” na dole.
- W `.facts` przy 1280 px widełki łamią się na dwie linie. Jest to czytelne, ale można dać tej komórce podwójną szerokość.
