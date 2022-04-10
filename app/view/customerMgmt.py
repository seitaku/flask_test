from flask import Blueprint, abort, redirect, send_from_directory, jsonify, Response, url_for
from flask import Flask, render_template, session, request

import traceback
from app.models import CCustomerInfo
from app.utils.decorators import my_token_required
from app import db
from string_utils import is_full_string, is_integer
from sqlalchemy import asc, not_

app_customerMgmt = Blueprint('app_customerMgmt', __name__)

import logging
log = logging.getLogger(__name__)

# @app_customerMgmt.route("/", methods=['GET'])
# def home():
#     return render_template('cusMgmt.html')

@app_customerMgmt.route("/")
@app_customerMgmt.route("/q", methods=['GET'])
def query():
    try:
        cusCode = request.args.get('cusCode')
        shortName = request.args.get('shortName')
        # cusName = request.args.get('cusName')

        country = request.args.get('country')
        region = request.args.get('region')
        status = request.args.get('status')

        if status is None:
            status= str(0)
        condition = {}
        condition['code']=cusCode
        condition['short_name']=shortName
        # condition['name']=cusName
        condition['country']=country
        condition['region']=region
        condition['status']=status
        log.info('app_customerMgmt query condition:', condition)
        
        cus_list =[]
        if request.path.endswith('/q'):
            cus_list = queryData(condition)

        country_list = __to_list(query_country_list())
        region_list = __to_list(query_region_list())

        # rolo_list = queryRoloList()
        # log.debug('user_list:', user_list)
        for cus in cus_list:
            print(vars(cus))
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)
    # End login post handler

    print('\n\nre condition :',condition)
    return render_template('cusMgmt.html'
        , cus_list=cus_list
        , condition=condition
        , country_list=country_list
        , region_list=region_list)

def queryData(condition):
    try:
        # subq = db.session.query(UUserLevel.auth).filter_by(user_id = userId).subquery()
        
        # auth 1-10 高-低
        # mainq = db.session.query(UUser.id, UUser.user_name, UUser.email, UUser.status, UUserLevel.create_by, UUserLevel.auth
        # ).outerjoin(UUserLevel, UUserLevel.user_id == UUser.id 
        # ).filter( and_( 
        # (or_( UUserLevel.auth > subq , UUserLevel.auth == None) )
        # , UUser.status == status ) )
        # user_list = sql.all()

        cus_code = condition['code']
        cus_short_name = condition['short_name']
        # cus_name = condition['name']
        country = condition['country']
        region = condition['region']
        status = condition['status']

        sql = CCustomerInfo.query
        print('\n\ncondition:',condition)
        if is_full_string(cus_code):
            sql = sql.filter_by(code=cus_code)
        
        if is_full_string(cus_short_name):
            sql = sql.filter(CCustomerInfo.short_name.like( f'%{cus_short_name}%' ) )
        
        # if is_full_string(cus_name):
        #     sql = sql.filter_by(name=cus_name)
        
        if is_full_string(country):
            sql = sql.filter_by(country=country)
        
        if is_full_string(region):
            sql = sql.filter_by(region=region)

        if is_integer(status):
            sql = sql.filter_by(status=status)
        
        print('\n\nsql:',sql)
        
        return sql.all()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)


def query_country_list():
    try:
        return db.session.query(CCustomerInfo.country).\
            filter( not_( CCustomerInfo.country==None ) ).\
            distinct().\
            order_by(asc(CCustomerInfo.country)).\
            all()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)

def query_region_list():
    try:
        return CCustomerInfo.query.with_entities(CCustomerInfo.region).\
            filter( not_(CCustomerInfo.region == None)).\
            group_by(CCustomerInfo.region).\
            all()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)

def __to_list(obj):
    list = []
    for row in obj:
        list.append(row[0])
    return list