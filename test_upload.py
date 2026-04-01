import pandas as pd
import joblib
import re

MODEL_PATH = 'model/fake_review_model.pkl'
VEC_PATH = 'model/tfidf_vectorizer.pkl'
CSV_PATH = 'TestReviews.csv'

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VEC_PATH)
except Exception as e:
    print('MODEL_LOAD_ERROR:', e)
    raise SystemExit(1)

print('Models loaded OK')

df = pd.read_csv(CSV_PATH)
if 'review' not in df.columns:
    print("CSV missing 'review' column")
    raise SystemExit(1)

sample = df['review'].dropna().head(5)
for i, r in enumerate(sample, 1):
    cleaned = clean_text(r)
    vec = vectorizer.transform([cleaned])
    try:
        prob = model.predict_proba(vec)[0][1]
    except Exception as e:
        print('PREDICT_ERROR:', e)
        continue
    print(f'#{i} prob={prob:.4f} ->', 'FAKE' if prob>0.65 else 'GENUINE')
