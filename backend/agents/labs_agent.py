def analyze_labs(labs):
    RANGES = {
        "creatinine":(0.6,1.2),"potassium":(3.5,5.0),"sodium":(136,145),
        "wbc":(4.5,11.0),"hemoglobin":(12.0,17.0),"glucose":(70,100),"lactate":(0.5,2.0)
    }
    CRIT_HIGH = {"potassium":6.0,"lactate":4.0,"creatinine":4.0,"glucose":500}
    CRIT_LOW  = {"potassium":2.5,"sodium":120,"glucose":40}

    score, critical_flags, abnormal, trends = 0, [], {}, {}

    for key,(low,high) in RANGES.items():
        val = labs.get(key)
        if val is None: continue
        if val < low or val > high:
            abnormal[key] = val; score += 15
        if key in CRIT_HIGH and val > CRIT_HIGH[key]:
            critical_flags.append(f"{key}_critical_high"); score += 20
        if key in CRIT_LOW  and val < CRIT_LOW[key]:
            critical_flags.append(f"{key}_critical_low");  score += 20

    for key in ["creatinine","wbc","potassium"]:
        prev = labs.get(f"{key}_prev")
        curr = labs.get(key)
        if curr and prev:
            d = curr - prev
            trends[key] = "rising" if d>0.1 else "falling" if d<-0.1 else "stable"
            if key=="creatinine" and trends[key]=="rising": score += 10

    return {"labs_risk_score":min(100,score),"critical_flags":critical_flags,
            "trends":trends,"abnormal_results":abnormal}
