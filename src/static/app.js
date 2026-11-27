const state = {
  nodes: [],
  edges: [],
  activeTypes: new Set(["concept", "entity", "event", "claim"]),
  search: "",
  layout: "force",
  selectedId: null,
  chatHistory: [],
  draggingId: null,
  zoom: 1,
  pan: { x: 0, y: 0 },
  panning: false,
  panStart: { x: 0, y: 0 }
};

const TYPE_COLORS = {
  concept: "#a855f7",
  entity: "#06b6d4",
  event: "#eab308",
  claim: "#ec4899"
};

function toast(msg) {
  const el = document.getElementById("status-toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.add("hidden"), 2600);
}

async function loadGraphData() {
  const res = await fetch("/api/overview");
  const data = await res.json();

  const nodes = [];
  const edges = [];
  const nodeIds = new Set();

  function addNode(n) {
    if (nodeIds.has(n.id)) return;
    nodeIds.add(n.id);
    nodes.push({
      x: 220 + Math.random() * 760,
      y: 120 + Math.random() * 500,
      ...n
    });
  }

  for (const c of data.concepts || []) {
    addNode({
      id: c.id,
      label: c.canonical || c.id,
      type: "concept",
      meta: c
    });
  }

  for (const e of data.entities || []) {
    const lbl = (e.labels && e.labels[0]) || e.id;
    addNode({
      id: e.id,
      label: lbl,
      type: "entity",
      meta: e
    });
    if (e.concept_id && nodeIds.has(e.concept_id)) {
      edges.push({
        id: `edge_${e.id}_${e.concept_id}`,
        from: e.id,
        to: e.concept_id,
        label: "instance_of",
        kind: "membership"
      });
    }
  }

  for (const ev of data.events || []) {
    addNode({
      id: ev.id,
      label: ev.event_type || ev.id,
      type: "event",
      meta: ev
    });
    for (const [role, participantId] of Object.entries(ev.participants || {})) {
      if (nodeIds.has(participantId)) {
        edges.push({
          id: `edge_${ev.id}_${role}_${participantId}`,
          from: ev.id,
          to: participantId,
          label: role,
          kind: "relation"
        });
      }
    }
  }

  for (const row of data.inferred || []) {
    const cl = row.claim;
    addNode({
      id: cl.id,
      label: `${cl.relation}: ${cl.object_value}`,
      type: "claim",
      meta: { ...cl, provenance_trace: row.provenance_trace }
    });
    if (nodeIds.has(cl.subject_id)) {
      edges.push({
        id: `edge_${cl.subject_id}_${cl.id}`,
        from: cl.subject_id,
        to: cl.id,
        label: cl.epistemic_state,
        kind: "relation"
      });
    }
  }

  for (const cl of data.learned || []) {
    addNode({
      id: cl.id,
      label: `${cl.relation}=${cl.object_value}`,
      type: "claim",
      meta: cl
    });
    if (nodeIds.has(cl.subject_id)) {
      edges.push({
        id: `edge_${cl.subject_id}_${cl.id}`,
        from: cl.subject_id,
        to: cl.id,
        label: "learned",
        kind: "relation"
      });
    }
  }

  for (const u of data.unknown || []) {
    addNode({
      id: u.id,
      label: `${u.relation}?`,
      type: "claim",
      meta: u
    });
    if (nodeIds.has(u.subject_id)) {
      edges.push({
        id: `edge_${u.subject_id}_${u.id}`,
        from: u.subject_id,
        to: u.id,
        label: "UNKNOWN",
        kind: "conflict"
      });
    }
  }

  for (const pair of data.contradictions || []) {
    const a = pair.claim_a;
    const b = pair.claim_b;
    for (const cl of [a, b]) {
      addNode({
        id: cl.id,
        label: `${cl.relation}: ${cl.object_value}`,
        type: "claim",
        meta: cl
      });
      if (nodeIds.has(cl.subject_id)) {
        edges.push({
          id: `edge_${cl.subject_id}_${cl.id}`,
          from: cl.subject_id,
          to: cl.id,
          label: cl.relation,
          kind: "relation"
        });
      }
    }
    edges.push({
      id: pair.link.id,
      from: a.id,
      to: b.id,
      label: "contradicts",
      kind: "conflict",
      meta: pair.link
    });
  }

  for (const edge of data.lineage || []) {
    if (nodeIds.has(edge.from_concept_id) && nodeIds.has(edge.to_concept_id)) {
      edges.push({
        id: `lin_${edge.from_concept_id}_${edge.to_concept_id}`,
        from: edge.from_concept_id,
        to: edge.to_concept_id,
        label: edge.operation,
        kind: "lineage",
        meta: edge
      });
    }
  }

  state.nodes = nodes;
  state.edges = edges;
  computeLayout(state.layout);
  renderGraph();
}

function getFilteredGraph() {
  const q = state.search.trim().toLowerCase();
  const visibleNodes = state.nodes.filter(n => {
    if (!state.activeTypes.has(n.type)) return false;
    if (!q) return true;
    return (
      n.label.toLowerCase().includes(q) ||
      n.id.toLowerCase().includes(q) ||
      JSON.stringify(n.meta).toLowerCase().includes(q)
    );
  });
  const ids = new Set(visibleNodes.map(n => n.id));
  const visibleEdges = state.edges.filter(e => ids.has(e.from) && ids.has(e.to));
  return { visibleNodes, visibleEdges };
}

function computeLayout(mode) {
  const { visibleNodes, visibleEdges } = getFilteredGraph();
  const W = 1200, H = 760;

  if (mode === "circle") {
    const cx = W / 2, cy = H / 2, r = Math.min(W, H) * 0.36;
    visibleNodes.forEach((n, i) => {
      const angle = (2 * Math.PI * i) / Math.max(visibleNodes.length, 1);
      n.x = cx + r * Math.cos(angle);
      n.y = cy + r * Math.sin(angle);
    });
    return;
  }

  if (mode === "grid") {
    const cols = Math.max(1, Math.ceil(Math.sqrt(visibleNodes.length * 1.4)));
    const padX = 140, padY = 110;
    visibleNodes.forEach((n, i) => {
      const col = i % cols;
      const row = Math.floor(i / cols);
      n.x = padX + col * ((W - padX * 2) / Math.max(cols - 1, 1));
      n.y = padY + row * 125;
    });
    return;
  }

  const byId = Object.fromEntries(visibleNodes.map(n => [n.id, n]));
  for (let iter = 0; iter < 140; iter++) {
    for (let i = 0; i < visibleNodes.length; i++) {
      for (let j = i + 1; j < visibleNodes.length; j++) {
        const a = visibleNodes[i], b = visibleNodes[j];
        let dx = b.x - a.x, dy = b.y - a.y;
        const dist2 = dx * dx + dy * dy + 1;
        const force = 6200 / dist2;
        const dist = Math.sqrt(dist2);
        dx = (dx / dist) * force;
        dy = (dy / dist) * force;
        a.x -= dx; a.y -= dy;
        b.x += dx; b.y += dy;
      }
    }
    for (const e of visibleEdges) {
      const a = byId[e.from], b = byId[e.to];
      if (!a || !b) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const pull = (dist - 125) * 0.035;
      const fx = (dx / dist) * pull;
      const fy = (dy / dist) * pull;
      a.x += fx; a.y += fy;
      b.x -= fx; b.y -= fy;
    }
    for (const n of visibleNodes) {
      n.x += (W / 2 - n.x) * 0.012;
      n.y += (H / 2 - n.y) * 0.012;
      n.x = Math.max(80, Math.min(W - 80, n.x));
      n.y = Math.max(60, Math.min(H - 60, n.y));
    }
  }
}

function renderGraph() {
  const { visibleNodes, visibleEdges } = getFilteredGraph();
  document.getElementById("graph-counter").textContent =
    `${visibleNodes.length} nodes · ${visibleEdges.length} edges`;

  const byId = Object.fromEntries(visibleNodes.map(n => [n.id, n]));
  const edgesLayer = document.getElementById("edges-layer");
  const labelsLayer = document.getElementById("edge-labels-layer");
  const nodesLayer = document.getElementById("nodes-layer");

  edgesLayer.innerHTML = "";
  labelsLayer.innerHTML = "";
  nodesLayer.innerHTML = "";

  const transform = `translate(${state.pan.x}, ${state.pan.y}) scale(${state.zoom})`;
  edgesLayer.setAttribute("transform", transform);
  labelsLayer.setAttribute("transform", transform);
  nodesLayer.setAttribute("transform", transform);

  for (const e of visibleEdges) {
    const a = byId[e.from], b = byId[e.to];
    if (!a || !b) continue;

    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const distance = Math.hypot(dx, dy) || 1;
    const sourcePadding = a.type === "concept" ? 12 : 11;
    const targetPadding = b.type === "concept" ? 12 : 11;

    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", a.x + dx / distance * sourcePadding);
    line.setAttribute("y1", a.y + dy / distance * sourcePadding);
    line.setAttribute("x2", b.x - dx / distance * targetPadding);
    line.setAttribute("y2", b.y - dy / distance * targetPadding);
    line.setAttribute(
      "class",
      `edge-line ${e.kind === "membership" ? "membership" : ""} ${e.kind === "conflict" ? "conflict" : ""} ${e.kind === "lineage" ? "lineage" : ""}`
    );
    line.setAttribute(
      "marker-end",
      e.kind === "conflict" ? "url(#arrow-conflict)" : "url(#arrow)"
    );
    const edgeTitle = document.createElementNS("http://www.w3.org/2000/svg", "title");
    edgeTitle.textContent = `${a.label} ${e.label} ${b.label}`;
    line.appendChild(edgeTitle);
    line.onclick = () => selectEdge(e);
    edgesLayer.appendChild(line);

    const txt = document.createElementNS("http://www.w3.org/2000/svg", "text");
    txt.setAttribute("x", (a.x + b.x) / 2);
    txt.setAttribute("y", (a.y + b.y) / 2 - 4);
    txt.setAttribute("text-anchor", "middle");
    txt.setAttribute("class", `edge-label ${e.kind === "membership" ? "membership-label" : ""}`);
    txt.textContent = e.label;
    labelsLayer.appendChild(txt);
  }

  for (const n of visibleNodes) {
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("class", `node-group ${state.selectedId === n.id ? "selected" : ""}`);
    g.setAttribute("transform", `translate(${n.x}, ${n.y})`);

    const color = TYPE_COLORS[n.type] || "#22c55e";
    let shapeEl;

    if (n.type === "concept") {
      shapeEl = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      shapeEl.setAttribute("points", "0,-10 10,0 0,10 -10,0");
    } else if (n.type === "claim") {
      shapeEl = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      shapeEl.setAttribute("x", "-8");
      shapeEl.setAttribute("y", "-8");
      shapeEl.setAttribute("width", "16");
      shapeEl.setAttribute("height", "16");
      shapeEl.setAttribute("rx", "2");
    } else {
      shapeEl = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      shapeEl.setAttribute("r", "8");
    }

    shapeEl.setAttribute("fill", color);
    shapeEl.setAttribute("class", "node-shape");

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("y", "21");
    label.textContent = n.label.length > 26 ? n.label.slice(0, 24) + "…" : n.label;

    g.onmousedown = ev => {
      ev.stopPropagation();
      state.draggingId = n.id;
      selectNode(n);
    };

    g.appendChild(shapeEl);
    g.appendChild(label);
    nodesLayer.appendChild(g);
  }
}

function selectNode(n) {
  state.selectedId = n.id;
  renderGraph();

  const outgoing = state.edges.filter(e => e.from === n.id);
  const incoming = state.edges.filter(e => e.to === n.id);

  document.getElementById("details-content").innerHTML = `
    <div class="detail-heading">${n.label}</div>
    <div class="detail-sub">${n.type.toUpperCase()} · ${n.id}</div>
    <div class="prop-block">
      <div class="prop-key">Outgoing (${outgoing.length})</div>
      <div class="prop-val">${outgoing.map(e => `→ ${e.label} → ${e.to}`).join("<br/>") || "None"}</div>
    </div>
    <div class="prop-block">
      <div class="prop-key">Incoming (${incoming.length})</div>
      <div class="prop-val">${incoming.map(e => `← ${e.label} ← ${e.from}`).join("<br/>") || "None"}</div>
    </div>
    <div class="prop-block">
      <div class="prop-key">Metadata</div>
      <div class="prop-val"><pre style="white-space:pre-wrap;font-family:var(--font-mono);font-size:10px">${JSON.stringify(n.meta, null, 2)}</pre></div>
    </div>
  `;
}

function selectEdge(e) {
  document.getElementById("details-content").innerHTML = `
    <div class="detail-heading">${e.label}</div>
    <div class="detail-sub">${e.from} → ${e.to}</div>
    <div class="prop-block">
      <div class="prop-key">Edge Type</div>
      <div class="prop-val">${e.kind}</div>
    </div>
    ${e.meta ? `<div class="prop-block"><div class="prop-key">Details</div><div class="prop-val">${JSON.stringify(e.meta)}</div></div>` : ""}
  `;
}

function clearSelection() {
  state.selectedId = null;
  renderGraph();
  document.getElementById("details-content").innerHTML =
    `<div class="details-empty">Click any node or edge to inspect properties, connections, and epistemic state.</div>`;
}

function toggleType(type, btn) {
  if (state.activeTypes.has(type)) {
    state.activeTypes.delete(type);
    btn.classList.remove("active");
  } else {
    state.activeTypes.add(type);
    btn.classList.add("active");
  }
  computeLayout(state.layout);
  renderGraph();
}

function applyFilters() {
  state.search = document.getElementById("search-input").value;
  computeLayout(state.layout);
  renderGraph();
}

function setLayout(mode, btn) {
  state.layout = mode;
  document.querySelectorAll(".layout-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  computeLayout(mode);
  renderGraph();
}

function zoomBy(factor) {
  state.zoom = Math.max(0.4, Math.min(2.5, state.zoom * factor));
  renderGraph();
}

function resetZoom() {
  state.zoom = 1;
  state.pan = { x: 0, y: 0 };
  renderGraph();
}

async function askGraph() {
  const q = document.getElementById("ask-input").value.trim();
  if (!q) return;
  const box = document.getElementById("ask-box");
  box.classList.remove("hidden");
  box.textContent = "Querying...";
  const res = await fetch(`/api/ask?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  box.textContent = data.answer || JSON.stringify(data, null, 2);
}

function appendChatMessage(role, text) {
  const item = document.createElement("div");
  item.className = `chat-message ${role}`;

  if (role !== "system") {
    const speaker = document.createElement("div");
    speaker.className = "chat-role";
    speaker.textContent = role === "user" ? "You" : "Qwen";
    item.appendChild(speaker);
  }

  const content = document.createElement("div");
  content.className = "chat-copy";
  content.textContent = text;
  item.appendChild(content);

  const messages = document.getElementById("chat-messages");
  messages.appendChild(item);
  messages.scrollTop = messages.scrollHeight;
}

async function sendChat(event) {
  event.preventDefault();
  const input = document.getElementById("chat-input");
  const button = document.getElementById("chat-send");
  const status = document.getElementById("chat-status");
  const message = input.value.trim();
  if (!message) return;

  appendChatMessage("user", message);
  input.value = "";
  button.disabled = true;
  status.textContent = "Waiting for Qwen...";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: state.chatHistory })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Grok request failed.");

    const reply = typeof data.reply === "string" ? data.reply : "I couldn't form a response.";
    state.chatHistory.push(
      { role: "user", content: message },
      { role: "assistant", content: reply }
    );
    appendChatMessage("assistant", reply);

    const added = data.added || {};
    const concepts = Array.isArray(added.concepts) ? added.concepts : [];
    const entities = Array.isArray(added.entities) ? added.entities : [];
    const graphUpdates = [];
    if (concepts.length) graphUpdates.push(`${concepts.length} concept${concepts.length === 1 ? "" : "s"}`);
    if (entities.length) graphUpdates.push(`${entities.length} entit${entities.length === 1 ? "y" : "ies"}`);
    if (graphUpdates.length) {
      appendChatMessage("system", `Added ${graphUpdates.join(" and ")} to the graph.`);
      await loadGraphData();
    }
    status.textContent = data.model ? `Connected · ${data.model}` : "Connected to Qwen";
  } catch (error) {
    const message = error instanceof Error ? error.message : "Qwen request failed.";
    appendChatMessage("error", message);
    status.textContent = "Qwen is unavailable";
  } finally {
    button.disabled = false;
    input.focus();
  }
}

async function ingestText() {
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
    document.getElementById("ingest-input").value = "";
    toast("Ingested into CRS");
    await loadGraphData();
  } else {
    toast(data.error || "Ingest failed");
  }
}

async function runAction(endpoint, label) {
  const res = await fetch(endpoint, { method: "POST" });
  const data = await res.json();
  toast(res.ok ? `${label} complete` : (data.error || `${label} failed`));
  await loadGraphData();
}

document.addEventListener("DOMContentLoaded", () => {
  const svg = document.getElementById("graph-svg");
  svg.addEventListener("mousedown", ev => {
    if (ev.target === svg) {
      state.panning = true;
      state.panStart = { x: ev.clientX - state.pan.x, y: ev.clientY - state.pan.y };
    }
  });
  window.addEventListener("mousemove", ev => {
    if (state.draggingId) {
      const node = state.nodes.find(n => n.id === state.draggingId);
      if (node) {
        const rect = svg.getBoundingClientRect();
        node.x = ((ev.clientX - rect.left) * (1200 / rect.width) - state.pan.x) / state.zoom;
        node.y = ((ev.clientY - rect.top) * (760 / rect.height) - state.pan.y) / state.zoom;
        renderGraph();
      }
    } else if (state.panning) {
      state.pan.x = ev.clientX - state.panStart.x;
      state.pan.y = ev.clientY - state.panStart.y;
      renderGraph();
    }
  });
  window.addEventListener("mouseup", () => {
    state.draggingId = null;
    state.panning = false;
  });

  loadGraphData();
});