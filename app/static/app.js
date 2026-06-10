const state = {
  containers: [],
  summary: null,
};

const elements = {
  sourceBadge: document.querySelector("#sourceBadge"),
  refreshButton: document.querySelector("#refreshButton"),
  riskFilter: document.querySelector("#riskFilter"),
  searchInput: document.querySelector("#searchInput"),
  rows: document.querySelector("#containerRows"),
  total: document.querySelector("#totalContainers"),
  running: document.querySelector("#runningContainers"),
  unhealthy: document.querySelector("#unhealthyContainers"),
  highRisk: document.querySelector("#highRiskContainers"),
};

async function load() {
  elements.refreshButton.disabled = true;
  try {
    const [summaryResponse, containersResponse] = await Promise.all([
      fetch("/api/summary"),
      fetch("/api/containers"),
    ]);
    state.summary = await summaryResponse.json();
    const containerPayload = await containersResponse.json();
    state.containers = containerPayload.containers;
    renderSummary();
    renderRows();
  } finally {
    elements.refreshButton.disabled = false;
  }
}

function renderSummary() {
  elements.sourceBadge.textContent = state.summary.source;
  elements.total.textContent = state.summary.total_containers;
  elements.running.textContent = state.summary.running;
  elements.unhealthy.textContent = state.summary.unhealthy;
  elements.highRisk.textContent = state.summary.high_risk;
}

function renderRows() {
  const risk = elements.riskFilter.value;
  const query = elements.searchInput.value.trim().toLowerCase();

  const rows = state.containers
    .filter((container) => risk === "all" || container.risk_level === risk)
    .filter((container) => {
      const haystack = [
        container.name,
        container.image,
        container.owner,
        container.service,
        container.compose_project,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return haystack.includes(query);
    })
    .sort((a, b) => b.risk_score - a.risk_score)
    .map(containerRow)
    .join("");

  elements.rows.innerHTML =
    rows || '<tr><td colspan="6">No containers match the current filters.</td></tr>';
}

function containerRow(container) {
  const reasons = container.risk_reasons.join("; ");
  const project = container.compose_project || "no compose project";
  const owner = container.owner || "unowned";
  return `
    <tr>
      <td>
        <span class="name">${escapeHtml(container.name)}</span>
        <span class="subtle">${escapeHtml(container.service || "unknown service")} · ${escapeHtml(project)}</span>
      </td>
      <td>
        ${escapeHtml(container.image)}
        <span class="subtle">${container.image_created_days_ago ?? "unknown"} days old</span>
      </td>
      <td>
        ${escapeHtml(container.status)}
        <span class="subtle">health: ${escapeHtml(container.health)} · restarts: ${container.restart_count}</span>
      </td>
      <td>${escapeHtml(owner)}</td>
      <td><span class="risk ${container.risk_level}">${container.risk_score}</span></td>
      <td>${escapeHtml(reasons)}</td>
    </tr>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

elements.refreshButton.addEventListener("click", load);
elements.riskFilter.addEventListener("change", renderRows);
elements.searchInput.addEventListener("input", renderRows);

load();
