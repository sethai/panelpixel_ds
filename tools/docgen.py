"""Generator: Panel & Piksel — dokumentacja komponentów dla designerów (v2). Uruchom: python3 tools/docgen.py
Dane kart K21–K29 w tools/doc_cards.py; wycinki w docs/evidence (tools/crops.js)."""
import base64, html, json, os
D2 = os.path.dirname(os.path.abspath(__file__)) + '/'

R = os.path.normpath(os.path.join(D2, '..')) + '/'
EV = R + 'docs/evidence/'
OUT = R + 'docs/panel-piksel-komponenty-v2.html'
CROPS = {c['id']: c for c in json.load(open(EV + 'crops.json'))}

# ---------- statusy ----------
ST = {'D': ('Potwierdzone w dokumentacji', 'd'), 'S': ('Szacunek z obrazu', 's'), 'R': ('Rekomendacja', 'r'),
      'P': ('Do potwierdzenia', 'p'), 'T': ('Do testu we wdrożeniu', 't')}
def st(k): return f'<span class="st st-{ST[k][1]}" title="{ST[k][0]}">{ST[k][0]}</span>'
def tag(text):  # replace [D] [S] [R] [P] [T] markers with badges
    for k in ST:
        text = text.replace(f'[{k}]', st(k))
    return text
def table(head, rows, cls=''):
    h = f'<div class="tw"><table class="{cls}"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in head) + '</tr></thead><tbody>'
    for r in rows:
        h += '<tr>' + ''.join(f'<td>{tag(c)}</td>' for c in r) + '</tr>'
    return h + '</tbody></table></div>'
def img(cid, cap):
    c = CROPS[cid]
    data = base64.b64encode(open(EV + c['crop'].split('/')[-1], 'rb').read()).decode()
    return (f'<figure class="ev" id="ev-{cid}"><img src="data:image/png;base64,{data}" alt="{html.escape(cap)}">'
            f'<figcaption><b>{cid}</b> · {html.escape(cap)}<br><span class="meta">{c["source"]} · {html.escape(c["file"])} · selektor <code>{html.escape(c["selector"])}</code> · szerokość {c["viewport"]} px · stan: {html.escape(c["state"])}</span></figcaption></figure>')
def figs(*pairs, cols=2):
    return f'<div class="figs c{cols}">' + ''.join(img(a, b) for a, b in pairs) + '</div>'
def sw(hexv): return f'<span class="sw" style="background:{hexv}"></span><code>{hexv}</code>'

SOURCES = [
    ('S01', 'design.md v1.9.0', 'design.md', 'Specyfikacja systemu: zarządzanie §0, tokeny §2–4, komponenty i wzorce §6, treści §6A, dostępność §8, kod §9'),
    ('S02', 'tokens.css + components.css + icons.css v1.9', 'skills/panel-piksel-ui/assets/', 'Implementacja referencyjna stylów (to samo co design.md §9)'),
    ('S03', 'list-controls.js, table-sort.js, ui-controls.js, charts.js', 'skills/panel-piksel-ui/assets/', 'Zachowanie: listy, tabele, formularze, nakładki, powiadomienia, wykresy'),
    ('S04', 'Studium kierunku (sekcja Komponenty)', 'research/direction-study.html', 'Macierz stanów przycisku, warianty blokady, badge, detale graficzne'),
    ('S05', 'Porównanie palet', 'research/palette-comparison.html', 'Uzasadnienie palety SNES + akcenty NES, kontrasty'),
    ('S10', 'Landing page portalu (PikselPraca)', 'screens/landing/landing-portal-pracy.html', 'Hero, kategorie, karty ofert, kroki, tabela rankingu, pakiety, CTA'),
    ('S11', 'Lista ofert z filtrami (LevelUp Jobs)', 'skills/panel-piksel-ui-workspace/iteration-1/job-board-listing-filters/…/levelup-jobs-wyniki.html', 'Karty, zakładki sortowania, panel filtrów, aktywne filtry, pusty stan'),
    ('S12', 'Leaderboard (Kosmiczny Kret)', '…/leaderboard-high-scores/…/leaderboard.html', 'Podium, tabela sortowalna, zakładki okresu, paginacja'),
    ('S13', 'Sklep z przedmiotami (PikselBazar)', '…/game-item-shop/…/sklep-przedmiotow.html', 'Karty przedmiotów, rzadkość, koszyk, blokada zakupu'),
    ('S14', 'Katalog (PixelHub)', '…/catalog-home-directory/…/index.html', 'Siatka paneli kategorii, panel wyróżniony'),
    ('S15', 'Szczegóły oferty (Smocza Jama Studio)', '…/job-offer-detail/…/oferta-senior-unity-developer.html', 'Fakty, panel akcji z blokadą, przełącznik „Zapisz”'),
    ('S06', 'Rejestr komponentów i wersja', 'skills/panel-piksel-ui/assets/components.json, VERSION', 'Status każdej rodziny (stabilny / testowy / kandydat / wycofywany), wersja 1.9.0'),
    ('S07', 'Decyzje v1.1', 'docs/decyzje-v1-1.html', 'Porównania wariantów i wybory z 2026-11-10'),
    ('S20', 'Katalog komponentów', 'skills/panel-piksel-ui/examples/komponenty.html', 'Wszystkie komponenty i stany, jasny/ciemny, formularze, nakładki, powiadomienia'),
    ('S21', 'Wzorce', 'skills/panel-piksel-ui/examples/wzorce.html', 'Formularz w krokach, zaznaczanie wierszy, ładowanie, wykresy'),
    ('S22', 'Katalog ikon', 'skills/panel-piksel-ui/examples/ikony.html', 'Ikony interfejsu, kolorowe wersje, przedmioty z gier'),
    ('S16', 'Panel pracodawcy (PikselPraca)', '…/employer-dashboard-table/…/panel-pracodawcy.html', 'Tabele w zakładkach, znaczniki pakietów i statusu, callout'),
]

# ---------- fundamenty ----------
FOUND = f'''
<section class="part" id="fundamenty"><h2>Fundamenty wspólne dla wszystkich rodzin</h2>
<p class="small">Wartości ze specyfikacji S01 §2–§5 i implementacji S02. Karty komponentów odsyłają tu zamiast powtarzać tokeny. Wszystkie nazwy tokenów są nazwami z S01/S02 {st('D')}.</p>
<h3>Kolor</h3>
{table(['Token', 'Wartość', 'Rola', 'Kontrast (S01 §2.1, wyliczony z hex)'], [
 ['<code>--paper</code>', sw('#F0EDD8'), 'tło strony', '—'],
 ['<code>--surface</code>', sw('#FFFFFF'), 'panele, karty, pola (jedyny kolor spoza palety SNES)', '—'],
 ['<code>--ink</code>', sw('#00021C'), 'tekst, ramki, cienie', '17.4:1 na paper, 20.5:1 na surface [D]'],
 ['<code>--ink-2</code> / <code>--ink-3</code>', sw('#1C284D') + ' ' + sw('#2D5280'), 'opisy / meta, numery wierszy', '14.4:1 / 8.0:1 na surface [D]'],
 ['<code>--action</code> + <code>--action-edge</code>', sw('#17735F') + ' ' + sw('#00021C'), 'jedyny kolor akcji + dolna krawędź klawisza', 'biały 5.7:1 [D]'],
 ['<code>--highlight</code>', sw('#F7C93E'), '„Nowa”, wyróżnione, zaznaczenie checkboxa', 'ink 13.0:1 [D]'],
 ['<code>--link</code> = <code>--focus</code>', sw('#2469B3'), 'linki, okruszki, pierścień fokusu', '5.6:1 na surface, 4.8:1 na paper [D]'],
 ['<code>--focus-deco</code>', sw('#0BAFE6'), 'kolorowy cień wyszukiwarki — dekoracja', '2.2:1 — nie do fokusu [D]'],
 ['<code>--danger</code>', sw('#D9214F'), 'błąd, wygasanie', '4.9:1 [D]'],
 ['<code>--featured</code>', sw('#D94C87'), 'cień wyróżnionego panelu', 'dekoracja'],
 ['<code>--chip</code> / <code>--chip-more</code>', sw('#A3CCD9') + ' ' + sw('#F0BB90'), 'tło chipów / licznik „+N”', 'ink ≥ 11:1 [D]'],
 ['<code>--disabled-bg / -ink / -line</code>', sw('#BCBCBC') + ' ' + sw('#1C284D') + ' ' + sw('#2D5280'), 'przycisk zablokowany (wariant A)', 'tekst 7.6:1 [D]'],
 ['<code>--podium --gold --silver --bronze</code>', sw('#0000BC') + ' ' + sw('#F8B800') + ' ' + sw('#BCBCBC') + ' ' + sw('#E45C10'), 'akcenty NES — tylko ranking', 'złoto na podium 6.9:1 [D]'],
 ['<code>--tier-legendary/epic/rare/common</code>', sw('#AC7C00') + ' ' + sw('#6844FC') + ' ' + sw('#0078F8') + ' ' + sw('#7C7C7C'), 'akcenty NES — pakiety', '3.7–5.5:1 na bieli [D]'],
 ['<code>--status-info/success/warning/error</code> (v1.7)', sw('#2469B3') + ' ' + sw('#17735F') + ' ' + sw('#E45C10') + ' ' + sw('#D9214F'), 'statusy komunikatów — kafelek ikony i krawędź; znak <code>--on-status-*</code>', 'znak 4.9–5.7:1 [D]'],
 ['<code>--chart-single</code>, <code>--chart-1…4</code> (v1.10)', sw('#2D5280') + ' · ' + sw('#B36159') + ' ' + sw('#1BA683') + ' ' + sw('#A6216E') + ' ' + sw('#119955'), 'jedna seria · kategorie w stałej kolejności (bez kolorów pakietów i statusów)', 'sprawdzone validate_palette.js, jasny i ciemny [D]'],
 ['<code>--line</code>, <code>--shadow-color</code>, <code>--on-light</code>, <code>--row-hover</code>, <code>--row-selected</code>', '—', 'ramki, cienie, tekst na jasnych wypełnieniach, wiersze tabeli — osobno od tekstu dla trybu ciemnego', '[D] v1.6–1.8'],
 ['<code>--avatar-1…6</code>', sw('#17735F') + ' ' + sw('#2469B3') + ' ' + sw('#993649') + ' ' + sw('#732866') + ' ' + sw('#00021C') + ' ' + sw('#D9214F'), 'tła monogramów', 'biały tekst — do policzenia dla każdego [P]'],
])}
<h3>Typografia</h3>
{table(['Rola', 'Font', 'Rozmiar / interlinia', 'Weight / tracking', 'Status'], [
 ['display (hero)', 'Archivo', '40/44 (32/36 &lt; 600 px na S10)', '900 / −1px', '[D] S01 §3.2; wariant mobilny [S] S10'],
 ['h1 strony', 'Archivo', '24/32', '900 / −0.6px', '[D]'],
 ['tytuł panelu, sekcji, filtrów', 'Archivo', '18/28', '900 / −0.45px', '[D]'],
 ['tytuł karty', 'Archivo', '18/24', '800', '[D]'],
 ['body', 'Archivo', '16/24', '400', '[D]'],
 ['nazwa w wierszu listy', 'Archivo', '14/20', '600', '[D]'],
 ['small / opis', 'Archivo', '14/20', '400', '[D]'],
 ['label (badge, nagłówek tabeli)', 'Archivo', '12/16', '700–800, WERSALIKI, +0.3px', '[D]'],
 ['pixel-xs (liczniki, kwoty w wierszach)', 'Press Start 2P', '10/16', '400 / +1px', '[D]'],
 ['pixel-sm/md/lg (kwoty, punkty, miejsca)', 'Press Start 2P', '12 / 16 / 20–32', '400', '[D]'],
])}
<p class="small">Oba fonty z Google Fonts mają polskie znaki (subset latin-ext) — sprawdzone renderem „Zażółć gęślą jaźń” i <code>document.fonts.check</code> na wszystkich ekranach {st('D')}. Press Start 2P nie służy do akapitów ani etykiet formularzy {st('D')} S01 §3.3.</p>
<h3>Przestrzeń, kształt, głębia, ruch</h3>
{table(['Element', 'Wartość', 'Status / źródło'], [
 ['siatka odstępów', '4 · 8 · 12 · 16 · 24 · 32 · 48 px', '[D] S01 §4.1'],
 ['ramka', '2px solid --ink (wyjątek: lewa krawędź tieru 10 px)', '[D] S01 §4.3'],
 ['promień', '0 wszędzie; małe kontrolki: schodkowy narożnik 2 px (<code>--notch</code>, clip-path)', '[D]'],
 ['cienie', '--shadow-sm 2px 2px 0 · --shadow-md 4px 4px 0 · --shadow-lg 6px 6px 0 (bez rozmycia)', '[D] S01 §4.4'],
 ['wysokość przycisku', '44 px stała we wszystkich stanach (<code>--btn-h</code>)', '[D] S01 §6.1, S02'],
 ['wiersz listy', '32 px desktop · 40 px &lt; 600 px (<code>--row-h</code>)', '[D]'],
 ['kontener', 'max 1216 px, padding 24 px (16 px &lt; 600 px)', '[D] S01 §6.11'],
 ['ruch', '--motion-fast 60 ms (przyciski) · --motion-base 120 ms (menu, podpowiedź) · --motion-slow 200 ms (okno, szuflada, powiadomienie) · --ease-steps steps(3); prefers-reduced-motion → 0', '[D] S01 §4.5'],
 ['warstwy', '--z-sticky 10 · --z-dropdown 100 · --z-drawer 200 · --z-modal 300 · --z-toast 400 · --z-tooltip 500; okno i szuflada w warstwie top layer (dialog)', '[D] S01 §4.6'],
 ['punkty przełamania', '--bp-sm 600 · --bp-md 900 · --bp-lg 1200 px (w @media wpisane liczbami)', '[D] S01 §4.6'],
])}
<h3>Tryb ciemny i wysoki kontrast</h3><p class="small">Tryb ciemny: <code>data-theme="dark"</code> lub <code>"auto"</code> na <code>&lt;html&gt;</code> — te same komponenty, inne tokeny (papier #00021C, panele #1C284D, ramki kremowe, cienie niebieskie #2469B3), kontrasty w S01 §2.6 {st('D')}. Wysoki kontrast (Windows): prawdziwe ramki i zaznaczenia w kolorach systemowych, S01 §8 {st('D')}; nie sprawdzone na Windows {st('T')}.</p>''' + figs(('dark-list', 'Panel listy, karty i sortowanie w trybie ciemnym (S20)'), cols=1) + f'''
</section>'''

# ---------- karty ----------
CARDS = []
def card(id, name, purpose, anatomy, variants, props, tokens, dims, typo, behavior, dodont, a11y, sources, figures='', combos=''):
    CARDS.append(dict(id=id, name=name, purpose=purpose, anatomy=anatomy, variants=variants, props=props, tokens=tokens, dims=dims,
                      typo=typo, behavior=behavior, dodont=dodont, a11y=a11y, sources=sources, figures=figures, combos=combos))

A11Y_HEAD = ['Obszar', 'Ustalenie lub wymaganie', 'Dowód / status', 'Kryterium / wzorzec', 'Jak sprawdzić']
DD_HEAD = ['Zalecane — przykład', 'Niewskazane — przykład', 'Powód / status / źródło']
ANAT_HEAD = ['Część / rola', 'Wymagana / opcjonalna', 'Składnik / źródło', 'Co można zmienić / status']
VAR_HEAD = ['Oś', 'Wartość', 'Kiedy użyć', 'Co się zmienia', 'Ograniczenia / status / źródło']
PROP_HEAD = ['Właściwość / atrybut', 'Typ', 'Wartości pokazane / opisane', 'Domyślna', 'Efekt i zastosowanie', 'Zależności / status / źródło']
TOK_HEAD = ['Zastosowanie', 'Token', 'Tryb / wariant', 'Wartość', 'Źródło', 'Status']
DIM_HEAD = ['Elementy / krawędzie', 'Wariant', 'Wartość / relacja', 'Token', 'Reguła / źródło / dokładność']
TYP_HEAD = ['Rola tekstu', 'Styl', 'Font / weight', 'Rozmiar', 'Interlinia', 'Tracking', 'Kolor / zachowanie / status']

# K01 — Przycisk
card('K01', 'Przycisk',
 '''Wywołuje akcję (aplikuj, zapisz, wybierz pakiet, pokaż wyniki) albo prowadzi do kluczowej podstrony, gdy ma wygląd przycisku. <b>Główny</b> — jedna najważniejsza akcja w sekcji; <b>drugorzędny</b> — pozostałe. Do nawigacji w tekście używaj linku, do przełączania widoku listy — zakładek (K10), do statusu — badge (K02). {D} S01 §6.1.
 <br>Przełącznik („Zapisz” ↔ „Zapisano”) to wariant tego samego przycisku z <code>aria-pressed</code> {D} S01 §6.12, S03.''',
 [['kontener z ramką 2 px (rysowaną inset box-shadow)', 'wymagany', 'S02 <code>.btn</code>', 'kolor wg wariantu [D]'],
  ['schodkowy narożnik 2 px', 'wymagany', '<code>--notch</code> (clip-path)', 'nie zmieniać [D]'],
  ['dolna krawędź klawisza 4 px', 'wymagana (poza stanem wciśnięty/zablokowany)', 'inset box-shadow', '6 px na hover, 0 przy wciśnięciu [D]'],
  ['etykieta', 'wymagana', 'Archivo 15/700', 'czasownik; do ~3 słów [R]'],
  ['ikona 16 px po lewej', 'opcjonalna', 'pokazana tylko kłódka <code>.lock</code>', 'inne ikony nie pokazane [P]'],
  ['powód blokady pod przyciskiem', 'wymagany przy blokadzie', '<code>.btn-reason</code> + aria-describedby', 'S15, S13 [D]']],
 [['hierarchia', 'główny <code>.btn-primary</code>', 'jedna najważniejsza akcja sekcji (Aplikuj, Wybierz Epicki, Załóż konto)', 'tło --action, biały tekst', 'max 1 na sekcję [D] S01 §6.1'],
  ['hierarchia', 'drugorzędny <code>.btn-secondary</code>', 'pozostałe akcje, linki-przyciski (Wszystkie kategorie, Pełny ranking)', 'tło białe, krawędź #A3CCD9', '[D]'],
  ['szerokość', 'pełna <code>.btn-full</code>', 'w panelach bocznych i kartach pakietów', 'width 100%', 'S10, S11, S15 [D]'],
  ['rozmiar', 'kompaktowy <code>.btn-compact</code> 36 px', 'przycisk powtarzany w każdej pozycji listy: stopka karty, wiersz tabeli, koszyk', 'wysokość 36 px, padding 14 px, etykieta 14 px; stany jak w 44 px', 'decyzja właściciela 2026-11-10 [D]; w components.css v1.6 — <a href="decyzje-v1-1.html#kompakt">specyfikacja</a>'],
  ['stan', 'najechanie', 'kursor nad aktywnym przyciskiem', 'krawędź 6 px, translateY(−2px)', '[D] S04 macierz'],
  ['stan', 'wciśnięty / aria-pressed=true', 'klik; „Zapisano”', 'krawędź 0, etykieta 4 px niżej', '[D]'],
  ['stan', 'fokus', 'klawiatura', 'wewnętrzny pierścień 3 px --focus + 2 px biały', '[D]; outline obcinany przez clip-path'],
  ['stan', 'zablokowany (wariant A)', 'akcja niedostępna z powodem', 'tło #BCBCBC, ramka/tekst granat, kłódka, brak krawędzi', '[D]; wybrany przez zespół; kłódka przetestowana nieformalnie'],
  ['stan', 'ładowanie <code>.is-loading</code>', 'wysyłanie', 'etykieta znika, 3 migające piksele, rozmiar bez zmian; aria-busy', '[D] v1.6 — K28'],
  ['ikona', 'z ikoną 24 px', 'akcja z czytelnym symbolem', 'ikona po lewej, −4 px', '[D] v1.7 — K21']],
 [['wariant', 'enum', 'primary, secondary', 'brak — wybierasz klasę', 'hierarchia', '[D]'],
  ['pełna szerokość', 'boolean', 'tak / nie', 'nie', 'w wąskich kolumnach', '[D]'],
  ['etykieta', 'tekst', 'Aplikuj teraz, Zapisz ofertę, Pokaż 42 oferty, Wybierz Epicki…', '—', 'licznik w etykiecie aktualizuje się (K20)', '[D]'],
  ['zablokowany', 'boolean (aria-disabled)', 'true + powód', 'false', 'płaski, kłódka, powód', 'wymaga <code>aria-describedby</code> [D]'],
  ['wciśnięty (przełącznik)', 'boolean (aria-pressed)', 'false/true + data-label-on/off', 'false', 'zmienia etykietę', 'S03 [D]'],
  ['ikona', 'slot', 'kłódka', 'brak', '—', 'inne ikony [P]']],
 [['tło głównego', '--action', 'domyślny', '#17735F', 'S01', '[D]'], ['krawędź głównego', '--action-edge', '', '#00021C', 'S01', '[D]'],
  ['krawędź drugorzędnego', '--btn-secondary-edge', '', '#A3CCD9', 'S01', '[D]'], ['zablokowany', '--disabled-bg/-ink/-line', '', '#BCBCBC / #1C284D / #2D5280', 'S01', '[D]'],
  ['fokus', '--focus', '', '#2469B3', 'S01', '[D]'], ['wysokość', '--btn-h', '', '44px', 'S01', '[D]']],
 [['wysokość', 'wszystkie stany', '44 px stała', '--btn-h', 'zmierzone 0 px różnicy w 14 przyciskach [D]'],
  ['padding poziomy', '—', '18 px', '—', '[D] S02'], ['ikona ↔ etykieta', '—', 'gap 8 px', '—', '[D]'],
  ['powód ↔ przycisk', '—', '8 px', '—', '[D] <code>.btn-reason</code>'], ['kompaktowy', '<code>.btn-compact</code>', '36 px stała, padding 14 px', '—', 'decyzja 2026-11-10 [D]']],
 [['etykieta', '—', 'Archivo 700', '15 px', '1', '—', 'biały / --ink / --disabled-ink [D]'], ['powód blokady', '—', 'Archivo 600', '13 px', '—', '—', '--ink-2 [D]']],
 '''Najechanie unosi klawisz, wciśnięcie „wciska” go — rozmiar nigdy się nie zmienia (reguła z testów: wcześniej przycisk rósł o 2–4 px i przesuwał panel filtrów) {D} S01 §12. Blokada nie znika po najechaniu, kliknięcie nie wykonuje akcji (obsługa w kodzie) {T}. Treść: czasownik + obiekt („Aplikuj teraz”, „Pokaż 8 ofert” z polską odmianą) {R}.''',
 [['„Wybierz Epicki” jako jedyny główny w sekcji pakietów (S10)', 'cztery zielone przyciski obok siebie', 'jeden kolor akcji, inaczej brak hierarchii [D] S01 zasada 6'],
  ['zablokowany z kłódką i powodem „Dodaj CV do profilu, aby aplikować.” (S15)', 'szary przycisk bez wyjaśnienia lub atrybut disabled', 'użytkownik wie, co zrobić; zachowany fokus [D]'],
  ['„Zapisz” jako przełącznik z aria-pressed (S10, S15)', 'przycisk „Zapisz”, który nic nie robi', 'martwe kontrolki były zgłaszane jako błąd [D] S01 §6.12'],
  ['żółty tylko w badge „Nowa”', 'żółty przycisk', '--highlight nie jest kolorem akcji [D]']],
 [['rozmiar celu', '44 px wysokości; kompaktowy 36 px', 'zmierzone [D]', 'WCAG 2.2 2.5.8 Target Size (Minimum), AA — min. 24×24 CSS px', 'pomiar w przeglądarce'],
  ['fokus widoczny', 'pierścień wewnętrzny 3 px', 'widoczny w S04 [D]', 'WCAG 2.4.7 Focus Visible (AA), 2.4.11 Focus Not Obscured (AA)', 'Tab po stronie'],
  ['kontrast etykiety', 'biały na #17735F 5.7:1; granat na #BCBCBC 7.6:1', 'wyliczone z hex [D]', 'WCAG 1.4.3 (AA) — wyjątek dla nieaktywnych komponentów', 'narzędzie kontrastu na wdrożeniu'],
  ['stan przełącznika', 'aria-pressed true/false, zmiana etykiety', 'S03 [D]', 'WCAG 4.1.2 (A); APG Button (toggle)', 'czytnik ekranu [T]'],
  ['blokada', 'aria-disabled + aria-describedby z powodem', 'S15 [D]', 'WCAG 4.1.2, 1.3.1', 'czytnik ekranu odczytuje powód [T]']],
 'S01 §6.1, §6.12; S02 .btn; S03; S04 macierz stanów i warianty blokady; S10, S11, S13, S15.',
 figs(('btn-states', 'Macierz stanów: główny i drugorzędny × domyślny, najechanie, wciśnięty, fokus, zablokowany'), ('btn-disabled-variants', 'Warianty blokady A (wybrany), B, C'), cols=1)
 + figs(('btn-disabled-in-context', 'Blokada w kontekście: panel akcji oferty z powodem i przyciskiem „Zapisz ofertę”'), ('btn-toggle-pressed', 'Przełącznik „Zapisz” w stanie „Zapisano” — .btn-compact 36 px w .card-foot (S10, v1.6)')),
 table(['Kombinacja', 'Gdzie pokazano'], [['główny × domyślny/hover/wciśnięty/fokus/zablokowany', 'S04 [D]'], ['drugorzędny × te same stany', 'S04 [D]'], ['główny × pełna szerokość', 'S11 „Pokaż N ofert”, S10 pakiety [D]'], ['drugorzędny × przełącznik pressed', 'S10, S15 [D]'], ['drugorzędny × zablokowany w kontekście', 'S13 koszyk (główny zablokowany) [D]'], ['dowolny × ładowanie', 'nie pokazano [P]']]))

# K02 — Badge
card('K02', 'Badge',
 'Krótka etykieta statusu przy obiekcie: „Nowa”, „Polecany”, para klucz–wartość („Zdalnie | 100%”). Nie jest klikalna. Do tagów technologii użyj chipa (K03), do liczby pozycji — licznika (K04). [D] S01 §6.2.',
 [['kontener z ramką 2 px i cieniem 2 px', 'wymagany', '<code>.badge</code>', 'tło wg wariantu [D]'], ['etykieta wersalikami', 'wymagana', 'Archivo 12/700', '1–2 słowa [R]'], ['drugi segment (wartość)', 'opcjonalny', '<code>.badge-seg</code>', 'tło --ink [D]']],
 [['znaczenie', 'neutralny', 'status informacyjny', 'tło białe', '[D]'], ['znaczenie', 'nowe <code>.badge-new</code>', '„Nowa”, „Polecany”', 'tło --highlight', 'jedyne użycie żółtego [D]'],
  ['układ', 'segmentowy <code>.badge-seg</code>', 'klucz | wartość', 'dwa pola', 'S04 [D]'], ['rozmiar', 'mały <code>.badge-sm</code>', 'w wierszu listy, w nazwie pakietu', '10 px, bez cienia', 'S10, S14 [D]'],
  ['znaczenie', 'status z kolorowym kwadratem', 'AKTYWNA / SZKIC / WYGASŁA', 'kwadrat 8 px przed tekstem', 'tylko S16 — poza systemem [S]']],
 [['wariant', 'enum', 'neutralny, new, seg, sm', '—', '—', '[D]'], ['tekst', 'tekst', 'Nowa, Polecany, Zdalnie|100%', '—', '—', '[D]']],
 [['tło nowe', '--highlight', '', '#F7C93E', 'S01', '[D]'], ['ramka, cień', '--border, --shadow-sm', '', '2 px, 2 px', 'S01', '[D]'], ['segment wartości', '--ink / --on-ink', '', '#00021C / #F0EDD8', 'S01', '[D]']],
 [['padding', 'domyślny', '5×8 px', '—', '[D]'], ['padding', 'sm', '3×6 px', '—', '[D]']],
 [['etykieta', 'label', 'Archivo 700', '12 px (sm 10 px)', '1', '+0.3px', 'wersaliki, --ink [D]']],
 'Statyczny. Treść krótka; tłumaczenia dłuższe niż 2 słowa łamią układ wiersza — do sprawdzenia [P].',
 [['jeden „Nowa” na karcie (S11)', 'trzy badge na jednej karcie', 'badge traci wagę [R]'], ['„Polecany” obok nazwy pakietu (S10)', 'badge zasłaniający cenę', 'zaobserwowane i poprawione na S10 [D]']],
 [['kolor', '„Nowa” ma tekst, nie tylko kolor', '[D]', 'WCAG 1.4.1 Use of Color (A)', 'przegląd'], ['kontrast', 'ink na #F7C93E 13.0:1', '[D]', 'WCAG 1.4.3 (AA)', 'narzędzie']],
 'S01 §6.2; S02; S04; S10, S11, S14, S16.',
 figs(('badges', 'Badge new, segmentowy, chipy, licznik, „+N” (studium komponentów)'), cols=1))

# K03 — Chip
card('K03', 'Chip / tag',
 'Tag technologii, frazy lub aktywnego filtra. W karcie: informacyjny (bez akcji). W wierszu „Aktywne filtry”: przycisk usuwający filtr (×). Na landingu: link do wyszukiwania („Popularne”). [D] S01 §6.3, §6.12.',
 [['tło --chip, narożnik schodkowy', 'wymagane', '<code>.chip</code>', '[D]'], ['etykieta', 'wymagana', 'Archivo 13/600', '[D]'], ['× usuwania', 'opcjonalny (aktywne filtry)', 'generowany przez S03', '[D]'], ['licznik „+N”', 'opcjonalny', '<code>.chip-more</code> 32×32', 'gdy &gt; 4 chipów [D]']],
 [['rola', 'informacyjny', 'technologie w karcie', '—', '[D] S11, S10'], ['rola', 'link', '„Popularne” w hero', 'podkreślenie na hover', '[D] S10'], ['rola', 'usuwający filtr', 'aktywne filtry', 'przycisk z „×”', '[D] S11'], ['nadmiar', '„+N”', 'więcej niż 4 tagi', 'osobny kwadrat z ramką', '[D]']],
 [['etykieta', 'tekst', 'React, Unity, Zdalnie…', '—', '—', '[D]'], ['interaktywny', 'enum', 'brak / link / przycisk', 'brak', 'rola', 'wizualnie identyczne — patrz dostępność [R]']],
 [['tło', '--chip', '', '#A3CCD9', 'S01', '[D]'], ['„+N”', '--chip-more', '', '#F0BB90', 'S01', '[D]']],
 [['padding', '—', '6×8 px', '—', '[D]'], ['odstęp między chipami', '—', '6 px', '—', '[D] <code>.chips</code>']],
 [['etykieta', '—', 'Archivo 600', '13 px', '1', '—', '--ink [D]']],
 'Usunięcie aktywnego filtra odznacza checkbox i przelicza wyniki (S03) — sprawdzone testem klikania [D].',
 [['max 4 chipy + „+N”', '8 chipów w karcie', 'karta rośnie, gubi się kwota [D] S01 §6.3'], ['chipy bez cienia', 'chip z cieniem jak badge', 'chip nie jest „obiektem”; w liście jest ich wiele [D]']],
 [['interaktywność', 'chip-przycisk musi mieć aria-label „Usuń filtr: X”', 'S03 [D]', 'WCAG 4.1.2', 'czytnik [T]'], ['rozpoznawalność', 'chip-link i chip-przycisk wyglądają jak informacyjny', '[S]', 'WCAG 1.3.1 / dobra praktyka', 'rozważyć znak „×” lub podkreślenie [R]']],
 'S01 §6.3; S03; S10, S11.',
 figs(('chips-card', 'Chipy w karcie oferty z „+2”'), ('active-filters', 'Aktywne filtry jako chipy z ×')))

# K04 — Licznik
card('K04', 'Licznik',
 'Liczba pozycji w panelu, kategorii albo numer kroku. Zawsze liczba, zawsze w foncie pikselowym. [D] S01 §6.4.',
 [['kontener --ink', 'wymagany', '<code>.count</code>', '[D]'], ['liczba', 'wymagana', 'Press Start 2P 10 px', 'spacje tysięcy („1 128”) [D]']],
 [['kontekst', 'w nagłówku panelu', 'liczba ofert w kategorii', '—', '[D] S10, S14'], ['kontekst', 'numer kroku', '„Jak to działa”', '—', 'S10 — użycie ekranowe [S]']],
 [['liczba', 'liczba', '8, 128, 1 128', '—', '—', 'musi zgadzać się z danymi [D] S01 §6.12']],
 [['tło / tekst', '--ink / --on-ink', '', '#00021C / #F0EDD8', 'S01', '[D]']],
 [['padding', '—', '7×6×6 px', '—', '[D]']],
 [['liczba', 'pixel-xs', 'Press Start 2P', '10 px', '1', '+1px', '[D]']],
 'Liczniki dynamiczne (wyniki) aktualizuje S03 z polską odmianą.',
 [['„1 128” ze spacją', '„1128”', 'czytelność dużych liczb [R]'], ['liczba zgodna z listą', '„42 oferty” przy 8 kartach', 'zgłoszone przez użytkownika jako błąd [D]']],
 [['nazwa', 'licznik w nagłówku powinien być częścią nazwy sekcji dla czytnika', 'brak powiązania [P]', 'WCAG 1.3.1', 'czytnik [T]']],
 'S01 §6.4; S10, S14.', figs(('panel-list', 'Licznik w nagłówku panelu kategorii'), cols=1))

# K05 — Awatar
card('K05', 'Awatar / monogram',
 'Zastępuje logo firmy, gracza lub kategorii 1–2 literami. Dekoracyjny: nazwa zawsze obok w tekście. [D] S01 §5.',
 [['kwadrat w kolorze --avatar-n', 'wymagany', '<code>.avatar</code>', 'kolor przypisany deterministycznie [R]'], ['monogram', 'wymagany', 'Press Start 2P', 'polskie znaki dozwolone („ŁŻ”) [D]'], ['ramka 2 px', 'tylko xl', '<code>.avatar-xl</code>', '[D]']],
 [['rozmiar', '20 px', 'wiersz listy, tabela', '—', '[D]'], ['rozmiar', '56 px (xl)', 'karta, podium, panel akcji', 'ramka 2 px', '[D]']],
 [['litery', 'tekst', '1–2 znaki', '—', '—', '[D]'], ['kolor', 'enum 1–6', '--avatar-1…6', '—', '—', '[D]']],
 [['tło', '--avatar-1…6', '', '6 kolorów SNES', 'S01 §2.3', '[D]']],
 [['20 / 56 px', '—', 'kwadrat', '—', '[D]']],
 [['monogram', '—', 'Press Start 2P', '7 / 14 px', '1', '—', 'biały [D]']],
 'Nie dotyczy (statyczny).',
 [['monogram + nazwa obok', 'sam monogram jako jedyna identyfikacja', 'monogram jest dekoracją [D] aria-hidden'], ['kolor wg hash nazwy', 'losowy kolor przy każdym renderze', 'spójność [R]']],
 [['dekoracja', 'aria-hidden="true"', 'na ekranach [D]', 'WCAG 1.1.1 (A)', 'czytnik [T]'], ['kontrast monogramu', 'biały na #F0BB90 itp. nie dotyczy (inne tła)', 'biały na #2469B3 ≈ 5.6:1; reszta do policzenia', 'WCAG 1.4.3 — dekoracja zwolniona, jeśli aria-hidden', '[P]']],
 'S01 §5, §2.3; S10, S12, S16.', figs(('card-offer', 'Awatar xl w karcie oferty'), cols=1))

# K06 — Panel listy
card('K06', 'Panel listy',
 'Główna jednostka katalogu: kategoria z liczbą pozycji i krótką numerowaną listą. Strona główna — siatka paneli; strona kategorii — jeden panel z pełną listą. Gdy potrzebujesz porównania wielu atrybutów, użyj tabeli (K11); gdy pozycja potrzebuje opisu i tagów — karty (K07). [D] S01 §6.5.',
 [['panel (białe tło, ramka 2 px, cień 6 px)', 'wymagany', '<code>.panel</code>', '[D]'], ['nagłówek: tytuł + licznik', 'wymagany', '<code>.panel-head</code>, K04', '[D]'], ['motto kursywą', 'opcjonalne', '<code>.panel-motto</code>', '[D]'],
  ['wiersz: numer · awatar · nazwa · wartość', 'wymagany', '<code>.list a</code>', 'wartość: kwota lub badge-sm [D]'], ['„Zobacz wszystkie”', 'opcjonalny (skrócony panel)', '<code>.panel-more</code>', '[D]']],
 [['wyróżnienie', 'domyślny', 'każda kategoria', 'cień --ink', '[D]'], ['wyróżnienie', '<code>.is-featured</code>', '„Świeżo dodane” — 1 na ekran', 'cień --featured', '[D] S14'],
  ['długość', 'skrócony 5–8', 'strona główna, mobile', '+ „Zobacz wszystkie”', '[D]'], ['długość', 'pełny', 'strona kategorii', '—', '[D]'],
  ['siatka', '4 kolumny → 2×2', 'gdy wiersze mają kwoty w pikselowym foncie', 'więcej miejsca na nazwy', 'decyzja z S10 (nazwy ucinane w 4 kolumnach) [S]']],
 [['tytuł', 'tekst', 'Frontend, Backend…', '—', '—', '[D]'], ['licznik', 'liczba', '128, 1 128', '—', '—', '[D]'], ['wartość wiersza', 'enum', 'kwota / — / badge-sm', '—', '—', 'brak → „—” z aria-label [D]'], ['wyróżniony', 'boolean', '—', 'nie', 'cień różowy', 'max 1 [D]']],
 [['cień', '--shadow-lg', 'domyślny', '6px 6px 0 #00021C', 'S01', '[D]'], ['cień wyróżniony', '--featured', '', '6px 6px 0 #D94C87', 'S01', '[D]'], ['linia „Zobacz wszystkie”', '--line-soft', '', '2px dashed #A3CCD9', 'S01', '[D]'], ['numer wiersza', '--ink-3', '', '#2D5280', 'S01', '[D]']],
 [['padding panelu', '—', '16/16/20 px', '—', '[D]'], ['wiersz', 'desktop / mobile', '32 / 40 px', '--row-h', '[D]'], ['numer', '—', 'szerokość 22 px, do prawej', '—', '[D]'], ['odstęp między panelami', '—', '28 px', '—', '[D] .grid-panels']],
 [['tytuł', 'panel-title', 'Archivo 900', '18', '28', '−0.45px', '--ink [D]'], ['motto', '—', 'Archivo italic', '14', '—', '—', '--ink-3 [D]'], ['nazwa w wierszu', 'row', 'Archivo 600', '14', '20', '—', 'wielokropek + title [D]'], ['kwota', 'pixel-xs', 'Press Start 2P', '10', '1', '+0.5px', '--ink-2 [D]']],
 'Wiersz to link do pozycji; hover podkreśla nazwę [D]. Długie nazwy: jedna linia + wielokropek + pełny tekst w <code>title</code> [D]; na szerokości &lt; 600 px kwota w wierszu jest skracana do „18–24 tys.” (pełna wartość w <code>.sr-only</code>), żeby nie zabierała miejsca nazwie — decyzja 2026-11-10, wariant <a href="decyzje-v1-1.html#kwoty">C3</a> [D]; na desktopie pełna kwota [D].',
 [['5–8 pozycji + „Zobacz wszystkie” na stronie głównej', '20 pozycji w panelu strony głównej', 'strona staje się jednolita i długa [D]'], ['1 panel wyróżniony', 'wyróżniony każdy panel „nowych”', 'zasada jednego głośnego elementu [D]'], ['„—” z aria-label „brak widełek”', 'puste miejsce', 'brak danych musi być czytelny [D]']],
 [['struktura', '<code>section</code> + <code>h2</code> + <code>ol</code>', 'na ekranach [D]', 'WCAG 1.3.1 (A)', 'drzewo dostępności'], ['fokus wiersza', 'outline 3 px --focus', '[D]', 'WCAG 2.4.7', 'Tab'], ['ucięta nazwa', 'pełna nazwa w title — niewidoczna dla klawiatury', '[S]', 'WCAG 1.4.10 Reflow / 1.4.13', 'rozważyć 2 linie na mobile [R]']],
 'S01 §6.5; S02; S10, S14.',
 figs(('panel-list', 'Panel listy (S10, desktop, siatka 2×2)'), ('panel-featured', 'Panel wyróżniony (S14)')) + figs(('panel-list-mobile', 'Panel listy na 390 px — skrócone kwoty „28 tys.” (v1.6, wariant C3)'), cols=1))

# K07 — Karta
card('K07', 'Karta',
 'Pozycja wyników, gdy potrzeba więcej niż jednej linii: oferta (tytuł, firma, kwota, tagi) albo przedmiot sklepu (ikona, rzadkość, cena, akcja). Lista kart obsługuje sortowanie, filtry i „Zapisz” (K20). [D] S01 §6.6.',
 [['kontener (ramka 2 px, cień 4 px)', 'wymagany', '<code>.card</code>', '[D]'], ['awatar xl / ikona przedmiotu', 'wymagany', 'K05 / SVG pixel-art', '[D]'], ['tytuł (link)', 'wymagany', 'h3', '[D]'], ['badge „Nowa”', 'opcjonalny', 'K02', '[D]'],
  ['podtytuł (firma · miasto / tryb)', 'wymagany dla oferty', '<code>.card-sub</code>', '[D]'], ['kwota / „Widełki nie podane”', 'wymagana', '<code>.amount</code> / <code>.is-empty</code>', '[D]'], ['chipy', 'opcjonalne', 'K03', '[D]'],
  ['meta (poziom, tryb, dodano)', 'opcjonalna', '<code>.card-meta</code>, ikony 12 px opcjonalne', 'testowy od 1.10 [D]'], ['stopka (czas + Zapisz)', 'opcjonalna', 'S10', 'poza systemem [S]']],
 [['treść', 'oferta', 'listing ofert', 'awatar, firma, kwota zł', '[D] S10, S11'], ['treść', 'przedmiot sklepu', 'sklep', 'ikona pixel-art, rzadkość, cena w monetach, przycisk', '[S] S13 — anatomia własna ekranu'],
  ['stan danych', 'bez widełek', 'brak kwoty', 'kursywa „Widełki nie podane”', '[D]'], ['ukryta', '[hidden]', 'odfiltrowana', 'display none', '[D] S01 §6.12']],
 [['tytuł', 'tekst', '—', '—', 'wiele linii dozwolone', '[D]'], ['kwota', 'zakres liczb', '18 000–24 000 + jednostka', '—', 'brak → is-empty', '[D]'], ['nowa', 'boolean', '—', 'nie', 'badge-new', '[D]'], ['data-sort-*, data-f-*', 'atrybuty', 'date, salary, tryb, poziom, tech', '—', 'sortowanie/filtry', '[D] S03']],
 [['cień', '--shadow-md', '', '4px 4px 0', 'S01', '[D]'], ['kwota', '--font-pixel', '', '12 px', 'S01', '[D]'], ['jednostka', '--ink-3', '', '#2D5280', 'S01', '[D]']],
 [['padding', '—', '16 px', '—', '[D]'], ['awatar ↔ treść', '—', '16 px', '—', '[D]'], ['karty w liście', '—', '20 px', '—', '[D]'], ['siatka', 'S10', '2 kolumny → 1 &lt; 900 px', '—', 'decyzja ekranu [S]']],
 [['tytuł', 'card-title', 'Archivo 800', '18', '24', '—', 'link --ink, podkreślenie na hover [D]'], ['podtytuł', 'small', 'Archivo 400', '14', '—', '—', '--ink-2 [D]'], ['kwota', 'pixel-sm', 'Press Start 2P', '12', '1.6', '—', '[D]'], ['brak kwoty', '—', 'Archivo italic', '14', '—', '—', '--ink-3 [D]']],
 'Pozycje bez wartości idą na koniec sortowania (S03). Kwota w pikselowym foncie jest szeroka — przy 390 px łamie się, ale nie wystaje (zrzuty) [D].',
 [['„Widełki nie podane” kursywą', 'puste miejsce albo „0 zł”', 'brak danych ≠ zero [D]'], ['tytuł karty jako link w kolorze tekstu', 'niebieski podkreślony tytuł', 'pułapka z testów — tytuły dziedziczyły kolor linku [D]'], ['max 4 chipy', 'chmura tagów', '[D]']],
 [['nazwa linku', 'tytuł karty jest linkiem do oferty', '[D]', 'WCAG 2.4.4 Link Purpose (A)', 'czytnik [T]'], ['kwota', 'tekst, nie obraz', '[D]', 'WCAG 1.4.5 (AA)', 'zaznaczenie tekstu'], ['reflow', 'brak poziomego przewijania przy 390 px', 'zmierzone [D]', 'WCAG 1.4.10 (AA)', 'render_check']],
 'S01 §6.6; S03; S10, S11, S13.',
 figs(('card-offer', 'Karta oferty z badge „Nowa” (S11)'), ('card-offer-empty-salary', 'Karta bez widełek (S11)')) + figs(('card-item-shop', 'Karta przedmiotu sklepu z rzadkością (S13)'), ('card-offer-mobile', 'Karta oferty na 390 px (S10)')))

# K08 — Filtry i pola
card('K08', 'Panel filtrów i pola formularza',
 'Zawężanie listy: słowa kluczowe, grupy checkboxów, zakres kwot, „tylko z widełkami”, przycisk z liczbą wyników. Panel po prawej (desktop), nad wynikami (&lt; 900 px). [D] S01 §6.7, §6.12.',
 [['panel (cień 4 px)', 'wymagany', '<code>.panel-filters</code>', '[D]'], ['tytuł „Filtry”', 'wymagany', 'h2', '[D]'], ['pole wyszukiwania', 'opcjonalne', '<code>.field</code> + data-search', '[D]'], ['grupy (fieldset + legend)', 'wymagane', 'linia --line-soft', '[D]'],
  ['checkbox z liczbą', 'wymagany', '<code>.checkbox</code> + <code>.opt-n</code>', 'liczba w .opt-n wylicza list-controls.js; 0 → .is-zero (testowy od 1.10) [D]'], ['zakres od–do', 'opcjonalny', '<code>.range</code> + data-min/data-max', '„Od” > „Do” → .field-error (testowy od 1.10) [D]'], ['przycisk „Pokaż N ofert”', 'wymagany', 'K01 full', '[D]'], ['„Wyczyść filtry”', 'opcjonalny', 'link + data-clear-for', '[D]']],
 [['pole', 'tekst / search', 'słowa kluczowe', 'ramka 2 px, cień 2 px', '[D]'], ['pole', 'number', 'widełki od–do', '—', '[D] S11'], ['checkbox', 'zaznaczony', 'aktywna opcja', 'tło --ink + kwadrat --highlight', '[D]'], ['pole', 'błąd walidacji', '—', '—', 'nie pokazano [P]']],
 [['name/value', 'tekst', 'tryb=zdalnie…', '—', 'ta sama nazwa LUB, różne I', '[D] S03'], ['data-min/max', 'liczba', 'salary', '—', 'zakres', '[D]'], ['data-require', 'tekst', 'salary', '—', 'tylko z danymi', '[D]'], ['liczba przy opcji', 'liczba', '4, 3, 1', '—', 'liczba pasujących pozycji', '[D] reguła S01 §6.12']],
 [['ramka pola', '--border', '', '2 px', 'S01', '[D]'], ['cień pola', '--shadow-sm', '', '2 px', 'S01', '[D]'], ['fokus pola', '--focus + --focus-deco', '', 'outline 3 px + cień', 'S01', '[D]'], ['zaznaczenie', '--highlight', '', '#F7C93E', 'S01', '[D]']],
 [['panel', '—', 'padding 16 px; szer. 280 px', '—', '[D] .layout-results'], ['checkbox', '—', '16×16 px, kwadrat 6 px', '—', '[D]'], ['pole', '—', 'padding 8×10 px', '—', '[D]']],
 [['legend', 'legend', 'Archivo 800', '14', '—', '—', '[D]'], ['opcja', '—', 'Archivo 400', '14', '—', '—', '[D]'], ['liczba opcji', '—', 'Press Start 2P', '9', '—', '—', '--ink-3 [D]']],
 'Filtrowanie na żywo; „Pokaż N ofert” przelicza się z odmianą; zero wyników → pusty stan (K17). Sprawdzone testem klikania (23 przypadki) [D].',
 [['liczby przy opcjach zgodne z kartami', 'zmyślone liczby („Zdalnie 18” przy 8 kartach)', 'użytkownik traci zaufanie [D]'], ['działające filtry albo brak filtrów', 'statyczne checkboxy', '17 martwych kontrolek w pierwszej wersji S11 [D]']],
 [['etykiety', 'każde pole ma label (widoczny lub sr-only)', '[D]', 'WCAG 3.3.2 (A), 1.3.1', 'czytnik'], ['grupy', 'fieldset + legend', '[D]', 'WCAG 1.3.1', '—'], ['wynik', 'liczba wyników ogłaszana aria-live', 'S03 [D]', 'WCAG 4.1.3 Status Messages (AA)', 'czytnik [T]'], ['checkbox', 'natywny input (appearance none)', '[D]', 'APG Checkbox', 'Spacja przełącza [T]']],
 'S01 §6.7, §6.12; S03; S11.', figs(('filters', 'Panel filtrów (S11)'), ('empty-state', 'Wynik filtrowania = 0 → pusty stan (S11)')))

# K09 — Wyszukiwarka
card('K09', 'Wyszukiwarka główna',
 'Główne wejście w wyszukiwanie: pole + przycisk w jednej ramce z kolorowym cieniem. Max jedna na ekran; na landingu jest „głośnym” elementem. [D] S01 §6.11.',
 [['ramka 2 px + cień 6 px --focus-deco', 'wymagana', '<code>.search-main</code>', '[D]'], ['pole', 'wymagane', 'input type=search + label sr-only', '[D]'], ['przycisk „>”', 'wymagany', 'button 48 px na --ink', 'aria-label „Szukaj” [D]']],
 [['miejsce', 'w nagłówku', 'podstrony', '44 px', '[D] S11, S12'], ['miejsce', 'w hero', 'landing', '56 px, przycisk 64 px', 'nadpisanie S10 [S]']],
 [['placeholder', 'tekst', 'Stanowisko, technologia albo firma…', '—', '—', '[D]'], ['action', 'URL', '/oferty, /szukaj', '—', 'prowadzi do wyników', 'strona docelowa nie istnieje w materiałach [P]']],
 [['cień', '--focus-deco', '', '6px 6px 0 #0BAFE6', 'S01', '[D]'], ['przycisk', '--ink / --on-ink', '', '—', 'S01', '[D]']],
 [['wysokość', 'nagłówek / hero', '44 / 56 px', '—', '[D]/[S]'], ['przycisk', '—', '48 / 64 px', '—', '[D]/[S]']],
 [['wpisywany tekst', '—', 'Archivo 400', '15–17', '—', '—', '[D]/[S]']],
 'Wysłanie formularza przechodzi do wyników (poza zakresem materiałów) [P].',
 [['jedna wyszukiwarka na ekranie', 'wyszukiwarka w nagłówku i w hero jednocześnie', 'S10 usunął ją z nagłówka [D]'], ['placeholder z przykładami', 'placeholder jako jedyna etykieta', 'potrzebny label sr-only [D]']],
 [['etykieta', 'label sr-only + role=search', '[D]', 'WCAG 3.3.2, 4.1.2', 'czytnik'], ['fokus', 'outline wewnątrz pola 3 px', '[D]', 'WCAG 2.4.7', 'Tab'], ['kontrast placeholdera', '—', 'nie zmierzono [P]', 'WCAG 1.4.3', 'narzędzie']],
 'S01 §6.11; S10, S11, S12.', figs(('search-main-hero', 'Wyszukiwarka w hero (S10)'), cols=1))

# K10 — Zakładki
card('K10', 'Zakładki',
 'Przełączanie widoku tej samej treści: sortowanie listy (Najnowsze / Najwyższe widełki), okres rankingu (Dziś / Tydzień / Wszech czasów), status (Aktywne / Szkice / Wygasłe). Do nawigacji między stronami użyj nawigacji (K15). [D] S01 §6.11, §6.12.<br><b>Od v1.2:</b> sortowanie listy to <b>grupa przycisków przełączających</b> (<code>role="group"</code> + <code>aria-pressed</code>) w tym samym wyglądzie <code>.tabs</code>; zakładki (<code>role="tab"</code>) tylko tam, gdzie przełączają panele treści — okres (S12), status (S16). decyzja 2026-11-10, wariant <a href="decyzje-v1-1.html#sortowanie">B</a> [D]. Ekrany S10, S11, S13 przeniesione na grupę przycisków w pakiecie v1.6 [D].',
 [['kontener (ramka 2 px, cień 2 px)', 'wymagany', '<code>.tabs</code>', '[D]'], ['opcja', 'wymagana 2+', 'button role=tab (panele) / button aria-pressed (sortowanie)', '[D] decyzja 2026-11-10'], ['licznik w zakładce', 'opcjonalny', 'S16 („Aktywne 19”)', 'pixel-font [S]']],
 [['funkcja', 'sortowanie', 'kolejność kart', 'grupa przycisków aria-pressed + data-sort-for (S03)', '[D] decyzja 2026-11-10'], ['funkcja', 'okres', 'zmiana zbioru danych', 'kod ekranu', '[D] S12'], ['funkcja', 'status', 'pokazanie innej tabeli', 'kod ekranu', '[D] S16'], ['stan', 'wybrana', '—', 'tło --ink, tekst --on-ink', '[D]']],
 [['aria-selected', 'boolean', 'true/false', 'pierwsza', 'wybór zakładki (panele)', '[D]'], ['aria-pressed', 'boolean', 'true/false', 'pierwsza', 'wybór sortowania', '[D] decyzja 2026-11-10; styl .tabs [aria-pressed=true] w components.css v1.6'], ['data-sort-key/dir', 'tekst', 'date, salary, order, price; asc/desc', '—', 'sortowanie', '[D] S03']],
 [['wybrana', '--ink / --on-ink', '', '#00021C / #F0EDD8', 'S01', '[D]']],
 [['wysokość', '—', '36 px', '—', '[D]'], ['separator', '—', 'ramka 2 px między zakładkami', '—', '[D]'], ['przepełnienie', 'mobile', 'przewija się w ramce', '—', '[D] v1.2']],
 [['etykieta', '—', 'Archivo 700', '14', '—', '—', '[D]']],
 'Klik i strzałki ←/→ zmieniają wybór (S03, S12, S16) [D]. Zmiana jest ogłaszana aria-live (S03) [D].',
 [['zakładki, które działają', 'zakładki sortowania bez obsługi', 'zgłoszone przez użytkownika jako błąd [D]'], ['2–4 krótkie opcje', '6 zakładek na mobile', 'przewijanie ukrywa opcje [R]']],
 [['wzorzec', 'role=tablist/tab, aria-selected, strzałki', '[D]', 'APG Tabs; WCAG 4.1.2, 2.1.1', 'klawiatura [T]'], ['sortowanie', 'role=group z aria-label „Sortuj …”, przyciski aria-pressed; każdy przycisk to przystanek Tab', '[D] decyzja 2026-11-10', 'APG Button (toggle); WCAG 4.1.2', 'czytnik ogłasza „przycisk przełączający, wciśnięty” [T]']],
 'S01 §6.11–6.12; S03; S11, S12, S16.', figs(('tabs-sort', 'Sortowanie jako grupa przycisków aria-pressed (S11, v1.6)'), ('tabs-period', 'Okres — zakładki z panelami (S12)'), ('tabs-status', 'Status z licznikami — zakładki (S16)'), cols=3))

# K11 — Tabela
card('K11', 'Tabela danych',
 'Porównanie wielu atrybutów wielu pozycji: ranking, panel pracodawcy, top pracodawcy. Jeśli sortujesz — każdą kolumnę z danymi. Do przeglądania bez porównywania użyj panelu listy (K06). [D] S01 §6.11, v1.5.',
 [['ramka + cień 6 px', 'wymagana', '<code>.table-wrap</code> (position relative, przewijanie)', '[D]'], ['nagłówek', 'wymagany', 'th na --paper, przyklejony', '[D]'], ['przycisk sortowania', 'opcjonalny', '<code>.sort</code> (cała komórka klikalna)', '[D] v1.5'], ['znacznik kolejności stałej', 'opcjonalny', '<code>.sorted</code>', '[D]'],
  ['miejsce', 'opcjonalne', '<code>.rank</code>, 1–3 w kolorach podium', '[D]'], ['encja (awatar + link)', 'opcjonalna', '<code>.cell-entity</code>', '[D]'], ['liczby', '—', '<code>.num</code> pixel-font, do prawej', '[D]'], ['zmiana', 'opcjonalna', '<code>.delta-up/down</code>', '[D]'], ['znacznik pakietu/statusu', 'opcjonalny', 'K14 tier-tag, badge', '[D]/[S]']],
 [['sortowanie', 'brak', 'tabela informacyjna', '—', '[D]'], ['sortowanie', 'pełne', 'każda kolumna z danymi', '◆ / ▲ / ▼', '[D] S12, S16, S10'], ['sortowanie', 'stała kolejność', 'ranking po wyniku', '<code>.sorted</code> ▼ bez przycisku', '[D]'], ['wiersz', 'wygasający', 'oferta kończy się za ≤ 5 dni', 'lewa krawędź --danger + „za 2 dni”', 'S16 — poza systemem [S]']],
 [['aria-sort', 'enum', 'ascending, descending, none', 'none', 'kierunek na th', '[D]'], ['data-sort-value', 'liczba', '1–4 dla pakietów', '—', 'sortowanie po znaczeniu', '[D]'], ['data-sort-first', 'enum', 'descending', 'num: desc, tekst: asc', '—', '[D]'], ['data-sort-manual', 'flaga', '—', '—', 'sortuje kod ekranu', '[D] S12']],
 [['nagłówek', '--paper', '', '#F0EDD8', 'S01', '[D]'], ['separator wierszy', '--paper', '', '2px solid', 'S01', '[D]'], ['hover wiersza', '—', '', '#F8F6EC', 'S02', '[D] tint spoza palety'], ['miejsca 1–3', '--gold/silver/bronze', '', 'NES', 'S01', '[D]']],
 [['nagłówek', '—', '40 px', '—', '[D]'], ['wiersz', '—', '44 px', '—', '[D]'], ['padding komórki', '—', '0 12 px', '—', '[D]'], ['rank', '—', 'min 28×28 px, rośnie dla 3 cyfr', '—', '[D] v1.2']],
 [['nagłówek', 'label', 'Archivo 800', '12', '—', '+0.3px', 'wersaliki [D]'], ['nazwa', '—', 'Archivo 600', '14', '20', '—', '[D]'], ['liczby', 'pixel-xs', 'Press Start 2P', '10', '1', '+0.5px', '[D]']],
 'Klik w dowolne miejsce nagłówka sortuje; drugi odwraca; puste („—”) zawsze na końcu; tekst porównywany po polsku (Ż po Z) — 52 testy klikania [D]. Mobile: tabela przewija się w ramce [D].',
 [['sortowalne wszystkie kolumny z danymi (S12, S16 po poprawce)', 'sortowalne 2 z 6 kolumn', 'użytkownik zgłosił „sortowanie nie działa” [D]'], ['pakiet sortowany po randze', 'pakiet alfabetycznie (Epicki, Legendarny, Rzadki…)', 'znaczenie, nie alfabet [D]'], ['zmiana ze strzałką i tekstem dla czytnika', 'sam kolor zielony/czerwony', 'WCAG 1.4.1 [D]']],
 [['struktura', 'natywna table, th scope=col, caption', '[D]', 'WCAG 1.3.1; APG Table', 'czytnik'], ['sortowanie', 'button w th, aria-sort na th', '[D]', 'APG Sortable Table', 'czytnik ogłasza kierunek [T]'], ['aria-sort="none"', 'zostaje na nieaktywnych sortowalnych kolumnach (decyzja 2026-11-10); przykład APG ustawia atrybut tylko na aktywnej', '[D]', 'WAI-ARIA aria-sort', 'czy czytnik nie powtarza „bez sortowania” przy każdej kolumnie [T]'], ['ogłoszenie', 'aria-live „Posortowano: X, malejąco”', 'S03 [D]', 'WCAG 4.1.3', '[T]']],
 'S01 §6.11, §12 (v1.3–v1.5); S03 table-sort.js; S10, S12, S16.',
 figs(('table-leaderboard-sorted', 'Tabela posortowana po Rozgrywkach (S12)'), ('table-dashboard', 'Tabela z pakietami, statusami i wierszami wygasającymi (S16)')) + figs(('table-ranking', 'Tabela top pracodawców na landingu (S10)'), ('table-mobile', 'Tabela na 390 px — przewijanie w ramce (S12)')))

# K12 — Paginacja
card('K12', 'Paginacja',
 'Przejście między stronami wyników, gdy dane istnieją na kolejnych stronach. Nie dodawaj stron, które nie działają. [D] S01 §6.11, §6.12.',
 [['kwadraty 36 px z ramką i cieniem 2 px', 'wymagane', '<code>.pagination</code>', '[D]'], ['bieżąca strona', 'wymagana', 'aria-current="page"', '[D]'], ['wielokropek', 'opcjonalny', '<code>.gap</code>', '[D]'], ['strzałka wyłączona', 'opcjonalna', 'aria-disabled', '[D]']],
 [['stan', 'bieżąca', '—', 'tło --ink', '[D]'], ['stan', 'wyłączona strzałka', 'pierwsza/ostatnia', 'szara ramka', '[D] S12']],
 [['liczba stron', 'liczba', '3, 9, 25', '—', '—', '[D] S12']], [['bieżąca', '--ink', '', '#00021C', 'S01', '[D]']],
 [['kwadrat', '—', 'min 36×36 px', '—', '[D]'], ['odstęp', '—', '8 px', '—', '[D]']], [['numer', 'pixel-xs', 'Press Start 2P', '10', '1', '—', '[D]']],
 'S12: działa na danych (hash w URL). S11: usunięta, bo prowadziła do nieistniejących stron [D].',
 [['paginacja tylko z danymi', 'strony 2–6 prowadzące donikąd', '[D]']],
 [['nawigacja', 'nav z aria-label, aria-current', '[D]', 'WCAG 1.3.1, 2.4.8', 'czytnik [T]'], ['rozmiar celu', '36 px', '[D]', 'WCAG 2.5.8 (AA)', '—']],
 'S01 §6.11; S11, S12.', figs(('pagination', 'Paginacja z wielokropkiem (S12)'), cols=1))

# K13 — Podium
card('K13', 'Podium',
 'Scena rankingu dla miejsc 1–3; jedyny „głośny” element ekranu rankingu. Reszta rankingu w tabeli (K11). [D] S01 §6.8.',
 [['tło --podium, ramka, cień 6 px', 'wymagane', '<code>.podium</code>', '[D]'], ['miejsce: awatar xl, nazwa, punkty, stopień', 'wymagane ×3', 'li.podium-1/2/3', '[D]'], ['meta (kraj, liczba gier)', 'opcjonalna', '<code>.podium-meta</code> S12', 'poza systemem [S]']],
 [['miejsce', '1 / 2 / 3', '—', 'stopień 96 / 64 / 44 px; złoto / srebro / brąz', '[D]']],
 [['kolejność DOM', '—', '1, 2, 3', '—', 'wizualnie 2-1-3 (order)', '[D]']],
 [['tło', '--podium', '', '#0000BC', 'S01', '[D]'], ['stopnie', '--gold/--silver/--bronze', '', 'NES', 'S01', '[D]']],
 [['stopnie', '1/2/3', '96 / 64 / 44 px', '—', '[D]']], [['punkty', 'pixel-sm', 'Press Start 2P', '12', '—', '—', 'zwycięzca --gold [D]'], ['miejsce', 'pixel-lg', 'Press Start 2P', '20', '—', '—', '[D]']],
 'Statyczne; zmienia się z okresem (S12).',
 [['jedno podium na stronie', 'podium i wyróżniony panel razem', 'zasada jednego głośnego elementu [D]'], ['DOM 1-2-3', 'DOM 2-1-3', 'czytnik czyta kolejność wizualną źle [D]']],
 [['kolejność', 'DOM 1-2-3', '[D]', 'WCAG 1.3.2 Meaningful Sequence (A)', 'czytnik'], ['kolor', 'miejsce = numer + wysokość + kolor', '[D]', 'WCAG 1.4.1', '—'], ['mobile', 'działa do 360 px; węższe → lista', '[D]/[R]', 'WCAG 1.4.10', 'render']],
 'S01 §6.8; S12.', figs(('podium', 'Podium (S12)'), cols=1))

# K14 — Pakiet
card('K14', 'Pakiet (tier) i znacznik pakietu',
 'Oferta handlowa jako rzadkość przedmiotu z gry: Legendarny / Epicki / Rzadki / Zwykły. <b>Karta pakietu</b> (<code>.tier</code>) — cennik; <b>znacznik</b> (<code>.tier-tag</code>) — w tabeli, karcie, koszyku. [D] S01 §6.9, v1.2.',
 [['kontener z lewą krawędzią 10 px w kolorze tieru', 'wymagany', '<code>.tier</code> / <code>.tier-tag</code>', '[D]'], ['nazwa', 'wymagana', '—', 'kolor zawsze z nazwą [D]'], ['cena', 'wymagana w karcie', 'pixel-sm', '[D]'], ['opis', 'wymagany w karcie', '—', '[D]'], ['badge „Polecany”', 'opcjonalny', 'K02 sm przy nazwie', '[D] S10']],
 [['tier', 'Legendarny / Epicki / Rzadki / Zwykły', 'poziom pakietu', 'kolor krawędzi', '[D]'], ['forma', 'karta', 'cennik (S10)', 'cena + opis + lista + przycisk', '[D]'], ['forma', 'znacznik 24 px', 'tabela (S16)', 'tylko nazwa', '[D]'], ['forma', 'badge z kwadratem', 'rzadkość w sklepie (S13)', 'kwadrat 8 px zamiast krawędzi', 'odrzucony — sklep używa .tier-tag w kartach i koszyku od v1.6 (decyzja 2026-11-10, wariant <a href="decyzje-v1-1.html#rzadkosc">A</a>) [D]']],
 [['tier', 'enum', 'legendary, epic, rare, common', '—', 'kolor', '[D]'], ['cena', 'liczba + waluta', '0, 249, 499, 899 zł', '—', '—', '[D]'], ['polecany', 'boolean', '—', 'nie', 'badge + przycisk główny', '[D]']],
 [['krawędź', '--tier-*', '', '#AC7C00 / #6844FC / #0078F8 / #7C7C7C', 'S01', '[D]']],
 [['krawędź', '—', '10 px', '—', '[D]'], ['karta', '—', 'padding 10×12 px, cień 2 px', '—', '[D]'], ['znacznik', '—', '24 px wysokości', '—', '[D]']],
 [['nazwa', '—', 'Archivo 900', '16', '—', '—', '[D]'], ['cena', 'pixel-sm', 'Press Start 2P', '12', '1.8', '—', '[D]']],
 'Pakiety w tabeli sortują się po randze (data-sort-value) [D].',
 [['kolor + nazwa', 'sam kolorowy pasek', 'WCAG 1.4.1 [D]'], ['jeden przycisk główny przy polecanym', 'główny przy każdym pakiecie', '[D]'], ['rzadkość zawsze jako .tier-tag (karta, tabela, koszyk)', 'badge z kwadratem 8 px', '[D] decyzja 2026-11-10']],
 [['kolor', 'krawędź 3.7–5.5:1 na bieli + nazwa', '[D]', 'WCAG 1.4.11 (AA), 1.4.1', '—']],
 'S01 §6.9; S10, S13, S16.', figs(('tiers', 'Karty pakietów z polecanym (S10)'), cols=1) + figs(('tier-tag-table', 'Znacznik pakietu w tabeli (S16)'), ('rarity-shop', 'Rzadkość w karcie sklepu jako .tier-tag (S13, v1.6)')) + figs(('cart-shop', 'Koszyk sklepu z .tier-tag i przyciskiem zablokowanym (S13, v1.6)'), cols=1))

# K15 — Struktura strony
card('K15', 'Nagłówek, nawigacja i struktura strony',
 'Szkielet każdego ekranu: nagłówek serwisu (logo, nawigacja, akcja lub wyszukiwarka), okruszki, nagłówek treści, sekcje, stopka. Hero tylko na landingu. [D] S01 §6.11.',
 [['nagłówek serwisu', 'wymagany', '<code>.site-header</code>', '[D]'], ['logo pikselowe (2 człony, drugi w --action)', 'wymagane', '<code>.logo</code>', '[D]'], ['nawigacja', 'wymagana', '<code>.site-nav</code> aria-current', '[D]'], ['okruszki', 'opcjonalne (poza landingiem)', '<code>.breadcrumbs</code>', '[D]'],
  ['nagłówek treści', 'wymagany', '<code>.page-head</code>', '[D]'], ['tytuł sekcji + akcja', 'opcjonalny', '<code>.section-title</code>', '[D]'], ['hero', 'tylko landing', 'display + lead + wyszukiwarka + fakty', 'S10 [S]'], ['stopka', 'wymagana', '<code>.site-footer</code>', '[D]']],
 [['akcja w nagłówku', 'wyszukiwarka', 'podstrony', '—', '[D]'], ['akcja w nagłówku', 'przycisk drugorzędny', 'landing („Dodaj ofertę”)', '—', '[D] S10'], ['mobile', 'zawijanie', '&lt; 600 px', 'nawigacja w 2 rzędach', '[D] zrzuty']],
 [['aria-current', 'enum', 'page', '—', 'aktywna pozycja podkreślona 2 px', '[D]']],
 [['tło nagłówka', '--paper', '', '#F0EDD8', 'S01', '[D]'], ['linia dolna', '--border', '', '2 px', 'S01', '[D]'], ['zakreślenie w display', '--mint', '', '#96E3C9', 'S01', '[D]']],
 [['nagłówek', '—', 'min 72 px', '—', '[D]'], ['sekcje', '—', 'odstęp 40 px', '—', '[D]'], ['stopka', '—', 'margines 64 px, padding 24/40', '—', '[D]']],
 [['logo', '—', 'Press Start 2P', '14', '1', '+1px', '[D]'], ['nawigacja', '—', 'Archivo 700', '15', '—', '—', '[D]'], ['display', 'display', 'Archivo 900', '40 (32 mobile)', '44', '−1px', '[D]/[S]']],
 'Nawigacja zawija się na mobile [D]; od v1.7 przy 4+ pozycjach zwija się do przycisku „Menu” — K26 [D].',
 [['link „Przejdź do treści”', 'brak skip-linku', '[D] starter'], ['aria-current na bieżącej pozycji', 'tylko kolor', '[D]']],
 [['landmarki', 'header, nav aria-label, main, footer', '[D]', 'WCAG 1.3.1, 2.4.1 (A)', 'czytnik'], ['skip link', 'pierwszy element', '[D]', 'WCAG 2.4.1', 'Tab'], ['mobile', 'nawigacja w 2 rzędach — przy 4+ pozycjach do oceny', '[S]', 'WCAG 1.4.10', 'render [P]']],
 'S01 §6.11; starter S02; S10, S12.', figs(('header', 'Nagłówek landingu (S10)'), cols=1) + figs(('breadcrumbs-pagehead', 'Nagłówek z wyszukiwarką, okruszki i nagłówek treści (S12)'), cols=1) + figs(('hero', 'Hero landingu (S10)'), ('header-mobile', 'Nagłówek na 390 px (S10)')))

# K16 — Callout
card('K16', 'Callout',
 'Wyróżniony komunikat w treści: wskazówka, ostrzeżenie o terminie, zaproszenie do akcji. Nie zastępuje komunikatu błędu formularza. [D] S01 §6.10–6.11.',
 [['tło --mint, ramka 2 px, bez cienia', 'wymagane', '<code>.callout</code>', '[D]'], ['pogrubiony lead', 'opcjonalny', 'strong', '[D]'], ['przycisk', 'opcjonalny', 'K01', '[D] S10, S16']],
 [['rola', 'CTA', 'zachęta (landing)', 'przycisk główny po prawej', '[D] S10'], ['rola', 'ostrzeżenie o terminie', 'panel pracodawcy', 'przycisk drugorzędny', '[D] S16'], ['ton', 'błąd / sukces', '—', '—', 'od v1.7 powiadomienia K22; <code>.callout-danger</code> wycofywany (od 1.7, usunięcie w 2.0) [D]']],
 [['treść', 'tekst', '—', '—', '—', '[D]']], [['tło', '--mint', '', '#96E3C9', 'S01', '[D]']],
 [['padding', '—', '14×16 px', '—', '[D]']], [['lead', '—', 'Archivo 800', '16', '—', '—', '[D]']],
 'Statyczny.',
 [['jeden callout w sekcji', 'callout w każdej sekcji', 'traci wagę [R]'], ['callout ostrzegawczy z tekstem „wygasają w tym tygodniu”', 'sam kolor', '[D]']],
 [['rola', 'dla pilnych komunikatów rozważyć role=status', '[R]', 'WCAG 4.1.3', 'czytnik [T]'], ['kontrast', 'ink na #96E3C9 ≥ 12:1', '[D]', 'WCAG 1.4.3', '—']],
 'S01 §6.10; S10, S16.', figs(('callout-cta', 'Callout CTA (S10)'), ('callout-dashboard', 'Callout o wygasaniu (S16)')))

# K17 — Pusty stan
card('K17', 'Pusty stan',
 'Zero wyników albo brak treści: tytuł, jedno zdanie i akcja naprawcza. Dobre miejsce na jedyną ilustrację ekranu. [D] S01 §6.10–6.11.',
 [['panel z cieniem 6 px', 'wymagany', '<code>.empty</code>', '[D]'], ['ilustracja 96 px', 'opcjonalna', '<code>.empty-art</code>', 'nie pokazano [P]'], ['tytuł h2', 'wymagany', '—', '[D]'], ['zdanie', 'wymagane', '—', '[D]'], ['przycisk', 'wymagany', 'K01 „Wyczyść filtry”', '[D]']],
 [['przyczyna', 'brak wyników filtrów', 'S11', 'data-empty-for', '[D]']], [['hidden', 'boolean', '—', 'true', 'pokazywany przy 0', '[D] S03']],
 [['cień', '--shadow-lg', '', '6 px', 'S01', '[D]']], [['padding', '—', '40×24 px', '—', '[D]']], [['tytuł', 'h1-size', 'Archivo 900', '24', '32', '−0.6px', '[D]']],
 'Pojawia się automatycznie przy 0 wynikach; „Wyczyść filtry” przywraca listę (test klikania) [D].',
 [['przycisk naprawczy', 'sam tekst „Brak wyników”', '[D]']],
 [['ogłoszenie', 'liczba wyników 0 ogłaszana aria-live', 'S03 [D]', 'WCAG 4.1.3', '[T]']],
 'S01 §6.10; S03; S11.', figs(('empty-state', 'Pusty stan po filtrowaniu (S11)'), cols=1))

# K18 — Fakty
card('K18', 'Fakty encji',
 'Kluczowe atrybuty obiektu w siatce: liczby portalu (hero), parametry oferty (szczegóły). [D] S01 §6.11.',
 [['siatka w ramce 2 px', 'wymagana', '<code>.facts</code> (dl)', '[D]'], ['etykieta', 'wymagana', 'dt wersaliki', '[D]'], ['wartość', 'wymagana', 'dd; liczby .num', '[D]']],
 [['treść', 'liczby portalu', 'hero (S10)', '—', '[D]'], ['treść', 'parametry oferty', 'S15', '—', '[D]']],
 [['etykieta/wartość', 'tekst', 'Widełki / 22 000–28 000 zł', '—', '—', '[D]']], [['linie wewnętrzne', '--paper', '', '2 px', 'S01', '[D]']],
 [['kolumna', '—', 'min 180 px (auto-fit)', '—', '[D] v1.2'], ['komórka', '—', 'padding 10×12 px', '—', '[D]']],
 [['etykieta', '—', 'Archivo 800', '11', '—', '+0.3px', '--ink-3, wersaliki [D]'], ['wartość', '—', 'Archivo 600 / Press Start 2P', '15 / 12', '—', '—', '[D]']],
 'Na 390 px komórki układają się w 1 kolumnę; długie kwoty łamią się (S15) [D].',
 [['4–8 faktów', '15 faktów', 'gubi się hierarchia [R]']],
 [['struktura', 'dl/dt/dd', '[D]', 'WCAG 1.3.1', 'czytnik']],
 'S01 §6.11; S10, S15.', figs(('facts-hero', 'Fakty w hero (S10)'), ('facts-offer', 'Fakty oferty (S15)')))

# K19 — Detale graficzne
card('K19', 'Detale graficzne',
 'Elementy, które niosą pikselowy charakter bez obciążania czytania: separator „dither”, kwadratowe punktory, pikselowe ikony (kłódka, ikony kategorii), kroki „Jak to działa”. [D] S01 §5.',
 [['separator dither', 'opcjonalny', '<code>.dither</code>', 'między dużymi sekcjami [D]'], ['punktor 6 px', 'opcjonalny', '<code>.list-square</code>', '[D]'], ['kłódka 8×9', 'przy blokadzie', '<code>.lock</code>', '[D]'], ['ikony 8×8', 'opcjonalne', 'box-shadow / SVG crispEdges', '[D]'], ['krok z numerem', 'opcjonalny', 'panel + licznik (S10)', 'poza systemem [S]']],
 [['—', '—', '—', '—', 'Nie dotyczy — elementy bez wariantów']], [['kolor', 'token', '--action (dither, punktor), currentColor (kłódka)', '—', '—', '[D]']],
 [['dither', '--action', '', '#17735F', 'S01', '[D]']], [['dither', '—', '8 + 8 px', '—', '[D]'], ['punktor', '—', '6 px, wcięcie 18 px', '—', '[D]'], ['ikony', '—', 'skala ×2/×3, pixelated', '—', '[D]']],
 [['Nie dotyczy', '', '', '', '', '', '']],
 'Statyczne.',
 [['ilustracje tylko w palecie SNES', 'zdjęcia stockowe z gradientami', '[D] S01 §5'], ['separator na granicy dużych sekcji', 'separator między każdym akapitem', 'szum [D]']],
 [['dekoracje', 'aria-hidden / role=presentation', '[D]', 'WCAG 1.1.1', '—']],
 'S01 §5; S04; S10.', figs(('details-dither', 'Separator, punktory, ikony (S04)'), ('steps', 'Kroki z numerami (S10)')))

# K20 — Sterowanie listą
card('K20', 'Sterowanie listą (wzorzec interakcji)',
 'Wspólne zachowanie list kart: sortowanie zakładkami, filtry na żywo, licznik z polską odmianą, aktywne filtry, pusty stan, przełącznik „Zapisz”. Zasada nadrzędna: wszystko, co wygląda na klikalne, działa, a liczby zgadzają się z tym, co widać. [D] S01 §6.12, S03.',
 [['lista + pozycje', 'wymagane', 'data-list, data-item', '[D]'], ['sortowanie', 'opcjonalne', 'data-sort-for (K10)', '[D]'], ['filtry', 'opcjonalne', 'data-filter-for (K08)', '[D]'], ['licznik', 'opcjonalny', 'data-count-for + formy odmiany', '[D]'], ['aktywne filtry', 'opcjonalne', 'data-active-for (K03)', '[D]'], ['pusty stan', 'wymagany przy filtrach', 'data-empty-for (K17)', '[D]']],
 [['funkcja', 'sortowanie', '—', 'kolejność; brak wartości na końcu', '[D]'], ['funkcja', 'filtrowanie', '—', 'ta sama grupa LUB, różne I', '[D]'], ['funkcja', 'przełącznik', '—', 'aria-pressed + etykieta', '[D]']],
 [['data-count-forms', 'tekst', 'oferta|oferty|ofert', '—', '1 / 2–4 / 5+', '[D]'], ['data-sort-key', 'tekst', 'order = kolejność z HTML', '—', '—', '[D]']],
 [['Nie dotyczy — wzorzec zachowania korzysta z tokenów komponentów K01, K03, K08, K10, K17', '', '', '', '', '']],
 [['Nie dotyczy', '', '', '', '']], [['Nie dotyczy', '', '', '', '', '', '']],
 'Zweryfikowane: 23 testy list (S11, S13, S15), test klikania każdej kontrolki na 7 ekranach (0 martwych) [D]. Kontrolki w ukrytych zakładkach wymagają osobnego testu [D].',
 [['„Pokaż 1 ofertę / 4 oferty / 7 ofert”', '„Pokaż 42 oferty” przy 8 kartach', 'zgłoszone przez użytkownika [D]'], ['paginacja tylko z danymi', 'strony prowadzące donikąd', '[D]']],
 [['ogłoszenia', 'aria-live dla wyników i sortowania', 'S03 [D]', 'WCAG 4.1.3 (AA)', 'czytnik [T]'], ['fokus', 'po filtrowaniu fokus zostaje na kontrolce', '[D]', 'WCAG 3.2.2 On Input (A)', 'klawiatura [T]']],
 'S01 §6.12; S03; S10, S11, S13, S15.', '')

exec(open(D2 + 'doc_cards.py').read())

# ---------- aneks: elementy spoza systemu ----------
ANNEX = table(['Element (ekran)', 'Opis', 'Status', 'Rekomendacja'], [
 ['<code>.callout-danger</code> (v1.6)', 'ostrzeżenie w treści', '[D] wycofywany od 1.7', 'zastąpić <code>.notice.notice-error</code> (K22); check_screen ostrzega'],
 ['<code>.card-meta</code> (S11)', 'wiersz „Poziom · Tryb · Dodano” w karcie', '[D] przyjęty jako testowy (v1.10)', 'K07 — .card-meta'],
 ['<code>.opt-n</code> (S11)', 'liczba przy opcji filtra (pixel-font)', '[D] przyjęty jako testowy (v1.10)', 'K08 — liczby liczy list-controls.js'],
 ['<code>.range</code> (S11)', 'pola widełek od–do', '[D] przyjęty jako testowy (v1.10)', 'K08 — błąd „Od > Do”'],
 ['stopka karty + kompaktowy przycisk 36 px (S10)', 'czas dodania + „Zapisz”', '[S]', 'przycisk przyjęty jako .btn-compact [D]; .card-foot w components.css v1.6 [D]'],
 ['badge statusu z kwadratem (S16)', 'AKTYWNA / SZKIC / WYGASŁA', '[S]', 'dopisać jako wariant badge „status” [R]'],
 ['wiersz wygasający (S16)', 'lewa krawędź --danger + „za 2 dni”', '[S]', 'dopisać do K11 [R]'],
 ['rzadkość z kwadratem (S13)', 'inny zapis niż .tier-tag', '[S] rozbieżność', 'zastąpić .tier-tag — decyzja 2026-11-10 [D]'],
 ['koszyk, wiersz z −/+, pasek monet, portfel (S13)', 'komponenty sklepu', '[D] zastąpiony klockami systemu (v1.10)', 'S01 §6.23: .stepper, .tier-tag, .facts, .progress — ekran S13 przebudowany'],
 ['<code>.cc</code> (S12, ranking iteracja 2)', 'kod kraju zamiast flag-emoji', '[D] przyjęty jako testowy (v1.11)', 'K11 — .cc, zawsze z nazwą kraju'],
 ['<code>.delta-same</code>, <code>.podium-meta</code> (S12)', '„bez zmian”, meta pod podium', '[S]', 'dopisać do K11/K13 [R]'],
 ['wyszukiwarka z listą miast (migracja KodRekrut)', 'select w .search-main', '[D] przyjęty jako testowy (v1.11)', 'K09 — .search-main.has-select; poprawiony podwójny cień pola'],
 ['pionowa karta produktu (sklep, iteracja 2)', 'ilustracja nad nazwą, cena w stopce', '[D] przyjęty jako testowy (v1.11)', 'K07 — .card-vertical + .card-art + .card-price'],
 ['<code>.wallet</code> (sklep, iteracje 1–2)', 'saldo monet w nagłówku', '[D] wzorzec, bez klasy (v1.11)', 'S01 §6.24 — .badge-seg + sprite waluty'],
 ['hero, kroki (S10)', 'landing', '[S]', 'przepis „Landing” w skillu [R]'],
])

QUESTIONS = table(['#', 'Kwestia', 'Stan', 'Status'], [
 ['1', 'Właściciel systemu', 'Konrad Kosiorek (konrad.kosiorek@gmail.com) — decyzja 2026-11-10, S01 §0.5.', '[D] zamknięte'],
 ['2', 'Kolory wykresów a pakiety', 'Nowa paleta (terakota, morski, malinowy, zielony) + łupkowy dla jednej serii — wariant B, <a href="kwestie-otwarte.html#kolory">porównanie</a>; system 1.10.0.', '[D] zamknięte'],
 ['3', 'Kolor błędu w trybie ciemnym', '#F27961 jest w palecie Jehkoba32 (S01 §2.4).', '[D] zamknięte'],
 ['4', 'Skrót kwot', '„18–24 tys.” zamiast „18–24K” — decyzja właściciela 2026-11-10, system 1.9.1.', '[D] zamknięte'],
 ['5', 'Testy ręczne', 'Czytnik ekranu (VoiceOver, NVDA), Windows w wysokim kontraście, telefon — warunek statusu „stabilny” dla 14 rodzin testowych.', '[T]'],
 ['6', 'Kandydaci z ekranów', 'Przyjęte jako testowe: .card-meta, .opt-n (liczby liczy skrypt), .range (błąd „Od > Do”); koszyk złożony z istniejących klocków, ekran sklepu przebudowany (S01 §6.23). <a href="kwestie-otwarte.html#kandydaci">Porównanie</a>.', '[D] zamknięte'],
 ['6b', 'Kandydaci z testów skilla (iteracja 2)', 'Przyjęte jako testowe: .cc, .search-main.has-select, .card-vertical; saldo jako wzorzec z .badge-seg (S01 §6.24); usunięty podwójny cień pola wyszukiwarki. <a href="kandydaci.html">Porównanie</a>; system 1.11.0.', '[D] zamknięte'],
 ['7', 'Komponenty React / biblioteka Figma', 'Poza zakresem v1.9; tokens.json (format W3C) gotowy do importu.', '[R]'],
 ['—', 'Decyzje z v1.1 (zamknięte)', 'Przycisk 36 px, rzadkość .tier-tag, aria-sort="none", sortowanie przyciskami, skrót kwot, tryb ciemny i stany — <a href="decyzje-v1-1.html">decyzje v1.1</a>.', '[D]'],
])

# ---------- HTML ----------
REG = {x['id']: x for x in json.load(open(R + 'skills/panel-piksel-ui/assets/components.json'))['components']}
STATUS_OF = {'K01': ['button', 'button-compact', 'button-loading'], 'K02': ['badge'], 'K03': ['chip'], 'K04': ['count'], 'K05': ['avatar'], 'K06': ['panel-list'],
  'K07': ['card', 'card-meta', 'product-card-vertical'], 'K08': ['filters', 'opt-count', 'range'], 'K09': ['search-main', 'search-select'], 'K10': ['tabs'], 'K11': ['table', 'country-code'], 'K12': ['pagination'], 'K13': ['podium'], 'K14': ['tier', 'rarity-badge'],
  'K15': ['page-structure'], 'K16': ['callout', 'callout-danger'], 'K17': ['empty'], 'K18': ['facts'], 'K19': ['details'], 'K20': ['list-controls', 'sort-as-tabs'],
  'K21': ['icons'], 'K22': ['notice'], 'K23': ['form-controls', 'field-states'], 'K24': ['form-pattern'], 'K25': ['overlays', 'icon-button'], 'K26': ['mobile-nav'],
  'K27': ['selectable-table'], 'K28': ['loading', 'load-more'], 'K29': ['charts']}
SPL = {'stable': ('stabilny', 'ss'), 'preview': ('testowy', 'sp'), 'draft': ('kandydat', 'sd'), 'deprecated': ('wycofywany', 'sx')}
def status_line(cid):
    out = []
    for rid in STATUS_OF.get(cid, []):
        r = REG[rid]; lab, cls = SPL[r['status']]
        extra = ''
        if r['status'] == 'preview' and r.get('missing'): extra = ' — brakuje: ' + ', '.join(r['missing'])
        if r['status'] == 'deprecated': extra = f" — zastąpione: {html.escape(r['replacedBy'])}, usunięcie w {r['removeIn']}"
        out.append(f'<span class="sys sys-{cls}">{lab}</span> {html.escape(r["name"])} <span class="small">(od {r.get("since", "—")}{extra})</span>')
    return '<p class="sysline"><b>Status w systemie:</b> ' + ' · '.join(out) + '</p>' if out else ''

def card_html(c):
    sec = lambda t, body: f'<h3>{t}</h3>{body}'
    return f'''<section class="card-doc" id="{c['id']}"><p class="cid">{c['id']}</p><h2>{c['name']}</h2>{status_line(c['id'])}
{sec('Przeznaczenie i wybór', '<p>' + tag(c['purpose'].replace('{D}', '[D]').replace('{R}', '[R]').replace('{S}', '[S]').replace('{P}', '[P]').replace('{T}', '[T]')) + '</p>')}
{c['figures']}
{sec('Anatomia i komponenty składowe', table(ANAT_HEAD, c['anatomy']))}
{sec('Warianty i ich zastosowanie', table(VAR_HEAD, c['variants']) + (('<h4>Zaobserwowane kombinacje</h4>' + c['combos']) if c['combos'] else ''))}
{sec('Dostępne właściwości i atrybuty', table(PROP_HEAD, c['props']) + '<p class="small">Atrybuty <code>data-*</code>, klasy i ARIA pochodzą z implementacji referencyjnej (S02, S03). To konfiguracja dla designera i agenta budującego ekrany, nie publiczne API biblioteki. ' + st('D') + '</p>')}
{sec('Tokeny i style', table(TOK_HEAD, c['tokens']))}
{sec('Wymiary, odległości i układ', table(DIM_HEAD, c['dims']))}
{sec('Typografia', table(TYP_HEAD, c['typo']))}
{sec('Zachowanie, treści i lokalizacja', '<p>' + tag(c['behavior']) + '</p>')}
{sec('Zalecane i niewskazane praktyki', table(DD_HEAD, c['dodont']))}
{sec('Dostępność', '<p class="small">Cel: WCAG 2.2 AA dla webu [R]. Statyczne materiały i testy automatyczne w Chrome nie dowodzą zgodności.</p>' + table(A11Y_HEAD, c['a11y']))}
{sec('Źródła i otwarte kwestie', '<p class="small">' + c['sources'] + '</p>')}
</section>'''

INDEX = table(['Karta', 'Rodzina', 'Przeznaczenie', 'Źródła'], [[f'<a href="#{c["id"]}">{c["id"]}</a>', f'<a href="#{c["id"]}">{c["name"]}</a>', re.sub(r'<[^>]+>', '', c['purpose'].replace('{D}', '').replace('{R}', ''))[:110].rsplit(' ', 1)[0] + '…', c['sources'][:70]] for c in CARDS]) if False else ''
import re
INDEX = table(['Karta', 'Rodzina', 'Przeznaczenie (skrót)', 'Źródła'], [[f'<a href="#{c["id"]}">{c["id"]}</a>', f'<a href="#{c["id"]}">{html.escape(c["name"])}</a>', html.escape(re.sub(r'\[[A-Z]\]|\{[A-Z]\}', '', re.sub(r'<[^>]+>', '', c['purpose'])))[:120].rsplit(' ', 1)[0] + '…', html.escape(c['sources'])] for c in CARDS])

_cnt = {}
for _r in REG.values(): _cnt[_r['status']] = _cnt.get(_r['status'], 0) + 1
GOV = f'''<section class="part" id="zarzadzanie"><h2>Zarządzanie i statusy</h2>
<p>Każda rodzina ma status z rejestru <code>components.json</code> (S06): <span class="sys sys-ss">stabilny</span> spełnia checklistę „gotowe” (S01 §0.2), <span class="sys sys-sp">testowy</span> działa i ma przykład, ale brakuje części testów lub użycia na 2 ekranach — można używać, szczegóły mogą się zmienić w wersji minor, <span class="sys sys-sd">kandydat</span> widziany na ekranach, poza systemem, <span class="sys sys-sx">wycofywany</span> zastąpiony — działa do 2.0, check_screen ostrzega.</p>
<div class="boxes"><div class="box"><h3>Rejestr {{REG_VERSION}}</h3><ul><li>stabilne: {_cnt.get('stable', 0)}</li><li>testowe: {_cnt.get('preview', 0)}</li><li>kandydaci: {_cnt.get('draft', 0)}</li><li>wycofywane: {_cnt.get('deprecated', 0)}</li></ul></div>
<div class="box"><h3>Wersje</h3><ul><li>semver w <code>VERSION</code>: poprawka · nowy element · usunięcie</li><li>wycofanie → ostrzeżenie → usunięcie w następnej wersji major</li><li>historia: S01 §12</li></ul></div>
<div class="box"><h3>Jedno źródło i testy</h3><ul><li>kod: tylko <code>skills/panel-piksel-ui/assets/</code>; kopie aktualizuje <code>sync_system.py</code> (<code>--check</code>)</li><li>test wizualny: <code>visual_regression.py</code>, wzorce w <code>tests/visual/</code></li><li>przeglądarki i test z czytnikiem: S01 §0.6</li></ul></div></div>
</section>'''
REG_VERSION = json.load(open(R + 'skills/panel-piksel-ui/assets/components.json'))['version']
GOV = GOV.replace('{REG_VERSION}', REG_VERSION)

CSS = '''
:root{--bg:#f6f4ee;--rp:#fffdf8;--ink:#1d1b18;--mute:#6b655c;--line:#ddd6c7;--acc:#c2410c;--link:#1d4ed8}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;background:var(--bg);color:var(--ink);font:15.5px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--link)}code{font:.85em ui-monospace,Menlo,monospace;background:#ece6d8;padding:1px 4px;border-radius:3px}
.top{position:sticky;top:0;z-index:5;background:rgba(246,244,238,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:10px 24px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.top b{font:700 12px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.08em}.top nav{display:flex;gap:4px;flex-wrap:wrap}
.top nav a{font:700 11px ui-monospace,Menlo,monospace;text-decoration:none;color:var(--ink);border:1.5px solid var(--ink);padding:2px 6px;background:var(--rp)}
.top nav a:hover,.top nav a:focus-visible{background:var(--ink);color:var(--rp)}
main{max-width:1180px;margin:0 auto;padding:28px 24px 80px}
h1{font-size:clamp(28px,4.5vw,44px);line-height:1.1;margin:6px 0 10px;letter-spacing:-.02em}
h2{font-size:clamp(22px,3vw,30px);margin:0 0 10px;letter-spacing:-.01em}h3{font-size:14px;text-transform:uppercase;letter-spacing:.06em;margin:26px 0 8px}h4{font-size:14px;margin:14px 0 6px}
.kick{font:700 12px ui-monospace,Menlo,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--acc)}
.small{font-size:13.5px;color:var(--mute)}
.part,.card-doc{border-top:3px solid var(--ink);padding:30px 0 10px;margin-top:30px}
.sysline{margin:4px 0 14px;font-size:13.5px}.sys{display:inline-block;font:700 10px/1.4 ui-monospace,Menlo,monospace;padding:1px 6px;border-radius:3px;color:#fff;text-transform:uppercase}.sys-ss{background:#166534}.sys-sp{background:#1e40af}.sys-sd{background:#a16207}.sys-sx{background:#6b7280;text-decoration:line-through}
.cid{margin:0;font:700 12px ui-monospace,Menlo,monospace;color:var(--acc)}
.boxes{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin:18px 0}.box{background:var(--rp);border:1px solid var(--line);border-radius:6px;padding:14px 16px}.box h3{margin:0 0 6px}.box ul{margin:0;padding-left:18px;font-size:14px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--rp);margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{text-align:left;vertical-align:top;padding:7px 9px;border-bottom:1px solid var(--line)}thead th{background:#ede7d9;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em}
.st{display:inline-block;font:700 10px/1.4 ui-monospace,Menlo,monospace;padding:1px 5px;border-radius:3px;color:#fff;white-space:nowrap;vertical-align:1px}
.st-d{background:#166534}.st-s{background:#a16207}.st-r{background:#7e22ce}.st-p{background:#b91c1c}.st-t{background:#1e40af}
.sw{display:inline-block;width:12px;height:12px;border:1px solid #0003;vertical-align:-1px;margin-right:4px}
.figs{display:grid;gap:14px;margin:14px 0}.figs.c1{grid-template-columns:1fr}.figs.c2{grid-template-columns:repeat(2,minmax(0,1fr))}.figs.c3{grid-template-columns:repeat(3,minmax(0,1fr))}
.ev{margin:0;background:var(--rp);border:1px solid var(--line);border-radius:6px;overflow:hidden}.ev img{display:block;width:100%;height:auto;background:#f0edd8}
.ev figcaption{padding:8px 10px;font-size:13px}.meta{color:var(--mute);font-size:11.5px;word-break:break-word}
@media (max-width:820px){.figs.c2,.figs.c3{grid-template-columns:1fr}main{padding:18px 14px 60px}html{scroll-padding-top:110px}}
@media print{.top{display:none}.card-doc,.part{break-before:page}.ev,tr{break-inside:avoid}}
'''

nav = ''.join(f'<a href="#{a}">{t}</a>' for a, t in [('zrodla', 'Źródła'), ('indeks', 'Indeks'), ('zarzadzanie', 'Statusy'), ('fundamenty', 'Fundamenty')] + [(c['id'], c['id']) for c in CARDS] + [('aneks', 'Aneks'), ('pytania', 'Otwarte')])
src_rows = [[s[0], s[1], '<code>' + html.escape(s[2]) + '</code>', s[3]] for s in SOURCES]
HTML = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Panel i Piksel — komponenty v2.0</title><style>{CSS}</style></head><body>
<div class="top"><b>Panel &amp; Piksel · komponenty v2.0</b><nav aria-label="Spis">{nav}</nav></div>
<main>
<p class="kick"><a href="decyzje-v1-1.html" style="color:inherit">→ Decyzje v1.1</a> · Dokumentacja komponentów dla designerów · v2.0 · zaakceptowana · system 1.9.0 · 2026-11-10</p>
<h1>Panel &amp; Piksel — dokumentacja komponentów · v2.0</h1>
<p>Jak wybrać komponent, skonfigurować go i poprawnie zastosować. Dokumentacja opiera się na specyfikacji systemu (design.md 1.9.0), implementacji referencyjnej ze skilla <code>panel-piksel-ui</code>, siedmiu ekranach zbudowanych w tym systemie i trzech stronach przykładów (komponenty, wzorce, ikony).</p>
<div class="boxes">
<div class="box"><h3>Pokrycie</h3><ul><li>Przeanalizowane: 17 z 17 materiałów (7 dokumentów i kodu, 7 ekranów, 3 strony przykładów).</li><li>Rodziny: 29 (K01–K20 z v1, K21–K29 nowe w v2).</li><li>Dowody wizualne: {len(CROPS)} wycinki w 1280 i 390 px, jasne i ciemne (DPR 2), metadane w <code>docs/evidence/crops.json</code>.</li></ul></div>
<div class="box"><h3>Status</h3><ul><li>Wersja v2.0 zaakceptowana 2026-11-10 — dopisane rodziny z systemu 1.7–1.9: ikony, powiadomienia, pola formularza, formularz, nakładki, nawigacja mobilna, zaznaczanie wierszy, ładowanie, wykresy; statusy z rejestru przy każdej karcie; fundamenty uzupełnione o statusy, wykresy, ruch, warstwy, tryb ciemny.</li><li>Poprzednia wersja (v1.2, zaakceptowana): <a href="panel-piksel-komponenty-v1.html">panel-piksel-komponenty-v1.html</a>.</li><li>Testów z czytnikiem ekranu i na Windows nie wykonano.</li></ul></div>
<div class="box"><h3>Legenda</h3><ul style="list-style:none;padding:0"><li>{st('D')} ze specyfikacji, kodu referencyjnego lub zmierzone na ekranie</li><li>{st('S')} widoczne na ekranie, ale poza specyfikacją / przybliżenie</li><li>{st('R')} propozycja</li><li>{st('P')} brak danych lub konflikt</li><li>{st('T')} wymaga sprawdzenia we wdrożeniu (np. czytnik ekranu)</li></ul></div>
</div>
<section class="part" id="zrodla"><h2>Źródła</h2>{table(['ID', 'Materiał', 'Plik', 'Co z niego wynika'], src_rows)}
<p class="small">Standardy: <a href="https://www.w3.org/WAI/WCAG22/quickref/">WCAG 2.2 Quick Reference</a>, <a href="https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/">What’s New in WCAG 2.2</a>, <a href="https://www.w3.org/WAI/ARIA/apg/patterns/table/">APG Table</a> i <a href="https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/">Sortable Table Example</a>, <a href="https://www.w3.org/WAI/ARIA/apg/patterns/tabs/">APG Tabs</a>, <a href="https://www.w3.org/WAI/ARIA/apg/patterns/button/">APG Button</a>, <a href="https://www.w3.org/WAI/ARIA/apg/patterns/checkbox/">APG Checkbox</a>. APG to wzorce, nie kryteria normatywne.</p>
<p class="small">Dowody zachowania: testy klikania z <code>render_check.py</code> (7 ekranów + 3 strony przykładów, 0 martwych kontrolek), 23 testy list, 52 testy sortowania tabel, testy interakcji v1.7–1.8 (okno, menu, podpowiedź, przełącznik, licznik, plik, szuflada, walidacja, kroki, zaznaczanie, „Pokaż więcej”, dymki wykresów), test wizualny 12 widoków — Chrome headless 2026-11-09/10. Nie testowano czytnika ekranu ani innych przeglądarek.</p></section>
<section class="part" id="indeks"><h2>Indeks rodzin</h2>{INDEX}</section>
{GOV}
{FOUND}
{''.join(card_html(c) for c in CARDS)}
<section class="part" id="aneks"><h2>Aneks — elementy spoza systemu zaobserwowane na ekranach</h2><p class="small">Ekrany testowe (S11–S16) zbudowali agenci ze skillem; poniższe elementy nie występują w design.md. Od v1.9 są w rejestrze jako „kandydaci” albo „wycofywane”.</p>{ANNEX}</section>
<section class="part" id="pytania"><h2>Decyzje i otwarte kwestie</h2>{QUESTIONS}</section>
</main></body></html>'''
if os.environ.get('PP_NO_WRITE') != '1':
    open(OUT, 'w').write(HTML)
print(len(HTML) / 1e6, 'MB', len(CARDS), 'kart')
