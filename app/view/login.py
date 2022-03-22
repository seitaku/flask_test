from flask import Blueprint, abort, jsonify, render_template, request
import json
import app.utils.EncryptUtils as EncryptUtils
import app.utils.CookieUtils as ck

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


@app_login.route("/register", methods=['POST'])
def register():
    flag = False
    try:
        if (request.method == 'POST'):
            print(request.get_data())
            data = json.loads(request.get_data())
            account = data['account']
            password = data['password']
            flag = __registerAccount(account, password)
    except Exception as e:
        return(f'db連線異常')
    return flag

@app_login.route("/")
@app_login.route("/login", methods=['POST'])
def login():
    try:
        if (request.method == 'POST'):
            print(request.get_data())
            data = json.loads(request.get_data())

            account = data['account']
            password = data['password']
            isSuccess = __verifyPassword(account, password)
            print(isSuccess)
            if not isSuccess:
                return jsonify({'code':999, 'msg':'登入失敗'})

            access_token = create_access_token(identity=account)
            # return jsonify(access_token=access_token)
            print('ss')
            return render_template('qprd.html', tables={'code':0, 'msg':''})

            # return jsonify({'code':0, 'msg':''})
        
    except Exception as e:
        # log
        abort(404)
    
    userinfo = {
        'username': 'xx',
        'personalname': 'yy',


    }
    return render_template('index.html')
    # return "Hello World!"
