import joblib
import re

# Load model
model = joblib.load("model/fake_review_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# Heuristic rules
def behavior_score(review):
    score = 0
    if len(review.split()) < 4:
        score += 1
    if review.count("!") > 2:
        score += 1
    if any(word in review.lower() for word in ["buy now", "guaranteed", "100%", "cheap"]):
        score += 1
    return score

def predict_review(review):
    cleaned = clean_text(review)
    vec = vectorizer.transform([cleaned])
    
    ml_pred = model.predict(vec)[0]
    ml_prob = model.predict_proba(vec)[0][1]

    score = behavior_score(review)

    # FINAL DECISION
    if ml_prob > 0.65 and score >= 1:
        return "FAKE REVIEW"
    else:
        return "GENUINE REVIEW"

# TEST
while True:
    review = input("Enter review (or exit): ")
    if review.lower() == "exit":
        break
    print(predict_review(review))
