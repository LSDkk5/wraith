from flask import render_template, Blueprint

from web import app
from models import User
 
@app.route('/')
def login():
    return render_template('index.html')