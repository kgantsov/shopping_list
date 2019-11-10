from app.db import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    email = db.Column(db.Unicode(), unique=True, index=True)
    password_hash = db.Column(db.Unicode())
