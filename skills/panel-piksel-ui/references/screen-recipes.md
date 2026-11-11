# Przepisy ekranów — Panel & Piksel

Każdy przepis: **cel → struktura → „głośny” element → HTML szkieletu → pułapki**. Szkielety wstawiasz do `<main>` w `assets/starter.html`. Klasy pochodzą z `assets/components.css`; szczegóły komponentów w `design-system.md` §6.

Spis: 1. Katalog (strona główna) · 2. Kategoria · 3. Wyniki z filtrami · 4. Szczegóły encji · 5. Ranking / leaderboard · 6. Cennik / pakiety · 7. Profil (firmy, sprzedawcy, gracza) · 8. Formularz · 9. Pusty stan / 404 · 10. Panel użytkownika (tabela własnych pozycji)

---

## 1. Katalog — strona główna

**Cel:** przegląd kategorii i szybkie wejście w listy. **Głośny element:** jeden panel `.is-featured` (np. „Świeżo dodane”).

```html
<section class="section" aria-labelledby="h-kat">
  <div class="section-title"><h2 id="h-kat">Kategorie</h2><a class="btn btn-secondary" href="/kategorie">Wszystkie kategorie</a></div>
  <div class="grid-panels">
    <section class="panel" aria-labelledby="k1">
      <header class="panel-head"><h2 id="k1">Frontend</h2><span class="count">128</span></header>
      <p class="panel-motto">„Krótki, zabawny opis kategorii”</p>
      <ol class="list">
        <li><a href="/o/1"><span class="list-n">1.</span><span class="avatar" style="--av:var(--avatar-1)">PF</span><span class="list-name">Senior Frontend Developer</span><span class="list-value"><span class="amt-full">18 000–24 000</span><span class="amt-short" aria-hidden="true">18–24 tys.</span></span></a></li>
        <!-- 5–8 pozycji -->
      </ol>
      <a class="panel-more" href="/k/frontend">Zobacz wszystkie</a>
    </section>
    <section class="panel is-featured" aria-labelledby="k-new">
      <header class="panel-head"><h2 id="k-new">Świeżo dodane</h2><span class="count">8</span></header>
      <ol class="list">
        <li><a href="/o/9"><span class="list-n">1.</span><span class="avatar" style="--av:var(--avatar-6)">DK</span><span class="list-name">Game Designer</span><span class="badge badge-new badge-sm">Nowa</span></a></li>
      </ol>
      <a class="panel-more" href="/nowe">Zobacz wszystkie</a>
    </section>
    <!-- kolejne panele -->
  </div>
</section>
```

**Pułapki:** nie więcej niż jeden `.is-featured`; panele mają różną długość — to normalne (`align-items: start`); liczby w `.count` i `.list-value`, nie w nazwie; kwota w wierszu zawsze jako para `.amt-full` + `.amt-short` (skrót „18–24 tys.” pokazuje się < 600 px, żeby nie ucinać nazw).

## 2. Kategoria

**Cel:** pełna lista jednej kategorii + nawigacja do pokrewnych. **Głośny element:** brak lub wyróżniony panel boczny.

```html
<div class="layout-main-side">
  <section class="panel" aria-labelledby="h-list">
    <header class="panel-head"><h2 id="h-list">Wszystkie oferty</h2><span class="count">128</span></header>
    <ol class="list"><!-- wszystkie pozycje --></ol>
  </section>
  <aside class="stack" aria-label="Inne kategorie">
    <section class="panel"><header class="panel-head"><h2>Backend</h2><span class="count">96</span></header>
      <p><span class="avatar" style="--av:var(--avatar-2)">8B</span> <span class="avatar" style="--av:var(--avatar-3)">KQ</span> <span class="chip-more">+54</span></p>
    </section>
  </aside>
</div>
<ul class="pagination" aria-label="Strony"><li><span aria-current="page">1</span></li><li><a href="?p=2">2</a></li></ul>
```

## 3. Wyniki wyszukiwania z filtrami

**Cel:** porównanie wielu pozycji i zawężanie. **Głośny element:** zwykle żaden (praca, nie scena) — ewentualnie badge „Nowa” na kartach.

```html
<div class="layout-results">
  <div class="stack">
    <div class="section-title"><h2>42 oferty</h2>
      <div class="tabs" role="group" aria-label="Sortuj oferty"><button type="button" aria-pressed="true">Najnowsze</button><button type="button" aria-pressed="false">Najwyższe widełki</button></div>
    </div>
    <article class="card">
      <span class="avatar avatar-xl" style="--av:var(--avatar-1)">PF</span>
      <div class="card-body">
        <div class="card-head"><h3><a href="/o/1">Senior Frontend Developer</a></h3><span class="badge badge-new">Nowa</span></div>
        <p class="card-sub">Pixel Forge · Kraków / zdalnie</p>
        <p class="amount">18 000–24 000 <small>zł netto B2B</small></p>
        <div class="chips"><span class="chip">React</span><span class="chip">TypeScript</span><span class="chip-more">+2</span></div>
      </div>
    </article>
  </div>
  <aside class="panel-filters" aria-label="Filtry">
    <h2>Filtry</h2>
    <label class="field"><span class="sr-only">Słowa kluczowe</span><input type="search" placeholder="Słowa kluczowe"></label>
    <fieldset><legend>Tryb pracy</legend>
      <label class="checkbox"><input type="checkbox"> Zdalnie</label>
    </fieldset>
    <button class="btn btn-primary btn-full" type="button">Pokaż 42 oferty</button>
  </aside>
</div>
```

**Działające sortowanie i filtry** (`assets/list-controls.js`, dołącz przed `</body>`). Wartości trzymaj w atrybutach kart, a kontrolki połącz identyfikatorem listy:

```html
<h2><span data-count-for="oferty" data-count-forms="oferta|oferty|ofert">8 ofert</span></h2>
<!-- sortowanie = grupa przycisków przełączających (nie zakładki: nie ma paneli treści) -->
<div class="tabs" role="group" aria-label="Sortuj oferty" data-sort-for="oferty">
  <button type="button" aria-pressed="true"  data-sort-key="date"   data-sort-dir="desc">Najnowsze</button>
  <button type="button" aria-pressed="false" data-sort-key="salary" data-sort-dir="desc">Najwyższe widełki</button>
  <button type="button" aria-pressed="false" data-sort-key="order">Trafność</button>
</div>
<p class="active-filters">Aktywne filtry: <span data-active-for="oferty"></span></p>
<div class="stack" data-list="oferty">
  <article class="card" data-item data-sort-date="20261109" data-sort-salary="27000" data-n-salary="20000 27000"
           data-f-tryb="zdalnie" data-f-poziom="senior" data-f-tech="unity csharp">…</article>
  <!-- brak widełek: bez data-sort-salary / data-n-salary — trafi na koniec sortowania -->
</div>
<div class="empty" data-empty-for="oferty" hidden><h2>Brak ofert dla tych filtrów</h2><button class="btn btn-secondary" type="button" data-clear-for="oferty">Wyczyść filtry</button></div>

<form class="panel-filters" data-filter-for="oferty">
  <label class="checkbox"><input type="checkbox" name="tryb" value="zdalnie"> Zdalnie <span class="opt-n">4</span></label>
  <input type="number" data-min="salary"> <input type="number" data-max="salary">
  <label class="checkbox"><input type="checkbox" data-require="salary"> Tylko z widełkami</label>
  <button class="btn btn-primary btn-full" type="submit">Pokaż <span data-count-for="oferty" data-count-forms="ofertę|oferty|ofert">8 ofert</span></button>
</form>
```

Ta sama nazwa checkboxów = LUB, różne nazwy = I. Liczby przy opcjach (`.opt-n`) policz z faktycznych kart na stronie.

**Pułapki:** link w tytule karty dziedziczy kolor — dopisz w `<style id="screen">` `.card-head h3 a { color: var(--ink); text-decoration: none; }` + podkreślenie na hover; brak kwoty → `.amount.is-empty`; max 4 chipy + `.chip-more`.

## 4. Szczegóły encji (oferta, produkt, przedmiot)

**Cel:** decyzja (aplikuj/kup). **Głośny element:** blok akcji z ceną/kwotą lub ilustracja.

```html
<div class="layout-main-side">
  <article class="stack">
    <div class="card">
      <span class="avatar avatar-xl" style="--av:var(--avatar-1)">PF</span>
      <div class="card-body"><div class="card-head"><h2>Senior Frontend Developer</h2><span class="badge badge-new">Nowa</span></div><p class="card-sub">Pixel Forge · Kraków / zdalnie</p></div>
    </div>
    <dl class="facts">
      <div><dt>Widełki</dt><dd class="num">18 000–24 000 zł</dd></div>
      <div><dt>Tryb</dt><dd>Zdalnie</dd></div>
      <div><dt>Poziom</dt><dd>Senior</dd></div>
    </dl>
    <section class="panel prose"><h2>O projekcie</h2><p>…</p><ul class="list-square"><li>…</li></ul></section>
  </article>
  <aside class="stack">
    <section class="panel">
      <p class="amount">24 000 <small>zł / mies.</small></p>
      <button class="btn btn-primary btn-full" type="button">Aplikuj teraz</button>
      <button class="btn btn-secondary btn-full" type="button" style="margin-top:12px">Zapisz</button>
    </section>
    <section class="panel"><header class="panel-head"><h2>Podobne oferty</h2><span class="count">5</span></header><ol class="list"><!-- … --></ol></section>
  </aside>
</div>
```

**Pułapki:** długi opis wyłącznie Archivo (`.prose`); jeśli akcja niedostępna — `aria-disabled` + `.lock` + `.btn-reason`. Przycisk „Zapisz” jako działający przełącznik: `<button class="btn btn-secondary btn-full" type="button" aria-pressed="false" data-label-on="Zapisano" data-label-off="Zapisz ofertę">Zapisz ofertę</button>` + `list-controls.js`.

## 5. Ranking / leaderboard / high score

**Cel:** kto prowadzi i jak się zmienia. **Głośny element:** podium (jedno na stronę).

```html
<div class="page-head"><div><h1>Ranking pracodawców</h1></div>
  <div class="tabs" role="tablist" aria-label="Okres"><button role="tab" aria-selected="true">Ten tydzień</button><button role="tab" aria-selected="false">Ogółem</button></div></div>
<ol class="podium" aria-label="Podium">
  <li class="podium-1"><span class="avatar avatar-xl" style="--av:var(--avatar-1)">PF</span><b>Pixel Forge</b><span class="podium-pts">1 980</span><span class="podium-step">1</span></li>
  <li class="podium-2">…<span class="podium-step">2</span></li>
  <li class="podium-3">…<span class="podium-step">3</span></li>
</ol>
<div class="section table-wrap">
  <table class="table">
    <caption class="sr-only">Pełny ranking</caption>
    <thead><tr><th scope="col">#</th><th scope="col">Firma</th><th scope="col" class="num" aria-sort="descending"><span class="sorted">Punkty</span></th><th scope="col" class="num">Zmiana</th></tr></thead>
    <tbody>
      <tr><td><span class="rank">4</span></td><td class="name"><span class="cell-entity"><span class="avatar" style="--av:var(--avatar-4)">ŁŻ</span><a href="/f/4">Łódzkie Żetony</a></span></td><td class="num">720</td><td class="num delta-up">2</td></tr>
    </tbody>
  </table>
</div>
```

**Pułapki:** tabela zaczyna się od miejsca 4 (1–3 są na podium) albo pokazuje wszystkie z `.rank-1/2/3`; liczby do prawej; zmiana zawsze ze strzałką. **Kolejność rankingu jest stała** — kolumna wyniku dostaje statyczne `.sorted`, nie przycisk. Jeśli chcesz dodatkowo sortować po innej kolumnie (np. liczbie rozgrywek), a wiersze są generowane z danych z paginacją, oznacz tabelę `data-sort-manual`, sortuj tablicę danych w kodzie (przez wszystkie strony, nie tylko bieżącą), ustawiaj `aria-sort` na `<th>` i wracaj na stronę 1.

## 6. Cennik / pakiety

**Cel:** wybór pakietu. **Głośny element:** rekomendowany pakiet (`.panel.is-featured` wokół lub badge „Polecany”).

```html
<div class="grid-panels">
  <section class="panel is-featured">
    <div class="tier tier-legendary"><span class="tier-name">Legendarny</span><span class="tier-price">899 zł</span><span class="tier-desc">Podium + wyróżniony panel 30 dni</span></div>
    <ul class="list-square"><li>…</li></ul>
    <button class="btn btn-primary btn-full" type="button">Wybierz Legendarny</button>
  </section>
  <section class="panel">
    <div class="tier tier-epic">…</div><ul class="list-square"><li>…</li></ul>
    <button class="btn btn-secondary btn-full" type="button">Wybierz Epicki</button>
  </section>
  <!-- tier-rare, tier-common -->
</div>
```

**Pułapki:** tylko jeden przycisk główny (przy rekomendowanym), reszta drugorzędne; nazwy tierów: Legendarny / Epicki / Rzadki / Zwykły (lub odpowiedniki domeny), kolor zawsze z nazwą.

## 7. Profil (firma, sprzedawca, gracz)

**Cel:** zaufanie + lista pozycji tej encji. **Głośny element:** pozycja w rankingu (`.rank-1/2/3`) lub ilustracja.

Struktura: `.card` z `.avatar-xl`, nazwą, `.badge-seg` (np. „Ranking | #2”) → `.facts` (liczby: oferty, odpowiedzi, rok założenia) → `.tabs` (Oferty / O firmie / Opinie) → `.panel` z `.list` pozycji → `.prose`.

## 8. Formularz (dodaj ofertę, kontakt, ustawienia)

**Cel:** bezbłędne wypełnienie. **Głośny element:** żaden.

```html
<form class="panel stack" style="max-width:640px;display:grid;gap:16px">
  <h2>Dodaj ofertę</h2>
  <div class="field"><label for="t">Stanowisko <span class="req" aria-hidden="true">*</span></label><input id="t" name="title" required></div>
  <div class="field"><label for="lvl">Poziom</label><div class="select"><select id="lvl"><option>Junior</option><option selected>Mid</option><option>Senior</option></select></div></div>
  <fieldset><legend>Tryb pracy</legend>
    <label class="radio"><input type="radio" name="mode" value="zdalnie" checked>Zdalnie</label>
    <label class="radio"><input type="radio" name="mode" value="hybrydowo">Hybrydowo</label></fieldset>
  <div class="field"><label for="d">Opis</label><textarea id="d" maxlength="2000" data-count="d-n" aria-describedby="d-n"></textarea><p class="field-count" id="d-n"></p></div>
  <div class="field"><span id="logo-l" style="display:block;margin:0 0 6px;font:700 14px var(--font-sans)">Logo firmy</span>
    <label class="upload" data-max-mb="2"><input type="file" id="logo" accept=".png,.svg" aria-labelledby="logo-l" aria-describedby="logo-h">
      <span class="icon icon-lg i-upload" aria-hidden="true"></span><span class="upload-title">Przeciągnij plik albo <u>wybierz z dysku</u></span><span class="upload-hint" id="logo-h">PNG lub SVG, do 2 MB</span></label>
    <p class="field-error" data-upload-error hidden></p><ul class="file-list" data-files-for="logo"></ul></div>
  <div class="notice notice-info"><span class="notice-icon"><span class="icon i-info" aria-hidden="true"></span></span><div class="notice-body"><strong class="notice-title">Wskazówka</strong><p>Oferty z widełkami dostają 2× więcej odpowiedzi.</p></div></div>
  <button class="btn btn-primary" type="submit">Opublikuj</button>
</form>
<!-- wymaga: icons.css + ui-controls.js -->
```

**Pułapki:** etykieta zawsze widoczna nad polem (`.field label`); wymagane = `required` + `<span class="req">*</span>`; błąd = `.field.is-error` + `.field-error` + `aria-invalid` + `aria-describedby` (§6.13); po wysłaniu potwierdzenie `ppToast({status:'success', …})`; przycisk wysyłki zablokowany tylko z powodem (`.btn-reason`). Przełącznik `.switch` tylko dla ustawień działających od razu — w formularzu z „Zapisz” użyj checkboxa.

## 9. Pusty stan / 404 / brak wyników

```html
<div class="empty">
  <!-- opcjonalnie: <img class="empty-art" src="…pixel-art.png" alt=""> (paleta SNES) -->
  <h2>Brak wyników</h2>
  <p>Spróbuj usunąć część filtrów albo zmienić słowa kluczowe.</p>
  <button class="btn btn-primary" type="button">Wyczyść filtry</button>
</div>
```

To dobre miejsce na jedyną ilustrację pixel-art na ekranie (głośny element).

## 10. Panel użytkownika (tabela własnych pozycji)

**Cel:** zarządzanie (status, statystyki, akcje). **Głośny element:** żaden lub `.callout` z najważniejszą informacją.

Struktura: `.page-head` z przyciskiem głównym („Dodaj ofertę”) → `.tabs` statusów (Aktywne / Szkice / Wygasłe) → `.table-wrap` z kolumnami: nazwa (`.name`), status (`.badge`), liczby (`.num`: wyświetlenia, aplikacje), akcje (`.btn-secondary` lub link) → `.pagination`.

Sortowalne kolumny (wiersze w HTML) — przyciski w nagłówkach + skrypt systemu:

```html
<th scope="col" class="num"><button type="button" class="sort">Wyświetlenia</button></th>
<th scope="col" class="num"><button type="button" class="sort">Wygasa</button></th>
<!-- przed </body>: -->
<script src="./panel-piksel/table-sort.js"></script>
```

Daty w formacie dd.mm.rrrr i liczby z odstępami są rozpoznawane same; gdy komórka ma dodatkowy tekst (np. „za 2 dni”), podaj `data-sort-value`.

**Pułapki:** statusy jako `.badge` z tekstem (nie sam kolor); akcje w tabeli jako drugorzędne — przycisk główny tylko w nagłówku strony.

## 11. Wspólne stany i warianty (v1.6)

- **Przycisk powtarzany w każdej pozycji** (stopka karty, wiersz tabeli, koszyk): `.btn-compact` (36 px). Akcja sekcji zostaje 44 px.
  `<div class="card-foot"><span>dodano 2 godz. temu</span><button class="btn btn-secondary btn-compact" type="button" aria-pressed="false" data-label-on="Zapisano" data-label-off="Zapisz">Zapisz</button></div>`
- **Rzadkość / pakiet w karcie, tabeli, koszyku:** zawsze `<span class="tier-tag tier-epic">Epicki</span>` — nie badge z kwadratem.
- **Zakładki vs przełącznik:** `role="tablist"`/`role="tab"`/`aria-selected` tylko gdy zmienia się panel treści (okres rankingu, statusy); sortowanie → `role="group"` + `aria-pressed`.
- **Błąd pola:** `<div class="field is-error"><label for="x">…</label><input id="x" aria-invalid="true" aria-describedby="x-err"><p class="field-error" id="x-err">Co poprawić.</p></div>`
- **Ładowanie:** przycisk `.is-loading` + `aria-disabled="true"` + `aria-busy="true"`; lista: wiersze `.skel-row` z `.skel-n`, `.skel-av`, `.skel` (kontener `aria-busy="true"`); błąd wczytania: `.load-error` z `role="alert"` i „Spróbuj ponownie”; błąd w treści: `.callout.callout-danger`.
- **Tryb ciemny:** `<html lang="pl" data-theme="dark">` (lub `auto`). Działa tylko wtedy, gdy style ekranu używają tokenów — żadnych wpisanych `#00021C`, `#FFFFFF`, `#F0EDD8`; ramki `var(--border)` / `var(--line)`, cienie `var(--shadow-*)`, tekst na jasnych wypełnieniach `var(--on-light)`.
- **Filtry na telefonie (v1.7):** formularz filtrów dostaje `id` i `data-drawer-form`; obok sortowania `<button class="btn btn-secondary btn-compact filters-toggle" type="button" data-dialog-open="filtry"><span class="icon i-filter" aria-hidden="true"></span>Filtry</button>`; na końcu `<body>`: `<dialog class="drawer" id="filtry" data-drawer-source="ID-formularza" aria-labelledby="filtry-h"><div class="modal-head"><h2 id="filtry-h">Filtry</h2><button class="icon-btn" type="button" data-dialog-close aria-label="Zamknij filtry"><span class="icon i-close" aria-hidden="true"></span></button></div><div class="modal-body" data-drawer-slot></div></dialog>`.
- **Zwijana nawigacja (v1.7):** w `.site-header` przed `<nav>`: `<button class="icon-btn is-boxed nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span class="icon i-menu" aria-hidden="true"></span></button>` i `<nav class="site-nav" id="nav" data-collapsible>`.
- **Ikony (v1.7):** `<span class="icon i-NAZWA" aria-hidden="true"></span>` (kolor tekstu) i `<span class="sprite s-NAZWA" aria-hidden="true"></span>` (przedmiot z gry). Lista w `examples/ikony.html`. Żadnych emoji ani obcych zestawów ikon.
- **Powiadomienia, okno, menu, podpowiedź:** wzory w `examples/komponenty.html` (sekcje „Statusy i powiadomienia”, „Nakładki”).
- **Sklep / koszyk (v1.10):** koszyk to `.panel` z wierszami (nazwa + `.tier-tag`, pod spodem `.stepper` i cena), `.facts` z sumą i brakującą kwotą, `.progress` z odsetkiem posiadanych środków i przycisk zakupu zablokowany z powodem. Nie twórz własnych przycisków −/+ ani pasków — wzór: ekran sklepu S13, design.md §6.23.
- **Siatka produktów (v1.11):** `ul` z siatką `repeat(auto-fill, minmax(210px, 1fr))`, w niej `.card.card-vertical`: `.card-art` ze sprite’em `-xl` → `h3` → `.tier-tag` → `.card-meta` → `.card-foot` z `.card-price` i `.btn-compact`. Saldo w nagłówku: `.badge.badge-seg` ze sprite’em waluty (design.md §6.24) — bez klasy `.wallet`.
- **Wyszukiwarka z miastem / kategorią (v1.11):** `<form class="search-main has-select" role="search">` → `input` → `<div class="select"><select name="miasto" aria-label="Miasto">…</select></div>` → `<button type="submit">Szukaj</button>`. Jedna lista; więcej filtrów → `.panel-filters`.
- **Ranking z krajami (v1.11):** `<td><span class="cc" aria-hidden="true">PL</span>Polska</td>` — nigdy flagi-emoji.
- **Karta oferty (v1.10):** atrybuty „Poziom / Tryb / Dodano” w `ul.card-meta` pod podtytułem; liczby przy opcjach filtrów w pustym `<span class="opt-n"></span>` — wypełnia je skrypt; widełki od–do w `.range`.
- **Formularz (v1.8):** zawsze `<form data-validate>`; dłuższy niż ~8 pól → kroki (`data-wizard`, wzór w `examples/wzorce.html#formularz`).
- **Panel pracodawcy / tabela własnych pozycji (v1.8):** kafelki `.stats` na górze, tabela `data-selectable` + `.bulk-bar`, wykresy `figure.chart` pod spodem (wzór: `examples/wzorce.html#zaznaczanie`, `#wykresy`).
- **Długie listy do przeglądania (v1.8):** `data-page-size` + `.load-more` zamiast paginacji.
- Wszystkie warianty i stany w działaniu: `examples/komponenty.html`, wzorce: `examples/wzorce.html`.

