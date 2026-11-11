/* Panel & Piksel — sortowanie tabel v1.0
 *
 * Każdy <button class="sort"> w nagłówku <th> tabeli dostaje działające sortowanie wierszy <tbody>.
 * - Kierunek trzyma <th aria-sort="ascending|descending|none">; system rysuje strzałkę ▲/▼.
 * - Pierwsze kliknięcie: kolumny liczbowe (<th class="num">) malejąco, tekstowe rosnąco (zmiana: data-sort-first="descending"
 *   na <th>, np. dla rang/pakietów); kolejne kliknięcia odwracają.
 * - Wartość komórki: atrybut data-sort-value (gdy podany); w kolumnach <th class="num"> data dd.mm.rrrr
 *   albo liczba (spacje i jednostki są pomijane); w pozostałych — tekst (porównanie po polsku). Puste i „—” zawsze na końcu.
 * - Kliknąć można całą komórkę nagłówka (CSS systemu rozciąga przycisk).
 * - Zmianę ogłasza czytnikom ekranu przez niewidoczny region aria-live.
 * - Tabele, których wiersze buduje kod aplikacji (np. paginacja z danych), oznacz data-sort-manual —
 *   skrypt je pominie, a sortowanie zrób na danych i ustaw aria-sort samodzielnie.
 */
(function () {
  'use strict';

  function cellValue(td, numeric) {
    if (!td) return '';
    var raw = td.getAttribute('data-sort-value');
    if (raw !== null) return isNaN(+raw) ? raw.toLowerCase() : +raw;
    var t = td.textContent.replace(/\s+/g, ' ').trim();
    if (t === '' || /^[—–\-]+$/.test(t)) return null;   // brak danych
    if (!numeric) return t.toLowerCase();                 // kolumna tekstowa: tylko tekst
    var d = t.match(/(\d{1,2})\.(\d{1,2})\.(\d{4})/);
    if (d) return +(d[3] + ('0' + d[2]).slice(-2) + ('0' + d[1]).slice(-2));
    var n = t.replace(/[\s  ]/g, '').match(/^[^\d\-]*(-?\d+(?:[.,]\d+)?)/);
    if (n) return parseFloat(n[1].replace(',', '.'));
    return t.toLowerCase();
  }

  function compare(a, b) {
    if (typeof a === 'number' && typeof b === 'number') return a - b;
    if (typeof a === 'number') return -1;   // liczby przed tekstem
    if (typeof b === 'number') return 1;
    return String(a).localeCompare(String(b), 'pl');
  }

  function init(table) {
    if (!table.tHead || !table.tBodies.length || table.__ppSort) return;
    table.__ppSort = true;
    var headers = Array.prototype.slice.call(table.tHead.rows[table.tHead.rows.length - 1].cells);
    var live = document.createElement('span');
    live.className = 'sr-only';
    live.setAttribute('aria-live', 'polite');
    table.parentNode.insertBefore(live, table.nextSibling);

    headers.forEach(function (th, index) {
      var btn = th.querySelector('.sort');
      if (!btn) return;
      btn.removeAttribute('aria-sort'); // aria-sort należy do <th>, nie do przycisku
      if (!th.hasAttribute('aria-sort')) th.setAttribute('aria-sort', 'none');
      btn.addEventListener('click', function () {
        var current = th.getAttribute('aria-sort');
        var numeric = th.classList.contains('num');
        var first = th.getAttribute('data-sort-first') || (numeric ? 'descending' : 'ascending');
        var dir = current === 'none' ? first
                : current === 'descending' ? 'ascending' : 'descending';
        headers.forEach(function (h) { if (h !== th && h.querySelector('.sort')) h.setAttribute('aria-sort', 'none'); });
        th.setAttribute('aria-sort', dir);
        var body = table.tBodies[0];
        var rows = Array.prototype.slice.call(body.rows);
        rows.forEach(function (r, i) { if (!r.hasAttribute('data-pp-order')) r.setAttribute('data-pp-order', i); });
        rows.sort(function (r1, r2) {
          var x = cellValue(r1.cells[index], numeric), y = cellValue(r2.cells[index], numeric);
          if (x === null && y === null) return +r1.getAttribute('data-pp-order') - +r2.getAttribute('data-pp-order');
          if (x === null) return 1;               // puste zawsze na końcu, w obu kierunkach
          if (y === null) return -1;
          var res = compare(x, y);
          if (res === 0) res = +r1.getAttribute('data-pp-order') - +r2.getAttribute('data-pp-order');
          return dir === 'ascending' ? res : -res;
        });
        rows.forEach(function (r) { body.appendChild(r); });
        live.textContent = 'Posortowano: ' + btn.textContent.trim() + (dir === 'ascending' ? ', rosnąco' : ', malejąco');
      });
    });
  }

  function initAll(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll('table'), function (t) {
      if (t.querySelector('th .sort') && !t.hasAttribute('data-sort-manual')) init(t);
    });
  }

  window.ppTableSort = { init: init, initAll: initAll };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
