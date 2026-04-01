from flask import Flask, render_template, request, Response, url_for
import joblib
import re
import pandas as pd
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)

OUTPUT_DIR = 'output'
DASHBOARD_FILE = os.path.join(OUTPUT_DIR, 'upload_predictions.csv')
SINGLE_PRED_FILE = os.path.join(OUTPUT_DIR, 'single_predictions.csv')

# Load trained model and vectorizer (with graceful error handling)
model = None
vectorizer = None
model_load_error = None
try:
    model = joblib.load("model/fake_review_model.pkl")
    vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
except Exception as e:
    model_load_error = str(e)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

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
    if model is None or vectorizer is None:
        return f"ERROR: model not loaded ({model_load_error})"

    cleaned = clean_text(review)
    vec = vectorizer.transform([cleaned])

    ml_prob = model.predict_proba(vec)[0][1]
    score = behavior_score(review)

    if ml_prob > 0.65 and score >= 1:
        return "FAKE REVIEW"
    else:
        return "GENUINE REVIEW"


def get_prediction_details(review):
    """Return (label, ml_prob) without changing global predict_review behavior."""
    if model is None or vectorizer is None:
        return (f"ERROR: model not loaded ({model_load_error})", 0.0)

    cleaned = clean_text(review)
    vec = vectorizer.transform([cleaned])
    ml_prob = float(model.predict_proba(vec)[0][1])
    score = behavior_score(review)
    label = "FAKE REVIEW" if (ml_prob > 0.65 and score >= 1) else "GENUINE REVIEW"
    return (label, ml_prob)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_route():
    review_text = request.form.get("review", "")
    prediction = ""
    prediction_class = ""

    if review_text:
        # use detailed prediction (label + prob)
        label, prob = get_prediction_details(review_text)
        prediction = label
        prediction_class = "fake" if "FAKE" in prediction.upper() else "genuine"

        # ensure output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        row = {
            'timestamp': datetime.utcnow().isoformat(),
            'review': review_text,
            'prediction': prediction,
            'prob': prob
        }

        # append to CSV
        try:
            import csv
            write_header = not os.path.exists(SINGLE_PRED_FILE)
            with open(SINGLE_PRED_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp','review','prediction','prob'])
                if write_header:
                    writer.writeheader()
                writer.writerow(row)
        except Exception:
            pass

    return render_template("index.html",
                           prediction=prediction,
                           review_text=review_text,
                           prediction_class=prediction_class)


@app.route("/upload", methods=["POST"])
def upload():
    # Accept CSV or Excel upload and run predictions on a column named 'review'
    file = request.files.get("file")
    table_html = ""

    if not file:
        return render_template("index.html", table="<p>No file uploaded</p>")

    filename = file.filename.lower()
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return render_template("index.html", table="<p>Unsupported file type</p>")
    except Exception as e:
        return render_template("index.html", table=f"<p>Failed to read file: {e}</p>")

    if 'review' not in df.columns:
        return render_template("index.html", table="<p>File must contain a 'review' column</p>")

    df = df.dropna(subset=['review']).copy()

    # compute predictions and probabilities
    preds = [get_prediction_details(r) for r in df['review']]
    df['prediction'] = [p[0] for p in preds]
    df['prob'] = [p[1] for p in preds]

    # save to dashboard CSV
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        # Keep a copy of the latest uploaded source file for traceability.
        uploads_dir = 'uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        latest_upload_file = os.path.join(uploads_dir, 'latest_uploaded.csv')
        df[['review']].to_csv(latest_upload_file, index=False, encoding='utf-8')

        df_to_save = df[['review','prediction','prob']].copy()
        df_to_save.insert(0, 'timestamp', datetime.utcnow().isoformat())
        # Overwrite on each upload so dashboard always shows latest uploaded file data.
        df_to_save.to_csv(DASHBOARD_FILE, index=False, encoding='utf-8')
    except Exception as e:
        return render_template("index.html", table=f"<p>Failed to save predictions: {e}</p>")

    table_html = df.to_html(classes='pred-table', index=False)

    return render_template("index.html", table=table_html)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not os.path.exists(DASHBOARD_FILE):
        return render_template('dashboard.html', summary=None, table=None, chart_data=None, page=1, total_pages=0)

    try:
        df = pd.read_csv(DASHBOARD_FILE)

        # query params
        q = request.args.get('q', '').strip()
        f = request.args.get('filter', 'all').lower()
        try:
            per_page = int(request.args.get('per_page', 20))
        except Exception:
            per_page = 20
        try:
            page = int(request.args.get('page', 1))
        except Exception:
            page = 1

        # filters
        if q:
            df = df[df['review'].str.contains(q, case=False, na=False)]
        if f == 'fake':
            df = df[df['prediction'].str.contains('FAKE', na=False)]
        elif f == 'genuine':
            df = df[df['prediction'].str.contains('GENUINE', na=False)]

        total = len(df)
        total_pages = max(1, (total + per_page - 1) // per_page) if total else 1
        page = max(1, min(page, total_pages))
        start = (page - 1) * per_page
        end = start + per_page

        page_df = df.sort_values(by='timestamp', ascending=False).iloc[start:end]
        table_html = page_df.to_html(classes='pred-table', index=False)

        # summary
        fake = df['prediction'].str.contains('FAKE', na=False).sum()
        genuine = total - fake
        fake_pct = round(100 * fake / total, 2) if total else 0.0
        genuine_pct = round(100 * genuine / total, 2) if total else 0.0
        summary = {
            'total': int(total),
            'fake': int(fake),
            'genuine': int(genuine),
            'fake_pct': fake_pct,
            'genuine_pct': genuine_pct
        }

        # chart data: counts per date
        df['date'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.date
        counts = df.groupby(['date', 'prediction']).size().unstack(fill_value=0)
        labels = [str(d) for d in counts.index]
        fake_counts = counts['FAKE REVIEW'].tolist() if 'FAKE REVIEW' in counts.columns else [0] * len(labels)
        genuine_counts = counts['GENUINE REVIEW'].tolist() if 'GENUINE REVIEW' in counts.columns else [0] * len(labels)
        chart_data = {'labels': labels, 'fake': fake_counts, 'genuine': genuine_counts}

        return render_template('dashboard.html', summary=summary, table=table_html, chart_data=chart_data,
                               page=page, per_page=per_page, total_pages=total_pages, q=q, f=f)
    except Exception:
        return render_template('dashboard.html', summary=None, table=None, chart_data=None, page=1, total_pages=0)


@app.route('/dashboard/export', methods=['GET'])
def dashboard_export():
    if not os.path.exists(DASHBOARD_FILE):
        return Response('No data', status=404)

    try:
        df = pd.read_csv(DASHBOARD_FILE)
        q = request.args.get('q', '').strip()
        f = request.args.get('filter', 'all').lower()
        if q:
            df = df[df['review'].str.contains(q, case=False, na=False)]
        if f == 'fake':
            df = df[df['prediction'].str.contains('FAKE', na=False)]
        elif f == 'genuine':
            df = df[df['prediction'].str.contains('GENUINE', na=False)]

        csv_bytes = df.to_csv(index=False).encode('utf-8')
        return Response(csv_bytes,
                        mimetype='text/csv',
                        headers={"Content-Disposition": "attachment;filename=predictions_export.csv"})
    except Exception as e:
        return Response(f'Error exporting: {e}', status=500)

if __name__ == "__main__":
    app.run(debug=True)
