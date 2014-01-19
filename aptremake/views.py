
from flask import render_template, send_from_directory, request
from werkzeug import secure_filename

from aptremake import app
from apt import generate_presentation
from metadata import read_metadata
from test import construct_test_query

import json

CARS = "/Users/salspaugh/classes/visualization/project/aptremake/specs/json/cars.spec"

@app.route("/", methods=["GET", "POST"])
def design():
    metadata = read_metadata(CARS)
    db = metadata["database"]
    design = None
    button_data = [{"name": r.name, "selected": False, "importance": -1} for r in metadata["relations"].values()]
    if request.method == "POST":
        selection_data = json.loads(request.form["relations"])
        apt_input = sorted(selection_data, key=lambda x: int(x["importance"]))
        apt_input = [metadata["relations"][s["name"]] for s in apt_input]
        query = construct_test_query(apt_input) 
        if len(apt_input) == 1:
            r = apt_input[0]
            labels = ["APTREMAKEID"] + [r.determinant.name, r.dependent.name]
        else:    
            r = apt_input[0]
            labels = ["APTREMAKEID", r.determinant.name] + [r.dependent.name for r in apt_input]
        design = generate_presentation(db, apt_input, query, labels, limit=1).next()
        print query
        print labels
        print design
        for s in selection_data:
            metadata["relations"][s["name"]].selected = True
            metadata["relations"][s["name"]].importance = s["importance"]
        button_data = [{"name": r.name, "selected": r.selected, "importance": r.importance} for r in metadata["relations"].values()]
    button_data.sort(key=lambda x: len(x["name"]))
    return render_template("index.html", design=design, buttons=button_data)

@app.route("/data/<path:filename>")
def data(filename):
    return send_from_directory("data", filename) 


    
