import json
import traceback

from app.models import MLeftMenu, UUser, UUserLevel
from flask import Blueprint, jsonify, request, flash, abort, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import or_
from app.utils.JsonUtils import AlchemyEncoder

app_login = Blueprint('app_login', __name__)

import logging
log = logging.getLogger(__name__)

@app_login.route("/signUp", methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        try:
            print()
            if (request.method == 'POST'):
                print(request.form)
                email = request.form.get('email')
                user_name = request.form.get('userName')
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')

                user = UUser.query.filter( or_(UUser.email==email, UUser.user_name==user_name) ).filter_by(status=0).first()

                if user:
                    flash('Email or UserName already exists.', category='error')
                elif len(email) < 4:
                    flash('Email must be greater than 3 characters.', category='error')
                elif len(user_name) < 2:
                    flash('First name must be greater than 1 character.', category='error')
                elif password1 != password2:
                    flash('Passwords don\'t match.', category='error')
                elif len(password1) < 6:
                    flash('Password must be at least 6 characters.', category='error')
                else:
                    new_user = UUser(email=email, user_name=user_name, password=generate_password_hash(
                        password1, method='sha384'), status=0, create_by='system')
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Account created!', category='success')
                    return redirect(url_for('login'))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:{1!r} \n"
            message = template.format(type(ex).__name__, ex.args)
            log.error('msg: ',message, traceback.format_exc())
            return(f'錯誤頁面')
    # End sign_up post handler

    return render_template('sign_up.html')


# """
# from request
# """
@app_login.route("/")
@app_login.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try:
            print('\n\n')
            print(request.form)
            user_name = request.form.get('userName')
            password = request.form.get('password')

            user = UUser.query.filter_by(user_name=user_name).filter_by(status=0).first()
            if user:
                # if check_password_hash(user.password, password):
                if True:
                    flash('Logged in successfully!', category='success')
                    session['userInfo'] = {'userId':user.id,'role':1}

                    left_menu = leftMenu(user.id)
                    session['leftMenu'] = json.dumps(left_menu, cls=AlchemyEncoder)
                    return redirect(url_for('app_login.home'))
                else:
                    flash('Incorrect username or password, try again.', category='error')
            else:
                flash('Incorrect username or password, try again.', category='error')

            # access_token = create_access_token(identity=account)
            # return jsonify(access_token=access_token)

            # return jsonify({'code':0, 'msg':''})
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:{1!r} \n"
            message = template.format(type(ex).__name__, ex.args)
            log.error('msg: ',message, traceback.format_exc())
            abort(404)
    # End login post handler

    # 若存有正確session則導向登入後首頁
    se = session.get('userInfo')
    if se is not None:
        userId = se.get('userId')
        log.info(f'userId:[{userId}] logging in, redirect to home page')
        return redirect(url_for('app_login.home'))

    return render_template('login.html')

def leftMenu(userId):
    left_menu_list = {}
    left_menu_str = UUserLevel.query.filter_by( user_id=userId ).with_entities(UUserLevel.left_menu).first()[0]
    if left_menu_str is None:
        return left_menu_list
    log.info(f'userId:[{userId}] get leftMenu, menu_id_str:[{left_menu_list}]')

    left_menu_id = str(left_menu_str).split(',')
    if left_menu_id is None:
        return left_menu_list
    
    if 'all' in left_menu_id:
        left_menu_list = MLeftMenu.query.all()
    else:
        left_menu_list = MLeftMenu.query.filter( MLeftMenu.id.in_( left_menu_id ) ).all()
    
    return left_menu_list

@app_login.route("/home")
def home():
    se = session.get('userInfo')
    if se is None:
        return redirect(url_for('app_login.login'))

    return render_template('home.html')

@app_login.route("/logout", methods=['GET'])
def logout():
    try:
        session.clear()
        return redirect(url_for('app_login.login'))
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        abort(404)
