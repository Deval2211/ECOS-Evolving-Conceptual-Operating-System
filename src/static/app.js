let cachedConcepts = [];

function showToast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 3200);
}

function switchTab(tabName, btn) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById(`tab-${tabName}`).classList.add("active");
}

async function loadOverview() {
  const res = await fetch("/api/overview");
  const data = await res.json();

  // 1. Telemetry Bar
  const statsBar = document.getElementById("stats-bar");
  const statLabels = {
    concepts: "Concepts",
    entities: "Entities",
    events: "Events",
    claims: "Total Claims",
    inferred: "Inferred",
    learned: "Learned",
    contradictions: "Contradictions",
    audit_logs: "Audit Entries"
  };
  statsBar.innerHTML = Object.entries(statLabels)
    .map(([key, label]) => `
      <div class="stat-cell">
        <div class="stat-label">${label}</div>
        <div class="stat-val">${data.stats[key] ?? 0}</div>
      </div>
    `).join("");

  // 2. Contradictions
  document.getElementById("contra-count").textContent = data.contradictions.length;
  const contraEl = document.getElementById("contradictions-list");
  contraEl.innerHTML = data.contradictions.length
    ? data.contradictions.map(item => `
        <div class="item-card">
          <div class="row-between">
            <span class="code-id">${item.claim_a.subject_id}.${item.claim_a.relation}</span>
            <span class="badge badge-warn">CONFLICT</span>
          </div>
          <div class="mt-8">
            <div><strong>A:</strong> <code>${item.claim_a.object_value}</code> <span class="mono-hint">(${item.claim_a.id} via ${item.claim_a.source_id || "unknown"})</span></div>
            <div><strong>B:</strong> <code>${item.claim_b.object_value}</code> <span class="mono-hint">(${item.claim_b.id} via ${item.claim_b.source_id || "unknown"})</span></div>
          </div>
          <div class="mono-hint mt-8">${item.link.note}</div>
        </div>
      `).join("")
    : `<div class="mono-hint">No active contradictions.</div>`;

  // 3. Unknowns
  document.getElementById("unknown-count").textContent = data.unknown.length;
  const unkEl = document.getElementById("unknowns-list");
  unkEl.innerHTML = data.unknown.length
    ? data.unknown.map(u => `
        <div class="item-card">
          <div class="row-between">
            <span class="code-id">${u.subject_id}.${u.relation}</span>
            <span class="badge badge-danger">POLARITY: ${u.polarity}</span>
          </div>
          <div class="mono-hint mt-8">ID: ${u.id} | Guard: ${JSON.stringify(u.uncertainty)}</div>
        </div>
      `).join("")
    : `<div class="mono-hint">No unknown epistemic states recorded.</div>`;

  // 4. Provenance Chain
  const provEl = document.getElementById("provenance-chain");
  provEl.innerHTML = data.provenance.map(node => `
    <div class="prov-step">
      <span class="badge badge-info">${node.kind}</span>
      <span class="code-id">${node.id}</span>
      <span>${node.summary}</span>
    </div>
  `).join("");

  // 5. Concepts & Lineage
  cachedConcepts = data.concepts;
  renderConcepts(cachedConcepts);

  document.getElementById("lineage-tbody").innerHTML = data.lineage.map(edge => `
    <tr>
      <td class="code-id">${edge.from_concept_id}</td>
      <td><span class="badge badge-info">${edge.operation}</span></td>
      <td class="code-id">${edge.to_concept_id}</td>
      <td>${edge.reason}</td>
    </tr>
  `).join("");

  // 6. Inferred & Learned Claims
  document.getElementById("inferred-tbody").innerHTML = data.inferred.map(row => `
    <tr>
      <td class="code-id">${row.claim.id}</td>
      <td class="code-id">${row.claim.subject_id}</td>
      <td>${row.claim.relation}</td>
      <td><code>${row.claim.object_value}</code></td>
      <td class="mono-hint">${row.provenance_trace}</td>
    </tr>
  `).join("");

  document.getElementById("learned-tbody").innerHTML = data.learned.map(c => `
    <tr>
      <td class="code-id">${c.id}</td>
      <td class="code-id">${c.subject_id}</td>
      <td>${c.relation}</td>
      <td><code>${c.object_value}</code></td>
      <td><span class="badge badge-ok">${c.epistemic_state}</span></td>
    </tr>
  `).join("");
}

function renderConcepts(list) {
  document.getElementById("concepts-tbody").innerHTML = list.map(c => {
    const labels = Object.entries(c.labels || {})
      .map(([lang, words]) => `<strong>${lang}:</strong> ${words.join(", ")}`)
      .join(" &nbsp;|&nbsp; ");
    const rules = [
      c.defaults?.length ? `Defaults: ${c.defaults.join(", ")}` : "",
      c.exceptions?.length ? `Exceptions: ${c.exceptions.join(", ")}` : ""
    ].filter(Boolean).join("<br/>") || "—";

    return `
      <tr>
        <td class="code-id">${c.id}</td>
        <td><strong>${c.canonical}</strong></td>
        <td class="mono-hint">v${c.version}</td>
        <td>${labels || "—"}</td>
        <td class="mono-hint">${rules}</td>
      </tr>
    `;
  }).join("");
}

function filterConcepts() {
  const q = document.getElementById("concept-filter").value.toLowerCase();
  const filtered = cachedConcepts.filter(c =>
    c.id.toLowerCase().includes(q) ||
    c.canonical.toLowerCase().includes(q) ||
    JSON.stringify(c.labels).toLowerCase().includes(q)
  );
  renderConcepts(filtered);
}

async function askCRS() {
  const q = document.getElementById("ask-input").value.trim();
  if (!q) return;
  const out = document.getElementById("ask-result");
  out.textContent = "Querying CRS...";
  const res = await fetch(`/api/ask?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
}

async function ingestSentence() {
  const sentence = document.getElementById("ingest-input").value.trim();
  const mode = document.getElementById("ingest-mode").value;
  if (!sentence) return;

  const res = await fetch("/api/ingest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sentence, mode })
  });
  const data = await res.json();
  if (res.ok) {
    showToast("Ingested statement into CRS");
    document.getElementById("ingest-input").value = "";
    loadOverview();
  } else {
    showToast(`Error: ${data.error}`);
  }
}

async function queryTemporal() {
  const subject = document.getElementById("temp-subject").value.trim();
  const dt = document.getElementById("temp-date").value;
  const res = await fetch(`/api/temporal?subject=${encodeURIComponent(subject)}&date=${encodeURIComponent(dt)}`);
  const claims = await res.json();

  const container = document.getElementById("temporal-result");
  container.innerHTML = claims.length
    ? claims.map(c => `
        <div class="item-card">
          <div class="row-between">
            <span class="code-id">${c.relation} = ${c.object_value}</span>
            <span class="badge badge-ok">${c.epistemic_state}</span>
          </div>
          <div class="mono-hint mt-8">Window: ${c.temporal.valid_from || "-∞"} to ${c.temporal.valid_to || "present"}</div>
        </div>
      `).join("")
    : `<div class="mono-hint">No valid claims on ${dt}.</div>`;
}

async function triggerEngine(endpoint, btn) {
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Running...";
  try {
    const res = await fetch(endpoint, { method: "POST" });
    const data = await res.json();
    showToast(`${endpoint.replace("/api/", "").toUpperCase()} completed`);
    console.log(endpoint, data);
    await loadOverview();
  } finally {
    btn.disabled = false;
    btn.textContent = original;
  }
}

document.addEventListener("DOMContentLoaded", loadOverview);