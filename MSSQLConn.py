# @app.route('/favicon.ico') 
# def favicon(): 
#     print('path:', os.path.join(app.root_path, 'static'))
#     return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon2.ico'
#         , mimetype='image/vnd.microsoft.icon')

import os
from dotenv import load_dotenv
from flask import flash, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

# change env ['dev', 'testing']
from app import create_app
# app = create_app('dev')
app = create_app('testing')

# skip check session list
pass_api=[
    '/',
    '/login',
    '/signUp',
    '/creat_token',
    '/creat_token_c'
]

@app.before_request
def log_request():
    # filter static source
    if request.path.startswith('/static'):
        return None

    app.logger.info( f'request path = [{request.path}] method = [{request.method}]' )
    # check api pass list
    for api in pass_api:
        if request.path == api:
            return None
    
    # print('\n\nsession:',session.get('userInfo') )
    se = session.get('userInfo')
    # check session 
    if se is False or se is None:
        if request.path != '/logout':
            flash('Please reLogin', category='relogin')
        return redirect(url_for('app_login.login'))
    
    return None
    # if 'Authorization' not in request.headers:
    #     app.logger.info('no token, redircet to /')
    #     return redirect('/')
    
@app.after_request
def process_response(response):
    try:
    # clear flashes data
        session.pop('_flashes', None)
        
        if not request.path.startswith('/static'):
            ip = request.remote_addr
            url = request.path
            app.logger.info( f'ip:[{ip}] 訪問 url:[{url}] 成功' )

    except Exception as e:
        app.logger.error( f'ip:[{ip}] 訪問 url:[{url}] 失敗 {e}' )
    
    return response

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()

@app.errorhandler(404)
def handle_404_error(err):
    print('\n\n\n EEEERRRRR錯誤')
    print('err: ',err, type(err))
    return err

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt
)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000)