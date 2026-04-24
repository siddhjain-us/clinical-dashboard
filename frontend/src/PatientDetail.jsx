import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchPatient } from "./api.js";
import { useToast } from "./ToastContext.jsx";

function Section({ title, children }) {
  return (
    <section>
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function JsonBlock({ data }) {
  if (data == null) return <p>—</p>;
  return <pre className="block">{JSON.stringify(data, null, 2)}</pre>;
}

function ListOrDash({ items }) {
  if (!Array.isArray(items) || !items.length) return <p>—</p>;
  return (
    <ul className="plain">
      {items.map((t, i) => (
        <li key={i}>{typeof t === "string" ? t : JSON.stringify(t)}</li>
      ))}
    </ul>
  );
}

function ProbaBars({ proba }) {
  if (!proba || typeof proba !== "object") return null;
  const entries = Object.entries(proba).sort((a, b) => b[1] - a[1]);
  return (
    <div className="proba-wrap" aria-label="Class probabilities">
      {entries.map(([k, v]) => (
        <div key={k} className="proba-row">
          <span className="proba-name">{k}</span>
          <div className="proba-bar-bg">
            <div className="proba-bar-fill" style={{ width: `${Math.min(100, v * 100)}%` }} />
          </div>
          <span className="proba-pct">{(v * 100).toFixed(0)}%</span>
        </div>
      ))}
    </div>
  );
}

function downloadJson(patient, onDone) {
  const name = (patient.patient_id || "patient") + "-export.json";
  const blob = new Blob([JSON.stringify(patient, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
  onDone?.();
}

export default function PatientDetail() {
  const toast = useToast();
  const { id } = useParams();
  const [p, setP] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    fetchPatient(id)
      .then(setP)
      .catch((e) => {
        setError(e.message);
        setP(null);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p className="loading">Loading patient…</p>;
  if (error) {
    return (
      <>
        <Link className="back" to="/">
          ← Back to list
        </Link>
        <div className="banner-err">{error}</div>
      </>
    );
  }
  if (!p) return null;

  const b = p.brief || {};
  const ml = p.ml_note || {};

  return (
    <div className="detail">
      <div className="detail-actions">
        <Link className="back" to="/">
          ← Back to list
        </Link>
        <button
          type="button"
          className="btn primary"
          onClick={() => downloadJson(p, () => toast("Downloaded JSON", "ok"))}
        >
          Download JSON
        </button>
      </div>

      <div className="card time-strip">
        <span className="time-label">Analyzed at</span>{" "}
        <time dateTime={p.analyzed_at}>{p.analyzed_at || "—"}</time>
      </div>

      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          {p.name} <span style={{ color: "#5c6b7a", fontWeight: 400 }}>({p.patient_id})</span>
        </h2>
        <p>
          <span className={`badge badge-${p.severity || "AMBER"}`}>{p.severity || "—"}</span>{" "}
          &nbsp; score <strong>{p.composite_score}</strong> · {p.age}y {p.sex}
        </p>
        <p>
          <strong>Primary concern:</strong> {p.primary_concern}
        </p>
      </div>

      <div className="card explainability">
        <h3>Signals at a glance</h3>
        <p>
          <strong>Rule-based composite (0–100):</strong> {p.composite_score} (drives {p.severity}{" "}
          band from vitals, labs, meds, history)
        </p>
        {ml.model_available && ml.tier != null && (
          <p>
            <strong>ML note risk tier:</strong> {ml.tier} (extra signal on clinical text, not
            a diagnosis)
          </p>
        )}
        {b.actions && b.actions[0] && (
          <p className="why-line">
            <strong>Why it matters (first action):</strong> {b.actions[0]}
          </p>
        )}
      </div>

      <Section title="AI note risk (ml_note)">
        {ml.model_available ? (
          <>
            <p>
              <strong>Tier:</strong> {ml.tier ?? "—"}
            </p>
            <ProbaBars proba={ml.proba} />
            <p className="muted small-print">
              Probabilities are from the trained classifier on the note; use with clinician
              review.
            </p>
          </>
        ) : (
          <p style={{ color: "#5c6b7a" }}>
            No model on server — place <code>priority_model.pkl</code> under <code>backend/models/</code>{" "}
            or run training. API still works with rule-based scores.
          </p>
        )}
      </Section>

      <Section title="Summary (brief)">
        <p>
          <strong>Concern / chronic</strong>
        </p>
        <p>{b.concern}</p>
        <p>
          <strong>Abnormalities</strong>
        </p>
        <p>{b.abnormalities}</p>
        <p>
          <strong>Medications</strong>
        </p>
        <p>{b.medications}</p>
        <p>
          <strong>Actions</strong>
        </p>
        <ListOrDash items={b.actions} />
      </Section>

      <Section title="Clinical note">
        <pre className="block">{p.notes || "—"}</pre>
      </Section>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
        <div className="card">
          <h3 style={{ fontSize: "0.85rem", margin: "0 0 0.5rem" }}>Vitals agent</h3>
          <JsonBlock data={p.vitals} />
        </div>
        <div className="card">
          <h3 style={{ fontSize: "0.85rem", margin: "0 0 0.5rem" }}>Labs agent</h3>
          <JsonBlock data={p.labs} />
        </div>
        <div className="card">
          <h3 style={{ fontSize: "0.85rem", margin: "0 0 0.5rem" }}>Medication agent</h3>
          <JsonBlock data={p.medications} />
        </div>
        <div className="card">
          <h3 style={{ fontSize: "0.85rem", margin: "0 0 0.5rem" }}>History agent</h3>
          <JsonBlock data={p.history} />
        </div>
      </div>
    </div>
  );
}
