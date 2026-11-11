Migracja zrobiona — KodRekrut jest teraz w stylu Panel & Piksel. Treść, linki, formularze i zapisywanie ofert działają tak jak wcześniej.

## Co się zmieniło

- `site/index.html` — przepisany na komponenty systemu (przepis „Wyniki wyszukiwania z filtrami”).
- `site/panel-piksel/` — nowy katalog z plikami systemu skopiowanymi bez zmian: `tokens.css`, `components.css`, `icons.css`, `list-controls.js`, `ui-controls.js`.
- `site/style.css` — usunięty. Stary design (Inter, gradienty, zaokrąglenia, rozmyte cienie) gryzłby się z systemem. Wygląd ekranu to teraz system plus krótki blok `<style id="screen">` (sam układ, tylko tokeny `var(--…)`).
- **Głośny element ekranu:** główna wyszukiwarka (`.search-main` z kolorowym cieniem). Nie ma innych akcentów.

## Co zostało bez zmian

- **Teksty:** wszystkie nagłówki, opisy, nazwy ofert, firmy, technologie i stopka.
  - Wyjątek: zapis widełek. Zamiast „22 000 – 28 000 zł” jest „22 000–28 000 zł” — tak każe reguła treści systemu (§6A).
- **Linki:** `/`, `/oferty`, `/firmy`, `/blog`, `/dodaj-oferte`, `/oferta/101–104`, `?sort=data`, `?sort=widelki`, `?page=1/2/3`, „Dalej →”, `/regulamin`, `/prywatnosc`, `/kontakt`.
- **Wyszukiwarka:** `action="/szukaj"`, `method="get"`, pola `q` i `miasto` z tymi samymi opcjami i wartościami.
- **Newsletter:**
  - `id="newsletter-form"`, `action="/newsletter"`, `method="post"`, pola `email` i `zgoda` — oba nadal `required`.
  - Doszło `data-validate`: przy pustych polach błędy pokazują się przy polach. Gdy wszystko jest wypełnione, formularz wysyła się normalnie, na ten sam adres i z tymi samymi polami.
- **Zapisywanie ofert:**
  - Logika jest ta sama: klasa `.save`, `data-id`, klasa `is-saved`, zmiana `aria-label` („Zapisz ofertę” ↔ „Usuń z zapisanych”), `localStorage['saved-<id>']` = `'1'` / `''`.
  - Jedyna zmiana w Twoim skrypcie: zamiast podmieniać znak ♡/♥, przełącza pikselową ikonę serca (`i-heart-outline` ↔ `i-heart`).
- **Identyfikatory i klasy:** zostały `#job-list`, `data-id` na `li.job` oraz klasy `job`, `featured`, `company`, `salary`, `tags`, `filters`, `pager`, `consent` (jako znaczniki dla skryptów i testów, bez starych stylów).

## Mapa: stary element → komponent systemu

| Stary element | Komponent Panel & Piksel |
|---|---|
| `header.nav` | `.site-header > .container` |
| `.brand` „KodRekrut” | `.logo` („Kod**Rekrut**”, drugi człon w kolorze akcji) |
| `nav a.active` | `.site-nav` + `aria-current="page"` |
| `.btn.btn-gradient` „Dodaj ofertę” | `.btn.btn-primary` |
| `section.hero` (h1 + opis) | `.page-head` |
| `form.search` (input + select + przycisk) | `form.search-main[role=search]` + `.select` dla miasta, przycisk „Szukaj” w stylu `.search-main button` |
| `main.layout` (filtry + lista) | `.layout-results` (lista po lewej, filtry po prawej; na telefonie filtry nad listą) |
| `aside.filters` | `aside.panel-filters` + `form[data-filter-for]` |
| `fieldset` / `legend` | `fieldset` / `legend` systemu |
| `label > input[type=checkbox]` | `.checkbox` + `.opt-n` (liczba pasujących ofert) |
| `.list-head` h2 „Najnowsze oferty” | nagłówek sekcji + `.count` (liczba widocznych ofert) |
| „Sortuj: najnowsze · widełki” (linki) | `.tabs` z linkami `<a>` (aktywny ma `aria-current`) |
| `ul.jobs` | `ul.stack[data-list]` |
| `li.job` | `.card` (`.card-body`, `.card-head`) |
| `.logo-circle` | `.avatar.avatar-xl` (kwadrat, kolory `--avatar-1…4`) |
| `h3 > a` | `.card-head h3 a` |
| `.company` | `.card-sub` |
| `.salary` | `.amount` (kwota pikselowym fontem + `<small>zł netto B2B</small>`) |
| `.salary.muted` „Wynagrodzenie do uzgodnienia” | `.amount.is-empty` |
| `.tags span` | `.chips > .chip` |
| `.pill` „Polecana” | `.badge.badge-new` + ikona `i-star` (żółty = „wyróżnione”) |
| `.job.featured` (różowa obwódka) | brak osobnej ramki; wyróżnienie niesie tylko znacznik „Polecana” |
| `button.save` ♡/♥ | `.icon-btn.is-boxed` + `.icon.i-heart-outline` / `.i-heart` |
| `nav.pager` | `nav > ul.pagination` |
| `section.newsletter` (gradient) | `.panel` + `.panel-head` |
| label + `input[type=email]` | `.field` (etykieta nad polem) + `.req` |
| `label.consent` | `.checkbox` + `.req` |
| `.btn-gradient` „Zapisz się” | `.btn.btn-primary` |
| `footer.footer` | `.site-footer` |
| — (nowe) | `.empty[data-empty-for]` „Brak ofert dla tych filtrów” + „Wyczyść filtry” |

## Na co zwrócić uwagę

1. **Filtry działają teraz w przeglądarce.** W starej wersji checkboxy nie były w żadnym formularzu i nic nie robiły. Po migracji wyglądały jak działające kontrolki, więc je podłączyłem (`list-controls.js`): filtrują 4 oferty na stronie, a liczniki się aktualizują.
   - Przez to „Mid” ma 0 ofert.
   - Oferty 102 (Backend Go) i 104 (Lead Unity) nie mają w treści poziomu, a 102 również trybu pracy. Nie dopisywałem ich, żeby nie wymyślać danych.
   - Jeśli filtry mają działać na serwerze, backend powinien wypisać `data-f-poziom` / `data-f-tryb` na `li.job` albo zamienić formularz na `action="/szukaj"`.
2. **Sortowanie dalej jest po stronie serwera** (linki `?sort=…`). Mały skrypt zaznacza tylko aktywną zakładkę na podstawie adresu; domyślnie „najnowsze”.
3. **Zapisane oferty nie są odtwarzane po przeładowaniu.** Tak było też w starej wersji: skrypt zapisuje do `localStorage`, ale nic go nie odczytuje przy wejściu na stronę. Zostawiłem to bez zmian. Mogę dopisać odczyt, jeśli chcesz.
4. **Hero i newsletter są teraz wewnątrz `<main>`.** Kolejność w DOM: lista ofert przed filtrami, tak wymaga układ `.layout-results`.

**Elementy spoza systemu (kandydaci, design.md §0.5):**
- Wyszukiwarka z polem wyboru miasta. Sam `.search-main` ma tylko pole tekstowe i wąski przycisk, więc w stylach ekranu dodałem lewą ramkę dla selecta i szerszy przycisk z tekstem „Szukaj”, a na telefonie zawijanie w dwa rzędy.
- Wyróżniona karta (`.card` z cieniem `--featured`) — tego w systemie nie ma, więc wyróżnienie niesie sam znacznik.

## Wyniki sprawdzeń

- `check_screen.py`: **OK — brak uwag** (0 ERROR, 0 WARN).
- `render_check.py`:
  - **1280 px i 390 px:** szerokość dokumentu bez poziomego przewijania, Archivo i Press Start 2P ładują się z polskimi znakami.
  - **Test klikania:** 10 z 14 kontrolek kliknięto, 0 martwych.
  - Obejrzałem oba zrzuty. Na telefonie znacznik „Polecana” ściskał tytuł, więc poprawiłem to zawijaniem nagłówka karty.
- **Ręcznie w przeglądarce (lokalny serwer):**
  - Zapis oferty przełącza klasę, ikonę, `aria-label` i `localStorage['saved-102']` (`'1'` → `''`).
  - Filtr „Zdalnie” zostawia 1 ofertę i licznik pokazuje 1; „Mid” pokazuje pusty stan.
  - Pusty newsletter jest blokowany z błędem przy polu. Wypełniony wysyła pola `email` i `zgoda`.
  - Wyszukiwarka wysyła `q` i `miasto`.
- **Nie sprawdzałem:** prawdziwych odpowiedzi serwera (`/szukaj`, `/newsletter`, `?sort`, `?page`), bo strona jest statyczna.
