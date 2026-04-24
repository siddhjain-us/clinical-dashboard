import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle, os

df = pd.read_csv('backend/data/mtsamples.csv').dropna(subset=['transcription','medical_specialty'])

RISK_MAP = {
    'Emergency Room Reports':'HIGH','Cardiovascular / Pulmonary':'HIGH',
    'Neurosurgery':'HIGH','Hematology - Oncology':'HIGH','Nephrology':'HIGH',
    'General Medicine':'MEDIUM','Endocrinology':'MEDIUM','Gastroenterology':'MEDIUM',
    'Neurology':'MEDIUM','Orthopedic':'MEDIUM','Radiology':'MEDIUM',
    'Office Notes':'LOW','SOAP / Chart / Progress Notes':'LOW',
    'Dermatology':'LOW','Ophthalmology':'LOW','Pediatrics - Neonatal':'LOW',
}
df['risk_tier'] = df['medical_specialty'].map(RISK_MAP)
df = df.dropna(subset=['risk_tier'])

vec = TfidfVectorizer(max_features=500, stop_words='english')
X   = vec.fit_transform(df['transcription'])
X_tr, X_te, y_tr, y_te = train_test_split(X, df['risk_tier'], test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_tr, y_tr)

print("=== TRAINING COMPLETE ===")
print(classification_report(y_te, clf.predict(X_te)))

names = vec.get_feature_names_out()
top   = clf.feature_importances_.argsort()[-20:][::-1]
print("\nTop 20 words predicting high-risk notes:")
for i in top:
    print(f"  {names[i]}: {clf.feature_importances_[i]:.4f}")

os.makedirs('backend/models', exist_ok=True)
with open('backend/models/priority_model.pkl','wb') as f:
    pickle.dump({'clf':clf,'vectorizer':vec}, f)
print("\nSaved → backend/models/priority_model.pkl")
