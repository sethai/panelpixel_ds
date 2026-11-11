#!/usr/bin/env python3
"""Jedno źródło systemu: assets/ skilla → wszystkie kopie w projekcie. Bez zewnętrznych bibliotek.

Użycie (w katalogu projektu, gdzie leży panel-piksel.config.json):
  python3 <skill>/scripts/sync_system.py           # zapisuje: kopie, wklejone bloki, design.md §0 i §9, tokens.json
  python3 <skill>/scripts/sync_system.py --check   # tylko sprawdza rozjazdy (kod wyjścia 1, jeśli są) — do CI

panel-piksel.config.json:
{
  "designMd": "design.md",                         // specyfikacja; §9 (kod) i tabela statusów w §0 są generowane
  "copies": ["screens/landing/panel-piksel"],      // katalogi z kopią plików systemu (strony z <link>)
  "builds": [{"from": "screens/landing/index.html", "to": "screens/landing/landing-portal-pracy.html"}],
  "inlined": ["skills/…/outputs/*.html"],          // pliki z wklejonymi blokami <style id="pp-…">, <script id="pp-…">
  "installed": "~/.claude/skills/panel-piksel-ui"  // opcjonalnie: zainstalowana kopia skilla
}
Źródłem są zawsze pliki w assets/ skilla — kopie się nadpisuje, nigdy nie edytuje.
"""
import filecmp
import glob
import json
import os
import re
import shutil
import subprocess
import sys

SKILL = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ASSETS = os.path.join(SKILL, 'assets')
FILES = ['tokens.css', 'components.css', 'icons.css', 'list-controls.js', 'table-sort.js', 'ui-controls.js', 'charts.js']
STYLE_IDS = {'tokens': 'tokens.css', 'components': 'components.css', 'icons': 'icons.css'}
SCRIPT_IDS = {'list-controls': 'list-controls.js', 'table-sort': 'table-sort.js', 'ui-controls': 'ui-controls.js', 'charts': 'charts.js'}


def read(p):
    return open(p, encoding='utf-8').read()


def version():
    return read(os.path.join(SKILL, 'VERSION')).strip()


# ---------- tokens.json (format W3C Design Tokens) ----------
def css_vars(block):
    out = {}
    for m in re.finditer(r'--([\w-]+)\s*:\s*([^;]+);', re.sub(r'/\*.*?\*/', '', block, flags=re.S)):
        out[m.group(1)] = m.group(2).strip()
    return out


def tokens_json():
    css = read(os.path.join(ASSETS, 'tokens.css'))
    root = css_vars(re.search(r':root\s*\{(.*?)\n\}', css, re.S).group(1))
    dark = css_vars(re.search(r'\[data-theme="dark"\]\s*\{(.*?)\n\}', css, re.S).group(1))
    groups = {}

    def kind(name, v):
        if name.startswith(('font-',)):
            return 'fontFamily', 'font'
        if name.startswith('z-'):
            return 'number', 'zIndex'
        if name.startswith(('motion', 'ease')):
            return ('duration' if v.endswith('ms') else None), 'motion'
        if name.startswith('shadow') or name in ('border', 'notch'):
            return None, 'shape'
        if name.startswith(('space-', 'btn-h', 'row-h', 'bp-')):
            return 'dimension', 'size'
        return 'color', 'color'

    def val(v):
        a = re.fullmatch(r'var\(--([\w-]+)\)', v)
        if a:
            return '{%s.%s}' % (kind(a.group(1), root.get(a.group(1), ''))[1], a.group(1))
        return v
    for name, v in root.items():
        t, g = kind(name, v)
        tok = {'$value': int(v) if t == 'number' and v.isdigit() else val(v)}
        if t:
            tok['$type'] = t
        if name in dark and dark[name] != v:
            tok['$extensions'] = {'panel-piksel.dark': val(dark[name])}
        groups.setdefault(g, {})[name] = tok
    groups['$description'] = f'Panel & Piksel {version()} — wygenerowane z assets/tokens.css przez scripts/sync_system.py. Nie edytuj ręcznie.'
    return json.dumps(groups, ensure_ascii=False, indent=2) + '\n'


# ---------- design.md ----------
STATUS_PL = {'stable': 'stabilny', 'preview': 'testowy', 'draft': 'kandydat', 'deprecated': 'wycofywany'}


def registry_table():
    reg = json.loads(read(os.path.join(ASSETS, 'components.json')))
    rows = ['| Komponent | Status | Od | Klasy / skrypt | Opis | Brakuje do „stabilny” / zastąpione przez |', '|---|---|---|---|---|---|']
    order = {'stable': 0, 'preview': 1, 'draft': 2, 'deprecated': 3}
    for c in sorted(reg['components'], key=lambda c: order[c['status']]):
        cls = ', '.join('`%s`' % x for x in c.get('classes', [])[:4]) + (' …' if len(c.get('classes', [])) > 4 else '')
        if c.get('js'):
            cls += (' · ' if cls else '') + '`%s`' % c['js']
        extra = ', '.join(c.get('missing', []))
        if c['status'] == 'deprecated':
            extra = '→ %s · wycofany w %s, usunięcie w %s' % (c['replacedBy'], c['deprecatedIn'], c['removeIn'])
        elif c.get('note'):
            extra = (extra + '; ' if extra else '') + c['note']
        rows.append('| %s | **%s** | %s | %s | %s | %s |' % (c['name'], STATUS_PL[c['status']], c.get('since', '—'), cls or '—', c.get('docs', '—'), extra or '—'))
    return '\n'.join(rows)


def design_md(path):
    s = read(path)
    a = s.find('<!-- pp:registry -->'), s.find('<!-- /pp:registry -->')
    if a[0] >= 0 and a[1] > a[0]:
        s = s[:a[0]] + '<!-- pp:registry -->\n' + registry_table() + '\n' + s[a[1]:]
    i, j = s.find('### 9.1 `tokens.css`'), s.find('### 9.3 Pozostałe pliki')
    if i >= 0 and j > i:
        s = (s[:i] + '### 9.1 `tokens.css`\n\n```css\n' + read(os.path.join(ASSETS, 'tokens.css')).rstrip() + '\n```\n\n'
             '### 9.2 `components.css`\n\n```css\n' + read(os.path.join(ASSETS, 'components.css')).rstrip() + '\n```\n\n' + s[j:])
    s = re.sub(r'> Wersja \*\*[\d.]+\*\*', '> Wersja **%s**' % version(), s, count=1)
    return s


# ---------- wklejone bloki ----------
def inline_refresh(html):
    for sid, f in STYLE_IDS.items():
        body = read(os.path.join(ASSETS, f))
        html = re.sub(r'<style id="(?:pp|panel-piksel)-%s">.*?</style>' % sid, lambda m: '<style id="pp-%s">\n%s\n</style>' % (sid, body), html, count=1, flags=re.S)
    for sid, f in SCRIPT_IDS.items():
        body = read(os.path.join(ASSETS, f))
        html = re.sub(r'<script id="pp-%s">.*?</script>' % sid, lambda m: '<script id="pp-%s">\n%s\n</script>' % (sid, body), html, count=1, flags=re.S)
    return html


def main():
    check = '--check' in sys.argv
    cfg_path = os.path.join(os.getcwd(), 'panel-piksel.config.json')
    cfg = json.loads(read(cfg_path)) if os.path.exists(cfg_path) else {}
    drift, wrote = [], []

    def put(path, content):
        old = read(path) if os.path.exists(path) else None
        if old != content:
            drift.append(os.path.relpath(path))
            if not check:
                open(path, 'w', encoding='utf-8').write(content)
                wrote.append(os.path.relpath(path))

    put(os.path.join(ASSETS, 'tokens.json'), tokens_json())
    if cfg.get('designMd'):
        md = design_md(cfg['designMd'])
        put(cfg['designMd'], md)
        put(os.path.join(SKILL, 'references', 'design-system.md'), md)
    for d in cfg.get('copies', []):
        for f in FILES:
            src, dst = os.path.join(ASSETS, f), os.path.join(d, f)
            if not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False):
                drift.append(dst)
                if not check:
                    shutil.copyfile(src, dst); wrote.append(dst)
    for b in cfg.get('builds', []):
        if not check:
            subprocess.run([sys.executable, os.path.join(SKILL, 'scripts', 'inline_css.py'), b['from'], b['to']], capture_output=True)
        put(b['to'], inline_refresh(read(b['to'])))
    for pattern in cfg.get('inlined', []):
        for p in sorted(glob.glob(pattern)):
            put(p, inline_refresh(read(p)))
    inst = cfg.get('installed') and os.path.expanduser(cfg['installed'])
    if inst and os.path.isdir(inst):
        cmp = filecmp.dircmp(SKILL, inst)
        def differs(c):
            return bool(c.left_only or c.right_only or c.diff_files) or any(differs(x) for x in c.subdirs.values())
        if differs(cmp):
            drift.append(inst)
            if not check:
                subprocess.run(['rsync', '-a', '--delete', SKILL + '/', inst + '/'], check=True); wrote.append(inst)

    print('Panel & Piksel', version())
    if check:
        if drift:
            print('ROZJAZD z assets/ — uruchom sync_system.py bez --check:')
            for d in drift:
                print('  ', d)
            sys.exit(1)
        print('OK — wszystkie kopie zgodne ze źródłem.')
    else:
        print('Zaktualizowano:' if wrote else 'Nic do zmiany.')
        for w in wrote:
            print('  ', w)


if __name__ == '__main__':
    main()
