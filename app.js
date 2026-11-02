/* S2000 Build Tracker — data lives in localStorage; no build step, no dependencies. */
(() => {
  'use strict';

  const STORAGE_KEY = 's2000-tracker-v1';
  const CATEGORIES = [
    'Engine', 'Intake', 'Exhaust', 'Fuel', 'Cooling', 'Drivetrain', 'Suspension',
    'Brakes', 'Wheels/Tires', 'Aero/Exterior', 'Interior', 'Electrical', 'Tools', 'Other',
  ];

  // Starting maintenance schedule. Intervals are common enthusiast intervals,
  // tighter than the factory schedule in places — check your owner's manual.
  const DEFAULT_MAINT = [
    ['Engine oil & filter', 5000, 6, '10W-30, about 5 qt with filter (check manual for your chassis)'],
    ['Valve clearance check', 30000, 0, 'Cold spec in service manual; adjust if out of range'],
    ['Transmission fluid', 30000, 24, 'Honda MTF'],
    ['Differential fluid', 30000, 24, 'Hypoid gear oil SAE 90 (GL-5); LSD-compatible'],
    ['Brake fluid flush', 0, 24, 'DOT 3/4 (or high-temp fluid for track use)'],
    ['Clutch fluid flush', 0, 24, 'Same fluid as brakes'],
    ['Engine air filter', 15000, 0, 'Inspect more often with an open intake'],
    ['Coolant', 60000, 60, 'Honda Type 2 coolant'],
    ['Spark plugs', 60000, 0, 'Iridium; torque per manual'],
    ['Alignment check', 0, 12, 'Staggered tires: front/rear rotation not possible'],
    ['Soft top inspection / clean', 0, 12, 'Clean & protect fabric/vinyl; clear the drain holes'],
  ];

  const uid = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  const today = () => new Date().toISOString().slice(0, 10);

  function defaults() {
    return {
      car: { year: '', chassis: 'AP1', color: '', vin: '', budget: '', goal: '' },
      odometer: '',
      parts: [],
      maintenance: DEFAULT_MAINT.map(([name, intervalMiles, intervalMonths, notes]) => ({
        id: uid(), name, intervalMiles: intervalMiles || '', intervalMonths: intervalMonths || '',
        lastMiles: '', lastDate: '', notes,
      })),
      log: [],
      todos: [],
    };
  }

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return { ...defaults(), ...JSON.parse(raw) };
    } catch (e) { /* storage blocked or corrupted: fall through */ }
    return defaults();
  }

  let state = load();
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) { /* ignore */ }
    render();
  }

  // ---------- helpers ----------
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const num = (v) => (v === '' || v == null || isNaN(+v) ? 0 : +v);
  const money = (v) => '$' + num(v).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 });
  const miles = (v) => num(v).toLocaleString() + ' mi';

  function formData(form) {
    const o = {};
    new FormData(form).forEach((v, k) => { o[k] = typeof v === 'string' ? v.trim() : v; });
    return o;
  }
  function fillForm(form, obj) {
    $$('[name]', form).forEach((el) => { el.value = obj[el.name] ?? ''; });
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function resetForm(form) { form.reset(); const id = form.querySelector('[name=id]'); if (id) id.value = ''; }
  function upsert(list, item) {
    if (item.id) { const i = list.findIndex((x) => x.id === item.id); if (i >= 0) { list[i] = item; return; } }
    item.id = uid(); list.push(item);
  }

  // Maintenance due calculation: returns { milesLeft, daysLeft, status }
  function dueInfo(m) {
    const odo = num(state.odometer);
    let milesLeft = null, daysLeft = null;
    if (num(m.intervalMiles) && m.lastMiles !== '' && odo) milesLeft = num(m.lastMiles) + num(m.intervalMiles) - odo;
    if (num(m.intervalMonths) && m.lastDate) {
      const d = new Date(m.lastDate + 'T00:00:00');
      d.setMonth(d.getMonth() + num(m.intervalMonths));
      daysLeft = Math.round((d - new Date(today() + 'T00:00:00')) / 86400000);
    }
    let status = 'unknown';
    if (milesLeft !== null || daysLeft !== null) {
      const over = (milesLeft !== null && milesLeft < 0) || (daysLeft !== null && daysLeft < 0);
      const soon = (milesLeft !== null && milesLeft <= 500) || (daysLeft !== null && daysLeft <= 30);
      status = over ? 'over' : soon ? 'soon' : 'ok';
    }
    return { milesLeft, daysLeft, status };
  }
  function dueText(info) {
    const bits = [];
    if (info.milesLeft !== null) bits.push(info.milesLeft < 0 ? `${miles(-info.milesLeft)} over` : `${miles(info.milesLeft)} left`);
    if (info.daysLeft !== null) bits.push(info.daysLeft < 0 ? `${-info.daysLeft} d over` : `${info.daysLeft} d left`);
    return bits.join(' · ') || 'Set last-done';
  }

  // ---------- rendering ----------
  function render() {
    const c = state.car;
    $('#carLabel').textContent = [c.year, 'Honda S2000', c.chassis, c.color].filter(Boolean).join(' ');
    if (document.activeElement !== $('#odometer')) $('#odometer').value = state.odometer;
    renderDashboard();
    renderParts();
    renderMaint();
    renderLog();
    renderTodos();
  }

  function renderDashboard() {
    const parts = state.parts;
    const spent = parts.filter((p) => p.status !== 'planned').reduce((s, p) => s + num(p.cost), 0)
      + state.log.reduce((s, l) => s + num(l.cost), 0);
    const planned = parts.filter((p) => p.status === 'planned').reduce((s, p) => s + num(p.cost), 0);
    const budget = num(state.car.budget);
    const installed = parts.filter((p) => p.status === 'installed').length;
    const hours = state.log.reduce((s, l) => s + num(l.hours), 0);
    const overdue = state.maintenance.filter((m) => dueInfo(m).status === 'over').length;
    const pct = budget ? Math.min(100, (spent / budget) * 100) : 0;

    $('#stats').innerHTML = `
      <div class="stat"><div class="label">Spent</div><div class="value">${money(spent)}</div>
        <div class="sub">${budget ? `${pct.toFixed(0)}% of ${money(budget)} budget` : 'Set a budget in Settings'}</div>
        ${budget ? `<div class="meter"><span style="width:${pct}%"></span></div>` : ''}</div>
      <div class="stat"><div class="label">Planned</div><div class="value">${money(planned)}</div><div class="sub">not yet bought</div></div>
      <div class="stat"><div class="label">Parts installed</div><div class="value">${installed} / ${parts.length}</div></div>
      <div class="stat"><div class="label">Wrench hours</div><div class="value">${hours.toLocaleString()}</div></div>
      <div class="stat"><div class="label">Overdue service</div><div class="value ${overdue ? 'due-over' : ''}">${overdue}</div></div>`;

    const due = state.maintenance.map((m) => ({ m, info: dueInfo(m) }))
      .filter((x) => x.info.status === 'over' || x.info.status === 'soon')
      .sort((a, b) => (a.info.status === 'over' ? -1 : 1) - (b.info.status === 'over' ? -1 : 1));
    $('#dueList').innerHTML = due.length
      ? due.map(({ m, info }) => `<li><span>${esc(m.name)}</span><span class="due-${info.status}">${dueText(info)}</span></li>`).join('')
      : '<li class="muted">Nothing due soon. Keep the odometer and last-done dates current.</li>';

    const byCat = {};
    parts.filter((p) => p.status !== 'planned').forEach((p) => { byCat[p.category] = (byCat[p.category] || 0) + num(p.cost); });
    const cats = Object.entries(byCat).sort((a, b) => b[1] - a[1]);
    const max = cats.length ? cats[0][1] : 0;
    $('#catBars').innerHTML = cats.length
      ? cats.map(([k, v]) => `<div class="bar"><span>${esc(k)}</span><div class="track"><div class="fill" style="width:${max ? (v / max) * 100 : 0}%"></div></div><span class="amt">${money(v)}</span></div>`).join('')
      : '<p class="muted">No purchased parts yet.</p>';

    const open = state.todos.filter((t) => !t.done).sort((a, b) => a.priority - b.priority).slice(0, 6);
    $('#dashTodos').innerHTML = open.length
      ? open.map((t) => `<li><span>${esc(t.text)}</span>${t.priority == 1 ? '<span class="due-over">High</span>' : ''}</li>`).join('')
      : '<li class="muted">No open tasks.</li>';

    const recent = [...state.log].sort((a, b) => (b.date || '').localeCompare(a.date || '')).slice(0, 5);
    $('#dashLog').innerHTML = recent.length
      ? recent.map((l) => `<li><span>${esc(l.title)}</span><span class="muted">${esc(l.date)}</span></li>`).join('')
      : '<li class="muted">No log entries yet.</li>';
  }

  function renderParts() {
    const q = $('#partSearch').value.toLowerCase();
    const f = $('#partFilter').value;
    const rows = state.parts
      .filter((p) => !f || p.status === f)
      .filter((p) => !q || [p.name, p.brand, p.vendor, p.partNo, p.category, p.notes].join(' ').toLowerCase().includes(q))
      .sort((a, b) => (a.category || '').localeCompare(b.category || '') || a.name.localeCompare(b.name));
    const total = rows.reduce((s, p) => s + num(p.cost), 0);
    $('#partTable').innerHTML = `
      <thead><tr><th>Part</th><th>Category</th><th>Vendor</th><th>Status</th><th class="num">Cost</th><th></th></tr></thead>
      <tbody>${rows.map((p) => `
        <tr>
          <td><strong>${p.link ? `<a href="${esc(p.link)}" target="_blank" rel="noopener">${esc(p.name)}</a>` : esc(p.name)}</strong>
            <div class="muted">${esc([p.brand, p.partNo].filter(Boolean).join(' · '))}${p.notes ? ' — ' + esc(p.notes) : ''}</div></td>
          <td>${esc(p.category)}</td>
          <td>${esc(p.vendor)}</td>
          <td><select data-status="${p.id}" class="badge s-${p.status}">
            ${['planned', 'ordered', 'received', 'installed'].map((s) => `<option ${s === p.status ? 'selected' : ''}>${s}</option>`).join('')}
          </select></td>
          <td class="num">${money(p.cost)}</td>
          <td><button class="icon" data-edit-part="${p.id}" title="Edit">✎</button><button class="icon" data-del-part="${p.id}" title="Delete">✕</button></td>
        </tr>`).join('') || '<tr><td colspan="6" class="muted">No parts yet. Add one above.</td></tr>'}
      </tbody>
      <tfoot><tr><td colspan="4">Total (${rows.length})</td><td class="num">${money(total)}</td><td></td></tr></tfoot>`;
  }

  function renderMaint() {
    $('#maintTable').innerHTML = `
      <thead><tr><th>Item</th><th>Interval</th><th>Last done</th><th>Due</th><th></th></tr></thead>
      <tbody>${state.maintenance.map((m) => {
        const info = dueInfo(m);
        const interval = [m.intervalMiles ? miles(m.intervalMiles) : '', m.intervalMonths ? `${m.intervalMonths} mo` : ''].filter(Boolean).join(' / ');
        const last = [m.lastMiles !== '' ? miles(m.lastMiles) : '', m.lastDate].filter(Boolean).join(' · ') || '—';
        return `<tr>
          <td><strong>${esc(m.name)}</strong><div class="muted">${esc(m.notes)}</div></td>
          <td>${interval || '—'}</td>
          <td>${last}</td>
          <td class="due-${info.status}">${dueText(info)}</td>
          <td style="white-space:nowrap"><button class="ghost" data-done="${m.id}" title="Mark done now">Done</button>
            <button class="icon" data-edit-maint="${m.id}" title="Edit">✎</button><button class="icon" data-del-maint="${m.id}" title="Delete">✕</button></td>
        </tr>`;
      }).join('')}</tbody>`;
  }

  function renderLog() {
    const entries = [...state.log].sort((a, b) => (b.date || '').localeCompare(a.date || ''));
    $('#logList').innerHTML = entries.map((l) => `
      <article class="log-entry">
        <header><strong>${esc(l.title)}</strong>
          <span><button class="icon" data-edit-log="${l.id}" title="Edit">✎</button><button class="icon" data-del-log="${l.id}" title="Delete">✕</button></span></header>
        <div class="meta">${esc(l.date)}${l.miles ? ' · ' + miles(l.miles) : ''}${num(l.cost) ? ' · ' + money(l.cost) : ''}${num(l.hours) ? ' · ' + l.hours + ' h' : ''}</div>
        ${l.notes ? `<p>${esc(l.notes)}</p>` : ''}
      </article>`).join('') || '<p class="muted">No entries yet.</p>';
  }

  function renderTodos() {
    const list = [...state.todos].sort((a, b) => (a.done - b.done) || (a.priority - b.priority));
    $('#todoList').innerHTML = list.map((t) => `
      <li class="${t.done ? 'done' : ''} p${t.priority}">
        <input type="checkbox" data-toggle="${t.id}" ${t.done ? 'checked' : ''}>
        <span>${esc(t.text)}</span>
        <button class="icon" data-del-todo="${t.id}" title="Delete">✕</button>
      </li>`).join('') || '<li class="muted">No tasks.</li>';
  }

  // ---------- events ----------
  $$('.tabs button').forEach((b) => b.addEventListener('click', () => {
    $$('.tabs button').forEach((x) => x.classList.toggle('active', x === b));
    $$('.tab').forEach((t) => t.classList.toggle('active', t.id === b.dataset.tab));
    try { localStorage.setItem(STORAGE_KEY + ':tab', b.dataset.tab); } catch (e) { /* ignore */ }
  }));
  try {
    const t = localStorage.getItem(STORAGE_KEY + ':tab');
    if (t) $(`.tabs button[data-tab="${t}"]`)?.click();
  } catch (e) { /* ignore */ }

  $('#odometer').addEventListener('change', (e) => { state.odometer = e.target.value; save(); });

  $('#partForm [name=category]').innerHTML = CATEGORIES.map((c) => `<option>${c}</option>`).join('');
  $$('[data-reset]').forEach((b) => b.addEventListener('click', () => resetForm(b.closest('form'))));

  $('#partForm').addEventListener('submit', (e) => {
    e.preventDefault(); upsert(state.parts, formData(e.target)); resetForm(e.target); save();
  });
  $('#maintForm').addEventListener('submit', (e) => {
    e.preventDefault(); upsert(state.maintenance, formData(e.target)); resetForm(e.target); save();
  });
  $('#logForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const entry = formData(e.target);
    upsert(state.log, entry);
    if (num(entry.miles) > num(state.odometer)) state.odometer = entry.miles;
    resetForm(e.target); e.target.date.value = today(); save();
  });
  $('#logForm').date.value = today();
  $('#todoForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const d = formData(e.target);
    state.todos.push({ id: uid(), text: d.text, priority: +d.priority, done: false });
    e.target.reset(); save();
  });
  $('#carForm').addEventListener('submit', (e) => { e.preventDefault(); state.car = formData(e.target); save(); });
  fillCarForm();
  function fillCarForm() { $$('#carForm [name]').forEach((el) => { el.value = state.car[el.name] ?? ''; }); }

  $('#partSearch').addEventListener('input', renderParts);
  $('#partFilter').addEventListener('change', renderParts);

  document.addEventListener('click', (e) => {
    const t = e.target.closest('button, input[type=checkbox]');
    if (!t) return;
    const d = t.dataset;
    const find = (list, id) => list.find((x) => x.id === id);
    const del = (key, id) => { if (confirm('Delete this item?')) { state[key] = state[key].filter((x) => x.id !== id); save(); } };

    if (d.editPart) fillForm($('#partForm'), find(state.parts, d.editPart));
    else if (d.delPart) del('parts', d.delPart);
    else if (d.editMaint) fillForm($('#maintForm'), find(state.maintenance, d.editMaint));
    else if (d.delMaint) del('maintenance', d.delMaint);
    else if (d.editLog) fillForm($('#logForm'), find(state.log, d.editLog));
    else if (d.delLog) del('log', d.delLog);
    else if (d.delTodo) del('todos', d.delTodo);
    else if (d.toggle) { const td = find(state.todos, d.toggle); td.done = t.checked; save(); }
    else if (d.done) {
      const m = find(state.maintenance, d.done);
      m.lastDate = today();
      if (state.odometer !== '') m.lastMiles = state.odometer;
      state.log.push({ id: uid(), date: today(), miles: state.odometer, title: m.name, cost: '', hours: '', notes: m.notes ? `Service: ${m.notes}` : '' });
      save();
    }
  });
  document.addEventListener('change', (e) => {
    const id = e.target.dataset?.status;
    if (!id) return;
    const p = state.parts.find((x) => x.id === id);
    p.status = e.target.value; save();
  });

  // ---------- import / export ----------
  function download(name, text, type) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type }));
    a.download = name; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  $('#exportBtn').addEventListener('click', () => download(`s2000-tracker-${today()}.json`, JSON.stringify(state, null, 2), 'application/json'));
  $('#exportCsv').addEventListener('click', () => {
    const cols = ['name', 'category', 'brand', 'vendor', 'partNo', 'cost', 'status', 'link', 'notes'];
    const q = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
    const csv = [cols.join(','), ...state.parts.map((p) => cols.map((c) => q(p[c])).join(','))].join('\n');
    download(`s2000-parts-${today()}.csv`, csv, 'text/csv');
  });
  $('#importFile').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      if (typeof data !== 'object' || !Array.isArray(data.parts)) throw new Error('Not a tracker export');
      if (!confirm('Replace all current data with this file?')) return;
      state = { ...defaults(), ...data }; fillCarForm(); save();
    } catch (err) { alert('Import failed: ' + err.message); }
    e.target.value = '';
  });
  $('#resetBtn').addEventListener('click', () => {
    if (confirm('Erase all data and restore the default maintenance schedule?')) { state = defaults(); fillCarForm(); save(); }
  });

  render();
})();
