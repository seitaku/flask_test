import traceback

from app.models import MLeftMenu, UUser, UUserLevel
from flask import Blueprint, jsonify, request, flash, abort, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import or_

app_dashboard = Blueprint('app_dashboard', __name__)

import logging
log = logging.getLogger(__name__)

@app_dashboard.route("/left_menu", methods=['GET'])
def leftMenu():
    if request.method == 'POST':
        abort(404)
    
    try:
        se = session.get('userInfo')
        print('\n\nse:',se)
        userId = se['userId']
        left_menu_str = UUserLevel.query.filter_by( user_id=userId ).first()
        print('\n\nleft_menu_str:',vars(left_menu_str), type(vars(left_menu_str)))

        left_menu_id = str(left_menu_str.leftMenu).split(',')
        print('\n\nleft_menu_list:',left_menu_id)
    
        left_menu_list = MLeftMenu.query.filter( MLeftMenu.id.in_( left_menu_id ) ).all()
        print('\n\nleft_menu_list:',left_menu_list)
        for i in left_menu_list:
            print(vars(i))
        

        # print('\n\nleft_menu_list:',vars(left_menu_list))
        # print('\n\nleft_menu_list:',jsonify(left_menu_list))

        # if left_menu:
        #     flash('Email or UserName already exists.', category='error')
        # else:
        #     flash('Account created!', category='success')
            
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        return(f'錯誤頁面')

    return render_template('home.html', left_menu_list=left_menu_list)

