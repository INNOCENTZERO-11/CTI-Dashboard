from flask import render_template
from db.mongo_handler import get_trend_data
from utils.graph_generator import generate_threat_trend_chart
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
@app.route("/trends")
def trends():
    data = get_trend_data()
    generate_threat_trend_chart(data)  # creates `static/images/threat_trend.png`
    return render_template("trends.html")
