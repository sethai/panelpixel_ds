#!/usr/bin/env python3
"""Buduje statyczną stronę dokumentacji Panel & Piksel → site/ (gotowe do Cloudflare Pages).

Uruchom z katalogu projektu:  python3 tools/build_site.py
Źródła (nic nie jest przepisywane ręcznie):
  design.md                                  — fundamenty, zasady, specyfikacje §6, zarządzanie, historia
  tools/docgen.py + tools/doc_cards.py       — karty komponentów (anatomia, warianty, tokeny, dostępność…)
  skills/panel-piksel-ui/assets/             — CSS, JS, ikony, rejestr komponentów (strona używa systemu, który opisuje)
  skills/panel-piksel-ui/examples/*.html     — przykłady na żywo (sekcje wycinane do stron komponentów)
  docs/evidence/*.png                        — zrzuty z ekranów
Wynik jest czystym HTML/CSS/JS bez budowania po stronie Cloudflare (Build command: brak, Output: site).
"""
import html
import json
import os
import re
import runpy
import shutil
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SK = os.path.join(ROOT, 'skills', 'panel-piksel-ui')
OUT = os.path.join(ROOT, 'site')
VERSION = open(os.path.join(SK, 'VERSION')).read().strip()
DESIGN = open(os.path.join(ROOT, 'design.md'), encoding='utf-8').read()
REG = json.load(open(os.path.join(SK, 'assets', 'components.json')))
ZIP_NAME = f'panel-piksel-{VERSION}.zip'

# ---------- dane kart z generatora dokumentacji ----------
os.environ['PP_NO_WRITE'] = '1'
_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
NS = runpy.run_path(os.path.join(ROOT, 'tools', 'docgen.py'))
sys.stdout = _stdout
CARDS = {c['id']: c for c in NS['CARDS']}
table, tag, st_badge = NS['table'], NS['tag'], NS['st']
STATUS_OF, REGMAP, SPL = NS['STATUS_OF'], NS['REG'], NS['SPL']
HEADS = {k: NS[k] for k in ['ANAT_HEAD', 'VAR_HEAD', 'PROP_HEAD', 'TOK_HEAD', 'DIM_HEAD', 'TYP_HEAD', 'DD_HEAD', 'A11Y_HEAD']}


# ---------- markdown → HTML (podzbiór używany w design.md) ----------
def inline(t):
    codes = []
    def keep(m):
        codes.append('<code>' + html.escape(m.group(1)) + '</code>')
        return f'\x00{len(codes) - 1}\x00'
    t = re.sub(r'`([^`]+)`', keep, t)
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" rel="noopener">\1</a>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', t)
    t = re.sub(r'(?<![\w#&])#([0-9A-Fa-f]{6})\b', lambda m: f'<span class="sw" style="--c:#{m.group(1)}"></span>#{m.group(1)}', t)
    return re.sub('\x00(\\d+)\x00', lambda m: swatch_code(codes[int(m.group(1))]), t)


def swatch_code(c):
    m = re.fullmatch(r'<code>#([0-9A-Fa-f]{6})</code>', c)
    return f'<span class="sw" style="--c:#{m.group(1)}"></span>{c}' if m else c


def md(text, shift=0):
    out, lines, i = [], text.split('\n'), 0
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    lines = text.split('\n')
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        if l.startswith('```'):
            lang = l[3:].strip(); j = i + 1; buf = []
            while j < len(lines) and not lines[j].startswith('```'):
                buf.append(lines[j]); j += 1
            out.append(f'<pre class="code" data-lang="{lang}"><code>{html.escape(chr(10).join(buf))}</code></pre>')
            i = j + 1; continue
        m = re.match(r'(#{1,6})\s+(.*)', l)
        if m:
            lvl = min(6, len(m.group(1)) + shift); txt = m.group(2)
            hid = slug(re.sub(r'`', '', txt))
            out.append(f'<h{lvl} id="{hid}">{inline(txt)}</h{lvl}>'); i += 1; continue
        if l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i]); i += 1
            cells = [split_row(r) for r in rows if not re.match(r'^\|[\s\-:|]+\|$', r)]
            h = '<div class="tw"><table class="table doc-table"><thead><tr>' + ''.join(f'<th scope="col">{inline(c)}</th>' for c in cells[0]) + '</tr></thead><tbody>'
            for r in cells[1:]:
                h += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
            out.append(h + '</tbody></table></div>'); continue
        if re.match(r'\s*([-*]|\d+\.)\s', l):
            items, ordered = [], bool(re.match(r'\s*\d+\.', l))
            while i < len(lines) and (re.match(r'\s*([-*]|\d+\.)\s', lines[i]) or (lines[i].startswith('  ') and lines[i].strip())):
                if re.match(r'\s*([-*]|\d+\.)\s', lines[i]):
                    indent = len(lines[i]) - len(lines[i].lstrip())
                    items.append([indent, re.sub(r'^\s*([-*]|\d+\.)\s+', '', lines[i])])
                else:
                    items[-1][1] += ' ' + lines[i].strip()
                i += 1
            out.append(render_list(items, ordered)); continue
        if l.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].startswith('>'):
                buf.append(lines[i][1:].strip()); i += 1
            out.append('<blockquote class="callout">' + inline(' '.join(buf)) + '</blockquote>'); continue
        if l.strip() == '---':
            i += 1; continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'(#{1,6}\s|\||```|\s*([-*]|\d+\.)\s|>)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>')
    return '\n'.join(out)


def render_list(items, ordered):
    tagn = 'ol' if ordered else 'ul'
    h, depth = f'<{tagn}>', 0
    base = items[0][0]
    for ind, txt in items:
        d = 1 if ind > base else 0
        if d > depth: h += '<ul>'
        elif d < depth: h += '</ul>'
        depth = d
        txt = re.sub(r'^\[ \]\s*', '<span class="todo" aria-hidden="true"></span>', txt)
        h += '<li>' + inline(txt) + '</li>'
    if depth: h += '</ul>'
    return h + f'</{tagn}>'


def split_row(r):
    r = r.strip().strip('|')
    parts, buf, code = [], '', False
    for ch in r:
        if ch == '`': code = not code
        if ch == '|' and not code:
            parts.append(buf.strip()); buf = ''
        else:
            buf += ch
    parts.append(buf.strip())
    return parts


def slug(t):
    t = t.lower()
    for a, b in zip('ąćęłńóśźż', 'acelnoszz'):
        t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60]


def section(title_prefix, level='##', until_same=True):
    """Wycina sekcję design.md od nagłówka zaczynającego się od title_prefix do następnego nagłówka tego samego lub wyższego poziomu."""
    pat = re.compile(r'^' + re.escape(level) + r' ' + re.escape(title_prefix) + r'.*$', re.M)
    m = pat.search(DESIGN)
    if not m:
        raise KeyError(title_prefix)
    n = len(level)
    rest = DESIGN[m.end():]
    stop = re.search(r'^#{1,%d} ' % n, rest, re.M)
    body = rest[:stop.start()] if stop else rest
    return m.group(0).lstrip('#').strip(), body


# ---------- przykłady na żywo (wycinane z examples/*.html) ----------
EX = {n: open(os.path.join(SK, 'examples', n + '.html'), encoding='utf-8').read() for n in ('komponenty', 'wzorce', 'ikony')}


def grab(page, start_pat):
    src = EX[page]
    m = re.search(start_pat, src)
    if not m:
        raise KeyError(start_pat)
    i = m.start()
    tagname = re.match(r'<(\w+)', src[i:]).group(1)
    depth, j = 0, i
    for t in re.finditer(r'<(/?)' + tagname + r'\b[^>]*>', src[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            j = i + t.end(); break
    return src[i:j]


def demo_lists(h):
    # lista „Pokaż więcej” w wzorcach jest wypełniana skryptem strony — na stronie dokumentacji wstawiamy ją statycznie
    jobs = ['Senior Unity Developer', 'Game Designer', 'Pixel Artist', 'QA Tester', 'Lead Backend (Go)', 'Technical Artist', 'Level Designer', 'Community Manager', 'Producent gier', 'Sound Designer', 'UX Researcher', 'Animator 2D']
    firms = ['Smocza Jama', 'Kosmiczny Kret', '8bit Atelier', 'Pikselowo']
    cards = ''.join(f'<article class="card" data-item data-sort-name="{j.lower()}"><div><h3>{j}</h3><p>{firms[k % 4]} · dodano {k + 1} godz. temu</p></div></article>' for k, j in enumerate(jobs))
    return h.replace('<div class="mini-cards" data-list="nowe" data-page-size="4"></div>', f'<div class="mini-cards" data-list="nowe" data-page-size="4">{cards}</div>')


DIALOGS = grab('komponenty', r'<dialog class="modal" id="okno-aplikuj"') + '\n' + grab('komponenty', r'<dialog class="drawer" id="filtry-szuflada"')
LIVE = {
    'K01': ('komponenty', r'<section class="ex" id="przyciski"'),
    'K02': ('komponenty', r'<section class="ex" aria-labelledby="h-lab"'),
    'K06': ('komponenty', r'<section class="ex" id="listy"'),
    'K08': ('komponenty', r'<section class="ex" id="stany"'),
    'K10': ('komponenty', r'<section class="ex" id="tabele"'),
    'K13': ('komponenty', r'<section class="ex" aria-labelledby="h-rank"'),
    'K21': ('ikony', r'<section class="ex" aria-labelledby="h5"'),
    'K22': ('komponenty', r'<section class="ex" id="powiadomienia"'),
    'K23': ('komponenty', r'<section class="ex" id="formularze"'),
    'K24': ('wzorce', r'<section class="ex" id="formularz"'),
    'K25': ('komponenty', r'<section class="ex" id="nakladki"'),
    'K27': ('wzorce', r'<section class="ex" id="zaznaczanie"'),
    'K28': ('wzorce', r'<section class="ex" id="ladowanie"'),
    'K29': ('wzorce', r'<section class="ex" id="wykresy"'),
}
LIVE_ALIAS = {'K03': 'K02', 'K04': 'K02', 'K05': 'K02', 'K07': 'K06', 'K20': 'K06', 'K11': 'K10', 'K12': 'K10', 'K14': 'K13', 'K18': 'K13', 'K16': 'K08', 'K17': 'K10', 'K26': 'K06'}

# ---------- mapa stron ----------
COMPONENTS = ['K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K07', 'K08', 'K23', 'K09', 'K10', 'K11', 'K12', 'K13', 'K14', 'K15', 'K16', 'K17', 'K18', 'K19', 'K21', 'K22', 'K25', 'K29']
PATTERNS = ['K20', 'K24', 'K26', 'K27', 'K28']
SPEC = {'K01': '6.1', 'K02': '6.2', 'K03': '6.3', 'K04': '6.4', 'K06': '6.5', 'K07': '6.6', 'K08': '6.7', 'K13': '6.8', 'K14': '6.9', 'K16': '6.10', 'K17': '6.10', 'K15': '6.11',
        'K09': '6.11', 'K10': '6.11', 'K11': '6.11', 'K12': '6.11', 'K18': '6.11', 'K20': '6.12', 'K22': '6.15', 'K23': '6.14', 'K24': '6.18', 'K25': '6.16', 'K26': '6.17', 'K27': '6.19', 'K28': '6.20', 'K29': '6.21'}
SLUG = {cid: slug(CARDS[cid]['name'].split(' — ')[0].split(':')[0]) for cid in CARDS}
SLUG.update({'K24': 'formularz', 'K25': 'nakladki', 'K26': 'nawigacja-mobilna', 'K27': 'zaznaczanie-wierszy', 'K28': 'ladowanie-i-postep', 'K20': 'sterowanie-lista', 'K15': 'struktura-strony', 'K29': 'wykresy', 'K23': 'pola-formularza', 'K22': 'powiadomienia', 'K21': 'ikony'})

FOUNDATIONS = [
    ('esencja', 'Esencja i zasady', [('## 1. Esencja', '##')]),
    ('kolor', 'Kolor', [('## 2. Kolor', '##')]),
    ('typografia', 'Typografia', [('## 3. Typografia', '##')]),
    ('przestrzen', 'Przestrzeń, kształt, głębia, ruch', [('## 4. Przestrzeń', '##')]),
    ('ikony', 'Ikony i grafika', [('## 5. Grafika', '##')]),
    ('motywy', 'Motywy: ciemny i wysoki kontrast', [('### 2.6 Tryb ciemny', '###')]),
    ('tresci', 'Treści i język', [('## 6A. Treści', '##')]),
    ('dostepnosc', 'Dostępność', [('## 8. Dostępność', '##')]),
]
RESOURCES = [
    ('zarzadzanie', 'Zarządzanie i statusy', [('## 0. Zarządzanie', '##')]),
    ('macierz-stanow', 'Macierz stanów', [('### 6.22 Macierz stanów', '###')]),
    ('czego-nie-robic', 'Czego nie robić', [('## 10. Czego nie robić', '##')]),
    ('historia-zmian', 'Historia zmian', [('## 12. Historia zmian', '##')]),
]

# ---------- szkielet strony ----------
SITE_CSS = '''
:root { --side: 264px; --top: 56px; }
body { min-height: 100vh; }
.skip { position: absolute; left: 8px; top: -60px; z-index: 1000; padding: 8px 12px; background: var(--surface); border: var(--border); }
.skip:focus { top: 8px; }
.topbar { position: sticky; top: 0; z-index: var(--z-drawer); display: flex; align-items: center; gap: 16px; height: var(--top); padding: 0 16px; color: var(--on-ink); background: var(--ink); border-bottom: 2px solid var(--ink); }
.topbar .logo { color: var(--on-ink); font-size: 13px; }
.topbar .logo span { color: var(--mint); }
[data-theme="dark"] .topbar .logo span { color: var(--action); }
.side-theme { display: none !important; margin: 20px 16px 0; }
.topbar .ver { font: 9px/1 var(--font-pixel); padding: 5px 6px; color: var(--ink); background: var(--highlight); }
.topbar nav { display: flex; gap: 4px; margin-left: auto; }
.topbar nav a, .topbar .tb-btn { display: inline-flex; align-items: center; gap: 6px; height: 36px; padding: 0 10px; color: var(--on-ink); font: 700 14px var(--font-sans); text-decoration: none; background: none; border: 2px solid transparent; cursor: pointer; }
.topbar nav a:hover, .topbar .tb-btn:hover, .topbar nav a[aria-current="page"] { border-color: var(--on-ink); }
.topbar a:focus-visible, .topbar button:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.topbar .side-toggle { display: none; }
.shell { display: grid; grid-template-columns: var(--side) minmax(0, 1fr); }
.sidenav { position: sticky; top: var(--top); height: calc(100vh - var(--top)); overflow-y: auto; padding: 16px 0 40px; background: var(--surface); border-right: var(--border); box-sizing: border-box; }
.sidenav h2 { margin: 18px 16px 6px; font: 9px/1.4 var(--font-pixel); letter-spacing: .5px; color: var(--ink-3); text-transform: uppercase; }
.sidenav ul { margin: 0; padding: 0; list-style: none; }
.sidenav a { display: flex; align-items: center; justify-content: space-between; gap: 8px; min-height: 32px; padding: 4px 16px; font: 600 14px/20px var(--font-sans); color: var(--ink); text-decoration: none; border-left: 4px solid transparent; }
.sidenav a:hover { background: var(--paper); }
.sidenav a[aria-current="page"] { background: var(--paper); border-left-color: var(--action); font-weight: 800; }
.sidenav a:focus-visible { outline: 3px solid var(--focus); outline-offset: -3px; }
.sidenav .dot { flex: none; width: 8px; height: 8px; }
.dot-stable { background: var(--status-success); } .dot-preview { background: var(--status-info); } .dot-deprecated { background: var(--ink-3); }
.content { min-width: 0; padding: 32px clamp(16px, 4vw, 56px) 80px; }
.content > .inner { max-width: 1040px; }
.crumbs { margin: 0 0 8px; font-size: 13px; color: var(--ink-3); }
.crumbs a { color: var(--link); }
.page-title { margin: 0 0 8px; font: 900 clamp(28px, 4vw, 40px)/1.1 var(--font-sans); letter-spacing: -1px; }
.page-lead { max-width: 72ch; margin: 0 0 20px; font-size: 17px; line-height: 26px; color: var(--ink-2); }
.statusline { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 0 0 24px; font-size: 13px; color: var(--ink-3); }
.sbadge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 8px; font: 700 11px/1 var(--font-sans); letter-spacing: .3px; text-transform: uppercase; border: var(--border); background: var(--surface); color: var(--ink); }
.sbadge::before { content: ""; width: 8px; height: 8px; background: var(--c); }
.prose-doc { max-width: 80ch; }
.prose-doc h2, .doc h2 { margin: 40px 0 12px; font: 900 24px/32px var(--font-sans); letter-spacing: -.6px; }
.prose-doc h3, .doc h3 { margin: 28px 0 8px; font: 900 18px/26px var(--font-sans); }
.prose-doc h4, .doc h4 { margin: 20px 0 6px; font: 800 15px var(--font-sans); }
.prose-doc p, .prose-doc li, .doc p, .doc li { color: var(--ink-2); line-height: 26px; }
.prose-doc code, .doc code { font: 13px/1.5 ui-monospace, Menlo, monospace; padding: 1px 4px; background: var(--paper); border: 1px solid var(--line-soft); word-break: break-word; }
.doc-wide { max-width: none; }
.tw { overflow-x: auto; margin: 12px 0 20px; border: var(--border); background: var(--surface); box-shadow: var(--shadow-sm); }
.tw .table th { position: static; }
.doc-table td, .doc-table th { height: auto; padding: 8px 12px; vertical-align: top; font-size: 14px; line-height: 20px; }
.doc-table .num { font-family: var(--font-sans); }
pre.code { position: relative; margin: 12px 0 20px; padding: 16px; overflow-x: auto; font: 13px/1.6 ui-monospace, Menlo, monospace; color: var(--on-ink); background: var(--ink); border: var(--border); box-shadow: var(--shadow-sm); }
pre.code code { background: none; border: 0; padding: 0; color: inherit; word-break: normal; white-space: pre; }
.copy { position: absolute; right: 8px; top: 8px; height: 28px; padding: 0 8px; font: 700 12px var(--font-sans); color: var(--ink); background: var(--surface); border: 2px solid var(--surface); cursor: pointer; }
.copy:focus-visible { outline: 3px solid var(--focus); }
.sw { display: inline-block; width: 12px; height: 12px; margin-right: 4px; vertical-align: -1px; background: var(--c); border: 1px solid rgba(0, 2, 28, .35); }
.todo { display: inline-block; width: 12px; height: 12px; margin-right: 6px; vertical-align: -1px; border: 2px solid var(--ink-3); }
.doc-tabs { margin: 8px 0 24px; }
[role="tabpanel"][hidden] { display: none; }
.live { margin: 16px 0; padding: 20px; background: var(--paper); border: 2px dashed var(--line-soft); }
.live > .ex { margin: 0; padding: 0; border: 0; }
.live > .ex > h2 { margin-top: 0; }
.figs { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 360px), 1fr)); gap: 16px; margin: 16px 0; }
.figs .ev { margin: 0; background: var(--surface); border: var(--border); }
.figs .ev img { display: block; width: 100%; height: auto; }
.figs .ev figcaption { padding: 8px 10px; font-size: 13px; color: var(--ink-2); border-top: 2px solid var(--paper); }
.figs .ev .meta { display: block; font-size: 11.5px; color: var(--ink-3); word-break: break-word; }
.st { display: inline-block; padding: 1px 5px; font: 700 10px/1.4 ui-monospace, Menlo, monospace; color: #fff; white-space: nowrap; vertical-align: 1px; }
.st-d { background: #166534; } .st-s { background: #a16207; } .st-r { background: #7e22ce; } .st-p { background: #b91c1c; } .st-t { background: #1e40af; }
.tiles { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 240px), 1fr)); gap: 16px; margin: 16px 0 32px; padding: 0; list-style: none; }
.tile { display: grid; align-content: start; gap: 8px; height: 100%; padding: 16px; box-sizing: border-box; color: var(--ink); text-decoration: none; background: var(--surface); border: var(--border); box-shadow: var(--shadow-md); transition: transform var(--motion-fast), box-shadow var(--motion-fast); }
.tile:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 var(--shadow-color); }
.tile:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
.tile b { font: 900 17px/22px var(--font-sans); }
.tile span.desc { font-size: 14px; line-height: 20px; color: var(--ink-2); }
.hero { position: relative; margin: -32px calc(-1 * clamp(16px, 4vw, 56px)) 32px; padding: 56px clamp(16px, 4vw, 56px) 48px; background: var(--paper); border-bottom: var(--border); }
.hero h1 { margin: 0 0 12px; font: 900 clamp(32px, 6vw, 64px)/1.02 var(--font-sans); letter-spacing: -2px; }
.hero p { max-width: 64ch; font-size: 18px; line-height: 28px; color: var(--ink-2); }
.hero .row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 170px), 1fr)); gap: 16px; margin: 0 0 32px; }
.kpi { padding: 14px 16px; background: var(--surface); border: var(--border); box-shadow: var(--shadow-sm); }
.kpi b { display: block; font: 20px/1.4 var(--font-pixel); }
.kpi span { font-size: 13px; color: var(--ink-2); }
.filter-row { display: flex; flex-wrap: wrap; gap: 12px; align-items: end; margin: 0 0 16px; }
.filter-row .field { flex: 1 1 260px; max-width: 420px; }
.foot { margin-top: 64px; padding-top: 16px; border-top: var(--border); font-size: 13px; color: var(--ink-3); }
.foot a { color: var(--link); }
@media (max-width: 900px) {
  .shell { grid-template-columns: 1fr; }
  .topbar .side-toggle { display: inline-flex; }
  .topbar nav { display: none; }
  .topbar .theme-top { display: none; }
  .side-theme { display: flex !important; }
  .sidenav { position: fixed; z-index: var(--z-drawer); left: 0; top: var(--top); width: min(320px, 88vw); transform: translateX(-102%); transition: transform var(--motion-slow) var(--ease-steps); box-shadow: 6px 0 0 var(--shadow-color); }
  .sidenav.is-open { transform: none; }
}
@media print { .topbar, .sidenav { display: none; } .shell { display: block; } }
'''

SITE_JS = r'''
(function () {
  'use strict';
  // motyw: jasny / ciemny / systemowy — zapamiętany w przeglądarce
  var root = document.documentElement, KEY = 'pp-docs-theme';
  function setTheme(t) { root.setAttribute('data-theme', t); try { localStorage.setItem(KEY, t); } catch (e) {}
    document.querySelectorAll('[data-theme-set]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-theme-set') === t)); }); }
  try { var s = localStorage.getItem(KEY); if (s) setTheme(s); } catch (e) {}
  document.querySelectorAll('[data-theme-set]').forEach(function (b) { b.addEventListener('click', function () { setTheme(b.getAttribute('data-theme-set')); }); });
  // nawigacja boczna na telefonie
  var tog = document.querySelector('.side-toggle'), side = document.getElementById('sidenav');
  if (tog && side) {
    tog.addEventListener('click', function () { var o = !side.classList.contains('is-open'); side.classList.toggle('is-open', o); tog.setAttribute('aria-expanded', String(o)); if (o) { var a = side.querySelector('[aria-current="page"]') || side.querySelector('a'); a && a.focus(); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && side.classList.contains('is-open')) { side.classList.remove('is-open'); tog.setAttribute('aria-expanded', 'false'); tog.focus(); } });
  }
  var cur = side && side.querySelector('[aria-current="page"]'); if (cur) side.scrollTop = Math.max(0, cur.offsetTop - side.clientHeight / 2);
  // zakładki stron komponentów (APG Tabs)
  document.querySelectorAll('.doc-tabs').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role=tab]'));
    function sel(t, focus) { tabs.forEach(function (x) { var on = x === t; x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
      if (focus) t.focus(); if (history.replaceState) history.replaceState(null, '', '#' + t.id.replace('tab-', '')); window.ppCharts && ppCharts.initAll(); }
    tabs.forEach(function (t, i) { t.addEventListener('click', function () { sel(t); });
      t.addEventListener('keydown', function (e) { var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (k) { e.preventDefault(); sel(tabs[(i + k + tabs.length) % tabs.length], true); } }); });
    var want = location.hash && document.getElementById('tab-' + location.hash.slice(1)); if (want && tabs.indexOf(want) > -1) sel(want);
  });
  // kopiuj kod
  document.querySelectorAll('pre.code').forEach(function (pre) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'copy'; b.textContent = 'Kopiuj';
    b.addEventListener('click', function () { var t = pre.querySelector('code').textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { b.textContent = 'Skopiowano'; }, function () { b.textContent = 'Zaznacz i skopiuj'; });
      setTimeout(function () { b.textContent = 'Kopiuj'; }, 1800); });
    pre.appendChild(b);
  });
  // filtr listy komponentów
  var q = document.getElementById('comp-filter');
  if (q) q.addEventListener('input', function () { var v = q.value.trim().toLowerCase(), n = 0;
    document.querySelectorAll('[data-comp]').forEach(function (li) { var ok = !v || li.getAttribute('data-comp').indexOf(v) > -1; li.hidden = !ok; if (ok) n++; });
    document.getElementById('comp-count').textContent = n; });
  // zachowania z przykładów (demo): ładowanie, powiadomienia, akcje zbiorcze, postęp, zakładki statusów, formularze
  document.querySelectorAll('[data-demo-load]').forEach(function (b) { b.addEventListener('click', function () { if (b.classList.contains('is-loading')) return;
    b.classList.add('is-loading'); b.setAttribute('aria-disabled', 'true'); b.setAttribute('aria-busy', 'true');
    setTimeout(function () { b.classList.remove('is-loading'); b.removeAttribute('aria-disabled'); b.removeAttribute('aria-busy'); }, 2000); }); });
  var TOASTS = { success: { title: 'Zapisano ofertę', text: 'Znajdziesz ją w zakładce „Zapisane”.' }, info: { title: 'Nowe oferty w Twojej kategorii', text: '4 oferty od wczoraj.' }, error: { title: 'Nie udało się wysłać CV', text: 'Plik jest uszkodzony — wgraj go ponownie.' } };
  document.querySelectorAll('[data-toast]').forEach(function (b) { b.addEventListener('click', function () { var k = b.getAttribute('data-toast'); window.ppToast && ppToast({ status: k, title: TOASTS[k].title, text: TOASTS[k].text }); }); });
  var t = document.getElementById('t-oferty');
  document.querySelectorAll('[data-bulk]').forEach(function (b) { b.addEventListener('click', function () { var n = t && t.ppSelected ? t.ppSelected().length : 0;
    window.ppToast && ppToast(b.getAttribute('data-bulk') === 'delete' ? { status: 'warning', title: 'Usunąć ' + n + ' ' + (n === 1 ? 'ofertę' : n < 5 ? 'oferty' : 'ofert') + '?', text: 'W produkcie tu pojawia się okno potwierdzenia.' } : { status: 'success', title: 'Przedłużono o 30 dni', text: 'Liczba ofert: ' + n + '.' }); }); });
  var pr = document.getElementById('up-progress'), ups = document.getElementById('up-start');
  if (pr && ups) ups.addEventListener('click', function () { var v = 5; ppProgress(pr, v); var tm = setInterval(function () { v += 12.5; ppProgress(pr, Math.min(100, v)); if (v >= 100) { clearInterval(tm); ppToast({ status: 'success', title: 'CV wysłane' }); } }, 250); });
  var stt = document.getElementById('save-state'); if (stt) setTimeout(function () { stt.classList.add('is-done'); stt.textContent = 'Zapisano'; }, 2500);
  var stabs = Array.prototype.slice.call(document.querySelectorAll('#status-tabs [role=tab]'));
  stabs.forEach(function (x, i) { function s(t) { stabs.forEach(function (y) { var on = y === t; y.setAttribute('aria-selected', String(on)); y.tabIndex = on ? 0 : -1; document.getElementById(y.getAttribute('aria-controls')).hidden = !on; }); }
    x.addEventListener('click', function () { s(x); }); x.addEventListener('keydown', function (e) { var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (k) { var n = stabs[(i + k + stabs.length) % stabs.length]; n.focus(); s(n); } }); });
  var af = document.getElementById('apply-form'); if (af) af.addEventListener('pp:valid', function () { document.getElementById('okno-aplikuj').close(); ppToast({ status: 'success', title: 'Aplikacja wysłana', text: 'Smocza Jama Studio dostała Twoje zgłoszenie.' }); });
  var wz = document.querySelector('[data-wizard]'); if (wz) wz.addEventListener('pp:valid', function () { ppToast({ status: 'success', title: 'Oferta opublikowana', text: 'Pojawi się w wynikach po weryfikacji (do 2 godzin).' }); });
})();
'''


def status_badges(cid):
    out = []
    colors = {'stable': 'var(--status-success)', 'preview': 'var(--status-info)', 'draft': 'var(--status-warning)', 'deprecated': 'var(--ink-3)'}
    for rid in STATUS_OF.get(cid, []):
        r = REGMAP[rid]
        lab = SPL[r['status']][0]
        extra = ''
        if r['status'] == 'preview' and r.get('missing'):
            extra = ' — brakuje: ' + ', '.join(r['missing'])
        if r['status'] == 'deprecated':
            extra = f" — zastąpione: {html.escape(r['replacedBy'])}, usunięcie w {r['removeIn']}"
        out.append(f'<span class="sbadge" style="--c:{colors[r["status"]]}">{lab}</span> <span>{html.escape(r["name"])} · od {r.get("since", "—")}{extra}</span>')
    return '<p class="statusline">' + '<br>'.join(out) + '</p>' if out else ''


def main_status(cid):
    ids = STATUS_OF.get(cid, [])
    return REGMAP[ids[0]]['status'] if ids else 'stable'


def nav_html(cur, depth):
    pre = '../' * depth
    def link(href, label, dot=None):
        cs = ' aria-current="page"' if href == cur else ''
        d = f'<span class="dot dot-{dot}" aria-hidden="true"></span>' if dot else ''
        return f'<li><a href="{pre}{href}"{cs}><span>{label}</span>{d}</a></li>'
    h = '<nav class="sidenav" id="sidenav" aria-label="Dokumentacja">'
    h += '<h2>Start</h2><ul>' + link('index.html', 'Strona główna') + link('pierwsze-kroki.html', 'Pierwsze kroki') + link('pobierz.html', 'Pobierz') + '</ul>'
    h += '<h2>Fundamenty</h2><ul>' + ''.join(link(f'fundamenty/{s}.html', t) for s, t, _ in FOUNDATIONS) + '</ul>'
    h += '<h2>Komponenty</h2><ul>' + link('komponenty/index.html', 'Przegląd') + ''.join(link(f'komponenty/{SLUG[c]}.html', short(c), main_status(c)) for c in COMPONENTS) + '</ul>'
    h += '<h2>Wzorce</h2><ul>' + ''.join(link(f'wzorce/{SLUG[c]}.html', short(c), main_status(c)) for c in PATTERNS) + link('wzorce/koszyk.html', 'Koszyk sklepu') + link('wzorce/saldo.html', 'Saldo w nagłówku') + link('wzorce/przepisy-ekranow.html', 'Przepisy ekranów') + '</ul>'
    h += '<h2>Zasoby</h2><ul>' + ''.join(link(f'zasoby/{s}.html', t) for s, t, _ in RESOURCES) + link('przyklady/komponenty.html', 'Przykłady: komponenty') + link('przyklady/wzorce.html', 'Przykłady: wzorce') + link('archiwum/decyzje-v1-1.html', 'Archiwum: decyzje v1.1') + link('archiwum/kwestie-otwarte.html', 'Archiwum: kwestie otwarte') + link('archiwum/kandydaci.html', 'Archiwum: kandydaci 1.11') + '</ul>'
    h += '<div class="tabs side-theme" role="group" aria-label="Motyw"><button type="button" aria-pressed="true" data-theme-set="light">Jasny</button><button type="button" aria-pressed="false" data-theme-set="dark">Ciemny</button></div>'
    return h + '</nav>'


def short(cid):
    n = CARDS[cid]['name']
    return {'K23': 'Pola formularza', 'K24': 'Formularz', 'K25': 'Nakładki', 'K26': 'Nawigacja mobilna', 'K27': 'Zaznaczanie wierszy', 'K28': 'Ładowanie i postęp', 'K29': 'Wykresy',
            'K20': 'Sterowanie listą', 'K15': 'Struktura strony', 'K14': 'Pakiet i znacznik', 'K08': 'Panel filtrów', 'K22': 'Powiadomienia', 'K21': 'Ikony', 'K05': 'Awatar'}.get(cid, n)


def page(path, title, body, cur, desc='', wide=False):
    depth = path.count('/')
    pre = '../' * depth
    a = pre + 'assets/panel-piksel/'
    doc = f'''<!doctype html>
<html lang="pl" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Panel &amp; Piksel</title>
<meta name="description" content="{html.escape(desc or 'Panel & Piksel — retro-pikselowy design system dla katalogów, list, tabel, rankingów i sklepów.')}">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400&family=Press+Start+2P&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a}tokens.css">
<link rel="stylesheet" href="{a}components.css">
<link rel="stylesheet" href="{a}icons.css">
<link rel="stylesheet" href="{pre}site.css">
</head>
<body class="bg-dots">
<a class="skip" href="#tresc">Przejdź do treści</a>
<header class="topbar">
  <button class="tb-btn side-toggle" type="button" aria-expanded="false" aria-controls="sidenav" aria-label="Nawigacja"><span class="icon i-menu" aria-hidden="true"></span></button>
  <a class="logo" href="{pre}index.html">PANEL<span>&amp;PIKSEL</span></a><span class="ver">{VERSION}</span>
  <nav aria-label="Główna">
    <a href="{pre}pierwsze-kroki.html"{' aria-current="page"' if cur == 'pierwsze-kroki.html' else ''}>Pierwsze kroki</a>
    <a href="{pre}komponenty/index.html"{' aria-current="page"' if cur.startswith('komponenty/') else ''}>Komponenty</a>
    <a href="{pre}pobierz.html"{' aria-current="page"' if cur == 'pobierz.html' else ''}><span class="icon icon-sm i-download" aria-hidden="true"></span>Pobierz</a>
  </nav>
  <div class="tabs theme-top" role="group" aria-label="Motyw" style="margin-left:8px;box-shadow:none;border-color:var(--on-ink)">
    <button type="button" aria-pressed="true" data-theme-set="light">Jasny</button><button type="button" aria-pressed="false" data-theme-set="dark">Ciemny</button>
  </div>
</header>
<div class="shell">
{nav_html(cur, depth)}
<main class="content" id="tresc"><div class="inner{' doc-wide' if wide else ''}">
{body}
<footer class="foot">Panel &amp; Piksel {VERSION} · właściciel: Konrad Kosiorek · źródło prawdy: <code>design.md</code> · strona wygenerowana z repozytorium (<code>tools/build_site.py</code>)</footer>
</div></main>
</div>
{dialogs_if(body)}
<script src="{a}list-controls.js"></script>
<script src="{a}table-sort.js"></script>
<script src="{a}ui-controls.js"></script>
<script src="{a}charts.js"></script>
<script src="{pre}site.js"></script>
</body>
</html>
'''
    if depth:
        doc = re.sub(r'href="(decyzje-v1-1|kwestie-otwarte|kandydaci)\.html', lambda m: f'href="{pre}archiwum/{m.group(1)}.html', doc)
        doc = re.sub(r'href="(komponenty|wzorce|ikony)\.html', lambda m: f'href="{pre}przyklady/{m.group(1)}.html', doc)
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(doc)


def dialogs_if(body):
    return DIALOGS if ('data-dialog-open' in body) else ''


def figures_local(fig_html, depth):
    pre = '../' * depth
    return re.sub(r'<figure class="ev" id="ev-([\w-]+)"><img src="data:image/png;base64,[^"]+"', lambda m: f'<figure class="ev" id="ev-{m.group(1)}"><img src="{pre}img/{m.group(1)}.png" loading="lazy"', fig_html)


def card_tabs(cid, depth):
    c = CARDS[cid]
    sec = lambda t, b: f'<h3>{t}</h3>{b}'
    purpose = tag(c['purpose'].replace('{D}', '[D]').replace('{R}', '[R]').replace('{S}', '[S]').replace('{P}', '[P]').replace('{T}', '[T]'))
    spec = ''
    if cid in SPEC:
        try:
            title, body = section(SPEC[cid], '###')
            spec = f'<h3>Specyfikacja (design.md §{SPEC[cid]})</h3><div class="prose-doc">' + md(body, shift=1) + '</div>'
        except KeyError:
            pass
    live_key = cid if cid in LIVE else LIVE_ALIAS.get(cid)
    live = ''
    if live_key:
        pg, pat = LIVE[live_key]
        snip = grab(pg, pat)
        if live_key == 'K28':
            snip = demo_lists(snip)
        code_snip = re.sub(r'\n\s*\n', '\n', snip)
        live = (f'<h3>Przykład na żywo</h3><p class="small" style="color:var(--ink-3)">Ta sama sekcja co w <code>examples/{pg}.html</code> — działa na systemie {VERSION}. Przełącz motyw w nagłówku, żeby zobaczyć tryb ciemny.</p>'
                f'<div class="live">{snip}</div><h3>Kod przykładu</h3><pre class="code" data-lang="html"><code>{html.escape(code_snip)}</code></pre>')
    usage = (f'<div class="doc"><p class="page-lead" style="font-size:16px">{purpose}</p>' + figures_local(c['figures'], depth)
             + sec('Anatomia i komponenty składowe', table(HEADS['ANAT_HEAD'], c['anatomy']))
             + sec('Warianty i zastosowanie', table(HEADS['VAR_HEAD'], c['variants']) + (('<h4>Zaobserwowane kombinacje</h4>' + c['combos']) if c['combos'] else ''))
             + sec('Zachowanie, treści i lokalizacja', '<p>' + tag(c['behavior']) + '</p>')
             + sec('Zalecane i niewskazane', table(HEADS['DD_HEAD'], c['dodont'])) + '</div>')
    style = ('<div class="doc">' + sec('Tokeny i style', table(HEADS['TOK_HEAD'], c['tokens'])) + sec('Wymiary, odległości i układ', table(HEADS['DIM_HEAD'], c['dims']))
             + sec('Typografia', table(HEADS['TYP_HEAD'], c['typo'])) + '</div>')
    code = ('<div class="doc">' + live + sec('Właściwości i atrybuty', table(HEADS['PROP_HEAD'], c['props'])) + spec + '</div>')
    a11y = ('<div class="doc"><p>Cel: WCAG 2.2 AA. Statyczne materiały i testy automatyczne w Chrome nie dowodzą zgodności — miejsca oznaczone „Do testu we wdrożeniu” wymagają testu z czytnikiem ekranu (design.md §0.6).</p>'
            + table(HEADS['A11Y_HEAD'], c['a11y']) + sec('Źródła', '<p class="small">' + c['sources'] + '</p>') + '</div>')
    tabs = [('uzycie', 'Użycie', usage), ('styl', 'Styl', style), ('kod', 'Kod', code), ('dostepnosc', 'Dostępność', a11y)]
    h = '<div class="tabs doc-tabs" role="tablist" aria-label="Sekcje strony">' + ''.join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else " tabindex=" + chr(34) + "-1" + chr(34)}>{lab}</button>' for i, (k, lab, _) in enumerate(tabs)) + '</div>'
    h += ''.join(f'<section role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>{body}</section>' for i, (k, _, body) in enumerate(tabs))
    return h


def component_page(cid, folder, crumb):
    c = CARDS[cid]
    body = (f'<p class="crumbs"><a href="index.html">{crumb}</a> / {html.escape(short(cid))}</p>' if folder == 'komponenty' else f'<p class="crumbs">Wzorce / {html.escape(short(cid))}</p>')
    body += f'<h1 class="page-title">{html.escape(c["name"])}</h1>' + status_badges(cid) + card_tabs(cid, 1)
    page(f'{folder}/{SLUG[cid]}.html', c['name'], body, f'{folder}/{SLUG[cid]}.html', desc=re.sub(r'<[^>]+>|\[[A-Z]\]|\{[A-Z]\}', '', c['purpose'])[:160])


def md_page(path, title, parts, lead='', extra=''):
    body = f'<h1 class="page-title">{html.escape(title)}</h1>' + (f'<p class="page-lead">{lead}</p>' if lead else '')
    for head, lvl in parts:
        t, b = section(head.lstrip('#').strip(), lvl)
        body += '<div class="prose-doc">' + md(b, shift=-1 if lvl == '##' else -2) + '</div>'
    body += extra
    page(path, title, body, path, wide=True)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # zasoby
    ad = os.path.join(OUT, 'assets', 'panel-piksel')
    shutil.copytree(os.path.join(SK, 'assets'), ad, ignore=shutil.ignore_patterns('starter.html'))
    shutil.copytree(os.path.join(ROOT, 'docs', 'evidence'), os.path.join(OUT, 'img'), ignore=shutil.ignore_patterns('*.json'))
    open(os.path.join(OUT, 'site.css'), 'w').write(SITE_CSS)
    open(os.path.join(OUT, 'site.js'), 'w').write(SITE_JS)
    shutil.copyfile(os.path.join(SK, 'assets', 'icons', 's-coin.svg'), os.path.join(OUT, 'favicon.svg'))
    dl = os.path.join(OUT, 'download'); os.makedirs(dl)
    shutil.copyfile(os.path.join(ROOT, 'design.md'), os.path.join(dl, 'design.md'))
    shutil.copyfile(os.path.join(SK, 'assets', 'tokens.json'), os.path.join(dl, 'tokens.json'))
    z = os.path.join(ROOT, 'dist', ZIP_NAME)
    if os.path.exists(z):
        shutil.copyfile(z, os.path.join(dl, ZIP_NAME))
    # strona główna
    counts = {}
    for r in REG['components']:
        counts[r['status']] = counts.get(r['status'], 0) + 1
    hist_t, hist_b = section('12. Historia zmian', '##')
    rows = [split_row(l) for l in hist_b.split('\n') if l.startswith('| 1.')][:4]
    news = ''.join(f'<li><b>{r[0]}</b> · {r[1]} — {inline(re.split(r"(?<=\.) ", r[2])[0])}</li>' for r in rows)
    tile = lambda href, t, d, ic: f'<li><a class="tile" href="{href}"><span class="sprite sprite-lg s-{ic}" aria-hidden="true"></span><b>{t}</b><span class="desc">{d}</span></a></li>'
    body = f'''<section class="hero"><h1>Panel &amp; <span class="mark">Piksel</span></h1>
<p>Retro-pikselowy design system dla katalogów, list ofert, tabel, rankingów i sklepów. Białe panele z czarną ramką 2 px i twardym cieniem, gęste listy, czytelne Archivo i piksel tam, gdzie się patrzy, a nie czyta: liczby, liczniki, ikony.</p>
<div class="row"><a class="btn btn-primary" href="pierwsze-kroki.html">Pierwsze kroki</a><a class="btn btn-secondary" href="pobierz.html"><span class="icon i-download" aria-hidden="true"></span>Pobierz {VERSION}</a></div></section>
<div class="kpis"><div class="kpi"><b>{len(CARDS)}</b><span>rodzin komponentów i wzorców</span></div><div class="kpi"><b>{counts.get('stable', 0)}</b><span>stabilnych · {counts.get('preview', 0)} testowych</span></div><div class="kpi"><b>86</b><span>ikon pikselowych (39 + 35 kolorowych + 12 przedmiotów)</span></div><div class="kpi"><b>2</b><span>motywy + tryb wysokiego kontrastu</span></div></div>
<h2 style="font:900 24px var(--font-sans)">Zacznij tutaj</h2>
<ul class="tiles">{tile('pierwsze-kroki.html', 'Pierwsze kroki', 'Jak podłączyć system w HTML, w projekcie i u agenta AI.', 'flag')}{tile('fundamenty/esencja.html', 'Fundamenty', 'Zasady, kolor, typografia, przestrzeń, ikony, motywy, treści, dostępność.', 'gem')}{tile('komponenty/index.html', 'Komponenty', 'Od przycisku po wykresy — z przykładami na żywo i kodem.', 'chest')}{tile('wzorce/formularz.html', 'Wzorce', 'Formularz w krokach, zaznaczanie wierszy, ładowanie, koszyk.', 'scroll')}{tile('zasoby/zarzadzanie.html', 'Zarządzanie', 'Statusy, wersje, wycofywanie, zgłaszanie zmian, testy.', 'shield')}{tile('pobierz.html', 'Pobierz', 'Paczka ZIP: CSS, JS, ikony, tokeny, design.md, skill dla agenta.', 'coin')}</ul>
<h2 style="font:900 24px var(--font-sans)">Co nowego</h2><ul class="list-square">{news}</ul>
<p><a href="zasoby/historia-zmian.html">Pełna historia zmian</a></p>'''
    page('index.html', 'Design system', body, 'index.html')
    # pierwsze kroki
    t, b = section('Start dla agenta budującego ekrany', '###')
    body = '<h1 class="page-title">Pierwsze kroki</h1><p class="page-lead">System to trzy rzeczy: zasady (<code>design.md</code>), kod (CSS + kilka małych skryptów bez zależności) i przykłady. Nie trzeba niczego budować — wystarczy podlinkować pliki.</p>'
    body += f'''<div class="prose-doc"><h2>Dla designerów</h2><ul><li>Przeczytaj <a href="fundamenty/esencja.html">esencję i 10 zasad</a> — to one decydują o wyglądzie: ramka 2 px, twarde cienie, jeden głośny element na ekran, piksel tylko dla liczb.</li><li>Komponenty mają zakładki <b>Użycie</b> (kiedy i jak), <b>Styl</b> (tokeny, wymiary, typografia), <b>Kod</b> (przykład na żywo) i <b>Dostępność</b>.</li><li>Tokeny do narzędzi projektowych: <a href="download/tokens.json">tokens.json</a> (format W3C Design Tokens; działa z Tokens Studio dla Figmy).</li></ul>
<h2>Dla programistów</h2><ol><li>Pobierz <a href="pobierz.html">paczkę {VERSION}</a> i skopiuj katalog <code>panel-piksel/</code> do projektu.</li><li>Podlinkuj fonty i style, a skrypty tylko wtedy, gdy ekran ich potrzebuje.</li><li>Zacznij od <code>starter.html</code> z paczki albo od przykładów w <code>examples/</code>.</li></ol></div>
<pre class="code" data-lang="html"><code>{html.escape(re.search(r"```html\n(.*?)```", b, re.S).group(1))}</code></pre>
<div class="prose-doc"><h2>Dla agentów AI (Claude Code)</h2><p>Paczka zawiera skill <code>panel-piksel-ui</code>: skopiuj go do <code>~/.claude/skills/</code>, a agent będzie składał ekrany z tych samych klocków i sprawdzał je skryptami (<code>check_screen.py</code>, <code>render_check.py</code>).</p></div>
<div class="prose-doc"><h2>Pliki i narzędzia</h2>{md(b, shift=-1)}</div>'''
    page('pierwsze-kroki.html', 'Pierwsze kroki', body, 'pierwsze-kroki.html')
    # pobierz
    zsize = os.path.getsize(z) / 1e6 if os.path.exists(z) else 0
    body = f'''<h1 class="page-title">Pobierz</h1><p class="page-lead">Wszystko, czego potrzeba, żeby używać systemu w innym projekcie albo podzielić się nim z zespołem.</p>
<ul class="tiles"><li><a class="tile" href="download/{ZIP_NAME}" download><span class="sprite sprite-lg s-chest" aria-hidden="true"></span><b>{ZIP_NAME}</b><span class="desc">Cały system: CSS, JS, ikony (SVG), tokeny, rejestr komponentów, przykłady, design.md, dokumentacja dla designerów i skill dla agenta. {zsize:.1f} MB.</span></a></li>
<li><a class="tile" href="download/design.md" download><span class="sprite sprite-lg s-scroll" aria-hidden="true"></span><b>design.md</b><span class="desc">Pełna specyfikacja w jednym pliku Markdown — źródło prawdy.</span></a></li>
<li><a class="tile" href="download/tokens.json" download><span class="sprite sprite-lg s-gem" aria-hidden="true"></span><b>tokens.json</b><span class="desc">Tokeny w formacie W3C Design Tokens, z wartościami trybu ciemnego.</span></a></li></ul>
<div class="prose-doc"><h2>Pojedyncze pliki</h2><ul>{''.join(f'<li><a href="assets/panel-piksel/{f}">{f}</a></li>' for f in ['tokens.css', 'components.css', 'icons.css', 'list-controls.js', 'table-sort.js', 'ui-controls.js', 'charts.js', 'components.json'])}</ul>
<h2>Wersje</h2><p>Bieżąca wersja: <b>{VERSION}</b> (semver: poprawka · nowy element · usunięcie). Zmiany: <a href="zasoby/historia-zmian.html">historia zmian</a>, zasady: <a href="zasoby/zarzadzanie.html">zarządzanie</a>.</p></div>'''
    page('pobierz.html', 'Pobierz', body, 'pobierz.html')
    # fundamenty
    icon_gallery = ''
    ik = EX['ikony']
    for sec_id in ('h1', 'h2', 'h3'):
        icon_gallery += grab('ikony', r'<section class="ex" aria-labelledby="' + sec_id + '"')
    leads = {'esencja': 'Skąd się wziął system, 10 zasad, kiedy go używać, a kiedy nie.', 'kolor': 'Paleta SNES (Jehkoba32) z akcentami NES. Kontrasty wyliczone z wartości hex.',
             'ikony': 'Siatka 12×12, rysowane piksel po pikselu. Pełna galeria poniżej — przełącz motyw, żeby zobaczyć wersje ciemne.', 'motywy': 'Te same komponenty, inne tokeny. Wysoki kontrast w Windows obsługuje CSS systemu.'}
    for s, t, parts in FOUNDATIONS:
        extra = ''
        if s == 'ikony':
            extra = '<h2 style="font:900 24px var(--font-sans);margin-top:40px">Galeria</h2>' + icon_gallery
        if s == 'motywy':
            hc = re.search(r'- \*\*Tryb wysokiego kontrastu.*', DESIGN).group(0)
            extra += '<div class="prose-doc"><h2>Wysoki kontrast</h2>' + md(hc) + '</div>'
        md_page(f'fundamenty/{s}.html', t, parts, leads.get(s, ''), extra)
    # komponenty
    for cid in COMPONENTS:
        component_page(cid, 'komponenty', 'Komponenty')
    for cid in PATTERNS:
        component_page(cid, 'wzorce', 'Wzorce')
    items = ''
    for cid in COMPONENTS:
        stt = main_status(cid)
        nm = short(cid)
        d = re.sub(r'<[^>]+>|\[[A-Z]\]|\{[A-Z]\}', '', CARDS[cid]['purpose'])
        d = html.escape(d[:130].rsplit(' ', 1)[0] + '…')
        colors = {'stable': 'var(--status-success)', 'preview': 'var(--status-info)', 'deprecated': 'var(--ink-3)'}
        items += f'<li data-comp="{html.escape((nm + " " + CARDS[cid]["name"]).lower())}"><a class="tile" href="{SLUG[cid]}.html"><span class="sbadge" style="--c:{colors.get(stt, "var(--ink-3)")};justify-self:start">{SPL[stt][0]}</span><b>{html.escape(nm)}</b><span class="desc">{d}</span></a></li>'
    body = f'''<h1 class="page-title">Komponenty</h1><p class="page-lead">Klocki, z których składa się każdy ekran. Status: <span class="sbadge" style="--c:var(--status-success)">stabilny</span> spełnia checklistę „gotowe”, <span class="sbadge" style="--c:var(--status-info)">testowy</span> działa i ma przykład, ale czeka na test z czytnikiem lub użycie na 2 ekranach.</p>
<div class="filter-row"><div class="field"><label for="comp-filter">Szukaj komponentu</label><input id="comp-filter" type="search" placeholder="np. tabela, przycisk, plik" autocomplete="off"></div><p style="margin:0 0 10px;font-size:14px;color:var(--ink-3)"><span id="comp-count">{len(COMPONENTS)}</span> z {len(COMPONENTS)}</p></div>
<ul class="tiles">{items}</ul>'''
    page('komponenty/index.html', 'Komponenty', body, 'komponenty/index.html')
    # koszyk + przepisy
    t, b = section('6.23 Koszyk', '###')
    shot = '<div class="figs"><figure class="ev"><img src="../img/cart-shop.png" alt="Koszyk sklepu złożony z klocków systemu" loading="lazy"><figcaption>Koszyk na ekranie sklepu (S13) po przebudowie w 1.10</figcaption></figure></div>'
    page('wzorce/koszyk.html', 'Koszyk sklepu', '<h1 class="page-title">Koszyk sklepu</h1><p class="page-lead">Złożenie z istniejących klocków — bez osobnego komponentu.</p><div class="prose-doc">' + md(b) + '</div>' + shot, 'wzorce/koszyk.html')
    t, b = section('6.24 Saldo', '###')
    page('wzorce/saldo.html', 'Saldo w nagłówku', '<h1 class="page-title">Saldo w nagłówku</h1><p class="page-lead">Złożenie z <code>.badge-seg</code> i sprite’a waluty — bez osobnego komponentu (decyzja 1.11).</p><div class="prose-doc">' + md(b) + '</div>', 'wzorce/saldo.html')
    rec = open(os.path.join(SK, 'references', 'screen-recipes.md'), encoding='utf-8').read()
    rec = re.sub(r'^# .*\n', '', rec)
    page('wzorce/przepisy-ekranow.html', 'Przepisy ekranów', '<h1 class="page-title">Przepisy ekranów</h1><p class="page-lead">Struktura i HTML dla typowych ekranów: katalog, kategoria, wyniki z filtrami, szczegóły, ranking, cennik, profil, formularz, pusty stan, panel użytkownika.</p><div class="prose-doc">' + md(rec) + '</div>', 'wzorce/przepisy-ekranow.html', wide=True)
    # zasoby
    for s, t, parts in RESOURCES:
        md_page(f'zasoby/{s}.html', t, parts)
    # 404 i Cloudflare
    page('404.html', 'Nie znaleziono', '<div class="empty" style="margin-top:24px"><span class="sprite sprite-xl s-key" aria-hidden="true"></span><h2>Tej strony nie ma</h2><p>Mogła zmienić adres po aktualizacji systemu.</p><a class="btn btn-primary" href="/index.html">Strona główna</a></div>', '404.html')
    open(os.path.join(OUT, '_headers'), 'w').write('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/assets/*
  Cache-Control: public, max-age=86400

/img/*
  Cache-Control: public, max-age=604800

/download/*
  Content-Disposition: attachment
''')
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n')
    open(os.path.join(OUT, '_redirects'), 'w').write('/favicon.ico /favicon.svg 301\n')
    os.makedirs(os.path.join(OUT, 'przyklady'), exist_ok=True)
    for n in ('komponenty', 'wzorce', 'ikony'):
        h = EX[n].replace('../assets/', '../assets/panel-piksel/')
        open(os.path.join(OUT, 'przyklady', n + '.html'), 'w', encoding='utf-8').write(h)
    os.makedirs(os.path.join(OUT, 'archiwum'), exist_ok=True)
    shutil.copytree(os.path.join(ROOT, 'docs', 'kandydaci'), os.path.join(OUT, 'archiwum', 'kandydaci'), dirs_exist_ok=True)
    for n in ('decyzje-v1-1', 'kwestie-otwarte', 'kandydaci'):
        h = open(os.path.join(ROOT, 'docs', n + '.html'), encoding='utf-8').read()
        h = h.replace('../skills/panel-piksel-ui/assets/', '../assets/panel-piksel/').replace('src="evidence/', 'src="../img/').replace('panel-piksel-komponenty-v2.html', '../komponenty/index.html')
        open(os.path.join(OUT, 'archiwum', n + '.html'), 'w', encoding='utf-8').write(h)
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f'site/: {n} plików, wersja {VERSION}')


if __name__ == '__main__':
    build()
