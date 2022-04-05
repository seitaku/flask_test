from asyncio.windows_events import NULL
import json
import traceback

from app.models import MLeftMenu, UUser, UUserLevel, UUserRolo
from flask import Blueprint, jsonify, request, flash, abort, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import or_, and_, join, outerjoin
from app.utils.JsonUtils import AlchemyEncoder

app_auth = Blueprint('app_auth', __name__)

import logging
log = logging.getLogger(__name__)


@app_auth.route("/")
@app_auth.route("/q", methods=['GET','POST'])
def home():
    try:
        user_name = request.args.get('userName')
        auth = request.args.get('auth')
        status = request.args.get('status')

        if status is None:
            status= str(0)
        condition = {}
        condition['user_name']=user_name
        condition['auth']=auth
        condition['status']=status
        print('\n\ncondition:',condition)
        log.info('condition:', condition)
        
        user_list = queryData(condition) 
        rolo_list = queryRoloList()
        log.debug('user_list:', user_list)
        for user in user_list:
            print(user)
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)
    # End login post handler

    print('\n\nre condition :',condition)
    return render_template('auth.html', user_list=user_list, condition=condition, rolo_list=rolo_list)


@app_auth.route("/update", methods=['GET','POST'])
def update():
    cb = request.form.getlist('user_checkbox')
    print('\n\ncb:',cb)
    if request.method == 'POST':
        pass
        # return None
    print('\n\n:','in update')
    return redirect(url_for('app_auth.home'))


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

        userId = session['userInfo'].get('userId')
        user_name = condition['user_name']
        auth = condition['auth']
        status = condition['status']

        sql = f"""
                select u.id,u.email,u.user_name,u.status, ul.auth,ul.create_by  
                from u_user u left join u_user_level ul on u.id = ul.user_id
                where (ul.auth> (
                    SELECT u.auth FROm u_user_level u where id={userId}) or ul.auth is null)
            """

        if user_name is not None and len(user_name) > 0:
            sql += f' and u.user_name = \'{user_name}\''

        if auth is not None and len(auth) > 0:
            sql += f' and ul.auth = {int(auth)}'
        print('status:',status)
        if status is not None and len(status) > 0:
            sql += f' and u.status = {status}'
        
        sql +=';'

        print('sql:',sql)
        
        return db.engine.execute(sql).fetchall()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)


def queryRoloList():
    try:
        return UUserRolo.query.all()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)

