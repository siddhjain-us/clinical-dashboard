import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchStats, fetchPatients } from "./api.js";

function SeverityBadge({ sev }) {
  const c = sev || "AMBER";
  return <span className={`badge badge-${c}`}>{c}</span>;
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [patients, setPatients] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
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

  if (loading && !error) {
    return <p className="loading">Loading dashboard…</p>;
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
            {(patients || []).map((p) => (
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
            {!patients || patients.length === 0 ? (
              <tr>
                <td colSpan={4} style={{ color: "#5c6b7a" }}>
                  No patients in store. Run the seed script (see message above) while the API is
                  up.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </>
  );
}
