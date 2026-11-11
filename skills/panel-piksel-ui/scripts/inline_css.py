#!/usr/bin/env python3
"""Zamienia linki do tokens.css / components.css (i skrypty table-sort.js, list-controls.js) na wklejone bloki — powstaje jeden przenośny plik.

Użycie:  python3 inline_css.py ekran.html [wynik.html]
Bez drugiego argumentu nadpisuje plik wejściowy. Plik z już wklejonymi blokami (id="pp-…") jest odświeżany do bieżącej wersji. CSS bierze z assets/ skillu (zawsze aktualna wersja systemu),
więc nie trzeba kopiować plików obok ekranu.
"""
import os
import re
import sys

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    src_path = sys.argv[1]
    dst_path = sys.argv[2] if len(sys.argv) > 2 else src_path
    html = open(src_path, encoding='utf-8').read()
    done = []
    for name in ('tokens.css', 'components.css', 'icons.css'):
        pat = re.compile(r'<link[^>]+href=["\'][^"\']*' + re.escape(name) + r'["\'][^>]*>', re.I)
        css = open(os.path.join(ASSETS, name), encoding='utf-8').read()
        block = f'<style id="pp-{name.split(".")[0]}">\n{css}\n</style>'
        html, n = pat.subn(lambda m: block, html, count=1)
        if n:
            done.append(name)
            continue
        # już wklejony blok — odśwież do aktualnej wersji systemu
        old = re.compile(r'<style id="(?:pp|panel-piksel)-' + name.split('.')[0] + r'">.*?</style>', re.S)
        html, n = old.subn(lambda m: block, html, count=1)
        if n:
            done.append(name + ' (odświeżony)')
        elif name == 'icons.css':
            pass  # ikony tylko gdy ekran je podlinkował
        else:
            # brak linku i brak wklejonego bloku — dodaj przed </head>
            html = html.replace('</head>', block + '\n</head>', 1)
            done.append(name + ' (dodany)')
    # skrypty systemu, jeśli są podlinkowane
    for js_name in ('table-sort.js', 'list-controls.js', 'ui-controls.js', 'charts.js'):
        js_pat = re.compile(r'<script[^>]+src=["\'][^"\']*' + re.escape(js_name) + r'["\'][^>]*>\s*</script>', re.I)
        if js_pat.search(html):
            js = open(os.path.join(ASSETS, js_name), encoding='utf-8').read()
            html = js_pat.sub(lambda m: '<script id="pp-' + js_name[:-3] + '">\n' + js + '\n</script>', html, count=1)
            done.append(js_name)
        else:
            old = re.compile(r'<script id="pp-' + js_name[:-3] + r'">.*?</script>', re.S)
            if old.search(html):
                js = open(os.path.join(ASSETS, js_name), encoding='utf-8').read()
                html = old.sub(lambda m: '<script id="pp-' + js_name[:-3] + '">\n' + js + '\n</script>', html, count=1)
                done.append(js_name + ' (odświeżony)')
    open(dst_path, 'w', encoding='utf-8').write(html)
    print(f'Wklejono: {", ".join(done) or "nic (już wklejone)"} → {dst_path}')


if __name__ == '__main__':
    main()
