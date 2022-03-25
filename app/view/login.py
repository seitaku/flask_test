from email.mime import application
import json
import traceback
import app.utils.EncryptUtils as EncryptUtils
import app.utils.CookieUtils as ck
from flask import Blueprint, abort, jsonify, render_template, request, flash, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token

app_login = Blueprint('app_login', __name__)

import logging
log = logging.getLogger(__name__)

@app_login.errorhandler(404)
def handle_404_error(err):
    print('err: ',err, type(err))
    return err

def __verifyPassword(account, password):
    # query account
    err_count = 4
    salt = ''
    org_key = ''
    if err_count >=5 :
        return False
    
    # if ( org_key != EncryptUtils.encryption_sha256(password, salt) ) :
    #     # insert login failed
    #     return False 
    return True
    

def __registerAccount(account, password):
    res = EncryptUtils.new_key_sha256(password)
    salt = res['salt']
    new_key = res['new_key']
    # save_account
    return True


# @app_login.route("/signUp", methods=['GET','POST'])
# def signUp():
#     flag = False
#     try:
#         print()
#         if (request.method == 'POST'):
#             print(request.get_data())

#             data = json.loads(request.get_data())
#             account = data['account']
#             password = data['password']
#             flag = __registerAccount(account, password)
#     except Exception as ex:
#         template = "An exception of type {0} occurred. Arguments:{1!r} \n"
#         message = template.format(type(ex).__name__, ex.args)
#         log.error('msg: ',message, traceback.format_exc())
#         return(f'db連線異常')
#     return render_template('sign_up.html', boolean = True)

@app_login.route("/signUp", methods=['GET','POST'])
def sign_up():
    flag = False
    try:
        print()
        if (request.method == 'POST'):
            print(request.form)
            data = request.form
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            # user = User.query.filter_by(email=email).first()
            # if user:
            #     flash('Email already exists.', category='error')
            if len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 6:
                flash('Password must be at least 6 characters.', category='error')
            else:
                # new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                #     password1, method='sha256'))
                # db.session.add(new_user)
                # db.session.commit()
                # login_user(new_user, remember=True)
                flash('Account created!', category='success')
                # return redirect(url_for('view.home'))
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:{1!r} \n"
        message = template.format(type(ex).__name__, ex.args)
        log.error('msg: ',message, traceback.format_exc())
        return(f'db連線異常')

    return render_template('sign_up.html', boolean = True)


# """
# from request
# """
@app_login.route("/login", methods=['GET','POST'])
def login():
    try:
        if (request.method == 'POST'):
            print(request.form)
            data = request.form

            # account = data['account']
            # password = data['password']
            # isSuccess = __verifyPassword(account, password)
            # print(isSuccess)
            # if not isSuccess:
            #     return jsonify({'code':999, 'msg':'登入失敗'})

            # access_token = create_access_token(identity=account)
            # return jsonify(access_token=access_token)
            print('ss')
            return render_template('qprd.html', tables={'code':0, 'msg':''})

            # return jsonify({'code':0, 'msg':''})
        
    except Exception as e:
        # log
        abort(404)
    
    userinfo = {
        'username': 'xx',
        'personalname': 'yy'
    }
    
    return render_template('login.html', text='test')

# @app_login.route("/login", methods=['GET','POST'])
# def login():
#     try:
#         if (request.method == 'POST'):
#             print(request.get_data())
#             data = json.loads(request.get_data())

#             account = data['account']
#             password = data['password']
#             isSuccess = __verifyPassword(account, password)
#             print(isSuccess)
#             if not isSuccess:
#                 return jsonify({'code':999, 'msg':'登入失敗'})

#             access_token = create_access_token(identity=account)
#             # return jsonify(access_token=access_token)
#             print('ss')
#             return render_template('qprd.html', tables={'code':0, 'msg':''})

#             # return jsonify({'code':0, 'msg':''})
        
#     except Exception as e:
#         # log
#         abort(404)
    
#     userinfo = {
#         'username': 'xx',
#         'personalname': 'yy'
#     }
    
#     return render_template('login.html', text='test')

@app_login.route("/")
def home():
    return render_template('home.html')

@app_login.route("/logout", methods=['GET'])
def logout():
    try:
        return render_template('login.html', tables={'code':0, 'msg':''})

    except Exception as e:
        # log
        abort(404)
    
    return render_template('index.html')
    # return "Hello World!"

