#!/usr/bin/env python3
"""Test wizualny: porównuje zrzuty stron z zatwierdzonymi wzorcami (baseline). Bez zewnętrznych bibliotek.

Użycie:
  python3 visual_regression.py --update KATALOG_WZORCÓW strona.html [strona2.html …]   # zapisz / zatwierdź wzorce
  python3 visual_regression.py KATALOG_WZORCÓW strona.html [strona2.html …]            # porównaj (kod wyjścia 1 przy różnicy)

Każda strona jest renderowana w 1280 i 390 px, w trybie jasnym i ciemnym (data-theme na <html>), z wyłączonym ruchem.
Różnica = odsetek bloków 8×8 px, których średni kolor zmienił się o więcej niż 20 (na kanał); próg zaliczenia 0,1%.
Porównanie blokowe ignoruje drgania wygładzania liter między uruchomieniami Chrome.
Przy różnicy powstaje obraz <nazwa>.diff.png: szary wzorzec + czerwone piksele, które się zmieniły.
Zmiana zamierzona? Obejrzyj diff i uruchom z --update (to jest „zatwierdzenie” nowego wyglądu).
Różnica jest zgłaszana dopiero po 3 próbach — fonty z Google Fonts czasem ładują się po zrzucie.
Wzorce zapisuj na tej samej maszynie i wersji Chrome, na której będą sprawdzane.
"""
import os
import struct
import subprocess
import sys
import tempfile
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_check import find_chrome  # noqa: E402

THRESHOLD = 0.001   # 0,1% bloków
CHANNEL = 20        # średnia zmiana kanału RGB w bloku
BLOCK = 8

WRAP = """<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0}iframe{border:0;display:block}</style></head><body>
<iframe id="f" style="width:%(w)dpx;height:%(h)dpx"></iframe>
<script>
const f=document.getElementById('f');
f.onload=async()=>{const d=f.contentDocument;d.documentElement.setAttribute('data-theme','%(theme)s');
  const st=d.createElement('style');st.textContent='*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}';d.head.appendChild(st);
  await d.fonts.ready;document.title='H'+d.documentElement.scrollHeight;};
f.src='%(src)s';
</script></body></html>"""


def run(chrome, args):
    return subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-prefers-reduced-motion', '--disable-lcd-text', '--font-render-hinting=none', '--force-device-scale-factor=1',
                           '--allow-file-access-from-files', '--virtual-time-budget=15000', *args], capture_output=True, text=True, timeout=180)


def shoot(chrome, html, width, theme, out, tmp):
    src = 'file://' + os.path.abspath(html)
    wrap = os.path.join(tmp, 'w.html')
    open(wrap, 'w').write(WRAP % {'w': width, 'h': 1200, 'theme': theme, 'src': src})
    dom = run(chrome, ['--window-size=%d,1200' % max(width, 520), '--dump-dom', 'file://' + wrap]).stdout
    import re
    m = re.search(r'<title>H(\d+)</title>', dom)
    h = min(int(m.group(1)) if m else 3000, 9000)
    open(wrap, 'w').write(WRAP % {'w': width, 'h': h, 'theme': theme, 'src': src})
    run(chrome, ['--window-size=%d,%d' % (max(width, 520), h), '--screenshot=' + out, 'file://' + wrap])
    return out


# ---------- PNG bez bibliotek ----------
def png_read(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    pos, idat, w = 8, b'', 0
    while pos < len(data):
        n, typ = struct.unpack('>I4s', data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if typ == b'IHDR':
            w, h, depth, ctype = struct.unpack('>IIBB', body[:10])
            assert depth == 8 and ctype in (2, 6), 'obsługiwane tylko 8-bit RGB/RGBA'
            bpp = 3 if ctype == 2 else 4
        elif typ == b'IDAT':
            idat += body
        pos += 12 + n
    raw, stride = zlib.decompress(idat), w * bpp
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f, line = raw[i], bytearray(raw[i + 1:i + 1 + stride]); i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif f == 4:
                p = a + b - c; pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line)); prev = line
    return w, h, bpp, rows


def png_write(path, w, h, rows):
    raw = b''.join(b'\x00' + r for r in rows)
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))


def compare(base, new, diff_path):
    """Porównanie blokowe: średni kolor kwadratów BLOCK×BLOCK px. Drgania wygładzania liter (pojedyncze piksele)
    giną w średniej; przesunięcie układu, zmiana koloru, ramki czy tekstu zmienia średnią wyraźnie."""
    bw, bh, bb, br = png_read(base)
    nw, nh, nb, nr = png_read(new)
    if (bw, bh) != (nw, nh):
        if os.path.exists(diff_path):
            os.remove(diff_path)
        return 1.0, f'inny rozmiar: wzorzec {bw}×{bh}, teraz {nw}×{nh} (zmienił się układ — porównaj zrzuty ręcznie)'
    cols, rows_n = bw // BLOCK, bh // BLOCK
    bad = set()
    for by in range(rows_n):
        acc_a = [[0, 0, 0] for _ in range(cols)]; acc_b = [[0, 0, 0] for _ in range(cols)]
        for y in range(by * BLOCK, by * BLOCK + BLOCK):
            a, b = br[y], nr[y]
            for bx in range(cols):
                sa, sb = acc_a[bx], acc_b[bx]
                for x in range(bx * BLOCK, bx * BLOCK + BLOCK):
                    ia, ib = x * bb, x * nb
                    sa[0] += a[ia]; sa[1] += a[ia + 1]; sa[2] += a[ia + 2]
                    sb[0] += b[ib]; sb[1] += b[ib + 1]; sb[2] += b[ib + 2]
        n = BLOCK * BLOCK
        for bx in range(cols):
            if max(abs(acc_a[bx][k] - acc_b[bx][k]) for k in range(3)) > CHANNEL * n:
                bad.add((bx, by))
    ratio = len(bad) / max(1, cols * rows_n)
    if ratio > THRESHOLD:
        out = []
        for y in range(bh):
            a, line = br[y], bytearray()
            for x in range(bw):
                if (x // BLOCK, y // BLOCK) in bad:
                    line += b'\xe0\x10\x40'
                else:
                    g = (a[x * bb] + a[x * bb + 1] + a[x * bb + 2]) // 6 + 100; line += bytes((g, g, g))
            out.append(bytes(line))
        png_write(diff_path, bw, bh, out)
    return ratio, f'{len(bad)} bloków {BLOCK}×{BLOCK} px ({ratio * 100:.2f}%)'


def main():
    args = [a for a in sys.argv[1:] if a != '--update']
    update = '--update' in sys.argv
    if len(args) < 2:
        print(__doc__); sys.exit(2)
    base_dir, pages = args[0], args[1:]
    os.makedirs(base_dir, exist_ok=True)
    chrome = find_chrome()
    if not chrome:
        print('Nie znaleziono Chrome/Chromium.'); sys.exit(2)
    fails = 0
    with tempfile.TemporaryDirectory() as tmp:
        for page in pages:
            name = os.path.splitext(os.path.basename(page))[0]
            for theme in ('light', 'dark'):
                for w in (1280, 390):
                    key = f'{name}-{theme}-{w}'
                    shot = shoot(chrome, page, w, theme, os.path.join(tmp, key + '.png'), tmp)
                    base = os.path.join(base_dir, key + '.png')
                    if update or not os.path.exists(base):
                        os.replace(shot, base); print(f'  zapisano wzorzec  {key}')
                        continue
                    ratio, msg = compare(base, shot, os.path.join(base_dir, key + '.diff.png'))
                    tries = 1
                    while ratio > THRESHOLD and tries < 3:  # fonty z sieci bywają spóźnione — ponów zrzut, zanim zgłosisz różnicę
                        shot = shoot(chrome, page, w, theme, os.path.join(tmp, key + '.png'), tmp)
                        ratio, msg = compare(base, shot, os.path.join(base_dir, key + '.diff.png'))
                        tries += 1
                    if tries > 1:
                        msg += f' (po {tries} próbach)'
                    ok = ratio <= THRESHOLD
                    fails += not ok
                    has_diff = os.path.exists(os.path.join(base_dir, key + '.diff.png'))
                    print(f'  {"OK     " if ok else "RÓŻNICA"} {key}: {msg}' + (f' → {key}.diff.png' if not ok and has_diff else ''))
                    if ok and os.path.exists(os.path.join(base_dir, key + '.diff.png')):
                        os.remove(os.path.join(base_dir, key + '.diff.png'))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
