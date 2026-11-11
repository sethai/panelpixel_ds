/* Panel & Piksel — sortowanie, filtry, „Pokaż więcej” i przełączniki dla list kart v1.3
 *
 * Działa na atrybutach data-*, bez zależności. Kontrakt:
 *
 * LISTA       <div data-list="oferty"> … <article data-item …> … </div>
 *   wartości  data-sort-<klucz>="…"        liczba albo tekst do sortowania (np. data-sort-date="20261109")
 *             data-f-<nazwa>="a b c"       tokeny faset do filtrów (np. data-f-tryb="zdalnie")
 *             data-n-<nazwa>="od do"       zakres liczbowy (np. data-n-salary="20000 27000"); brak = brak danych
 *
 * SORTOWANIE  <div class="tabs" role="group" aria-label="Sortuj oferty" data-sort-for="oferty">
 *               <button type="button" aria-pressed="true" data-sort-key="date" data-sort-dir="desc">Najnowsze</button>
 *             (v1.6: grupa przycisków aria-pressed; starsze role="tab" + aria-selected nadal działają)
 *             data-sort-key="order" = kolejność z HTML (np. „Trafność”, „Popularne”).
 *
 * FILTRY      <form data-filter-for="oferty"> (filtruje na żywo, przy każdej zmianie)
 *               <input type="checkbox" name="tryb" value="zdalnie">  — ta sama nazwa: LUB, różne nazwy: I
 *               <input type="checkbox" data-require="salary">        — tylko pozycje z data-n-salary
 *               <input type="number" data-min="salary"> / data-max="salary"
 *               <input type="search" data-search>                    — szuka w tekście pozycji (wszystkie słowa)
 *               <button type="submit">Pokaż <span data-count-for="oferty" data-count-forms="ofertę|oferty|ofert"></span></button>
 *             <span class="opt-n"></span> w etykiecie checkboxa — (v1.3) skrypt wpisuje liczbę pozycji, które zostaną po zaznaczeniu
 *               tej opcji (przy pozostałych filtrach); opcja z 0 dostaje .is-zero (wyszarzona, ale klikalna)
 *             .range z data-min i data-max — (v1.3) „Od” większe niż „Do” → komunikat .field-error pod zakresem
 *             [data-count-for] — liczba widocznych pozycji z polską odmianą (formy: 1|2–4|5+)
 *             [data-empty-for] — element pokazywany, gdy nic nie pasuje
 *             [data-active-for] — tu pojawią się chipy aktywnych filtrów; [data-clear-for] — czyści filtry
 *
 * POKAŻ WIĘCEJ  <div data-list="oferty" data-page-size="6"> + <div class="load-more" data-more-for="oferty">
 *               <p class="load-more-info"></p><button class="btn btn-secondary" type="button">Pokaż więcej</button></div>
 *             (v1.2) pokazuje pierwsze N pasujących pozycji, przycisk dokłada kolejne N; filtr/sortowanie wraca do pierwszej strony.
 *
 * PRZEŁĄCZNIK <button class="btn btn-secondary" aria-pressed="false" data-label-on="Zapisano" data-label-off="Zapisz ofertę">
 *
 * Zmiany są ogłaszane czytnikom ekranu przez niewidoczny region aria-live.
 */
(function () {
  'use strict';
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  function plural(n, forms) {
    var f = (forms || '').split('|');
    if (f.length < 3) return String(n);
    var form = n === 1 ? f[0] : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? f[1] : f[2];
    return n + ' ' + form;
  }
  function val(item, key) {
    if (key === 'order') return +item.getAttribute('data-pp-order');
    var v = item.getAttribute('data-sort-' + key);
    if (v === null || v === '') return null;
    return isNaN(+v) ? v.toLowerCase() : +v;
  }
  function range(item, name) {
    var v = item.getAttribute('data-n-' + name);
    if (!v) return null;
    var p = v.trim().split(/\s+/).map(Number);
    return [p[0], p.length > 1 ? p[1] : p[0]];
  }
  function announcer(list) {
    var live = document.createElement('span');
    live.className = 'sr-only';
    live.setAttribute('aria-live', 'polite');
    list.parentNode.insertBefore(live, list);
    return live;
  }

  function setup(list) {
    var id = list.getAttribute('data-list');
    var items = $$('[data-item]', list);
    items.forEach(function (it, i) { it.setAttribute('data-pp-order', i); });
    var live = announcer(list);
    var counts = $$('[data-count-for="' + id + '"]');
    var empties = $$('[data-empty-for="' + id + '"]');
    var actives = $$('[data-active-for="' + id + '"]');
    var pageSize = +list.getAttribute('data-page-size') || 0, page = 1;
    var mores = $$('[data-more-for="' + id + '"]');
    items.forEach(function (it) { it.__ppMatch = !it.hidden; });
    // „Pokaż więcej”: widoczne tylko pierwsze page × pageSize pasujące pozycje, w bieżącej kolejności DOM
    function limit(focusFrom) {
      var parent = items[0] && items[0].parentNode;
      var ordered = parent ? Array.prototype.filter.call(parent.children, function (c) { return items.indexOf(c) !== -1; }) : items;
      var matched = ordered.filter(function (it) { return it.__ppMatch; });
      var cap = pageSize ? page * pageSize : Infinity;
      ordered.forEach(function (it) { it.hidden = !it.__ppMatch; });
      matched.forEach(function (it, k) { if (k >= cap) it.hidden = true; });
      var shown = Math.min(matched.length, cap);
      mores.forEach(function (m) {
        m.hidden = shown >= matched.length;
        var info = m.querySelector('.load-more-info');
        if (info) info.textContent = shown + ' z ' + matched.length;
        var btn = m.querySelector('button');
        if (btn) btn.textContent = 'Pokaż więcej (' + Math.min(pageSize, matched.length - shown) + ')';
      });
      if (focusFrom != null && matched[focusFrom]) { var f = matched[focusFrom]; f.setAttribute('tabindex', '-1'); f.focus(); }
    }
    mores.forEach(function (m) {
      var btn = m.querySelector('button');
      if (btn) btn.addEventListener('click', function () {
        var first = page * pageSize; page++; limit(first);
        live.textContent = 'Dodano kolejne pozycje';
      });
    });

    // ---------- sortowanie ----------
    function sortBy(key, dir) {
      var parent = items[0] && items[0].parentNode;
      if (!parent) return;
      // miejsce wstawienia liczymy od pozycji, która JEST TERAZ ostatnia w DOM (po poprzednim sortowaniu kolejność jest inna)
      var inDom = Array.prototype.filter.call(parent.children, function (c) { return items.indexOf(c) !== -1; });
      var anchor = inDom[inDom.length - 1].nextSibling;
      items.slice().sort(function (a, b) {
        var x = val(a, key), y = val(b, key);
        if (x === null && y === null) return +a.getAttribute('data-pp-order') - +b.getAttribute('data-pp-order');
        if (x === null) return 1;            // brak wartości zawsze na końcu
        if (y === null) return -1;
        var r = (typeof x === 'number' && typeof y === 'number') ? x - y : String(x).localeCompare(String(y), 'pl');
        if (r === 0) r = +a.getAttribute('data-pp-order') - +b.getAttribute('data-pp-order');
        return dir === 'desc' && key !== 'order' ? -r : r;
      }).forEach(function (it) { parent.insertBefore(it, anchor); });
      page = 1; limit();
    }
    $$('[data-sort-for="' + id + '"]').forEach(function (group) {
      var btns = $$('[data-sort-key]', group);
      function select(btn, announce) {
        btns.forEach(function (b) {
          var on = b === btn;
          if (b.getAttribute('role') === 'tab') { b.setAttribute('aria-selected', on); b.tabIndex = on ? 0 : -1; }
          else b.setAttribute('aria-pressed', on);
        });
        sortBy(btn.getAttribute('data-sort-key'), btn.getAttribute('data-sort-dir') || 'asc');
        if (announce) live.textContent = 'Posortowano: ' + btn.textContent.trim();
      }
      btns.forEach(function (b, i) {
        b.addEventListener('click', function () { select(b, true); });
        b.addEventListener('keydown', function (e) {
          var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
          if (!k) return;
          var n = btns[(i + k + btns.length) % btns.length]; n.focus(); select(n, true); e.preventDefault();
        });
      });
      var initial = btns.filter(function (b) { return b.getAttribute('aria-selected') === 'true' || b.getAttribute('aria-pressed') === 'true'; })[0];
      if (initial) select(initial, false);
    });

    // ---------- filtry ----------
    var forms = $$('[data-filter-for="' + id + '"]');
    function apply(announce) {
      var groups = {}, require = [], mins = {}, maxs = {}, words = [], chips = [];
      forms.forEach(function (f) {
        $$('input', f).forEach(function (inp) {
          if (inp.type === 'checkbox' && inp.checked) {
            var lab = inp.closest('label'), label = lab ? Array.prototype.filter.call(lab.childNodes, function (n) { return !(n.classList && n.classList.contains('opt-n')); }).map(function (n) { return n.textContent; }).join('') : inp.value;
            label = label.replace(/\s+\d+\s*$/, '').trim();
            if (inp.hasAttribute('data-require')) require.push(inp.getAttribute('data-require'));
            else if (inp.name) (groups[inp.name] = groups[inp.name] || []).push(inp.value.toLowerCase());
            chips.push({ input: inp, label: label });
          } else if (inp.hasAttribute('data-min') && inp.value !== '') mins[inp.getAttribute('data-min')] = +inp.value;
          else if (inp.hasAttribute('data-max') && inp.value !== '') maxs[inp.getAttribute('data-max')] = +inp.value;
          else if (inp.hasAttribute('data-search') && inp.value.trim()) words = words.concat(inp.value.toLowerCase().trim().split(/\s+/));
        });
      });
      // zakres „od” > „do” — pokaż błąd i nie stosuj zakresu (zamiast cichego zera wyników)
      forms.forEach(function (f) {
        $$('.range', f).forEach(function (rg) {
          var lo = rg.querySelector('[data-min]'), hi = rg.querySelector('[data-max]');
          if (!lo || !hi) return;
          var bad = lo.value !== '' && hi.value !== '' && +lo.value > +hi.value;
          var msg = rg.nextElementSibling && rg.nextElementSibling.classList.contains('field-error') ? rg.nextElementSibling : null;
          if (bad && !msg) { msg = document.createElement('p'); msg.className = 'field-error'; msg.id = (lo.id || 'pp-range') + '-err'; rg.parentNode.insertBefore(msg, rg.nextSibling); }
          if (msg) { msg.hidden = !bad; msg.textContent = bad ? '„Od” nie może być większe niż „Do”. Zamień wartości albo popraw jedną z nich.' : ''; }
          [lo, hi].forEach(function (i) { if (bad) { i.setAttribute('aria-invalid', 'true'); i.setAttribute('aria-describedby', msg.id); } else { i.removeAttribute('aria-invalid'); } });
          if (bad) { delete mins[lo.getAttribute('data-min')]; delete maxs[hi.getAttribute('data-max')]; }
        });
      });
      function passes(it, skipGroup, extra) {
        var g = groups;
        if (extra && extra.name) { g = {}; for (var k in groups) g[k] = groups[k]; g[extra.name] = [extra.value]; }
        var ok = Object.keys(g).every(function (name) {
          if (name === skipGroup && !extra) return true;
          var tokens = (it.getAttribute('data-f-' + name) || '').toLowerCase().split(/\s+/);
          return g[name].some(function (v) { return tokens.indexOf(v) !== -1; });
        });
        var req = extra && extra.require ? require.concat([extra.require]) : require;
        ok = ok && req.every(function (n) { return range(it, n) !== null; });
        Object.keys(mins).forEach(function (n) { var r = range(it, n); if (ok && r && r[1] < mins[n]) ok = false; });
        Object.keys(maxs).forEach(function (n) { var r = range(it, n); if (ok && r && r[0] > maxs[n]) ok = false; });
        if (ok && words.length) {
          var text = it.textContent.toLowerCase();
          ok = words.every(function (w) { return text.indexOf(w) !== -1; });
        }
        return ok;
      }
      var shown = 0;
      items.forEach(function (it) {
        var ok = passes(it);
        it.__ppMatch = ok;
        if (ok) shown++;
      });
      // liczby przy opcjach: ile pozycji zostanie po zaznaczeniu tej opcji (ta sama grupa = LUB, więc grupa liczona bez siebie)
      forms.forEach(function (f) {
        $$('input[type="checkbox"]', f).forEach(function (inp) {
          var lab = inp.closest('label'), out = lab && lab.querySelector('.opt-n');
          if (!out) return;
          var n = 0;
          if (inp.hasAttribute('data-require')) items.forEach(function (it) { if (passes(it, null, { require: inp.getAttribute('data-require') })) n++; });
          else if (inp.name) items.forEach(function (it) { if (passes(it, inp.name, { name: inp.name, value: inp.value.toLowerCase() })) n++; });
          out.textContent = n;
          lab.classList.toggle('is-zero', n === 0 && !inp.checked);
        });
      });
      page = 1; limit();
      counts.forEach(function (c) { c.textContent = plural(shown, c.getAttribute('data-count-forms')); });
      empties.forEach(function (e) { e.hidden = shown > 0; });
      actives.forEach(function (box) {
        box.innerHTML = '';
        chips.forEach(function (ch) {
          var b = document.createElement('button');
          b.type = 'button'; b.className = 'chip'; b.textContent = ch.label + ' ×';
          b.setAttribute('aria-label', 'Usuń filtr: ' + ch.label);
          b.addEventListener('click', function () { ch.input.checked = false; apply(true); });
          box.appendChild(b);
        });
        box.hidden = !chips.length;
      });
      if (announce) live.textContent = 'Wyniki: ' + plural(shown, (counts[0] && counts[0].getAttribute('data-count-forms')) || 'pozycja|pozycje|pozycji');
    }
    forms.forEach(function (f) {
      f.addEventListener('change', function () { apply(true); });
      f.addEventListener('input', function (e) { if (e.target.type !== 'checkbox') apply(true); });
      f.addEventListener('submit', function (e) {
        e.preventDefault(); apply(true);
        var target = list.closest('section') || list;
        target.scrollIntoView({ block: 'start' });
      });
    });
    $$('[data-clear-for="' + id + '"]').forEach(function (c) {
      c.addEventListener('click', function (e) {
        e.preventDefault();
        forms.forEach(function (f) { $$('input', f).forEach(function (i) { if (i.type === 'checkbox') i.checked = false; else i.value = ''; }); });
        apply(true);
      });
    });
    if (forms.length) apply(false); else limit();
  }

  function toggles(root) {
    $$('button[aria-pressed][data-label-on]', root).forEach(function (b) {
      if (b.__ppToggle) return; b.__ppToggle = true;
      function label() { var on = b.getAttribute('aria-pressed') === 'true'; var t = b.getAttribute(on ? 'data-label-on' : 'data-label-off'); if (t) b.lastChild.nodeType === 3 ? (b.lastChild.textContent = t) : (b.textContent = t); }
      b.addEventListener('click', function () { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); label(); });
      label();
    });
  }

  function initAll(root) {
    $$('[data-list]', root).forEach(function (l) { if (!l.__ppList) { l.__ppList = true; setup(l); } });
    toggles(root);
  }
  window.ppListControls = { initAll: initAll };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
