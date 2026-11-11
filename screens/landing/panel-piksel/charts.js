/* Panel & Piksel — wykresy pikselowe v1.0 (system v1.8)
 *
 * Rysuje SVG z danych w <script type="application/json"> wewnątrz <figure class="chart" data-chart="…">.
 * Kolory tylko z tokenów (jedna seria: --chart-single; kategorie w segments: --chart-1…4), proste narożniki, cienkie słupki (≤ 24 px), linia 2 px, znaczniki 8 px,
 * siatka 1 px, podpisy selektywnie (maksimum i ostatnia wartość), dymek po najechaniu, tabela danych pod wykresem.
 *
 * <figure class="chart" data-chart="columns">
 *   <figcaption><p class="chart-title">Wyświetlenia ofert</p><p class="chart-sub">ostatnie 7 dni</p></figcaption>
 *   <script type="application/json">{"labels":["pn","wt",…],"values":[120,98,…],"unit":"wyświetleń"}</script>
 * </figure>
 *
 * Rodzaje:
 *   columns  — jedna seria w czasie lub kategoriach (słupki pionowe)
 *   bars     — ranking kategorii (słupki poziome, od największego); długie nazwy
 *   line     — jedna seria w czasie (linia + znacznik ostatniej wartości, celownik po najechaniu)
 *   segments — części całości (do 4 kategorii, jeden pasek 100%, legenda z wartością i %)
 *   spark    — minilinia do kafelka .stat (bez osi, ostatni punkt wyróżniony)
 * Więcej niż 4 kategorie w segments → zsumuj resztę w „Inne”. Dwie miary o różnych skalach → dwa wykresy, nigdy dwie osie Y.
 */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var fmt = function (n) { return Math.round(n).toLocaleString('pl-PL').replace(/ /g, ' '); };
  var compact = function (n) { return n >= 10000 ? (Math.round(n / 100) / 10).toString().replace('.', ',').replace(/,0$/, '') + ' tys.' : fmt(n); };
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function niceMax(v) {
    if (v <= 0) return 1;
    var p = Math.pow(10, Math.floor(Math.log10(v))), m = v / p;
    var n = m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10;
    return n * p;
  }
  function px(n) { return Math.round(n); } // całe piksele — ostre krawędzie

  function setupTip(fig) {
    var plot = fig.querySelector('.chart-plot');
    var tip = plot.querySelector('.chart-tip');
    if (!tip) { tip = document.createElement('div'); tip.className = 'chart-tip'; tip.hidden = true; plot.appendChild(tip); }
    return {
      show: function (x, y, title, value) {
        tip.innerHTML = ''; var t = document.createElement('span'); t.textContent = title; var b = document.createElement('b'); b.textContent = value;
        tip.appendChild(t); tip.appendChild(b); tip.hidden = false;
        var w = plot.clientWidth, half = tip.offsetWidth / 2;
        tip.style.left = Math.max(half, Math.min(w - half, x)) + 'px'; tip.style.top = y + 'px';
      },
      hide: function () { tip.hidden = true; }
    };
  }
  function table(fig, d, kind) {
    if (kind === 'spark' || fig.querySelector('.chart-data')) return;
    var det = document.createElement('details'); det.className = 'chart-data';
    var sum = document.createElement('summary'); sum.textContent = 'Pokaż dane w tabeli'; det.appendChild(sum);
    var wrap = document.createElement('div'); wrap.className = 'table-wrap';
    var t = document.createElement('table'); t.className = 'table';
    var title = fig.querySelector('.chart-title');
    var cap = document.createElement('caption'); cap.className = 'sr-only'; cap.textContent = title ? title.textContent : 'Dane wykresu'; t.appendChild(cap);
    var head = t.createTHead().insertRow();
    [d.labelHeader || 'Pozycja', d.valueHeader || 'Wartość'].forEach(function (h, k) { var th = document.createElement('th'); th.scope = 'col'; th.textContent = h; if (k) th.className = 'num'; head.appendChild(th); });
    var body = t.createTBody();
    d.labels.forEach(function (l, k) { var r = body.insertRow(); r.insertCell().textContent = l; var c = r.insertCell(); c.className = 'num'; c.textContent = fmt(d.values[k]) + (d.unitShort ? ' ' + d.unitShort : ''); });
    wrap.appendChild(t); det.appendChild(wrap); fig.appendChild(det);
  }
  function summaryLabel(d, kind) {
    var max = Math.max.apply(null, d.values), i = d.values.indexOf(max), last = d.values[d.values.length - 1];
    var kinds = { columns: 'Wykres słupkowy', bars: 'Ranking', line: 'Wykres liniowy', segments: 'Udział', spark: 'Trend' };
    if (kind === 'segments') {
      var total = d.values.reduce(function (a, b) { return a + b; }, 0);
      return kinds[kind] + ': ' + d.labels.map(function (l, k) { return l + ' ' + Math.round(d.values[k] / total * 100) + '%'; }).join(', ');
    }
    return kinds[kind] + ': ' + d.labels.length + ' pozycji, najwięcej ' + fmt(max) + ' (' + d.labels[i] + '), ostatnia ' + fmt(last) + (d.unit ? ' ' + d.unit : '');
  }

  function render(fig) {
    var kind = fig.getAttribute('data-chart');
    var src = fig.querySelector('script[type="application/json"]');
    if (!src) return;
    var d = JSON.parse(src.textContent);
    var plot = fig.querySelector('.chart-plot');
    if (!plot) { plot = document.createElement('div'); plot.className = 'chart-plot'; src.parentNode.insertBefore(plot, src); }
    var old = plot.querySelector('svg'); if (old) old.remove();
    var W = Math.max(160, plot.clientWidth || fig.clientWidth - 32);
    var H = kind === 'spark' ? 36 : kind === 'segments' ? 28 : kind === 'bars' ? d.values.length * 32 + 8 : +(fig.getAttribute('data-height') || 200);
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img', 'aria-label': summaryLabel(d, kind) });
    plot.insertBefore(svg, plot.firstChild);
    var tip = kind === 'spark' ? null : setupTip(fig);
    var unit = d.unit ? ' ' + d.unit : '';
    var max = Math.max.apply(null, d.values), maxI = d.values.indexOf(max), lastI = d.values.length - 1;

    if (kind === 'columns' || kind === 'line') {
      var ymax = niceMax(max);
      // margines osi Y wg najdłuższej etykiety (pixel-font 8 px ≈ 8 px na znak)
      var top = 14, bottom = 22, left = Math.max(34, compact(ymax).length * 8 + 10), right = kind === 'line' ? Math.max(40, compact(d.values[d.values.length - 1]).length * 8 + 12) : 8;
      var ph = H - top - bottom, pw = W - left - right;
      var y = function (v) { return px(top + ph - v / ymax * ph); };
      for (var g = 0; g <= 4; g++) { // siatka i oś Y
        var gv = ymax * g / 4, gy = y(gv);
        el('rect', { x: left, y: gy, width: pw, height: 1, style: 'fill:' + (g ? 'var(--chart-grid)' : 'var(--chart-axis)') }, svg);
        var tl = el('text', { x: left - 6, y: gy + 3, 'text-anchor': 'end' }, svg); tl.textContent = compact(gv);
      }
      var band = pw / d.values.length;
      d.labels.forEach(function (l, k) { // etykiety osi X — co druga, gdy ciasno
        if (band < 28 && (lastI - k) % 2) return; // licz od ostatniej — ostatnia etykieta zawsze widoczna, bez nachodzenia
        var t = el('text', { x: px(left + band * k + band / 2), y: H - 6, 'text-anchor': 'middle' }, svg); t.textContent = l;
      });
      if (kind === 'columns') {
        var bw = Math.max(4, Math.min(24, px(band * 0.6)));
        d.values.forEach(function (v, k) {
          var x = px(left + band * k + (band - bw) / 2), yy = y(v);
          el('rect', { x: x, y: yy, width: bw, height: Math.max(0, top + ph - yy), style: 'fill:var(--chart-single)' }, svg);
          if (k === maxI || k === lastI) { var t = el('text', { x: x + bw / 2, y: yy - 4, 'text-anchor': 'middle', class: 'lbl-strong' }, svg); t.textContent = compact(v); }
          var hit = el('rect', { x: px(left + band * k), y: top, width: px(band), height: ph, class: 'hit' }, svg);
          hit.addEventListener('mouseenter', function () { tip.show(x + bw / 2, yy, d.labels[k], fmt(v) + unit); });
          hit.addEventListener('mouseleave', tip.hide);
        });
      } else {
        var pts = d.values.map(function (v, k) { return [px(left + band * k + band / 2), y(v)]; });
        el('polygon', { points: pts.map(function (p) { return p.join(','); }).join(' ') + ' ' + pts[lastI][0] + ',' + (top + ph) + ' ' + pts[0][0] + ',' + (top + ph), style: 'fill:var(--chart-single);opacity:.1' }, svg);
        el('polyline', { points: pts.map(function (p) { return p.join(','); }).join(' '), style: 'fill:none;stroke:var(--chart-single);stroke-width:2;stroke-linejoin:miter', 'shape-rendering': 'auto' }, svg);
        var end = pts[lastI];
        el('rect', { x: end[0] - 4, y: end[1] - 4, width: 8, height: 8, style: 'fill:var(--chart-single);stroke:var(--surface);stroke-width:2' }, svg);
        var et = el('text', { x: end[0] + 8, y: end[1] + 3, class: 'lbl-strong' }, svg); et.textContent = compact(d.values[lastI]);
        var cross = el('rect', { x: 0, y: top, width: 1, height: ph, style: 'fill:var(--chart-axis);visibility:hidden' }, svg);
        var dot = el('rect', { x: 0, y: 0, width: 8, height: 8, style: 'fill:var(--chart-single);stroke:var(--surface);stroke-width:2;visibility:hidden' }, svg);
        var area = el('rect', { x: left, y: top, width: pw, height: ph, class: 'hit' }, svg);
        area.addEventListener('mousemove', function (e) {
          var r = svg.getBoundingClientRect(), mx = (e.clientX - r.left) * (W / r.width);
          var k = Math.max(0, Math.min(lastI, Math.floor((mx - left) / band)));
          cross.setAttribute('x', pts[k][0]); cross.style.visibility = 'visible';
          dot.setAttribute('x', pts[k][0] - 4); dot.setAttribute('y', pts[k][1] - 4); dot.style.visibility = 'visible';
          tip.show(pts[k][0] * r.width / W, pts[k][1] * r.height / H, d.labels[k], fmt(d.values[k]) + unit);
        });
        area.addEventListener('mouseleave', function () { cross.style.visibility = dot.style.visibility = 'hidden'; tip.hide(); });
      }
    } else if (kind === 'bars') {
      var order = d.values.map(function (v, k) { return k; }).sort(function (a, b) { return d.values[b] - d.values[a]; });
      var lw = Math.min(220, px(W * 0.45)), vw = 56, bw2 = W - lw - vw, row = 32, bh = 16;
      order.forEach(function (k, r) {
        var v = d.values[k], yy = r * row + 8, len = Math.max(2, px(v / max * bw2));
        var lab = el('text', { x: 0, y: yy + 12, class: 'lbl-cat' }, svg); lab.textContent = d.labels[k];
        lab.setAttribute('style', 'font:600 13px var(--font-sans);fill:var(--ink)');
        el('rect', { x: lw, y: yy, width: len, height: bh, style: 'fill:var(--chart-single)' }, svg);
        var vt = el('text', { x: lw + len + 6, y: yy + 12, class: 'lbl-strong' }, svg); vt.textContent = compact(v);
        var hit = el('rect', { x: 0, y: yy - 6, width: W, height: row, class: 'hit' }, svg);
        hit.addEventListener('mouseenter', function () { tip.show(lw + len / 2, yy, d.labels[k], fmt(v) + unit); });
        hit.addEventListener('mouseleave', tip.hide);
      });
      // nazwy dłuższe niż kolumna: przytnij z wielokropkiem, pełna nazwa w dymku i tabeli
      Array.prototype.forEach.call(svg.querySelectorAll('.lbl-cat'), function (t) {
        var s = t.textContent; while (t.getComputedTextLength && t.getComputedTextLength() > lw - 10 && s.length > 3) { s = s.slice(0, -1); t.textContent = s + '…'; }
      });
    } else if (kind === 'segments') {
      var total = d.values.reduce(function (a, b) { return a + b; }, 0), x0 = 0, gap = 2;
      d.values.forEach(function (v, k) {
        var w = (W - gap * (d.values.length - 1)) * v / total, xx = px(x0);
        el('rect', { x: xx, y: 0, width: Math.max(1, px(x0 + w) - xx), height: H, style: 'fill:var(--chart-' + (k + 1) + ')' }, svg);
        var hit = el('rect', { x: xx, y: 0, width: Math.max(1, px(w)), height: H, class: 'hit' }, svg);
        var mid = xx + w / 2;
        hit.addEventListener('mouseenter', function () { tip.show(mid, 0, d.labels[k], fmt(v) + unit + ' · ' + Math.round(v / total * 100) + '%'); });
        hit.addEventListener('mouseleave', tip.hide);
        x0 += w + gap;
      });
      if (!fig.querySelector('.chart-legend')) {
        var ul = document.createElement('ul'); ul.className = 'chart-legend';
        d.labels.forEach(function (l, k) {
          var li = document.createElement('li');
          li.innerHTML = '<span class="swatch" style="--c:var(--chart-' + (k + 1) + ')" aria-hidden="true"></span><span></span><span class="num"></span>';
          li.children[1].textContent = l; li.children[2].textContent = Math.round(d.values[k] / total * 100) + '%';
          ul.appendChild(li);
        });
        plot.parentNode.insertBefore(ul, plot.nextSibling);
      }
    } else if (kind === 'spark') {
      var mn = Math.min.apply(null, d.values), span = (max - mn) || 1, step = (W - 10) / lastI;
      var sp = d.values.map(function (v, k) { return [px(k * step + 1), px(4 + (H - 8) - (v - mn) / span * (H - 8))]; });
      el('polyline', { points: sp.map(function (p) { return p.join(','); }).join(' '), style: 'fill:none;stroke:var(--ink-3);stroke-width:2', 'shape-rendering': 'auto' }, svg);
      el('rect', { x: sp[lastI][0] - 3, y: sp[lastI][1] - 3, width: 6, height: 6, style: 'fill:var(--chart-single)' }, svg);
      svg.setAttribute('aria-hidden', 'true'); svg.removeAttribute('role');
    }
    table(fig, d, kind);
  }

  function initAll(root) {
    var figs = Array.prototype.slice.call((root || document).querySelectorAll('.chart[data-chart], .chart-spark[data-chart]'));
    figs.forEach(function (f) {
      render(f);
      if (window.ResizeObserver && !f.__ppRO) {
        var w = f.clientWidth;
        f.__ppRO = new ResizeObserver(function () { if (Math.abs(f.clientWidth - w) > 4) { w = f.clientWidth; render(f); } });
        f.__ppRO.observe(f);
      }
    });
  }
  window.ppCharts = { initAll: initAll, render: render };
  function start() { (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(function () { initAll(); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
