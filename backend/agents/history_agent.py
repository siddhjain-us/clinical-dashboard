from models.note_priority import predict_note_tier

HIGH_RISK = ["ckd","chronic kidney disease","heart failure","chf","copd",
             "diabetes","cirrhosis","cancer","sepsis","hiv"]


def analyze_history(history, notes_text="", ml_result=None):
    if ml_result is None:
        ml_result = predict_note_tier(notes_text or "")

    score = 0
    ml_category = (ml_result.get("tier") or "UNKNOWN") if ml_result.get("model_available") else "UNKNOWN"
    if ml_result.get("model_available") and ml_result.get("tier"):
        score += int(ml_result.get("history_ml_bonus", 0))

    diagnoses = [d.lower() for d in history.get("diagnoses",[])]
    chronic   = [d for d in diagnoses if any(h in d for h in HIGH_RISK)]
    score += min(30, len(chronic)*10)
    score += min(20, history.get("admissions_last_12mo",0)*7)

    chief = ""
    if notes_text:
        for line in notes_text.strip().split("\n")[:5]:
            if any(kw in line.lower() for kw in ["chief complaint","reason for visit","presenting"]):
                chief = line.split(":",1)[-1].strip(); break
        if not chief and notes_text.strip():
            chief = notes_text.strip().split("\n")[0][:80]

    return {"history_risk_score":min(100,score),"ml_risk_category":ml_category,
            "chronic_conditions":[d.title() for d in chronic],
            "recent_admissions":history.get("admissions_last_12mo",0),
            "chief_complaint":chief}
