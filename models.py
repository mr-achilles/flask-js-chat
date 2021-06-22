from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """ Model of chat user """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    hashed_pswd = db.Column(db.String(), nullable=False)

