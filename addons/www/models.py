from flask_login import UserMixin

from web import login_manager
from web import db


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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