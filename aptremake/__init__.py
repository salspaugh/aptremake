
import sqlite3

from flask import Flask, g

DATABASE = "aptremake.db"
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "default"
UPLOAD_FOLDER = "uploads"

METADATA = "metadata/cars.json" 

app = Flask(__name__)
app.config.from_object(__name__)

import aptremake.views

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def set_metadata(path):
    global METADATA
    metadata = path
