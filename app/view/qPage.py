import os
from unittest import result
from flask import Blueprint, abort, redirect, send_from_directory, jsonify, Response, url_for
from flask import Flask, render_template, session, request
import jwt
# from MSSQLConn import UUser
from app.utils.ParseExcel import ParseExcel as pe
from app.utils.ExcelReader import ExcelReader as er
# from MSSQLConn import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app_qPage = Blueprint('app_qPage', __name__)


@app_qPage.route("/qPage", methods=['GET'])
def qPage():
    return render_template('qprd.html')


@app_qPage.route("/q", methods=['GET'])
def query():
    orderId = request.args.get('orderId')
    name = request.args.get('name')
    print(f'log o={orderId} n={name}')

    if orderId is None:
        print(f'orderId is None')
    else:
        # result = UUser.query.filter((UUser.id==orderId)).all()
        result = {}
        for item in result:
            print('item id:'+str(item.id))
            print('item name:'+str(item.name))
    return 'query ok'


@app_qPage.route("/nq", methods=['GET'])
def nquery():
    cusCode = request.args.get('cusCode')
    prdName = request.args.get('prdName')
    print(f'log o={cusCode} n={prdName}')

    if cusCode is None:
        print(f'cusCode is None')
    else:
        sql = """
            select id, name from u_user
        """
        result = {}# db.engine.execute(sql).fetchall()

        for item in result:
            print('item id:'+str(item.id))
            print('item name:'+str(item.name))
    return 'nquery ok'



# from functools import wraps
# from flask_jwt_extended.view_decorators import _decode_jwt_from_request
# from flask_jwt_extended.exceptions import NoAuthorizationError
# def custom_validator(view_function):
#     @wraps(view_function)
#     def wrapper(*args, **kwargs):
#         jwt_data = _decode_jwt_from_request(request_type='access')
#         print( 'jjjjjjjjjj:', jwt_data )
#         # Do your custom validation here.
#         if (...):
#             authorized = True
#         else:
#             authorized = False

#         if not authorized:
#             raise NoAuthorizationError("Explanation goes here")

#         return view_function(*args, **kwargs)

#     return jwt_required(wrapper)

@app_qPage.route("/creat_token", methods=['GET'])
def create_token():
    print('in testToken')
    username = 'sei'
    access_token = create_jwt(username)
    # access_token = create_access_token(identity=username)
    print('token: ', access_token)
    return access_token
    

@app_qPage.route("/check_token", methods=['GET'])
@jwt_required()
def check_token():
    print('in testToken')
    print( request.headers['Authorization'] )
    current_user = get_jwt_identity()
    print ('current_user:', current_user)
    token = jsonify(logged_in_as=current_user)
    print('token: ', token)
    return 'y', 200

def create_jwt(name):
    access_token = create_access_token(identity=name)
    response = jsonify({
        'msg': 'ok',
        'access_token': access_token,
    })
    return response
