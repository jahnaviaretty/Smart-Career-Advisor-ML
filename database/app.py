
from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
MODEL_PATH = BASE_DIR / "models" / "career_model.joblib"
CHART_DIR = BASE_DIR / "static"
DB_PATH = BASE_DIR / "database" / "career_advisor.db"

CHART_DIR.mkdir(exist_ok=True)

# Flask application
app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(CHART_DIR)
)

app.secret_key = "change-this-to-a-random-secret-key"

# Load ML model
model = joblib.load(MODEL_PATH)


# Database connection
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not name or not email or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        try:
            connection.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            connection.commit()

            flash("Registration successful! Please login.")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Email already registered.")

        finally:
            connection.close()

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            flash("Login successful!")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")

    return redirect(url_for("login"))


# Homepage
@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    history = connection.execute(
        """
        SELECT career, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    total_predictions = len(history)

    return render_template(
        "dashboard.html",
        history=history,
        total_predictions=total_predictions
    )


# Career prediction
@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect(url_for("login"))

    features = {
        "GPA": float(request.form["GPA"]),
        "Python": int(request.form["Python"]),
        "SQL": int(request.form["SQL"]),
        "Communication": int(request.form["Communication"]),
        "Problem_Solving": int(request.form["Problem_Solving"]),
        "Projects": int(request.form["Projects"]),
        "Certifications": int(request.form["Certifications"])
    }

    input_data = pd.DataFrame([features])

    probabilities = model.predict_proba(input_data)[0]
    career_names = model.classes_

    top_indices = probabilities.argsort()[::-1][:3]

    top_careers = []

    for index in top_indices:

        top_careers.append({
            "name": career_names[index],
            "percentage": round(
                float(probabilities[index]) * 100, 2
            )
        })

    # Save top career recommendation
    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO predictions (user_id, career)
        VALUES (?, ?)
        """,
        (session["user_id"], top_careers[0]["name"])
    )

    connection.commit()
    connection.close()

    # Generate chart
    chart_path = CHART_DIR / "career_chart.png"

    names = [career["name"] for career in top_careers]
    scores = [career["percentage"] for career in top_careers]

    plt.figure(figsize=(9, 5))

    bars = plt.bar(names, scores)

    plt.title("Top 3 Career Recommendations")
    plt.xlabel("Career Options")
    plt.ylabel("Model Score (%)")
    plt.ylim(0, 100)

    for bar, score in zip(bars, scores):

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{score:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return render_template(
        "result.html",
        top_careers=top_careers,
        chart_url="/static/career_chart.png"
    )


# Run application
if __name__ == "__main__":
    app.run(debug=True)






