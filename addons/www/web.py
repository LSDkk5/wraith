from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from forms.LoginForm import LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
db = SQLAlchemy(app)

@app.route('/')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)    