from datetime import datetime, timedelta

INTERACTIONS = [
    (["warfarin"],["aspirin","ibuprofen","naproxen"],"bleeding risk: warfarin + NSAID"),
    (["lisinopril","enalapril","ramipril"],["spironolactone","triamterene"],"hyperkalemia risk: ACE + K-sparing diuretic"),
    (["warfarin"],["apixaban","rivaroxaban","heparin"],"CRITICAL: dual anticoagulation"),
]
NSAIDS = ["ibuprofen","naproxen","diclofenac","indomethacin","celecoxib"]

def analyze_medications(medications, labs=None):
    score, interactions = 0, []
    names = [m["name"].lower() for m in medications]

    for ga, gb, msg in INTERACTIONS:
        if any(m in names for m in ga) and any(m in names for m in gb):
            interactions.append(msg)
            score += 25 if "CRITICAL" in msg else 15

    if labs and labs.get("creatinine",0) > 1.5 and any(n in names for n in NSAIDS):
        interactions.append("NSAIDs contraindicated — elevated creatinine")
        score += 25

    if len(medications) >= 8:
        interactions.append("polypharmacy risk (8+ medications)"); score += 10

    cutoff = datetime.utcnow() - timedelta(hours=24)
    administered, missed = [], []
    for m in medications:
        t = m.get("time_administered")
        if t:
            try:
                dt = datetime.fromisoformat(t.replace("Z","+00:00")).replace(tzinfo=None)
                if dt > cutoff:
                    administered.append(f"{m['name']} {m.get('dose','')} at {dt.strftime('%H:%M')}")
            except Exception: pass
        if m.get("status") == "missed":
            missed.append(f"{m['name']} {m.get('dose','')}")

    return {"medication_risk_score":min(100,score),"interactions":interactions,
            "polypharmacy_risk":len(medications)>=8,
            "administered_last_24h":administered,"missed_doses":missed}
