import json

MINIMAL_PATIENT = {
    "patient_id": "T001",
    "name": "Test",
    "age": 40,
    "sex": "F",
    "notes": "Routine follow-up.",
    "vitals": [],
    "labs": {},
    "medications": [],
    "history": {"diagnoses": [], "admissions_last_12mo": 0, "allergies": []},
}


def test_root_and_health(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "clinical-dashboard-api" in r.get_json().get("service", "")

    h = client.get("/health")
    assert h.status_code == 200
    data = h.get_json()
    assert data["status"] == "ok"
    assert "ml_model_loaded" in data


def test_stats_empty(client):
    r = client.get("/api/stats")
    assert r.status_code == 200
    j = r.get_json()
    assert j["total"] == 0
    assert j["avg_score"] == 0


def test_add_requires_patient_id(client):
    r = client.post(
        "/api/patient/add",
        data=json.dumps({"name": "x"}),
        content_type="application/json",
    )
    assert r.status_code == 400
    assert "patient_id" in r.get_json().get("error", "").lower()


def test_add_and_get(client):
    r = client.post("/api/patient/add", json=MINIMAL_PATIENT)
    assert r.status_code == 200
    body = r.get_json()
    assert body.get("patient_id") == "T001"
    assert "composite_score" in body
    assert "ml_note" in body

    r2 = client.get("/api/patients")
    assert r2.status_code == 200
    assert len(r2.get_json()) == 1

    r3 = client.get("/api/patient/T001")
    assert r3.status_code == 200

    r4 = client.get("/api/patient/missing")
    assert r4.status_code == 404
    err = r4.get_json()
    assert err.get("error")


def test_analyze_no_persist(client):
    r = client.post("/api/patient/analyze", json=MINIMAL_PATIENT)
    assert r.status_code == 200
    assert r.get_json().get("patient_id") == "T001"
    s = client.get("/api/stats")
    # analyze does not append to store; only /add does
    assert s.get_json()["total"] == 0


def test_analyze_empty_json_object(client):
    r = client.post("/api/patient/analyze", json={})
    assert r.status_code == 200
    j = r.get_json()
    assert "ml_note" in j


def test_404_api(client):
    r = client.get("/api/missing")
    assert r.status_code == 404
    assert r.get_json().get("error")
