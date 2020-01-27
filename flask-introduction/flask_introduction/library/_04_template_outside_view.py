"""Moving the template code to a separate file.

Mixing Python code with HTML is ugly. Templates usually live in their own
location. By default, flask will look up for templates in a 'templates'
directory living in the same path as the application.

"""
from database_extractor import ExtractorID,extractDatabase
import firebase_admin
from firebase_admin import *
from firebase_admin import firestore

from flask import Flask
from flask import render_template  # !Important

app = Flask(__name__)


@app.route('/')
def hello_world():
    name = "Poe"
    cred=credentials.Certificate("project1-a9674-firebase-adminsdk-ddztm-263a615578.json")
    db = extractDatabase(cred)
    users_collection = db.collection('users')
    authors_list=ExtractorID(users_collection)
    
    #return render_template('index.html', library_name=name)
    return render_template('index.html',authors=authors_list)

@app.errorhandler(404)
def not_found(error):
    return (render_template('routing/404.html'),404)
