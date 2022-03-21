import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)

class BaseConfig:  # 基本配置
    # 設定 JWT 密鑰
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=14)

    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    SUPPORTED_LANGUAGES = ['zh', 'en']
    DEFAULT_LANGUAGE = 'zh'

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    # JWT_TOKEN_LOCATION = ['cookies']
    JWT_TOKEN_LOCATION = ['headers']
    # Set True When Production Env
    JWT_COOKIE_SECURE = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mssql://@127.0.0.1:1433/user?driver=SQL Server Native Client 11.0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('db')
    JSON_AS_ASCII = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    }


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("test.db")
    WTF_CSRF_ENABLED = False


config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
}