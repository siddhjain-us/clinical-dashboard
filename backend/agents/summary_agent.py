from datetime import datetime

WEIGHTS = {"vitals":0.35,"labs":0.25,"medications":0.20,"history":0.20}

def compose_summary(results, patient):
    scores = {k: results.get(k,{}).get(f"{k}_risk_score",0) for k in WEIGHTS}
    # summary_agent uses medication_risk_score key
    scores["medications"] = results.get("medications",{}).get("medication_risk_score",0)

    composite = round(sum(scores[k]*WEIGHTS[k] for k in WEIGHTS))
    severity  = "GREEN" if composite<40 else "AMBER" if composite<70 else "RED"

    v = results.get("vitals",{})
    l = results.get("labs",{})
    m = results.get("medications",{})
    h = results.get("history",{})

    abn     = l.get("abnormal_results",{})
    abn_str = ", ".join(f"{k} {val}" for k,val in abn.items()) or "none detected"
    vit_str = ", ".join(v.get("flags",[])) or "within normal range"
    med_str = "; ".join(m.get("interactions",[])) or "no interactions flagged"

    actions = []
    if v.get("sepsis_pattern"):
        actions.append("URGENT: sepsis protocol — blood cultures, IV antibiotics, IV fluids")
    if "creatinine_critical_high" in l.get("critical_flags",[]):
        actions.append("Nephrology consult — creatinine critical")
    if any("NSAIDs" in i for i in m.get("interactions",[])):
        actions.append("Hold NSAIDs immediately")
    if "potassium_critical_high" in l.get("critical_flags",[]):
        actions.append("Cardiac monitoring — hyperkalemia")
    for d in m.get("missed_doses",[]):
        actions.append(f"Administer missed dose: {d}")
    if not actions:
        actions = ["Continue monitoring","Reassess in 4 hours"]

    primary = h.get("chief_complaint") or "Review required"
    if v.get("sepsis_pattern"):
        primary = "Possible sepsis — immediate review required"
    elif abn:
        k = list(abn.keys())[0]
        primary = f"Abnormal {k} ({abn[k]}) — {l.get('trends',{}).get(k,'check trend')}"

    return {
        "composite_score": composite,
        "severity":        severity,
        "primary_concern": primary,
        "brief": {
            "concern":       f"{h.get('chief_complaint','See notes')}. Chronic: {', '.join(h.get('chronic_conditions',[])) or 'none'}.",
            "abnormalities": f"Labs: {abn_str}. Vitals: {vit_str}.",
            "medications":   med_str,
            "actions":       actions,
        },
        "analyzed_at": datetime.utcnow().isoformat()+"Z",
    }
