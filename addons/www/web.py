from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from forms.LoginForm import LoginForm
from forms.AddServerForm import AddServerForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Server(db.Model):
    __tablename__ = 'server'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    adress = db.Column(db.String(16), index=True, unique=False)
    port = db.Column(db.String(6), index=True, unique=False)
    rcon_pass = db.Column(db.String(42))
    status = db.Column(db.Boolean, nullable=False, default=False)
    game = db.Column(db.String(42))

@app.route('/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('logged'))
        else:
            flash('Login Unsuccessful, Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logged', methods=['GET', 'POST'])
def logged():
   return render_template('index.html')

@app.route('/add_server', methods=['GET', 'POST'])
def add_server():
    print(request.form)
    return render_template('add_server.html')

@app.route('/edit_server/<id>', methods=['GET', 'POST'])
def edit_server(id):
   pass

@app.route('/remove_server/<id>', methods=['GET', 'POST'])
def remove_server(id):
   pass

if __name__ == "__main__":
    app.run(debug=True)    