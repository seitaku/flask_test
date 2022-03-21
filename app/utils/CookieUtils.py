from datetime import datetime, timedelta
from flask import Flask, make_response, render_template, request, Response
import time

# 1.設定Cookie
def set_cookie(resp : any, cookie_name : str, value : str, expires :int = None):
    try :
        if expires is not None :
            expire_date = datetime.now()
            expire_date = expire_date + timedelta(hours = expires)
        else:
            expire_date = time.time() + time.time()

        resp = make_response(resp)
        resp.set_cookie(key = cookie_name, value = value, expires = expire_date)
    except Exception as e :
        print('set cookie err: ', e)
    
    return resp

def get_cookie(req : any, cookie_name : str):
    try:
        val = req.cookies.get(key = cookie_name)
    except Exception as e:
        print('get cookie err: ', e)
    return val

def del_cookie(resp : any, cookie_name : str):
    try:
        resp.set_cookie(key=cookie_name, expires=0)
    except Exception as e:
        print('del cookie err: ', e)
    return resp

# # 1.設定Cookie
# @app.route("/set")
# def setcookie():
#     resp = make_response('Setting cookie!')
#     resp.set_cookie(key='framework', value='flask', expires=time.time()+6*60)
#     return resp

# # 2.取得Cookie
# @app.route("/get")
# def getcookie():
#     framework = request.cookies.get('framework')
#     return 'The framework is ' + framework

# # 3.刪除Cookie
# @app.route('/del')
# def del_cookie():
#     res = Response('delete cookies')
#     res.set_cookie(key='framework', value='', expires=0)
#     return res