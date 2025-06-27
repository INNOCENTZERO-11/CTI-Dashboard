from flask import request, render_template
from utils.vt_lookup import lookup_ioc  # your VirusTotal function
from db.mongo_handler import insert_ioc
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
@app.route("/check", methods=["POST"])
def check_ioc():
    ioc_value = request.form.get("ioc")
    result = lookup_ioc(ioc_value)

    if result:
        insert_ioc(result)  # Optional: Save to MongoDB
        return render_template("result.html", result=result)
    else:
        return render_template("result.html", result={"error": "IOC not found"})

@app.route("/check", methods=["POST"])
def check_ioc():
    ioc_value = request.form.get("ioc")  # This expects a form input with name="ioc"
    
    # Placeholder logic – replace with your actual VirusTotal lookup
    from utils.vt_lookup import lookup_ioc
    from db.mongo_handler import insert_ioc
    
    result = lookup_ioc(ioc_value)

    if result:
        insert_ioc(result)  # Optional: store in MongoDB
        return render_template("result.html", result=result)
    else:
        return render_template("result.html", result={"error": "No result found"})
