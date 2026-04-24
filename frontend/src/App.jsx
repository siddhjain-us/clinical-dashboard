import { Routes, Route, NavLink, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import Dashboard from "./Dashboard.jsx";
import PatientDetail from "./PatientDetail.jsx";
import { fetchHealth } from "./api.js";

function HealthPill() {
  const [h, setH] = useState(null);
  const [err, setErr] = useState(false);
  useEffect(() => {
    fetchHealth()
      .then((d) => setH(d))
      .catch(() => {
        setErr(true);
        setH(null);
      });
  }, []);
  if (err) return <span className="health muted">API offline</span>;
  if (!h) return <span className="health muted">Checking API…</span>;
  return (
    <span className={h.ml_model_loaded ? "health" : "health muted"}>
      API ok
      {h.ml_model_loaded ? " · ML loaded" : " · no ML file"}
    </span>
  );
}

function EmptyHint() {
  const [q] = useSearchParams();
  if (q.get("empty") !== "1") return null;
  return (
    <p className="card" style={{ color: "#5c6b7a" }}>
      No patients yet. From the <code>backend</code> folder:{" "}
      <code>python -c &quot;from seed_patients import load; load()&quot;</code> (with the API
      running).
    </p>
  );
}

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Clinical triage dashboard</h1>
        <HealthPill />
      </header>
      <nav style={{ marginBottom: "0.75rem" }}>
        <NavLink to="/" end>
          List
        </NavLink>
      </nav>
      <EmptyHint />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/patient/:id" element={<PatientDetail />} />
      </Routes>
    </div>
  );
}
