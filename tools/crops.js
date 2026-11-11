// Element crops of components from the generated screens → docs/evidence/*.png (+ crops.json with metadata)
const puppeteer = require(process.env.PUPPETEER_CORE || 'puppeteer-core') // npm i puppeteer-core; Chrome z /Applications;
const fs = require('fs');
const R = require('path').resolve(__dirname, '..') + '/';
const WS = R + 'skills/panel-piksel-ui-workspace/iteration-1/';
const OUT = R + 'docs/evidence/';
fs.mkdirSync(OUT, { recursive: true });
const SRC = {
  S10: R + 'screens/landing/landing-portal-pracy.html',
  S11: WS + 'job-board-listing-filters/with_skill/outputs/levelup-jobs-wyniki.html',
  S12: WS + 'leaderboard-high-scores/with_skill/outputs/leaderboard.html',
  S13: WS + 'game-item-shop/with_skill/outputs/sklep-przedmiotow.html',
  S14: WS + 'catalog-home-directory/with_skill/outputs/index.html',
  S15: WS + 'job-offer-detail/with_skill/outputs/oferta-senior-unity-developer.html',
  S16: WS + 'employer-dashboard-table/with_skill/outputs/panel-pracodawcy.html',
  S04: R + 'research/direction-study.html',
  S20: R + 'skills/panel-piksel-ui/examples/komponenty.html',
  S21: R + 'skills/panel-piksel-ui/examples/wzorce.html',
  S22: R + 'skills/panel-piksel-ui/examples/ikony.html',
};
const ONLY = process.argv[2] ? process.argv[2].split(',') : null;
const C0 = [
  // id, source, selector, opts
  ['btn-states', 'S04', '#comp .states', {}],
  ['btn-disabled-variants', 'S04', '#comp .dis-grid', {}],
  ['btn-disabled-in-context', 'S15', 'aside .panel.is-featured, aside .panel', { pad: 10 }],
  ['btn-toggle-pressed', 'S10', '.offers .card', { pre: "document.querySelector('.offers .card button[data-label-on]').click()" }],
  ['badges', 'S04', '#comp .spec:has(.badge-seg)', { pad: 8 }],
  ['chips-card', 'S11', '[data-list] .card .chips', { pad: 8 }],
  ['active-filters', 'S11', '.active-filters', { pad: 8 }],
  ['panel-list', 'S10', '.cat-grid .panel', {}],
  ['panel-featured', 'S14', '.panel.is-featured', {}],
  ['panel-list-mobile', 'S10', '.cat-grid .panel', { w: 390 }],
  ['card-offer', 'S11', '[data-list] .card', {}],
  ['card-offer-empty-salary', 'S11', '[data-list] .card:not([hidden]):has(.amount.is-empty)', {}],
  ['card-item-shop', 'S13', '.item-grid li', {}],
  ['card-offer-mobile', 'S10', '.offers .card', { w: 390 }],
  ['filters', 'S11', '.panel-filters', {}],
  ['search-main-hero', 'S10', '.hero .search-main', { pad: 12 }],
  ['tabs-sort', 'S11', '.tabs[data-sort-for]', { pad: 8 }],
  ['tabs-period', 'S12', '[role=tablist]', { pad: 8 }],
  ['tabs-status', 'S16', '[role=tablist]', { pad: 8 }],
  ['table-ranking', 'S10', '#ranking .table-wrap', {}],
  ['table-dashboard', 'S16', '.table-wrap', { maxH: 420 }],
  ['table-leaderboard-sorted', 'S12', '.table-wrap', { maxH: 380, pre: "document.querySelector('th .sort[data-key=\"g\"]').click()" }],
  ['table-mobile', 'S12', '.table-wrap', { w: 390, maxH: 360 }],
  ['pagination', 'S12', '#pages', { pad: 8 }],
  ['podium', 'S12', '.podium', {}],
  ['tiers', 'S10', '.tiers', {}],
  ['tier-tag-table', 'S16', '.table-wrap', { clipCols: true, maxH: 260 }],
  ['rarity-shop', 'S13', '.item-grid li .item-top', { pad: 6 }],
  ['header', 'S10', '.site-header', {}],
  ['header-mobile', 'S10', '.site-header', { w: 390 }],
  ['breadcrumbs-pagehead', 'S12', 'main', { maxH: 230 }],
  ['footer', 'S10', '.site-footer', {}],
  ['callout-cta', 'S10', '.cta', { pad: 8 }],
  ['callout-dashboard', 'S16', '.callout', { pad: 8 }],
  ['empty-state', 'S11', '[data-empty-for]', { pad: 10, pre: "(()=>{const i=document.querySelector('input[data-search]');i.value='kobol';i.dispatchEvent(new Event('input',{bubbles:true}));})()" }],
  ['facts-hero', 'S10', '.hero .facts', { pad: 8 }],
  ['facts-offer', 'S15', '.facts', { pad: 8 }],
  ['details-dither', 'S04', '#comp .dither', { padTop: 40, pad: 30, parentSpec: true }],
  ['hero', 'S10', '.hero', {}],
  ['steps', 'S10', '.steps', {}],
  ['cart-shop', 'S13', '.cart', {}],
  ['tabs-sort-mobile', 'S11', '.tabs[data-sort-for]', { w: 390, pad: 8 }],
  ['icons-ui', 'S22', 'section:has(#h1) .ico-grid', { maxH: 760 }],
  ['icons-color', 'S22', 'section:has(#h2) .ico-grid', { maxH: 760 }],
  ['icons-items', 'S22', 'section:has(#h3) .ico-grid', {}],
  ['icons-usage', 'S22', 'section:has(#h5)', {}],
  ['notices', 'S20', '#powiadomienia .grid2', { pad: 10 }],
  ['toast', 'S20', '.toasts', { pad: 10, pre: "(()=>{document.querySelector('[data-toast=success]').click();document.querySelector('[data-toast=error]').click();})()" }],
  ['form-controls', 'S20', '#formularze .grid3', { pad: 10, pre: "(()=>{const i=document.getElementById('f-cv');const dt=new DataTransfer();dt.items.add(new File([new Uint8Array(248000)],'CV-Anna-Kowalska.pdf',{type:'application/pdf'}));i.files=dt.files;i.dispatchEvent(new Event('change',{bubbles:true}));})()" }],
  ['form-controls-dark', 'S20', '#formularze .grid3', { pad: 10, pre: "(document.documentElement.setAttribute('data-theme','dark'), (()=>{const i=document.getElementById('f-cv');const dt=new DataTransfer();dt.items.add(new File([new Uint8Array(248000)],'CV-Anna-Kowalska.pdf',{type:'application/pdf'}));i.files=dt.files;i.dispatchEvent(new Event('change',{bubbles:true}));})())" }],
  ['wizard-errors', 'S21', '.wizard', { pad: 10, pre: "document.querySelector('[data-wizard-next]').click()" }],
  ['wizard-warning', 'S21', '.wizard', { pad: 10, pre: "(()=>{const t=document.getElementById('w-title');t.value='Senior Unity Developer';const l=document.getElementById('w-lvl');l.value='Senior';document.getElementById('w-mode').checked=true;document.querySelector('[data-wizard-next]').click();const s=document.getElementById('w-sal');s.focus();document.getElementById('w-desc').focus();})()" }],
  ['modal', 'S20', 'dialog#okno-aplikuj', { pad: 24, pre: "document.querySelector('[data-dialog-open=okno-aplikuj]').click()" }],
  ['menu', 'S20', '#nakladki .row', { pad: 24, padB: 220, pre: "document.querySelector('[aria-controls=menu-oferta]').click()" }],
  ['tooltip', 'S20', '#nakladki .row', { pad: 12, padT: 110, pre: "document.querySelector('[aria-describedby=tip-b2b]').focus()" }],
  ['nav-mobile', 'S20', '.site-header', { w: 390, pre: "document.querySelector('.nav-toggle').click()" }],
  ['drawer-mobile', 'S20', 'dialog#filtry-szuflada', { w: 390, pad: 0, maxH: 700, pre: "document.querySelector('.filters-toggle').click()" }],
  ['selectable', 'S21', '#zaznaczanie', { pad: 8, pre: "(()=>{const r=document.querySelectorAll('#t-oferty [data-select-row]');r[0].click();r[2].click();})()" }],
  ['loading', 'S21', '#ladowanie .two', { pad: 10, pre: "ppProgress(document.getElementById('up-progress'),62)" }],
  ['skeleton-error', 'S20', '#stany .grid3 > .stack:last-child', { pad: 10 }],
  ['charts', 'S21', '#wykresy', { pad: 8 }],
  ['charts-dark', 'S21', '#wykresy', { pad: 8, pre: "document.documentElement.setAttribute('data-theme','dark')" }],
  ['dark-list', 'S20', '#listy .grid2', { pad: 10, pre: "document.documentElement.setAttribute('data-theme','dark')" }],
];
const C = ONLY ? C0.filter(c => ONLY.includes(c[0])) : C0;
(async () => {
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  const meta = [];
  for (const [id, src, sel, o] of C) {
    const p = await b.newPage();
    await p.setViewport({ width: o.w || 1280, height: 900, deviceScaleFactor: 2 });
    await p.goto('file://' + SRC[src], { waitUntil: 'networkidle0' });
    await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}*,*::before,*::after,::backdrop{transition:none!important;animation:none!important}' });
    await p.evaluate(() => document.fonts.ready);
    if (o.pre) { await p.evaluate(o.pre); await new Promise(r => setTimeout(r, 400)); }
    let target = sel;
    if (o.parentSpec) target = '#comp .spec.span2:has(.dither)';
    let el = await p.$(target);
    if (!el && o.fallback) el = await p.$(o.fallback);
    if (!el) { console.log('MISSING', id, sel); await p.close(); continue; }
    // współrzędne w układzie DOKUMENTU (clip w puppeteer liczy się od początku strony)
    const bb = await el.evaluate(e => { const r = e.getBoundingClientRect(); return r.width ? { x: r.left + scrollX, y: r.top + scrollY, width: r.width, height: r.height } : null; });
    if (!bb) { console.log('HIDDEN', id); await p.close(); continue; }
    const pad = o.pad ?? 16;
    const clip = { x: Math.max(0, bb.x - pad), y: Math.max(0, bb.y - pad - (o.padT || 0)), width: Math.min(bb.width + pad * 2 + 6, (o.w || 1280) - Math.max(0, bb.x - pad)), height: Math.min(bb.height + pad * 2 + 6 + (o.padB || 0) + (o.padT || 0), o.maxH || 5000) };
    const file = `${id}.png`;
    await p.screenshot({ path: OUT + file, clip, captureBeyondViewport: true });
    meta.push({ id, source: src, file: SRC[src].replace(R, ''), selector: target, viewport: o.w || 1280, state: o.pre ? 'po interakcji: ' + o.pre.slice(0, 80) : 'domyślny', crop: 'docs/evidence/' + file });
    console.log('ok', id, Math.round(clip.width) + 'x' + Math.round(clip.height));
    await p.close();
  }
  if (!ONLY) fs.writeFileSync(OUT + 'crops.json', JSON.stringify(meta, null, 2)); else { const old = JSON.parse(fs.readFileSync(OUT + 'crops.json')); meta.forEach(m => { const i = old.findIndex(x => x.id === m.id); if (i >= 0) old[i] = m; else old.push(m); }); fs.writeFileSync(OUT + 'crops.json', JSON.stringify(old, null, 2)); }
  await b.close();
})();
