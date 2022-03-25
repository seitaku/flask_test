

# db = SQLAlchemy()


# db.init_app(app)

# class User2(db.Model):
#     __tablename__ = 'user2'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(100), unique=True)
#     update_time = db.Column(db.Date, default=datetime.utcnow)

# class UUser(db.Model):
#     __tablename__ = 'u_user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))

# @app.route('/create_db')
# def index():
#     return 'ok'

# @app.route('/favicon.ico') 
# def favicon(): 
#     print('path:', os.path.join(app.root_path, 'static'))
#     return send_from_directory(os.path.join(app.root_path, 'static/image'), 'favicon2.ico'
#         , mimetype='image/vnd.microsoft.icon')

# @app.route("/printOrder")
# def printOrder():
#     html = render_template('print_proforma_invoice.html')
#     return html

import datetime
import os
from dotenv import load_dotenv
from flask import request, redirect

# load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)


# 切換環境
from app import create_app
app = create_app('dev')

# 不驗證 token 的 api
pass_api=[
    '/',
    '/login',
    '/creat_token',
    '/creat_token_c'
]

@app.before_request
def log_request():
    if request.path.startswith('/static'):
        return None

    app.logger.info( f'request path = {request.path}' )
    # for api in pass_api:
    #     if request.path == api:
    #         return None
    # print('\n\n')
    # print(request.cookies)
    return None
    # if 'Authorization' not in request.headers:
    #     app.logger.info('no token, redircet to /')
    #     return redirect('/')
    
@app.after_request
def process_response(response):
    try:
        if not request.path.startswith('/static'):
            ip = request.remote_addr
            url = request.path
            app.logger.info( f'ip:[{ip}] 訪問 url:[{url}] 成功' )
    except Exception as e:
        app.logger.error( f'ip:[{ip}] 訪問 url:[{url}] 失敗 {e}' )
    
    return response


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt
)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5000)