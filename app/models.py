import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class fish_records(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.LargeBinary)
    fish_name = db.Column(db.String(255))
    length = db.Column(db.Float)
    location = db.Column(db.String(255))
    date = db.Column(db.Date)
    memo = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
