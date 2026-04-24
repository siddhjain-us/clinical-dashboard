import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# Resolves from this file: backend/models/train_classifier.py -> backend/
BACKEND_ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = BACKEND_ROOT / "data" / "mtsamples.csv"
OUT_MODEL = Path(__file__).resolve().parent / "priority_model.pkl"


def main() -> None:
    if not DATA_CSV.is_file():
        raise SystemExit(
            f"Missing training data: {DATA_CSV}\n"
            "Download mtsamples (e.g. Kaggle) into backend/data/mtsamples.csv and retry."
        )

    df = pd.read_csv(DATA_CSV).dropna(subset=["transcription", "medical_specialty"])
    df["medical_specialty"] = df["medical_specialty"].str.strip()

    risk_map = {
        "Emergency Room Reports": "HIGH",
        "Cardiovascular / Pulmonary": "HIGH",
        "Neurosurgery": "HIGH",
        "Hematology - Oncology": "HIGH",
        "Nephrology": "HIGH",
        "General Medicine": "MEDIUM",
        "Endocrinology": "MEDIUM",
        "Gastroenterology": "MEDIUM",
        "Neurology": "MEDIUM",
        "Orthopedic": "MEDIUM",
        "Radiology": "MEDIUM",
        "Office Notes": "LOW",
        "SOAP / Chart / Progress Notes": "LOW",
        "Dermatology": "LOW",
        "Ophthalmology": "LOW",
        "Pediatrics - Neonatal": "LOW",
    }
    df["risk_tier"] = df["medical_specialty"].map(risk_map)
    df = df.dropna(subset=["risk_tier"])

    vec = TfidfVectorizer(max_features=500, stop_words="english")
    x = vec.fit_transform(df["transcription"])
    x_tr, x_te, y_tr, y_te = train_test_split(
        x, df["risk_tier"], test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(x_tr, y_tr)

    print("=== TRAINING COMPLETE ===")
    print(classification_report(y_te, clf.predict(x_te)))

    names = vec.get_feature_names_out()
    top = clf.feature_importances_.argsort()[-20:][::-1]
    print("\nTop 20 words predicting high-risk notes:")
    for i in top:
        print(f"  {names[i]}: {clf.feature_importances_[i]:.4f}")

    out_dir = OUT_MODEL.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(OUT_MODEL, "wb") as f:
        pickle.dump({"clf": clf, "vectorizer": vec}, f)
    print(f"\nSaved → {OUT_MODEL}")


if __name__ == "__main__":
    main()
