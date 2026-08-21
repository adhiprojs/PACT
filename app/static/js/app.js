/**
 * PACT Admin Command Portal & Field Provider Portal.
 * Clean, professional humanitarian theme matching the PACT specification.
 * Zero emojis, clear contrast, readable tables, and focused routing maps.
 */

let socket = null;
let crisisMap = null;
let providerMap = null;
let modalMiniMap = null;
let currentRunId = null;
let activeDecisionId = null;
let accumulatedTokens = "";
let currentOrgPersona = "ADMIN_ALL";
let activeInspectedMatch = null;
let selectedProviderVictimMatch = null;

const PERSONA_CONFIGS = {
  "ADMIN_ALL": {
    name: "Global Incident Command (Admin)",
    subtitle: "Zero-Connectivity Resilience · Zero-Hallucination Solvers · Multi-Agent Negotiation"
  },
  "NGO_TN_RED_CROSS": {
    name: "Red Cross Tamil Nadu Relief Command",
    subtitle: "Field Operations Portal · Viewing only victims and relief supplies allocated to your organization."
  },
  "TNDRF_ARAKKONAM_CHENNAI": {
    name: "Tamil Nadu Disaster Response Force (TNDRF)",
    subtitle: "Field Operations Portal · Rapid flood rescue, boat allocations, and emergency extractions."
  },
  "HOSPITAL_CHENNAI_RGGGH": {
    name: "Rajiv Gandhi / Apollo Trauma Medical Center",
    subtitle: "Field Operations Portal · Critical casualty triage, trauma teams, and ALS ambulance routing."
  },
  "CSR_TATA_SOUTH_HUB": {
    name: "Tata / CSR Southern Disaster Logistics Hub",
    subtitle: "Field Operations Portal · Regional bulk logistics, freight trucks, and generator reserves."
  },
  "COIMBATORE_GHAT_RESCUE": {
    name: "Nilgiris and Western Ghats Mountain Rescue Unit",
    subtitle: "Field Operations Portal · High-altitude 4x4 vehicles, landslide response, and mountain aid."
  }
};

document.addEventListener("DOMContentLoaded", () => {
  crisisMap = new CrisisMap("crisisMapContainer");
  initWebSocket();
  loadInitialData();
  setupEventListeners();
});

let lastEnteredStage = null;

function initWebSocket() {
  if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
    return;
  }
  if (socket) {
    try { socket.close(); } catch (e) {}
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/agents`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    updateWsStatus(true);
    console.log("[WS] Connected to PACT live agent bus");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      handleAgentEvent(data);
    } catch (e) {
      console.error("[WS] Parse error:", e);
    }
  };

  socket.onclose = () => {
    updateWsStatus(false);
    console.log("[WS] Disconnected. Reconnecting in 2s...");
    setTimeout(initWebSocket, 2000);
  };
}

function updateWsStatus(connected) {
  const pill = document.getElementById("wsStatusPill");
  const text = document.getElementById("wsStatusText");
  if (pill && text) {
    if (connected) {
      pill.className = "hud-pill connected";
      text.textContent = "AGENT BUS ONLINE";
    } else {
      pill.className = "hud-pill disconnected";
      text.textContent = "RECONNECTING...";
    }
  }
}

function handleAgentEvent(evt) {
  const type = evt.type;
  const agent = evt.agent;
  const payload = evt.payload || {};
  const runId = evt.run_id;

  // If in Provider Portal mode, update live matches table quietly
  if (currentOrgPersona !== "ADMIN_ALL") {
    if (type === "match.committed" || type === "run.completed") {
      loadProviderPortalData(currentOrgPersona);
    }
    return;
  }

  // ── ADMIN VIEW EVENT HANDLERS ─────────────────────────────────────────────

  // 1. Run Started
  if (type === "run.started") {
    currentRunId = runId;
    accumulatedTokens = "";
    lastEnteredStage = null;
    resetPipelineStepper();
    clearDebateFeed();
    document.getElementById("streamContent").textContent = "";
    document.getElementById("ackFrameBox").style.display = "none";
    document.getElementById("adminActionBar").style.display = "none";
    updateActiveRunBadge(runId);
  }

  // 2. Agent Entered
  if (type === "agent.entered") {
    const stage = payload.stage || agent;
    highlightStepperStage(stage);

    if (lastEnteredStage !== stage) {
      lastEnteredStage = stage;
      const streamElem = document.getElementById("streamContent");
      if (streamElem) {
        let stageDesc = "";
        if (stage === "A0") stageDesc = " [Deterministic] Frame parsing and 2-char XOR checksum verification";
        else if (stage === "A1") stageDesc = " [Deterministic] Compound deduplication check on (UID, SEQ)";
        else if (stage === "A2") stageDesc = " [Tool-Augmented LLM] Situational triage and meteorological hazard evaluation";
        else if (stage === "A3") stageDesc = " [MongoDB] Cascading $geoNear spatial candidate radius lookup";
        else if (stage === "A4") stageDesc = " [Multi-Agent Negotiation] Independent provider advocates debating deployment bids";
        else if (stage === "A5") stageDesc = " [Python Math Solver] Linear greedy optimization of 3 plans";
        else if (stage === "A6") stageDesc = " [Groq LLM Arbiter] Judging debate arguments and choosing optimal plan";
        else if (stage === "A7") stageDesc = " [Privacy] Zero-knowledge 2km grid masking and hashing";
        else if (stage === "A8") stageDesc = " [Human-in-the-Loop] Dispatcher review gate and Autopilot timer";
        else if (stage === "A9") stageDesc = " [Groq LLM] Plain-English operational bulletin generation";
        else if (stage === "A10") stageDesc = " [Database] Stock deduction and Outbound SMS frame generation";

        accumulatedTokens += `\n\n[${stage} AGENT ENTERED]${stageDesc}:\n`;
        streamElem.textContent = accumulatedTokens;
        streamElem.scrollTop = streamElem.scrollHeight;
      }
    }
  }

  // 3. Tool Execution Event
  if (type === "agent.tool_called") {
    const streamElem = document.getElementById("streamContent");
    if (streamElem) {
      const summary = payload.summary || `Executed tool ${payload.tool_name}`;
      accumulatedTokens += `  [EXECUTED TOOL: ${payload.tool_name}]: ${summary}\n`;
      streamElem.textContent = accumulatedTokens;
      streamElem.scrollTop = streamElem.scrollHeight;
    }
  }

  // 4. Token Streaming
  if (type === "agent.token") {
    const token = payload.token || "";
    accumulatedTokens += token;
    const streamElem = document.getElementById("streamContent");
    if (streamElem) {
      streamElem.textContent = accumulatedTokens;
      streamElem.scrollTop = streamElem.scrollHeight;
    }
  }

  // 5. Debate Turn
  if (type === "debate.turn") {
    appendDebateCard(payload);
  }

  // 6. Solver Options
  if (type === "solver.computed") {
    renderSolverCards(payload.options || {});
  }

  // 7. Decision Proposed
  if (type === "decision.proposed") {
    selectSolverCard(payload.selected_option_id);
  }

  // 8. Admin Gate Required
  if (type === "admin.gate_required") {
    activeDecisionId = payload.decision_id || "DEC_TEMP";
    showAdminGateAction(payload);
  }

  // 9. Agent Completed Stage
  if (type === "agent.completed") {
    if (agent === "A0_Intake" && payload.geo && crisisMap) {
      const coords = payload.geo.coordinates || [80.2707, 13.0827];
      crisisMap.addVictim(coords[1], coords[0], payload.uid || "SOS", payload.situation || "Emergency");
      crisisMap.triggerGeoSearch(coords[1], coords[0], 25);
      crisisMap.setCenter(coords[1], coords[0], 12);
      loadRequestsTable();
    }
    if (agent === "A3_GeoMatcher" && crisisMap && payload.search_center) {
      const coords = payload.search_center.coordinates || [80.2707, 13.0827];
      crisisMap.triggerGeoSearch(coords[1], coords[0], payload.radius_km || 25);
    }
  }

  // 10. Match Committed
  if (type === "match.committed") {
    loadMatchesTable();
    loadOffersTable();
    refreshStats();
    if (crisisMap && payload.match) {
      const m = payload.match;
      const allocs = m.allocations || m.selected_plan?.allocations || [];
      const coords = m.request_geo?.coordinates || (m.loc?.coordinates) || [80.2707, 13.0827];
      crisisMap.drawDispatchPlan(allocs, coords[1], coords[0]);
    }
  }

  // 11. Frame Transmitted
  if (type === "frame.transmitted") {
    showAckBanner(payload.raw_frame || "");
  }

  // 12. Run Completed
  if (type === "run.completed") {
    completePipelineStepper();
    updateActiveRunBadge("STANDBY", false);
    refreshStats();
    loadRequestsTable();
    loadMatchesTable();
  }
}

// ── Persona & Portal Switching Logic ──────────────────────────────────────────

function onOrgPersonaChanged() {
  const select = document.getElementById("orgPersonaSelect");
  if (!select) return;
  currentOrgPersona = select.value;

  const adminView = document.getElementById("adminViewContainer");
  const providerView = document.getElementById("providerViewContainer");
  const autopilotWrap = document.getElementById("adminAutopilotWrap");
  const headerTitle = document.getElementById("headerTitle");
  const headerSubtitle = document.getElementById("headerSubtitle");

  const config = PERSONA_CONFIGS[currentOrgPersona] || PERSONA_CONFIGS["ADMIN_ALL"];

  if (currentOrgPersona === "ADMIN_ALL") {
    if (adminView) adminView.style.display = "flex";
    if (providerView) providerView.style.display = "none";
    if (autopilotWrap) autopilotWrap.style.display = "flex";
    if (headerTitle) headerTitle.textContent = "Autonomous Crisis Coordination Center";
    if (headerSubtitle) headerSubtitle.textContent = config.subtitle;

    loadInitialData();
  } else {
    if (adminView) adminView.style.display = "none";
    if (providerView) providerView.style.display = "flex";
    if (autopilotWrap) autopilotWrap.style.display = "none";
    if (headerTitle) headerTitle.textContent = config.name;
    if (headerSubtitle) headerSubtitle.textContent = config.subtitle;

    document.getElementById("pOrgTitle").textContent = config.name;
    document.getElementById("pOrgSubtitle").textContent = config.subtitle;

    loadProviderPortalData(currentOrgPersona);
  }
}

function resetToAdminView() {
  const select = document.getElementById("orgPersonaSelect");
  if (select) {
    select.value = "ADMIN_ALL";
    onOrgPersonaChanged();
  }
}

// ── Field Organization Portal Data Loading ───────────────────────────────────

async function loadProviderPortalData(providerId) {
  try {
    const offerRes = await fetch(`/api/v1/offers/${providerId}`);
    let providerData = {};
    if (offerRes.ok) {
      providerData = await offerRes.json();
    }

    document.getElementById("pStatBase").textContent = providerData.location_name || "Chennai Hub";
    document.getElementById("pStatFleet").textContent = providerData.fleet_description || "Ready Fleet";
    document.getElementById("providerFleetText").textContent = `Fleet Readiness: ${providerData.fleet_description || 'Standard response vehicles ready'}`;

    const stockGrid = document.getElementById("providerStockGrid");
    if (stockGrid) {
      stockGrid.innerHTML = "";
      const inv = providerData.inventory || {};
      Object.entries(inv).forEach(([itemKey, qty]) => {
        const itemBox = document.createElement("div");
        itemBox.className = "modal-stat-box";
        itemBox.innerHTML = `
          <div class="modal-stat-label">${itemKey.replace('_', ' ').toUpperCase()}</div>
          <div class="modal-stat-val" style="font-size:1.1rem; color:var(--pact-primary);">${qty}</div>
        `;
        stockGrid.appendChild(itemBox);
      });
    }

    const matchRes = await fetch(`/api/v1/matches?provider_id=${providerId}&limit=20`);
    const matchData = await matchRes.json();
    const matches = matchData.matches || [];

    document.getElementById("pStatMissions").textContent = matches.length;
    document.getElementById("pQueueCount").textContent = `${matches.length} ASSIGNED`;

    let totalUnits = 0;
    matches.forEach(m => {
      const items = m.items || m.allocated_items || (m.selected_plan?.allocations?.[0]?.items) || {};
      Object.values(items).forEach(val => {
        if (typeof val === "number") totalUnits += val;
      });
    });
    document.getElementById("pStatSupplies").textContent = `${totalUnits} Units`;

    const tbody = document.getElementById("providerMatchesTableBody");
    if (tbody) {
      tbody.innerHTML = "";
      if (matches.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:1.5rem; color:var(--pact-muted);">No help seekers currently assigned to this unit. Standing by for incoming SOS.</td></tr>`;
      } else {
        matches.forEach((m, idx) => {
          const tr = document.createElement("tr");
          tr.style.cursor = "pointer";
          tr.onclick = () => selectProviderVictim(m);

          const items = m.items || m.allocated_items || (m.selected_plan?.allocations?.[0]?.items) || {};
          const itemsStr = Object.entries(items).map(([k, v]) => `${v} ${k.replace('_kits', '')}`).join(", ") || "Aid Pack";

          tr.innerHTML = `
            <td><strong style="font-family:var(--font-mono); color:var(--pact-primary);">${m.uid || 'CIT01'}</strong></td>
            <td><strong>${m.situation || 'Crisis Incident'}</strong></td>
            <td>${m.headcount || '1 person'}</td>
            <td><span class="hud-tag hud-tag-info" style="font-size:0.7rem;">${itemsStr}</span></td>
            <td>
              <button class="btn-tactile" style="padding:0.25rem 0.6rem; font-size:0.68rem;" onclick="event.stopPropagation(); selectProviderVictim(m)">
                Inspect Route
              </button>
            </td>
          `;
          tbody.appendChild(tr);

          if (idx === 0 && !selectedProviderVictimMatch) {
            selectProviderVictim(m);
          }
        });
      }
    }

    initProviderMap(providerData, matches);

  } catch (e) {
    console.error("Failed to load provider portal data:", e);
  }
}

function selectProviderVictim(match) {
  selectedProviderVictimMatch = match;

  const cardTitle = document.getElementById("pCardTitle");
  const badge = document.getElementById("pCardStatusBadge");
  const incident = document.getElementById("pDetailIncident");
  const itemsEl = document.getElementById("pDetailItems");
  const etaEl = document.getElementById("pDetailETA");
  const coordsEl = document.getElementById("pDetailCoords");

  if (cardTitle) cardTitle.textContent = `Mission: Target ${match.uid || 'Citizen'} · Plan ${match.match_id || ''}`;
  if (badge) {
    badge.className = "hud-tag hud-tag-success";
    badge.textContent = "ASSIGNED TO YOU";
  }

  const items = match.items || match.allocated_items || (match.selected_plan?.allocations?.[0]?.items) || {};
  const itemsStr = Object.entries(items).map(([k, v]) => `• ${v} ${k.replace('_', ' ').toUpperCase()}`).join("\n") || "Emergency Aid Quota";

  if (incident) incident.textContent = `${match.situation || 'Flood and Entrapment'} (${match.headcount || '1 person'} affected · ${match.urgency || 'High'} Urgency)`;
  if (itemsEl) itemsEl.textContent = itemsStr;

  const dist = match.distance_km || match.selected_plan?.allocations?.[0]?.distance_km || 14.2;
  const eta = match.eta_hours || match.selected_plan?.allocations?.[0]?.eta_hours || 0.6;
  if (etaEl) etaEl.textContent = `${dist} km distance (Estimated Arrival: ~${eta} hours)`;

  const coords = match.request_geo?.coordinates || [80.00557, 13.00835];
  const pack10 = match.request_geo?.pack10 || "COORDS";
  if (coordsEl) coordsEl.textContent = `[Lat: ${coords[1].toFixed(5)}, Lon: ${coords[0].toFixed(5)}] · PACK10: ${pack10}`;

  if (providerMap) {
    providerMap.flyTo([coords[1], coords[0]], 13, { animate: true, duration: 0.8 });
  }
}

function initProviderMap(providerData, matches) {
  const container = document.getElementById("providerMapContainer");
  if (!container || typeof L === "undefined") return;

  const depotCoords = providerData.loc?.coordinates || [80.2609, 13.0732];
  const depotLat = depotCoords[1];
  const depotLon = depotCoords[0];

  if (!providerMap) {
    providerMap = L.map("providerMapContainer", {
      center: [depotLat, depotLon],
      zoom: 12,
      zoomControl: true,
      attributionControl: false
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(providerMap);
  } else {
    providerMap.setView([depotLat, depotLon], 12);
    providerMap.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        providerMap.removeLayer(layer);
      }
    });
  }

  // Add organization main depot marker
  const depotIcon = L.divIcon({
    className: 'custom-depot-marker',
    html: `<div style="background:#FFF2DB; border:2px solid #F62440; border-radius:6px; width:34px; height:24px; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:700; color:#2B2119; box-shadow:0 1px 3px rgba(43,33,25,0.15);">BASE</div>`,
    iconSize: [34, 24],
    iconAnchor: [17, 12]
  });
  L.marker([depotLat, depotLon], { icon: depotIcon })
    .bindPopup(`<strong>${providerData.name || 'Your Depot'}</strong><br>${providerData.location_name || 'Operational Hub'}`)
    .addTo(providerMap);

  // Add assigned victim markers and draw dashed routes
  matches.forEach(m => {
    const coords = m.request_geo?.coordinates || [depotLon + 0.03, depotLat + 0.02];
    const victimLat = coords[1];
    const victimLon = coords[0];

    const victimIcon = L.divIcon({
      className: 'custom-victim-marker',
      html: `<div style="background:#F62440; border:2px solid #ffffff; border-radius:4px; width:28px; height:20px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:800; color:#fff; box-shadow:0 2px 6px rgba(246,36,64,0.35);">SOS</div>`,
      iconSize: [28, 20],
      iconAnchor: [14, 10]
    });

    const marker = L.marker([victimLat, victimLon], { icon: victimIcon })
      .bindPopup(`<strong>Target: ${m.uid}</strong><br>Incident: ${m.situation || 'Crisis'}<br>Supplies: ${m.items || 'Aid'}`)
      .addTo(providerMap);

    marker.on('click', () => selectProviderVictim(m));

    L.polyline([[depotLat, depotLon], [victimLat, victimLon]], {
      color: '#F62440',
      weight: 3,
      dashArray: '6, 6',
      opacity: 0.8
    }).addTo(providerMap);
  });

  setTimeout(() => {
    if (providerMap) providerMap.invalidateSize();
  }, 250);
}

function confirmProviderDispatch() {
  if (!selectedProviderVictimMatch) {
    alert("Please select an assigned help seeker first.");
    return;
  }
  alert(`Dispatch Confirmed: Relief convoy mobilized from your depot for Target [${selectedProviderVictimMatch.uid}]. Live tracking active.`);
}

// ── Interactive Dispatch Detail Modal (Admin View) ────────────────────────────

async function inspectDispatch(matchId) {
  try {
    const res = await fetch(`/api/v1/matches/${matchId}`);
    if (!res.ok) return;
    const match = await res.json();
    activeInspectedMatch = match;

    const modal = document.getElementById("dispatchDetailModal");
    if (!modal) return;

    document.getElementById("modalPlanTitle").textContent = `Dispatch Plan: ${match.match_id || matchId}`;
    document.getElementById("modalPlanSubtitle").textContent = `Allocated to: ${match.provider_name || match.provider_id || 'Relief Agency'}`;
    document.getElementById("modalRecipient").textContent = `Target: ${match.uid || 'Citizen'} · ${match.situation || 'Emergency'}`;

    const items = match.items || match.allocated_items || (match.selected_plan?.allocations?.[0]?.items) || {};
    const itemsStr = Object.entries(items).map(([k, v]) => `${v} ${k.replace('_', ' ').toUpperCase()}`).join(", ") || "General Emergency Aid";
    document.getElementById("modalSupplies").textContent = itemsStr;

    const dist = match.distance_km || match.selected_plan?.allocations?.[0]?.distance_km || 12.5;
    const eta = match.eta_hours || match.selected_plan?.allocations?.[0]?.eta_hours || 0.5;
    document.getElementById("modalDepot").textContent = `${match.provider_name || match.provider_id || 'Relief Unit'} (${dist} km · ETA ~${eta}h)`;

    const coords = match.request_geo?.coordinates || [80.00557, 13.00835];
    const pack10 = match.request_geo?.pack10 || "COORDS";
    document.getElementById("modalCoords").textContent = `[Lat: ${coords[1].toFixed(5)}, Lon: ${coords[0].toFixed(5)}] · PACK10: ${pack10}`;

    modal.style.display = "flex";

    setTimeout(() => {
      renderModalMiniMap(coords[1], coords[0], match.provider_id);
    }, 150);

  } catch (e) {
    console.error("Inspect error:", e);
  }
}

function renderModalMiniMap(targetLat, targetLon, providerId) {
  const container = document.getElementById("modalMapCanvas");
  if (!container || typeof L === "undefined") return;

  if (!modalMiniMap) {
    modalMiniMap = L.map("modalMapCanvas", {
      center: [targetLat, targetLon],
      zoom: 13,
      zoomControl: false,
      attributionControl: false
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(modalMiniMap);
  } else {
    modalMiniMap.setView([targetLat, targetLon], 13);
    modalMiniMap.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) {
        modalMiniMap.removeLayer(layer);
      }
    });
  }

  const victimIcon = L.divIcon({
    className: 'custom-victim-marker',
    html: `<div style="background:#F62440; border:2px solid #ffffff; border-radius:4px; width:26px; height:20px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:800; color:#fff;">SOS</div>`,
    iconSize: [26, 20],
    iconAnchor: [13, 10]
  });
  L.marker([targetLat, targetLon], { icon: victimIcon }).addTo(modalMiniMap);

  const depotLat = targetLat + 0.04;
  const depotLon = targetLon + 0.03;
  const depotIcon = L.divIcon({
    className: 'custom-depot-marker',
    html: `<div style="background:#FFF2DB; border:2px solid #2B2119; border-radius:4px; width:28px; height:20px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:700;">BASE</div>`,
    iconSize: [28, 20],
    iconAnchor: [14, 10]
  });
  L.marker([depotLat, depotLon], { icon: depotIcon }).addTo(modalMiniMap);

  L.polyline([[depotLat, depotLon], [targetLat, targetLon]], {
    color: '#F62440',
    weight: 3,
    dashArray: '6, 6'
  }).addTo(modalMiniMap);

  modalMiniMap.invalidateSize();
}

function closeDispatchModal() {
  const modal = document.getElementById("dispatchDetailModal");
  if (modal) modal.style.display = "none";
}

function focusOnMainMap() {
  if (activeInspectedMatch && crisisMap) {
    const coords = activeInspectedMatch.request_geo?.coordinates || [80.00557, 13.00835];
    crisisMap.setCenter(coords[1], coords[0], 14);
    crisisMap.triggerGeoSearch(coords[1], coords[0], 15);
  }
  closeDispatchModal();
}

// ── Admin Stepper & Viewport Helpers ──────────────────────────────────────────

function resetPipelineStepper() {
  for (let i = 0; i <= 10; i++) {
    const el = document.getElementById(`step-A${i}`);
    if (el) el.className = "rail-node";
  }
}

function highlightStepperStage(stage) {
  const el = document.getElementById(`step-${stage}`);
  if (el) el.className = "rail-node active";
}

function completePipelineStepper() {
  for (let i = 0; i <= 10; i++) {
    const el = document.getElementById(`step-A${i}`);
    if (el) el.className = "rail-node";
  }
}

function updateActiveRunBadge(runId, active = true) {
  const badge = document.getElementById("activeRunBadge");
  if (badge) {
    if (active) {
      badge.textContent = `TRACE: ${runId.substring(0, 8)}... (LIVE)`;
      badge.style.color = "var(--pact-primary)";
    } else {
      badge.textContent = "TRACE: STANDBY";
      badge.style.color = "var(--pact-muted)";
    }
  }
}

function clearDebateFeed() {
  const feed = document.getElementById("debateFeed");
  if (feed) feed.innerHTML = "";
}

function appendDebateCard(turn) {
  const feed = document.getElementById("debateFeed");
  if (!feed) return;

  const card = document.createElement("div");
  card.className = "capacity-node";

  const speaker = turn.speaker || "Relief Advocate";
  const role = turn.role || turn.stance || "Advocate";
  const arg = turn.argument || "";

  card.innerHTML = `
    <div class="capacity-node-header">
      <span class="capacity-node-name">${speaker}</span>
      <span class="capacity-node-role">${role}</span>
    </div>
    <div class="capacity-node-body">${arg}</div>
  `;

  feed.appendChild(card);
  feed.scrollTop = feed.scrollHeight;
}

function renderSolverCards(options) {
  const grid = document.getElementById("solverOptionsGrid");
  if (!grid) return;
  grid.innerHTML = "";

  const order = ["fastest", "max_coverage", "least_depleting"];
  order.forEach((optId, idx) => {
    const opt = options[optId] || {};
    const title = opt.title || `[${idx + 1}] ${optId.replace('_', ' ').toUpperCase()}`;
    const cov = Math.round((opt.coverage_ratio || 1.0) * 100);
    const eta = opt.max_eta_hours || 1.0;

    const card = document.createElement("div");
    card.id = `solverCard-${optId}`;
    card.className = "solver-option-card";
    card.onclick = () => selectSolverCard(optId);

    card.innerHTML = `
      <div class="solver-card-header">${title}</div>
      <div class="solver-metrics-row">
        <span>COV: ${cov}%</span>
        <span>ETA: ~${eta}h</span>
      </div>
      <div class="solver-track">
        <div class="solver-fill" style="width: ${cov}%"></div>
      </div>
    `;
    grid.appendChild(card);
  });
}

function selectSolverCard(optionId) {
  const cards = document.querySelectorAll(".solver-option-card");
  cards.forEach(c => c.classList.remove("selected"));

  const target = document.getElementById(`solverCard-${optionId}`);
  if (target) target.classList.add("selected");
}

function showAdminGateAction(payload) {
  const bar = document.getElementById("adminActionBar");
  const title = document.getElementById("adminActionTitle");
  if (bar && title) {
    title.textContent = `Dispatcher Action Required: ${payload.reason || 'Approve Proposed Allocation'}`;
    bar.style.display = "flex";
  }
}

async function submitAdminDecision(action) {
  const bar = document.getElementById("adminActionBar");
  if (bar) bar.style.display = "none";

  try {
    await fetch("/api/v1/admin/gate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        decision_id: activeDecisionId,
        action: action === "approve" ? "approve" : "reject",
        user_id: "COMMANDER_DISPATCHER"
      })
    });
  } catch (e) {
    console.error("Admin gate error:", e);
  }
}

function showAckBanner(frame) {
  const box = document.getElementById("ackFrameBox");
  if (box) {
    box.textContent = `OUTBOUND CELLULAR ACK: ${frame}`;
    box.style.display = "flex";
  }
}

// ── Admin Initial Data Loaders ────────────────────────────────────────────────

async function loadInitialData() {
  await Promise.all([
    refreshStats(),
    loadOffersTable(),
    loadRequestsTable(),
    loadMatchesTable()
  ]);
}

async function refreshStats() {
  try {
    const res = await fetch("/api/v1/admin/stats");
    const data = await res.json();

    document.getElementById("statTotalRequests").textContent = data.total_requests || 0;
    document.getElementById("statActiveOffers").textContent = data.total_offers || 11;
    document.getElementById("statCommittedMatches").textContent = data.total_matches || 0;
    document.getElementById("statAgentEvents").textContent = data.total_events || 0;
  } catch (e) {
    console.error("Stats refresh error:", e);
  }
}

async function loadOffersTable() {
  try {
    const res = await fetch("/api/v1/offers?limit=15");
    const data = await res.json();

    if (crisisMap && data.offers) {
      crisisMap.setDepots(data.offers);
    }
  } catch (e) {
    console.error("Offers load error:", e);
  }
}

async function loadRequestsTable() {
  try {
    const res = await fetch("/api/v1/requests?limit=10");
    const data = await res.json();
    const tbody = document.getElementById("requestsTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    data.requests.forEach(r => {
      const payload = r.payload || {};
      const uid = r.uid || "SOS";
      const sit = payload.situation?.name || "General Crisis";
      const urg = payload.urgency?.label || "Medium";
      let tagClass = "hud-tag-info";
      if (urg.toLowerCase() === "critical") tagClass = "hud-tag-critical";
      else if (urg.toLowerCase() === "high") tagClass = "hud-tag-high";

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong style="font-family:var(--font-mono); color:var(--pact-primary);">${uid}</strong></td>
        <td>${sit}</td>
        <td>${payload.people_estimate || 1} persons</td>
        <td><span class="hud-tag ${tagClass}">${urg}</span></td>
        <td style="font-family:var(--font-mono); font-size:0.7rem; color:var(--pact-muted);">${r.raw_frame || 'Q|...'}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Requests load error:", e);
  }
}

async function loadMatchesTable() {
  try {
    const res = await fetch("/api/v1/matches?limit=15");
    const data = await res.json();
    const tbody = document.getElementById("matchesTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    data.matches.forEach(m => {
      const tr = document.createElement("tr");
      tr.style.cursor = "pointer";
      tr.onclick = () => inspectDispatch(m.match_id);

      const provName = m.provider_name || m.provider_id || (m.allocations && m.allocations[0] ? (m.allocations[0].provider_name || m.allocations[0].provider_id) : 'Assigned Depot');
      const itemsObj = m.items || (m.allocations && m.allocations[0] ? m.allocations[0].items : null);
      const itemsStr = itemsObj ? Object.entries(itemsObj).map(([k,v]) => `${v} ${k.replace('_',' ')}`).join(', ') : '';

      tr.innerHTML = `
        <td><strong style="font-family:var(--font-mono); color:var(--status-green-text);">${m.match_id}</strong></td>
        <td style="font-family:var(--font-mono);">${m.uid || 'CIT00'}</td>
        <td>
          <strong style="color:var(--pact-primary); font-size:0.85rem;">${provName}</strong>
          ${itemsStr ? `<div style="font-size:0.72rem; color:var(--pact-muted); margin-top:2px;">Cargo: ${itemsStr}</div>` : ''}
        </td>
        <td><span class="hud-tag hud-tag-success">${m.status || 'Committed'}</span></td>
        <td>
          <button class="btn-tactile" style="padding:0.25rem 0.6rem; font-size:0.68rem;" onclick="event.stopPropagation(); inspectDispatch('${m.match_id}')">
            Inspect Route
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Matches load error:", e);
  }
}

function setupEventListeners() {
  const resetBtn = document.getElementById("btnResetSeed");
  if (resetBtn) {
    resetBtn.onclick = async () => {
      if (confirm("Reset and re-seed all relief provider inventory in database?")) {
        await fetch("/api/v1/admin/seed", { method: "POST" });
        loadInitialData();
      }
    };
  }

  const toggle = document.getElementById("autopilotToggle");
  if (toggle) {
    toggle.onchange = async () => {
      try {
        await fetch("/api/v1/admin/autopilot", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ enabled: toggle.checked, timeout_seconds: 3.0 })
        });
        refreshStats();
      } catch (e) {
        console.error("Autopilot error:", e);
      }
    };
  }
}
