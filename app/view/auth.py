from asyncio.windows_events import NULL
import json
import traceback

from app.models import MLeftMenu, UUser, UUserLevel
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
        print('\n\n')
        
        print(request.form)
        user_name = request.args.get('userName')
        auth = request.args.get('auth')
        status = request.args.get('status')
        if status is None :
            status = 0
        print(user_name,auth,status)
        



        userId= session['userInfo'].get('userId')
        
        subq = db.session.query(UUserLevel.auth).filter_by(user_id = userId).subquery()
        
        # auth 1-10 高-低
        mainq = db.session.query(UUser.id, UUser.user_name, UUser.email, UUser.status, UUserLevel.create_by, UUserLevel.auth
        ).outerjoin(UUserLevel, UUserLevel.user_id == UUser.id 
        ).filter( and_( 
        (or_( UUserLevel.auth > subq , UUserLevel.auth == None) )
        , UUser.status == status ) )
        print('mainq:',mainq)
        user_list = mainq.all()
        # print('user_list:',user_list)
        for user in user_list:
            print(user)
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)
    # End login post handler


    return render_template('auth.html', user_list=user_list,status = status)


@app_auth.route("/update", methods=['GET','POST'])
def update():
    cb = request.form.getlist('user_checkbox')
    print('\n\ncb:',cb)
    if request.method == 'POST':
        pass
        # return None
    print('\n\n:','in update')
    return redirect(url_for('app_auth.home'))

