
from flask import render_template, send_from_directory
from werkzeug import secure_filename

from aptremake import app
from apt import test

@app.route("/", methods=["GET", "POST"])
def recommendations():
    design = test()
    return render_template("index.html", design=design)

@app.route("/data/<path:filename>")
def data(filename):
    return send_from_directory("data", filename) 


    
