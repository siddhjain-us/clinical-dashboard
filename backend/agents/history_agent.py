import pickle

HIGH_RISK = ["ckd","chronic kidney disease","heart failure","chf","copd",
             "diabetes","cirrhosis","cancer","sepsis","hiv"]

def analyze_history(history, notes_text=""):
    model_data = None
    try:
        with open("backend/models/priority_model.pkl","rb") as f:
            model_data = pickle.load(f)
    except Exception: pass

    score, ml_category = 0, "UNKNOWN"

    if model_data and notes_text.strip():
        try:
            v = model_data["vectorizer"].transform([notes_text])
            ml_category = model_data["clf"].predict(v)[0]
            score += {"HIGH":40,"MEDIUM":20,"LOW":5}.get(ml_category,10)
        except Exception: pass

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
