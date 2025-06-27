# --- Cleaned Up & Fixed CTI Dashboard Flask App ---

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import os
import io
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# --- Custom Modules ---
from utils.vt_lookup import lookup_ioc, lookup_ioc_data, generate_threat_trend_chart

# --- App & DB Setup ---
app = Flask(__name__)
app.secret_key = 'super-secret-key'

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["cti_dashboard"]

# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html", current_year=datetime.now().year)


@app.route("/check", methods=["POST"])
def check():
    ioc = request.form.get('ioc')
    if not ioc:
        flash("IOC cannot be empty", "danger")
        return redirect(url_for('dashboard'))

    try:
        result = lookup_ioc(ioc)
        result['timestamp'] = datetime.utcnow()
        db.threats.insert_one(result)
        flash("IOC lookup successful", "success")
    except Exception as e:
        flash(f"Lookup failed: {e}", "danger")

    return redirect(url_for('dashboard'))


@app.route("/dashboard")
def dashboard():
    high = db.threats.count_documents({'threat_level': 'High'})
    medium = db.threats.count_documents({'threat_level': 'Medium'})
    low = db.threats.count_documents({'threat_level': 'Low'})
    results = list(db.threats.find().sort("timestamp", -1).limit(5))

    return render_template("dashboard.html",
                           high_count=high,
                           medium_count=medium,
                           low_count=low,
                           results=results)


@app.route("/lookup", methods=["POST"])
def lookup():
    ioc_input = request.form.get("ioc", "")
    ioc_list = [x.strip() for x in ioc_input.split(",") if x.strip()]

    results = {}
    for ioc in ioc_list:
        result_data = lookup_ioc_data(ioc)
        results[ioc] = result_data

    return render_template("result.html", results=results, current_year=datetime.now().year)


@app.route("/threat-trend.png")
def threat_trend():
    today = datetime.utcnow()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    date_labels = [d.strftime('%b %d') for d in days]
    counts = []

    for day in days:
        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)
        count = db.threats.count_documents({"timestamp": {"$gte": start, "$lt": end}})
        counts.append(count)

    plt.figure(figsize=(6, 3))
    plt.plot(date_labels, counts, marker='o', color='skyblue')
    plt.title("IOC Submissions (Last 7 Days)")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route("/trends")
def trends():
    trend_data = {}
    today = datetime.utcnow()
    for i in range(7):
        day = today - timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)
        trend_data[date_str] = db.threats.count_documents({"timestamp": {"$gte": start, "$lt": end}})

    generate_threat_trend_chart(trend_data, save_path="static/images/threat_trend.png")
    return render_template("trends.html", current_year=datetime.now().year)


# ---------- RUN ----------
if __name__ == "__main__":
    os.makedirs("static/images", exist_ok=True)
    app.run(debug=True)
