import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchStats, fetchPatients } from "./api.js";

function SeverityBadge({ sev }) {
  const c = sev || "AMBER";
  return <span className={`badge badge-${c}`}>{c}</span>;
}

const SORTS = [
  { id: "score_desc", label: "Score (high first)" },
  { id: "score_asc", label: "Score (low first)" },
  { id: "name", label: "Name (A–Z)" },
  { id: "id", label: "Patient ID" },
];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [patients, setPatients] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filterSev, setFilterSev] = useState("all");
  const [search, setQ] = useState("");
  const [sort, setSort] = useState("score_desc");
  const [, setSearch] = useSearchParams();

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([fetchStats(), fetchPatients()])
      .then(([s, p]) => {
        setStats(s);
        setPatients(p);
        if (!p.length) setSearch({ empty: "1" });
        else setSearch({}, { replace: true });
      })
      .catch((e) => {
        setError(
          e.message || "Is the API running? Start: cd backend && source venv/bin/activate && python app.py (port 8000)"
        );
        setStats(null);
        setPatients(null);
      })
      .finally(() => setLoading(false));
  }, [setSearch]);

  const raw = patients || [];
  const q = search.trim().toLowerCase();
  const filtered = useMemo(() => {
    const list = raw.filter((p) => {
      if (filterSev !== "all" && p.severity !== filterSev) return false;
      if (!q) return true;
      return (
        String(p.patient_id || "")
          .toLowerCase()
          .includes(q) || String(p.name || "")
          .toLowerCase()
          .includes(q)
      );
    });
    const copy = [...list];
    copy.sort((a, b) => {
      if (sort === "score_desc")
        return (b.composite_score || 0) - (a.composite_score || 0);
      if (sort === "score_asc")
        return (a.composite_score || 0) - (b.composite_score || 0);
      if (sort === "name")
        return String(a.name || "").localeCompare(String(b.name || ""), undefined, {
          sensitivity: "base",
        });
      return String(a.patient_id || "").localeCompare(String(b.patient_id || ""));
    });
    return copy;
  }, [raw, filterSev, q, sort]);

  if (loading && !error) {
    return <p className="loading skeleton-pulse">Loading dashboard…</p>;
  }
  if (error) {
    return <div className="banner-err">{error}</div>;
  }

  return (
    <>
      {stats && (
        <div className="grid-stats">
          <div className="card">
            <h3>Total patients</h3>
            <div className="val">{stats.total}</div>
          </div>
          <div className="card">
            <h3>Red</h3>
            <div className="val">{stats.red_count}</div>
          </div>
          <div className="card">
            <h3>Amber</h3>
            <div className="val">{stats.amber_count}</div>
          </div>
          <div className="card">
            <h3>Green</h3>
            <div className="val">{stats.green_count}</div>
          </div>
          <div className="card">
            <h3>Avg score</h3>
            <div className="val">{stats.avg_score}</div>
          </div>
        </div>
      )}

      {raw.length > 0 && (
        <div className="table-toolbar">
          <label>
            <span className="toolbar-label">Search</span>
            <input
              type="search"
              className="input"
              placeholder="Name or patient ID"
              value={search}
              onChange={(e) => setQ(e.target.value)}
              aria-label="Filter by name or ID"
            />
          </label>
          <label>
            <span className="toolbar-label">Severity</span>
            <select
              className="input"
              value={filterSev}
              onChange={(e) => setFilterSev(e.target.value)}
            >
              <option value="all">All</option>
              <option value="RED">RED</option>
              <option value="AMBER">AMBER</option>
              <option value="GREEN">GREEN</option>
            </select>
          </label>
          <label>
            <span className="toolbar-label">Sort</span>
            <select className="input" value={sort} onChange={(e) => setSort(e.target.value)}>
              {SORTS.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.label}
                </option>
              ))}
            </select>
          </label>
        </div>
      )}

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Severity</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((p) => (
              <tr key={p.patient_id}>
                <td>
                  <Link to={`/patient/${encodeURIComponent(p.patient_id)}`}>
                    {p.patient_id}
                  </Link>
                </td>
                <td>{p.name || "—"}</td>
                <td>
                  <SeverityBadge sev={p.severity} />
                </td>
                <td>{p.composite_score ?? "—"}</td>
              </tr>
            ))}
            {raw.length === 0 ? (
              <tr>
                <td colSpan={4}>
                  <div className="empty-state">
                    <p className="empty-title">No patients in the board yet</p>
                    <p className="empty-body">
                      With the API on port 8000, from <code>backend</code> run:{" "}
                      <code>python -c &quot;from seed_patients import load; load()&quot;</code>
                    </p>
                  </div>
                </td>
              </tr>
            ) : filtered.length === 0 ? (
              <tr>
                <td colSpan={4} className="muted-cell">
                  No patients match the current search or filter. Clear filters to see all{" "}
                  {raw.length} row(s).
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </>
  );
}
