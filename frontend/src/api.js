const base = () => import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function getJson(path) {
  const r = await fetch(`${base()}${path}`, { headers: { Accept: "application/json" } });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    const msg = data.error || r.statusText || "Request failed";
    throw new Error(msg);
  }
  return data;
}

export function fetchStats() {
  return getJson("/api/stats");
}

export function fetchPatients() {
  return getJson("/api/patients");
}

export function fetchPatient(id) {
  return getJson(`/api/patient/${encodeURIComponent(id)}`);
}

export function fetchHealth() {
  return getJson("/health");
}

export async function postAnalyze(body) {
  const r = await fetch(`${base()}/api/patient/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    const msg = data.error || r.statusText || "Request failed";
    throw new Error(msg);
  }
  return data;
}
