/* Panel & Piksel — formularze, nakładki i nawigacja mobilna v1.1 (system v1.8)
 *
 * Bez zależności, działa na atrybutach. Kontrakt:
 *
 * PRZEŁĄCZNIK   <button class="switch" type="button" role="switch" aria-checked="false">
 *                 <span class="switch-track" aria-hidden="true"></span>Powiadomienia e-mail<span class="switch-state" aria-hidden="true">WYŁ</span></button>
 * LICZNIK       <div class="stepper"><button type="button" data-step="-1" aria-label="Mniej">…</button>
 *                 <input type="number" min="0" max="9" value="1" aria-label="Liczba sztuk"><button type="button" data-step="1" aria-label="Więcej">…</button></div>
 * ZNAKI         <textarea maxlength="500" data-count="opis-licznik"> + <p class="field-count" id="opis-licznik"></p>
 * PLIK          <label class="upload" data-max-mb="5"><input type="file" accept=".pdf,.doc,.docx" aria-describedby="…"> …</label>
 *                 <ul class="file-list" data-files-for="ID-inputa"></ul>  (+ opcjonalnie <p class="field-error" data-upload-error hidden>)
 * OKNO          <button data-dialog-open="id-okna"> … <dialog class="modal" id="id-okna" aria-labelledby="…"> … <button data-dialog-close>
 * SZUFLADA      <dialog class="drawer" id="filtry-szuflada" data-drawer-source="filters-form"> … <div data-drawer-slot></div>
 *                 formularz: <form id="filters-form" data-drawer-form …> (poniżej 900 px ukryty w stronie, widoczny w szufladzie)
 *                 Formularz o id z data-drawer-source jest przenoszony do szuflady na czas otwarcia (te same pola, ten sam stan).
 * MENU          <div class="menu"><button class="icon-btn" aria-expanded="false" aria-controls="m1" aria-label="Więcej akcji">…</button>
 *                 <ul class="menu-list" id="m1" hidden><li><button type="button">Edytuj</button></li>…</ul></div>
 * PODPOWIEDŹ    <span class="tip"><button class="icon-btn" type="button" aria-describedby="t1">…</button><span class="tip-body" role="tooltip" id="t1">…</span></span>
 * NAWIGACJA     <button class="icon-btn nav-toggle" aria-expanded="false" aria-controls="nav">…</button> <nav class="site-nav" id="nav" data-collapsible>
 * POWIADOMIENIE <button data-dismiss> wewnątrz .notice zamyka je;  ppToast({ status: 'success', title: 'Zapisano', text: '…' })
 * WALIDACJA     <form data-validate> — required, type=email/url/number, minlength, pattern, min/max, data-match="id";
 *                 własne komunikaty: data-msg-required="…" (też -email, -minlength, -pattern, -min, -max, -match);
 *                 ostrzeżenie (nie blokuje): data-warn-empty="Oferty bez widełek dostają mniej odpowiedzi."
 *                 Błędy po opuszczeniu pola i przy wysłaniu; podsumowanie .error-summary na górze z linkami do pól.
 *                 Po poprawnym wysłaniu zdarzenie 'pp:valid' (formularz bez action nie przeładowuje strony).
 * KROKI         <form data-validate data-wizard> + <ol class="steps-progress"><li><span class="step-label">…</span></li>…</ol>
 *                 + <section class="wizard-step">…</section> × N + <div class="wizard-nav"><button data-wizard-prev>
 *                 <button data-wizard-next> <button type="submit"></div> — „Dalej” sprawdza tylko bieżący krok.
 * WYBÓR WIERSZY <table id="t" data-selectable> + th: <input type="checkbox" data-select-all aria-label="Zaznacz wszystkie">
 *                 + td: <input type="checkbox" data-select-row aria-label="Zaznacz: …"> + <div class="bulk-bar" data-bulk-for="t" hidden>
 *                 <span class="bulk-count" data-forms="ofertę|oferty|ofert"></span> … <button data-bulk-clear>Odznacz</button></div>
 * POSTĘP        <div class="progress"><div class="progress-label"><span id="pl">Wysyłanie CV</span><span class="num">0%</span></div>
 *                 <div class="progress-track" role="progressbar" aria-labelledby="pl" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
 *                 <div class="progress-fill"></div></div></div>  →  ppProgress(el, 40) / ppProgress(el, null) = nieokreślony
 */
(function () {
  'use strict';
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var ICON = { info: 'i-info', success: 'i-success', warning: 'i-warning', error: 'i-error' };

  // ---------- przełącznik ----------
  function switches(root) {
    $$('.switch[role="switch"]', root).forEach(function (sw) {
      if (sw.__pp) return; sw.__pp = true;
      var state = sw.querySelector('.switch-state');
      function paint() { if (state) state.textContent = sw.getAttribute('aria-checked') === 'true' ? 'WŁ' : 'WYŁ'; }
      sw.addEventListener('click', function () { sw.setAttribute('aria-checked', sw.getAttribute('aria-checked') === 'true' ? 'false' : 'true'); paint(); });
      paint();
    });
  }

  // ---------- licznik −/+ ----------
  function steppers(root) {
    $$('.stepper', root).forEach(function (st) {
      if (st.__pp) return; st.__pp = true;
      var input = st.querySelector('input');
      function clamp(v) {
        var min = input.min === '' ? -Infinity : +input.min, max = input.max === '' ? Infinity : +input.max;
        return Math.min(max, Math.max(min, isNaN(v) ? (min > -Infinity ? min : 0) : v));
      }
      function paint() {
        $$('[data-step]', st).forEach(function (b) {
          var d = +b.getAttribute('data-step'), v = +input.value;
          var off = (d < 0 && input.min !== '' && v <= +input.min) || (d > 0 && input.max !== '' && v >= +input.max);
          if (off) b.setAttribute('aria-disabled', 'true'); else b.removeAttribute('aria-disabled');
        });
      }
      $$('[data-step]', st).forEach(function (b) {
        b.addEventListener('click', function () {
          if (b.getAttribute('aria-disabled') === 'true') return;
          input.value = clamp(+input.value + +b.getAttribute('data-step'));
          input.dispatchEvent(new Event('change', { bubbles: true })); paint();
        });
      });
      input.addEventListener('change', function () { input.value = clamp(+input.value); paint(); });
      paint();
    });
  }

  // ---------- licznik znaków ----------
  function counters(root) {
    $$('[data-count][maxlength]', root).forEach(function (f) {
      if (f.__pp) return; f.__pp = true;
      var out = document.getElementById(f.getAttribute('data-count'));
      if (!out) return;
      out.setAttribute('aria-live', 'polite');
      var max = +f.getAttribute('maxlength'), timer;
      function paint(announce) {
        var left = max - f.value.length;
        out.classList.toggle('is-over', left <= Math.max(10, max * 0.05));
        clearTimeout(timer);
        // aktualizacja tekstu z opóźnieniem — czytnik nie ogłasza każdego znaku
        timer = setTimeout(function () { out.textContent = f.value.length + ' / ' + max; }, announce ? 600 : 0);
      }
      f.addEventListener('input', function () { paint(true); });
      paint(false);
    });
  }

  // ---------- wgrywanie plików ----------
  function fmtSize(b) { return b >= 1048576 ? (b / 1048576).toFixed(1).replace('.', ',') + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB'; }
  function uploads(root) {
    $$('.upload', root).forEach(function (zone) {
      if (zone.__pp) return; zone.__pp = true;
      var input = zone.querySelector('input[type="file"]');
      var list = document.querySelector('[data-files-for="' + input.id + '"]');
      var err = zone.parentNode.querySelector('[data-upload-error]');
      var maxMb = +(zone.getAttribute('data-max-mb') || 0);
      var files = [];
      function render() {
        if (!list) return;
        list.innerHTML = '';
        files.forEach(function (f, i) {
          var li = document.createElement('li');
          li.innerHTML = '<span class="sprite s-scroll" aria-hidden="true"></span><span class="file-name"></span><span class="file-size"></span>' +
            '<button class="icon-btn" type="button"><span class="icon i-trash" aria-hidden="true"></span></button>';
          li.querySelector('.file-name').textContent = f.name;
          li.querySelector('.file-size').textContent = fmtSize(f.size);
          var del = li.querySelector('button');
          del.setAttribute('aria-label', 'Usuń plik: ' + f.name);
          del.addEventListener('click', function () { files.splice(i, 1); render(); input.focus(); });
          list.appendChild(li);
        });
      }
      function add(fileList) {
        var bad = [];
        Array.prototype.forEach.call(fileList, function (f) {
          var okType = !input.accept || input.accept.split(',').some(function (a) { a = a.trim().toLowerCase(); return a && (f.name.toLowerCase().slice(-a.length) === a || f.type === a); });
          var okSize = !maxMb || f.size <= maxMb * 1048576;
          if (okType && okSize) { if (input.multiple) files.push(f); else files = [f]; }
          else bad.push(f.name + (okType ? ' — plik większy niż ' + maxMb + ' MB' : ' — nieobsługiwany format'));
        });
        zone.classList.toggle('is-error', bad.length > 0);
        if (err) { err.hidden = !bad.length; err.textContent = bad.length ? 'Nie dodano: ' + bad.join('; ') + '.' : ''; }
        input.setAttribute('aria-invalid', bad.length ? 'true' : 'false');
        render();
      }
      input.addEventListener('change', function () { add(input.files); });
      ['dragenter', 'dragover'].forEach(function (t) { zone.addEventListener(t, function (e) { e.preventDefault(); zone.classList.add('is-drag'); }); });
      ['dragleave', 'drop'].forEach(function (t) { zone.addEventListener(t, function () { zone.classList.remove('is-drag'); }); });
      zone.addEventListener('drop', function (e) { e.preventDefault(); add(e.dataTransfer.files); });
    });
  }

  // ---------- okno i szuflada (natywny <dialog>: pułapka fokusu, Esc, powrót fokusu) ----------
  function dialogs(root) {
    $$('[data-dialog-open]', root).forEach(function (btn) {
      if (btn.__pp) return; btn.__pp = true;
      btn.addEventListener('click', function () {
        var d = document.getElementById(btn.getAttribute('data-dialog-open'));
        if (!d || d.open) return;
        var srcId = d.getAttribute('data-drawer-source');
        if (srcId) {
          var form = document.getElementById(srcId), slot = d.querySelector('[data-drawer-slot]');
          if (form && slot) {
            if (!form.__ppHome) { form.__ppHome = document.createComment('pp-drawer-home'); form.parentNode.insertBefore(form.__ppHome, form); }
            slot.appendChild(form);
          }
        }
        d.showModal();
      });
    });
    $$('dialog', root).forEach(function (d) {
      if (d.__pp) return; d.__pp = true;
      d.addEventListener('click', function (e) {
        if (e.target.closest('[data-dialog-close]')) d.close();
        else if (e.target === d) { // klik w tło
          var r = d.getBoundingClientRect();
          if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) d.close();
        }
      });
      // „Pokaż N ofert” w szufladzie: filtry już działają na żywo — zamknij szufladę
      d.addEventListener('submit', function () { if (d.classList.contains('drawer')) setTimeout(function () { d.close(); }, 0); });
      d.addEventListener('close', function () {
        var srcId = d.getAttribute('data-drawer-source'), form = srcId && document.getElementById(srcId);
        if (form && form.__ppHome) form.__ppHome.parentNode.insertBefore(form, form.__ppHome.nextSibling);
      });
    });
  }

  // ---------- menu „więcej” (wzorzec disclosure + strzałki) ----------
  function menus(root) {
    $$('.menu > [aria-controls]', root).forEach(function (btn) {
      if (btn.__pp) return; btn.__pp = true;
      var list = document.getElementById(btn.getAttribute('aria-controls'));
      function items() { return $$('button, a', list); }
      function open(focusFirst) { list.hidden = false; btn.setAttribute('aria-expanded', 'true'); if (focusFirst) items()[0].focus(); }
      function close(returnFocus) { list.hidden = true; btn.setAttribute('aria-expanded', 'false'); if (returnFocus) btn.focus(); }
      btn.addEventListener('click', function (e) { e.stopPropagation(); list.hidden ? open(false) : close(false); });
      btn.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown') { e.preventDefault(); open(true); } });
      list.addEventListener('keydown', function (e) {
        var it = items(), i = it.indexOf(document.activeElement);
        if (e.key === 'ArrowDown') { e.preventDefault(); it[(i + 1) % it.length].focus(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); it[(i - 1 + it.length) % it.length].focus(); }
        else if (e.key === 'Escape') { e.preventDefault(); close(true); }
        else if (e.key === 'Tab') close(false);
      });
      list.addEventListener('click', function (e) { if (e.target.closest('button, a')) close(true); });
      document.addEventListener('click', function (e) { if (!list.hidden && !list.contains(e.target)) close(false); });
    });
  }

  // ---------- podpowiedź: Esc chowa (WCAG 1.4.13) ----------
  function tips(root) {
    $$('.tip', root).forEach(function (t) {
      if (t.__pp) return; t.__pp = true;
      var body = t.querySelector('.tip-body');
      // nie wychodź poza ekran: przesuń dymek, strzałka zostaje nad przyciskiem
      function place() {
        if (!body) return;
        body.style.removeProperty('--tip-shift');
        var r = body.getBoundingClientRect(), shift = 0;
        if (r.right > innerWidth - 8) shift = innerWidth - 8 - r.right;
        if (r.left + shift < 8) shift = 8 - r.left;
        if (shift) body.style.setProperty('--tip-shift', Math.round(shift) + 'px');
      }
      t.addEventListener('mouseenter', function () { requestAnimationFrame(place); });
      t.addEventListener('focusin', function () { requestAnimationFrame(place); });
      t.addEventListener('keydown', function (e) { if (e.key === 'Escape') t.classList.add('is-dismissed'); });
      t.addEventListener('mouseleave', function () { t.classList.remove('is-dismissed'); });
      t.addEventListener('focusout', function () { t.classList.remove('is-dismissed'); });
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') $$('.tip:hover').forEach(function (t) { t.classList.add('is-dismissed'); }); });
  }

  // ---------- nawigacja mobilna ----------
  function navs(root) {
    $$('.nav-toggle[aria-controls]', root).forEach(function (btn) {
      if (btn.__pp) return; btn.__pp = true;
      var nav = document.getElementById(btn.getAttribute('aria-controls'));
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') !== 'true';
        btn.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);
      });
      nav.addEventListener('keydown', function (e) { if (e.key === 'Escape') { btn.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); btn.focus(); } });
    });
  }

  // ---------- powiadomienia ----------
  function notices(root) {
    $$('.notice [data-dismiss]', root).forEach(function (b) {
      if (b.__pp) return; b.__pp = true;
      b.addEventListener('click', function () { b.closest('.notice').remove(); });
    });
  }
  var region, alertRegion;
  function regions() {
    if (region) return;
    region = document.createElement('ul'); region.className = 'toasts'; region.setAttribute('aria-live', 'polite'); region.setAttribute('aria-label', 'Powiadomienia');
    alertRegion = document.createElement('div'); alertRegion.className = 'sr-only'; alertRegion.setAttribute('role', 'alert');
    document.body.appendChild(region); document.body.appendChild(alertRegion);
  }
  /** ppToast({ status: 'info'|'success'|'warning'|'error', title, text, timeout }) — sukces/informacja znikają po 6 s
   *  (pauza po najechaniu i przy fokusie), ostrzeżenie i błąd zostają do zamknięcia. */
  function toast(o) {
    regions();
    var status = ICON[o.status] ? o.status : 'info';
    var li = document.createElement('li');
    li.className = 'notice notice-' + status + ' toast';
    li.innerHTML = '<span class="notice-icon"><span class="icon ' + ICON[status] + '" aria-hidden="true"></span></span>' +
      '<div class="notice-body"><strong class="notice-title"></strong><p></p></div>' +
      '<button class="icon-btn" type="button" aria-label="Zamknij powiadomienie"><span class="icon i-close" aria-hidden="true"></span></button>';
    li.querySelector('.notice-title').textContent = o.title || '';
    var p = li.querySelector('p'); if (o.text) p.textContent = o.text; else p.remove();
    li.querySelector('button').addEventListener('click', function () { li.remove(); });
    region.appendChild(li);
    if (status === 'error' || status === 'warning') alertRegion.textContent = (o.title || '') + ' ' + (o.text || '');
    var timeout = o.timeout != null ? o.timeout : (status === 'error' || status === 'warning' ? 0 : 6000);
    if (timeout) {
      var t, paused = false;
      var arm = function () { t = setTimeout(function () { if (!paused) li.remove(); }, timeout); };
      li.addEventListener('mouseenter', function () { paused = true; }); li.addEventListener('focusin', function () { paused = true; });
      li.addEventListener('mouseleave', function () { paused = false; clearTimeout(t); arm(); });
      arm();
    }
    return li;
  }

  // ================= v1.8: formularz (walidacja, podsumowanie błędów, kroki), wybór wierszy =================
  function plural(n, forms) {
    var f = forms.split('|');
    return n === 1 ? f[0] : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? f[1] : f[2];
  }
  function labelOf(el) {
    var l = el.id && document.querySelector('label[for="' + el.id + '"]');
    if (!l && el.getAttribute('aria-labelledby')) l = document.getElementById(el.getAttribute('aria-labelledby').split(' ')[0]);
    if (!l) { var fs = el.closest('fieldset'); l = fs && fs.querySelector('legend'); }
    if (!l) l = el.closest('label');
    return (l ? l.textContent : el.name || '').replace(/\*/g, '').replace(/\s+/g, ' ').trim();
  }
  // Komunikat: najpierw data-msg-<rodzaj> na polu, potem domyślny po polsku
  function problem(el) {
    if (el.disabled || el.type === 'hidden' || el.closest('[hidden]')) return null;
    var v = el.type === 'checkbox' || el.type === 'radio' ? null : el.value.trim();
    var msg = function (kind, def) { return el.getAttribute('data-msg-' + kind) || def; };
    if (el.required) {
      if (el.type === 'radio') { var form = el.form || document; if (!form.querySelector('input[type=radio][name="' + el.name + '"]:checked')) return msg('required', 'Wybierz jedną opcję: „' + labelOf(el) + '”.'); }
      else if (el.type === 'checkbox') { if (!el.checked) return msg('required', 'Zaznacz: „' + labelOf(el) + '”.'); }
      else if (el.type === 'file') { if (!el.files || !el.files.length) return msg('required', 'Dodaj plik: „' + labelOf(el) + '”.'); }
      else if (!v) return msg('required', 'Uzupełnij pole „' + labelOf(el) + '”.');
    }
    if (!v) return null;
    if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return msg('email', 'Wpisz adres e-mail w formacie nazwa@domena.pl.');
    if (el.type === 'url' && !/^https?:\/\/\S+\.\S+/.test(v)) return msg('url', 'Wpisz pełny adres strony, np. https://firma.pl.');
    if (el.minLength > 0 && v.length < el.minLength) return msg('minlength', 'Wpisz co najmniej ' + el.minLength + ' ' + plural(el.minLength, 'znak|znaki|znaków') + ' (teraz ' + v.length + ').');
    if (el.pattern && !new RegExp('^(?:' + el.pattern + ')$').test(v)) return msg('pattern', 'Sprawdź format pola „' + labelOf(el) + '”.');
    if (el.type === 'number' || el.inputMode === 'numeric') {
      var n = +v.replace(/\s/g, '').replace(',', '.');
      if (isNaN(n)) return msg('number', 'Wpisz liczbę.');
      if (el.min !== '' && n < +el.min) return msg('min', 'Wpisz liczbę od ' + el.min + (el.max !== '' ? ' do ' + el.max : '') + '.');
      if (el.max !== '' && n > +el.max) return msg('max', 'Wpisz liczbę ' + (el.min !== '' ? 'od ' + el.min + ' ' : '') + 'do ' + el.max + '.');
    }
    var other = el.getAttribute('data-match') && document.getElementById(el.getAttribute('data-match'));
    if (other && other.value !== el.value) return msg('match', 'Wartości w polach się różnią.');
    return null;
  }
  function boxOf(el) { return el.closest('.field') || el.closest('fieldset') || el.parentNode; }
  function setMsg(el, kind, text) {
    var box = boxOf(el), id = (el.id || el.name) + '-' + kind;
    var node = document.getElementById(id);
    var cls = kind === 'err' ? 'field-error' : 'field-warning';
    if (!text) {
      if (node) node.remove();
      el.setAttribute('aria-describedby', (el.getAttribute('aria-describedby') || '').split(' ').filter(function (x) { return x && x !== id; }).join(' '));
      if (!el.getAttribute('aria-describedby')) el.removeAttribute('aria-describedby');
      return;
    }
    if (!node) {
      node = document.createElement('p'); node.className = cls; node.id = id;
      var after = box.querySelector('.field-count, .field-hint, .file-list') || null;
      if (box.tagName === 'FIELDSET') box.appendChild(node); else if (after) box.insertBefore(node, after); else box.appendChild(node);
      var ids = (el.getAttribute('aria-describedby') || '').split(' ').filter(Boolean);
      if (ids.indexOf(id) < 0) ids.unshift(id);
      el.setAttribute('aria-describedby', ids.join(' '));
    }
    node.textContent = text;
  }
  function check(el, show) {
    var p = problem(el), group = el.type === 'radio' ? $$('input[type=radio][name="' + el.name + '"]', el.form || document) : [el];
    group.forEach(function (g) { if (p && show) g.setAttribute('aria-invalid', 'true'); else g.removeAttribute('aria-invalid'); });
    var box = boxOf(el);
    if (box.classList.contains('field')) box.classList.toggle('is-error', !!(p && show));
    var upload = el.closest('.upload'); if (upload) upload.classList.toggle('is-error', !!(p && show));
    setMsg(group[0], 'err', show ? p : null);
    // ostrzeżenie: data-warn-empty="tekst" — puste pole jest dozwolone, ale podpowiadamy
    if (el.hasAttribute('data-warn-empty')) {
      var warn = !p && show !== null && !el.value.trim() ? el.getAttribute('data-warn-empty') : null;
      if (box.classList.contains('field')) box.classList.toggle('is-warning', !!warn);
      setMsg(el, 'warn', warn);
    }
    return p;
  }
  function fieldsIn(scope) {
    var seen = {};
    return $$('input, select, textarea', scope).filter(function (el) {
      if (el.type === 'radio') { if (seen[el.name]) return false; seen[el.name] = true; }
      return !el.closest('[data-drawer-slot]') && ['submit', 'button', 'reset', 'hidden'].indexOf(el.type) < 0;
    });
  }
  function summary(form, errors) {
    var box = form.querySelector('.error-summary');
    if (!errors.length) { if (box) box.remove(); return; }
    if (!box) {
      box = document.createElement('div');
      box.className = 'notice notice-error error-summary'; box.setAttribute('tabindex', '-1'); box.setAttribute('role', 'alert');
      box.innerHTML = '<span class="notice-icon"><span class="icon i-error" aria-hidden="true"></span></span><div class="notice-body"><strong class="notice-title"></strong><ul></ul></div>';
      var anchor = form.querySelector('[data-error-summary]');
      if (anchor) anchor.appendChild(box); else form.insertBefore(box, form.firstElementChild && form.firstElementChild.matches('h1, h2, .steps-progress') ? form.firstElementChild.nextSibling : form.firstChild);
    }
    box.querySelector('.notice-title').textContent = 'Popraw ' + errors.length + ' ' + plural(errors.length, 'pole|pola|pól') + ', żeby przejść dalej';
    var ul = box.querySelector('ul'); ul.innerHTML = '';
    errors.forEach(function (e) {
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = '#' + e.el.id; a.textContent = e.msg;
      a.addEventListener('click', function (ev) { ev.preventDefault(); e.el.focus(); e.el.scrollIntoView({ block: 'center' }); });
      li.appendChild(a); ul.appendChild(li);
    });
    box.focus();
  }
  function validateScope(form, scope) {
    var errors = [];
    fieldsIn(scope).forEach(function (el) { el.__ppTouched = true; var p = check(el, true); if (p) errors.push({ el: el, msg: p }); });
    summary(form, errors);
    return errors.length === 0;
  }
  function forms(root) {
    $$('form[data-validate]', root).forEach(function (form) {
      if (form.__ppV) return; form.__ppV = true;
      form.setAttribute('novalidate', '');
      // Kiedy walidujemy: po opuszczeniu pola (jeśli coś wpisano albo już wysyłano); w trakcie pisania tylko gasimy błąd.
      form.addEventListener('focusout', function (e) {
        var el = e.target; if (!el.matches || !el.matches('input, select, textarea')) return;
        if (el.value && el.value.trim()) el.__ppTouched = true;
        if (el.__ppTouched || form.__ppSubmitted) check(el, true);
      });
      form.addEventListener('input', function (e) {
        var el = e.target;
        if (el.getAttribute('aria-invalid') === 'true' && !problem(el)) { check(el, true); if (form.__ppSubmitted) summary(form, fieldsIn(form).map(function (f) { return { el: f, msg: f.getAttribute('aria-invalid') === 'true' && problem(f) }; }).filter(function (x) { return x.msg; })); }
      });
      form.addEventListener('change', function (e) { var el = e.target; if (el.type === 'radio' || el.type === 'checkbox' || el.type === 'file' || el.tagName === 'SELECT') { if (form.__ppSubmitted || el.__ppTouched) check(el, true); } });
      form.addEventListener('submit', function (e) {
        form.__ppSubmitted = true;
        var wizard = form.matches('[data-wizard]') ? form : null;
        var scope = wizard ? wizard.querySelector('.wizard-step:not([hidden])') : form;
        if (!validateScope(form, scope)) { e.preventDefault(); e.stopImmediatePropagation(); return; }
        form.dispatchEvent(new CustomEvent('pp:valid', { bubbles: true }));
        if (!form.getAttribute('action')) e.preventDefault();
      });
    });
  }
  function wizards(root) {
    $$('[data-wizard]', root).forEach(function (w) {
      if (w.__ppW) return; w.__ppW = true;
      var steps = $$('.wizard-step', w), marks = $$('.steps-progress li', w);
      var prev = w.querySelector('[data-wizard-prev]'), next = w.querySelector('[data-wizard-next]'), submit = w.querySelector('[type=submit]');
      var live = document.createElement('p'); live.className = 'sr-only'; live.setAttribute('aria-live', 'polite'); w.appendChild(live);
      var i = 0;
      function go(n, focus) {
        i = n;
        steps.forEach(function (s, k) { s.hidden = k !== i; });
        marks.forEach(function (m, k) { m.classList.toggle('is-done', k < i); if (k === i) m.setAttribute('aria-current', 'step'); else m.removeAttribute('aria-current'); });
        if (prev) prev.hidden = i === 0;
        if (next) next.hidden = i === steps.length - 1;
        if (submit) submit.hidden = i !== steps.length - 1;
        var h = steps[i].querySelector('h2, h3, legend');
        live.textContent = 'Krok ' + (i + 1) + ' z ' + steps.length + (h ? ': ' + h.textContent.trim() : '');
        if (focus && h) { h.setAttribute('tabindex', '-1'); h.focus(); }
      }
      if (next) next.addEventListener('click', function () { w.__ppSubmitted = true; if (validateScope(w, steps[i])) go(i + 1, true); });
      if (prev) prev.addEventListener('click', function () { var s = w.querySelector('.error-summary'); if (s) s.remove(); go(i - 1, true); });
      go(0, false);
    });
  }
  function selectables(root) {
    $$('table[data-selectable]', root).forEach(function (t) {
      if (t.__ppS) return; t.__ppS = true;
      var all = t.querySelector('[data-select-all]'), bar = document.querySelector('[data-bulk-for="' + t.id + '"]');
      var count = bar && bar.querySelector('.bulk-count');
      function rows() { return $$('tbody input[data-select-row]', t); }
      function paint() {
        var r = rows(), on = r.filter(function (c) { return c.checked; });
        r.forEach(function (c) { c.closest('tr').setAttribute('aria-selected', String(c.checked)); });
        if (all) { all.checked = on.length === r.length && r.length > 0; all.indeterminate = on.length > 0 && on.length < r.length; }
        if (bar) {
          bar.hidden = !on.length;
          if (count) count.textContent = 'Zaznaczono ' + on.length + ' ' + plural(on.length, (count.getAttribute('data-forms') || 'pozycję|pozycje|pozycji'));
        }
      }
      t.addEventListener('change', function (e) {
        if (e.target === all) rows().forEach(function (c) { c.checked = all.checked; });
        if (e.target === all || e.target.hasAttribute('data-select-row')) paint();
      });
      if (bar) $$('[data-bulk-clear]', bar).forEach(function (b) { b.addEventListener('click', function () { rows().forEach(function (c) { c.checked = false; }); paint(); (all || t).focus(); }); });
      t.ppSelected = function () { return rows().filter(function (c) { return c.checked; }).map(function (c) { return c.closest('tr'); }); };
      paint();
    });
  }
  /** ppProgress(elem, wartość 0–100 | null) — null = nieokreślony */
  function progress(el, v) {
    var bar = el.querySelector('[role=progressbar]') || el;
    if (v == null) { el.classList.add('is-indeterminate'); bar.removeAttribute('aria-valuenow'); return; }
    el.classList.remove('is-indeterminate');
    bar.setAttribute('aria-valuenow', Math.round(v));
    el.style.setProperty('--value', Math.max(0, Math.min(100, v)) + '%');
    var num = el.querySelector('.progress-label .num'); if (num) num.textContent = Math.round(v) + '%';
  }

  function initAll(root) { switches(root); steppers(root); counters(root); uploads(root); dialogs(root); menus(root); tips(root); navs(root); notices(root); forms(root); wizards(root); selectables(root); }
  window.ppUi = { initAll: initAll, toast: toast, progress: progress };
  window.ppProgress = progress;
  window.ppToast = toast;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { initAll(); });
  else initAll();
})();
