# 引用 flask 內建函式
from os import path
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
# from flask_babel import Babel
from app.config.config import config
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
                                create_refresh_token, get_jwt_identity)
from .log import Logger

db = SQLAlchemy()
# babel = Babel()
jwt = JWTManager()
logger = Logger()

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])

    # app.config['JWT_SECRET_KEY'] = ''

    register_extensions(app)
    register_blueprints(app)

    from .models import UUser, Note
    create_mydb(app, config_name)
    # register_i18n(app)

    return app

def create_mydb(app, config_name):
    if not path.exists('app/database.db') and config_name != 'dev':
        db.create_all(app=app)
        print('Created DataBase!')
    else:
        print('DataBase Exists!')


def register_extensions(app):
    """Register extensions with the Flask application."""
    logger.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    from app.view.login import app_login
    app.register_blueprint(app_login, url_prefix='/')

    from app.view.qPage import app_qPage
    app.register_blueprint(app_qPage, url_prefix='/')


# def register_extensions(app):
#     """Register extensions with the Flask application."""
#     babel.init_app(app)
#     db.init_app(app)


# def register_i18n(app):
#     """Register i18n with the Flask application."""
#     defalut_language_str = app.config['DEFAULT_LANGUAGE']
#     support_language_list = app.config['SUPPORTED_LANGUAGES']

#     # 1 Get parameter lang_code from route
#     @app.url_value_preprocessor
#     def get_lang_code(endpoint, values):
#         if values is not None:
#             g.lang_code = values.pop('lang_code', defalut_language_str)

#     # 2 Check lang_code type is in config
#     @app.before_request
#     def ensure_lang_support():
#         lang_code = g.get('lang_code', None)
#         if lang_code and lang_code not in support_language_list:
#             g.lang_code = request.accept_languages.best_match(
#                 support_language_list)

#     # 3 Setting babel
#     # @babel.localeselector
#     # def get_locale():
#     #     return g.get('lang_code')

#     # 4 Check lang_code exist after step1 pop parameter of lang_code
#     @app.url_defaults
#     def set_language_code(endpoint, values):
#         if 'lang_code' in values or not g.lang_code:
#             return
#         if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
#             values['lang_code'] = g.lang_code