
# AI-Based Fake Review Detection System

![Project Banner](https://img.shields.io/badge/Status-Development-yellow) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Framework-Flask-green)
------------------------------------------------------------------------------------------------------------------------------------------------

## 🚀 Project Overview

The **AI-Based Fake Review Detection System** is designed to help businesses and users identify fake reviews on e-commerce platforms, restaurants, or products. This project combines **Machine Learning** with a **web application interface**, providing both users and administrators a seamless way to detect and monitor fraudulent reviews.

**Why this project?**
- Fake reviews affect buying decisions and brand credibility.
- Industry-relevant problem aligned with data analytics, ML, and full-stack development.
- Showcases end-to-end project skills.


------------------------------------------------------------------------------------------------------------------------------------------------

## 📌 Features

### User Module:
- Input reviews to check authenticity.
- Receive a **prediction** (Real or Fake) instantly.
- View statistics on detected fake reviews.

### Admin Module:
- Monitor all user queries.
- Analyze **fake vs real review trends**.
- Generate visual reports and model evaluation stats.

------------------------------------------------------------------------------------------------------------------------------------------------

## 🏗️ Architecture
<img width="1331" height="1600" alt="systemarch" src="https://github.com/user-attachments/assets/845275cb-2588-4471-a019-c11349007e13" />




**Key Modules:**

Frontend – Simple and professional UI for users and admin dashboard.

Backend – Flask application handling API calls and ML integration.

ML Model – TF-IDF + Logistic Regression (with optional BERT mention for advanced scaling).

Database – Stores user queries and admin reports.

------------------------------------------------------------------------------------------------------------------------------------------------

**🛠️ Tech Stack**


Programming Language: Python 3.10

Web Framework: Flask

ML Libraries: scikit-learn, pandas, numpy

Frontend: HTML, CSS, JavaScript

Deployment: Render /github

------------------------------------------------------------------------------------------------------------------------------------------------
**ML Pipeline**

Dataset Selection: Amazon & Yelp reviews.

Data Preprocessing:

Cleaning text (removing punctuation, stopwords)

Tokenization

TF-IDF Vectorization

Model Choice: Logistic Regression (beginner-friendly & effective)

Evaluation Metrics: Accuracy, Precision, Recall, F1-Score

------------------------------------------------------------------------------------------------------------------------------------------------

**⚡ How to Run Locally**

# Clone the repository
git clone https://github.com/ABHINAVKUMAR011/FAKE-REVIEW-DETECTION.git

# Navigate to project folder
cd AI-FAKE-REVIEW-DETECTION

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app/app.py

# Open your browser at
http://127.0.0.1:5000

------------------------------------------------------------------------------------------------------------------------------------------------
**📄 Future Improvements**


Integrate BERT or Transformer-based models for higher accuracy.

Add real-time review monitoring from e-commerce platforms.

Deploy on cloud with Docker + Render/Heroku.

Enhanced admin dashboard with charts & analytics.

------------------------------------------------------------------------------------------------------------------------------------------------

**🤝 Contributing**


Fork the repository

Create a new branch (git checkout -b feature-name)

Make your changes and commit (git commit -m "Add feature")

Push to the branch (git push origin feature-name)

Open a Pull Request

**WEB INTERFACE**
<img width="942" height="476" alt="image" src="https://github.com/user-attachments/assets/1276e5db-d293-4dee-a81b-a11b116e42a0" />

<img width="923" height="460" alt="image" src="https://github.com/user-attachments/assets/26657dae-33de-4586-96cb-4d16218f9377" />
<img width="938" height="469" alt="image" src="https://github.com/user-attachments/assets/6058465d-5431-474a-b811-bac1ddfaad0c" />
<img width="935" height="455" alt="image" src="https://github.com/user-attachments/assets/7e47092a-ffae-4268-8722-ebe0c412735f" />


