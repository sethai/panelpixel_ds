#!/usr/bin/env python3
"""Statyczna kontrola ekranu HTML pod kątem zasad Panel & Piksel.

Użycie:  python3 check_screen.py ekran.html [kolejny.html ...]
Wynik:   lista ERROR / WARN; kod wyjścia 1, jeśli jest choć jeden ERROR.

Sprawdza tylko to, co da się sprawdzić bez przeglądarki. Nie zastępuje
obejrzenia renderu w 1280 px i 390 px.
"""
import hashlib
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')

# Dozwolone kolory: paleta SNES (Jehkoba32), akcenty NES używane przez system, biel, tinty systemu.
SNES = """00021C 1C284D 343473 2D5280 4D7A99 7497A6 A3CCD9 F0EDD8 732866 A6216E D94C87 D9214F F25565 F27961
993649 B36159 F09C60 B38F24 B3B324 F7C93E 17735F 119955 67B31B 1BA683 47CCA9 96E3C9 2469B3 0B8BE6 0BAFE6
F28D85 F0BB90""".split()
NES_ACCENTS = "0000BC F8B800 BCBCBC E45C10 AC7C00 6844FC 0078F8 7C7C7C".split()
EXTRA = "FFFFFF FFF F8F6EC EAFBC8 000 000000".split()
ALLOWED = {c.upper() for c in SNES + NES_ACCENTS + EXTRA}

FONT_OK = re.compile(r'(var\(--font-(sans|pixel)\)|archivo|press start 2p|inherit|system-ui|ui-monospace|monospace|sans-serif)', re.I)


def norm_hex(h):
    h = h.upper()
    if len(h) == 3:
        return h
    return h[:6]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.styles, self.inline, self.links, self.tags = [], [], [], []
        self._in_style = False
        self.html_lang = None
        self.has_viewport = False
        self.fonts_link = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if tag == 'html':
            self.html_lang = a.get('lang')
        if tag == 'meta' and a.get('name') == 'viewport':
            self.has_viewport = True
        if tag == 'link' and 'stylesheet' in (a.get('rel') or ''):
            href = a.get('href') or ''
            if 'fonts.googleapis.com' in href and 'Archivo' in href and 'Press+Start+2P' in href:
                self.fonts_link = True
            self.links.append(href)
        if tag == 'style':
            self._in_style = True
            self.styles.append('')
        if a.get('style'):
            self.inline.append((tag, a['style']))

    def handle_endtag(self, tag):
        if tag == 'style':
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.styles[-1] += data


def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def rules(css):
    """Prosty parser: zwraca (selektor, deklaracje) — ignoruje zagnieżdżenie @media przez spłaszczenie."""
    css = strip_comments(css)
    out = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        sel = m.group(1).strip()
        if sel.startswith('@'):
            continue
        out.append((sel, m.group(2)))
    return out


def decls(block):
    for d in block.split(';'):
        if ':' in d:
            k, v = d.split(':', 1)
            yield k.strip().lower(), v.strip()


def split_shadows(v):
    parts, depth, cur = [], 0, ''
    for ch in v:
        depth += ch == '('
        depth -= ch == ')'
        if ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def check(path):
    errors, warns = [], []
    src = open(path, encoding='utf-8').read()
    c = Collector()
    c.feed(src)
    base = os.path.dirname(os.path.abspath(path))

    # --- fundament ---
    if not c.html_lang:
        warns.append('Brak atrybutu lang na <html> (np. lang="pl").')
    if not c.has_viewport:
        warns.append('Brak <meta name="viewport">.')
    system_css_present = False
    screen_css = list(c.styles)
    for href in c.links:
        if href.startswith('http'):
            continue
        p = os.path.normpath(os.path.join(base, href))
        name = os.path.basename(p)
        if name in ('tokens.css', 'components.css'):
            system_css_present = True
            ref = os.path.join(ASSETS, name)
            if os.path.exists(p) and os.path.exists(ref) and file_hash(p) != file_hash(ref):
                warns.append(f'{href} różni się od wersji ze skillu — system nie powinien być edytowany (style ekranu trzymaj osobno).')
            if not os.path.exists(p):
                errors.append(f'Brak pliku {href} — skopiuj assets/{name} obok ekranu.')
        elif os.path.exists(p):
            screen_css.append(open(p, encoding='utf-8').read())
    # wklejony system w <style>?
    inlined_system = [s for s in screen_css if '--paper:' in s or '.btn-primary' in s and '--notch' in s]
    if inlined_system:
        system_css_present = True
        screen_css = [s for s in screen_css if s not in inlined_system]
    if not system_css_present:
        errors.append('Nie znaleziono tokens.css / components.css (ani linkiem, ani wklejonych) — ekran nie korzysta z systemu.')
    if not c.fonts_link and 'Archivo' not in src:
        warns.append('Brak linku do Google Fonts z Archivo i Press Start 2P.')

    # --- style ekranu (bez plików systemu) ---
    all_rules = []
    for css in screen_css:
        all_rules += rules(css)
    all_rules += [(f'<{t} style>', s) for t, s in c.inline]

    for sel, block in all_rules:
        for k, v in decls(block):
            vl = v.lower()
            if k == 'border-radius' or k.endswith('-radius'):
                if not re.fullmatch(r'0(px)?(\s+0(px)?)*', vl.replace('!important', '').strip()):
                    errors.append(f'{sel}: {k}: {v} — system nie używa zaokrągleń (promień 0, małe kontrolki: --notch).')
            if k in ('box-shadow', 'filter') and vl not in ('none', 'inherit'):
                for sh in split_shadows(vl if k == 'box-shadow' else ' '.join(re.findall(r'drop-shadow\(([^)]*)\)', vl))):
                    bare = re.sub(r'(rgba?|hsla?|var|color-mix)\([^)]*\)', ' ', sh)
                    nums = re.findall(r'(?<![\w#.-])(-?\d*\.?\d+)(?:px|rem|em)?(?![\w%])', bare)
                    if len(nums) >= 3 and float(nums[2]) != 0:
                        errors.append(f'{sel}: {k}: {v} — rozmyty cień; dozwolone tylko twarde cienie --shadow-sm/md/lg.')
                        break
            if k == 'font-family' and not FONT_OK.search(vl):
                errors.append(f'{sel}: font-family: {v} — używaj var(--font-sans) lub var(--font-pixel).')
            if k in ('font',) and re.search(r'["\'][^"\']+["\']', v) and not FONT_OK.search(vl):
                errors.append(f'{sel}: font: {v} — nieznana rodzina fontu.')
            if re.fullmatch(r'border(-(top|right|bottom|left))?(-width)?', k):
                for w in re.findall(r'(\d+(?:\.\d+)?)px', vl):
                    if float(w) not in (0, 2) and not (k == 'border-left-width' and float(w) == 10):
                        warns.append(f'{sel}: {k}: {v} — ramki w systemie mają 2 px.')
            for h in re.findall(r'#([0-9a-fA-F]{3,8})\b', v):
                if norm_hex(h) not in ALLOWED:
                    warns.append(f'{sel}: {k}: #{h} — kolor spoza palety SNES/akcentów NES; użyj tokenu var(--…).')
            if re.search(r'rgba?\(', vl) and k not in ('--paper-dots',) and 'var(' not in vl:
                warns.append(f'{sel}: {k}: {v} — kolor rgb() zamiast tokenu.')
            if re.search(r':(hover|active|focus)', sel) and k in ('width', 'height', 'min-height', 'padding', 'padding-top', 'padding-bottom', 'margin', 'border-width', 'font-size'):
                if not sel.startswith('.btn'):
                    warns.append(f'{sel}: {k} zmienia się w stanie — stany nie mogą zmieniać rozmiaru (użyj koloru, cienia, transform).')
            if k in ('animation', 'animation-name') and vl not in ('none',):
                warns.append(f'{sel}: animacja — system nie używa animacji (tylko przejścia 60 ms).')

    # --- struktura HTML ---
    def classes(a):
        return (a.get('class') or '').split()
    featured = sum(1 for t, a in c.tags if 'is-featured' in classes(a))
    podiums = sum(1 for t, a in c.tags if 'podium' in classes(a))
    searches = sum(1 for t, a in c.tags if 'search-main' in classes(a))
    loud = featured + podiums
    if podiums > 1:
        errors.append(f'{podiums} podia na stronie — dozwolone jedno.')
    if featured > 1:
        warns.append(f'{featured} wyróżnione panele (.is-featured) — zasada: jeden głośny element na ekran.')
    if featured and podiums:
        warns.append('Podium i wyróżniony panel na jednym ekranie — wybierz jeden głośny element.')
    if searches > 1:
        warns.append(f'{searches} wyszukiwarki główne (.search-main) — dozwolona jedna.')
    primaries = sum(1 for t, a in c.tags if 'btn-primary' in classes(a) and a.get('aria-disabled') != 'true')
    if primaries > 6:
        warns.append(f'{primaries} aktywnych przycisków głównych — jedna akcja główna na sekcję.')

    ids = [a.get('id') for t, a in c.tags if a.get('id')]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append(f'Zduplikowane id: {", ".join(sorted(dup))}.')
    for t, a in c.tags:
        cl = classes(a)
        if t == 'button' and 'type' not in a:
            warns.append(f'<button class="{" ".join(cl)}"> bez atrybutu type.')
        if 'btn' in cl and a.get('aria-disabled') == 'true' and 'is-loading' not in cl:
            ref = a.get('aria-describedby')
            if not ref or ref not in ids:
                warns.append('Zablokowany przycisk bez aria-describedby wskazującego powód (.btn-reason).')
        if 'btn' in cl and 'disabled' in a:
            warns.append('Przycisk z atrybutem disabled — użyj aria-disabled="true" + powód, żeby zachować fokus.')
        if t == 'img' and 'alt' not in a:
            errors.append(f'<img src="{a.get("src", "")}"> bez alt.')
        if t == 'input' and a.get('type') not in ('hidden', 'submit', 'button', 'checkbox', 'radio'):
            iid = a.get('id')
            labelled = a.get('aria-label') or a.get('aria-labelledby')
            if not labelled and not iid:
                # może być w <label> — sprawdzamy tekstowo w okolicy
                pass
    # Przycisk sortowania bez obsługi = obietnica bez pokrycia
    sort_btns = [a for t, a in c.tags if 'sort' in classes(a) and t in ('button', 'a')]
    if sort_btns:
        live_src = re.sub(r'<!--.*?-->', '', src, flags=re.S)
        scripts = ' '.join(re.findall(r'<script[^>]*>(.*?)</script>', live_src, re.S))
        has_lib = 'ppTableSort' in scripts or re.search(r'<script[^>]+src=["\'][^"\']*table-sort\.js', live_src)
        manual = 'data-sort-manual' in src
        sel_ref = re.search(r'["\'][^"\'\n]*\.sort\b(?!\()[^"\'\n]*["\']', scripts) or re.search(r'(classList\.contains|getElementsByClassName)\(\s*["\']sort["\']', scripts)
        custom = sel_ref and re.search(r'addEventListener\(\s*["\']click|onclick', scripts)
        if not (has_lib or (manual and custom) or custom):
            errors.append(f'{len(sort_btns)} przycisk(ów) .sort bez kodu sortowania — dołącz assets/table-sort.js albo zamień na statyczny <span class="sorted"> (kolejność stała).')
        if manual and not custom:
            errors.append('Tabela z data-sort-manual bez własnej obsługi sortowania w skrypcie.')
    # Niekonsekwentne sortowanie: część kolumn z danymi sortowalna, część nie (użytkownik klika i „nie działa”)
    for tbl in re.findall(r'<table\b.*?</table>', re.sub(r'<!--.*?-->', '', src, flags=re.S), re.S):
        heads = re.findall(r'<th\b[^>]*>(.*?)</th>', (re.search(r'<thead\b.*?</thead>', tbl, re.S) or re.match('', '')).group(0) if re.search(r'<thead\b', tbl) else '', re.S)
        if not heads or not any('class="sort"' in h for h in heads):
            continue
        plain = [re.sub(r'<[^>]+>', '', h).strip() for h in heads if 'class="sort"' not in h and 'class="sorted"' not in h]
        plain = [h for h in plain if h and h not in ('#', 'Akcje', 'Akcja', '') and 'sr-only' not in h]
        if plain:
            warns.append('Tabela sortuje tylko część kolumn — bez sortowania: ' + ', '.join(plain[:6]) + '. Daj sortowanie każdej kolumnie z danymi (albo żadnej), inaczej klik w te nagłówki „nie działa”.')
    for t, a in c.tags:
        if 'sort' in classes(a) and a.get('aria-sort'):
            warns.append('aria-sort na przycisku .sort — atrybut należy do <th> (table-sort.js przenosi go sam).')
            break
    # Kontrolki, które coś obiecują (zakładki, filtry, przełączniki), a na stronie nie ma żadnego skryptu
    live_all = re.sub(r'<!--.*?-->', '', src, flags=re.S)
    has_script = bool(re.search(r'<script(?![^>]*type=["\']application/(ld\+)?json)[^>]*>(?!\s*</script>)', live_all)) or bool(re.search(r'<script[^>]+src=', live_all))
    promising = []
    if re.search(r'role=["\']tab["\']', src) or re.search(r'class="tabs"[^>]*>\s*<button', src):
        promising.append('zakładki')
    if re.search(r'class="panel-filters"', src) and re.search(r'type="checkbox"|type="number"|type="search"', src):
        promising.append('filtry')
    if re.search(r'<button[^>]+aria-pressed', src):
        promising.append('przełączniki aria-pressed')
    if promising and not has_script:
        errors.append('Na stronie są ' + ', '.join(promising) + ', ale nie ma żadnego skryptu — dołącz assets/list-controls.js (listy kart) / table-sort.js (tabele) albo własny kod, inaczej kontrolki są martwe.')
    if re.search(r'data-(list|sort-for|filter-for)=', src) and 'ppListControls' not in live_all and not re.search(r'<script[^>]+src=["\'][^"\']*list-controls\.js', live_all):
        errors.append('Użyto atrybutów data-list / data-sort-for / data-filter-for bez skryptu list-controls.js.')
    # v1.6: kwota w wierszu listy powinna mieć wersję skróconą
    if re.search(r'class="list-value">\s*[\d\s\u00a0]+(?:[–-][\d\s\u00a0]+)?\s*zł', src):
        warns.append('Kwota w .list-value bez pary .amt-full/.amt-short — na 390 px ucina nazwy; użyj <span class="amt-full">…</span><span class="amt-short" aria-hidden="true">18–24 tys.</span>.')
    # v1.6: wpisane kolory systemu w stylach ekranu psują tryb ciemny
    screen_css = ' '.join(re.findall(r'<style(?![^>]*id="pp-)[^>]*>(.*?)</style>', src, re.S))
    if re.search(r'#(00021C|F0EDD8|FFFFFF|fff)\b', screen_css, re.I):
        warns.append('Style ekranu zawierają wpisane kolory systemu (#00021C/#F0EDD8/#FFF) — użyj tokenów (var(--ink), var(--line), var(--surface)…), inaczej tryb ciemny się psuje.')
    # v1.7: emoji zamiast ikon systemu
    body_txt = re.sub(r'<(script|style)\b.*?</\1>', '', src, flags=re.S)
    if re.search('[\U0001F300-\U0001FAFF\u2600-\u27BF]', body_txt):
        warns.append('Emoji w treści — użyj ikon pikselowych systemu (.icon .i-… / .sprite .s-…, icons.css).')
    # v1.11: flagi-emoji → .cc; lista wyboru w wyszukiwarce → .search-main.has-select
    if re.search('[\U0001F1E6-\U0001F1FF]{2}', body_txt):
        warns.append('Flagi-emoji — użyj kodu kraju <span class="cc" aria-hidden="true">PL</span> z pełną nazwą obok (design.md §6.11).')
    for m in re.finditer(r'<form\b[^>]*class="([^"]*\bsearch-main\b[^"]*)"[^>]*>(.*?)</form>', body_txt, re.S):
        if '<select' in m.group(2) and 'has-select' not in m.group(1):
            warns.append('Lista wyboru w .search-main bez modyfikatora .has-select — dodaj class="search-main has-select" i owiń <select> w <div class="select"> (design.md §6.11).')
    # v1.7: klasy ikon bez icons.css (szukamy w znacznikach, nie we wklejonym CSS)
    markup = re.sub(r'<(script|style)\b.*?</\1>', '', src, flags=re.S)
    if re.search(r'class="[^"]*\b(icon|sprite)\b[^"]*\b(i|s)-[a-z]', markup) and 'icons.css' not in src and 'id="pp-icons"' not in src:
        errors.append('Użyto ikon (.icon .i-… / .sprite .s-…) bez assets/icons.css — ikony będą niewidoczne.')
    # v1.7: kontrolki z ui-controls.js bez skryptu
    if re.search(r'data-dialog-open|role="switch"|data-step=|class="upload"|class="menu"|nav-toggle', markup) and 'ppUi' not in src and 'ui-controls.js' not in src:
        errors.append('Okno / szuflada / przełącznik / licznik / plik / menu / zwijana nawigacja bez assets/ui-controls.js — kontrolki będą martwe.')
    # v1.8: wzorce wymagające skryptów
    if re.search(r'data-chart=', markup) and 'ppCharts' not in src and 'charts.js' not in src:
        errors.append('Wykres (data-chart) bez assets/charts.js — nic się nie narysuje.')
    if re.search(r'data-validate|data-wizard|data-selectable', markup) and 'ppUi' not in src and 'ui-controls.js' not in src:
        errors.append('Walidacja / kroki / zaznaczanie wierszy bez assets/ui-controls.js.')
    if re.search(r'data-page-size|data-more-for', markup) and 'ppListControls' not in src and 'list-controls.js' not in src:
        errors.append('„Pokaż więcej” (data-page-size) bez assets/list-controls.js.')
    if re.search(r'<form\b[^>]*>', markup) and re.search(r'\brequired\b', markup) and 'data-validate' not in markup:
        warns.append('Formularz z polami required bez data-validate — przeglądarka pokaże własne dymki zamiast komunikatów systemu (podsumowanie błędów, błąd pod polem).')
    if re.search(r'data-chart="segments"', markup) and len(re.findall(r'"labels"\s*:\s*\[([^\]]*)\]', src)) and any(l.count(',') >= 4 for l in re.findall(r'data-chart="segments"[\s\S]*?"labels"\s*:\s*\[([^\]]*)\]', src)):
        warns.append('Wykres „segments” ma więcej niż 4 kategorie — zsumuj resztę w „Inne”.')
    # v1.9: wycofywane wzorce z assets/components.json (status deprecated + regex detect)
    try:
        import json as _json
        _reg = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'components.json'), encoding='utf-8'))
        _screen_css = ' '.join(re.findall(r'<style(?![^>]*id="pp-)[^>]*>(.*?)</style>', src, re.S))
        for _c in _reg['components']:
            if _c.get('status') == 'deprecated' and _c.get('detect') and re.search(_c['detect'], markup + ' ' + _screen_css):
                warns.append(f'Wycofywany wzorzec: {_c["name"]} (od {_c["deprecatedIn"]}, usunięcie w {_c["removeIn"]}) — użyj: {_c["replacedBy"]}.')
    except (OSError, ValueError, KeyError):
        pass
    h1 = sum(1 for t, a in c.tags if t == 'h1')
    if h1 != 1:
        warns.append(f'Liczba <h1> na stronie: {h1} (oczekiwana 1).')
    if '<table' in src and '<th' not in src:
        errors.append('Tabela bez komórek nagłówkowych <th>.')
    # Press Start 2P na długim tekście: <p> lub .prose z klasą/stylem pixel
    for m in re.finditer(r'<p[^>]*style="[^"]*font-pixel[^"]*"[^>]*>([^<]{40,})<', src):
        warns.append('Długi akapit w foncie pikselowym — Press Start 2P tylko dla liczb i krótkich etykiet.')
    if re.search(r'\b(lorem|ipsum)\b', src, re.I):
        warns.append('Tekst „lorem ipsum” — użyj realistycznych danych (ujawniają problemy z długością).')

    return errors, warns


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    total_err = 0
    for path in sys.argv[1:]:
        errors, warns = check(path)
        total_err += len(errors)
        print(f'== {path}')
        for e in dict.fromkeys(errors):
            print('  ERROR', e)
        for w in dict.fromkeys(warns):
            print('  WARN ', w)
        if not errors and not warns:
            print('  OK — brak uwag (obejrzyj jeszcze render w 1280 i 390 px).')
        else:
            print(f'  Podsumowanie: {len(set(errors))} błędów, {len(set(warns))} ostrzeżeń.')
    sys.exit(1 if total_err else 0)


if __name__ == '__main__':
    main()
