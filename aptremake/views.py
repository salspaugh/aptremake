
from flask import render_template, send_from_directory, request
from werkzeug import secure_filename

from aptremake import app
from apt import test, generate_presentation
from data import read_data

import json

CARS = "/Users/salspaugh/classes/visualization/project/aptremake/data/cars.spec"
    

@app.route("/", methods=["GET", "POST"])
def design():
    relations = read_data(CARS)
    design, selected = test()
    if request.method == "POST":
        selected = json.loads(request.form["relations"])
        design = generate_presentation([relations[s] for s in selected])
    for (name, relation) in relations.iteritems():
        relation.selected = True if name in selected else False
    relations = [(r.name, r.selected) for r in relations.values()]
    relations.sort(key=lambda x: len(x[0]))
    return render_template("index.html", design=design, relations=relations)

@app.route("/data/<path:filename>")
def data(filename):
    return send_from_directory("data", filename) 


    
