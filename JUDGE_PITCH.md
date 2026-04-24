# Pitch for judges (2–3 minutes)

## One-line elevator

We turn messy patient data and clinical notes into a **prioritized, explainable** triage view—**multi-signal** rules plus **NLP** on the note—so teams can see **who to see first** and **why**.

## Suggested flow

1. **Problem (15–20 s)**  
   Clinicians are flooded with data. **Triage support** (not diagnosis) means surfacing who needs attention first, from vitals, labs, meds, history, and the **clinical note**.

2. **What you built (30–40 s)**  
   A **Flask API** with **parallel agents** (vitals, labs, medications, history) and a **summary** with a **composite score** and **RED / AMBER / GREEN**. A **RandomForest + TF‑IDF** model on the **note** adds an **`ml_note` tier and probabilities** when the model file is present. A **React dashboard** lists patients, shows stats, and a **detail** view with **actions** and an **“Analyze”** page for **preview-only** runs (`POST /api/patient/analyze` does not persist).

3. **Why this architecture (20–30 s)**  
   **Modular agents** are easy to extend. **One orchestrator** run keeps behavior consistent. **API + separate UI** matches how a real system would integrate with an EHR or data layer later.

4. **Live demo (45–60 s)**  
   Start the **API (8000)** and **Vite (5173)**. Show **List** with **search / sort / filter**. Open a **RED** patient: **Signals at a glance**, **ml_note** bars, **brief actions**, optional **Download JSON**. Open **Analyze**, **Run analysis** on the sample (preview, not saved). Point to the **footer**: demo / not for diagnosis.

5. **Limitations (15–20 s)**  
   Demo and synthetic or de-identified data. **Not a medical device**; real use needs validation, governance, and integration. **Next** could be history in a DB, auth, or a specific unit workflow.

## Phrases to use

- “Surfaces risk and supports **triage**” / “**Human-in-the-loop** by design.”
- “**Actionable** summary: recommended next steps in the brief, not just a score.”

## Phrases to avoid

- “Our AI diagnoses…” → use “flags patterns / supports prioritization.”
- “100% accurate” → “complements clinician judgment; limitations apply.”

## Run order (demo)

1. `cd backend && source venv/bin/activate && python app.py`  
2. `cd frontend && npm install && npm run dev`  
3. If the list is empty: from `backend`, `python -c "from seed_patients import load; load()"` then refresh.
