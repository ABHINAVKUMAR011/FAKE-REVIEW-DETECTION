import pandas as pd
import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ---------- CLEAN TEXT ----------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# ---------- LOAD DATA ----------
df = pd.read_csv("TestReviews.csv")

# IMPORTANT: correct column names
df = df[['review', 'class']]
df.dropna(inplace=True)

# Clean text
df['review'] = df['review'].apply(clean_text)

X = df['review']
y = df['class']   # 0 = genuine, 1 = fake

# ---------- TF-IDF ----------
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2),
    max_features=8000,
    min_df=5
)

X_vec = vectorizer.fit_transform(X)

# ---------- TRAIN TEST SPLIT ----------
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42, stratify=y
)

# ---------- MODEL ----------
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ---------- EVALUATION ----------
y_pred = model.predict(X_test)

print("Model Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ---------- SAVE ----------
joblib.dump(model, "model/fake_review_model.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully")
