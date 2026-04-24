# Clinical dashboard — backend

Flask API for multi-agent patient analysis (vitals, labs, medication, history, summary) with a trained **note** classifier (RandomForest + TF‑IDF on mtsamples-style data). One ML prediction per request is shared with history (risk score) and summary (transparent `ml_note` block).

**Repo (example):** [clinical-dashboard on GitHub](https://github.com/siddhjain-us/clinical-dashboard) — use your canonical remote if different.

## Use this folder in Cursor

1. **File → Open Folder…** (or **File → Add Folder to Workspace…**)
2. Choose: **`/Users/siddhjain/hackathon-project/backend`** (or the parent `hackathon-project` for a monorepo)

## Quick start (local)

```bash
cd /Users/siddhjain/hackathon-project/backend
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server listens on **http://127.0.0.1:8000** (port 8000 avoids common macOS Control Center conflicts on 5000).

**Another terminal** (server must be up first):

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/api/stats
```

Seed the three demo patients (HTTP `POST` to the running API):

```bash
cd /Users/siddhjain/hackathon-project/backend
source venv/bin/activate
python -c "from seed_patients import load; load()"
```

Patient list persistence: JSON at **`data/patients.json`** (created on first add). Override with env **`PATIENT_DATA_FILE=/path/to/file.json`**.

## Frontend dashboard (Vite + React)

The browser UI is in **[`../frontend/`](../frontend/)** — start the **API first**, then `cd ../frontend && npm install && npm run dev`. If the list is empty, run the **seed** command (above) and refresh. Full run order: [`../frontend/README.md`](../frontend/README.md). A **2–3 minute judge pitch** outline is in [`../JUDGE_PITCH.md`](../JUDGE_PITCH.md).

## Production-style server (optional)

From `backend/`:

```bash
gunicorn wsgi:app -b 127.0.0.1:8000 --threads 4
```

## API contract (OpenAPI)

A hand-maintained spec lives at [`docs/openapi.yaml`](docs/openapi.yaml) for the main GET/POST routes (use with Swagger UI or code generators as needed).

## API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Service name and pointers |
| GET | `/health` | Liveness + ML file path / loaded |
| POST | `/api/patient/add` | Run orchestrator; **requires** `patient_id`; persists to `data/patients.json` |
| POST | `/api/patient/analyze` | Run orchestrator only; does **not** persist |
| GET | `/api/patients` | List stored patients |
| GET | `/api/patient/<id>` | One patient; **404** JSON if missing |
| GET | `/api/stats` | Counts and averages over stored patients |

`POST` bodies must be **JSON objects** with `Content-Type: application/json`. Error shape: `{"error": "...", ...}` with **400** / **404** / **415** as appropriate.

Responses include a **`ml_note`** object: `model_available`, `tier` (e.g. HIGH / MEDIUM / LOW if trained labels match), `proba` (per-class probabilities when loaded).

CORS is enabled for frontend dev on another port.

## ML

- **Train** (once `data/mtsamples.csv` is present under `backend/data/`):

  ```bash
  cd /Users/siddhjain/hackathon-project/backend
  source venv/bin/activate
  python models/train_classifier.py
  ```

  Writes **`models/priority_model.pkl`** next to `note_priority.py`. Paths are independent of the shell working directory. If the file is missing, the API still runs; `ml_note.model_available` is false.

- **Runtime:** `models/note_priority.py` loads the pickle once; `orchestrator` runs `predict_note_tier` before the thread pool and passes the result to history + summary.

## Tests

```bash
cd /Users/siddhjain/hackathon-project/backend
source venv/bin/activate
pytest -q
```

## Project layout (high level)

- `app.py` — `create_app()` factory, `PatientStore` persistence, validation, `/health`, `/`
- `wsgi.py` — gunicorn entry
- `patient_store.py` — thread-safe list + JSON file
- `orchestrator.py` — parallel agents + one shared ML result per request
- `agents/` — domain logic
- `models/note_priority.py` — ML load + predict
- `models/train_classifier.py` — training script
- `seed_patients.py` — demo `POST` client; **requires API already listening**
- `data/` — training CSV (you supply), `patients.json` generated (gitignored)
- `tests/` — pytest + Flask test client
- `../frontend/` — Vite + React dashboard

## Troubleshooting

- **Seed fails / connection errors:** Start Flask *before* `seed_patients.load()`. Do not auto-seed in `app.py` at import time.
- **curl or stats “hangs” while another request runs:** Dev server uses `threaded=True` on `python app.py`. For heavy demos, use gunicorn (above).
- **Frontend can’t connect:** ensure `python app.py` is running on **8000** and `frontend/.env.development` has `VITE_API_BASE=http://127.0.0.1:8000`.
