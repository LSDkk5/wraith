from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin
from flask_bcrypt import Bcrypt

from forms.LoginForm import LoginForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

@app.route('/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(form.username.data, user.password):
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
        else:
            flash('Login Unsuccessful, Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)    