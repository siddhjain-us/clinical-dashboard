import { useState } from "react";
import { postAnalyze } from "./api.js";
import { useToast } from "./ToastContext.jsx";

const SAMPLE = `{
  "patient_id": "DEMO-1",
  "name": "Preview patient",
  "age": 65,
  "sex": "F",
  "notes": "CHIEF COMPLAINT: Shortness of breath. HISTORY: On anticoagulation, recent fall.",
  "vitals": [{"hr": 110, "sbp": 90, "dbp": 60, "o2": 92, "temp": 37.8, "rr": 24, "timestamp": "2024-01-15T10:00:00Z"}],
  "labs": {"creatinine": 1.8, "lactate": 2.5, "wbc": 12},
  "medications": [{"name": "warfarin", "dose": "5mg", "time_administered": "2024-01-15T08:00:00Z", "status": "given"}],
  "history": {"diagnoses": ["Atrial fibrillation"], "admissions_last_12mo": 1, "allergies": []}
}`;

export default function Analyze() {
  const toast = useToast();
  const [text, setText] = useState(SAMPLE);
  const [out, setOut] = useState(null);
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  function run() {
    setErr(null);
    setOut(null);
    let body;
    try {
      body = JSON.parse(text);
    } catch (e) {
      const msg = "Invalid JSON: " + (e && e.message);
      setErr(msg);
      toast(msg, "err");
      return;
    }
    if (typeof body !== "object" || body === null) {
      setErr("Body must be a JSON object.");
      toast("Body must be a JSON object.", "err");
      return;
    }
    setBusy(true);
    postAnalyze(body)
      .then((d) => {
        setOut(d);
        setErr(null);
        toast("Analysis complete (not saved to board).", "ok");
      })
      .catch((e) => {
        const msg = e.message || "Request failed";
        setErr(msg);
        toast(msg, "err");
        setOut(null);
      })
      .finally(() => setBusy(false));
  }

  return (
    <div className="analyze-page">
      <p className="lede">
        <strong>Preview only</strong> — calls <code>POST /api/patient/analyze</code> and does{" "}
        <strong>not</strong> save to the board. Use <strong>List</strong> and <strong>Add</strong> in
        the API to persist.
      </p>
      <div className="table-toolbar" style={{ marginBottom: "0.75rem" }}>
        <button type="button" className="btn" onClick={() => setText(SAMPLE)} disabled={busy}>
          Load sample JSON
        </button>
        <button type="button" className="btn primary" onClick={run} disabled={busy}>
          {busy ? "Running…" : "Run analysis"}
        </button>
      </div>
      {err && <div className="banner-err">{err}</div>}
      <textarea
        className="json-editor"
        value={text}
        onChange={(e) => setText(e.target.value)}
        spellCheck={false}
        aria-label="Patient JSON for analyze"
      />
      {out && (
        <div className="card" style={{ marginTop: "1rem" }}>
          <h2 style={{ marginTop: 0, fontSize: "1rem" }}>Result (not persisted)</h2>
          <p>
            <span className={`badge badge-${out.severity || "AMBER"}`}>{out.severity}</span>{" "}
            composite <strong>{out.composite_score}</strong>
            {out.ml_note?.tier != null && (
              <>
                {" "}
                · ML tier <strong>{out.ml_note.tier}</strong>
              </>
            )}
          </p>
          <pre className="block">{JSON.stringify(out, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
