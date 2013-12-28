
from flask import render_template, send_from_directory, request
from werkzeug import secure_filename

from aptremake import app
from apt import test, generate_presentation
from metadata import read_data

import json

CARS = "/Users/salspaugh/classes/visualization/project/aptremake/specs/json/cars.spec"

@app.route("/", methods=["GET", "POST"])
def design():
    relations = read_data(CARS)
    design, selection_data = test()
    if request.method == "POST":
        selection_data = json.loads(request.form["relations"])
        apt_input = sorted(selection_data, key=lambda x: int(x["importance"]))
        apt_input = [relations[s["name"]] for s in apt_input]
        design = generate_presentation(apt_input)
    for s in selection_data:
        relations[s["name"]].selected = True
        relations[s["name"]].importance = s["importance"]
    button_data = [{"name": r.name, "selected": r.selected, "importance": r.importance} for r in relations.values()]
    button_data.sort(key=lambda x: len(x["name"]))
    return render_template("index.html", design=design, buttons=button_data)

@app.route("/data/<path:filename>")
def data(filename):
    return send_from_directory("data", filename) 


    
