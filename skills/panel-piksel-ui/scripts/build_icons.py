#!/usr/bin/env python3
"""Buduje pikselowe ikony Panel & Piksel z rysunków ASCII 12×12.

Wynik:
  assets/icons.css      — klasy .icon .i-<nazwa> (maska, kolor = currentColor) i .sprite .s-<nazwa> (kolorowe przedmioty)
  assets/icons/*.svg    — pojedyncze pliki SVG (do Figmy, innych projektów)

Użycie:  python3 build_icons.py
Siatka 12×12, 1 piksel ikony = 2 px przy rozmiarze 24 px. Rysuj tylko w skali całkowitej (12 / 24 / 36 px).

Ikony UI (MONO): '#' = piksel w kolorze tekstu. Działają w trybie jasnym, ciemnym i wysokiego kontrastu.
Przedmioty (ITEMS): litery = kolory palety, 'k' = obrys. Dla trybu ciemnego obrys zamienia się na jasny.
"""
import os
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')

MONO = {
# --- nawigacja i akcje ---
'search': """
............
..#####.....
.##...##....
.#.....#....
.#.....#....
.#.....#....
.##...##....
..######....
.......###..
........###.
.........##.
............""",
'close': """
............
.##......##.
.###....###.
..###..###..
...######...
....####....
....####....
...######...
..###..###..
.###....###.
.##......##.
............""",
'chevron-right': """
............
...##.......
....##......
.....##.....
......##....
.......##...
.......##...
......##....
.....##.....
....##......
...##.......
............""",
'menu': """
............
............
.##########.
.##########.
............
.##########.
.##########.
............
.##########.
.##########.
............
............""",
'filter': """
............
.##########.
.##########.
..########..
...######...
....####....
....####....
....####....
....####....
....###.....
....##......
............""",
'sort': """
............
.....##.....
....####....
...######...
..########..
............
............
..########..
...######...
....####....
.....##.....
............""",
'plus': """
............
.....##.....
.....##.....
.....##.....
.....##.....
.##########.
.##########.
.....##.....
.....##.....
.....##.....
.....##.....
............""",
'minus': """
............
............
............
............
............
.##########.
.##########.
............
............
............
............
............""",
'check': """
............
............
.........##.
........###.
.......###..
.##...###...
.###.###....
..#####.....
...###......
....#.......
............
............""",
'more': """
............
............
............
............
............
.##..##..##.
.##..##..##.
............
............
............
............
............""",
'edit': """
............
.........##.
........####
.......####.
......####..
.....####...
....####....
...####.....
..####......
.###........
.##.........
............""",
'trash': """
....####....
.##########.
............
..########..
..#.#..#.#..
..#.#..#.#..
..#.#..#.#..
..#.#..#.#..
..#.#..#.#..
..########..
............
............""",
'upload': """
.....##.....
....####....
...######...
..########..
.....##.....
.....##.....
.....##.....
.....##.....
.#...##...#.
.#........#.
.##########.
............""",
'download': """
.....##.....
.....##.....
.....##.....
.....##.....
..########..
...######...
....####....
.....##.....
.#........#.
.#........#.
.##########.
............""",
'external': """
............
.......#####
.........###
........#.##
.......#...#
.#####.#....
.#....#.....
.#..........
.#.......#..
.#.......#..
.#########..
............""",
'eye': """
............
............
....####....
..##....##..
.#...##...#.
#...####...#
#...####...#
.#...##...#.
..##....##..
....####....
............
............""",
'lock': """
............
....####....
...#....#...
...#....#...
...#....#...
..########..
..########..
..###..###..
..###..###..
..########..
..########..
............""",
# --- obiekty domeny ---
'user': """
............
....####....
...######...
...######...
...######...
....####....
............
..########..
.##########.
.##########.
.##########.
............""",
'home': """
............
.....##.....
....####....
...######...
..########..
.##########.
..########..
..###..###..
..###..###..
..###..###..
..###..###..
............""",
'mail': """
............
............
.##########.
.###....###.
.#.##..##.#.
.#..####..#.
.#...##...#.
.#........#.
.#........#.
.##########.
............
............""",
'bell': """
.....##.....
....####....
...######...
...######...
..########..
..########..
..########..
.##########.
.##########.
............
....####....
............""",
'pin': """
....####....
...######...
..###..###..
..##....##..
..###..###..
...######...
...######...
....####....
....####....
.....##.....
.....##.....
............""",
'hourglass': """
.##########.
..#......#..
..########..
...######...
....####....
.....##.....
.....##.....
....#..#....
...#....#...
..#..##..#..
..#.####.#..
.##########.""",
'calendar': """
............
...#....#...
.##########.
.##########.
.#........#.
.#.##.##..#.
.#........#.
.#.##.##..#.
.#........#.
.##########.
............
............""",
'cart': """
............
##..........
.#..........
.##########.
..#########.
..########..
..#######...
..#.........
..########..
...##..##...
...##..##...
............""",
'list': """
............
.##.#######.
.##.#######.
............
.##.#######.
.##.#######.
............
.##.#######.
.##.#######.
............
............
............""",
'grid': """
............
.####..####.
.####..####.
.####..####.
.####..####.
............
............
.####..####.
.####..####.
.####..####.
.####..####.
............""",
'heart': """
............
..##....##..
.####..####.
.##########.
.##########.
.##########.
..########..
...######...
....####....
.....##.....
............
............""",
'heart-outline': """
............
..##....##..
.#..#..#..#.
.#...##...#.
.#........#.
.#........#.
..#......#..
...#....#...
....#..#....
.....##.....
............
............""",
'star': """
.....##.....
.....##.....
....####....
############
.##########.
..########..
...######...
...######...
..###..###..
..##....##..
.##......##.
............""",
'coin': """
...######...
..#......#..
.#...##...#.
#....##....#
#....##....#
#....##....#
#....##....#
#....##....#
#....##....#
.#...##...#.
..#......#..
...######...""",
'trophy': """
.##########.
###......###
#.#......#.#
#.#......#.#
.##......##.
..#......#..
...#....#...
....####....
.....##.....
....####....
...######...
...######...""",
# --- statusy (wypełnione kafelki z wyciętym znakiem) ---
'info': """
...######...
..########..
.####..####.
.####..####.
.##########.
.####..####.
.####..####.
.####..####.
.####..####.
..########..
...######...
............""",
'success': """
...######...
..########..
.#########..
.#######..#.
.######..##.
.#..##..###.
.##....####.
.###..#####.
.##########.
..########..
...######...
............""",
'warning': """
.....##.....
....####....
....####....
...##..##...
...##..##...
..###..###..
..###..###..
.##########.
#####..#####
############
............
............""",
'error': """
...######...
..########..
.#..####..#.
.##..##..##.
.###....###.
.####..####.
.####..####.
.###....###.
.##..##..##.
.#..####..#.
..########..
...######...""",
}
# pochodne
def _rot(art, mode):
    rows = [r for r in art.strip('\n').split('\n')]
    if mode == 'mirror':
        return '\n'.join(r[::-1] for r in rows)
    if mode == 'cw':   # obrót o 90° w prawo
        return '\n'.join(''.join(rows[11 - c][r] for c in range(12)) for r in range(12))
    if mode == 'ccw':
        return '\n'.join(''.join(rows[c][11 - r] for c in range(12)) for r in range(12))
MONO['chevron-left'] = _rot(MONO['chevron-right'], 'mirror')
MONO['chevron-down'] = _rot(MONO['chevron-right'], 'cw')
MONO['chevron-up'] = _rot(MONO['chevron-right'], 'ccw')

# Przedmioty z gier — kolorowe; 'k' = obrys
ITEM_COLORS = {
    'k': '#00021C', 'y': '#F8B800', 'd': '#AC7C00', 'w': '#FFFFFF', 'r': '#D9214F', 'R': '#993649',
    'p': '#D94C87', 'b': '#2469B3', 'c': '#0BAFE6', 'g': '#17735F', 'm': '#96E3C9', 'n': '#993649',
    'N': '#732866', 's': '#BCBCBC', 'e': '#F0EDD8', 'o': '#E45C10', 'v': '#6844FC', 'a': '#A3CCD9',
}
DARK_OUTLINE = '#F0EDD8'
ITEMS = {
'coin': """
...kkkkkk...
..kyyyyyyk..
.kywyyyyydk.
kywyyddyyydk
kyyyyddyyydk
kyyyyddyyydk
kyyyyddyyydk
kyyyyddyyydk
kyyyyddyyydk
.kyyyyyyyddk
..kddddddk..
...kkkkkk...""",
'heart': """
............
.kkk....kkk.
krrrk..krrrk
krwrrkkrrrRk
krwrrrrrrrRk
krrrrrrrrrRk
.krrrrrrrRk.
..krrrrrRk..
...krrrRk...
....krRk....
.....kk.....
............""",
'star': """
.....kk.....
....kyyk....
....kyyk....
kkkkywyykkkk
kyyyywyyyydk
.kyyyyyyydk.
..kyyyyyydk.
..kyyyyyyk..
.kyyykkyyyk.
.kyyk..kyyk.
kykk....kkyk
kk........kk""",
'gem': """
............
............
...kkkkkk...
..kccwcbbk..
.kccwccbbbk.
kkkkkkkkkkkk
.kccbbbbbbk.
..kcbbbbbk..
...kcbbbk...
....kcbk....
.....kk.....
............""",
'trophy': """
.kkkkkkkkkk.
kkwyyyyyydkk
kkwyyyyyydkk
.kkyyyyyydk.
..kyyyyyyk..
...kyyydk...
....kyyk....
....kddk....
...kyyyyk...
..kkkkkkkk..
..kddddddk..
..kkkkkkkk..""",
'potion': """
....kkkk....
....knnk....
....kkkk....
....kwek....
...kweeek...
..kweeeeek..
.kwrrrrrrrk.
kwrrrrrrrrRk
krrrrrrrrrRk
krrrrrrrrRRk
.kRRRRRRRRk.
..kkkkkkkk..""",
'chest': """
............
..kkkkkkkk..
.knnnnnnnnk.
knnnnnnnnnnk
kkkkkyykkkkk
kNNNkyykNNNk
kNNNNkkNNNNk
kNNNNNNNNNNk
kNNNNNNNNNNk
kkkkkkkkkkkk
............
............""",
'key': """
............
.kkkk.......
kyyyyk......
kykkyk......
kykkykkkkkkk
kyyyyyyyyyyk
.kkkkkkyykyk
.......kk.k.
............
............
............
............""",
'scroll': """
..kkkkkkkkk.
.keeeeeeeeek
.kekkkkkkeek
.keeeeeeeeek
.kekkkkkeeek
.keeeeeeeeek
.kekkkkkkeek
.keeeeeeeeek
.kekkkkeeeek
kkkeeeeeeeek
kaakkkkkkkk.
.kk.........""",
'shield': """
kkkkkkkkkkkk
kbbbbbwbbbbk
kbbbbbwbbbbk
kbbbbbwbbbbk
kwwwwwwwwwwk
kbbbbbwbbbbk
.kbbbbwbbbk.
.kbbbbwbbbk.
..kbbbwbbk..
...kbbwbk...
....kkkk....
............""",
'sword': """
..........kk
.........kak
........kak.
.......kak..
......kak...
.....kak....
.k..kak.....
.kkkak......
..kok.......
.kkokk......
kk...k......
k...........""",
'flag': """
.kk.........
.kskkkkkkk..
.ksggggggk..
.ksgmgggggk.
.ksggggggk..
.kskkkkkkk..
.ks.........
.ks.........
.ks.........
.ks.........
kkkk........
kkkk........""",
}

def path_from(art, want):
    rows = [r for r in art.strip('\n').split('\n')]
    assert len(rows) == 12 and all(len(r) == 12 for r in rows), (want, [len(r) for r in rows])
    d = []
    for y, row in enumerate(rows):
        x = 0
        while x < 12:
            if want(row[x]):
                s = x
                while x < 12 and want(row[x]):
                    x += 1
                d.append(f'M{s} {y}h{x - s}v1h-{x - s}z')
            else:
                x += 1
    return ''.join(d)

def svg_mono(art):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" shape-rendering="crispEdges"><path d="{path_from(art, lambda ch: ch == "#")}"/></svg>'

def svg_item(art, dark=False):
    used = sorted({ch for row in art.strip().split('\n') for ch in row if ch != '.'})
    parts = []
    for ch in used:
        col = ITEM_COLORS[ch]
        if dark and ch == 'k':
            col = DARK_OUTLINE
        parts.append(f'<path fill="{col}" d="{path_from(art, lambda c, ch=ch: c == ch)}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" shape-rendering="crispEdges">{"".join(parts)}</svg>'

def data_uri(svg):
    return 'url("data:image/svg+xml,' + urllib.parse.quote(svg, safe=' =:/";,') .replace('"', "'") + '")'

# Kolorowe wersje ikon interfejsu (v1.1): kształt ikony w kolorze + twardy cień 1 px w prawo-dół,
# jak napisy i ikony w menu gier 16-bit. Kolor = znaczenie ikony; para (tryb jasny, tryb ciemny).
BLUE, GREEN, RED, ORANGE, PURPLE, PLUM, GOLD, SLATE = (
    ('#2469B3', '#0BAFE6'), ('#17735F', '#96E3C9'), ('#D9214F', '#F27961'), ('#E45C10', '#E45C10'),
    ('#6844FC', '#9878F8'), ('#993649', '#D94C87'), ('#AC7C00', '#F8B800'), ('#2D5280', '#A3CCD9'))
TINT = {
    'search': BLUE, 'close': RED, 'menu': SLATE, 'more': SLATE, 'filter': PURPLE, 'sort': PURPLE,
    'chevron-left': SLATE, 'chevron-right': SLATE, 'chevron-up': SLATE, 'chevron-down': SLATE,
    'plus': GREEN, 'minus': RED, 'check': GREEN, 'edit': ORANGE, 'trash': RED, 'upload': GREEN, 'download': BLUE,
    'external': BLUE, 'eye': BLUE, 'lock': SLATE, 'list': SLATE, 'grid': SLATE, 'home': PLUM, 'user': BLUE,
    'mail': BLUE, 'bell': GOLD, 'pin': RED, 'calendar': PLUM, 'hourglass': GOLD, 'cart': GREEN,
    'heart-outline': RED, 'info': BLUE, 'success': GREEN, 'warning': ORANGE, 'error': RED,
}
SHADOW = '#00021C'
SHADOW_DARK = '#000000'

def svg_tinted(art, fill, shadow):
    rows = [r for r in art.strip('\n').split('\n')]
    on = lambda x, y: 0 <= x < 12 and 0 <= y < 12 and rows[y][x] == '#'
    sh = [[('#' if (on(x - 1, y - 1) and not on(x, y)) else '.') for x in range(12)] for y in range(12)]
    sh_art = '\n'.join(''.join(r) for r in sh)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" shape-rendering="crispEdges">'
            f'<path fill="{shadow}" d="{path_from(sh_art, lambda c: c == "#")}"/>'
            f'<path fill="{fill}" d="{path_from(art, lambda c: c == "#")}"/></svg>')

PL = {'search': 'szukaj', 'close': 'zamknij', 'chevron-right': 'dalej', 'chevron-left': 'wstecz', 'chevron-down': 'rozwiń', 'chevron-up': 'zwiń',
      'menu': 'menu', 'filter': 'filtry', 'sort': 'sortuj', 'plus': 'dodaj', 'minus': 'odejmij', 'check': 'gotowe', 'more': 'więcej', 'edit': 'edytuj',
      'trash': 'usuń', 'upload': 'wgraj', 'download': 'pobierz', 'external': 'link zewn.', 'eye': 'podgląd', 'lock': 'blokada', 'user': 'konto',
      'home': 'start', 'mail': 'wiadomość', 'bell': 'powiadomienia', 'pin': 'lokalizacja', 'hourglass': 'czas / dodano', 'calendar': 'data',
      'cart': 'koszyk', 'list': 'widok listy', 'grid': 'widok siatki', 'heart': 'zapisano', 'heart-outline': 'zapisz', 'star': 'polecane',
      'coin': 'widełki / cena', 'trophy': 'ranking', 'info': 'informacja', 'success': 'sukces', 'warning': 'ostrzeżenie', 'error': 'błąd'}
PL_ITEMS = {'coin': 'moneta — cena, widełki', 'heart': 'serce — zapisane', 'star': 'gwiazda — polecane', 'gem': 'klejnot — pakiet',
            'trophy': 'puchar — ranking', 'potion': 'mikstura — przedmiot sklepu', 'chest': 'skrzynia — nagroda, oferta specjalna',
            'key': 'klucz — dostęp, logowanie', 'scroll': 'zwój — CV, dokument', 'shield': 'tarcza — weryfikacja, bezpieczeństwo',
            'sword': 'miecz — przedmiot sklepu', 'flag': 'flaga — punkt kontrolny, cel'}
ORDER = ['search', 'close', 'menu', 'more', 'filter', 'sort', 'chevron-left', 'chevron-right', 'chevron-up', 'chevron-down', 'plus', 'minus',
         'check', 'edit', 'trash', 'upload', 'download', 'external', 'eye', 'lock', 'list', 'grid', 'home', 'user', 'mail', 'bell', 'pin',
         'calendar', 'hourglass', 'cart', 'heart-outline', 'heart', 'star', 'coin', 'trophy', 'info', 'success', 'warning', 'error']


def gallery(tinted):
    tile = lambda cls, code, label: f'<li><span class="{cls}" aria-hidden="true"></span><code>{code}</code><span>{label}</span></li>'
    ui = ''.join(tile(f'icon icon-lg i-{n}', f'i-{n}', PL[n]) for n in ORDER)
    col = ''.join(tile(f'sprite sprite-lg s-{n}', f's-{n}', PL[n]) for n in ORDER if n in tinted)
    items = ''.join(tile(f'sprite sprite-lg s-{n}', f's-{n}', PL_ITEMS[n]) for n in ITEMS)
    return f"""<!doctype html>
<html lang="pl" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ikony · Panel i Piksel</title>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800;900&family=Press+Start+2P&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/tokens.css">
  <link rel="stylesheet" href="../assets/components.css">
  <link rel="stylesheet" href="../assets/icons.css">
  <!-- Strona wygenerowana przez scripts/build_icons.py — nie edytuj ręcznie -->
  <style id="screen">
    .ico-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; margin: 0; padding: 0; list-style: none; }}
    .ico-grid li {{ display: grid; justify-items: start; gap: 6px; padding: 12px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-sm); font-size: 13px; color: var(--ink-2); }}
    .ico-grid code {{ font: 12px ui-monospace, Menlo, monospace; color: var(--ink); }}
    .sizes {{ display: flex; flex-wrap: wrap; gap: 20px; align-items: end; }}
    .ex {{ margin: 40px 0 0; padding-top: 24px; border-top: var(--border); }}
    .ex > h2 {{ margin: 0 0 4px; font: 900 18px/28px var(--font-sans); }}
    .ex > p {{ margin: 0 0 16px; max-width: 76ch; color: var(--ink-2); font-size: 14px; }}
    .theme-switch {{ margin-left: auto; }}
    .demo-row {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }}
  </style>
</head>
<body class="bg-dots">
<header class="site-header"><div class="container">
  <a class="logo" href="komponenty.html">PANEL<span>&amp;PIKSEL</span></a>
  <nav class="site-nav" aria-label="Przykłady"><a href="komponenty.html">Komponenty</a><a href="ikony.html" aria-current="page">Ikony</a></nav>
  <div class="tabs theme-switch" role="group" aria-label="Motyw">
    <button type="button" aria-pressed="true" data-theme-set="light">Jasny</button><button type="button" aria-pressed="false" data-theme-set="dark">Ciemny</button>
  </div></div></header>
<main class="container" id="tresc">
  <div class="page-head"><div><h1>Ikony pikselowe</h1>
  <p>Siatka 12 × 12, rysowane piksel po pikselu w duchu ikon z gier 8/16-bit. Trzy grupy: <b>ikony interfejsu</b> w kolorze tekstu ({len(ORDER)}), <b>kolorowe wersje</b> tych samych ikon z twardym cieniem ({len(tinted)}) i <b>przedmioty z gier</b> ({len(ITEMS)}). Źródło: <code>scripts/build_icons.py</code>.</p></div></div>

  <section class="ex" aria-labelledby="h1"><h2 id="h1">Ikony interfejsu · <code>.icon .i-…</code></h2>
    <p>Kolor = kolor tekstu, więc działają w każdym motywie i w trybie wysokiego kontrastu. To podstawowy wybór do przycisków, pól i nawigacji. Pokazane w 36 px.</p>
    <ul class="ico-grid">{ui}</ul></section>

  <section class="ex" aria-labelledby="h2"><h2 id="h2">Kolorowe wersje · <code>.sprite .s-…</code></h2>
    <p>Ten sam kształt w kolorze znaczenia (niebieski — informacja i nawigacja, zielony — dodanie i sukces, czerwony — usunięcie i błąd, pomarańczowy — edycja i ostrzeżenie, fioletowy — filtry, złoty — czas i powiadomienia) z twardym cieniem 1 px jak w menu gier 16-bit. Do akcentów: kafelki kategorii, puste stany, nagłówki sekcji, listy cech. W ciemnym motywie kolor jaśnieje. Nie zastępują ikon interfejsu w przyciskach — kolor ma tam znaczyć stan, nie dekorację. Serce, gwiazda, moneta i puchar mają ręcznie rysowane wersje w grupie przedmiotów.</p>
    <ul class="ico-grid">{col}</ul></section>

  <section class="ex" aria-labelledby="h3"><h2 id="h3">Przedmioty z gier · <code>.sprite .s-…</code></h2>
    <p>Ręcznie rysowane, wielokolorowe, z obrysem: moneta przy kwotach i cenach, serce przy zapisanych, puchar w rankingu, klejnot przy pakietach, zwój przy CV. W ciemnym motywie obrys zmienia się na jasny.</p>
    <ul class="ico-grid">{items}</ul></section>

  <section class="ex" aria-labelledby="h4"><h2 id="h4">Rozmiary — tylko wielokrotności 12</h2>
    <div class="sizes"><span class="icon icon-sm i-search" aria-hidden="true"></span><span class="icon i-search" aria-hidden="true"></span><span class="icon icon-lg i-search" aria-hidden="true"></span><span class="icon icon-xl i-search" aria-hidden="true"></span>
      <span class="sprite sprite-sm s-search" aria-hidden="true"></span><span class="sprite s-search" aria-hidden="true"></span><span class="sprite sprite-lg s-search" aria-hidden="true"></span><span class="sprite sprite-xl s-search" aria-hidden="true"></span>
      <span class="sprite sprite-sm s-coin" aria-hidden="true"></span><span class="sprite s-coin" aria-hidden="true"></span><span class="sprite sprite-lg s-coin" aria-hidden="true"></span><span class="sprite sprite-xl s-coin" aria-hidden="true"></span></div>
    <p style="font-size:13px;color:var(--ink-3)">12 · 24 · 36 · 48 px. Rozmiary pośrednie (np. 16 px, 20 px) rozmywają piksele.</p></section>

  <section class="ex" aria-labelledby="h5"><h2 id="h5">W użyciu</h2>
    <div class="demo-row">
      <a class="btn btn-primary" href="komponenty.html#formularze"><span class="icon i-upload" aria-hidden="true"></span>Wgraj CV</a>
      <button class="btn btn-secondary" type="button" aria-pressed="false" data-label-on="Zapisano" data-label-off="Zapisz"><span class="icon i-heart-outline" aria-hidden="true"></span>Zapisz</button>
      <a class="btn btn-secondary btn-compact" href="komponenty.html#listy"><span class="icon i-filter" aria-hidden="true"></span>Filtry</a>
      <span class="badge"><span class="icon icon-sm i-pin" aria-hidden="true"></span>&nbsp;Kraków</span>
      <span class="amount" style="margin:0"><span class="sprite s-coin" aria-hidden="true"></span> 22 000–28 000 <small>zł</small></span>
      <span class="tier-tag tier-epic"><span class="sprite sprite-sm s-gem" aria-hidden="true"></span>&nbsp;Epicki</span>
    </div>
    <div class="grid-panels" style="margin-top:24px">
      <section class="panel"><div class="panel-head"><h2><span class="sprite s-calendar" aria-hidden="true"></span> Wydarzenia</h2><span class="count">12</span></div></section>
      <section class="panel"><div class="panel-head"><h2><span class="sprite s-mail" aria-hidden="true"></span> Wiadomości</h2><span class="count">3</span></div></section>
      <section class="panel"><div class="panel-head"><h2><span class="sprite s-pin" aria-hidden="true"></span> W pobliżu</h2><span class="count">48</span></div></section>
      <section class="panel"><div class="panel-head"><h2><span class="sprite s-hourglass" aria-hidden="true"></span> Wygasające</h2><span class="count">5</span></div></section>
    </div></section>
</main>
<script src="../assets/list-controls.js"></script>
<script>
document.querySelectorAll('[data-theme-set]').forEach(function (b, _, all) {{ b.addEventListener('click', function () {{ document.documentElement.setAttribute('data-theme', b.dataset.themeSet); all.forEach(function (x) {{ x.setAttribute('aria-pressed', String(x === b)); }}); }}); }});
</script>
</body></html>
"""


def main():
    os.makedirs(os.path.join(ASSETS, 'icons'), exist_ok=True)
    assert set(ORDER) == set(MONO), set(ORDER) ^ set(MONO)
    css = ['/* Panel & Piksel — ikony pikselowe v1.1 (wygenerowane: scripts/build_icons.py — nie edytuj ręcznie)',
           ' * UI:        <span class="icon i-search" aria-hidden="true"></span>  — kolor = currentColor',
           ' * Kolorowe:  <span class="sprite s-search" aria-hidden="true"></span> — ta sama ikona w kolorze z cieniem 1 px',
           ' * Przedmiot: <span class="sprite s-coin" aria-hidden="true"></span>  — ręcznie rysowany przedmiot z gry',
           ' * Rozmiary tylko całkowite: .icon-sm 12 px, domyślnie 24 px, .icon-lg 36 px, .icon-xl 48 px (to samo dla .sprite). */',
           '.icon { display: inline-block; flex: none; width: 24px; height: 24px; vertical-align: middle; background-color: currentColor;',
           '  -webkit-mask: var(--i) center / 100% 100% no-repeat; mask: var(--i) center / 100% 100% no-repeat; forced-color-adjust: none; }',
           '.sprite { display: inline-block; flex: none; width: 24px; height: 24px; vertical-align: middle; background: var(--s) center / 100% 100% no-repeat; }',
           '.icon-sm, .sprite-sm { width: 12px; height: 12px; }',
           '.icon-lg, .sprite-lg { width: 36px; height: 36px; }',
           '.icon-xl, .sprite-xl { width: 48px; height: 48px; }']
    for name, art in MONO.items():
        svg = svg_mono(art)
        open(os.path.join(ASSETS, 'icons', f'i-{name}.svg'), 'w').write(svg)
        css.append(f'.i-{name} {{ --i: {data_uri(svg)}; }}')
    dark_rules = []
    tinted = [n for n in ORDER if n not in ITEMS]
    missing = [n for n in tinted if n not in TINT]
    assert not missing, missing
    for name in tinted:
        (light, dark) = TINT[name]
        svg, svgd = svg_tinted(MONO[name], light, SHADOW), svg_tinted(MONO[name], dark, SHADOW_DARK)
        open(os.path.join(ASSETS, 'icons', f's-{name}.svg'), 'w').write(svg)
        css.append(f'.s-{name} {{ --s: {data_uri(svg)}; }}')
        dark_rules.append(f'.s-{name} {{ --s: {data_uri(svgd)}; }}')
    for name, art in ITEMS.items():
        svg, svgd = svg_item(art), svg_item(art, dark=True)
        open(os.path.join(ASSETS, 'icons', f's-{name}.svg'), 'w').write(svg)
        css.append(f'.s-{name} {{ --s: {data_uri(svg)}; }}')
        dark_rules.append(f'.s-{name} {{ --s: {data_uri(svgd)}; }}')
    css.append('/* tryb ciemny: jaśniejsze kolory ikon i jasny obrys przedmiotów */')
    css.append('[data-theme="dark"] ' + '\n[data-theme="dark"] '.join(dark_rules))
    css.append('@media (prefers-color-scheme: dark) {\n  [data-theme="auto"] ' + '\n  [data-theme="auto"] '.join(dark_rules) + '\n}')
    css.append('@media (forced-colors: active) { .sprite { forced-color-adjust: none; } }')
    open(os.path.join(ASSETS, 'icons.css'), 'w').write('\n'.join(css) + '\n')
    open(os.path.join(HERE, '..', 'examples', 'ikony.html'), 'w').write(gallery(tinted))
    print(f'{len(MONO)} ikon UI, {len(tinted)} kolorowych wersji, {len(ITEMS)} przedmiotów → assets/icons.css, assets/icons/, examples/ikony.html')

if __name__ == '__main__':
    main()
