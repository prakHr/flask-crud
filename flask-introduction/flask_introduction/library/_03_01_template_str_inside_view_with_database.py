"""Using Flask template engines.

In this example we're using Flask template engine (Jinja2) to simplify
the process to generate the resulting HTML.

**TODO**
In our previous example we had to do a lot of string handling to
create the <ul> with authors.
It's your turn to use the template engine to build the same result.
"""
from flask import Flask
from flask import render_template_string  # !Important
from database_extractor import ExtractorID,extractDatabase
import firebase_admin
from firebase_admin import *
from firebase_admin import firestore

app = Flask(__name__)


@app.route('/')
def hello_world():
    name = "Poe"
    html = """
        <html>
            <h1>Welcome to {{library_name}} library!</h1>
            <ul>
                {% for author in authors %}
                    <li>{{ author }}</li>
                {% endfor %}
            </ul>
        </html>
    """
    #authors_list = ["Alan Poe", "Jorge L. Borges", "Mark Twain","new Name"]
    # Using an <ul> tag add the authors using the template engine
    cred=credentials.Certificate("project1-a9674-firebase-adminsdk-ddztm-263a615578.json")
    db = extractDatabase(cred)
    users_collection = db.collection('users')
    authors_list=ExtractorID(users_collection)
    rendered_html = render_template_string(html, library_name=name,authors=authors_list)
    
    return rendered_html
