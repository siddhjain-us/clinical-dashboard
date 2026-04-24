from flask import Flask, jsonify, request
from flask_cors import CORS
from orchestrator import run_orchestrator

app = Flask(__name__)
CORS(app)
patient_store = []

@app.route("/api/patient/add", methods=["POST"])
def add_patient():
    result = run_orchestrator(request.json)
    patient_store.append(result)
    patient_store.sort(key=lambda p: p.get("composite_score",0), reverse=True)
    return jsonify(result)

@app.route("/api/patient/analyze", methods=["POST"])
def analyze():
    return jsonify(run_orchestrator(request.json))

@app.route("/api/patients", methods=["GET"])
def get_patients():
    return jsonify(patient_store)

@app.route("/api/patient/<pid>", methods=["GET"])
def get_patient(pid):
    p = next((p for p in patient_store if p.get("patient_id")==pid), None)
    return jsonify(p) if p else (jsonify({"error":"not found"}), 404)

@app.route("/api/stats", methods=["GET"])
def stats():
    total = len(patient_store)
    return jsonify({
        "total":       total,
        "red_count":   sum(1 for p in patient_store if p.get("severity")=="RED"),
        "amber_count": sum(1 for p in patient_store if p.get("severity")=="AMBER"),
        "green_count": sum(1 for p in patient_store if p.get("severity")=="GREEN"),
        "avg_score":   round(sum(p.get("composite_score",0) for p in patient_store)/total,1) if total else 0,
    })

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
