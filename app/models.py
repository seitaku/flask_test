from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    note_content = db.Column(db.String(10000))
    modify_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('u_user.id'))


class UUser(db.Model, UserMixin):
    __tablename__ = 'u_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    user_name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    status = db.Column(db.SmallInteger)
    create_by = db.Column(db.String(20))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note')
    levels = db.relationship('UUserLevel')
    