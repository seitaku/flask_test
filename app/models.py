from flask import jsonify
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    note_content = db.Column(db.String(255))
    modify_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('u_user.id'))


class UUser(db.Model):
    __tablename__ = 'u_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(50), unique=True)
    user_name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    status = db.Column(db.SmallInteger) #0啟用 1暫停
    create_by = db.Column(db.String(20))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note')
    levels = db.relationship('UUserLevel')


class UUserLevel(db.Model):
    __tablename__ = 'u_user_level'
    id= db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('u_user.id'), unique=True)
    rolo_id = db.Column(db.SmallInteger, nullable=True)
    other = db.Column(db.String(50), nullable=True)
    left_menu = db.Column(db.String(50))
    create_by = db.Column(db.String(20))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class MLeftMenu(db.Model):
    __tablename__ = 'm_left_menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(10))
    path = db.Column(db.String(50))
    level = db.Column(db.SmallInteger)
    parent = db.Column(db.Integer)
    sorted = db.Column(db.Integer)

class UUserRolo(db.Model):
    __tablename__ = 'u_user_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    code = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(10))


class PProductInfo(db.Model):
    __tablename__ = 'p_product_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    customer_prd_code = db.Column(db.String(20), nullable=True)
    customer_prd_name = db.Column(db.String(50), nullable=True)
    customer_id = db.Column(db.Integer, nullable=True) 
    specification = db.Column(db.String(100)) # 規格
    quantity = db.Column(db.Integer)
    product_unit = db.Column(db.String(10))
    price = db.Column(db.Numeric(10,4))
    currency_unit = db.Column(db.String(10))
    status = db.Column(db.SmallInteger) # 0_顯示 1_關閉 2_停產 3...(自訂)
    create_by = db.Column(db.String(20))
    create_date = db.Column(db.DateTime(timezone=True))
    update_by = db.Column(db.String(20))
    update_date = db.Column(db.DateTime(timezone=True), default=func.now())

class CCustomerInfo(db.Model):
    __tablename__ = 'c_customer_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    short_name = db.Column(db.String(20))
    type = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    region = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    status = db.Column(db.SmallInteger, default=0) # 0_合作中 1_到期 2...(自訂)
    create_by = db.Column(db.String(20))
    create_date = db.Column(db.DateTime(timezone=True))
    update_by = db.Column(db.String(20))
    update_date = db.Column(db.DateTime(timezone=True), default=func.now())