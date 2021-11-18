from flask_login import UserMixin
from ..import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(50), unique=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(200))
