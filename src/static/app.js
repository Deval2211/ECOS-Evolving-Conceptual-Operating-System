const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));

function fillSelect(id, options, extraLast = null) {
  const el = document.getElementById(id);
  const prev = el.value;
  el.innerHTML = options.map(o => `<option value="${esc(o.v)}">${esc(o.t)}</option>`).join('') +
    (extraLast ? `<option value="${esc(extraLast.v)}">${esc(extraLast.t)}</option>` : '');
  if (prev && [...el.options].some(opt => opt.value === prev)) {
    el.value = prev;
  }
}

async function ingestSentence() {
  const body = {
    sentence: document.getElementById('nlpSentence').value,
    mode: document.getElementById('nlpMode').value,
  };
  const res = await fetch('/api/ingest', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const d = await res.json();
  document.getElementById('ingestMsg').innerHTML = res.ok
    ? `<div class="msg ok"><b>ADAPTER [${esc(d.parser_used)}] STORED CLAIM:</b> <code>${esc(d.claim.id)}</code> ` +
      `(${esc(d.claim.subject_id)}.${esc(d.claim.relation)} = <b>${esc(d.claim.object_value)}</b>, ` +
      `state=${esc(d.claim.epistemic_state)})</div>`
    : `<div class="msg err"><b>ADAPTER ERROR:</b> ${esc(d.error)}</div>`;
  await loadOverview();
}

async function askQuestion() {
  const q = document.getElementById('nlpAsk').value;
  const res = await fetch('/api/ask?q=' + encodeURIComponent(q));
  const d = await res.json();
  document.getElementById('askMsg').innerHTML = res.ok
    ? `<div class="msg ok"><b>CRS ANSWER:</b> ${esc(d.answer)}</div>`
    : `<div class="msg err"><b>ERROR:</b> ${esc(d.error)}</div>`;
}

async function loadOverview() {
  const d = await (await fetch('/api/overview')).json();

  document.getElementById('stats').innerHTML = Object.entries(d.stats)
    .map(([k, v]) => `<div class="stat"><b>${v}</b><span>${esc(k)}</span></div>`)
    .join('');

  const entOpts = d.entities.map(e => ({ v: e.id, t: `${e.labels[0] || e.id} (${e.id})` }));
  fillSelect('tSubj', entOpts);
  fillSelect('wSubj', entOpts, { v: 'ent_missing', t: 'ent_missing (Triggers Ref Error)' });
  fillSelect('eConcept', d.concepts.map(c => ({ v: c.id, t: `${c.canonical} (${c.id})` })));

  document.getElementById('inferredBox').innerHTML = d.inferred.length ? `<table>
    <tr><th>Claim ID</th><th>Subject</th><th>Relation</th><th>Derived Value</th><th>Provenance Trace</th></tr>
    ${d.inferred.map(item => `<tr>
      <td><code>${esc(item.claim.id)}</code></td>
      <td>${esc(item.claim.subject_id)}</td>
      <td>${esc(item.claim.relation)}</td>
      <td><span class="tag purple">${esc(item.claim.object_value)}</span></td>
      <td><small>${esc(item.provenance_trace)}</small></td>
    </tr>`).join('')}
  </table>` : '<p class="hint">No inferred claims yet. Click "Run Reasoning Engine" above.</p>';

  const learnedList = (d.learned || []).map(c =>
    `<li><span class="tag ok">INTERPRETED</span> <code>${esc(c.id)}</code>: ` +
    `<b>${esc(c.subject_id)}</b> has <b>${esc(c.object_value)}</b> claim(s)</li>`
  ).join('');

  document.getElementById('evolutionBox').innerHTML = learnedList
    ? `<p><b>Learned Multi-Claim Profiles:</b><ul>${learnedList}</ul></p>`
    : '<p class="hint">No learned profiles yet. Click "Run Learning &amp; Evolution" above.</p>';

  const contra = d.contradictions.map(x =>
    `<li><span class="tag err">CONTESTED</span> ` +
    `<code>${esc(x.claim_a.id)}</code> (${esc(x.claim_a.subject_id)}.${esc(x.claim_a.relation)}=<b>${esc(x.claim_a.object_value)}</b>) ` +
    `<b>&harr; contradicts &harr;</b> ` +
    `<code>${esc(x.claim_b.id)}</code> (<b>${esc(x.claim_b.object_value)}</b>) ` +
    `<small>— ${esc(x.link.note)}</small></li>`
  ).join('');

  const unk = d.unknown.map(c =>
    `<li><span class="tag warn">${esc(c.epistemic_state)}</span> ` +
    `<code>${esc(c.id)}</code>: ${esc(c.subject_id)}.${esc(c.relation)} ` +
    `(polarity=<b>${esc(c.polarity)}</b> — Unknown != False)</li>`
  ).join('');

  const prov = d.provenance
    .map(n => `<span class="tag">${esc(n.kind.toUpperCase())}: ${esc(n.id)}</span>`)
    .join(' &larr; ');

  const lin = d.lineage.map(e =>
    `<li><code>${esc(e.from_concept_id)}</code> ` +
    `<b>--${esc(e.operation)}--&gt;</b> ` +
    `<code>${esc(e.to_concept_id)}</code> (${esc(e.reason)})</li>`
  ).join('');

  document.getElementById('overviewBox').innerHTML = `
    <p><b>Preserved Contradictions:</b><ul>${contra}</ul></p>
    <p><b>Explicit Unknowns:</b><ul>${unk}</ul></p>
    <p><b>Provenance Trace (Dog_001 warm-blooded):</b><br/>${prov}</p>
    <p><b>Concept Evolution Lineage:</b><ul>${lin}</ul></p>
  `;
}

async function runReasoning() {
  const res = await fetch('/api/reason', { method: 'POST' });
  const r = await res.json();
  document.getElementById('reasonMsg').innerHTML =
    `<div class="msg ok"><b>REASONING PASS COMPLETE:</b> Added <b>${r.inferences_added}</b> new inferred claim(s) ` +
    `and detected <b>${r.contradictions_detected}</b> new contradiction(s).</div>`;
  await loadOverview();
  loadTemporal();
}

async function runSupervisor() {
  const res = await fetch('/api/supervise', { method: 'POST' });
  const r = await res.json();
  document.getElementById('supervisorMsg').innerHTML =
    `<div class="msg ok"><b>SUPERVISOR REVIEW COMPLETE:</b> Reviewed <b>${r.contradictions_reviewed}</b> contradiction(s), ` +
    `<b>${r.unknown_alerts}</b> unknown state(s), and <b>${r.fragile_inferences}</b> fragile inference(s).</div>`;

  const triages = (r.contradiction_reports || []).map(t =>
    `<li><span class="tag warn">${esc(t.verdict)}</span> <b>${esc(t.subject)}.${esc(t.relation)}</b>: ` +
    `${esc(t.claim_a.value)} (${esc(t.claim_a.source)}, score=${esc(t.claim_a.score)}) vs ` +
    `${esc(t.claim_b.value)} (${esc(t.claim_b.source)}, score=${esc(t.claim_b.score)}) &rarr; <em>${esc(t.recommended_action)}</em></li>`
  ).join('');

  const uAlerts = (r.unknown_reports || []).map(u =>
    `<li><span class="tag ${u.priority === 'HIGH_SAFETY' ? 'err' : 'warn'}">${esc(u.priority)}</span> ` +
    `<code>${esc(u.subject)}.${esc(u.relation)}</code> &rarr; ${esc(u.guidance)}</li>`
  ).join('');

  const fragile = (r.fragile_inference_reports || []).map(f =>
    `<li><span class="tag err">FRAGILE</span> <code>${esc(f.subject)}.${esc(f.relation)}</code> = ` +
    `<b>${esc(f.value)}</b> (weak sources: ${esc(f.weak_sources.join(', '))})</li>`
  ).join('');

  document.getElementById('supervisorBox').innerHTML = `
    <p><b>Contradiction Triage:</b><ul>${triages || '<li>None</li>'}</ul></p>
    <p><b>Critical UNKNOWN Alerts:</b><ul>${uAlerts || '<li>None</li>'}</ul></p>
    <p><b>Fragile Inferences:</b><ul>${fragile || '<li>None</li>'}</ul></p>
  `;
  await loadOverview();
}

async function runEvolution() {
  const res = await fetch('/api/evolve', { method: 'POST' });
  const r = await res.json();
  document.getElementById('evolutionMsg').innerHTML =
    `<div class="msg ok"><b>EVOLUTION PASS COMPLETE:</b> Learned <b>${r.learned_claims_added}</b> profile(s), ` +
    `refined <b>${r.concepts_refined}</b> concept(s), and split <b>${r.concepts_split}</b> ambiguous label(s).</div>`;
  await loadOverview();
  loadConcepts();
}

async function loadConcepts() {
  const q = document.getElementById('qConcept').value;
  const rows = await (await fetch('/api/concepts?q=' + encodeURIComponent(q))).json();
  document.getElementById('conceptBox').innerHTML = `<table>
    <tr><th>ID</th><th>Canonical</th><th>Ver</th><th>Multilingual Labels</th><th>Defaults / Exceptions</th></tr>
    ${rows.map(c => `<tr>
      <td><code>${esc(c.id)}</code></td>
      <td><b>${esc(c.canonical)}</b></td>
      <td>v${c.version}</td>
      <td>${Object.entries(c.labels).map(([l, v]) =>
        `<span class="tag">${esc(l)}: ${esc(v.join(', '))}</span>`
      ).join('')}</td>
      <td>${esc(c.defaults.join(', '))}${c.exceptions.length
        ? '<br/><span class="warn">Exceptions: ' + esc(c.exceptions.join(', ')) + '</span>'
        : ''}</td>
    </tr>`).join('')}
  </table>`;
}

function quickConcept(v) {
  document.getElementById('qConcept').value = v;
  loadConcepts();
}

async function loadTemporal() {
  const s = document.getElementById('tSubj').value || 'ent_car_001';
  const dt = document.getElementById('tDate').value;
  const url = `/api/temporal?subject=${encodeURIComponent(s)}&date=${encodeURIComponent(dt)}`;
  const rows = await (await fetch(url)).json();
  document.getElementById('tempBox').innerHTML = rows.length ? `<table>
    <tr><th>Claim ID</th><th>Relation</th><th>Value</th><th>State</th><th>Valid Window</th></tr>
    ${rows.map(c => `<tr>
      <td><code>${esc(c.id)}</code></td>
      <td>${esc(c.relation)}</td>
      <td><b>${esc(c.object_value)}</b></td>
      <td><span class="tag">${esc(c.epistemic_state)}</span></td>
      <td>${esc(c.temporal.valid_from || 'open')} &rarr; ${esc(c.temporal.valid_to || 'present')}</td>
    </tr>`).join('')}
  </table>` : '<p class="hint">No valid claims on this date.</p>';
}

function quickTemporal(subj, dt) {
  document.getElementById('tSubj').value = subj;
  document.getElementById('tDate').value = dt;
  loadTemporal();
}

async function addConcept() {
  const body = {
    id: document.getElementById('cId').value.trim(),
    canonical: document.getElementById('cCanon').value.trim().toUpperCase(),
    en: document.getElementById('cEn').value,
    hi: document.getElementById('cHi').value,
    gu: document.getElementById('cGu').value,
  };
  const res = await fetch('/api/concepts', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const data = await res.json();
  document.getElementById('createMsg').innerHTML = res.ok
    ? `<div class="msg ok"><b>CONCEPT CREATED:</b> <code>${esc(data.id)}</code> (${esc(data.canonical)}) saved to SQLite.</div>`
    : `<div class="msg err"><b>ERROR:</b> ${esc(data.error)}</div>`;
  await loadOverview();
  loadConcepts();
}

async function addEntity() {
  const body = {
    id: document.getElementById('eId').value.trim(),
    concept_id: document.getElementById('eConcept').value,
    label: document.getElementById('eLabel').value.trim(),
  };
  const res = await fetch('/api/entities', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const data = await res.json();
  document.getElementById('createMsg').innerHTML = res.ok
    ? `<div class="msg ok"><b>ENTITY CREATED:</b> <code>${esc(data.id)}</code> (instance of ${esc(data.concept_id)}) added.</div>`
    : `<div class="msg err"><b>ERROR:</b> ${esc(data.error)}</div>`;
  await loadOverview();
}

async function submitClaim() {
  const body = {
    actor: document.getElementById('wActor').value,
    subject_id: document.getElementById('wSubj').value,
    relation: document.getElementById('wRel').value,
    object_value: document.getElementById('wVal').value,
    epistemic_state: document.getElementById('wState').value,
    polarity: document.getElementById('wPol').value,
  };
  const res = await fetch('/api/claims', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const data = await res.json();
  document.getElementById('writeMsg').innerHTML = res.ok
    ? `<div class="msg ok"><b>STORED IN SQLITE:</b> <code>${esc(data.id)}</code> written by ${esc(body.actor)}.</div>`
    : `<div class="msg err"><b>BLOCKED (${res.status}):</b> ${esc(data.error)}</div>`;
  loadOverview();
}

(async () => {
  await loadOverview();
  loadConcepts();
  loadTemporal();
})();
