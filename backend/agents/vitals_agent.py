def analyze_vitals(vitals_readings):
    if not vitals_readings:
        return {"vitals_risk_score":0,"flags":[],"trends":{},"sepsis_pattern":False}

    RANGES = {"hr":(60,100),"sbp":(90,140),"dbp":(60,90),
              "o2":(95,100),"temp":(36.1,37.5),"rr":(12,20)}
    FLAG_NAMES = {
        "hr":  ("bradycardia","tachycardia"),
        "sbp": ("hypotension","hypertension"),
        "o2":  ("hypoxia","hypoxia"),
        "temp":("hypothermia","fever"),
        "rr":  ("bradypnea","tachypnea"),
    }
    latest = vitals_readings[-1]
    flags, score = [], 0

    for key,(low,high) in RANGES.items():
        val = latest.get(key)
        if val is None: continue
        if val < low:
            flags.append(FLAG_NAMES[key][0]); score += 15
        elif val > high:
            flags.append(FLAG_NAMES[key][1]); score += 15

    trends = {}
    if len(vitals_readings) >= 2:
        prev = vitals_readings[-2]
        for key in ["hr","sbp","o2","temp"]:
            if key in latest and key in prev:
                d = latest[key] - prev[key]
                trends[key] = "rising" if d>2 else "falling" if d<-2 else "stable"

    fever = latest.get("temp",37) > 37.8
    tachy = latest.get("hr",80)   > 100
    hypo  = latest.get("sbp",120) < 100
    sepsis = fever and tachy and hypo
    if sepsis:
        score = min(100, score+30)
        flags.append("sepsis_pattern")

    return {"vitals_risk_score":min(100,score),
            "flags":list(set(flags)),"trends":trends,"sepsis_pattern":sepsis}
