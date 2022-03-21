# -*- coding: utf-8 -*-

import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from flask.logging import default_handler
import os

from logging.handlers import RotatingFileHandler
from logging import handlers
from logging import StreamHandler


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, 'logs')

LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
LOG_PATH_ALL = os.path.join(LOG_PATH, 'all.log')

# 日誌檔案最大 100MB
# LOG_FILE_MAX_BYTES = 500 * 1024 * 1024
LOG_FILE_MAX_BYTES = 100 * 1024
# 輪轉數量是 10 個
LOG_FILE_BACKUP_COUNT = 10



class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    # def __init__(self, filename='tt.log', level='info', when='M', backCount=3,
    #              fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
    #     self.logger = logging.getLogger(filename)
    #     format_str = logging.Formatter(fmt)  # 設定日誌格式
    #     self.logger.setLevel(self.level_relations.get(level))  # 設定日誌級別

    #     # 向控制檯輸出日誌
    #     stream_handler = logging.StreamHandler()
    #     stream_handler.setFormatter(format_str)
    #     self.logger.addHandler(stream_handler)


    #     # 日誌按檔案大小寫入檔案
    #     # 1MB = 1024 * 1024 bytes
    #     # 這裡設定檔案的大小為500MB
    #     # rotating_file_handler = handlers.RotatingFileHandler(
    #     #     filename=filename, mode='a', maxBytes=1024 * 1024 * 500, backupCount=3, encoding='utf-8')
    #     # rotating_file_handler.setFormatter(format_str)
    #     # self.logger.addHandler(rotating_file_handler)

    #     # 往檔案裡寫入
    #     # 指定間隔時間自動生成檔案的處理器
    #     timed_rotating_file_handler = handlers.TimedRotatingFileHandler(
    #         filename=filename, when=when, backupCount=backCount, encoding='utf-8'
    #         , delay=False, utc=True)

    #     # 例項化TimedRotatingFileHandler
    #     # interval是時間間隔，backupCount是備份檔案的個數，如果超過這個個數，就會自動刪除，when是間隔的時間單位，單位有以下幾種：
    #     # S 秒
    #     # M 分
    #     # H 小時、
    #     # D 天、
    #     # W 每星期（interval==0時代表星期一）
    #     # midnight 每天凌晨
    #     timed_rotating_file_handler.setFormatter(format_str)  # 設定檔案裡寫入的格式
    #     self.logger.addHandler(timed_rotating_file_handler)

    #     # 往螢幕上輸出
    #     stream_handler = logging.StreamHandler()
    #     stream_handler.setFormatter(format_str)
    #     self.logger.addHandler(stream_handler)


    def init_app(self, app):
        # 移除預設的handler
        app.logger.removeHandler(default_handler)

        formatter = logging.Formatter(
            '%(asctime)s [%(thread)d:%(threadName)s] [%(filename)s:%(module)s:%(funcName)s] '
            '[%(levelname)s]: %(message)s'
        )
        # filename='tt.log'
        # when='M'
        # backCount=10
        # # 往檔案裡寫入
        # # 指定間隔時間自動生成檔案的處理器
        # timed_rotating_file_handler = handlers.TimedRotatingFileHandler(
        #     filename=filename, when=when, backupCount=backCount, encoding='utf-8'
        #     , delay=False, utc=True)

        # # 例項化TimedRotatingFileHandler
        # # interval是時間間隔，backupCount是備份檔案的個數，如果超過這個個數，就會自動刪除，when是間隔的時間單位，單位有以下幾種：
        # # S 秒
        # # M 分
        # # H 小時、
        # # D 天、
        # # W 每星期（interval==0時代表星期一）
        # # midnight 每天凌晨
        # timed_rotating_file_handler.setFormatter(formatter)  # 設定檔案裡寫入的格式
        # app.logger.addHandler(timed_rotating_file_handler)

        # 將日誌輸出到檔案
        # 1 MB = 1024 * 1024 bytes
        # 此處設定日誌檔案大小為500MB，超過500MB自動開始寫入新的日誌檔案，歷史檔案歸檔
        file_handler = ConcurrentRotatingFileHandler(
            filename=LOG_PATH_ALL,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # terminal
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        for logger in (
                # 這裡自己還可以新增更多的日誌模組，具體請參閱Flask官方文件
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')
        ):
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            
            


# log = Logger('all.log', level='info')
# log.logger.info('[測試log] hello, world')