#!/usr/bin/env python3
"""Pełna odbudowa Panel & Piksel w jednym kroku — uruchom z katalogu repozytorium:

    python3 tools/build_all.py            # odbuduj wszystko
    python3 tools/build_all.py --check    # tylko sprawdź, czy kopie systemu są zgodne ze źródłem

Kolejność (każdy krok czyta wynik poprzedniego):
  1. skills/panel-piksel-ui/scripts/sync_system.py — tokens.json, tabela rejestru i kod w design.md §0/§9,
     references/design-system.md, kopie CSS/JS w ekranach, skill zainstalowany w ~/.claude/skills
  2. tools/docgen.py     — dokumentacja dla designerów: docs/panel-piksel-komponenty-v2.html
  3. tools/build_zip.py  — paczka do dzielenia się: dist/panel-piksel-<wersja>.zip
  4. tools/build_site.py — strona dla Cloudflare Pages: site/ (zawiera ZIP z kroku 3 do pobrania)
  5. ZIP strony          — dist/panel-piksel-site-<wersja>.zip (do wgrania w Cloudflare → Upload assets)
"""
import os
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, 'skills', 'panel-piksel-ui')


def run(*args):
    print('→', ' '.join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def zip_site(version):
    site = os.path.join(ROOT, 'site')
    out = os.path.join(ROOT, 'dist', f'panel-piksel-site-{version}.zip')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for base, dirs, files in os.walk(site):
            dirs.sort()
            for f in sorted(files):
                if f == '.DS_Store':
                    continue
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, site))
    print(f'{os.path.relpath(out, ROOT)} · {os.path.getsize(out) / 1e6:.1f} MB')


def main():
    sync = os.path.join(SK, 'scripts', 'sync_system.py')
    if '--check' in sys.argv:
        run(sync, '--check')
        return
    version = open(os.path.join(SK, 'VERSION')).read().strip()
    run(sync)
    run('tools/docgen.py')
    run('tools/build_zip.py')
    run('tools/build_site.py')
    zip_site(version)
    run(sync, '--check')


if __name__ == '__main__':
    main()
