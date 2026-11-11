
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
