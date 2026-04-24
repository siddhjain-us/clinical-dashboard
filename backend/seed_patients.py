import requests, time

PATIENTS = [
    {
        "patient_id":"P001","name":"James Okafor","age":71,"sex":"M",
        "notes":"CHIEF COMPLAINT: Fever and confusion onset 6 hours ago.\nHISTORY: Temperature 38.9C, HR 118, BP 88/55. CKD stage 3. On NSAIDs for arthritis. Appears acutely unwell.",
        "vitals":[
            {"timestamp":"2024-01-15T06:00:00Z","hr":78,"sbp":122,"dbp":78,"o2":98,"temp":37.1,"rr":14},
            {"timestamp":"2024-01-15T12:00:00Z","hr":95,"sbp":105,"dbp":65,"o2":96,"temp":38.2,"rr":18},
            {"timestamp":"2024-01-15T18:00:00Z","hr":118,"sbp":88,"dbp":55,"o2":94,"temp":38.9,"rr":22},
        ],
        "labs":{"creatinine":2.1,"creatinine_prev":1.4,"potassium":5.8,"sodium":138,
                "wbc":14.2,"hemoglobin":11.2,"glucose":210,"lactate":3.8},
        "medications":[
            {"name":"ibuprofen","dose":"400mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
            {"name":"lisinopril","dose":"10mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
            {"name":"aspirin","dose":"75mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
            {"name":"metformin","dose":"500mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
            {"name":"furosemide","dose":"40mg","time_administered":"2024-01-15T12:00:00Z","status":"missed"},
        ],
        "history":{"diagnoses":["CKD Stage 3","Type 2 Diabetes","Hypertension"],
                   "admissions_last_12mo":2,"allergies":["penicillin"]},
    },
    {
        "patient_id":"P002","name":"Sandra Mwangi","age":58,"sex":"F",
        "notes":"CHIEF COMPLAINT: Hypertension follow-up.\nHISTORY: Mild creatinine rise on last bloods. On ACE inhibitor and potassium-sparing diuretic.",
        "vitals":[
            {"timestamp":"2024-01-15T09:00:00Z","hr":82,"sbp":148,"dbp":92,"o2":97,"temp":37.2,"rr":16},
            {"timestamp":"2024-01-15T14:00:00Z","hr":88,"sbp":142,"dbp":88,"o2":97,"temp":37.3,"rr":16},
        ],
        "labs":{"creatinine":1.5,"creatinine_prev":1.2,"potassium":5.6,"sodium":141,
                "wbc":7.2,"hemoglobin":13.1,"glucose":105},
        "medications":[
            {"name":"lisinopril","dose":"10mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
            {"name":"spironolactone","dose":"25mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
            {"name":"amlodipine","dose":"5mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
        ],
        "history":{"diagnoses":["Hypertension","CKD Stage 2","Hypercholesterolaemia"],
                   "admissions_last_12mo":0,"allergies":[]},
    },
    {
        "patient_id":"P003","name":"Thomas Adeyemi","age":34,"sex":"M",
        "notes":"CHIEF COMPLAINT: Post-operative day 2, appendectomy.\nHISTORY: Uncomplicated laparoscopic appendectomy. Recovering well. Tolerating oral fluids.",
        "vitals":[
            {"timestamp":"2024-01-15T07:00:00Z","hr":74,"sbp":122,"dbp":76,"o2":99,"temp":37.0,"rr":14},
            {"timestamp":"2024-01-15T13:00:00Z","hr":76,"sbp":118,"dbp":74,"o2":99,"temp":36.9,"rr":14},
        ],
        "labs":{"creatinine":0.9,"potassium":4.1,"sodium":140,"wbc":9.8,"hemoglobin":14.2,"glucose":88},
        "medications":[
            {"name":"paracetamol","dose":"1g","time_administered":"2024-01-15T06:00:00Z","status":"given"},
            {"name":"paracetamol","dose":"1g","time_administered":"2024-01-15T12:00:00Z","status":"given"},
            {"name":"amoxicillin","dose":"500mg","time_administered":"2024-01-15T08:00:00Z","status":"given"},
        ],
        "history":{"diagnoses":["Acute Appendicitis (resolved)"],"admissions_last_12mo":1,"allergies":[]},
    },
]

def load():
    time.sleep(1)
    for p in PATIENTS:
        try:
            r = requests.post("http://localhost:8000/api/patient/add", json=p)
            d = r.json()
            print(f"Seeded {p['name']}: {d.get('severity')} score={d.get('composite_score')}")
        except Exception as e:
            print(f"Seed failed {p['name']}: {e}")
