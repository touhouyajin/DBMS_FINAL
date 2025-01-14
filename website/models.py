from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Music(db.Model):
    id = db.Column(db.String(1000), primary_key=True)
    title = db.Column(db.String(10000))
    play_url = db.Column(db.String(10000))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
