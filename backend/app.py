import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from models.note_priority import get_model, model_path
from orchestrator import run_orchestrator
from patient_store import PatientStore


def _api_error(message: str, code: int = 400, **extra: object):
    return jsonify({"error": message, **extra}), code


def _require_json_object() -> tuple[dict | None, tuple | None]:
    """Parse JSON object body. Empty body is treated as {}. Returns (data, error_response)."""
    if request.data and not request.is_json:
        return None, _api_error("Content-Type must be application/json", 415)
    body = request.get_data(as_text=True) or ""
    if not body.strip():
        return {}, None
    data = request.get_json(silent=True)
    if data is None:
        return None, _api_error("Invalid JSON body", 400)
    if not isinstance(data, dict):
        return None, _api_error("Request body must be a JSON object", 400)
    return data, None


def create_app(patient_file: Path | None = None) -> Flask:
    app = Flask(__name__)
    CORS(app)
    default_path = Path(__file__).resolve().parent / "data" / "patients.json"
    env_path = os.environ.get("PATIENT_DATA_FILE")
    path = patient_file or (Path(env_path) if env_path else default_path)
    store = PatientStore(path)
    app.config["PATIENT_STORE_PATH"] = str(path)

    @app.get("/")
    def root():
        return jsonify(
            {
                "service": "clinical-dashboard-api",
                "docs": "see README.md",
                "health": "/health",
            }
        )

    @app.get("/health")
    def health():
        p = model_path()
        m = get_model()
        return jsonify(
            {
                "status": "ok",
                "ml_model_path": str(p),
                "ml_model_exists": p.is_file(),
                "ml_model_loaded": m is not None,
            }
        )

    @app.post("/api/patient/add")
    def add_patient():
        data, e = _require_json_object()
        if e:
            return e
        assert data is not None
        if not (data.get("patient_id") or "").strip():
            return _api_error("patient_id is required", 400)
        result = run_orchestrator(data)
        store.append_sorted(result)
        return jsonify(result)

    @app.post("/api/patient/analyze")
    def analyze():
        data, e = _require_json_object()
        if e:
            return e
        assert data is not None
        return jsonify(run_orchestrator(data))

    @app.get("/api/patients")
    def get_patients():
        return jsonify(store.all())

    @app.get("/api/patient/<pid>")
    def get_patient(pid):
        p = store.get(pid)
        if not p:
            return _api_error("patient not found", 404, patient_id=pid)
        return jsonify(p)

    @app.get("/api/stats")
    def stats():
        rows = store.iter_for_stats()
        total = len(rows)
        return jsonify(
            {
                "total": total,
                "red_count": sum(1 for p in rows if p.get("severity") == "RED"),
                "amber_count": sum(1 for p in rows if p.get("severity") == "AMBER"),
                "green_count": sum(1 for p in rows if p.get("severity") == "GREEN"),
                "avg_score": round(
                    sum(p.get("composite_score", 0) for p in rows) / total, 1
                )
                if total
                else 0,
            }
        )

    @app.errorhandler(404)
    def not_found(e):  # noqa: ARG001
        if request.path.startswith("/api/"):
            return _api_error("not found", 404, path=request.path)
        return (jsonify({"error": "not found", "path": request.path}), 404)

    return app


app = create_app()

if __name__ == "__main__":
    # threaded=True: dev server can answer /api/stats while a slow orchestrator
    # POST is in progress (avoids "stuck" curl in another terminal)
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        threaded=True,
        use_reloader=False,
    )
