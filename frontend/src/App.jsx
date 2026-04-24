import { Routes, Route, NavLink, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import Dashboard from "./Dashboard.jsx";
import PatientDetail from "./PatientDetail.jsx";
import Analyze from "./Analyze.jsx";
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

const THEME_KEY = "clinical-theme";

function ThemeToggle() {
  const [dark, setDark] = useState(
    () => localStorage.getItem(THEME_KEY) === "dark"
  );
  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    localStorage.setItem(THEME_KEY, dark ? "dark" : "light");
  }, [dark]);
  return (
    <button
      type="button"
      className="btn theme-btn"
      onClick={() => setDark((d) => !d)}
      aria-pressed={dark}
      title="Toggle dark mode"
    >
      {dark ? "Light" : "Dark"} mode
    </button>
  );
}

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Clinical triage dashboard</h1>
        <div className="header-right">
          <ThemeToggle />
          <HealthPill />
        </div>
      </header>
      <nav className="main-nav" style={{ marginBottom: "0.75rem" }}>
        <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : undefined)}>
          List
        </NavLink>
        <NavLink
          to="/analyze"
          end
          className={({ isActive }) => (isActive ? "active" : undefined)}
        >
          Analyze
        </NavLink>
      </nav>
      <EmptyHint />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/patient/:id" element={<PatientDetail />} />
      </Routes>
      <footer className="limitations" role="note">
        <strong>Demo / hackathon</strong> — not for clinical diagnosis. Rule-based and ML scores
        support <em>triage awareness</em> only; use de-identified or synthetic data. Model trained on
        public-style text, not your institution.
      </footer>
    </div>
  );
}
