# -*- coding: utf-8 -*-

import os
import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from flask.logging import default_handler
from logging import StreamHandler

from app.TimedRotatingFileHandler import TimedRotatingFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'logs')
LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
LOG_PATH_ALL = os.path.join(LOG_PATH, 'all.log')

# 1 MB = 1024 * 1024 bytes
# 此處設定日誌檔案大小為500MB，超過500MB自動開始寫入新的日誌檔案，歷史檔案歸檔
LOG_FILE_MAX_BYTES = 500 * 1024 * 1024
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

    def init_app(self, app):
        app.logger.removeHandler(default_handler) # 移除預設的handler

        formatter = logging.Formatter(
            '%(asctime)s [%(thread)d:%(threadName)s] [%(filename)s:%(module)s:%(funcName)s] '
            '[%(levelname)s]: %(message)s'
        )

        timed_rotating_file_handler = TimedRotatingFileHandler(
            filename=LOG_PATH_ALL, when='h', encoding='utf-8')

        timed_rotating_file_handler.setFormatter(formatter)  # 設定檔案裡寫入的格式
        

        # 將日誌輸出到檔案
        # file_handler = ConcurrentRotatingFileHandler(
        #     filename=LOG_PATH_ALL,
        #     mode='a',
        #     maxBytes=LOG_FILE_MAX_BYTES,
        #     backupCount=LOG_FILE_BACKUP_COUNT,
        #     encoding='utf-8'
        # )

        # file_handler.setFormatter(formatter)
        # file_handler.setLevel(logging.INFO)

        # terminal log
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        for logger in (
                # 這裡自己還可以新增更多的日誌模組，具體請參閱Flask官方文件
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')
        ):
            logger.addHandler(stream_handler) # terminal log
            # logger.addHandler(file_handler) # size split log
            logger.addHandler(timed_rotating_file_handler) # time split log
            