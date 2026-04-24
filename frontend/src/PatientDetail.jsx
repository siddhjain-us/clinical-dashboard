import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchPatient } from "./api.js";

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

export default function PatientDetail() {
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
      <Link className="back" to="/">
        ← Back to list
      </Link>

      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          {p.name} <span style={{ color: "#5c6b7a", fontWeight: 400 }}>({p.patient_id})</span>
        </h2>
        <p>
          <span className={`badge badge-${p.severity || "AMBER"}`}>{p.severity || "—"}</span>{" "}
          &nbsp; score <strong>{p.composite_score}</strong> · {p.age}y {p.sex} · {p.analyzed_at}
        </p>
        <p>
          <strong>Primary concern:</strong> {p.primary_concern}
        </p>
      </div>

      <Section title="AI note risk (ml_note)">
        {ml.model_available ? (
          <p>
            <strong>Tier:</strong> {ml.tier ?? "—"}{" "}
            {ml.proba && (
              <span style={{ color: "#5c6b7a", fontSize: "0.85rem" }}>
                (proba: {Object.entries(ml.proba)
                  .map(([k, v]) => `${k}: ${(v * 100).toFixed(0)}%`)
                  .join(", ")}
                )
              </span>
            )}
          </p>
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
