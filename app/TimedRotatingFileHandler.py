import os
import logging
import logging.config
from datetime import datetime
try:
    import codecs
except ImportError:
    codecs = None
 
 
class TimedRotatingFileHandler(logging.FileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False):
        # 日誌文件日期後綴
        when_map = {'S': '%Y-%m-%d_%H-%M-%S', 'M': '%Y-%m-%d_%H-%M', 'H': '%Y-%m-%d_%H', 'D': '%Y-%m-%d'}
        time_suffix = when_map.get(when.upper())
        if not time_suffix:
            raise ValueError('Error params when: %s' % when)
 
        self.backupCount = backupCount
        interval_map = {'S': 1, 'M': 60, 'H': 3600, 'D': 3600 * 24}
        self.interval = interval_map[when.upper()] * interval
        self.file_formater = '%s.%s' % (filename, time_suffix)  # 拼接日誌文件路徑格式化字符串
        self.filename = datetime.now().strftime(self.file_formater)  # 使用當前時間生成日誌文件路徑
        self.file_time = datetime.strptime(self.filename, self.file_formater)  # 生成當前日誌文件對應的時間戳
        self.log_dir = os.path.dirname(os.path.abspath(self.filename))  # 獲得日誌文件夾路徑
        if not os.path.exists(self.log_dir):  # 如果日誌文件夾不存在，則創建文件夾
            os.makedirs(self.log_dir)
 
        if codecs is None:
            encoding = None
        super(TimedRotatingFileHandler, self).__init__(self.filename, 'a+', encoding, delay)  # 沒有加鎖，必須使用a+模式打開
        self.delete_expire_files()  # 刷新日誌文件
 
    def should_change_file2_write(self, record):
        record_time = datetime.fromtimestamp(record.created)
        if (record_time - self.file_time).total_seconds() >= self.interval:  # 如果當前時間超過指定步長
            self.filename = record_time.strftime(self.file_formater)  # 更新到最新的日誌文件名
            self.file_time = datetime.strptime(self.filename, self.file_formater)
            return True
        return False
 
    def do_change_file(self):
        self.baseFilename = os.path.abspath(self.filename)  # 日誌文件的絕對路徑
        if self.stream:  # stream is not None 表示OutStream中還有未輸出完的緩存數據
            self.stream.close()  # 將緩存寫入文件並關閉文件
            self.stream = None  # 關閉stream後必須重新設置stream為None，否則會造成對已關閉文件進行IO操作
        if not self.delay:
            self.stream = self._open()  # 打開新的日誌文件文件流
        self.delete_expire_files()  # 刪除多於保留個數的所有日誌文件
 
    def is_log_file(self, filename, file_match):
        try:
            if datetime.strptime(filename, file_match):
                return True
        except:
            pass
 
    def delete_expire_files(self):
        if self.backupCount <= 0:
            return
        file_match = os.path.basename(self.file_formater)
        result = [filename for filename in os.listdir(self.log_dir) if self.is_log_file(filename, file_match)]  # 提取出日誌文件名
        for s in sorted(result)[:-self.backupCount]:  # 刪除多於保留文件個數的日誌文件
            try:
                os.remove(os.path.join(self.log_dir, s))
            except:
                pass
 
    def emit(self, record):
        try:
            if self.should_change_file2_write(record):  # 判斷是否需要刪除舊文件增加新文件
                self.do_change_file()
            logging.FileHandler.emit(self, record)  # 寫入日誌內容
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)