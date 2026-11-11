#!/usr/bin/env python3
"""Render ekranu w 1280 px i 390 px przez headless Chrome — bez dodatkowych bibliotek.

Użycie:  python3 render_check.py ekran.html [katalog_na_zrzuty]
Wynik:   szerokość dokumentu dla obu szerokości (czy strona przewija się poziomo),
         sprawdzenie załadowania fontów z polskimi znakami, zrzuty <nazwa>-1280.png i <nazwa>-390.png
         oraz test klikania: każdy przycisk, zakładka, checkbox i link „#” w <main> jest klikany
         na świeżo załadowanej stronie — kontrolka, po której nic się nie zmienia, jest zgłaszana jako MARTWA.

Dlaczego przez ramkę: okno headless Chrome nie zwęża się poniżej ok. 500 px, więc widok 390 px
jest renderowany w <iframe> o szerokości 390 px wewnątrz szerszego okna.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CANDIDATES = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
    'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome',
]


def find_chrome():
    for c in CANDIDATES:
        p = c if os.path.isabs(c) else shutil.which(c)
        if p and os.path.exists(p):
            return p
    return None


WRAPPER = """<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#888}iframe{border:0;display:block;background:#fff}</style></head>
<body><iframe id="f" src="SRC" style="width:WIDTHpx;height:HEIGHTpx"></iframe><pre id="out"></pre>
<script>
const f=document.getElementById('f');
f.addEventListener('load',async()=>{
  const d=f.contentDocument; let r={width:WIDTH};
  try{ await d.fonts.ready; await Promise.all([d.fonts.load('16px Archivo','ąę'), d.fonts.load('10px "Press Start 2P"','łż')]).catch(()=>{});
    r.scrollWidth=d.documentElement.scrollWidth; r.height=d.documentElement.scrollHeight;
    r.fonts={archivo:d.fonts.check('16px Archivo','ąę'), pixel:d.fonts.check('10px "Press Start 2P"','łż')};
    const wide=[...d.querySelectorAll('body *')].filter(e=>{const b=e.getBoundingClientRect();return b.right>WIDTH+1 && getComputedStyle(e).position!=='fixed' && !e.closest('.table-wrap,.tabs')}).slice(0,5);
    r.offenders=wide.map(e=>e.tagName.toLowerCase()+(e.className?'.'+String(e.className).trim().split(/\\s+/).join('.'):'')+' → '+Math.round(e.getBoundingClientRect().right)+'px');
  }catch(e){ r.error=String(e); }
  document.getElementById('out').textContent='RESULT'+JSON.stringify(r)+'END';
});
</script></body></html>"""


def run(chrome, args):
    return subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                           '--allow-file-access-from-files', '--virtual-time-budget=15000', *args],
                          capture_output=True, text=True, timeout=120)


def check(chrome, html, width, outdir, tmp):
    src = 'file://' + os.path.abspath(html)
    base = os.path.splitext(os.path.basename(html))[0]
    wrap = os.path.join(tmp, f'wrap-{width}.html')
    open(wrap, 'w').write(WRAPPER.replace('SRC', src).replace('WIDTH', str(width)).replace('HEIGHT', '1200'))
    out = run(chrome, ['--window-size=%d,1200' % max(width, 520), '--dump-dom', 'file://' + wrap]).stdout
    m = re.search(r'RESULT(.*?)END', out, re.S)
    res = json.loads(m.group(1).replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')) if m else {'width': width, 'error': 'brak wyniku (Chrome nie załadował strony?)'}
    h = min(int(res.get('height') or 1200), 12000)
    open(wrap, 'w').write(WRAPPER.replace('SRC', src).replace('WIDTH', str(width)).replace('HEIGHT', str(h)))
    shot = os.path.join(outdir, f'{base}-{width}.png')
    run(chrome, ['--window-size=%d,%d' % (width if width >= 520 else 520, h), '--screenshot=' + shot, 'file://' + wrap])
    res['screenshot'] = shot if os.path.exists(shot) else None
    return res


AUDIT = r"""<!doctype html><html><head><meta charset="utf-8"></head><body>
<iframe id="f" style="width:1280px;height:900px;border:0"></iframe><pre id="out"></pre>
<script>
const SRC = "SRCURL";
const SEL = 'main button, main [role=tab], main a[href^="#"], main input[type=checkbox], main input[type=radio], main summary, main select';
const f = document.getElementById('f');
const load = () => new Promise(r => { f.onload = () => setTimeout(r, 300); f.src = SRC + '?t=' + Math.random(); });
// stan strony: treść <main>, otwarte okna (<dialog>), powiadomienia poza <main>, wartości pól, adres
const snap = d => { const m = d.querySelector('main');
  const vals = [...d.querySelectorAll('input, select, textarea')].map(e => e.type === 'checkbox' || e.type === 'radio' ? (e.checked ? 1 : 0) : e.value).join('|');
  const overlays = [...d.querySelectorAll('dialog[open], .toasts')].map(e => e.id + e.innerHTML.length).join('|');
  return (m ? m.innerHTML : d.body.innerHTML).replace(/ data-pp-probe="1"/g, '') + '|' + vals + '|' + overlays + '|' + d.defaultView.location.hash; };
(async () => {
  await load();
  let d = f.contentDocument, n = d.querySelectorAll(SEL).length, dead = [], tested = 0;
  for (let i = 0; i < n && i < 80; i++) {
    await load(); d = f.contentDocument;
    const el = d.querySelectorAll(SEL)[i];
    if (!el || !el.getClientRects().length || el.getAttribute('aria-disabled') === 'true' || el.disabled) continue;
    if (el.tagName === 'SELECT' || (el.type === 'radio' && el.checked)) continue;
    if (el.getAttribute('aria-pressed') === 'true' && el.closest('.tabs[role=group]')) continue; // wybrana opcja w grupie przełączników — ponowny klik z definicji nic nie zmienia // lista: wybór z systemowej listy; zaznaczone radio: klik nic nie zmienia z definicji
    const tipId = el.getAttribute('aria-describedby'); if (tipId && d.getElementById(tipId) && d.getElementById(tipId).getAttribute('role') === 'tooltip') continue; // podpowiedź: najechanie / fokus
    if (el.closest('form') && el.type === 'submit' && !el.closest('form').hasAttribute('data-filter-for') && el.closest('form').getAttribute('action')) continue; // wysyła na serwer
    tested++;
    const before = snap(d);
    try { el.click(); } catch (e) {}
    await new Promise(r => setTimeout(r, 200));
    let after; try { after = snap(f.contentDocument); } catch (e) { after = 'NAV'; }
    const label = (el.textContent.trim() || el.getAttribute('aria-label') || (el.closest('label') || {}).textContent || el.value || '').replace(/\s+/g, ' ').trim().slice(0, 40);
    if (before === after && !(f.contentDocument && f.contentDocument !== d)) dead.push(el.tagName.toLowerCase() + (el.type === 'checkbox' ? '[checkbox]' : '') + ' „' + label + '”');
  }
  document.getElementById('out').textContent = 'RESULT' + JSON.stringify({ total: n, tested, dead }) + 'END';
})();
</script></body></html>"""


def click_audit(chrome, html, tmp):
    wrap = os.path.join(tmp, 'audit.html')
    open(wrap, 'w').write(AUDIT.replace('SRCURL', 'file://' + os.path.abspath(html)))
    out = run(chrome, ['--window-size=1300,950', '--virtual-time-budget=120000', '--dump-dom', 'file://' + wrap]).stdout
    m = re.search(r'RESULT(.*?)END', out, re.S)
    return json.loads(m.group(1).replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')) if m else None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    html = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(html))
    os.makedirs(outdir, exist_ok=True)
    chrome = find_chrome()
    if not chrome:
        print('Nie znaleziono Chrome/Chromium — obejrzyj ekran ręcznie w 1280 i 390 px.')
        sys.exit(2)
    bad = False
    with tempfile.TemporaryDirectory() as tmp:
        for w in (1280, 390):
            r = check(chrome, html, w, outdir, tmp)
            if 'error' in r:
                print(f'{w}px: BŁĄD — {r["error"]}')
                bad = True
                continue
            over = r['scrollWidth'] > w + 1
            bad |= over
            fonts = r.get('fonts', {})
            print(f'{w}px: szerokość dokumentu {r["scrollWidth"]}px {"— PRZEWIJA SIĘ POZIOMO" if over else "(OK)"}; '
                  f'fonty: Archivo {"OK" if fonts.get("archivo") else "BRAK"}, Press Start 2P {"OK" if fonts.get("pixel") else "BRAK"}; '
                  f'zrzut: {r["screenshot"]}')
            if over and r.get('offenders'):
                print('   wystają: ' + '; '.join(r['offenders']))
        audit = click_audit(chrome, html, tmp)
        if audit is None:
            print('Test klikania: brak wyniku (pomiń albo sprawdź ręcznie).')
        else:
            print(f'Test klikania: {audit["tested"]} z {audit["total"]} kontrolek klikniętych, bez żadnego efektu: {len(audit["dead"])}')
            for d in audit['dead']:
                print('   MARTWA ' + d)
            bad |= bool(audit['dead'])
    print('Obejrzyj oba zrzuty — skrypt nie oceni układu ani nakładania się elementów.')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
