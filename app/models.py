import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class FishRecord(db.Model):
    __tablename__ = 'fish_records'
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    photo_path = db.Column(db.String(255), nullable=False, default='default.jpg')
    fish_name = db.Column(db.String(255), nullable=False, default='無銘の魚')
    length = db.Column(db.Float, nullable=False, default=999999)
    location = db.Column(db.String(255), nullable=False, default='NoData')
    date = db.Column(db.Date, nullable=False, default=date(1, 1, 1))
    memo = db.Column(db.String(255), nullable=False, default='NoData')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    __table_args__ = (
        db.CheckConstraint('length > 0', name='check_length_positive'),
    )

    def is_default_date(self):
        return self.date == date(1, 1, 1)
    
class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class FishRecordTag(db.Model):
    __tablename__ = 'fish_record_tags'
    record_id = db.Column(db.Integer, db.ForeignKey('fish_records.record_id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())