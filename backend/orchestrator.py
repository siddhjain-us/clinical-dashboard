from concurrent.futures import ThreadPoolExecutor, as_completed
from models.note_priority import predict_note_tier
from agents.vitals_agent     import analyze_vitals
from agents.labs_agent       import analyze_labs
from agents.medication_agent import analyze_medications
from agents.history_agent    import analyze_history
from agents.summary_agent    import compose_summary


def run_orchestrator(patient):
    notes = patient.get("notes") or ""
    ml = predict_note_tier(notes)
    results = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {
            ex.submit(analyze_vitals,    patient.get("vitals",[])):                           "vitals",
            ex.submit(analyze_labs,      patient.get("labs",{})):                             "labs",
            ex.submit(analyze_medications, patient.get("medications",[]), patient.get("labs",{})): "medications",
            ex.submit(analyze_history,   patient.get("history",{}), notes, ml): "history",
        }
        for f in as_completed(futures):
            key = futures[f]
            try:    results[key] = f.result()
            except Exception as e: results[key] = {"error":str(e)}

    summary = compose_summary(results, patient, ml)
    return {**patient, **results, **summary}
